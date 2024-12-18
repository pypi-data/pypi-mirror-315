import uuid
import time
import os
import sys
import grpc
from grpc._channel import _InactiveRpcError
from typing import List, Dict, Optional, Union
from pathlib import Path
import torch
from contextlib import contextmanager
from outerport.client._torch_extensions import get_device_uuid

from outerport.generated.model_services_pb2 import (
    LoadToRamRequest,
    UnloadFromRamRequest,
    LoadToGpuRequest,
    OffloadToRamRequest,
    LoadFromRamRequest,
    WriteToDiskRequest,
    TensorTransportRequestResponse,
    GetModelStatusesRequest,
    GetModelStatusesResponse,
    GetJobStatusesRequest,
    GetJobStatusesResponse,
    ModelState,
    ModelStatus,
    IpcTensorGroup,
    IpcTensorGroupList,
)

from outerport.generated.model_services_pb2_grpc import TensorTransportServiceStub
from outerport.client.mem import get_pinned_cuda_allocations
from outerport.client.utils import (
    parse_size_to_int,
    get_cpp_tensor_memory_layout_by_device_id,
    copy_tensor,
    hash_files,
    get_global_tensor_memory_layout,
    map_tensors_to_devices,
    map_tensors_to_shards,
    allocate_cuda_memory_for_devices,
    use_pinned_cuda_memory,
    get_ipc_gpu_memory_by_device_id,
    get_per_device_ipc_tensor_groups,
    construct_torch_tensors,
    DAEMON_PORT,
)


@contextmanager
def handle_grpc_connection():
    try:
        yield
    except _InactiveRpcError as e:
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            raise Exception(
                f"Failed to connect to the daemon. Please ensure the daemon is running on port {DAEMON_PORT}."
            )
        else:
            raise Exception(e.details())
    except grpc.RpcError as e:
        raise Exception(f"RPC connection error: {e}")


def create_tensor_transport_service_stub() -> TensorTransportServiceStub:
    """
    Creates a stub for the TensorTransportService.

    Returns:
        TensorTransportServiceStub: Stub for the TensorTransportService.
    """
    # Load address from env
    address = os.getenv("OUTERPORT_ADDRESS", "localhost")
    channel = grpc.insecure_channel(f"{address}:{DAEMON_PORT}")
    stub = TensorTransportServiceStub(channel)
    return stub


def get_model_statuses() -> Dict[str, ModelState]:
    """
    Gets the statuses of all models.

    Returns:
        Dict[str, str]: Dictionary of model statuses.
    """
    stub = create_tensor_transport_service_stub()

    get_model_statuses_request = GetModelStatusesRequest()
    with handle_grpc_connection():
        get_model_statuses_response: GetModelStatusesResponse = stub.GetModelStatuses(
            get_model_statuses_request
        )

    model_statuses: Dict[str, ModelState] = {
        key: value for key, value in get_model_statuses_response.map.items()
    }

    return model_statuses


