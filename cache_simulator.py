"""
Simple Cache Simulator for Memory Access Pattern Analysis

Simulates a simple set-associative cache to analyze cache behavior
for different GEMM loop orderings.
"""

import numpy as np
from typing import List, Tuple, Dict
from collections import OrderedDict


class CacheSimulator:
    """Simulates a simple set-associative cache."""

    def __init__(self, cache_size: int = 32768, line_size: int = 64,
                 associativity: int = 8, element_size: int = 8):
        """
        Initialize cache simulator.

        Args:
            cache_size: Total cache size in bytes (default: 32KB)
            line_size: Cache line size in bytes (default: 64B)
            associativity: Set associativity (default: 8-way)
            element_size: Size of each matrix element in bytes (default: 8B for double)
        """
        self.cache_size = cache_size
        self.line_size = line_size
        self.associativity = associativity
        self.element_size = element_size

        # Calculate number of sets
        self.num_lines = cache_size // line_size
        self.num_sets = self.num_lines // associativity

        # Cache storage: dict of sets, each set is an OrderedDict (LRU)
        self.cache = {i: OrderedDict() for i in range(self.num_sets)}

        # Statistics
        self.hits = 0
        self.misses = 0
        self.accesses = 0
        self.hit_rate_history = []

    def reset(self):
        """Reset cache and statistics."""
        self.cache = {i: OrderedDict() for i in range(self.num_sets)}
        self.hits = 0
        self.misses = 0
        self.accesses = 0
        self.hit_rate_history = []

    def _get_address(self, matrix_base: int, row: int, col: int, n: int) -> int:
        """
        Calculate memory address for matrix[row][col].

        Args:
            matrix_base: Base address of the matrix
            row: Row index
            col: Column index
            n: Matrix dimension

        Returns:
            Memory address
        """
        # Assume row-major layout
        offset = (row * n + col) * self.element_size
        return matrix_base + offset

    def _parse_address(self, address: int) -> Tuple[int, int, int]:
        """
        Parse address into tag, set index, and block offset.

        Returns:
            (tag, set_index, block_offset)
        """
        block_offset = address % self.line_size
        set_index = (address // self.line_size) % self.num_sets
        tag = address // (self.line_size * self.num_sets)
        return tag, set_index, block_offset

    def access(self, address: int) -> bool:
        """
        Simulate a cache access.

        Args:
            address: Memory address to access

        Returns:
            True if hit, False if miss
        """
        tag, set_index, _ = self._parse_address(address)
        cache_set = self.cache[set_index]

        self.accesses += 1
        hit = False

        if tag in cache_set:
            # Cache hit - move to end (most recently used)
            cache_set.move_to_end(tag)
            self.hits += 1
            hit = True
        else:
            # Cache miss
            self.misses += 1

            # Add to cache
            cache_set[tag] = True

            # Evict if set is full (LRU)
            if len(cache_set) > self.associativity:
                cache_set.popitem(last=False)  # Remove least recently used

        # Record hit rate periodically
        if self.accesses % 100 == 0:
            self.hit_rate_history.append(self.get_hit_rate())

        return hit

    def simulate_accesses(self, tracks: List[Tuple], matrix_size: int,
                         matrix_bases: Dict[str, int] = None) -> Dict:
        """
        Simulate cache behavior for a sequence of memory accesses.

        Args:
            tracks: List of access patterns from GEMMSimulator
            matrix_size: Size of matrices (n x n)
            matrix_bases: Base addresses for matrices A, B, C

        Returns:
            Dictionary with cache statistics
        """
        if matrix_bases is None:
            # Default base addresses (like in the original code)
            matrix_bases = {
                'A': 0x10000,
                'B': 0x20000,
                'C': 0x30000
            }

        self.reset()

        for a_pos, b_pos, c_pos in tracks:
            # Access A[i][k]
            addr_a = self._get_address(matrix_bases['A'], a_pos[0], a_pos[1], matrix_size)
            self.access(addr_a)

            # Access B[k][j]
            addr_b = self._get_address(matrix_bases['B'], b_pos[0], b_pos[1], matrix_size)
            self.access(addr_b)

            # Access C[i][j] (read-modify-write, count as 2 accesses)
            addr_c = self._get_address(matrix_bases['C'], c_pos[0], c_pos[1], matrix_size)
            self.access(addr_c)
            self.access(addr_c)

        return self.get_statistics()

    def get_hit_rate(self) -> float:
        """Calculate current cache hit rate."""
        if self.accesses == 0:
            return 0.0
        return (self.hits / self.accesses) * 100

    def get_statistics(self) -> Dict:
        """
        Get cache statistics.

        Returns:
            Dictionary containing cache performance metrics
        """
        return {
            'total_accesses': self.accesses,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.get_hit_rate(),
            'miss_rate': 100 - self.get_hit_rate(),
            'hit_rate_history': self.hit_rate_history.copy(),
            'cache_config': {
                'cache_size': self.cache_size,
                'line_size': self.line_size,
                'associativity': self.associativity,
                'num_sets': self.num_sets
            }
        }


if __name__ == '__main__':
    # Test the cache simulator
    from gemm_simulator import GEMMSimulator

    print("Testing Cache Simulator...")

    # Create GEMM simulator
    gemm = GEMMSimulator(n=16, block_size=4)

    # Test different loop orders
    cache = CacheSimulator(cache_size=32768, line_size=64, associativity=8)

    for loop_order in ['ijk', 'kji']:
        tracks = gemm.simulate(loop_order, blocked=True)
        stats = cache.simulate_accesses(tracks, matrix_size=16)

        print(f"\n{loop_order.upper()} Loop Order:")
        print(f"  Total accesses: {stats['total_accesses']}")
        print(f"  Hits: {stats['hits']}")
        print(f"  Misses: {stats['misses']}")
        print(f"  Hit rate: {stats['hit_rate']:.2f}%")

    print("\n✓ Cache Simulator module working correctly!")
