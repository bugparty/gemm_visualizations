from cpu_l1_cache import L1Cache, SimulatedArray
from cache_viz import plot_miss_rate, plot_access_heatmap, plot_access_3d
import random

def run_simulation():
    print("Initializing Cache System...")
    cache = L1Cache()

    # 64x64 matrix of integers (4 bytes)
    # Total items = 4096. Size = 16KB. Fits in 32KB cache.
    rows, cols = 64, 64
    arr = SimulatedArray(cache, rows * cols, dtype='i', base_addr=0x1000)

    print("Simulating Access Patterns...")

    # 1. Sequential Scan (Row-major) - Good spatial locality
    for i in range(len(arr)):
        val = arr[i]

    # 2. Column-major Scan - Bad spatial locality (strided)
    # Stride = 64 items * 4 bytes = 256 bytes.
    # Cache line = 64 bytes.
    # This will cause many misses.
    for c in range(cols):
        for r in range(rows):
            idx = r * cols + c
            val = arr[idx]
            arr[idx] = val + 1 # Read-Modify-Write

    # 3. Random Access Hotspots
    # Focus on the center 16x16 block
    center_r = rows // 2
    center_c = cols // 2
    for _ in range(5000):
        r = random.randint(center_r - 8, center_r + 8)
        c = random.randint(center_c - 8, center_c + 8)
        idx = r * cols + c
        val = arr[idx]

    print(f"Simulation Complete.")
    print(f"Stats: {cache.stats}")

    print("Generating Visualizations...")
    plot_miss_rate(cache, window_size=200, save_path='viz_miss_rate.png')
    plot_access_heatmap(arr, width=cols, save_path='viz_heatmap.png')
    plot_access_3d(arr, width=cols, save_path='viz_3d.png')

if __name__ == '__main__':
    run_simulation()
