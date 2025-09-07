"""
AviUtl Layer Change Tool v1.0 - PySide6 GUI

AUP2 レイヤー処理のコンパクト版:
- シーンオブジェクトのレイヤーを変換
- フレーム範囲を調整
- テキストに抽出

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

# Add current directory and parent directory to path for module import
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

try:
    from .layerchange import transform_layer_in_scene, extract_text_to_txt, validate_file_paths, validate_scene_and_layer_ids
    from .aup2_parser import AUP2Parser
except ImportError:
    # If relative import fails, use absolute import
    import layerchange
    transform_layer_in_scene = layerchange.transform_layer_in_scene
    extract_text_to_txt = layerchange.extract_text_to_txt
    validate_file_paths = layerchange.validate_file_paths
    validate_scene_and_layer_ids = layerchange.validate_scene_and_layer_ids

    # Import aup2_parser
    import aup2_parser
    AUP2Parser = aup2_parser.AUP2Parser


transform_layer_in_scene = layerchange.transform_layer_in_scene
extract_text_to_txt = layerchange.extract_text_to_txt
validate_file_paths = layerchange.validate_file_paths
validate_scene_and_layer_ids = layerchange.validate_scene_and_layer_ids

class LayerChangeGUIPySide6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AviUtl Layer Change Tool v1.0")
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(700, 400)

        # Define font constants for easy maintenance and modification
        self.default_font = QFont("Yu Gochic UI", 8)
        self.default_font_bold = QFont("Yu Gochic UI", 8, QFont.Weight.Bold)
        self.title_font = QFont("Yu Gochic UI", 9, QFont.Weight.Bold)
        self.title_font_large = QFont("Yu Gochic UI", 9, QFont.Weight.Bold)
        self.status_font = QFont("Yu Gochic UI", 8)
        self.textbox_font = QFont("Yu Gochic UI", 8)

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main horizontal layout
        main_layout = QHBoxLayout(central_widget)

        # Create QSplitter for splitting left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create left operation panel
        self.setup_left_panel(splitter)

        # Create right parsing text panel
        self.setup_right_panel(splitter)

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Set initial proportions (left:right = 5:3)
        splitter.setSizes([480, 320])

    def setup_left_panel(self, splitter):
        # Create left operation panel
        left_panel = QWidget()
        splitter.addWidget(left_panel)

        # Create main layout
        main_layout = QVBoxLayout(left_panel)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)

        # File selection area
        self.setup_file_section(scroll_layout)

        # Parameter configuration area
        self.setup_params_section(scroll_layout)

        # Operation options area
        self.setup_operations_section(scroll_layout)

        # Operation buttons area
        self.setup_buttons_section(scroll_layout)

    def setup_file_section(self, layout):
        file_frame = QGroupBox("📁 ファイル")
        file_frame.setFont(self.title_font)
        file_layout = QVBoxLayout(file_frame)

        # Input file
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("入力:"))
        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText("参照...")
        input_layout.addWidget(self.input_entry)
        self.input_button = QPushButton("📂 参照")
        input_layout.addWidget(self.input_button)
        file_layout.addLayout(input_layout)

        # Output file
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("出力:"))
        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("保存...")
        output_layout.addWidget(self.output_entry)
        self.output_button = QPushButton("💾 保存")
        output_layout.addWidget(self.output_button)
        file_layout.addLayout(output_layout)

        layout.addWidget(file_frame)

    def setup_params_section(self, layout):
        params_frame = QGroupBox("⚙️ パラメータ")
        params_frame.setFont(self.title_font)
        params_layout = QVBoxLayout(params_frame)

        # Scene ID
        scene_layout = QHBoxLayout()
        scene_layout.addWidget(QLabel("シーン:"))
        self.scene_id_entry = QLineEdit()
        self.scene_id_entry.setPlaceholderText("すべて")
        scene_layout.addWidget(self.scene_id_entry)
        params_layout.addLayout(scene_layout)

        # Target Layer
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

        # Frame adjustment checkbox
        self.adjust_frames_checkbox = QCheckBox("🎬 連続フレーム")
        self.adjust_frames_checkbox.setChecked(True)
        operations_layout.addWidget(self.adjust_frames_checkbox)

        # Multi-scene isolation processing checkbox
        self.scenes_isolation_checkbox = QCheckBox("🚩 シーンを隔離")
        self.scenes_isolation_checkbox.setChecked(True)
        operations_layout.addWidget(self.scenes_isolation_checkbox)

        # Operation type radio buttons
        operation_group = QGroupBox()
        operation_layout = QHBoxLayout(operation_group)

        self.operation_group = QButtonGroup(self)
        self.transform_radio = QRadioButton("🔄 変換")
        self.extract_radio = QRadioButton("📄 テキスト")
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

        # Operation buttons
        button_layout = QHBoxLayout()
        self.parse_button = QPushButton("🔍 解析")
        self.parse_button.setFont(self.default_font_bold)
        button_layout.addWidget(self.parse_button)

        self.execute_button = QPushButton("▶️ 実行")
        self.execute_button.setFont(self.default_font_bold)
        button_layout.addWidget(self.execute_button)
        buttons_layout.addLayout(button_layout)

        # Status information
        self.status_label = QLabel("✓ 準備完了")
        self.status_label.setFont(self.status_font)
        buttons_layout.addWidget(self.status_label)

        layout.addWidget(buttons_frame)

        # Connect scene ID input event
        self.scene_id_entry.textChanged.connect(self.update_scenes_isolation_visibility)

        # Initially update isolation option visibility
        self.update_scenes_isolation_visibility()

    def setup_right_panel(self, splitter):
        # Create right parsing text panel
        right_panel = QWidget()
        splitter.addWidget(right_panel)

        analysis_layout = QVBoxLayout(right_panel)

        analysis_label = QLabel("📊 結果")
        analysis_label.setFont(self.title_font)
        analysis_layout.addWidget(analysis_label)

        self.structure_text = QTextEdit()
        self.structure_text.setFont(self.textbox_font)
        analysis_layout.addWidget(self.structure_text)

        # Add a validate button to ensure proper display
        validate_button = QPushButton("🔬 確認")
        validate_button.clicked.connect(self.validate_parsing)
        validate_button.setFont(self.default_font_bold)
        analysis_layout.addWidget(validate_button)

        # Set initial text
        initial_content = """💡 解析結果

