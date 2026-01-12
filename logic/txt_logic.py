"""
TXT文档生成与合并模块
负责将字幕文件转换为TXT文档，并提供TXT文档合并功能。
"""

import os
from function.file_utils import get_save_path, get_organized_path, find_files_recursively
from function.volumes import smart_group_files
from function.parsers import parse_subtitle_to_list
from function.naming import generate_output_name, clean_filename_title

def run_txt_creation_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None, volume_pattern="智能", stop_flag=[False]):
    """运行TXT文档生成任务
    
    从指定目录扫描字幕文件，生成带时间戳的TXT文档。
    
    Args:
        target_dir: 目标目录
        log_func: 日志记录函数
        progress_bar: 进度条信号
        root: 根窗口
        batch_size: 批量大小
        output_dir: 输出目录
        volume_pattern: 分卷模式
    """
    log_func(f"[TXT生成] 扫描目录: {target_dir.replace('/', '\\')}")
    # 递归查找字幕文件
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass', '.smi'))
    
    if not files:
        return log_func(f"❌ 未找到任何字幕文件")

    # 智能分组文件
    file_groups = smart_group_files(files, batch_size)
    total_files = len(files)
    count = 0

    # 确定基础输出目录
    base_output_dir = output_dir if output_dir else target_dir

    for group in file_groups:
        # 检查停止标志
        if stop_flag[0]:
            return
            
        if not group: 
            continue
        
        # 生成输出文件名
        out_name = generate_output_name([os.path.basename(f) for f in group], ".txt", volume_pattern)
        # 获取组织化路径
        out_path = get_organized_path(base_output_dir, out_name)
        
        try:
            with open(out_path, 'w', encoding='utf-8') as outfile:
                for fp in group:
                    # 检查停止标志
                    if stop_flag[0]:
                        log_func("⚠️ 任务已被用户停止")
                        return
                        
                    title = clean_filename_title(os.path.basename(fp))
                    outfile.write(f"{'='*50}\n【{title}】\n{'='*50}\n\n")
                    
                    # 解析字幕内容
                    content_list = parse_subtitle_to_list(fp)
                    if not content_list:
                        outfile.write("[内容为空或解析失败]\n\n")
                    else:
                        for time_str, text in content_list:
                            # 检查停止标志
                            if stop_flag[0]:
                                log_func("⚠️ 任务已被用户停止")
                                return
                            
                            outfile.write(f"[{time_str}]  {text}\n")
                    outfile.write("\n\n")
                    
                    count += 1
                    # 更新进度，支持不同类型的进度回调
                    try:
                        # 尝试PyQt的信号方式（progress_bar是信号对象）
                        progress_bar.emit(int(count / total_files * 100))
                    except AttributeError:
                        try:
                            # 尝试直接调用方式（progress_bar是emit方法本身）
                            progress_bar(int(count / total_files * 100))
                        except Exception as e:
                            pass
            log_func(f"📄 已生成: {os.path.join('txt', out_name).replace('/', '\\')}")
        except Exception as e:
            log_func(f"❌ 写入失败 {out_name}: {e}")

    # 重置进度条
    try:
        progress_bar.emit(0)
    except AttributeError:
        try:
            progress_bar(0)
        except Exception as e:
            pass

