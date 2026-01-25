#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试系列分组功能
验证get_series_name函数和smart_group_files函数的行为
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.naming import get_series_name, generate_output_name
from function.volumes import smart_group_files


def test_get_series_name():
    """测试get_series_name函数"""
    test_cases = [
        # 带集数标识的情况
        ("Series.Name.S01E01.srt", "series name"),
        ("Series.Name.E02.srt", "series name"),
        # 不带集数标识的情况
        ("중국 '실전 봉쇄' 훈련 중인데... 도로 위에서 불타버린 대만군 '용호' 전차.whisper.[kor].srt", "중국"),
        ("중국 제3 항모 첫 실전 훈련...미국 _6척 더 만든다_ 견제 _ YTN.whisper.[kor].srt", "중국"),
    ]
    
    print("=== 测试 get_series_name 函数 ===")
    for filename, expected in test_cases:
        result = get_series_name(filename)
        print(f"{filename:<80} -> {result:<20} (预期: {expected})")


def test_smart_group_files():
    """测试smart_group_files函数"""
    test_files = [
        "중국 '실전 봉쇄' 훈련 중인데... 도로 위에서 불타버린 대만군 '용호' 전차.whisper.[kor].srt",
        "중국 제3 항모 첫 실전 훈련...미국 _6척 더 만든다_ 견제 _ YTN.whisper.[kor].srt",
    ]
    
    # 转换为完整路径
    test_file_paths = [os.path.join("test", f) for f in test_files]
    
    print("\n=== 测试 smart_group_files 函数（整季模式） ===")
    # 整季模式下的分组
    groups = smart_group_files(test_file_paths, 0)  # 0表示整季模式
    
    for i, group in enumerate(groups):
        print(f"组 {i+1}: {[os.path.basename(f) for f in group]}")
    
    print(f"\n总共生成了 {len(groups)} 个组")


def test_generate_output_name():
    """测试generate_output_name函数"""
    test_files = [
        "중국 '실전 봉쇄' 훈련 중인데... 도로 위에서 불타버린 대만군 '용호' 전차.whisper.[kor].srt",
        "중국 제3 항모 첫 실전 훈련...미국 _6척 더 만든다_ 견제 _ YTN.whisper.[kor].srt",
    ]
    
    print("\n=== 测试 generate_output_name 函数 ===")
    # 整季模式下的输出文件名生成
    output_name = generate_output_name(test_files, ".pdf", "整季")
    print(f"输出文件名: {output_name}")


if __name__ == "__main__":
    test_get_series_name()
    test_smart_group_files()
    test_generate_output_name()