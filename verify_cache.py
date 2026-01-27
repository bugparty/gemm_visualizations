import unittest
from cpu_l1_cache import L1Cache, SimulatedArray

class TestCacheSimulator(unittest.TestCase):
    def setUp(self):
        self.cache = L1Cache()

    def test_sequential_access_int32(self):
        print("\n--- Test 1: Sequential Access (Spatial Locality) ---")
        # 128 bytes = 2 cache lines (64B each). Int32 = 4 bytes.
        # 128 / 4 = 32 items.
        arr = SimulatedArray(self.cache, 32, dtype='i', base_addr=0x1000)

        # Read all
        for i in range(32):
            val = arr[i]

        # First access (index 0) -> Miss (fetches 0-63 bytes)
        # Next 15 accesses (index 1-15) -> Hits
        # Index 16 -> Miss (fetches 64-127 bytes)
        # Next 15 accesses (index 17-31) -> Hits

        hits = self.cache.stats['hits']
        misses = self.cache.stats['misses']

        print(f"Stats: Hits={hits}, Misses={misses}")

        self.assertEqual(misses, 2, "Should have exactly 2 misses for 2 cache lines")
        self.assertEqual(hits, 30, "Should have 30 hits")

    def test_write_back_eviction(self):
        print("\n--- Test 2: Write-Back Eviction (Associativity) ---")
        # 8-way associative.
        # We need 9 addresses that map to the same set.
        # Line size = 64. Sets = 64.
        # Stride = 64 * 64 = 4096 bytes ensures same set index, different tag.

        stride = 4096
        base = 0x2000

        # 1. Write to first line -> State M
        self.cache.write_byte(base, 99)
        self.assertEqual(self.cache.stats['misses'], 1)
        self.assertEqual(self.cache.stats['write_backs'], 0)

        # 2. Read 7 other lines to fill the set (Total 8 lines occupied)
        # i = 1..7
        for i in range(1, 8):
            addr = base + (i * stride)
            self.cache.read_byte(addr)

        # Stats so far: 1 write miss, 7 read misses. Total 8 lines in set. Set is FULL.
        self.assertEqual(self.cache.stats['evictions'], 0, "Should have 0 evictions so far")

        print(f"Before eviction: {self.cache.stats}")

        # 3. Access 1 more line (the 9th unique address) to evict Line0 (LRU)
        addr = base + (8 * stride)
        self.cache.read_byte(addr)

        print(f"After eviction: {self.cache.stats}")

        self.assertEqual(self.cache.stats['evictions'], 1, "Should have exactly 1 eviction now")
        self.assertEqual(self.cache.stats['write_backs'], 1, "Should have 1 write-back (Line0 was dirty)")

        # Verify Main Memory has the data for Line0
        val = self.cache.memory.read(base, 1)[0]
        self.assertEqual(val, 99, "Main memory should be updated after write-back")

    def test_data_integrity(self):
        print("\n--- Test 3: Data Integrity ---")
        arr = SimulatedArray(self.cache, 10, dtype='i', base_addr=0x3000)

        arr[5] = 123456789
        val = arr[5]

        self.assertEqual(val, 123456789, "Should read back what was written")

        # Force eviction of that line and read back from memory
        # Only if we implement full eviction logic in test (reusing logic from Test 2)
        # But even without eviction, cache consistency is key.

        # Let's try strided access across lines
        arr2 = SimulatedArray(self.cache, 100, dtype='B', base_addr=0x4000) # Bytes
        # Write across boundary 63-64
        arr2[63] = 1
        arr2[64] = 2

        self.assertEqual(arr2[63], 1)
        self.assertEqual(arr2[64], 2)

if __name__ == '__main__':
    unittest.main()
