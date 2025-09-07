"""
AviUtl 图层转换工具 GUI版本 - PySide6 实现

此GUI提供了AUP2文件图层处理的图形界面，包括：
- 指定场景对象的图层修改
- 帧范围调整
- 文件提取和转换

作者: gasdyueer
Version: 1.0 (PySide6 版本)
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

# 添加当前目录和上级目录到路径，以便导入模块
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

try:
    from .layerchange import transform_layer_in_scene, extract_text_to_txt, validate_file_paths, validate_scene_and_layer_ids
    from .aup2_parser import AUP2Parser
except ImportError:
    # 如果相对导入失败，使用绝对导入
    import layerchange
    transform_layer_in_scene = layerchange.transform_layer_in_scene
    extract_text_to_txt = layerchange.extract_text_to_txt
    validate_file_paths = layerchange.validate_file_paths
    validate_scene_and_layer_ids = layerchange.validate_scene_and_layer_ids

    # 导入 aup2_parser
    import aup2_parser
    AUP2Parser = aup2_parser.AUP2Parser


transform_layer_in_scene = layerchange.transform_layer_in_scene
extract_text_to_txt = layerchange.extract_text_to_txt
validate_file_paths = layerchange.validate_file_paths
validate_scene_and_layer_ids = layerchange.validate_scene_and_layer_ids

class LayerChangeGUIPySide6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AviUtl 图层转换 v1.0")
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(700, 400)

        # 定义字体常量，便于维护和修改，提高可读性
        self.default_font = QFont("微软雅黑", 9)
        self.default_font_bold = QFont("微软雅黑", 9, QFont.Weight.Bold)
        self.title_font = QFont("微软雅黑", 10, QFont.Weight.Bold)
        self.title_font_large = QFont("微软雅黑", 10, QFont.Weight.Bold)
        self.status_font = QFont("微软雅黑", 9)
        self.textbox_font = QFont("微软雅黑", 9)

        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主水平布局
        main_layout = QHBoxLayout(central_widget)

        # 创建QSplitter用于分割左右面板
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建左侧操作面板
        self.setup_left_panel(splitter)

        # 创建右侧解析文本面板
        self.setup_right_panel(splitter)

        # 添加分割器到主布局
        main_layout.addWidget(splitter)

        # 设置初始比例 (左侧:右侧 = 5:3)
        splitter.setSizes([480, 320])

    def setup_left_panel(self, splitter):
        # 创建左侧操作面板
        left_panel = QWidget()
        splitter.addWidget(left_panel)

        # 创建主布局
        main_layout = QVBoxLayout(left_panel)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)

        # 文件选择区域
        self.setup_file_section(scroll_layout)

        # 参数配置区域
        self.setup_params_section(scroll_layout)

        # 操作选项区域
        self.setup_operations_section(scroll_layout)

        # 操作按钮区域
        self.setup_buttons_section(scroll_layout)

    def setup_file_section(self, layout):
        file_frame = QGroupBox("📁 文件")
        file_frame.setFont(self.title_font)
        file_layout = QVBoxLayout(file_frame)

        # 输入文件
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入:"))
        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText("选择...")
        input_layout.addWidget(self.input_entry)
        self.input_button = QPushButton("📂 选择")
        input_layout.addWidget(self.input_button)
        file_layout.addLayout(input_layout)

        # 输出文件
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出:"))
        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("保存...")
        output_layout.addWidget(self.output_entry)
        self.output_button = QPushButton("💾 保存")
        output_layout.addWidget(self.output_button)
        file_layout.addLayout(output_layout)

        layout.addWidget(file_frame)

    def setup_params_section(self, layout):
        params_frame = QGroupBox("⚙️ 参数")
        params_frame.setFont(self.title_font)
        params_layout = QVBoxLayout(params_frame)

        # 场景ID
        scene_layout = QHBoxLayout()
        scene_layout.addWidget(QLabel("场景:"))
        self.scene_id_entry = QLineEdit()
        self.scene_id_entry.setPlaceholderText("全场景")
        scene_layout.addWidget(self.scene_id_entry)
        params_layout.addLayout(scene_layout)

        # 目标图层
        layer_layout = QHBoxLayout()
        layer_layout.addWidget(QLabel("图层:"))
        self.target_layer_entry = QLineEdit("0")
        layer_layout.addWidget(self.target_layer_entry)
        params_layout.addLayout(layer_layout)

        layout.addWidget(params_frame)

    def setup_operations_section(self, layout):
        operations_frame = QGroupBox("🔧 选项")
        operations_frame.setFont(self.title_font)
        operations_layout = QVBoxLayout(operations_frame)

        # 帧调整复选框
        self.adjust_frames_checkbox = QCheckBox("🎬 连续帧")
        self.adjust_frames_checkbox.setChecked(True)
        operations_layout.addWidget(self.adjust_frames_checkbox)

        # 多场景隔离处理复选框
        self.scenes_isolation_checkbox = QCheckBox("🚩 隔离场景")
        self.scenes_isolation_checkbox.setChecked(True)
        operations_layout.addWidget(self.scenes_isolation_checkbox)

        # 操作类型单选按钮
        operation_group = QGroupBox()
        operation_layout = QHBoxLayout(operation_group)

        self.operation_group = QButtonGroup(self)
        self.transform_radio = QRadioButton("🔄 转换")
        self.extract_radio = QRadioButton("📄 提取TXT")
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

        # 操作按钮
        button_layout = QHBoxLayout()
        self.parse_button = QPushButton("🔍 解析")
        self.parse_button.setFont(self.default_font_bold)
        button_layout.addWidget(self.parse_button)

        self.execute_button = QPushButton("▶️ 执行")
        self.execute_button.setFont(self.default_font_bold)
        button_layout.addWidget(self.execute_button)
        buttons_layout.addLayout(button_layout)

        # 状态信息
        self.status_label = QLabel("✓ 就绪")
        self.status_label.setFont(self.status_font)
        buttons_layout.addWidget(self.status_label)

        layout.addWidget(buttons_frame)

        # 连接场景ID输入事件
        self.scene_id_entry.textChanged.connect(self.update_scenes_isolation_visibility)

        # 初始时更新隔离选项可见性
        self.update_scenes_isolation_visibility()

    def setup_right_panel(self, splitter):
        # 创建右侧解析文本面板
        right_panel = QWidget()
        splitter.addWidget(right_panel)

        analysis_layout = QVBoxLayout(right_panel)

        analysis_label = QLabel("📊 分析结果")
        analysis_label.setFont(self.title_font)
        analysis_layout.addWidget(analysis_label)

        self.structure_text = QTextEdit()
        self.structure_text.setFont(self.textbox_font)
        analysis_layout.addWidget(self.structure_text)

        # 添加一个验证按钮来确保正确显示
        validate_button = QPushButton("🔬 验证")
        validate_button.clicked.connect(self.validate_parsing)
        validate_button.setFont(self.default_font_bold)
        analysis_layout.addWidget(validate_button)

        # 设置初始文本
        initial_content = """💡 分析结果