def load_torch_tensors(
    model_files: List[Path],
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
    device: Optional[Union[int, str, torch.device]] = None,
    cache_id: Optional[str] = None,
    pinned_cuda_memory_by_device_id: Optional[Dict[int, int]] = None,
) -> Dict[str, torch.Tensor]:
    """
    Loads a model from a list of files into a torch tensor.

    Args:
        model_files (List[Path]): List of files to load.
        device_map (Optional[Union[str, Dict[str, Union[int, str, torch.device]]]]):
            Device map. Defaults to "auto".
        device (Optional[Union[int, str, torch.device]]): If provided,
            device_map is ignored. Defaults to None.
        cache_id (Optional[str]): Cache id. Defaults to None.
        cuda_allocation_ptrs (Optional[Dict[int, int]]): CUDA allocation pointers (device_id, ptr) to place the tensors in.
            Defaults to None.

    Returns:
        torch_tensors (Dict[str, torch.Tensor]): Dictionary of torch tensors.
    """
    start_time = time.perf_counter()
    assert isinstance(model_files, list), "model_files must be a list"
    # Add a fail safe for users who pass in strings instead of Path objects
    model_files = [Path(file).resolve() for file in model_files]
    if not all(file.exists() for file in model_files):
        raise FileNotFoundError(f"One or more files do not exist: {model_files}")
    if cache_id is None:
        model_hash = hash_files(model_files)
        cache_id = model_hash

    # this is where the tensors are placed in a single contiguous chunk of memory
    global_tensor_memory_layout = get_global_tensor_memory_layout(model_files)
    # this is where the tensors are placed on each GPU, as well as the memory requirements
    tensor_memory_layout_by_device_id, memory_requirements_by_device_id = (
        map_tensors_to_devices(global_tensor_memory_layout, device_map, device)
    )

    if pinned_cuda_memory_by_device_id is not None:
        # use shared cuda memory
        cuda_allocations_by_device_id = use_pinned_cuda_memory(
            memory_requirements_by_device_id, pinned_cuda_memory_by_device_id
        )
    else:
        for device_id, memory_requirements in memory_requirements_by_device_id.items():
            print(f"device_id: {device_id}, memory_requirements: {memory_requirements / 1024 ** 3} GB")
        # memory allocations and ipc handles are created for each GPU
        cuda_allocations_by_device_id = allocate_cuda_memory_for_devices(
            memory_requirements_by_device_id
        )

    ipc_gpu_memory_by_device_id = get_ipc_gpu_memory_by_device_id(
        cuda_allocations_by_device_id, memory_requirements_by_device_id
    )

    per_device_ipc_tensor_groups = {}
    for device_id, tensor_memory_layout in tensor_memory_layout_by_device_id.items():
        device_uuid = get_device_uuid(device_id)

        ipc_gpu_memory = ipc_gpu_memory_by_device_id[device_id]
        ipc_tensor_group = IpcTensorGroup(
            ipc_gpu_memory=ipc_gpu_memory, tensor_memory_layout=tensor_memory_layout
        )
        per_device_ipc_tensor_groups[device_uuid] = IpcTensorGroupList(
            list=[ipc_tensor_group]
        )

    stub = create_tensor_transport_service_stub()
    end_time = time.perf_counter()
    # print(f"preparing load to gpu request: {end_time - start_time}")

    load_to_gpu_request = LoadToGpuRequest(
        model_name=cache_id,
        model_files=[str(file) for file in model_files],
        per_device_ipc_tensor_groups=per_device_ipc_tensor_groups,
    )
    with handle_grpc_connection():
        load_to_gpu_response: TensorTransportRequestResponse = stub.LoadToGpu(
            load_to_gpu_request
        )
    if not load_to_gpu_response.success:
        raise Exception("Failed to load model to GPU")

    torch_tensors = construct_torch_tensors(
        tensor_memory_layout_by_device_id, cuda_allocations_by_device_id
    )

    return torch_tensors


def copy_torch_tensors(
    torch_tensors: Dict[str, torch.Tensor],
    pinned_cuda_memory_by_device_id: Dict[int, int],
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
    device: Optional[Union[int, str, torch.device]] = None,
) -> Dict[str, torch.Tensor]:
    """
    Copies the tensors to the pinned CUDA memory. TODO: support device map.
    """
    device_id = 0
    total_size = sum(tensor.nbytes for tensor in torch_tensors.values())
    pinned_cuda_allocations = get_pinned_cuda_allocations()
    for device_id, cuda_memory in pinned_cuda_memory_by_device_id.items():
        if cuda_memory not in pinned_cuda_allocations:
            raise Exception(f"Pinned CUDA allocation for device {device_id} not found")

        pinned_size, pinned_device_id = pinned_cuda_allocations[cuda_memory]

        if device_id != pinned_device_id:
            raise Exception(
                f"Pinned CUDA allocation for device {device_id} is on the wrong device: {pinned_device_id}"
            )
        if total_size > pinned_size:
            raise Exception(
                f"Pinned CUDA allocation for device {device_id} is too small, {pinned_size} < {total_size}"
            )

    running_address = pinned_cuda_memory_by_device_id[device_id]
    new_tensors = {}
    for name, tensor in torch_tensors.items():
        new_tensor = copy_tensor(tensor, device_id, running_address)
        running_address += tensor.nbytes
        new_tensors[name] = new_tensor

    return new_tensors


def load_to_ram(model_files: List[Path], cache_id: Optional[str] = None) -> None:
    """
    Loads a model to RAM.

    Args:
        model_files (List[Path]): List of files to load.
        cache_id (Optional[str]): Cache id. Defaults to None.
    """
    # Add a fail safe for users who pass in strings instead of Path objects
    model_files = [Path(file).resolve() for file in model_files]
    if cache_id is None:
        model_hash = hash_files(model_files)
        cache_id = model_hash

    stub = create_tensor_transport_service_stub()
    load_to_ram_request = LoadToRamRequest(
        model_name=cache_id, model_files=[str(file) for file in model_files]
    )
    with handle_grpc_connection():
        load_to_ram_response: TensorTransportRequestResponse = stub.LoadToRam(
            load_to_ram_request
        )
    if not load_to_ram_response.success:
        raise Exception("Failed to load model to RAM")


