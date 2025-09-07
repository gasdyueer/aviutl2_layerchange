# AviUtl Layer Change Tool

[![PySide6](https://img.shields.io/badge/PySide6-6.6.2-green)](https://pypi.org/project/PySide6/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Powerful AviUtl (AUP2) file layer processing tool with compact GUI design.

## 🖼️ Feature Demonstration

When we import multiple media files at once in AviUtl, these files are placed in multiple layers by default, which makes linear editing inconvenient. Therefore, this tool achieves the goal of placing all objects in a specified layer within a scene by changing the specific data in the AUP2 project file through external tools, avoiding tedious drag-and-drop operations.

This method requires the use of the [parser](https://github.com/gasdyueer/aviutl2_aup2_parser) I wrote to parse, modify, and reorganize the AUP2 data structure. Currently, the [parser](https://github.com/gasdyueer/aviutl2_aup2_parser) is somewhat complex with extensive regular expression matching. Some data may fail to match, and while I've resolved some special data matching issues, there may be other matching problems I haven't discovered. The tool is usable in non-extreme scenarios.

The following shows the structure of AUP2 data organization:

```
[project] Global information

[scene.0] Scene 0 information
    [0] Scene 0 layer object ID 0 (layer=0, scene=0, frame=0,80)
        [0.0] Effect 1
        [0.1] Effect 2
    [1] Scene 0 layer object ID 1 (layer=0, scene=0, frame=81,161)
        [1.0] Effect 1
        [1.1] Effect 2
    [2] Scene 0 layer object ID 2 (layer=1, scene=0, frame=0,80, focus=1)
        [2.0] Effect 1
        [2.1] Effect 2
        [2.2] Effect 3

[scene.1] Scene 1 information
    [3] Scene 1 layer object ID 3 (layer=0, scene=1, frame=0,80)
        [3.0] Effect 1
        [3.1] Effect 2
    [4] Scene 1 layer object ID 4 (layer=1, scene=1, frame=0,80)
        [4.0] Effect 1
        [4.1] Effect 2
        [4.2] Effect 3
    [5] Scene 1 layer object ID 5 (layer=1, scene=1, frame=81,161, focus=1)
        [5.0] Effect 1
        [5.1] Effect 2

... (Subsequent scenes and their layer objects repeat this pattern)
```

Hope this inspires you.

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