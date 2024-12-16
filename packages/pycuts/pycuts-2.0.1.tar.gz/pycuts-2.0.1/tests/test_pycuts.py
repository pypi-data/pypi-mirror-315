import os
import unittest
from pycuts import HuggingFaceUtils, TorchUtils, GradioUtils

class TestHuggingFaceUtils(unittest.TestCase):

    def test_is_available(self):
        os.environ["SPACE_ID"] = "test_space"
        self.assertTrue(HuggingFaceUtils.spaces.is_available())
        del os.environ["SPACE_ID"]
        self.assertFalse(HuggingFaceUtils.spaces.is_available())

    def test_is_zero_gpu(self):
        os.environ["SPACES_ZERO_GPU"] = "1"
        self.assertTrue(HuggingFaceUtils.spaces.is_zero_gpu())
        del os.environ["SPACES_ZERO_GPU"]
        self.assertFalse(HuggingFaceUtils.spaces.is_zero_gpu())


class TestTorchUtils(unittest.TestCase):

    def test_is_gpu_available(self):
        # This test assumes the environment's GPU state.
        # If GPU is available, it should return True; otherwise, False.
        self.assertIsInstance(TorchUtils.is_gpu_available(), bool)

    def test_get_device(self):
        # Ensure that get_device returns one of the expected values.
        self.assertIn(TorchUtils.get_device(), ["cuda", "mps", "cpu"])

    def test_device_count(self):
        # device_count should return an integer (0 if no GPUs available).
        self.assertIsInstance(TorchUtils.device_count(), int)

    def test_manual_seed(self):
        try:
            TorchUtils.manual_seed(42)
        except Exception as e:
            self.fail(f"manual_seed raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
