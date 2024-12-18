from typing import Union, Dict, Optional, List
import torch
from accelerate.utils import set_module_tensor_to_device, find_tied_parameters
from outerport.client.utils import weak_ref_tensor
from torch import nn


def map_named_buffers_to_devices(
    model: nn.Module,
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
) -> None:
    """
    Maps the named buffers of a PyTorch model to specified devices.

    This function iterates through all named buffers in the model and moves them
    to the appropriate device based on the provided device_map.

    Args:
        model (nn.Module): The PyTorch model whose buffers need to be mapped.
        device_map (Union[str, Dict[str, Union[int, str, torch.device]]], optional):
            Specifies how to map model parts to devices. Defaults to 'auto'.
            If a string, it should be 'auto' (currently treated as 'cuda').
            If a dict, keys are module names and values are target devices.

    Note:
        This function allocates new memory for the buffers on the specified devices (usually small tensors).
    """

    for full_name, _ in model.named_buffers(recurse=True):
        # eg: "model.layers.0.self_attn.rotary_emb", "inv_freq"
        submodule_name, buffer_name = full_name.rsplit(".", 1)
        submodule = model.get_submodule(submodule_name)
        buffer = submodule._buffers[buffer_name]
        if buffer is None:
            continue
        if isinstance(device_map, dict):
            for group_name, device in device_map.items():
                # device_map doesn't always contain the full name, so we need to check for a prefix match
                if full_name.startswith(group_name):
                    device = device_map[full_name]
                    submodule._buffers[buffer_name] = buffer.to(device=device)
                    continue
        else:
            submodule._buffers[buffer_name] = buffer.to(device="cuda")


def map_tied_parameters(module: nn.Module, tied_parameters: List[List[str]]) -> None:
    """
    Maps the tied parameters of a PyTorch module to the appropriate devices.
    """

    model_state_dict = module.state_dict()
    for group in tied_parameters:
        reference_tensor = None
        # for each tied group, find a reference tensor that is not a meta tensor
        for name in group:
            if model_state_dict[name].device != torch.device("meta"):
                reference_tensor = model_state_dict[name]
        if reference_tensor is None:
            raise ValueError(
                f"No reference tensor found for the tied parameters group {group}"
            )
        # set all tensors in the group to the device of the reference tensor
        for name in group:
            if name != reference_tensor.name:
                set_module_tensor_to_device(
                    module, name, reference_tensor.device, reference_tensor
                )


def drain_weights(module: torch.nn.Module):
    """Drain weights from module, replacing them with meta tensors. Return a dictionary of weak tensors.

    Args:
        module: PyTorch module to drain weights from
    Returns:
        weak_refs: Dictionary mapping parameter/buffer names to their weak references
    """

    for name, param in module.named_parameters():
        if param is not None:
            module_name, param_name = name.rsplit(".", 1)
            submodule = module.get_submodule(module_name)
            empty_param = torch.nn.Parameter(
                torch.empty(param.shape, dtype=param.dtype, device="meta"),
                requires_grad=param.requires_grad,
            )
            setattr(submodule, param_name, empty_param)


def extract_weights(module: torch.nn.Module, drain=False) -> Dict[str, torch.Tensor]:
    """Extract state dict from module, optionally draining weights after extraction.

    Args:
        module: PyTorch module to extract weights from
        drain: If True, replace weights with meta tensors after extraction
    Returns:
        Module's state dict containing weights and buffers
    """
    state_dict = module.state_dict()
    if drain:
        drain_weights(module)

    return state_dict


def load_weights(module: torch.nn.Module, state_dict: Dict[str, torch.Tensor]) -> None:
    """Load state dict into module

    Args:
        module: PyTorch module to load weights into
        state_dict: State dict containing weights and buffers to load
    """

    for name, param in module.named_parameters():
        if name in state_dict:
            param.data = state_dict[name]

    tied_parameters = find_tied_parameters(module)
    map_tied_parameters(module, tied_parameters)
