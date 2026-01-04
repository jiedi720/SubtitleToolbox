#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命名与文件名处理模块
负责从文件名中提取纯净标题、系列名以及生成合并输出文件名。
"""

import os
import re

__all__ = [
    'clean_filename_title',
    'get_series_name',
    'generate_output_name'
]

def clean_filename_title(filename):
    """从文件名中提取纯净的标题
    
    保留对单集集数的识别，确保 PDF 内部标题含有 S01E01 格式。
    对于电影文件，提取完整标题并移除常见垃圾词。
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 清理后的纯净标题
    """
    name = os.path.splitext(filename)[0]
    
    # 提取 S01E01 或 年份之前的标题部分
    match_se = re.search(r'(.*?(?:S\d{1,2}[\s.]?E\d{1,3}|E\d{1,3}))', name, re.IGNORECASE)
    if match_se: 
        name = match_se.group(1)
    else:
        # 对于电影文件，尝试提取年份之前的部分
        match_year = re.search(r'(.*?)[._\s(\[](19|20)\d{2}', name)
        if match_year: 
            name = match_year.group(1)
    
    # 替换分隔符为空格
    clean_name = name.replace('.', ' ').replace('_', ' ').replace('-', ' ')
    
    # 过滤常见垃圾词
    junk_words = [
        r'\b(19|20)\d{2}\b', r'1080[pi]', r'720[pi]', r'2160[pi]', r'4k', 
        r'WEB.?DL', r'WEB.?Rip', r'BluRay', r'HDTV', r'H\.?264', r'H\.?265', 
        r'x264', r'x265', r'HEVC', r'AAC', r'AC3', r'E\.?AC3', r'DDP', r'5\.1', 
        r'Netflix', r'NF', r'AMZN', r'DSNP', r'Subs', r'Repack', r'Proper', 
        r'TC', r'CMCTV', r'text', r'track\d+', r'FRDS', r'\[kor\]', r'\[chi\]', r'\[cht\]'
    ]
    for junk in junk_words: 
        clean_name = re.sub(junk, '', clean_name, flags=re.IGNORECASE)
    
    # 移除多余空格并返回
    return re.sub(r'\s+', ' ', clean_name).strip()

def get_series_name(filename):
    """提取剧集系列名，用于文件分组
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 小写的剧集系列名
    """
    name = os.path.splitext(filename)[0]
    match = re.search(r'(.*?)[ ._-]*(?:S\d{1,2}|E\d{1,3})', name, re.IGNORECASE)
    if match: 
        return match.group(1).replace('.', ' ').replace('_', ' ').strip().lower()
    return name.split(' ')[0].lower() 

def generate_output_name(filenames, ext=".docx", volume_pattern="智能"):
    """生成合并输出文件名，根据不同模式生成不同格式
    
    目标格式:
    - 整季模式: All.of.Us.Are.Dead.S01.pdf
    - 单集模式: All.of.Us.Are.Dead.S01E01.pdf
    - 电影文件: Kingdom.Ashin.of.the.North.pdf
    
    Args:
        filenames: 文件名列表
        ext: 输出文件扩展名
        volume_pattern: 分卷模式（"整季"或"智能"）
        
    Returns:
        str: 生成的输出文件名
    """
    if not filenames: 
        return f"merged_output{ext}"
    
    basenames = [os.path.basename(f) for f in filenames]
    
    # 解析所有文件的集数信息
    pattern_se = re.compile(r'[Ss](\d{1,2})[\s.]*[Ee](\d{1,3})', re.IGNORECASE)
    pattern_e = re.compile(r'[ ._-][Ee](\d{1,3})', re.IGNORECASE)

    parsed_files = []
    for fname in basenames:
        m = pattern_se.search(fname)
        if m:
            parsed_files.append({'s': int(m.group(1)), 'e': int(m.group(2))})
            continue
        m2 = pattern_e.search(fname)
        if m2:
            parsed_files.append({'s': 1, 'e': int(m2.group(1))})
            continue
        parsed_files.append({'s': 999, 'e': 999})

    # 按季和集数排序
    parsed_files.sort(key=lambda x: (x['s'], x['e']))
    first, last = parsed_files[0], parsed_files[-1]
    
    # 1. 从第一集提取带 S01E01 的完整标题
    full_title = clean_filename_title(basenames[0])
    
    # 2. 切除标题里的集数部分，保留系列名
    series_only = re.sub(r'[._\s]S\d{1,2}[Ee]\d{1,3}.*', '', full_title, flags=re.IGNORECASE).strip()
    
    # 3. 转成点号连接格式
    final_prefix = series_only.replace(' ', '.')

    if first['s'] == 999:
        # 电影文件或没有集数信息的文件：只显示标题
        return f"{final_prefix}{ext}"

    s_start, e_start = first['s'], first['e']
    s_end, e_end = last['s'], last['e']

    # 4. 根据分卷模式拼接总文件名
    if volume_pattern == "整季":
        # 整季模式：只显示季号，不显示集数范围
        return f"{final_prefix}.S{s_start:02d}{ext}"
    elif s_start == s_end:
        # 同一季的情况
        if e_start == e_end:
            # 单集模式：只显示一个集数编号
            return f"{final_prefix}.S{s_start:02d}E{e_start:02d}{ext}"
        else:
            # 多集模式：显示集数范围
            return f"{final_prefix}.S{s_start:02d}E{e_start:02d}-{e_end:02d}{ext}"
    else:
        # 跨季情况：显示完整范围
        return f"{final_prefix}.S{s_start:02d}E{e_start:02d}-S{s_end:02d}E{e_end:02d}{ext}"