"""
pycuts.py
---------
pycuts is a small Python library that provides a collection 
of shortcut functions for common operations across various libraries.
"""

import os

class HuggingFaceUtils:
    """
    HuggingFaceUtils
    ----------------
    A namespace for utilities related to Hugging Face.

    This class contains tools to detect and interact with the Hugging Face
    environment, such as determining if the script is running within a
    Hugging Face Space or whether ZeroGPU hardware is being used.
    """

    class spaces:
        """
        spaces
        ------
        Provides utilities to check the environment of Hugging Face Spaces.
        """

        @staticmethod
        def is_available():
            """
            Checks if the current script is running on a Hugging Face Space.

            Returns:
                bool: True if running on Hugging Face Space, False otherwise.
            """
            return os.getenv("SPACE_ID") is not None

        @staticmethod
        def is_zero_gpu():
            """
            Checks if the current Hugging Face Space is using ZeroGPU hardware.

            Returns:
                bool: True if ZeroGPU hardware is being used, False otherwise.
            """
            return bool(os.getenv("SPACES_ZERO_GPU"))


class TorchUtils:
    """
    TorchUtils
    -----------
    A namespace for utilities related to PyTorch.

    This class includes tools to check the availability and functionality
    of GPU accelerators (CUDA or MPS) as well as utility functions to manage
    memory and set random seeds for reproducibility.
    """

    # Class-level attribute to store the imported torch module
    _torch = None

    @classmethod
    def _ensure_torch_imported(cls):
        """
        Ensures the `torch` module is imported and stored in the class-level attribute.
        """
        if cls._torch is None:
            try:
                import torch
            except ImportError:
                raise ImportError("Please install the Torch library.")
            cls._torch = torch

    @staticmethod
    def is_gpu_available():
        """
        Checks if any GPU-like accelerator (CUDA or MPS) is available.

        Returns:
            bool: `True` if a GPU-like accelerator is available, `False` otherwise.
        """
        TorchUtils._ensure_torch_imported()
        return (TorchUtils._torch.cuda.is_available() or 
                (hasattr(TorchUtils._torch.backends, "mps") and TorchUtils._torch.backends.mps.is_available()))

    @staticmethod
    def empty_cache():
        """
        Frees up unused GPU memory by clearing the cache on CUDA devices.
        (MPS currently does not offer an equivalent empty_cache operation.)
        """
        TorchUtils._ensure_torch_imported()
        if TorchUtils._torch.cuda.is_available():
            TorchUtils._torch.cuda.empty_cache()
        # If MPS becomes supported in future versions of PyTorch for empty_cache, add it here.

    @staticmethod
    def get_device():
        """
        Determines which GPU-like accelerator is being used (CUDA, MPS, or CPU).

        Returns:
            str: The name of the device backend ('cuda', 'mps', or 'cpu').
        """
        TorchUtils._ensure_torch_imported()
        if TorchUtils._torch.cuda.is_available():
            # NVIDIA GPUs using CUDA backend.
            return "cuda"
        elif hasattr(TorchUtils._torch.backends, "mps") and TorchUtils._torch.backends.mps.is_available():
            # Apple's Metal Performance Shaders (MPS) for macOS.
            return "mps"
        else:
            # Fallback to CPU
            return "cpu"

    @staticmethod
    def device_count():
        """
        Returns the number of devices available for the current GPU-like accelerator.

        Returns:
            int: The number of available devices (0 if no GPU-like accelerator is available).
        """
        TorchUtils._ensure_torch_imported()
        if TorchUtils._torch.cuda.is_available():
            # Return the number of GPUs available.
            return TorchUtils._torch.cuda.device_count()
        elif hasattr(TorchUtils._torch.backends, "mps") and TorchUtils._torch.backends.mps.is_available():
            # MPS generally represents a single GPU device on Apple silicon.
            return 1
        else:
            return 0

    @staticmethod
    def manual_seed(seed: int):
        """
        Sets the random seed for both CPU and GPU contexts (if available) for reproducibility.

        Args:
            seed (int): The seed value to set.
        """
        TorchUtils._ensure_torch_imported()
        TorchUtils._torch.manual_seed(seed)
        if TorchUtils._torch.cuda.is_available():
            TorchUtils._torch.cuda.manual_seed(seed)
        # For MPS, as of current PyTorch versions, torch.manual_seed also sets seed for MPS.

class GradioUtils:
    """
    GradioUtils
    ------------
    A namespace for utilities related to Gradio.
    """

    _gr = None

    @classmethod
    def _ensure_gradio_imported(cls):
        """
        Ensures the `gradio` module is imported and stored in the class-level attribute.
        """
        if cls._gr is None:
            try:
                import gradio as gr
            except ImportError:
                raise ImportError("Please install the Gradio library.")
            cls._gr = gr

    @staticmethod
    def dark_mode():
        """
        Automatically applies dark mode to a Gradio Blocks instance on load.
        """
        GradioUtils._ensure_gradio_imported()
        INIT_DARK_MODE_JS = """
        () => {
            if (!document.body.classList.contains('dark')) {
                document.body.classList.add('dark');
            }
        }
        """
        with GradioUtils._gr.Blocks() as blocks:
            blocks.load(None, None, None, js=INIT_DARK_MODE_JS)
        return blocks

    @staticmethod
    def light_mode():
        """
        Automatically applies light mode to a Gradio Blocks instance on load.
        """
        GradioUtils._ensure_gradio_imported()
        INIT_LIGHT_MODE_JS = """
        () => {
            if (document.body.classList.contains('dark')) {
                document.body.classList.remove('dark');
            }
        }
        """
        with GradioUtils._gr.Blocks() as blocks:
            blocks.load(None, None, None, js=INIT_LIGHT_MODE_JS)
        return blocks

    @staticmethod
    def system_mode():
        """
        Automatically applies the system's preferred color scheme (light or dark mode)
        to a Gradio Blocks instance on load.
        """
        GradioUtils._ensure_gradio_imported()
        INIT_SYSTEM_MODE_JS = """
        () => {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark && !document.body.classList.contains('dark')) {
                document.body.classList.add('dark');
            } else if (!prefersDark && document.body.classList.contains('dark')) {
                document.body.classList.remove('dark');
            }
        }
        """
        with GradioUtils._gr.Blocks() as blocks:
            blocks.load(None, None, None, js=INIT_SYSTEM_MODE_JS)
        return blocks


    @staticmethod
    def appearance(_mode: str):
        """
        Changes the appearance mode of a Gradio Blocks instance.

        Args:
            _mode (str): 'dark', 'light', or 'system'.
        Returns:
            The Blocks instance with the applied mode.
        """
        if _mode == "dark":
            return GradioUtils.dark_mode()
        elif _mode == "light":
            return GradioUtils.light_mode()
        elif _mode == "system":
            return GradioUtils.system_mode()
        else:
            raise ValueError(
                f"Invalid value: '{_mode}'. "
                "Please choose between 'dark', 'light' or 'system'."
            )
