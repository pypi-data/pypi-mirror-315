import torch
from typing import Dict, Tuple, Union
from torch.types import Device
import threading
from outerport.client.basics import get_device_id


# Global dictionary to track allocations: {ptr: (device_id, size_bytes)}
_cuda_allocations: Dict[int, Tuple[int, int]] = {}
_pinned_cuda_allocations: Dict[int, Tuple[int, int]] = {}
_allocation_lock = threading.Lock()


def create_pinned_cuda_allocations(size: int, device: Union[Device, int] = None) -> int:
    """Create pinned CUDA allocations from the global allocator."""

    ptr = torch.cuda.caching_allocator_alloc(size, device)
    device_id = get_device_id(device)

    with _allocation_lock:
        _pinned_cuda_allocations[ptr] = (size, device_id)
        _cuda_allocations[ptr] = (size, device_id)

    return ptr


def get_pinned_cuda_allocations() -> Dict[int, Tuple[int, int]]:
    """Get a shared CUDA allocation."""
    return _pinned_cuda_allocations


def allocate_cuda_memory(size: int, device: Union[Device, int] = None) -> int:
    """Allocate CUDA memory from the global allocator and track it."""

    ptr = torch.cuda.caching_allocator_alloc(size, device)
    device_id = get_device_id(device)

    with _allocation_lock:
        _cuda_allocations[ptr] = (size, device_id)

    return ptr


def free_cuda_memory(ptr: int) -> None:
    """Free CUDA memory allocated by `alloc_cuda_memory`."""
    with _allocation_lock:
        if ptr in _cuda_allocations:
            del _cuda_allocations[ptr]
            if ptr in _pinned_cuda_allocations:
                del _pinned_cuda_allocations[ptr]
            torch.cuda.caching_allocator_delete(ptr)


def get_allocation_status() -> Dict[str, Union[int, Dict[int, int]]]:
    """Returns current CUDA memory allocation status."""
    with _allocation_lock:
        total_allocated = sum(size for size, _ in _cuda_allocations.values())
        allocations_by_device = {}
        for _, (size, device_id) in _cuda_allocations.items():
            if device_id not in allocations_by_device:
                allocations_by_device[device_id] = 0
            allocations_by_device[device_id] += size

        return {
            "total_allocations": len(_cuda_allocations),
            "total_bytes_allocated": total_allocated,
            "allocations_by_device": allocations_by_device,
        }


def get_cuda_allocations() -> Dict[int, Tuple[int, int]]:
    """Returns current CUDA memory allocation status."""
    return _cuda_allocations
