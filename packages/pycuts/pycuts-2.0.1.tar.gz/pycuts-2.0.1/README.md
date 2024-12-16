# pycuts

**pycuts** is a small Python library that provides a collection of shortcut functions for common operations across various libraries like Hugging Face, PyTorch, and Gradio.

## Features

- **HuggingFaceUtils**: Detect if you're running inside a Hugging Face Space, and if ZeroGPU hardware is being used.
- **TorchUtils**: Quickly check if a GPU-like accelerator (CUDA or MPS) is available, free GPU memory, or set random seeds for reproducibility.
- **GradioUtils**: Easily toggle between dark, light, or system appearance modes for Gradio interfaces.

## Installation

```bash
pip install pycuts
```

Optionally, install with extra dependencies:

```bash
# With PyTorch
pip install "pycuts[torch]"

# With Gradio
pip install "pycuts[gradio]"
```

## Quick Start

```python
import pycuts

# Check Hugging Face Space availability
if pycuts.is_spaces_available:
    print("Running inside a Hugging Face Space!")

# Check if GPU is available
if pycuts.is_gpu_available:
    print(f"GPU available, using device: {pycuts.get_device}")
else:
    print("No GPU, using CPU")

# Change Gradio Blocks appearance mode (requires Gradio installed)
# e.g. pycuts.gradio_utils.appearance("dark")
```

## Function Descriptions

### HuggingFaceUtils

| Function            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `spaces.is_available()` | Checks if the current script is running on a Hugging Face Space.            |
| `spaces.is_zero_gpu()`   | Checks if the Hugging Face Space is using ZeroGPU hardware.                |

### TorchUtils

| Function            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `is_gpu_available()` | Checks if any GPU-like accelerator (CUDA or MPS) is available.             |
| `empty_cache()`      | Frees up unused GPU memory by clearing the cache on CUDA devices.           |
| `get_device()`       | Determines which GPU-like accelerator is being used (CUDA, MPS, or CPU).   |
| `device_count()`     | Returns the number of available GPU-like devices.                          |
| `manual_seed(seed)`  | Sets the random seed for CPU and GPU contexts for reproducibility.          |

### GradioUtils

| Function            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `dark_mode()`        | Applies dark mode to a Gradio Blocks instance on load.                     |
| `light_mode()`       | Applies light mode to a Gradio Blocks instance on load.                    |
| `system_mode()`      | Applies the system's preferred color scheme (light or dark) to Gradio Blocks. |
| `appearance(mode)`   | Changes the appearance mode of a Gradio Blocks instance (dark, light, system). |

## Project Structure

- `pycuts/__init__.py` - Makes the main utilities easily accessible.
- `pycuts/pycuts.py` - Contains the implementations of the utility classes and functions.

## License

This project is licensed under the [MIT License](LICENSE).

