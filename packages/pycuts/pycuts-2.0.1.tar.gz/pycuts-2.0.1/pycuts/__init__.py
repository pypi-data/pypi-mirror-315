"""
__init__.py
-----------
Initialize the pycuts library, making the main utilities easily accessible.
"""

from .pycuts import HuggingFaceUtils, TorchUtils, GradioUtils

# top-level attributes referencing various utility, 
# namespaces and their commonly used functionalities.
huggingface_utils = HuggingFaceUtils
torch_utils = TorchUtils
gradio_utils = GradioUtils
is_spaces_available = huggingface_utils.spaces.is_available
is_zero_gpu = huggingface_utils.spaces.is_zero_gpu
is_gpu_available = torch_utils.is_gpu_available
get_device = torch_utils.get_device

__all__ = [
    HuggingFaceUtils,
    TorchUtils,
    GradioUtils,
    huggingface_utils,
    torch_utils,
    is_spaces_available,
    is_zero_gpu,
    is_gpu_available,
    get_device,
]
