import unittest
import numpy as np
from olevester_transform.transform import OlevesterTransform

class TestOlevesterTransform(unittest.TestCase):
    def test_normalize_field(self):
        field = np.array([[1, 2], [3, 4]])
        normalized = OlevesterTransform.normalize_field(field)
        self.assertAlmostEqual(np.linalg.norm(normalized), 1.0, places=6)

    def test_dimensional_expand(self):
        field = np.array([1, 2, 3])
        expanded = OlevesterTransform.dimensional_expand(field, (3, 3))
        self.assertEqual(expanded.shape, (3, 3))

    def test_dimensional_reduce(self):
        field = np.array([[1, 2], [3, 4]])
        reduced = OlevesterTransform.dimensional_reduce(field, (1,))
        self.assertEqual(reduced.shape, (1,))

if __name__ == "__main__":
    unittest.main()
