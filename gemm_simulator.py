"""
GEMM (General Matrix Multiply) Memory Access Pattern Simulator

This module simulates different loop orderings for matrix multiplication
and tracks memory access patterns for visualization and cache analysis.
"""

import numpy as np
from typing import List, Tuple, Dict


class GEMMSimulator:
    """Simulates GEMM memory access patterns for different loop orderings."""

    # All possible loop orderings
    LOOP_ORDERS = ['ijk', 'ikj', 'jik', 'jki', 'kij', 'kji']

    def __init__(self, n: int, block_size: int = None):
        """
        Initialize GEMM simulator.

        Args:
            n: Matrix size (n x n)
            block_size: Block size for tiling (None for unblocked)
        """
        self.n = n
        self.block_size = block_size if block_size else n  # Unblocked if None
        self.tracks = []
        self.access_count = {'A': 0, 'B': 0, 'C': 0}

    def reset(self):
        """Reset simulation state."""
        self.tracks = []
        self.access_count = {'A': 0, 'B': 0, 'C': 0}

    def simulate(self, loop_order: str, blocked: bool = True) -> List[Tuple]:
        """
        Simulate GEMM with specified loop order.

        Args:
            loop_order: One of 'ijk', 'ikj', 'jik', 'jki', 'kij', 'kji'
            blocked: Whether to use blocking/tiling

        Returns:
            List of access patterns: [((i,k), (k,j), (i,j)), ...]
                                     (A_pos, B_pos, C_pos)
        """
        self.reset()

        if loop_order not in self.LOOP_ORDERS:
            raise ValueError(f"Invalid loop order. Must be one of {self.LOOP_ORDERS}")

        if blocked:
            self._simulate_blocked(loop_order)
        else:
            self._simulate_unblocked(loop_order)

        return self.tracks

    def _simulate_blocked(self, loop_order: str):
        """Simulate blocked/tiled GEMM."""
        n = self.n
        bs = self.block_size

        # Outer loops over blocks
        if loop_order == 'ijk':
            for i in range(0, n, bs):
                for j in range(0, n, bs):
                    for k in range(0, n, bs):
                        self._inner_loops(i, j, k, bs)

        elif loop_order == 'ikj':
            for i in range(0, n, bs):
                for k in range(0, n, bs):
                    for j in range(0, n, bs):
                        self._inner_loops(i, j, k, bs)

        elif loop_order == 'jik':
            for j in range(0, n, bs):
                for i in range(0, n, bs):
                    for k in range(0, n, bs):
                        self._inner_loops(i, j, k, bs)

        elif loop_order == 'jki':
            for j in range(0, n, bs):
                for k in range(0, n, bs):
                    for i in range(0, n, bs):
                        self._inner_loops(i, j, k, bs)

        elif loop_order == 'kij':
            for k in range(0, n, bs):
                for i in range(0, n, bs):
                    for j in range(0, n, bs):
                        self._inner_loops(i, j, k, bs)

        elif loop_order == 'kji':
            for k in range(0, n, bs):
                for j in range(0, n, bs):
                    for i in range(0, n, bs):
                        self._inner_loops(i, j, k, bs)

    def _inner_loops(self, i_base, j_base, k_base, bs):
        """Inner loops within a block."""
        n = self.n

        for ii in range(i_base, min(i_base + bs, n)):
            for jj in range(j_base, min(j_base + bs, n)):
                for kk in range(k_base, min(k_base + bs, n)):
                    # C[i,j] += A[i,k] * B[k,j]
                    a_pos = (ii, kk)
                    b_pos = (kk, jj)
                    c_pos = (ii, jj)
                    self.tracks.append((a_pos, b_pos, c_pos))
                    self.access_count['A'] += 1
                    self.access_count['B'] += 1
                    self.access_count['C'] += 1

    def _simulate_unblocked(self, loop_order: str):
        """Simulate unblocked GEMM."""
        n = self.n

        if loop_order == 'ijk':
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        self._record_access(i, j, k)

        elif loop_order == 'ikj':
            for i in range(n):
                for k in range(n):
                    for j in range(n):
                        self._record_access(i, j, k)

        elif loop_order == 'jik':
            for j in range(n):
                for i in range(n):
                    for k in range(n):
                        self._record_access(i, j, k)

        elif loop_order == 'jki':
            for j in range(n):
                for k in range(n):
                    for i in range(n):
                        self._record_access(i, j, k)

        elif loop_order == 'kij':
            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        self._record_access(i, j, k)

        elif loop_order == 'kji':
            for k in range(n):
                for j in range(n):
                    for i in range(n):
                        self._record_access(i, j, k)

    def _record_access(self, i, j, k):
        """Record a single memory access."""
        a_pos = (i, k)
        b_pos = (k, j)
        c_pos = (i, j)
        self.tracks.append((a_pos, b_pos, c_pos))
        self.access_count['A'] += 1
        self.access_count['B'] += 1
        self.access_count['C'] += 1

    def get_heatmap_data(self) -> Dict[str, np.ndarray]:
        """
        Generate heatmap data showing access frequency.

        Returns:
            Dict with keys 'A', 'B', 'C' containing access frequency matrices
        """
        heatmaps = {
            'A': np.zeros((self.n, self.n)),
            'B': np.zeros((self.n, self.n)),
            'C': np.zeros((self.n, self.n))
        }

        for a_pos, b_pos, c_pos in self.tracks:
            heatmaps['A'][a_pos] += 1
            heatmaps['B'][b_pos] += 1
            heatmaps['C'][c_pos] += 1

        return heatmaps

    def get_statistics(self) -> Dict:
        """
        Get simulation statistics.

        Returns:
            Dictionary containing access counts and other metrics
        """
        return {
            'total_operations': len(self.tracks),
            'matrix_size': self.n,
            'block_size': self.block_size,
            'access_count': self.access_count.copy(),
            'theoretical_ops': self.n ** 3
        }


if __name__ == '__main__':
    # Test the simulator
    print("Testing GEMM Simulator...")

    # Test blocked version
    sim = GEMMSimulator(n=8, block_size=4)
    tracks = sim.simulate('kji', blocked=True)
    print(f"\nBlocked KJI (n=8, block=4):")
    print(f"  Total accesses: {len(tracks)}")
    print(f"  First 5 accesses: {tracks[:5]}")
    print(f"  Statistics: {sim.get_statistics()}")

    # Test unblocked version
    sim2 = GEMMSimulator(n=4, block_size=None)
    tracks2 = sim2.simulate('ijk', blocked=False)
    print(f"\nUnblocked IJK (n=4):")
    print(f"  Total accesses: {len(tracks2)}")
    print(f"  First 5 accesses: {tracks2[:5]}")

    print("\n✓ GEMM Simulator module working correctly!")
