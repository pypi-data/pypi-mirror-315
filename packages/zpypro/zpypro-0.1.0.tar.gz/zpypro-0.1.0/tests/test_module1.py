# tests/test_module1.py
import unittest
from pypro.module1 import example_function


class TestModule1(unittest.TestCase):
    def test_example_function(self):
        # Add tests for example_function
        self.assertIsNone(example_function())


if __name__ == "__main__":
    unittest.main()