def unload_from_ram(
    model_files: Optional[List[Path]] = None, cache_id: Optional[str] = None
) -> None:
    """
    Unloads a model from RAM.

    If cache_id is None, model_files must be provided.

    Args:
        model_files (Optional[List[Path]]): List of files to unload. Defaults to None.
        cache_id (Optional[str]): Cache id. Defaults to None.
    """
    # Add a fail safe for users who pass in strings instead of Path objects
    if cache_id is None:
        if model_files is None:
            raise ValueError("model_files must be provided if cache_id is None")
        model_files = [Path(file).resolve() for file in model_files]
        model_hash = hash_files(model_files)
        cache_id = model_hash

    stub = create_tensor_transport_service_stub()
    unload_from_ram_request = UnloadFromRamRequest(
        model_name=cache_id,
    )
    with handle_grpc_connection():
        unload_from_ram_response = stub.UnloadFromRam.with_call(unload_from_ram_request)
    if not unload_from_ram_response.success:
        raise Exception("Failed to unload model from RAM")


def offload_to_ram(
    torch_tensors: Dict[str, torch.Tensor], cache_id: Optional[str] = None
) -> str:
    """
    Offloads a model to RAM.

    Args:
        torch_tensors (Dict[str, torch.Tensor]): Dictionary of torch tensors.
        cache_id (Optional[str]): Cache id. Defaults to None.

    Returns:
        str: Cache id.
    """
    if cache_id is None:
        cache_id = uuid.uuid4().hex  # Generate a random hex string

    per_device_ipc_tensor_groups = get_per_device_ipc_tensor_groups(torch_tensors)

    stub = create_tensor_transport_service_stub()
    offload_to_ram_request = OffloadToRamRequest(
        model_name=cache_id, per_device_ipc_tensor_groups=per_device_ipc_tensor_groups
    )
    with handle_grpc_connection():
        offload_to_ram_response: TensorTransportRequestResponse = stub.OffloadToRam(
            offload_to_ram_request
        )
    if not offload_to_ram_response.success:
        raise Exception("Failed to offload tensors to RAM")

    return cache_id


def load_from_ram(
    cache_id: str,
    torch_tensors: Optional[Dict[str, torch.Tensor]] = None,
    pinned_cuda_memory_by_device_id: Optional[Dict[int, int]] = None,
) -> Dict[str, torch.Tensor]:
    """
    Loads a model from RAM to GPU.

    Args:
        cache_id (str): The unique identifier for the model to load from RAM.
        pinned_cuda_allocations (Optional[Dict[int, int]]): Shared CUDA allocations to place the tensors in.
            Defaults to None.

    Returns:
        Dict[str, torch.Tensor]: Dictionary of torch tensors loaded onto GPU.
    """
    if torch_tensors is not None and pinned_cuda_memory_by_device_id is not None:
        raise ValueError(
            "Only one of torch_tensors or pinned_cuda_memory_by_device_id can be provided"
        )

    model_statuses = get_model_statuses()
    if cache_id not in model_statuses:
        raise Exception(f"Model {cache_id} not found")
    if model_statuses[cache_id].status != ModelStatus.RAM:
        raise Exception(f"Model {cache_id} is not loaded to RAM")

    tensor_memory_layout = model_statuses[cache_id].tensor_memory_layout
    tensor_memory_layout_by_device_id, memory_requirements_by_device_id = (
        map_tensors_to_devices(tensor_memory_layout, "auto")
    )

    if torch_tensors is not None:
        pass
    elif pinned_cuda_memory_by_device_id is not None:
        # use shared cuda memory
        cuda_allocations_by_device_id = use_pinned_cuda_memory(
            memory_requirements_by_device_id, pinned_cuda_memory_by_device_id
        )
    else:
        # memory allocations and ipc handles are created for each GPU
        cuda_allocations_by_device_id = allocate_cuda_memory_for_devices(
            memory_requirements_by_device_id
        )
    ipc_gpu_memory_by_device_id = get_ipc_gpu_memory_by_device_id(
        cuda_allocations_by_device_id, memory_requirements_by_device_id
    )

    per_device_ipc_tensor_groups = {}
    for device_id, tensor_memory_layout in tensor_memory_layout_by_device_id.items():
        device_uuid = get_device_uuid(device_id)

        ipc_gpu_memory = ipc_gpu_memory_by_device_id[device_id]
        ipc_tensor_group = IpcTensorGroup(
            ipc_gpu_memory=ipc_gpu_memory, tensor_memory_layout=tensor_memory_layout
        )
        per_device_ipc_tensor_groups[device_uuid] = IpcTensorGroupList(
            list=[ipc_tensor_group]
        )

    stub = create_tensor_transport_service_stub()
    end_time = time.perf_counter()
    # print(f"preparing load to gpu request: {end_time - start_time}")

    load_from_ram_request = LoadFromRamRequest(
        model_name=cache_id,
        per_device_ipc_tensor_groups=per_device_ipc_tensor_groups,
    )
    with handle_grpc_connection():
        load_from_ram_response: TensorTransportRequestResponse = stub.LoadFromRam(
            load_from_ram_request
        )
    if not load_from_ram_response.success:
        raise Exception("Failed to load model from RAM to GPU")

    if torch_tensors is not None:
        return torch_tensors
    else:
        torch_tensors = construct_torch_tensors(
            tensor_memory_layout_by_device_id, cuda_allocations_by_device_id
        )

    return torch_tensors


