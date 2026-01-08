#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 UI 图标路径脚本（通用版）
处理同目录下所有 ui_xxxx.py 文件的图标路径更新
"""

import os
import sys
import io
import glob
import re

# 设置标准输出为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（脚本所在目录的父目录）
base_dir = os.path.dirname(script_dir)
resources_dir = os.path.join(base_dir, "resources")

print("=" * 60)
print("UI 图标路径更新脚本（通用版）")
print("=" * 60)
print(f"脚本目录: {script_dir}")
print(f"项目根目录: {base_dir}")
print(f"资源目录: {resources_dir}")
print("=" * 60)

# 查找所有 ui_xxxx.py 文件
ui_pattern = os.path.join(script_dir, "ui_*.py")
ui_files = glob.glob(ui_pattern)

if not ui_files:
    print(f"[警告] 未找到任何 ui_xxxx.py 文件")
    print(f"搜索路径: {ui_pattern}")
    sys.exit(0)

print(f"\n找到 {len(ui_files)} 个 UI 文件:")
for i, ui_file in enumerate(ui_files, 1):
    print(f"  {i}. {os.path.basename(ui_file)}")

print("\n" + "=" * 60)

# 构建正确的路径格式
abs_resources_path = resources_dir.replace('\\', '/')
new_pattern = abs_resources_path + '/'

# 处理每个 UI 文件
success_count = 0
error_count = 0

for ui_file in ui_files:
    ui_filename = os.path.basename(ui_file)
    print(f"\n正在处理: {ui_filename}")
    print("-" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(ui_file):
        print(f"  [错误] 文件不存在: {ui_file}")
        error_count += 1
        continue
    
    # 读取文件内容
    try:
        with open(ui_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [错误] 无法读取文件: {e}")
        error_count += 1
        continue
    
    original_size = len(content)
    
    # 更新图标路径为绝对路径
    old_pattern = 'Icons/'
    count_before = content.count(old_pattern)
    content = content.replace(old_pattern, new_pattern)
    count_after = content.count(old_pattern)
    actual_replaced = count_before - count_after
    
    print(f"  替换: {old_pattern} -> {new_pattern}")
    print(f"  替换前: {count_before} 处")
    print(f"  替换后: {count_after} 处")
    print(f"  实际替换: {actual_replaced} 处")
    
    # 修复进度条初始值：将 setValue(24) 改为 setValue(0)
    progress_before = content.count('ProgressBar.setValue(24)')
    content = content.replace('ProgressBar.setValue(24)', 'ProgressBar.setValue(0)')
    progress_after = content.count('ProgressBar.setValue(24)')
    progress_fixed = progress_before - progress_after
    
    if progress_fixed > 0:
        print(f"  修复: ProgressBar.setValue(24) -> ProgressBar.setValue(0)")
        print(f"  修复前: {progress_before} 处")
        print(f"  修复后: {progress_after} 处")
        print(f"  实际修复: {progress_fixed} 处")
    
    # 如果没有替换，跳过
    if actual_replaced == 0:
        print(f"  [跳过] 没有需要替换的内容")
        continue
    
    # 写回文件
    try:
        with open(ui_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] 已更新文件")
    except Exception as e:
        print(f"  [错误] 无法写入文件: {e}")
        error_count += 1
        continue
    
    # 验证语法
    try:
        with open(ui_file, 'r', encoding='utf-8') as f:
            compile(f.read(), ui_file, 'exec')
        print(f"  [OK] 语法验证通过")
    except SyntaxError as e:
        print(f"  [错误] 语法错误: {e}")
        print(f"    行号: {e.lineno}")
        print(f"    错误: {e.msg}")
        error_count += 1
        continue
    
    success_count += 1

print("\n" + "=" * 60)
print("处理完成！")
print("=" * 60)
print(f"成功: {success_count} 个文件")
print(f"失败: {error_count} 个文件")
print(f"总计: {len(ui_files)} 个文件")
print()