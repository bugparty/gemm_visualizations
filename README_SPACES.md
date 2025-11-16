---
title: GEMM Memory Access Visualizer
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: dash
sdk_version: 2.14.0
app_file: app.py
pinned: false
license: mit
tags:
  - computer-architecture
  - cache-simulation
  - educational
  - visualization
  - performance-optimization
---

# 🔬 GEMM Memory Access Pattern Visualizer

An **interactive educational tool** for visualizing and analyzing memory access patterns in General Matrix Multiply (GEMM) operations.

Perfect for students, educators, and engineers learning about:
- 🎓 Computer architecture
- 💾 Cache memory behavior
- ⚡ Performance optimization
- 🔄 Loop transformations

## 🚀 Quick Start

1. **Select matrix size** (4×4 to 32×32)
2. **Choose loop order** (IJK, IKJ, JIK, JKI, KIJ, KJI)
3. **Enable/disable blocking** (tiling optimization)
4. **Press ▶ Play** to watch the animation!

## 🎯 What You'll Learn

### Loop Orderings Impact

Matrix multiplication: `C[i][j] += A[i][k] * B[k][j]`

Different loop orderings dramatically affect cache performance:

| Loop Order | Cache Hit Rate | Best For |
|------------|----------------|----------|
| **IKJ** | 🟢 85-95% | General purpose |
| **KJI** | 🟢 85-95% | Blocked algorithms |
| **IJK** | 🟡 70-85% | Simple implementations |
| **JKI/JIK** | 🔴 60-75% | Poor cache locality |

### Blocking/Tiling Benefits

- **Unblocked**: Simple but cache-inefficient
- **Blocked**: Divides work into cache-friendly chunks
- **Performance gain**: 2-10x speedup for large matrices!

## 📊 Features

### Interactive Visualization
- ✅ Real-time memory access animation
- ✅ Live cache hit rate tracking
- ✅ Access frequency heatmaps
- ✅ Detailed performance statistics

### Educational Controls
- 🎮 Play/Pause/Step animation
- 🎛️ Adjustable matrix and block sizes
- 📈 Compare 6 different loop orderings
- 💡 Visual understanding of cache behavior

## 🔬 Technical Details

### Cache Simulation
- **Size**: 32 KB L1 cache
- **Line Size**: 64 bytes
- **Associativity**: 8-way set associative
- **Replacement**: LRU (Least Recently Used)

### Matrix Operations
- **Sizes**: 4×4 to 32×32 (configurable)
- **Element size**: 8 bytes (double precision)
- **Layout**: Row-major order
- **Operations**: Full GEMM (C = C + A × B)

## 💡 How to Use

### For Students
1. Start with a small matrix (8×8)
2. Try different loop orders
3. Observe cache hit rates
4. Compare blocked vs unblocked

### For Educators
- Use in computer architecture courses
- Demonstrate cache hierarchy concepts
- Explain loop optimization techniques
- Show real-world performance impacts

### For Engineers
- Understand why BLAS libraries are fast
- Learn blocking/tiling strategies
- Optimize your own matrix code
- Experiment with different cache sizes

## 📚 Learn More

### Recommended Reading
- *Computer Architecture: A Quantitative Approach* (Hennessy & Patterson)
- *Optimizing Matrix Multiply* (Goto & Geijn)
- [Cache-Oblivious Algorithms](https://en.wikipedia.org/wiki/Cache-oblivious_algorithm)

### Related Topics
- Cache memory hierarchy
- Spatial and temporal locality
- Loop tiling/blocking
- BLAS (Basic Linear Algebra Subprograms)

## 🤝 Contributing

This project is open source! Contributions welcome:
- GitHub: [bugparty/gemm_visualizations](https://github.com/bugparty/gemm_visualizations)
- Report issues or suggest features

## 📄 License

MIT License - Free for educational use!

## 🙏 Acknowledgments

Built with:
- [Dash](https://dash.plotly.com/) - Interactive web framework
- [Plotly](https://plotly.com/) - Visualization library
- [NumPy](https://numpy.org/) - Numerical computing

---

**Made with ❤️ for computer science education**

*Try adjusting the parameters and see how cache performance changes!*