def write_to_disk(
    torch_tensors: Dict[str, torch.Tensor],
    path_prefix: Path,
    max_shard_size: Optional[Union[int, str]] = None,
    overwrite: bool = False,
    cache_id: Optional[str] = None,
) -> str:
    """
    Writes torch tensors to disk in safetensors format, with optional sharding.

    Args:
        torch_tensors (Dict[str, torch.Tensor]): Dictionary of tensors to write to disk.
        path_prefix (Path): Path prefix for the output files. For multiple shards,
            files will be named {prefix}_0.safetensors, {prefix}_1.safetensors, etc.
        max_shard_size (Optional[Union[int, str]]): Maximum size per shard in bytes.
            Can be specified as int or string (e.g., "2GB"). Defaults to None (no sharding).
        overwrite (bool): If True, overwrites existing files. Defaults to False.
        cache_id (Optional[str]): Unique identifier for the model. If None, a random
            UUID will be generated.

    Returns:
        str: The cache_id used for the operation.
    """
    if cache_id is None:
        cache_id = uuid.uuid4().hex  # Generate a random hex string

    if isinstance(max_shard_size, str):
        max_shard_size = parse_size_to_int(max_shard_size)
    elif max_shard_size is None:
        max_shard_size = sys.maxsize

    per_shard_tensor_memory_layout = map_tensors_to_shards(
        torch_tensors, max_shard_size
    )
    num_shards = len(per_shard_tensor_memory_layout)
    path_prefix = Path(path_prefix).resolve()
    file_paths = []
    for shard_index in range(num_shards):
        file_path = path_prefix.with_name(
            f"{path_prefix.stem}_{shard_index}.safetensors"
        )
        if file_path.exists():
            if not overwrite:
                raise FileExistsError(f"File {file_path} already exists")
            else:
                file_path.unlink()
        file_paths.append(file_path)

    per_device_ipc_tensor_groups = get_per_device_ipc_tensor_groups(torch_tensors)

    stub = create_tensor_transport_service_stub()
    write_to_disk_request = WriteToDiskRequest(
        model_name=cache_id,
        per_device_ipc_tensor_groups=per_device_ipc_tensor_groups,
        per_shard_tensor_memory_layout=per_shard_tensor_memory_layout,
        model_files=[str(file_path) for file_path in file_paths],
    )
    try:
        write_to_disk_response: TensorTransportRequestResponse = stub.WriteToDisk(
            write_to_disk_request
        )
    except grpc.RpcError as e:
        raise Exception(
            f"Failed to connect to the daemon. Please ensure the daemon is running on port {DAEMON_PORT}."
        )
    if not write_to_disk_response.success:
        raise Exception("Failed to begin writing to disk")

    return cache_id


def get_job_statuses() -> Dict[str, str]:
    """
    Gets the statuses of the async jobs.

    Returns:
        Dict[str, str]: Dictionary of job statuses.
    """

    stub = create_tensor_transport_service_stub()

    get_job_statuses_request = GetJobStatusesRequest()
    get_job_statuses_response: GetJobStatusesResponse = stub.GetJobStatuses(
        get_job_statuses_request
    )

    job_statuses: Dict[str, str] = {
        key: value for key, value in get_job_statuses_response.map.items()
    }

    return job_statuses
