#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试命名处理函数
验证clean_filename_title函数是否能正确移除whisper相关后缀
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.naming import clean_filename_title


def test_clean_filename_title():
    """测试clean_filename_title函数的各种情况"""
    test_cases = [
        # 基本情况：无whisper后缀
        ("test_file.srt", "test_file"),
        # 带whisper后缀的情况
        ("test_file.whisper.[kor].srt", "test_file"),
        ("test_file.whisper.[eng].srt", "test_file"),
        ("test_file.whisper.[jpn].srt", "test_file"),
        # 带集数标识的情况
        ("Series.Name.S01E01.whisper.[kor].srt", "Series Name S01E01"),
        ("Series.Name.E02.whisper.[eng].srt", "Series Name E02"),
        # 带年份标识的情况
        ("Movie.Title.2023.whisper.[kor].srt", "Movie Title 2023"),
        # 复杂情况
        ("Complex.Series.S02E05.1080p.whisper.[kor].srt", "Complex Series S02E05"),
        # 不同大小写
        ("Test.File.WHISPER.[KOR].srt", "Test.File"),
        # 空格分隔
        ("test file.whisper. [kor] .srt", "test file"),
    ]
    
    print("=== 测试 clean_filename_title 函数 ===")
    all_passed = True
    
    for filename, expected in test_cases:
        result = clean_filename_title(filename)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} | {filename:<50} -> {result:<30} (预期: {expected})")
        if result != expected:
            all_passed = False
    
    print("\n=== 测试结果 ===")
    if all_passed:
        print("✅ 所有测试通过！")
        return True
    else:
        print("❌ 部分测试失败！")
        return False


if __name__ == "__main__":
    success = test_clean_filename_title()
    sys.exit(0 if success else 1)