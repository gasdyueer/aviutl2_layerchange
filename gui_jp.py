"""
AviUtlレイヤー変換 v1.0 - PySide6 GUI

AUP2ファイル処理コンパクト版:
- シーンオブジェクトのレイヤー変換
- フレーム範囲調整
- TXT抽出

Author: gasdyueer
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QCheckBox, QRadioButton, QButtonGroup, QGroupBox,
    QTabWidget, QTextEdit, QFileDialog, QMessageBox, QFrame, QScrollArea,
    QGridLayout, QSplitter
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont

# 現在のディレクトリと親ディレクトリをパスに追加してモジュールをインポート
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

try:
    from .layerchange import transform_layer_in_scene, extract_text_to_txt, validate_file_paths, validate_scene_and_layer_ids
    from .aup2_parser import AUP2Parser
except ImportError:
    # 相対インポートが失敗した場合、絶対インポートを使用
    import layerchange
    transform_layer_in_scene = layerchange.transform_layer_in_scene
    extract_text_to_txt = layerchange.extract_text_to_txt
    validate_file_paths = layerchange.validate_file_paths
    validate_scene_and_layer_ids = layerchange.validate_scene_and_layer_ids

    # aup2_parser をインポート
    import aup2_parser
    AUP2Parser = aup2_parser.AUP2Parser


transform_layer_in_scene = layerchange.transform_layer_in_scene
extract_text_to_txt = layerchange.extract_text_to_txt
validate_file_paths = layerchange.validate_file_paths
validate_scene_and_layer_ids = layerchange.validate_scene_and_layer_ids

class LayerChangeGUIPySide6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LayerChg v1.0")
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(700, 400)

        # フォント定数を定義（保守性のために）
        self.default_font = QFont("Meiryo", 8)
        self.default_font_bold = QFont("Meiryo", 8, QFont.Weight.Bold)
        self.title_font = QFont("Meiryo", 9, QFont.Weight.Bold)
        self.title_font_large = QFont("Meiryo", 9, QFont.Weight.Bold)
        self.status_font = QFont("Meiryo", 8)
        self.textbox_font = QFont("Meiryo", 8)

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # 中央ウィジェットを作成
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # メイン水平レイアウトを作成
        main_layout = QHBoxLayout(central_widget)

        # QSplitterを使用して左右パネルを分割
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左側操作パネルを作成
        self.setup_left_panel(splitter)

        # 右側パーステキストパネルを作成
        self.setup_right_panel(splitter)

        # メインレイアウトにスプリッターを追加
        main_layout.addWidget(splitter)

        # 初期比率を設定 (左:右 = 5:3)
        splitter.setSizes([480, 320])

    def setup_left_panel(self, splitter):
        # 左側操作パネルを作成
        left_panel = QWidget()
        splitter.addWidget(left_panel)

        # メインレイアウトを作成
        main_layout = QVBoxLayout(left_panel)

        # スクロールエリアを作成
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)

        # ファイル選択エリア
        self.setup_file_section(scroll_layout)

        # パラメータ構成エリア
        self.setup_params_section(scroll_layout)

        # 操作オプションエリア
        self.setup_operations_section(scroll_layout)

        # 操作ボタンエリア
        self.setup_buttons_section(scroll_layout)

    def setup_file_section(self, layout):
        file_frame = QGroupBox("📁 ファイル")
        file_frame.setFont(self.title_font)
        file_layout = QVBoxLayout(file_frame)

        # 入力ファイル
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("入:"))
        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText("選択...")
        input_layout.addWidget(self.input_entry)
        self.input_button = QPushButton("📂 選択")
        input_layout.addWidget(self.input_button)
        file_layout.addLayout(input_layout)

        # 出力ファイル
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("出:"))
        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("保存...")
        output_layout.addWidget(self.output_entry)
        self.output_button = QPushButton("💾 保存")
        output_layout.addWidget(self.output_button)
        file_layout.addLayout(output_layout)

        layout.addWidget(file_frame)

    def setup_params_section(self, layout):
        params_frame = QGroupBox("⚙️ 設定")
        params_frame.setFont(self.title_font)
        params_layout = QVBoxLayout(params_frame)

        # シーンID
        scene_layout = QHBoxLayout()
        scene_layout.addWidget(QLabel("シーン:"))
        self.scene_id_entry = QLineEdit()
        self.scene_id_entry.setPlaceholderText("全シーン")
        scene_layout.addWidget(self.scene_id_entry)
        params_layout.addLayout(scene_layout)

        # ターゲットレイヤー
        layer_layout = QHBoxLayout()
        layer_layout.addWidget(QLabel("レイヤー:"))
        self.target_layer_entry = QLineEdit("0")
        layer_layout.addWidget(self.target_layer_entry)
        params_layout.addLayout(layer_layout)

        layout.addWidget(params_frame)

    def setup_operations_section(self, layout):
        operations_frame = QGroupBox("🔧 オプション")
        operations_frame.setFont(self.title_font)
        operations_layout = QVBoxLayout(operations_frame)

        # フレーム調整チェックボックス
        self.adjust_frames_checkbox = QCheckBox("🎬 連続フ")
        self.adjust_frames_checkbox.setChecked(True)
        operations_layout.addWidget(self.adjust_frames_checkbox)

        # マルチシーン隔離処理チェックボックス
        self.scenes_isolation_checkbox = QCheckBox("🚩 隔離")
        self.scenes_isolation_checkbox.setChecked(True)
        operations_layout.addWidget(self.scenes_isolation_checkbox)

        # 操作タイプラジオボタン
        operation_group = QGroupBox()
        operation_layout = QHBoxLayout(operation_group)

        self.operation_group = QButtonGroup(self)
        self.transform_radio = QRadioButton("🔄 変換")
        self.extract_radio = QRadioButton("📄 TXT")
        self.transform_radio.setChecked(True)

        self.operation_group.addButton(self.transform_radio, 0)
        self.operation_group.addButton(self.extract_radio, 1)

        operation_layout.addWidget(self.transform_radio)
        operation_layout.addWidget(self.extract_radio)
        operations_layout.addWidget(operation_group)

        layout.addWidget(operations_frame)

    def setup_buttons_section(self, layout):
        buttons_frame = QWidget()
        buttons_layout = QVBoxLayout(buttons_frame)

        # 操作ボタン
        button_layout = QHBoxLayout()
        self.parse_button = QPushButton("🔍 解析")
        self.parse_button.setFont(self.default_font_bold)
        button_layout.addWidget(self.parse_button)

        self.execute_button = QPushButton("▶️ 実行")
        self.execute_button.setFont(self.default_font_bold)
        button_layout.addWidget(self.execute_button)
        buttons_layout.addLayout(button_layout)

        # ステータス情報
        self.status_label = QLabel("✓ 準備OK")
        self.status_label.setFont(self.status_font)
        buttons_layout.addWidget(self.status_label)

        layout.addWidget(buttons_frame)

        # シーンID入力イベント接続
        self.scene_id_entry.textChanged.connect(self.update_scenes_isolation_visibility)

        # 初期隔離オプション表示更新
        self.update_scenes_isolation_visibility()

    def setup_right_panel(self, splitter):
        # 右側パーステキストパネルを作成
        right_panel = QWidget()
        splitter.addWidget(right_panel)

        analysis_layout = QVBoxLayout(right_panel)

        analysis_label = QLabel("📊 結果")
        analysis_label.setFont(self.title_font)
        analysis_layout.addWidget(analysis_label)

        self.structure_text = QTextEdit()
        self.structure_text.setFont(self.textbox_font)
        analysis_layout.addWidget(self.structure_text)

        # 正しい表示を確保するための検証ボタン追加
        validate_button = QPushButton("🔬 確認")
        validate_button.clicked.connect(self.validate_parsing)
        validate_button.setFont(self.default_font_bold)
        analysis_layout.addWidget(validate_button)

        # 初期テキスト設定
        initial_content = """💡 解析結果

