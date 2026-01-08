#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具任务模块
负责处理各种工具任务，如合并任务和清理任务
"""

import os
import threading
from PySide6.QtWidgets import QMessageBox
from function.merge import run_txt_merge_task, run_pdf_merge_task, run_win32_merge_task
from function.trash import clear_output_to_trash


def start_generic_task(task_func, path_var, log_callback, update_progress, root, gui, **kwargs):
    """
    启动通用任务
    
    Args:
        task_func: 要执行的任务函数
        path_var: 源目录路径
        log_callback: 日志回调函数
        update_progress: 进度回调函数
        root: 根窗口对象
        gui: GUI 对象
        **kwargs: 额外的参数
    """
    # 获取目标目录
    target = path_var.strip()
    if not target or not os.path.exists(target): 
        QMessageBox.critical(None, "错误", "请选择有效目录")
        return
    
    # 设置日志回调
    final_log = log_callback if log_callback else None
    
    # 更新进度条
    if hasattr(gui, 'ProgressBar'):
        gui.ProgressBar.setValue(0)

    # 启动任务线程
    threading.Thread(
        target=task_func,
        args=(target, final_log, update_progress, root),
        kwargs={'output_dir': kwargs.get('output_dir', target)},
        daemon=True
    ).start()


def execute_merge_tasks(path_var, output_path_var, log_callback, update_progress, root, gui):
    """
    执行合并任务
    
    Args:
        path_var: 源目录路径
        output_path_var: 输出目录路径
        log_callback: 日志回调函数
        update_progress: 进度回调函数
        root: 根窗口对象
        gui: GUI 对象
    """
    # 获取目标目录
    target_dir = path_var.strip()
    if not target_dir or not os.path.exists(target_dir):
        QMessageBox.critical(None, "错误", "请选择有效目录")
        return
    
    # 获取输出目录
    if output_path_var.strip():
        final_out = output_path_var.strip()
    else:
        final_out = target_dir
    
    # 检查Merge标签页中的复选框状态
    try:
        # 获取Merge标签页中的复选框状态
        merge_pdf = gui.MergePDF.isChecked()
        merge_word = gui.MergeWord.isChecked()
        merge_txt = gui.MergeTxt.isChecked()
        
        # 检查是否至少选中了一个合并选项
        if not merge_pdf and not merge_word and not merge_txt:
            log_callback("❌ 请至少选择一个合并选项")
            return
        
        # 根据选中的选项执行相应的合并任务
        if merge_pdf:
            run_pdf_merge_task(
                target_dir, 
                log_callback, 
                update_progress, 
                root, 
                output_dir=final_out
            )
        
        if merge_word:
            run_win32_merge_task(
                target_dir, 
                log_callback, 
                update_progress, 
                root, 
                output_dir=final_out
            )
        
        if merge_txt:
            run_txt_merge_task(
                target_dir, 
                log_callback, 
                update_progress, 
                root, 
                output_dir=final_out
            )
            
    except Exception as e:
        log_callback(f"❌ Merge模式处理失败: {e}")