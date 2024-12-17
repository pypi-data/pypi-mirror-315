"""Array module for unified CPU/GPU array operations.

This module provides a unified interface for array operations across CPU (NumPy)
and GPU (CuPy) backends, with automatic handling of device selection and memory
management.
"""

# pylint: disable=no-name-in-module,import-error,import-outside-toplevel, line-too-long
from typing import Any, Callable, Literal, Tuple, Union
import numpy as np
import scipy

from qubit_measurement_analysis.cython._compilation_utils import check_cython_compiled

# Device type definitions
DeviceType = Literal["cpu", "cuda"]
DEVICE_CPU = "cpu"
DEVICE_CUDA = "cuda"


class Transformations:
    """Container for array transformation operations.

    Holds references to various array transformation functions that can be executed
    on either CPU or GPU depending on the parent ArrayModule's device setting.
    """

    def __init__(self) -> None:
        # Basic arithmetic operations
        self.add: Callable = None
        self.sub: Callable = None
        self.mul: Callable = None
        self.div: Callable = None

        # Statistical operations
        self.mean: Callable = None
        self.mean_filter: Callable = None
        self.mean_convolve: Callable = None
        self.mean_centring: Callable = None
        self.normalize: Callable = None
        self.standardize: Callable = None

        # Signal processing
        self.demodulate: Callable = None
        self.whittaker_eilers_smoother: Callable = None


class ArrayModule:
    """Unified interface for CPU/GPU array operations.

    Provides a consistent interface for array operations that can be executed on either
    CPU (using NumPy) or GPU (using CuPy) with automatic device management.

    Args:
        device: Target device for computations ("cpu" or "cuda[:device_id]")
        use_cython: Whether to use Cython-optimized implementations when available
    """

    def __init__(
        self, device: Union[DeviceType, str] = DEVICE_CPU, use_cython: bool = False
    ):
        self.device = device.lower()
        self.use_cython = use_cython

        # Initialize backend libraries
        if self.device == DEVICE_CPU:
            self._init_cpu_backend()
        elif self.device.startswith(DEVICE_CUDA):
            self._init_cuda_backend()
        else:
            raise ValueError(f"Unsupported device: {self.device}")

        # Initialize SSPD functions
        self.sspd_cross_product, self.sspd_pairwise, self.sspd_self_cross_product = (
            self._get_sspd_module()
        )

        # Initialize transformations
        self.transformations = Transformations()
        self._get_transformations_module()

    def _init_cpu_backend(self) -> None:
        """Initialize CPU backend using NumPy and SciPy."""
        self.np = np
        self.scipy = scipy
        self.array_transport = self.asarray

    def _init_cuda_backend(self) -> None:
        """Initialize CUDA backend using CuPy."""
        if self.use_cython:
            raise ValueError("Cython optimization cannot be used with CUDA backend")

        import cupy as cp
        import cupyx.scipy

        self.np = cp
        self.scipy = cupyx.scipy
        self.array_transport = cp.asnumpy

        # Set CUDA device if specified
        device_id = int(self.device.split(":")[1]) if ":" in self.device else 0
        cp.cuda.Device(device_id).use()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to numpy module."""
        return getattr(self.np, name)

    def __repr__(self) -> str:
        """String representation of the ArrayModule."""
        return f"{self.device} array module with {self.np} as numpy and {self.scipy} as scipy"

    def free_all_blocks(self) -> None:
        """Free all memory blocks when using CUDA backend."""
        if self.device.startswith(DEVICE_CUDA):
            self.get_default_memory_pool().free_all_blocks()
            self.get_default_pinned_memory_pool().free_all_blocks()

    @property
    def dtype(self) -> Any:
        """Default dtype for array operations."""
        return self.complex64

    def _get_sspd_module(self) -> Tuple[Callable, ...]:
        """Load appropriate SSPD implementation based on device and optimization settings."""
        if self.device == DEVICE_CPU:
            if check_cython_compiled() and self.use_cython:
                from qubit_measurement_analysis.cython import _sspd as sspd
            else:
                from qubit_measurement_analysis import _sspd as sspd
        else:
            from qubit_measurement_analysis.cuda import sspd

        return sspd.cross_product, sspd.pairwise, sspd.self_cross_product

    def _get_transformations_module(self) -> None:
        """Load and initialize transformation functions based on device and optimization settings."""
        if check_cython_compiled() and self.use_cython:
            from qubit_measurement_analysis.cython._transformations_wrapper import (
                _add,
                _sub,
                _mul,
                _div,
                _mean,
                _mean_convolve,
                _mean_centring,
                _demodulate,
                _whittaker_eilers_smoother,
            )
        else:
            from qubit_measurement_analysis._transformations import (
                _add,
                _sub,
                _mul,
                _div,
                _mean,
                _mean_convolve,
                _mean_centring,
                _demodulate,
                _whittaker_eilers_smoother,
            )

        # Map transformation functions
        transform_map = {
            "add": _add,
            "sub": _sub,
            "mul": _mul,
            "div": _div,
            "mean": _mean,
            "mean_convolve": _mean_convolve,
            "mean_centring": _mean_centring,
            "demodulate": _demodulate,
            "whittaker_eilers_smoother": _whittaker_eilers_smoother,
        }

        # Apply transformations
        for name, func in transform_map.items():
            setattr(self.transformations, name, func)
