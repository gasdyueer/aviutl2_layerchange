"""
AviUtl AUP2 图层转换工具

此模块提供了AUP2文件图层处理的各种功能，包括：
- 指定场景对象的图层修改
- 多场景到单场景的转换
- 帧范围调整
- 文件提取和转换

作者: Roo
版本: 2.0
"""

import os
import re
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
import sys

# 添加一级的父目录到路径，以便导入aup2_parser
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from aup2_parser import AUP2Parser
except ImportError:
    # 如果失败，尝试绝对导入
    import aup2_parser
    AUP2Parser = aup2_parser.AUP2Parser

# 常量定义
DEFAULT_ENCODING = 'utf-8'
OBJECT_PREFIX = 'object.'
SCENE_PREFIX = 'scene.'

# 错误信息常量
ERROR_FILE_NOT_FOUND = "错误: 文件 '{filepath}' 未找到。"
ERROR_INVALID_SCENE_ID = "错误: 无效的场景ID '{scene_id}'，必须是非负整数。"
ERROR_INVALID_LAYER_ID = "错误: 无效的图层ID '{layer_id}'，必须是非负整数。"
ERROR_NO_OBJECTS_FOUND = "警告: 未找到场景 {scene_id} 中的对象，或者文件不包含对象。"
SUCCESS_TRANSFORMATION = "转换成功！新文件已保存至: {output_filepath}"

