# AviUtl Layer Change Tool

[![PySide6](https://img.shields.io/badge/PySide6-6.6.2-green)](https://pypi.org/project/PySide6/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Powerful AviUtl (AUP2) file layer processing tool with compact GUI design.

## 🌍 Language Selection
- [简体中文](./README.md) | [English](./README_en.md) | [日本語](./README_jp.md)

## ✨ Quick Features

### 🎯 Core Functions
- Layer conversion for scene objects
- Frame range optimization
- Multi-scene isolation processing
- TXT export for data viewing

### 🎨 Multi-language Compact GUI
- 🇺🇸 English version (gui_en.py) - **Recommended**
- 🇨🇳 Chinese version (gui.py)
- 🇯🇵 Japanese version (gui_jp.py)

### 🛠️ Key Advantages
- 🚀 High performance with PySide6
- 🎛️ Flexible parameter configuration
- 🔍 Smart data validation
- 📊 Real-time structure analysis

## 🖥️ Compact Interface
- **Window Size**: 800×500 pixels
- **Text Length**: 2-4 characters/words
- **Design**: Efficient, minimal layout

## 📦 Quick Start

### Option 1: Pre-built Executables
```bash
# Download and run directly (Windows)
aup2_layerchange_gui_en.exe
```

### Option 2: From Source Code
```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI
python gui_en.py
```

## 🚀 Usage Guide

### GUI Interface

#### File Settings
- **Files**: Select input/output files
- **In:** Choose AUP2 source file
- **Out:** Set output location

#### Parameters
- **Scene:** Target scene ID (empty = all scenes)
- **Layer:** Target layer number (default: 0)

#### Operations
- **Cont. Frames**: Adjust frame range to make continuous
- **Isolate Scenes**: Independent per-scene processing
- **Convert**: Layer conversion mode
- **TXT**: Export to TXT

#### Execution
- **Parse**: Analyze file structure
- **Run**: Start conversion process

### Command Line
```bash
# Basic usage
python layerchange.py input.aup2 output.aup2

# Advanced options
python layerchange.py input.aup2 output.aup2 --scene_id 0 --target_layer 1 --adjust_frames
```

## 📥 Downloads

| Language Version | File Name | Size | Download |
|-----------------|-----------|------|----------|
| 🇨🇳 Chinese (Recommended) | `aup2_layerchange_gui_zh.exe` | ~20MB | [Download]() |
| 🇺🇸 English | `aup2_layerchange_gui_en.exe` | ~20MB | [Download]() |
| 🇯🇵 Japanese | `aup2_layerchange_gui_jp.exe` | ~20MB | [Download]() |

## 📋 System Requirements

- Windows 10/11
- 512MB RAM
- 100MB free disk space
- Python 3.9+ (for source installation)

## 🎯 Common Scenarios

| Use Case | Parameters | Description |
|----------|------------|-------------|
| **Bulk Organization** | All scenes, Layer 0, Cont. Frames ON | Organize console objects |
| **Scene Isolation** | Specific scene, Isolate ON | Keep independent timelines |
| **Data Review** | Export TXT | View internal file structure |

## 🏗️ Project Structure

```
├── gui_en.py           # English GUI (compact, recommended)
├── gui.py             # Chinese GUI (compact)
├── gui_jp.py          # Japanese GUI (compact)
├── layerchange.py     # Core processing module
├── README_en.md       # English documentation
└── output/           # Pre-compiled executables
```

## 🛠️ Technology Stack

- **GUI Framework**: PySide6 (Qt6 bindings)
- **Programming Language**: Python 3.9+
- **Build Tools**: PyInstaller, uv/pip

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Feature Requests
- 🔧 Interface improvements
- 🌍 Additional language support
- ⚡ Performance optimizations

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 👨‍💻 Author

gasdyueer

---

⭐ Star this project if it helps you!