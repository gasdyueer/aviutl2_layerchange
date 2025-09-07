# AviUtl レイヤー変換ツール

[![PySide6](https://img.shields.io/badge/PySide6-6.6.2-green)](https://pypi.org/project/PySide6/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

AviUtl（AUP2）ファイル処理ツール。コンパクトな日本語インターフェースで使いやすく設計。

## 🌍 言語選択
- [简体中文](./README.md) | [English](./README_en.md) | [日本語](./README_jp.md)

## ✨ 主な機能

### 🎯 コア機能
- レイヤー変換（シーンオブジェクト）
- フレーム範囲最適化
- マルチシーン隔離処理
- TXTエクスポート（データ閲覧用）

### 🎨 多言語コンパクトGUI
- 🇯🇵 **日本語版 (gui_jp.py)** - **おすすめ**
- 🇨🇳 中国語版 (gui.py)
- 🇺🇸 英語版 (gui_en.py)

### 🛠️ 主な利点
- 🚀 PySide6で高性能
- 🎛️ 柔軟なパラメータ設定
- 🔍 スマートなデータ検証
- 📊 リアルタイム解析

## 🖥️ インターフェース
- **ウィンドウサイズ**: 800×500 ピクセル
- **文字長さ**: 2-4文字
- **デザイン**: 効率的な最小限レイアウト

## 📦 クイックスタート

### 方法1: ビルド済み実行ファイル
```bash
# ダウンロードして直接実行
aup2_layerchange_gui_jp.exe
```

### 方法2: ソースから
```bash
# 依存パッケージインストール
pip install -r requirements.txt

# GUI起動
python gui_jp.py
```

## 🚀 使用ガイド

### GUI オプション説明

#### ファイル設定
- **入:** AUP2ソースファイル選択
- **出:** 出力場所設定

#### パラメータ設定
- **シーン:** 対象シーンID（空白=全シーン）
- **レイヤー:** ターゲットレイヤー番号（初期値: 0）

#### 操作オプション
- **連続フ:** フレーム範囲調整して連続化
- **隔離:** シーン別独立処理
- **変換:** レイヤー変換モード
- **TXT:** TXT形式でエクスポート

#### 実行操作
- **解析:** ファイル構造解析
- **実行:** 変換処理開始

### コマンドライン
```bash
# 基本使用
python layerchange.py input.aup2 output.aup2

# 高性能オプション
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
- メモリ 512MB以上
- 空きディスク 100MB以上
- Python 3.9+ （ソースインストール時）

## 🎯 使用例

| 使用ケース | パラメータ | 説明 |
|----------|-----------|------|
| **一括整理** | 全シーン、レイヤー0、連続フON | プロジェクト内オブジェクト整理 |
| **シーン隔離** | 指定シーン、隔離ON | 各シーンリトライト保持 |
| **データ確認** | TXTエクスポート | ファイル内部構造閲覧 |

## 🏗️ プロジェクト構造

```
├── gui_jp.py           # 日語GUI（コンパクト、おすすめ）
├── gui.py             # 中国語GUI（コンパクト）
├── gui_en.py          # 英語GUI（コンパクト）
├── layerchange.py     # コア処理モジュール
├── README_jp.md       # 日語ドキュメント
└── output/           # ビルド実行ファイル
```

## 🛠️ 技術スタック

- **GUIフレームワーク**: PySide6 (Qt6バインディング)
- **プログラミング言語**: Python 3.9+
- **ビルドツール**: PyInstaller, uv/pip

## 🤝 開発協力

IssuesとPull Requests大歓迎！

### 機能リクエスト
- 🔧 インターフェース改善
- 🌍 追加言語サポート
- ⚡ パフォーマンス最適化

## 📄 ライセンス

MITライセンス - [LICENSE](LICENSE)参照

## 👨‍💻 作者

gasdyueer

---

⭐ 役に立ったらスターお願いします！