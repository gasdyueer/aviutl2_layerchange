# AviUtl レイヤー変換ツール

[![PySide6](https://img.shields.io/badge/PySide6-6.6.2-green)](https://pypi.org/project/PySide6/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

コンパクトな GUI デザインを備えた強力な AviUtl (AUP2) のファイルレイヤー処理ツール。

## 🌍 言語選択
- [简体中文](./README.md) | [English](./README_en.md) | [日本語](./README_jp.md)

## ✨ 主な機能

### 🎯 コア機能
- レイヤー変換 (シーンオブジェクト)
- フレーム範囲の最適化
- マルチシーンの隔離処理
- テキストでのエクスポート (データ閲覧用)

### 🎨 多言語なコンパクト GUI
- 🇯🇵 **日本語版 (gui_jp.py)** - **おすすめ**
- 🇨🇳 中国語版 (gui.py)
- 🇺🇸 英語版 (gui_en.py)

### 🛠️ 主な利点
- 🚀 PySide6 で高性能
- 🎛️ 柔軟なパラメータ設定
- 🔍 スマートなデータ検証
- 📊 リアルタイムな解析

## 🖥️ インターフェース
- **ウィンドウサイズ**: 800×500 ピクセル
- **文字長さ**: 2-4文字
- **デザイン**: 効率的な最小限レイアウト

## 📦 クイックスタート

### 方法1: ビルド済みの実行ファイル
```bash
# ダウンロードして直接実行
aup2_layerchange_gui_jp.exe
```

### 方法2: ソースから実行
```bash
# 依存パッケージインストール
pip install -r requirements.txt

# GUI起動
python gui_jp.py
```

## 🚀 使用ガイド

### GUI オプションの説明

#### ファイル設定
- **入力:** AUP2 のソースファイルを選択
- **出力:** 出力先を選択

#### パラメータ設定
- **シーン:** 対象シーンID (空白=すべてのシーン)
- **レイヤー:** ターゲットレイヤー番号 (初期値: 0)

#### 操作オプション
- **連続フレーム:** フレームの範囲を調整して連続化
- **隔離:** シーン別で独立にて処理
- **変換:** レイヤー変換モード
- **テキスト:** テキストファイルでエクスポート

#### 実行操作
- **解析:** ファイル構造を解析
- **実行:** 変換処理の開始

### コマンドライン
```bash
# 基本的な使用方法
python layerchange.py input.aup2 output.aup2

# 高度なオプション
python layerchange.py input.aup2 output.aup2 --scene_id 0 --target_layer 1 --adjust_frames
```

## 📥 ダウンロード

| 表示言語 | ファイル名 | サイズ | ダウンロード |
|---------|----------|------|------------|
| 🇯🇵 **日本語 (おすすめ)** | `aup2_layerchange_gui_jp.exe` | ~20MB | [ダウンロード]() |
| 🇨🇳 中国語 | `aup2_layerchange_gui_zh.exe` | ~20MB | [ダウンロード]() |
| 🇺🇸 英語 | `aup2_layerchange_gui_en.exe` | ~20MB | [ダウンロード]() |

## 📋 システム要件

- Windows 10/11
- メモリ 512MB 以上
- 空き容量 100MB 以上
- Python 3.9+ (ソースインストール時)

## 🎯 使用例

| 使用ケース | パラメータ | 説明 |
|----------|-----------|------|
| **一括整理** | 全シーン、レイヤー0、連続ファイル ON | プロジェクト内オブジェクト整理 |
| **シーン隔離** | 指定シーン、隔離 ON | 各シーンリトライト保持 |
| **データ確認** | テキストをエクスポート | ファイル内部構造閲覧 |

## 🏗️ プロジェクト構造

```
├── gui_jp.py           # 日本語の GUI (コンパクト、おすすめ)
├── gui.py             # 中国語の GUI (コンパクト)
├── gui_en.py          # 英語の GUI (コンパクト)
├── layerchange.py     # コア処理モジュール
├── README_jp.md       # 日本語のドキュメント
└── output/           # ビルド実行ファイル
```

## 🛠️ 技術スタック

- **GUI フレームワーク**: PySide6 (Qt6 バインディング)
- **プログラミング言語**: Python 3.9+
- **ビルドツール**: PyInstaller、uv/pip

## 🤝 開発協力

Issues と Pull Requests を歓迎します！

### 機能のリクエスト
- 🔧 インターフェースの改善
- 🌍 追加言語のサポート
- ⚡ パフォーマンスの最適化

## 📄 ライセンス

MIT ライセンス - [LICENSE](LICENSE) を参照

## 👨‍💻 開発者

gasdyueer

---

⭐ お役に立てたなら Star をお願いします！
