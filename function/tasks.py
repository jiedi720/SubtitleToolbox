#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务执行模块
负责处理应用程序的各种任务执行逻辑
"""

import os
from PySide6.QtWidgets import QMessageBox
from logic.txt_logic import run_txt_creation_task
from logic.pdf_logic import run_pdf_task
from logic.word_logic import run_word_creation_task
from font.srt2ass import run_ass_task
from function.merge import run_pdf_merge_task, run_win32_merge_task, run_txt_merge_task
from function.volumes import get_batch_size_from_volume_pattern


def execute_task(task_mode, path_var, output_path_var, log_callback, progress_callback, root, gui, **kwargs):
    """
    执行任务
    
    Args:
        task_mode: 任务模式
        path_var: 源目录路径
        output_path_var: 输出目录路径
        log_callback: 日志回调函数
        progress_callback: 进度回调函数
        root: 根窗口对象
        gui: GUI 对象
        **kwargs: 额外的参数
    """
    # 验证源目录
    target_dir = path_var.strip()
    if not target_dir or not os.path.exists(target_dir):
        QMessageBox.critical(None, "错误", "源目录无效")
        return False
    
    # 获取输出目录
    if output_path_var.strip():
        final_out = output_path_var.strip()
    else:
        final_out = target_dir
    
    log_callback("--- 任务启动 ---")
    
    try:
        if task_mode == "Srt2Ass":
            # 执行SRT转ASS任务
            run_ass_task(
                target_dir, 
                kwargs.get('_get_current_styles', lambda: {'kor': '', 'chn': ''}), 
                log_callback, 
                progress_callback, 
                root, 
                output_dir=final_out
            )
        elif task_mode == "Script":
            # 根据分卷模式获取batch_size
            batch = 0
            if hasattr(gui, 'volume_pattern'):
                batch = get_batch_size_from_volume_pattern(gui.volume_pattern)
            
            # 获取当前分卷模式
            volume_pattern = getattr(gui, 'volume_pattern', '智能')
            
            # 执行各类输出任务
            if gui.output2pdf:
                run_pdf_task(
                    target_dir, 
                    log_callback, 
                    progress_callback, 
                    root, 
                    batch, 
                    final_out, 
                    volume_pattern
                )
            if gui.output2word:
                run_word_creation_task(
                    target_dir, 
                    log_callback, 
                    progress_callback, 
                    root, 
                    batch, 
                    final_out, 
                    volume_pattern
                )
            if gui.output2txt:
                run_txt_creation_task(
                    target_dir, 
                    log_callback, 
                    progress_callback, 
                    root, 
                    batch, 
                    final_out, 
                    volume_pattern
                )
        elif task_mode == "Merge":
            # 执行合并任务
            # 检查Merge标签页中的复选框状态
            try:
                # 获取Merge标签页中的复选框状态
                merge_pdf = gui.MergePDF.isChecked()
                merge_word = gui.MergeWord.isChecked()
                merge_txt = gui.MergeTxt.isChecked()
                
                # 检查是否至少选中了一个合并选项
                if not merge_pdf and not merge_word and not merge_txt:
                    log_callback("❌ 请至少选择一个合并选项")
                    return False
                
                # 根据选中的选项执行相应的合并任务
                if merge_pdf:
                    run_pdf_merge_task(
                        target_dir, 
                        log_callback, 
                        progress_callback, 
                        root, 
                        output_dir=final_out
                    )
                
                if merge_word:
                    run_win32_merge_task(
                        target_dir, 
                        log_callback, 
                        progress_callback, 
                        root, 
                        output_dir=final_out
                    )
                
                if merge_txt:
                    run_txt_merge_task(
                        target_dir, 
                        log_callback, 
                        progress_callback, 
                        root, 
                        output_dir=final_out
                    )
            except Exception as e:
                log_callback(f"❌ Merge模式处理失败: {e}")
                return False
        elif task_mode == "AutoSub":
            # 执行自动字幕生成任务
            try:
                from function.AutoSubtitles import SubtitleGenerator
                
                # 获取模型配置
                from function.settings import ConfigManager
                config = ConfigManager()
                model_config = config.get_whisper_model_config()
                model_size = model_config["model_size"]
                model_path = model_config["model_path"]
                
                # 创建字幕生成器
                generator = SubtitleGenerator(
                    model_size=model_size,
                    model_path=model_path,
                    device="auto",
                    language=model_config.get("language", None),
                    allow_download=model_config.get("allow_download", False)
                )
                
                # 初始化模型
                generator.initialize_model(progress_callback=lambda m: log_callback(m))
                
                # 批量处理
                results = generator.batch_process(
                    input_dir=target_dir,
                    progress_callback=lambda m: log_callback(m)
                )
                
                # 统计结果
                success_count = sum(1 for _, _, success in results if success)
                fail_count = len(results) - success_count
                
                log_callback(f"\n✓ 处理完成: 成功 {success_count} 个，失败 {fail_count} 个")
                
                # 清理模型资源
                try:
                    del generator
                    log_callback("已释放模型资源")
                except:
                    pass
                
            except Exception as e:
                log_callback(f"❌ AutoSub模式处理失败: {e}")
                import traceback
                log_callback(f"详细错误: {traceback.format_exc()}")
                return False
        
        log_callback("✅ 任务流处理完毕。")
        return True
        
    except Exception as e: 
        log_callback(f"❌ 出错: {e}")
        return False
