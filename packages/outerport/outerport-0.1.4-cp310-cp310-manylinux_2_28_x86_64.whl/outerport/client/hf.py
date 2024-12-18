from typing import Union, Dict, Optional, List
from pathlib import Path
import torch
from torch import nn
from concurrent.futures import ThreadPoolExecutor, wait
from accelerate import init_empty_weights
from accelerate.utils import set_module_tensor_to_device, find_tied_parameters
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
import transformers  # required for constructing module from string
import diffusers
from diffusers.pipelines.auto_pipeline import AutoPipelineForText2Image
from outerport.client.apis import load_torch_tensors
from outerport.client.utils import copy_tensor
from outerport.client.nn import map_named_buffers_to_devices, map_tied_parameters


# TODO: (10/21/24, Allen): turn this into a HF compatible interface (like AutoModelForCausalLM.from_pretrained)
# Right this function looks for safetensors files within the provided path - it's missing looking into snapshots/ folder, etc.
def load_llm(
    path: Path,
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
) -> AutoModelForCausalLM:
    """
    Load a large language model from path containing safetensors files and config.json.

    Args:
        path (Path): Directory containing the model files.
        device_map (Union[str, Dict[str, Union[int, str, torch.device]]], optional):
            Specifies how to map model parts to devices. Defaults to 'auto'.

    Returns:
        model (AutoModelForCausalLM): Loaded and initialized language model.
    """

    safetensor_files = list(sorted(Path(path).glob("*.safetensors")))

    # load the model without initializing the weights - could take 0.4 secs for llama3.1 8b
    def load_empty_model():
        config = AutoConfig.from_pretrained(path)
        with init_empty_weights():
            model = AutoModelForCausalLM.from_config(config).to(config.torch_dtype)

        model.tie_weights()
        map_named_buffers_to_devices(model, device_map)

        # find all tied parameters
        tied_parameters = find_tied_parameters(model)

        return model, tied_parameters

    with ThreadPoolExecutor() as executor:
        state_dict_future = executor.submit(
            load_torch_tensors, safetensor_files, device_map
        )
        model_future = executor.submit(load_empty_model)

        (model, tied_parameters), state_dict = executor.map(
            lambda f: f.result(), [model_future, state_dict_future]
        )

    for name, tensor in state_dict.items():
        set_module_tensor_to_device(model, name, tensor.device, tensor)
    map_tied_parameters(model, tied_parameters)

    model.eval()

    return model


def _remove_typed_safetensors(files: List[Path]):
    """
    Remove typed safetensors files from the list, if an untyped version exists.

    Args:
        files (List[Path]): list of safetensors files to potentially remove typed versions of

    Returns:
        List[Path]: list of safetensors files to keep
    """
    file_names = set(file.name for file in files)
    filtered_files = []

    for file in files:
        should_skip = False
        for precision in ["fp16", "fp8"]:
            # Check both 'fp16.' and 'fp16' patterns
            for pattern in [f"{precision}.", precision, f".{precision}"]:
                if (
                    pattern in file.name
                    and file.name.replace(pattern, "") in file_names
                ):
                    should_skip = True
                    break
            if should_skip:
                break

        if not should_skip:
            filtered_files.append(file)

    return filtered_files


def load_pipeline(
    path: Path,
    dtype: torch.dtype = torch.float16,
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
):
    path = Path(path).resolve()
    config, _ = AutoPipelineForText2Image.load_config(path, return_unused_kwargs=True)

    component_safetensors_files = {}
    for component_name, _ in config.items():
        if component_name.startswith("_"):
            continue
        component_files = list((path / component_name).glob("*.safetensors"))
        if len(component_files) > 0:
            component_safetensors_files[component_name] = _remove_typed_safetensors(component_files)

    def load_empty_pipeline(config):
        pipeline_cls = getattr(diffusers, config["_class_name"])
        with init_empty_weights():
            components = {}
            for component_name, component_path in config.items():
                if component_name.startswith("_"):
                    continue
                module_name, class_name = component_path
                module = globals()[module_name]
                component_cls = getattr(module, class_name)

                if "tokenizer" in component_name:
                    component = AutoTokenizer.from_pretrained(path / component_name)
                elif module_name == "diffusers":
                    config = component_cls.load_config(
                        path / component_name
                    )
                    component = component_cls(**config)
                elif module_name == "transformers":
                    config = AutoConfig.from_pretrained(
                        path / component_name
                    )
                    component = component_cls(config=config)

                components[component_name] = component

                if hasattr(component, "tie_weights"):
                    component.tie_weights()  # type: ignore
                if isinstance(component, nn.Module):
                    map_named_buffers_to_devices(component, device_map)
            pipeline = pipeline_cls(**components)

        return pipeline

    with ThreadPoolExecutor() as executor:
        pipeline_future = executor.submit(load_empty_pipeline, config)

        component_state_dict_futures = {}
        for component_name, component_files in component_safetensors_files.items():
            component_state_dict_futures[component_name] = executor.submit(
                load_torch_tensors, component_files, device_map, cache_id=str(path / component_name)
            )

                # Wait for all futures to complete
        all_futures = [pipeline_future] + list(component_state_dict_futures.values())
        wait(all_futures)

        # Get results
        pipeline = pipeline_future.result()

        component_state_dicts = {}
        for component_name, state_dict_future in component_state_dict_futures.items():
            state_dict = state_dict_future.result()
            for name, tensor in state_dict.items():
                if tensor.dtype != dtype:
                    new_tensor = tensor.to(dtype, copy=False)
                    copied_tensor = copy_tensor(new_tensor, tensor.device, tensor.data_ptr())
                    print(f"copied_tensor: {copied_tensor.shape} {copied_tensor.dtype} {copied_tensor.device}")
                    state_dict[name] = copied_tensor

            component_state_dicts[component_name] = state_dict

    # For CUDA memory
    free, total = torch.cuda.mem_get_info()
    allocated = torch.cuda.memory_allocated()
    reserved = torch.cuda.memory_reserved()

    print(f"CUDA Memory:")
    print(f"Free: {free / 1024**3:.2f} GB")
    print(f"Total: {total / 1024**3:.2f} GB")
    print(f"Allocated: {allocated / 1024**3:.2f} GB")
    print(f"Reserved: {reserved / 1024**3:.2f} GB")

    for attr_name in dir(pipeline):
        try:
            attr = getattr(pipeline, attr_name)
        except:
            continue
        if isinstance(attr, nn.Module):
            component = attr
            component_name = attr_name

            if component_name in component_state_dicts:
                component.load_state_dict(component_state_dicts[component_name], strict=False, assign=True)
                tied_parameters = find_tied_parameters(component)
                map_tied_parameters(component, tied_parameters)
                component.eval()

    return pipeline
