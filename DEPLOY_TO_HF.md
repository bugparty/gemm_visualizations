# 🚀 部署到 Hugging Face Spaces 指南

完整的一步步部署教程

## 📋 准备工作

### 1. 创建 Hugging Face 账号

如果还没有账号：
1. 访问 https://huggingface.co/join
2. 注册账号（免费）
3. 验证邮箱

### 2. 获取 Access Token

1. 登录后访问：https://huggingface.co/settings/tokens
2. 点击 **"New token"**
3. 填写信息：
   - Name: `gemm-visualizer-deploy`（或任意名称）
   - Role: 选择 **"Write"** 权限
4. 点击 **"Generate a token"**
5. **复制并保存** token（只显示一次！）

## 🎯 方法 1: 通过网页界面上传（最简单）

### 步骤 1: 创建新的 Space

1. 访问 https://huggingface.co/spaces
2. 点击右上角 **"Create new Space"**
3. 填写信息：
   - **Owner**: 你的用户名
   - **Space name**: `gemm-visualizer`（或其他名称）
   - **License**: MIT
   - **Select the Space SDK**: 选择 **"Dash"**
   - **Space hardware**: Free CPU（默认即可）
   - **Space visibility**: Public（公开）或 Private（私有）
4. 点击 **"Create Space"**

### 步骤 2: 上传文件

在创建好的 Space 页面：

1. 点击 **"Files"** 标签页
2. 点击 **"Add file"** → **"Upload files"**
3. 上传以下文件（按顺序）：
   ```
   app.py
   gemm_simulator.py
   cache_simulator.py
   requirements.txt
   ```
4. 点击 **"Commit changes to main"**

### 步骤 3: 更新 README

1. 在 Files 页面找到 `README.md`
2. 点击编辑（铅笔图标）
3. 删除所有内容
4. 复制 `README_SPACES.md` 的内容粘贴进去
5. 点击 **"Commit changes to main"**

### 步骤 4: 等待部署

- Space 会自动开始构建（约 2-5 分钟）
- 在页面顶部可以看到 "Building..." 状态
- 构建完成后会自动启动应用
- 看到应用界面即表示成功！🎉

## 🖥️ 方法 2: 通过 Git 命令行（高级）

### 步骤 1: 安装 Git LFS

```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Windows
# 从 https://git-lfs.github.com/ 下载安装

# 初始化
git lfs install
```

### 步骤 2: 克隆 Space 仓库

首先在 HF 网页上创建 Space（按方法1的步骤1），然后：

```bash
# 替换 YOUR_USERNAME 为你的用户名
git clone https://huggingface.co/spaces/YOUR_USERNAME/gemm-visualizer
cd gemm-visualizer
```

### 步骤 3: 配置 Git 凭据

```bash
# 设置用户名
git config user.email "your-email@example.com"
git config user.name "Your Name"

# 设置 token 作为密码（运行后会提示输入）
# 用户名: 你的 HF 用户名
# 密码: 粘贴你的 Access Token
```

### 步骤 4: 复制文件并推送

```bash
# 从项目目录复制文件到 Space 目录
cp /home/user/gemm_visualizations/app.py .
cp /home/user/gemm_visualizations/gemm_simulator.py .
cp /home/user/gemm_visualizations/cache_simulator.py .
cp /home/user/gemm_visualizations/requirements.txt .
cp /home/user/gemm_visualizations/README_SPACES.md ./README.md

# 添加所有文件
git add .

# 提交
git commit -m "Initial deployment of GEMM visualizer"

# 推送到 Hugging Face
git push
```

### 步骤 5: 查看部署

访问：`https://huggingface.co/spaces/YOUR_USERNAME/gemm-visualizer`

## 📝 需要上传的文件清单

确保以下文件都在 Space 中：

- ✅ `app.py` - 主应用文件（Dash 入口）
- ✅ `gemm_simulator.py` - GEMM 模拟器核心
- ✅ `cache_simulator.py` - 缓存模拟器
- ✅ `requirements.txt` - Python 依赖
- ✅ `README.md` - Space 主页描述（使用 README_SPACES.md 的内容）

**不需要上传**：
- ❌ `gen.py` - 这是本地视频生成脚本
- ❌ `.ipynb` 文件 - Jupyter notebooks
- ❌ `.mp4` 文件 - 视频文件
- ❌ `__pycache__/` - Python 缓存

## 🔧 常见问题

### Q: Space 构建失败怎么办？

**A:** 检查 Build logs：
1. 在 Space 页面点击 **"Logs"** 标签
2. 查看错误信息
3. 常见问题：
   - 依赖安装失败 → 检查 `requirements.txt`
   - 导入错误 → 确保所有 `.py` 文件都已上传
   - 端口问题 → `app.py` 已经配置好了 PORT 环境变量

### Q: 应用启动但显示空白？

**A:** 检查：
1. 浏览器控制台是否有 JavaScript 错误
2. Space logs 中是否有 Python 错误
3. 尝试刷新页面（Ctrl+F5 强制刷新）

### Q: 可以使用免费的 CPU 吗？

**A:** 可以！这个应用很轻量，Free CPU 完全够用。

### Q: 如何更新已部署的 Space？

**A:**
- 网页方式：直接在 Files 页面编辑/上传文件
- Git 方式：修改文件后 `git push` 即可

### Q: 可以设置为私有吗？

**A:** 可以！在 Space Settings 中可以修改 visibility。

## 🎨 自定义你的 Space

### 修改标题和描述

编辑 `README.md` 顶部的 YAML front matter：

```yaml
---
title: 你的自定义标题
emoji: 🚀  # 任意 emoji
colorFrom: blue  # 起始颜色
colorTo: purple  # 结束颜色
---
```

### 修改应用界面

编辑 `app.py` 中的：
- 标题：搜索 `"GEMM Memory Access Pattern Visualizer"`
- 颜色：修改 `COLORS` 字典
- 布局：调整 `app.layout` 部分

## 📊 监控你的 Space

### 查看使用统计

在 Space 页面可以看到：
- 👥 访问量
- ⭐ 点赞数
- 📈 使用趋势

### 分享你的 Space

Space URL 格式：
```
https://huggingface.co/spaces/YOUR_USERNAME/gemm-visualizer
```

可以分享到：
- 课程网站
- 教学材料
- 社交媒体
- 论文补充材料

## 🌟 提升可见度

### 添加标签

在 README.md 的 YAML 部分：

```yaml
tags:
  - computer-architecture
  - education
  - visualization
  - cache
  - performance
```

### 写详细的描述

好的 README 能让更多人发现和使用你的 Space！

### 嵌入到网页

Hugging Face 提供嵌入代码：

```html
<iframe
  src="https://YOUR_USERNAME-gemm-visualizer.hf.space"
  frameborder="0"
  width="100%"
  height="800"
></iframe>
```

## 🎉 部署完成！

部署成功后，你将拥有：

✅ 一个公开访问的 Web 应用
✅ 永久的 URL 可以分享
✅ 自动的 HTTPS 支持
✅ 全球 CDN 加速
✅ 免费的托管服务

**示例 URL**: `https://huggingface.co/spaces/YOUR_USERNAME/gemm-visualizer`

---

## 📞 需要帮助？

- Hugging Face 文档: https://huggingface.co/docs/hub/spaces
- Discord 社区: https://huggingface.co/join/discord
- 论坛: https://discuss.huggingface.co/

**祝部署顺利！🚀**