AUP2 ファイルを選択後に解析ボタンをクリックしてください。

解析の内容:
📁 プロジェクトの情報
🎭 シーンのパラメータ
🎯 オブジェクトの情報

💡 ヒント:
- レイヤーの値を確認
- データから抽出

💡 隔離の処理:
フレームの有効時に個別シーンを配置
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
        """パーサーが正しく動作しているかどうかを検証し、詳細なデバッグ情報を表示します"""
        input_path = self.input_entry.text().strip()
        if not input_path:
            QMessageBox.warning(self, "エラー", "入力するファイルを選択してください")
            return

        try:
            # Parse file structure
            parser = AUP2Parser.from_file(input_path)
            data = parser.parse()

            # Generate validation report
            validation_lines = []
            validation_lines.append("=== 解析の検証レポート ===\n")
            validation_lines.append(f"📁 入力: {input_path}\n")

            # Check layer distribution
            layer_distribution = {}
            object_keys = [k for k in data if k.startswith('object.')]

            validation_lines.append("🎯 オブジェクトレイヤーを確認:\n")
            for obj_key in sorted(object_keys, key=lambda x: int(x.split('.')[1])):
                obj_data = data[obj_key]
                obj_id = obj_key.split('.')[1]
                layer = obj_data.get('layer', 'MISSING')
                frame = obj_data.get('frame', [0, 0])
                scene = obj_data.get('scene', 0)

                # Update statistics
                if isinstance(layer, int):
                    layer_distribution[layer] = layer_distribution.get(layer, 0) + 1

                validation_lines.append(f"   🔵 オブジェクト {obj_id}: l={layer}, s={scene}, f={frame}")

            validation_lines.append("\n📊 レイヤーの統計:")
            for layer, count in sorted(layer_distribution.items()):
                validation_lines.append(f"   レイヤー {layer}: {count} 個のオブジェクト")

            # Check if there are layers other than 0
            non_zero_layers = [l for l in layer_distribution.keys() if l != 0]
            if non_zero_layers:
                validation_lines.append(f"\n✅ ノンゼロ: {sorted(non_zero_layers)}")
            else:
                validation_lines.append("\n⚠️ すべてのレイヤー=0")

            # Display results
            result_text = '\n'.join(validation_lines)
            self.structure_text.setPlainText(result_text)

            self.status_label.setText("検証が完了しました")
            self.status_label.setStyleSheet("color: green;")

        except Exception as e:
            error_text = f"検証エラー:\n{str(e)}\n\n正しい形式、ファイルが存在するかを確認してください。"
            self.structure_text.setPlainText(error_text)
            self.status_label.setText("検証に失敗しました")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "検証エラー", f"解析の検証エラー:\n{str(e)}")

    @Slot()
    def update_scenes_isolation_visibility(self):
        scene_id_str = self.scene_id_entry.text().strip()
        adjust_frames = self.adjust_frames_checkbox.isChecked()

        # Show isolation option condition: Scene ID empty and frame adjustment enabled
        should_show = (scene_id_str == "" and adjust_frames)
        self.scenes_isolation_checkbox.setVisible(should_show)

    @Slot()
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "入力の AUP2 ファイルを選択",
            "",
            "AUP2 ファイル (*.aup2);;すべてのファイル (*.*)"
        )
        if file_path:
            self.input_entry.setText(file_path)

    @Slot()
    def select_output_file(self):
        operation = "extract" if self.extract_radio.isChecked() else "transform"
        if operation == "extract":
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "テキストファイルを保存",
                "",
                "テキストファイル (*.txt);;すべてのファイル (*.*)"
            )
            if file_path and not file_path.lower().endswith('.txt'):
                file_path += '.txt'
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "出力の AUP2 ファイルを保存",
                "",
                "AUP2 ファイル (*.aup2);;すべてのファイル (*.*)"
            )
        if file_path:
            self.output_entry.setText(file_path)

    @Slot()
    def parse_file_structure(self):
        input_path = self.input_entry.text().strip()
        if not input_path:
            QMessageBox.warning(self, "エラー", "最初に入力するファイルを選択してください")
            return

        try:
            # Parse file structure
            parser = AUP2Parser.from_file(input_path)
            data = parser.parse()

            # Generate structure information
            structure_lines = []
            structure_lines.append("=== AUP2 ファイルの解析 ===\n")

            # Project information
            if 'project' in data:
                structure_lines.append("📁 プロジェクト:")
                for key, value in data['project'].items():
                    structure_lines.append(f"   {key}: {value}")

            # Scene information
            scene_keys = [k for k in data if k.startswith('scene.')]
            if scene_keys:
                structure_lines.append(f"\n🎭 シーン ({len(scene_keys)} 個のシーン):")
                for scene_key in sorted(scene_keys):
                    scene_id = scene_key.split('.')[1]
                    structure_lines.append(f"   📺 シーン {scene_id}:")
                    if scene_key in data:
                        for key, value in data[scene_key].items():
                            if key in ['scene', 'name', 'video.width', 'video.height', 'cursor.frame']:
                                structure_lines.append(f"      {key}: {value}")

            # Object information
            object_keys = [k for k in data if k.startswith('object.')]
            if object_keys:
                objects_by_scene = {}
                for obj_key in object_keys:
                    obj_data = data[obj_key]
                    scene_id = obj_data.get('scene', 0)
                    if scene_id not in objects_by_scene:
                        objects_by_scene[scene_id] = []
                    objects_by_scene[scene_id].append(obj_key)

                structure_lines.append(f"\n🎯 オブジェクト ({len(object_keys)} 個のオブジェクト):")
                for scene_id in sorted(objects_by_scene.keys()):
                    scene_objects = objects_by_scene[scene_id]
                    structure_lines.append(f"   📋 シーン {scene_id}: {len(scene_objects)} 個のオブジェクト")

                    # Display object details sorted by ID
                    sorted_objects = sorted(scene_objects, key=lambda x: int(x.split('.')[1]))
                    for obj_key in sorted_objects:
                        obj_id = obj_key.split('.')[1]
                        obj_data = data[obj_key]
                        frame = obj_data.get('frame', [0, 0])
                        layer = obj_data.get('layer', 0)  # Default to 0
                        structure_lines.append(f"      🔵 オブジェクト {obj_id}: l={layer}, f={frame}")

                        # Add debug information to GUI display
                        if 'effects' in obj_data:
                            effects_count = len(obj_data['effects'])
                            structure_lines.append(f"         └─ Efx: {effects_count}")

            # Display results
            result_text = '\n'.join(structure_lines)
            self.structure_text.setPlainText(result_text)

            self.status_label.setText("解析が完了しました")
            self.status_label.setStyleSheet("color: green;")

        except Exception as e:
            self.structure_text.setPlainText(f"解析エラー:\n{str(e)}")
            self.status_label.setText("解析に失敗しました")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "解析エラー", f"解析エラー:\n{str(e)}")

    @Slot()
    def execute_operation(self):
        input_path = self.input_entry.text().strip()
        output_path = self.output_entry.text().strip()

        if not input_path:
            QMessageBox.warning(self, "エラー", "入力するファイルを選択してください")
            return
        if not output_path:
            QMessageBox.warning(self, "エラー", "出力するファイルを選択してください")
            return

        is_extract = self.extract_radio.isChecked()

        # Debug information
        print("=== GUI 入力情報 ===")
        print(f"入力: {input_path}")
        print(f"出力: {output_path}")
        print(f"操作: {'extract' if is_extract else 'convert'}")

        try:
            if is_extract:
                extract_text_to_txt(input_path, output_path)
                self.status_label.setText(f"保存済み: {os.path.basename(output_path)}")
                self.status_label.setStyleSheet("color: green;")
                QMessageBox.information(self, "成功", f"テキストファイルを保存しました: {output_path}")
            else:
                # Parse parameters
                scene_id_str = self.scene_id_entry.text().strip()
                scene_id = None if scene_id_str == "" else int(scene_id_str)

                target_layer_str = self.target_layer_entry.text().strip()
                target_layer = int(target_layer_str)

                adjust_frames = self.adjust_frames_checkbox.isChecked()

                # Debug information print transformation parameters
                print(f"シーン: {scene_id}")
                print(f"ターゲット: {target_layer}")
                print(f"調整: {adjust_frames}")
                print(f"隔離: {self.scenes_isolation_checkbox.isChecked() if adjust_frames and scene_id is None else 'N/A'}")
                print("===============")

                # Call transform function
                transform_layer_in_scene(
                    input_path,
                    output_path,
                    scene_id=scene_id,
                    target_layer=target_layer,
                    adjust_frames=adjust_frames
                )

                self.status_label.setText(f"成功: {os.path.basename(output_path)}")
                self.status_label.setStyleSheet("color: green;")
                QMessageBox.information(self, "成功", f"変換に成功しました！ファイルを保存しました: {output_path}")

        except FileNotFoundError as e:
            self.status_label.setText(f"ファイルエラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "ファイルエラー", str(e))
        except ValueError as e:
            self.status_label.setText(f"パラメータエラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "パラメータエラー", str(e))
        except Exception as e:
            self.status_label.setText(f"実行エラー: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "実行エラー", f"Execution error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = LayerChangeGUIPySide6()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