def validate_file_paths(input_path: Union[str, Path], output_path: Union[str, Path]) -> Tuple[Path, Path]:
    """
    验证和标准化文件路径。

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径

    Returns:
        Tuple[Path, Path]: 标准化的输入和输出路径

    Raises:
        FileNotFoundError: 如果输入文件不存在
        ValueError: 如果路径无效
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(ERROR_FILE_NOT_FOUND.format(filepath=input_path))

    if not input_path.suffix.lower() == '.aup2':
        raise ValueError("输入文件必须是.aup2格式")

    return input_path, output_path

def validate_scene_and_layer_ids(scene_id: Optional[int], layer_id: int) -> None:
    """
    验证场景ID和图层ID。

    Args:
        scene_id: 场景ID（可选）
        layer_id: 图层ID

    Raises:
        ValueError: 如果ID无效
    """
    if scene_id is not None and scene_id < 0:
        raise ValueError(ERROR_INVALID_SCENE_ID.format(scene_id=scene_id))

    if layer_id < 0:
        raise ValueError(ERROR_INVALID_LAYER_ID.format(layer_id=layer_id))

def extract_text_to_txt(input_filepath: Union[str, Path], output_txt_filepath: Union[str, Path]) -> None:
    """
    将AviUtl工程文件的文本内容提取并输出为TXT文件。

    Args:
        input_filepath: 输入AviUtl工程文件的路径。
        output_txt_filepath: 输出TXT文件的路径。

    Raises:
        FileNotFoundError: 如果输入文件不存在
        IOError: 如果读取或写入失败
    """
    input_path, output_path = validate_file_paths(input_filepath, output_txt_filepath)

    try:
        with open(input_path, 'r', encoding=DEFAULT_ENCODING) as f:
            content = f.read()

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入TXT文件
        with open(output_path, 'w', encoding=DEFAULT_ENCODING) as f:
            f.write(content)

        print(f"TXT文件已保存至: {output_path}")

    except FileNotFoundError:
        print(ERROR_FILE_NOT_FOUND.format(filepath=input_path))
        raise
    except IOError as e:
        print(f"文件操作错误: {e}")
        raise
    except Exception as e:
        print(f"提取文本时发生错误: {e}")
        raise

def transform_layer_in_scene(input_filepath: Union[str, Path],
                           output_filepath: Union[str, Path],
                           scene_id: Optional[int] = None,
                           target_layer: int = 0,
                           adjust_frames: bool = False) -> None:
    """
    修改指定场景中所有对象的图层到目标图层（增强版）。

    支持根据解析后的结构层次进行准确的对象处理：
    - 精确场景-对象关联
    - 保持原始对象ID顺序
    - 智能帧范围调整，使对象连续排列而无重叠
    - 自动插入1帧间隔以保持对象连续性

    Args:
        input_filepath: 输入AUP2文件的路径。
        output_filepath: 输出AUP2文件的路径。
        scene_id: 指定场景ID，None表示处理所有场景，0表示默认场景。
        target_layer: 目标图层编号，默认为0。
        adjust_frames: 是否调整帧范围使对象连续排列，默认为False。

    Raises:
        FileNotFoundError: 如果输入文件不存在
        ValueError: 如果参数无效
        Exception: 其他处理过程中的错误

    处理流程:
    1. 验证参数和文件路径
    2. 解析AUP2文件获取结构化数据
    3. 使用get_objects_by_scene获取指定场景的对象列表
    4. 确保对象具有正确的scene属性
    5. 根据adjust_frames参数处理图层和帧范围
    6. 重建AUP2内容并保存
    """
    # 验证输入参数
    validate_scene_and_layer_ids(scene_id, target_layer)
    input_path, output_path = validate_file_paths(input_filepath, output_filepath)

    try:
        # 使用AUP2Parser解析文件
        parser = AUP2Parser.from_file(input_path)
        data = parser.parse()

        # 移除元数据，专注于对象数据
        if '_metadata' in data:
            del data['_metadata']

        # 获取指定场景的对象，使用解析器的辅助方法
        scene_objects = parser.get_objects_by_scene(scene_id)

        if not scene_objects:
            message = ERROR_NO_OBJECTS_FOUND.format(scene_id=scene_id if scene_id is not None else "all")
            print(message)
            return

        # 提取对象键列表
        target_scene_objects = [obj['id'] for obj in scene_objects]

        print(f"在场景 {scene_id if scene_id is not None else '全部'} 中发现 {len(target_scene_objects)} 个对象需要处理")
        layer_str = '、'.join(str(obj['layer']) for obj in scene_objects[:5])
        extra = " 等..." if len(scene_objects) > 5 else ""
        print(f"处理的图层组合: {layer_str}{extra}")

        # 确保对象具有正确的scene属性（针对重建时的场景关联）
        for obj in scene_objects:
            obj_key = obj['id']
            if scene_id is not None and data[obj_key].get('scene') is None:
                # 为特定场景的对象添加scene属性
                data[obj_key]['scene'] = scene_id

        if adjust_frames:
            print("开始帧范围调整，使对象连续排列...")
            if scene_id is None:
                # 多场景隔离处理：分别调整每个场景的对象连续性，保持场景间隔离
                print("执行多场景隔离处理：每个场景独立连续排列对象")
                all_objects_with_data = []

                # 获取所有场景ID，按排序处理
                all_scenes = sorted(set(obj['scene'] for obj in scene_objects if obj.get('scene') is not None))
                if any(obj.get('scene') is None for obj in scene_objects):
                    all_scenes.append(None)  # 处理默认场景0或无scene的

                for sc_id in all_scenes:
                    scene_list = [obj for obj in scene_objects if obj.get('scene') == sc_id]
                    if scene_list:
                        # 为当前场景的objects设置连续帧
                        scene_objects_temp = []
                        for obj in scene_list:
                            obj_key = obj['id']
                            obj_data = data[obj_key].copy()

                            # 设置目标图层
                            obj_data['layer'] = target_layer

                            # 移除focus（场景内最后一个对象将获得）
                            if 'focus' in obj_data:
                                del obj_data['focus']

                            obj_data['_original_id'] = int(obj_key.split('.')[1])
                            scene_objects_temp.append(obj_data)

                        # 按ID排序
                        scene_objects_temp.sort(key=lambda x: x.get('_original_id', 0))

                        # 当前场景内部帧调整（隔离）
                        previous_frame_end = -1
                        for idx, obj_data in enumerate(scene_objects_temp):
                            original_frame = obj_data.get('frame', [0, 0])
                            duration = original_frame[1] - original_frame[0] + 1

                            if idx == 0:
                                # 场景内第一个对象保持其原始起始位置
                                obj_data['frame'] = original_frame
                                previous_frame_end = original_frame[1]
                            else:
                                # 后续对象连续排列，保持场景内部连续性
                                frame_start = previous_frame_end + 1
                                obj_data['frame'] = [frame_start, frame_start + duration - 1]
                                previous_frame_end = frame_start + duration - 1

                        # 将当前场景调整后的对象添加全局列表
                        all_objects_with_data.extend(scene_objects_temp)

                # 删除所有原对象
                for obj_key in target_scene_objects:
                    del data[obj_key]

                # 重新分配所有对象ID，从0开始，但保持调整后的帧和图层
                for idx, obj_data in enumerate(all_objects_with_data):
                    new_obj_key = f"{OBJECT_PREFIX}{idx}"
                    data[new_obj_key] = obj_data

            else:
                # 单场景处理：简单连续排列
                # 准备对象数据，按原始ID排序保持创建顺序
                objects_with_data = []
                for obj in scene_objects:
                    obj_key = obj['id']
                    obj_data = data[obj_key].copy()

                    # 设置目标图层
                    obj_data['layer'] = target_layer

                    # 移除focus（将由最后一个对象获得）
                    if 'focus' in obj_data:
                        del obj_data['focus']

                    # 保存原始ID用于精确排序
                    obj_data['_original_id'] = int(obj_key.split('.')[1])
                    objects_with_data.append(obj_data)

                # 按原始对象ID排序，保持原始顺序
                objects_with_data.sort(key=lambda x: x.get('_original_id', 0))

                # 删除原有对象键
                for obj_key in target_scene_objects:
                    del data[obj_key]

                # 重新分配对象，从第一个位置开始连续排列
                previous_frame_end = -1  # 初始化帧结束位置

                for idx, obj_data in enumerate(objects_with_data):
                    original_frame = obj_data.get('frame', [0, 0])
                    duration = original_frame[1] - original_frame[0] + 1

                    if idx == 0:
                        # 第一个对象保持原帧位置
                        obj_data['frame'] = original_frame
                        previous_frame_end = original_frame[1]
                    else:
                        # 后续对象在前一个对象结束后连续排列
                        # 插入1帧间隔以保持连续性
                        frame_start = previous_frame_end + 1
                        obj_data['frame'] = [frame_start, frame_start + duration - 1]
                        previous_frame_end = frame_start + duration - 1

                    # 重新写入对象（编号从0开始）
                    new_obj_key = f"{OBJECT_PREFIX}{idx}"
                    data[new_obj_key] = obj_data

                # 为最后一个对象设置focus
                if objects_with_data:
                    last_obj_key = f"{OBJECT_PREFIX}{len(objects_with_data) - 1}"
                    if last_obj_key in data:
                        data[last_obj_key]['focus'] = 1

                print(f"单场景帧范围调整完成：已连续排列 {len(objects_with_data)} 个对象")

            # 为所有调整后的对象设置最后一个focus（对于多场景，取最后一个场景的最后一个对象）
            all_adjusted_objects = [k for k in data if k.startswith(OBJECT_PREFIX)]
            if all_adjusted_objects:
                last_key = max(all_adjusted_objects, key=lambda x: int(x.split('.')[1]))
                if last_key in data and 'focus' not in data[last_key]:
                    data[last_key]['focus'] = 1

            print(f"帧范围调整完成：处理了 {len(target_scene_objects)} 个对象，按场景隔离连续排列") if scene_id is None else ""

        else:
            # 无帧调整，只是修改图层
            print(f"开始图层修改：将场景 {scene_id if scene_id is not None else '全部'} 的对象图层设为 {target_layer}")
            for obj_key in target_scene_objects:
                data[obj_key]['layer'] = target_layer
            print(f"图层修改完成：已处理 {len(target_scene_objects)} 个对象")

        # 使用解析器重建AUP2内容，确保输出格式正确
        reconstructed_content = AUP2Parser.reconstruct_from_dict(data)

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存转换后的文件
        with open(output_path, 'w', encoding=DEFAULT_ENCODING) as f:
            f.write(reconstructed_content)

        print(SUCCESS_TRANSFORMATION.format(output_filepath=output_path))

        # 显示最终统计
        final_summary = parser.get_summary()
        print("转换后的统计信息:")
        print(f"  - 总对象数: {final_summary['objects']}")
        print(f"  - 图层分布: {final_summary['layer_distribution']}")

    except FileNotFoundError:
        print(ERROR_FILE_NOT_FOUND.format(filepath=input_path))
        raise
    except ValueError as e:
        print(f"参数验证错误: {e}")
        raise
    except Exception as e:
        print(f"图层转换过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        raise

def transform_multilayer_to_singlelayer(input_filepath: Union[str, Path],
                                      output_filepath: Union[str, Path]) -> None:
    """
    向后兼容：将多层转换为单层的等效函数。

    这等效于调用 transform_layer_in_scene(scene_id=None, target_layer=0, adjust_frames=True)。

    Args:
        input_filepath: 输入文件路径
        output_filepath: 输出文件路径
    """
    transform_layer_in_scene(input_filepath, output_filepath, scene_id=None, target_layer=0, adjust_frames=True)

def transform_aviutl_project_to_serial_single_layer(input_filepath: Union[str, Path],
                                                 output_filepath: Union[str, Path]) -> None:
    """
    兼容性函数：保持与旧版本的接口兼容。
    """
    transform_multilayer_to_singlelayer(input_filepath, output_filepath)

if __name__ == "__main__":
    """
    主程序入口，可用于命令行调用

    用法示例:
    python layerchange.py

    这将运行两个预定义的转换示例：
    1. 单场景处理示例
    2. 多场景隔离处理示例（帧调整）
    """
    # 请根据你的实际文件路径修改这里
    input_file = "test_multiscene_multilayer.aup2"
    output_file1 = "test_scene_processed.aup2"
    output_file2 = "test_multiscene_consecutive.aup2"

    try:
        print("=== 示例1: 单场景处理 ===")
        # 示例：修改场景0中的所有对象到图层2
        transform_layer_in_scene(input_file, output_file1, scene_id=0, target_layer=2, adjust_frames=False)
        print(f"完成！请查看输出文件: {output_file1}")
    except Exception as e:
        print(f"示例1失败: {e}")

    try:
        print("\n=== 示例2: 多场景隔离处理（连续排列）===")
        # 示例：处理所有场景对象到图层0，并调整帧范围，使每个场景内对象连续排列
        transform_layer_in_scene(input_file, output_file2, scene_id=None, target_layer=0, adjust_frames=True)
        print(f"完成！请查看输出文件: {output_file2}")
        print("此示例演示了不同场景对象之间的隔离处理逻辑")
    except Exception as e:
        print(f"示例2失败: {e}")
        exit(1)