先选择AUP2文件，
再点解析按钮分析内容。

分析内容：
📁项目信息
🎭场景参数
🎯对象信息

💡 提示:
- 检查图层信息
- 层值从数据提取

💡 隔离处理:
启用帧调整时，
各场景对象独立排列。
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
        """验证解析器是否正确工作并显示详细的调试信息"""
        input_path = self.input_entry.text().strip()
        if not input_path:
            QMessageBox.warning(self, "错误", "请先选择输入文件")
            return

        try:
            # 解析文件结构
            parser = AUP2Parser.from_file(input_path)
            data = parser.parse()

            # 生成验证报告
            validation_lines = []
            validation_lines.append("=== 解析验证报告 ===\n")
            validation_lines.append(f"📁 输入文件: {input_path}\n")

            # 检查layer分布
            layer_distribution = {}
            object_keys = [k for k in data if k.startswith('object.')]

            validation_lines.append("🎯 对象图层验证:\n")
            for obj_key in sorted(object_keys, key=lambda x: int(x.split('.')[1])):
                obj_data = data[obj_key]
                obj_id = obj_key.split('.')[1]
                layer = obj_data.get('layer', 'MISSING')
                frame = obj_data.get('frame', [0, 0])
                scene = obj_data.get('scene', 0)

                # 更新统计
                if isinstance(layer, int):
                    layer_distribution[layer] = layer_distribution.get(layer, 0) + 1

                validation_lines.append(f"   🔵 对象 {obj_id}: layer={layer}, scene={scene}, frame={frame}")

            validation_lines.append("\n📊 图层分布统计:")
            for layer, count in sorted(layer_distribution.items()):
                validation_lines.append(f"   图层 {layer}: {count} 个对象")

            # 检查是否有layer=0以外的值
            non_zero_layers = [l for l in layer_distribution.keys() if l != 0]
            if non_zero_layers:
                validation_lines.append(f"\n✅ 发现非零图层: {sorted(non_zero_layers)}")
            else:
                validation_lines.append("\n⚠️ 警告: 所有对象的图层都为0")

            # 显示结果
            result_text = '\n'.join(validation_lines)
            self.structure_text.setPlainText(result_text)

            self.status_label.setText("解析验证完成")
            self.status_label.setStyleSheet("color: green;")

        except Exception as e:
            error_text = f"验证解析时出错:\n{str(e)}\n\n请确保文件格式正确且文件存在。"
            self.structure_text.setPlainText(error_text)
            self.status_label.setText("解析验证失败")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "验证错误", f"验证解析时出错:\n{str(e)}")

    @Slot()
    def update_scenes_isolation_visibility(self):
        scene_id_str = self.scene_id_entry.text().strip()
        adjust_frames = self.adjust_frames_checkbox.isChecked()

        # 显示隔离选项的条件：场景ID为空且帧调整启用
        should_show = (scene_id_str == "" and adjust_frames)
        self.scenes_isolation_checkbox.setVisible(should_show)

    @Slot()
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择输入AUP2文件",
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
                "保存TXT文件",
                "",
                "Text files (*.txt);;All files (*.*)"
            )
            if file_path and not file_path.lower().endswith('.txt'):
                file_path += '.txt'
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存输出AUP2文件",
                "",
                "AUP2 files (*.aup2);;All files (*.*)"
            )
        if file_path:
            self.output_entry.setText(file_path)

    @Slot()
    def parse_file_structure(self):
        input_path = self.input_entry.text().strip()
        if not input_path:
            QMessageBox.warning(self, "错误", "请先选择输入文件")
            return

        try:
            # 解析文件结构
            parser = AUP2Parser.from_file(input_path)
            data = parser.parse()

            # 生成结构信息
            structure_lines = []
            structure_lines.append("=== AUP2 文件结构分析 ===\n")

            # 项目信息
            if 'project' in data:
                structure_lines.append("📁 PROJECT:")
                for key, value in data['project'].items():
                    structure_lines.append(f"   {key}: {value}")

            # 场景信息
            scene_keys = [k for k in data if k.startswith('scene.')]
            if scene_keys:
                structure_lines.append(f"\n🎭 SCENES ({len(scene_keys)} 个场景):")
                for scene_key in sorted(scene_keys):
                    scene_id = scene_key.split('.')[1]
                    structure_lines.append(f"   📺 场景 {scene_id}:")
                    if scene_key in data:
                        for key, value in data[scene_key].items():
                            if key in ['scene', 'name', 'video.width', 'video.height', 'cursor.frame']:
                                structure_lines.append(f"      {key}: {value}")

            # 对象信息
            object_keys = [k for k in data if k.startswith('object.')]
            if object_keys:
                objects_by_scene = {}
                for obj_key in object_keys:
                    obj_data = data[obj_key]
                    scene_id = obj_data.get('scene', 0)
                    if scene_id not in objects_by_scene:
                        objects_by_scene[scene_id] = []
                    objects_by_scene[scene_id].append(obj_key)

                structure_lines.append(f"\n🎯 OBJECTS ({len(object_keys)} 个对象):")
                for scene_id in sorted(objects_by_scene.keys()):
                    scene_objects = objects_by_scene[scene_id]
                    structure_lines.append(f"   📋 场景 {scene_id}: {len(scene_objects)} 个对象")

                    # 按ID排序显示对象的详细信息
                    sorted_objects = sorted(scene_objects, key=lambda x: int(x.split('.')[1]))
                    for obj_key in sorted_objects:
                        obj_id = obj_key.split('.')[1]
                        obj_data = data[obj_key]
                        frame = obj_data.get('frame', [0, 0])
                        layer = obj_data.get('layer', 0)  # 默认值为0
                        structure_lines.append(f"      🔵 对象 {obj_id}: layer={layer}, frame={frame}")

                        # 添加调试信息到GUI显示
                        if 'effects' in obj_data:
                            effects_count = len(obj_data['effects'])
                            structure_lines.append(f"         └─ 效果数量: {effects_count}")

            # 显示结果
            result_text = '\n'.join(structure_lines)
            self.structure_text.setPlainText(result_text)

            self.status_label.setText("文件结构解析完成")
            self.status_label.setStyleSheet("color: green;")

        except Exception as e:
            self.structure_text.setPlainText(f"解析文件结构时出错:\n{str(e)}")
            self.status_label.setText("文件结构解析失败")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "解析错误", f"解析文件结构时出错:\n{str(e)}")

    @Slot()
    def execute_operation(self):
        input_path = self.input_entry.text().strip()
        output_path = self.output_entry.text().strip()

        if not input_path:
            QMessageBox.warning(self, "错误", "请选择输入文件")
            return
        if not output_path:
            QMessageBox.warning(self, "错误", "请选择输出文件")
            return

        is_extract = self.extract_radio.isChecked()

        # 调试信息
        print("=== GUI 用户输入信息 ===")
        print(f"输入文件: {input_path}")
        print(f"输出文件: {output_path}")
        print(f"操作类型: {'extract' if is_extract else 'transform'}")

        try:
            if is_extract:
                extract_text_to_txt(input_path, output_path)
                self.status_label.setText(f"TXT文件已保存: {os.path.basename(output_path)}")
                self.status_label.setStyleSheet("color: green;")
                QMessageBox.information(self, "成功", f"TXT文件已保存至: {output_path}")
            else:
                # 解析参数
                scene_id_str = self.scene_id_entry.text().strip()
                scene_id = None if scene_id_str == "" else int(scene_id_str)

                target_layer_str = self.target_layer_entry.text().strip()
                target_layer = int(target_layer_str)

                adjust_frames = self.adjust_frames_checkbox.isChecked()

                # 调试信息打印转换参数
                print(f"场景ID: {scene_id}")
                print(f"目标图层: {target_layer}")
                print(f"调整帧范围: {adjust_frames}")
                print(f"多场景隔离: {self.scenes_isolation_checkbox.isChecked() if adjust_frames and scene_id is None else 'N/A'}")
                print("=========================")

                # 调用转换函数
                transform_layer_in_scene(
                    input_path,
                    output_path,
                    scene_id=scene_id,
                    target_layer=target_layer,
                    adjust_frames=adjust_frames
                )

                self.status_label.setText(f"转换成功: {os.path.basename(output_path)}")
                self.status_label.setStyleSheet("color: green;")
                QMessageBox.information(self, "成功", f"转换成功！新文件已保存至: {output_path}")

        except FileNotFoundError as e:
            self.status_label.setText(f"文件错误: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "文件错误", str(e))
        except ValueError as e:
            self.status_label.setText(f"参数错误: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "参数错误", str(e))
        except Exception as e:
            self.status_label.setText(f"执行错误: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "执行错误", f"执行错误: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = LayerChangeGUIPySide6()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()