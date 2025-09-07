"""
AUP2 Parser Package
用于解析AviUtl AUP2文件的Python库

示例用法:
    from pycode.aviutl2_scripts.aup2_parser import AUP2Parser, parse_aup2_file

    # 使用类
    parser = AUP2Parser(aup2_content)
    data = parser.parse()

    # 使用便利函数
    data = parse_aup2_file('path/to/file.aup2')
"""

from .aup2_parser import (
    AUP2Parser,
    AUP2ParseError,
    AUP2ValidationError,
    AUP2ReconstructionError,
    parse_aviutl_aup2_to_dict,
    parse_aup2_file,
    reconstruct_aup2_dict,
    validate_aup2_file
)

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "A Python parser for AviUtl AUP2 files"

# 简化的导入接口
def parse(content: str) -> dict:
    """简化接口：解析AUP2内容字符串"""
    return parse_aviutl_aup2_to_dict(content)

def parse_file(filepath: str) -> dict:
    """简化接口：解析AUP2文件"""
    return parse_aup2_file(filepath)