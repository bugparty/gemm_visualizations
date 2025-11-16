---
title: GEMM Memory Access Pattern Visualizer
emoji: 🔬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🔬 GEMM Memory Access Pattern Visualizer

An interactive educational tool for visualizing and analyzing memory access patterns in General Matrix Multiply (GEMM) operations. Compare different loop orderings, understand cache behavior, and explore the impact of blocking/tiling optimizations.

## 🚀 Try It Out

This is a live demo running on Hugging Face Spaces. Simply adjust the controls on the left panel to explore different GEMM configurations!

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

## 🎛️ How to Use

### Configuration Panel
1. **Matrix Size**: Adjust from 4×4 to 32×32
2. **Block Size**: Set block size (2-16) for blocked algorithms
3. **Loop Order**: Select from 6 different orderings
4. **Blocking**: Toggle between blocked/unblocked

### Animation Controls
- **▶ Play**: Start automatic animation
- **⏸ Pause**: Pause animation
- **🔄 Reset**: Reset to frame 0
- **Speed Slider**: Control animation speed (1-100)
- **Frame Slider**: Jump to specific frame

## 📊 Interpreting Results

### Cache Hit Rate
- **> 90%**: Excellent cache utilization ✅
- **70-90%**: Good performance 👍
- **< 70%**: Poor cache behavior, consider optimization ⚠️

### Access Frequency Heatmap
- **Bright spots**: Frequently accessed elements
- **Uniform color**: Good spatial locality
- **Scattered patterns**: Cache-unfriendly access

## 🧪 Try These Experiments

### Experiment 1: Blocked vs Unblocked
1. Set matrix size to 16×16, block size to 4
2. Select "KJI" loop order, set "Blocked" to ON
3. Note the cache hit rate
4. Switch "Blocked" to OFF
5. Compare performance! You should see a significant difference

### Experiment 2: Best vs Worst Loop Order
**For blocked algorithms (16×16, block=4):**
- Best: KJI or IKJ (~85%+ hit rate)
- Worst: JKI or JIK (~60-70% hit rate)

## 💡 Educational Use

This tool is designed for:
- **Computer Architecture courses**: Teaching cache hierarchies
- **Performance optimization**: Understanding memory access patterns
- **Algorithm analysis**: Comparing loop transformations
- **Research**: Experimenting with blocking strategies

## 📚 Technical Details

### Memory Layout
- **Row-major order**: C[i][j] stored at `base + (i*n + j)*sizeof(element)`
- **Cache line**: 64 bytes (8 doubles)
- **Spatial locality**: Sequential elements benefit from cache prefetch

### Cache Simulation
- **LRU replacement**: Least Recently Used eviction policy
- **Set-associative**: 8-way associativity (configurable)
- **Address mapping**: Tag-Index-Offset breakdown
- **Cache size**: 32KB L1 cache simulation

## 🔧 Local Installation

```bash
# Clone the repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/gemm-visualizer
cd gemm-visualizer

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Then open your browser to: **http://127.0.0.1:7860**

## 🤝 Contributing

Contributions welcome! Visit the [GitHub repository](https://github.com/bugparty/gemm_visualizations) for:
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

For questions or feedback, please open an issue on the [GitHub repository](https://github.com/bugparty/gemm_visualizations).

---

**Happy Learning! 🚀**
