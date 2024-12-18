import ctypes
from typing import Union
import torch
from torch.types import Device

PyCapsule_New = ctypes.pythonapi.PyCapsule_New
PyCapsule_New.restype = ctypes.py_object


def get_cpp_cuda_ptr(cuda_memory_address: int) -> ctypes.py_object:
    # Convert int to c_void_p first, then create PyCapsule
    ptr = ctypes.c_void_p(cuda_memory_address)
    return PyCapsule_New(ptr, None, None)


def get_device_id(device: Union[int, str, Device]) -> int:
    """
    Gets the device id from a device.

    Args:
        device (Union[int, str, Device]): Device.

    Returns:
        int: Device id.
    """

    if device is None:
        device = torch.cuda.current_device()
    if isinstance(device, str):
        device = int(device)

    if isinstance(device, torch.device):
        device = device.index

    return device
