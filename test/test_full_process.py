#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整处理流程
验证整季模式下每个文件都会生成独立的输出文件
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.naming import generate_output_name
from function.volumes import smart_group_files


def test_full_process():
    """测试完整处理流程：分组 + 生成输出文件名"""
    test_files = [
        "중국 '실전 봉쇄' 훈련 중인데... 도로 위에서 불타버린 대만군 '용호' 전차.whisper.[kor].srt",
        "중국 제3 항모 첫 실전 훈련...미국 _6척 더 만든다_ 견제 _ YTN.whisper.[kor].srt",
    ]
    
    # 转换为完整路径
    test_file_paths = [os.path.join("test", f) for f in test_files]
    
    print("=== 测试完整处理流程（整季模式） ===")
    
    # 1. 智能分组（整季模式）
    print("1. 智能分组...")
    groups = smart_group_files(test_file_paths, 0)  # 0表示整季模式
    
    # 2. 为每个组生成输出文件名
    print("\n2. 生成输出文件名...")
    output_files = []
    
    for i, group in enumerate(groups):
        # 提取文件名
        filenames = [os.path.basename(f) for f in group]
        
        # 生成输出文件名
        output_name = generate_output_name(filenames, ".pdf", "整季")
        output_files.append(output_name)
        
        print(f"组 {i+1}:")
        for f in filenames:
            print(f"  - {f}")
        print(f"  → 输出文件名: {output_name}")
    
    print(f"\n3. 处理结果：")
    print(f"   总文件数: {len(test_files)}")
    print(f"   分组数: {len(groups)}")
    print(f"   生成的输出文件名: {output_files}")
    
    # 验证结果
    if len(groups) == len(test_files):
        print(f"\n✅ 测试通过：每个文件都生成了独立的输出文件！")
        return True
    else:
        print(f"\n❌ 测试失败：文件没有正确分组！")
        return False


if __name__ == "__main__":
    success = test_full_process()
    sys.exit(0 if success else 1)