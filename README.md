# 🔬 GEMM Memory Access Pattern Visualizer

An interactive educational tool for visualizing and analyzing memory access patterns in General Matrix Multiply (GEMM) operations. Compare different loop orderings, understand cache behavior, and explore the impact of blocking/tiling optimizations.

## ✨ Features

### 🎮 Interactive Web Interface
- **Real-time animation** of memory access patterns
- **Multiple loop orderings**: ijk, ikj, jik, jki, kij, kji
- **Blocking comparison**: blocked vs unblocked implementations
- **Play/pause/step controls** for detailed analysis

### 📊 Comprehensive Visualization
- **Live memory access animation** showing A, B, C matrix accesses
- **Cache hit rate tracking** with real-time performance graphs
- **Access frequency heatmaps** for pattern analysis
- **Detailed statistics** on cache performance

### 🎥 Video Generation (Legacy)
- Generate MP4 animations for presentations
- Cross-platform video encoding support
- Customizable animation speed and quality

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bugparty/gemm_visualizations.git
cd gemm_visualizations

# Install dependencies
pip install -r requirements.txt
```

### Run Interactive Visualizer

```bash
python interactive_viz.py
```

Then open your browser to: **http://127.0.0.1:8050**

### Generate Videos (Original Method)

```bash
python gen.py
```

This will generate MP4 animations for different loop orderings.

## 📁 Project Structure

```
gemm_visualizations/
├── interactive_viz.py      # 🎮 Main Dash web application
├── gemm_simulator.py        # 🧮 Core GEMM simulation engine
├── cache_simulator.py       # 💾 Cache behavior simulator
├── gen.py                   # 🎥 Video generation script (legacy)
├── requirements.txt         # 📦 Python dependencies
├── README.md               # 📖 This file
├── drawGemmForLoop.ipynb   # 📓 Jupyter notebook examples
└── cacheSimu.ipynb         # 📓 Cache simulation examples
```

## 🎯 Understanding Loop Orderings

Matrix multiplication: `C[i][j] += A[i][k] * B[k][j]`

Different loop orderings affect memory access patterns:

| Loop Order | Description | Cache Behavior |
|------------|-------------|----------------|
| **IJK** | Row-Column-Depth | Good for C, poor for B |
| **IKJ** | Row-Depth-Column | Good spatial locality |
| **JIK** | Column-Row-Depth | Poor for row-major matrices |
| **JKI** | Column-Depth-Row | Poor spatial locality |
| **KIJ** | Depth-Row-Column | Moderate performance |
| **KJI** | Depth-Column-Row | Good for blocked algorithms |

## 🎛️ Interactive Controls

### Configuration Panel
- **Matrix Size**: 4×4 to 32×32
- **Block Size**: 2 to 16 (for blocked algorithms)
- **Loop Order**: Select from 6 different orderings
- **Blocking**: Toggle between blocked/unblocked

### Animation Controls
- **▶ Play**: Start automatic animation
- **⏸ Pause**: Pause animation
- **🔄 Reset**: Reset to frame 0
- **Speed Slider**: Control animation speed (1-100 fps)
- **Frame Slider**: Jump to specific frame

## 📊 Interpreting Results

### Cache Hit Rate
- **> 90%**: Excellent cache utilization
- **70-90%**: Good performance
- **< 70%**: Poor cache behavior, consider optimization

### Access Frequency Heatmap
- **Bright spots**: Frequently accessed elements
- **Uniform color**: Good spatial locality
- **Scattered patterns**: Cache-unfriendly access

## 🧪 Examples

### Compare Blocked vs Unblocked

1. Set matrix size to 16×16, block size to 4
2. Select "KJI" loop order, set "Blocked" to ON
3. Note the cache hit rate
4. Switch "Blocked" to OFF
5. Compare performance!

### Best vs Worst Loop Order

**For blocked algorithms (16×16, block=4):**
- Best: KJI or IKJ (~85%+ hit rate)
- Worst: JKI or JIK (~60-70% hit rate)

## 💡 Educational Use

This tool is designed for:
- **Computer Architecture courses**: Teaching cache hierarchies
- **Performance optimization**: Understanding memory access patterns
- **Algorithm analysis**: Comparing loop transformations
- **Research**: Experimenting with blocking strategies

## 🔧 Advanced Usage

### Customize Cache Configuration

Edit `cache_simulator.py`:

```python
cache = CacheSimulator(
    cache_size=32768,      # 32KB L1 cache
    line_size=64,          # 64-byte cache lines
    associativity=8,       # 8-way set associative
    element_size=8         # 8 bytes per double
)
```

### Add New Loop Orders

Edit `gemm_simulator.py` to add custom loop transformations.

### Export Data

Modify `interactive_viz.py` to add CSV/JSON export functionality.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in interactive_viz.py
app.run_server(debug=True, host='0.0.0.0', port=8051)
```

### Video Encoding Fails
```bash
# Install FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/
```

### Module Not Found
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt --upgrade
```

## 📚 Technical Details

### Memory Layout
- **Row-major order**: C[i][j] stored at `base + (i*n + j)*sizeof(element)`
- **Cache line**: 64 bytes (8 doubles)
- **Spatial locality**: Sequential elements benefit from cache prefetch

### Cache Simulation
- **LRU replacement**: Least Recently Used eviction policy
- **Set-associative**: Configurable N-way associativity
- **Address mapping**: Tag-Index-Offset breakdown

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional cache replacement policies (FIFO, Random)
- 3D visualization of memory access
- Performance prediction models
- Multi-level cache hierarchy
- Non-square matrix support

## 📄 License

MIT License - feel free to use for educational purposes!

## 🙏 Acknowledgments

Based on classical GEMM optimization techniques from:
- *Computer Architecture: A Quantitative Approach* (Hennessy & Patterson)
- *Optimizing Matrix Multiply* (Goto & Geijn)

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

**Happy Learning! 🚀**
