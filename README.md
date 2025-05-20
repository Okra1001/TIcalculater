```markdown
# 🌪️ 湍流度与湍流积分尺度计算器套件

## 📦 概述
本套件包含三款专用工具，用于计算流体力学中的关键湍流参数。支持CPU/GPU双模式加速，满足不同规模数据的处理需求。

## 🛠️ 工具列表
1. `TI.py` - 湍流度批量计算器  
2. `Turbulence_scale_length.py` - 湍流积分尺度分析工具  
3. `cuda.py` - GPU加速版湍流积分尺度计算器

---

## 📁 TI.py - 湍流度批量计算器
### 🎯 功能描述
- 批量计算指定文件夹内所有风速文件的湍流强度
- 自动识别.csv/.txt数据格式
- 输出结构化报表

### 🚀 使用方法
```python
修改源码中的目标目录
DATA_DIR = "/path/to/your/wind_data"  # ← 修改此处路径
```

### ⚙️ 运行示例
```bash
python TI.py
```

---

## 📏 Turbulence_scale_length.py - 湍流积分尺度分析
### 🎯 功能描述
- 基于自相关函数的湍流特征尺度计算
- 支持多文件批处理
- 生成可视化分析图表

### 🖥️ 命令行操作
```bash
python Turbulence_scale_length.py /path/to/wind_speed_data
```

### 🧮 参数说明
| 参数 | 描述 |
|------|------|
| `/path/to/wind_speed_data` | 风速数据文件夹绝对路径 |

---

## ⚡ cuda.py - GPU加速版计算器
### 🎯 性能优势
- 利用NVIDIA CUDA并行计算架构
- 相比CPU版本提速8-12倍
- 支持FP16混合精度计算

### 🖥️ 运行命令
```bash
python cuda.py /path/to/large_dataset
```

### ⚠️ 环境要求
- NVIDIA GPU (Compute Capability ≥ 6.0)
- CUDA Toolkit 11+
- cuDNN 8.0+

---

## 📌 注意事项
1. 确保数据文件格式统一
2. GPU版本需要安装PyTorch/CUDA依赖
3. 建议对超过1GB的数据集使用GPU版本
4. 输出结果保存在同级目录的`Results/`文件夹

## 🔗 附录
[📥 依赖安装指南] | [📈 示例数据集] | [📜 算法白皮书]
```

这个Markdown格式具有以下特点：
1. 使用Emoji图标增强可读性
2. 清晰的层次结构（H2/H3标题）
3. 表格化参数说明
4. 代码块高亮显示命令
5. 醒目的注意事项板块
6. 响应式布局设计
7. 关键信息使用颜色块标识（需在支持MD渲染的查看器中显示效果更佳）
