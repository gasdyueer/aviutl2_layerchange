# AviUtl 层转换工具 (Layer Change Tool for AviUtl)

[![PySide6](https://img.shields.io/badge/PySide6-6.6.2-green)](https://pypi.org/project/PySide6/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

一个强大的AviUtl（AUP2）文件层处理工具，提供**图形界面**和**命令行接口**两种使用方式，支持多语言界面设计。

## 🌍 语言选择 (Language Selection)

- **[🇨🇳 简体中文](./README.md)**
- **[🇺🇸 English](./README_en.md)**
- **[🇯🇵 日本語](./README_jp.md)**

> 💡 **选择您的语言** | Choose Your Language | 言語を選択してください

## ✨ 功能特性

### 🎯 核心功能
- **🔄 层转换**: 将指定场景的对象图层统一调整为目标图层
- **🎬 帧范围调整**: 使连续对象帧范围更加紧凑
- **🚩 多场景隔离**: 各场景对象独立连续排列，保持时间线独立性
- **📄 TXT导出**: 将AUP2文件内容转换为文本格式便于查看

### 🎨 多语言图形界面
- **🇨🇳 中文版本** (gui.py) - 紧凑设计，界面文字精炼获取优越的可用性
- **🇺🇸 英文版本** (gui_en.py) - 国际化支持，标准英文界面
- **🇯🇵 日文版本** (gui_jp.py) - 面向日语用户，截短版界面

### 🛠️ 技术优势
- 🚀 **高性能**: 基于PySide6，使用原生C++性能
- 🎛️ **灵活配置**: 支持指定场景ID、目标层级等参数
- 🔍 **智能验证**: 内建解析校验功能，确保数据正确性
- 📊 **实时分析**: 文件结构分析和统计报告

## 📋 系统要求

- **Python**: 3.9 或更高版本
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **内存**: 至少512MB可用内存
- **存储**: 至少100MB可用磁盘空间

## 🚀 快速开始

### 方式1: 使用预编译版本 (推荐)

```bash
# 直接运行预编译的可执行文件 (Windows)
./output/aup2_layerchange_gui_zh.exe   # 中文版本
./output/aup2_layerchange_gui_en.exe   # 英文版本
./output/aup2_layerchange_gui_jp.exe   # 日文版本
```

#### 🌍 **可执行文件说明**
- **🇨🇳 中文版**: `aup2_layerchange_gui_zh.exe` - 紧凑界面，最小化设计
- **🇺🇸 英文版**: `aup2_layerchange_gui_en.exe` - 国际化界面标准设计
- **🇯🇵 日文版**: `aup2_layerchange_gui_jp.exe` - 日语优化，文字精炼

### 方式2: 从源码安装

#### 1. 克隆项目
```bash
git clone https://github.com/gasdyueer/aviutl2_layerchange.git
cd aviutl2_layerchange
```

#### 2. 安装依赖
```bash
# 使用pip安装（推荐）
pip install -r requirements.txt

# 或者使用uv（更快的包管理器）
uv sync
```

#### 3. 运行程序
```bash
# 图形界面版本
python gui.py          # 中文紧凑版界面
python gui_en.py       # 英文紧凑版界面
python gui_jp.py       # 日文紧凑版界面

# 命令行版本
python layerchange.py --help
```

## 📖 使用指南

### 图形界面使用

#### 1. 文件设置
- **📁 文件**: 选择输入和输出文件
  - **入:**: 选择AUP2源文件
  - **出:**: 指定输出位置

#### 2. 参数配置
- **⚙️ 参数**: 设置转换参数
  - **场景:**: 目标场景ID（留空处理所有场景）
  - **图层:**: 目标图层号（默认0）

#### 3. 操作选项
- **🔧 选项**: 选择处理方式
  - **🎬 连续帧**: 调整帧范围使对象连续
  - **🚩 隔离场景**: 多场景独立处理
  - **🔄 转换**: 图层转换模式
  - **📄 TXT**: 导出为文本文件

#### 4. 执行操作
- **🔍 解析**: 分析文件结构
- **▶️ 执行**: 开始转换处理

### 命令行使用

```bash
# 基本用法
python layerchange.py input.aup2 output.aup2

# 指定场景和图层
python layerchange.py input.aup2 output.aup2 --scene_id 0 --target_layer 1

# 启用帧范围调整
python layerchange.py input.aup2 output.aup2 --adjust_frames

# 导出为TXT文件
python layerchange.py input.aup2 output.txt --extract
```

### 📥 下载最新版本

#### 💾 **可执行文件下载**
访问 releases 页面下载对应版本：

```bash
# 🔗 最新版本下载链接
https://github.com/[username]/aviutl2_layerchange/releases/latest

# 📦 文件列表:
# - aup2_layerchange_gui_zh.exe (中文紧凑版 - 推荐)
# - aup2_layerchange_gui_en.exe (英文国际化版)
# - aup2_layerchange_gui_jp.exe (日文优化版)
```

#### 📋 **版本选择建议**
| 用户类型 | 推荐版本 | 优势 |
|---------|----------|------|
| **🇨🇳 中文用户** | 中文版 (zh) | 界面最简洁，高效操作 |
| **🇺🇸 英文用户** | 英文版 (en) | 国际化标准设计 |
| **🇯🇵 日文用户** | 日文版 (jp) | 日语文字优化显示 |

### 命令行参数说明

```
positional arguments:
  input_path            输入AUP2文件路径
  output_path           输出文件路径

optional arguments:
  -h, --help            显示帮助信息
  --scene_id SCENE_ID   指定场景ID (默认: None)
  --target_layer TARGET_LAYER
                        目标图层 (默认: 0)
  --adjust_frames       启用帧范围调整
  --extract             导出为TXT格式
```

## 🎨 界面特性

### 中文紧凑版 (gui.py)
- 尺寸: 800×500 像素
- 特点: 文字精炼，界面紧凑高效
- 适用场景: 对中文用户友好，屏幕空间有限时使用

### 英文标准版 (gui_en.py)
- 尺寸: 800×500 像素
- 特点: 国际化设计，文字简洁清晰
- 适用场景: 英文用户或国际化环境

### 日文優化版 (gui_jp.py)
- 尺寸: 800×500 像素
- 特点: 日语界面友好，文字高度精炼
- 适用场景: 日语用户或特定区域使用

## 🏗️ 项目结构

```
aviutl2_layerchange/
├── gui.py              # 中文图形界面 (紧凑版)
├── gui_en.py           # 英文图形界面 (紧凑版)
├── gui_jp.py           # 日文图形界面 (紧凑版)
├── layerchange.py      # 核心转换功能模块
├── aup2_parser/        # AUP2文件解析器模块
│   ├── __init__.py
│   └── aup2_parser.py
├── test.aup2          # 测试用AUP2文件
├── pyproject.toml     # 项目配置
├── uv.lock           # 包锁定文件
├── output/           # 编译可执行文件目录
│   ├── aup2_layerchange_gui_zh.exe   # 中文版可执行文件
│   ├── aup2_layerchange_gui_en.exe   # 英文版可执行文件
│   └── aup2_layerchange_gui_jp.exe   # 日文版可执行文件
├── README.md         # 项目说明 (本文档) 🇨🇳
├── README_en.md      # English Documentation 🇺🇸
├── README_jp.md      # 日本語ドキュメント 🇯🇵
└── .gitignore       # Git忽略文件
```

## 🛠️ 技术栈

### 核心技术
- **GUI框架**: PySide6 (Qt6绑定)
- **编程语言**: Python 3.9+
- **包管理**: uv / pip
- **版本控制**: Git

### 开发依赖
- `PySide6`: 高性能GUI框架
- `pathlib`: 现代化路径处理
- `typing`: 类型注解支持

## 🔧 开发模式

### 环境设置
```bash
# 创建开发环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e .
pip install pytest black flake8  # 开发工具
```

### 运行测试
```bash
pytest tests/ -v
```

### 打包应用程序
```bash
# 使用PyInstaller打包所有GUI版本
pyinstaller --onefile --windowed gui.py     # 中文版
pyinstaller --onefile --windowed gui_en.py  # 英文版
pyinstaller --onefile --windowed gui_jp.py  # 日文版

# 输出文件会保存在 dist/ 目录下
# 重命名为规范的文件名后放入 output/ 目录
```

## 📝 使用示例

### 示例1: 基础转换
```bash
# 将所有对象移动到图层0，并调整帧范围
python layerchange.py input.aup2 output.aup2 --target_layer 0 --adjust_frames
```

### 示例2: 场景特定转换
```bash
# 只处理场景0中的对象，转换为图层1
python layerchange.py input.aup2 output.aup2 --scene_id 0 --target_layer 1
```

### 示例3: 数据导出
```bash
# 将AUP2文件转换为文本格式
python layerchange.py input.aup2 output.txt --extract
```

## 🚀 快速使用指南

### 对于新用户

#### ✨ **5分钟上手**

1. **下载**: 从 releases 页面下载 `aup2_layerchange_gui_zh.exe`
2. **运行**: 双击运行程序，窗口大小约 800×500 像素
3. **选择文件**:
   - 点击"📂 选择"选择输入AUP2文件
   - 点击"💾 保存"选择输出文件位置
4. **设置参数**:
   - 场景留空=处理所有场景
   - 图层输入0=移动到第0层
5. **执行**: 点击"▶️ 执行"按钮开始处理
6. **完成**: 进度显示在界面的状态栏

#### 🎯 **常见场景**

| 使用场景 | 推荐参数 | 说明 |
|---------|----------|------|
| **批量整理** | 全场景，目标图层0，连续帧开 | 统一整理项目中的对象图层 |
| **场景隔离** | 指定场景，隔离处理开 | 保持各场景时间线独立 |
| **数据查看** | 导出TXT | 查看AUP2文件内部结构 |

#### ❓ **遇到问题？**
- 确保输入文件是有效的AUP2格式
- 检查输出路径是否有写入权限
- 如界面显示异常，请点击界面右下角的"🔬 确认"按钮进行验证

## 🤝 贡献指南

欢迎提交Issues和Pull Requests！

### 代码规范
- 使用Black格式化代码
- 类型注解是必须的
- 提交前请运行测试

### 翻译贡献
如果您想为其他语言版本做出贡献：
1. Fork此仓库
2. 创建新的GUI文件 (如 `gui_de.py` 德国版)
3. 遵循相同的设计模式和文字长度限制
4. 提交Pull Request

## 📜 许可证

本项目采用 **MIT 许可证** - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

**gasdyueer**
- GitHub: [@gasdyueer](https://github.com/gasdyueer)
- Email: gasdyueer@example.com

## 🙏 致谢

- AviUtl社区的开发者们
- PySide6项目的贡献者
- 开源社区的支持者

## 📞 支持

如遇到问题或有建议，请：

1. 查看 [Issues](../../issues) 页面
2. 提交问题反馈
3. 阅读本文档和示例

---

⭐ 如果这个项目对你有帮助，请给它一个星标!