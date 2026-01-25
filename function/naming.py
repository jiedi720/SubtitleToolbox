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
    """从文件名中提取纯净标题
    
    保留对单集集数的识别，确保 PDF 内部标题含有 S01E01 格式。
    对于没有 S01E01 或年份标识的文件名，保留完整的原始文件名（包括括号、空格、连字符等特殊字符）。
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 清理后的纯净标题
    """
    name = os.path.splitext(filename)[0]
    
    # 移除 whisper 相关后缀，如 .whisper.[kor]、.whisper.[eng] 等
    # 处理各种变体：大小写不敏感，允许空格
    whisper_pattern = r'\.whisper[\s.]*\[[^\]]+\][\s.]*'
    name = re.sub(whisper_pattern, '', name, flags=re.IGNORECASE)
    
    # 提取 S01E01 或 年份之前的标题部分
    match_se = re.search(r'(.*?(?:S\d{1,2}[\s.]?E\d{1,3}|E\d{1,3}))', name, re.IGNORECASE)
    if match_se: 
        name = match_se.group(1)
        # 对于有集数标识的文件，替换分隔符为空格并清理
        clean_name = name.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        return re.sub(r'\s+', ' ', clean_name).strip()
    else:
        # 对于电影文件，尝试提取年份之前的部分
        match_year = re.search(r'(.*?)[._\s(\[](19|20)\d{2}', name)
        if match_year: 
            # 保留到年份为止，包括年份
            year_pos = match_year.end()
            name = name[:year_pos]
            # 对于有年份的文件，替换分隔符为空格并清理
            clean_name = name.replace('.', ' ').replace('_', ' ').replace('-', ' ')
            return re.sub(r'\s+', ' ', clean_name).strip()
        else:
            # 如果没有找到 S01E01 或年份，保留完整的原始文件名
            # 不做任何清理，只移除文件扩展名
            # 这样可以保留括号、空格、连字符等特殊字符
            return name.strip()

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

def generate_output_name(filenames, ext=".docx", volume_pattern="智能", target_dir=None):
    """生成合并输出文件名，根据不同模式生成不同格式
    
    目标格式:
    - 整季模式: All.of.Us.Are.Dead.S01.pdf
    - 单集模式: All.of.Us.Are.Dead.S01E01.pdf
    - 电影文件: Kingdom.Ashin.of.the.North.pdf
    - 无剧集编号的整季文件: Korean.Grammar.in.Use.Be.Jp.pdf
    
    Args:
        filenames: 文件名列表
        ext: 输出文件扩展名
        volume_pattern: 分卷模式（"整季"或"智能"）
        target_dir: 目标目录路径，用于提取目录标题名称
        
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
    
    # 1. 检查是否有剧集编号
    has_episode_number = any(p['s'] != 999 for p in parsed_files)
    
    # 2. 如果没有剧集编号，提取文件的共有名称
    common_prefix = None
    if not has_episode_number:
        # 提取文件名的基础名称（不含扩展名）
        base_names = [os.path.splitext(fname)[0] for fname in basenames]
        if base_names:
            # 找到最长的共有前缀
            common_prefix = os.path.commonprefix(base_names)
            # 清理共有前缀，去除末尾的分隔符和不需要的字符串
            common_prefix = re.sub(r'[._-]+$', '', common_prefix)
            # 移除不需要的字符串，如whisper和[kor]
            junk_patterns = [
                r'\.whisper', 
                r'\[kor\]', r'\[chi\]', r'\[cht\]',
                r'@[^@\s]+@',  # 匹配 @xxx@ 格式的字符串
                r'￡[^￡\s]*@[^\s]*',  # 匹配 ￡xxx@xxx 格式的字符串
                r'_track\d+',  # 匹配 _track7 格式的字符串
            ]
            for pattern in junk_patterns:
                common_prefix = re.sub(pattern, '', common_prefix, flags=re.IGNORECASE)
            # 再次清理，确保没有多余的分隔符
            common_prefix = re.sub(r'[._-]+$', '', common_prefix)
    
    # 3. 如果没有共有前缀，使用传统方式处理
    if not common_prefix:
        # 从第一集提取带 S01E01 的完整标题
        full_title = clean_filename_title(basenames[0])
        
        # 切除标题里的集数部分，保留系列名
        series_only = re.sub(r'[._\s]S\d{1,2}[Ee]\d{1,3}.*', '', full_title, flags=re.IGNORECASE).strip()
        
        # 转成点号连接格式
        final_prefix = series_only.replace(' ', '.')
    else:
        # 使用共有前缀作为最终前缀
        final_prefix = common_prefix.replace(' ', '.')

    if first['s'] == 999:
        # 电影文件或没有集数信息的文件：使用年份之前的标题
        # 从第一个文件名中提取年份之前的部分
        first_basename = os.path.splitext(basenames[0])[0]
        
        # 尝试匹配年份 (19xx 或 20xx)
        match_year = re.search(r'(.*?)[._\s(\[](19|20)\d{2}', first_basename)
        if match_year:
            # 保留到年份为止，包括年份
            year_pos = match_year.end()
            movie_title = first_basename[:year_pos]
        else:
            # 如果没有找到年份，使用当前的 final_prefix
            movie_title = final_prefix
        
        # 清理电影标题中的垃圾信息
        junk_patterns = [
            r'\.whisper', 
            r'\[kor\]', r'\[chi\]', r'\[cht\]',
            r'@[^@\s]+@',  # 匹配 @xxx@ 格式的字符串
            r'￡[^￡\s]*@[^\s]*',  # 匹配 ￡xxx@xxx 格式的字符串
            r'_track\d+',  # 匹配 _track7 格式的字符串
        ]
        for pattern in junk_patterns:
            movie_title = re.sub(pattern, '', movie_title, flags=re.IGNORECASE)
        
        # 清理末尾的分隔符
        movie_title = re.sub(r'[._-]+$', '', movie_title)
        
        # 转换为点号连接格式
        final_prefix = movie_title.replace(' ', '.')
        
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