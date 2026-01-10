"""
文件清理模块
负责将文件发送到回收站，提供智能清理功能，永远不会删除.srt原始文件。
"""

import os
from PySide6.QtWidgets import QMessageBox

__all__ = [
    'clear_output_to_trash'
]

try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False

def clear_output_to_trash(target_root, log_func, parent=None, current_mode=None):
    """智能清理输出目录，将文件发送到回收站

    根据不同模式实现不同的清理逻辑：
    - Script，Merge，Srt2Ass模式：只清理生成的文件，不要清理任何原始文件
    - AutoSub模式：只清理目标目录里生成的whisper字幕，不处理子文件夹

    注意：永远不会删除 .srt 原始文件，仅对被占用的文件名使用错误标签。

    Args:
        target_root: 目标根目录
        log_func: 日志记录函数
        parent: 父窗口对象，用于继承主题设置
        current_mode: 当前任务模式
    """
    if not HAS_SEND2TRASH:
        QMessageBox.critical(parent, "缺少组件", "请安装：pip install send2trash")
        return

    # 直接处理目标目录，不再寻找script文件夹
    cleanup_dir = target_root

    if not os.path.exists(cleanup_dir):
        log_func("[清理] ℹ️ 目录不存在。")
        return

    try:
        items = os.listdir(cleanup_dir)
    except Exception as e:
        log_func(f"❌ 无法读取目录: {e}")
        return

    if not items:
        log_func("[清理] ℹ️ 目录已空。")
        return

    if not QMessageBox.question(parent, "确认清空", f"即将清空: {cleanup_dir}\n确定吗？", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        return

    deleted_total = 0
    error_total = 0
    deleted_items = []  # 记录具体清理的项目

    for item in items:
        full_path = os.path.abspath(os.path.join(cleanup_dir, item))
        
        # 检查文件是否为原始文件，根据不同模式决定是否跳过
        is_original_file = False
        
        if current_mode in ["Script", "Merge", "Srt2Ass"]:
            # Script，Merge，Srt2Ass模式：只清理生成的文件，不要清理任何原始文件
            # 原始文件包括：.srt, .vtt, .ass, .smi, .mp3, .mp4, .mkv, .avi等媒体文件和字幕文件
            original_extensions = ['.srt', '.vtt', '.ass', '.smi', '.mp3', '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv']
            if any(item.lower().endswith(ext) for ext in original_extensions):
                is_original_file = True
            
            # Script，Merge，Srt2Ass模式下，不要清理任何原始文件，包括生成的.ass文件
            # 对于Script和Merge模式，.pdf, .docx, .txt可能是生成的文件
            # 对于Srt2Ass模式，.ass是生成的文件，也不要清理
        
        # 永远不会删除 .srt 原始文件
        if item.lower().endswith('.srt'):
            is_original_file = True
        
        if is_original_file:
            continue
            
        try:
            if os.path.isdir(full_path):
                # 检查当前模式
                if current_mode in ["Script", "Merge", "Srt2Ass"]:
                    # Script、Merge、Srt2Ass模式下，只清空生成的pdf、word、txt子文件夹
                    generated_folders = ["pdf", "word", "txt"]
                    if item.lower() in generated_folders:
                        # 递归清理生成的子文件夹
                        d, e, recursive_items = _recursive_delete(full_path, log_func, current_mode)
                        deleted_total += d
                        error_total += e
                        # 保存完整路径的相对形式，显示更清晰
                        for recursive_item in recursive_items:
                            full_item_path = os.path.join(item, recursive_item)
                            deleted_items.append(full_item_path)
                        # 删除空文件夹
                        try:
                            send2trash(full_path)
                            deleted_total += 1
                            deleted_items.append(item)
                        except Exception:
                            # 文件夹可能不是空的，或者有其他问题，忽略
                            pass
                else:
                    # 其他模式下，正常递归清理文件夹
                    d, e, recursive_items = _recursive_delete(full_path, log_func, current_mode)
                    deleted_total += d
                    error_total += e
                    # 保存完整路径的相对形式，显示更清晰
                    for recursive_item in recursive_items:
                        full_item_path = os.path.join(item, recursive_item)
                        deleted_items.append(full_item_path)
                    # 删除空文件夹
                    try:
                        send2trash(full_path)
                        deleted_total += 1
                        deleted_items.append(item)
                    except Exception:
                        # 文件夹可能不是空的，或者有其他问题，忽略
                        pass
            else:
                # 删除单个文件
                send2trash(full_path)
                deleted_total += 1
                deleted_items.append(item)
        except Exception:
            # 针对单个文件占用，使用错误标签
            log_func(f"❌ 占用中: {item}", "error")
            error_total += 1

    # 汇总信息
    if deleted_total > 0:
        log_func(f"✅ 已清理完成，共处理 {deleted_total} 个项目", "success")
        # 列出具体清理的项目
        log_func("[清理] 已清理的项目:")
        for item in deleted_items:
            log_func(f"  - {item}")
    if error_total > 0:
        log_func(f"⚠️ 提示: 仍有 {error_total} 个文件未删除，请参考上方红字路径。")

def _recursive_delete(folder_path, log_func, current_mode=None):
    """递归清理文件夹，将文件发送到回收站
    
    Args:
        folder_path: 文件夹路径
        log_func: 日志记录函数
        current_mode: 当前任务模式
        
    Returns:
        tuple: (删除成功数量, 删除失败数量, 已删除项目列表)
    """
    d_count = 0
    e_count = 0
    deleted_items = []
    
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_p = os.path.join(root, name)
            
            # 检查文件是否为原始文件，根据不同模式决定是否跳过
            is_original_file = False
            
            if current_mode in ["Script", "Merge", "Srt2Ass"]:
                # Script，Merge，Srt2Ass模式：只清理生成的文件，不要清理任何原始文件
                # 原始文件包括：.srt, .vtt, .ass, .smi, .mp3, .mp4, .mkv, .avi等媒体文件和字幕文件
                original_extensions = ['.srt', '.vtt', '.ass', '.smi', '.mp3', '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv']
                if any(name.lower().endswith(ext) for ext in original_extensions):
                    is_original_file = True
                
                # Script，Merge，Srt2Ass模式下，不要清理任何原始文件，包括生成的.ass文件
            # 对于Script和Merge模式，.pdf, .docx, .txt可能是生成的文件
            # 对于Srt2Ass模式，.ass是生成的文件，也不要清理
            
            # 永远不会删除 .srt 原始文件
            if name.lower().endswith('.srt'):
                is_original_file = True
            
            if is_original_file:
                continue
            
            try:
                send2trash(os.path.abspath(file_p))
                d_count += 1
                # 保存相对路径，显示更清晰
                relative_path = os.path.relpath(file_p, folder_path)
                deleted_items.append(relative_path)
            except Exception:
                # 仅对该行报错使用错误标签
                relative_path = os.path.join(os.path.basename(root), name)
                log_func(f"❌ 占用中: {relative_path}", "error")
                e_count += 1
        
        for name in dirs:
            dir_p = os.path.join(root, name)
            try:
                if not os.listdir(dir_p):
                    os.rmdir(dir_p)
            except:
                pass
                
    return d_count, e_count, deleted_items