AUP2ファイルを選択、
解析ボタンをクリック。

分析内容:
📁プロジェクト情報
🎭シーン設定
🎯オブジェクト情報

💡 ヒント:
- レイヤー値確認
- データから抽出

💡 隔離処理:
フレーム有効時、
個別シーン配置。
"""
        self.structure_text.setPlainText(initial_content)

    def setup_connections(self):
        self.input_button.clicked.connect(self.select_input_file)
        self.output_button.clicked.connect(self.select_output_file)
        self.parse_button.clicked.connect(self.parse_file_structure)
        self.execute_button.clicked.connect(self.execute_operation)
        self.adjust_frames_checkbox.stateChanged.connect(self.update_scenes_isolation_visibility)

    @Slot()
    def validate_parsing(self):
        """パーサーが正しく動作しているかを検証し、詳細なデバッグ情報を表示"""
        input_path = self.input_entry.text().strip()
        if not input_path:
            QMessageBox.warning(self, "エラー", "入力ファイルを選択")
            return

        try:
            # ファイル構造を解析
            parser = AUP2Parser.from_file(input_path)
            data = parser.parse()

            # 検証レポート生成
            validation_lines = []
            validation_lines.append("=== 解析検証レポート ===\n")
            validation_lines.append(f"📁 入: {input_path}\n")

            # レイヤー分布をチェック
            layer_distribution = {}
            object_keys = [k for k in data if k.startswith('object.')]

            validation_lines.append("🎯 レイヤー確認:\n")
            for obj_key in sorted(object_keys, key=lambda x: int(x.split('.')[1])):
                obj_data = data[obj_key]
                obj_id = obj_key.split('.')[1]
                layer = obj_data.get('layer', 'MISSING')
                frame = obj_data.get('frame', [0, 0])
                scene = obj_data.get('scene', 0)

                # 統計更新
                if isinstance(layer, int):
                    layer_distribution[layer] = layer_distribution.get(layer, 0) + 1

                validation_lines.append(f"   🔵 オブジ{obj_id}: l={layer}, s={scene}, f={frame}")

            validation_lines.append("\n📊 レイヤー統計:")
            for layer, count in sorted(layer_distribution.items()):
                validation_lines.append(f"   レイヤー{layer}: {count}個")

            # レイヤー0以外が存在するかチェック
            non_zero_layers = [l for l in layer_distribution.keys() if l != 0]
            if non_zero_layers:
                validation_lines.append(f"\n✅ 非ゼロ: {sorted(non_zero_layers)}")
            else:
                validation_lines.append("\n⚠️ 全0")

            # 結果表示
            result_text = '\n'.join(validation_lines)
            self.structure_text.setPlainText(result_text)

            self.status_label.setText("検証完了")
            self.status_label.setStyleSheet("color: green;")

        except Exception as e:
            error_text = f"検証エラー:\n{str(e)}\n\n形式とファイルを確認。"
            self.structure_text.setPlainText(error_text)
            self.status_label.setText("検証失敗")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "検証エラー", f"エラー:\n{str(e)}")

    @Slot()
    def update_scenes_isolation_visibility(self):
        scene_id_str = self.scene_id_entry.text().strip()
        adjust_frames = self.adjust_frames_checkbox.isChecked()

        # 隔離オプション表示条件：シーンID空欄かつフレーム調整有効
        should_show = (scene_id_str == "" and adjust_frames)
        self.scenes_isolation_checkbox.setVisible(should_show)

    @Slot()
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "AUP2ファイル選択",
            "",
            "AUP2 files (*.aup2);;All files (*.*)"
        )
        if file_path:
            self.input_entry.setText(file_path)

    @Slot()
    def select_output_file(self):
        operation = "extract" if self.extract_radio.isChecked() else "transform"
        if operation == "extract":
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "TXT保存",
                "",
                "Text files (*.txt);;All files (*.*)"
            )
            if file_path and not file_path.lower().endswith('.txt'):
                file_path += '.txt'
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "AUP2保存",
                "",
                "AUP2 files (*.aup2);;All files (*.*)"
            )
        if file_path:
            self.output_entry.setText(file_path)

    @Slot()
    def parse_file_structure(self):
        input_path = self.input_entry.text().strip()
        if not input_path:
            QMessageBox.warning(self, "エラー", "入力ファイルを選択")
            return

        try:
            # ファイル構造を解析
            parser = AUP2Parser.from_file(input_path)
            data = parser.parse()

            # 構造情報生成
            structure_lines = []
            structure_lines.append("=== AUP2 ファイル分析 ===\n")

            # プロジェクト情報
            if 'project' in data:
                structure_lines.append("📁 PROJECT:")
                for key, value in data['project'].items():
                    structure_lines.append(f"   {key}: {value}")

            # シーン情報
            scene_keys = [k for k in data if k.startswith('scene.')]
            if scene_keys:
                structure_lines.append(f"\n🎭 SCENES ({len(scene_keys)} シーン):")
                for scene_key in sorted(scene_keys):
                    scene_id = scene_key.split('.')[1]
                    structure_lines.append(f"   📺 シーン{scene_id}:")
                    if scene_key in data:
                        for key, value in data[scene_key].items():
                            if key in ['scene', 'name', 'video.width', 'video.height', 'cursor.frame']:
                                structure_lines.append(f"      {key}: {value}")

            # オブジェクト情報
            object_keys = [k for k in data if k.startswith('object.')]
            if object_keys:
                objects_by_scene = {}
                for obj_key in object_keys:
                    obj_data = data[obj_key]
                    scene_id = obj_data.get('scene', 0)
                    if scene_id not in objects_by_scene:
                        objects_by_scene[scene_id] = []
                    objects_by_scene[scene_id].append(obj_key)

                structure_lines.append(f"\n🎯 OBJECTS ({len(object_keys)} オブジェクト):")
                for scene_id in sorted(objects_by_scene.keys()):
                    scene_objects = objects_by_scene[scene_id]
                    structure_lines.append(f"   📋 シーン{scene_id}: {len(scene_objects)}個")

                    # IDでソートしてオブジェクト詳細を表示
                    sorted_objects = sorted(scene_objects, key=lambda x: int(x.split('.')[1]))
                    for obj_key in sorted_objects:
                        obj_id = obj_key.split('.')[1]
                        obj_data = data[obj_key]
                        frame = obj_data.get('frame', [0, 0])
                        layer = obj_data.get('layer', 0)  # デフォルトは0
                        structure_lines.append(f"      🔵 オブジ{obj_id}: l={layer}, f={frame}")

                        # GUI表示にデバッグ情報を追加
                        if 'effects' in obj_data:
                            effects_count = len(obj_data['effects'])
                            structure_lines.append(f"         └─ Efx: {effects_count}")

            # 結果表示
            result_text = '\n'.join(structure_lines)
            self.structure_text.setPlainText(result_text)

            self.status_label.setText("解析完了")
            self.status_label.setStyleSheet("color: green;")

        except Exception as e:
            self.structure_text.setPlainText(f"解析エラー:\n{str(e)}")
            self.status_label.setText("解析失敗")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "解析エラー", f"エラー:\n{str(e)}")

    @Slot()
    def execute_operation(self):
        input_path = self.input_entry.text().strip()
        output_path = self.output_entry.text().strip()

        if not input_path:
            QMessageBox.warning(self, "エラー", "入力ファイルを選択")
            return
        if not output_path:
            QMessageBox.warning(self, "エラー", "出力ファイルを選択")
            return

        is_extract = self.extract_radio.isChecked()

        # デバッグ情報
        print("=== GUI入力情報 ===")
        print(f"入: {input_path}")
        print(f"出: {output_path}")
        print(f"操作: {'TXT' if is_extract else '変換'}")

        try:
            if is_extract:
                extract_text_to_txt(input_path, output_path)
                self.status_label.setText(f"保存: {os.path.basename(output_path)}")
                self.status_label.setStyleSheet("color: green;")
                QMessageBox.information(self, "成功", f"TXT保存: {output_path}")
            else:
                # パラメータ解析
                scene_id_str = self.scene_id_entry.text().strip()
                scene_id = None if scene_id_str == "" else int(scene_id_str)

                target_layer_str = self.target_layer_entry.text().strip()
                target_layer = int(target_layer_str)

                adjust_frames = self.adjust_frames_checkbox.isChecked()

                # デバッグ情報変換パラメータ出力
                print(f"シーン: {scene_id}")
                print(f"ターゲット: {target_layer}")
                print(f"調整: {adjust_frames}")
                print(f"隔離: {self.scenes_isolation_checkbox.isChecked() if adjust_frames and scene_id is None else 'N/A'}")
                print("=======\n")

                # 変換関数呼び出し
                transform_layer_in_scene(
                    input_path,
                    output_path,
                    scene_id=scene_id,
                    target_layer=target_layer,
                    adjust_frames=adjust_frames
                )

                self.status_label.setText(f"成功: {os.path.basename(output_path)}")
                self.status_label.setStyleSheet("color: green;")
                QMessageBox.information(self, "成功", f"変換成功! 保存: {output_path}")

        except FileNotFoundError as e:
            self.status_label.setText(f"ファイルエラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "エラー", str(e))
        except ValueError as e:
            self.status_label.setText(f"値エラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "値エラー", str(e))
        except Exception as e:
            self.status_label.setText(f"実行エラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "実行エラー", f"エラー:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    window = LayerChangeGUIPySide6()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()