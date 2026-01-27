import matplotlib.pyplot as plt
import numpy as np
from cpu_l1_cache import L1Cache, SimulatedArray

def plot_miss_rate(cache: L1Cache, window_size=100, save_path='miss_rate.png'):
    """
    Plots the cache miss rate over time using a rolling window.

    Args:
        cache: The L1Cache instance containing access history.
        window_size: The number of accesses to average over.
        save_path: File path to save the plot.
    """
    history = cache.access_history
    if not history:
        print("No access history to plot.")
        return

    # Convert history (True=Hit, False=Miss) to Miss (1) / Hit (0)
    # Miss = 1 (if False), Hit = 0 (if True)
    miss_indicators = [1 if not h else 0 for h in history]

    # Calculate rolling average
    if len(miss_indicators) < window_size:
        miss_rates = [sum(miss_indicators) / len(miss_indicators)] * len(miss_indicators)
    else:
        # Use simple moving average
        miss_rates = []
        current_sum = sum(miss_indicators[:window_size])
        miss_rates.append(current_sum / window_size)

        for i in range(1, len(miss_indicators) - window_size + 1):
            current_sum = current_sum - miss_indicators[i-1] + miss_indicators[i+window_size-1]
            miss_rates.append(current_sum / window_size)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(miss_rates, label=f'Rolling Miss Rate (Window={window_size})')
    plt.title('Cache Miss Rate Over Time')
    plt.xlabel('Access Window Index')
    plt.ylabel('Miss Rate (0.0 - 1.0)')
    plt.grid(True)
    plt.legend()
    plt.savefig(save_path)
    print(f"Miss rate plot saved to {save_path}")
    plt.close()

def plot_access_heatmap(sim_array: SimulatedArray, width: int, save_path='heatmap.png'):
    """
    Plots a 2D heatmap of access frequencies for the SimulatedArray.

    Args:
        sim_array: The SimulatedArray instance.
        width: The width of the 2D representation (number of items per row).
        save_path: File path to save the plot.
    """
    cache = sim_array.cache
    base_addr = sim_array.base_addr
    item_size = sim_array.item_size
    length = sim_array.length

    # Calculate dimensions
    height = int(np.ceil(length / width))

    # Create grid
    access_grid = np.zeros((height, width))

    # Fill grid
    for i in range(length):
        # Calculate address of item i
        # Note: SimulatedArray access might touch multiple bytes.
        # We aggregate counts for bytes belonging to item i.
        # Simple approach: Check count of the starting byte of the item.
        addr = base_addr + (i * item_size)

        # Aggregate counts for all bytes in the item?
        # Or just take the start byte count.
        # Let's sum counts for bytes in this item.
        count = 0
        for offset in range(item_size):
            count += cache.access_counts.get(addr + offset, 0)

        row = i // width
        col = i % width
        access_grid[row, col] = count

    # Plot
    plt.figure(figsize=(12, 8))
    plt.imshow(access_grid, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Access Count')
    plt.title(f'Memory Access Heatmap (Array Shape: {height}x{width})')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    plt.savefig(save_path)
    print(f"Heatmap saved to {save_path}")
    plt.close()

def plot_access_3d(sim_array: SimulatedArray, width: int, save_path='access_3d.png'):
    """
    Plots a 3D bar chart of access frequencies.

    Args:
        sim_array: The SimulatedArray instance.
        width: The width of the 2D representation.
        save_path: File path to save the plot.
    """
    cache = sim_array.cache
    base_addr = sim_array.base_addr
    item_size = sim_array.item_size
    length = sim_array.length

    height = int(np.ceil(length / width))

    # Prepare data
    x_data = []
    y_data = []
    z_data = []

    for i in range(length):
        addr = base_addr + (i * item_size)
        count = 0
        for offset in range(item_size):
            count += cache.access_counts.get(addr + offset, 0)

        row = i // width
        col = i % width

        x_data.append(col)
        y_data.append(row)
        z_data.append(count)

    # Plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Use bars
    # ax.bar3d(x, y, z, dx, dy, dz)
    # x, y are coordinates of bar. z is start height (0).
    # dx, dy are width/depth (1). dz is height (count).

    top = np.array(z_data)
    bottom = np.zeros_like(top)
    width_bar = depth_bar = 0.8

    ax.bar3d(x_data, y_data, bottom, width_bar, depth_bar, top, shade=True)

    ax.set_title('3D Memory Access Frequency')
    ax.set_xlabel('Column')
    ax.set_ylabel('Row')
    ax.set_zlabel('Access Count')

    plt.savefig(save_path)
    print(f"3D plot saved to {save_path}")
    plt.close()
