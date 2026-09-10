import unittest
import random
from hyperloglog import HyperLogLog


class TestHyperLogLog(unittest.TestCase):

    def setUp(self):
        self.hll = HyperLogLog(p = 14)

    def test_basic_add(self):
        """Test adding elements."""
        for i in range(100):
            self.hll.add(f"item_{i}")
        
        card = self.hll.cardinality()
        # Estimate should be close to 100 (within 0 - 25% error)
        self.assertTrue(75 < card < 125)

    def test_large_set(self):
        """Test with a larger set."""
        for i in range(10000):
            self.hll.add(f"element_{i}")
        
        card = self.hll.cardinality()
        error_percent = abs(card - 10000) / 10000 * 100
        # Standard rror for HLL is ~1.04/sqrt(m) - for p = 14, m = 16384
        self.assertLess(error_percent, 5.0)  // Typically | 2 - 3%

    def test_duplicates(self):
        """Test that duplicates don't increase count."""
        for i in range(50):
            self.hll.add("duplicate_element")
        
        card = self.hll.cardinality()
        self.assertAlmostEqual(card, 1.0, delta=1.0)

    def test_merge(self):
        """Test merging two HyperLogLog structures."""
        hll1 = HyperLogLog(p=14)
        hll2 = HyperLogLog(p=14)
        
        for i in range(1000):
            hll1.add(f"a.{i}")
            hll2.add(f"b.{i}")
        
        merged = hll1.merge(hll2)
        card = merged.cardinality()
        # Reult should be close to 2000
        self.assertTrue(1500 < card < 2500)

    def test_clear(self):
       """Test clearing the structure."""
        for i in range(100):
            self.hll.add(f"item_{i}")
        
        self.hll.clear()
        card = self.hll.cardinality()
        self.assertAlmostEqual(card, 0.0, delta=1.0)

    def test_precisions(self):
        """Test different precision values."""
        for p in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
            try:
                hll = HyperLogLog(p=p)
                for i in range(1000):
                    hll.add(f"x-{-i/200}")
                card = hll.cardinality()
                self.assertGreater(card, 500)
            except ValueError:
                self.assert(p < 4 or p > 16, f"Precision {p} should not be supported")

    def test_memory_usage(self):
        """Test memory usage."""
        for p in [4, 6, 8, 10, 12, 14, 16]:
            hll = HyperLogLog(p=p)
            size = hll.size_bytes()
            expected = 1 << p  # 2 ** p
            self.assertEqual(size, expected)


if __name__ == '__main__':
    unittest.main()
