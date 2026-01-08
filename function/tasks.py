#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务执行模块
负责处理应用程序的各种任务执行逻辑
"""

import os
import sys

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
        **kwargs: 其他参数
    """
    # 声明全局变量
    global _global_generator
    # 如果全局变量不存在，初始化它
    try:
        _global_generator
    except NameError:
        _global_generator = None
    # 验证源目录
    target_dir = path_var.strip()
    if not target_dir or not os.path.exists(target_dir):
        QMessageBox.critical(root, "错误", "源目录无效")
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
            if gui.Output2PDF:
                run_pdf_task(
                    target_dir, 
                    log_callback, 
                    progress_callback, 
                    root, 
                    batch, 
                    final_out, 
                    volume_pattern
                )
            if gui.Output2Word:
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
            from function.AutoSubtitles import SubtitleGenerator

            # 获取模型配置（从控制器获取，确保使用最新的设置）
            # 注意：root 在 PySide6 中可能是 None，所以直接使用传入的 gui 对象
            model_config = gui.app.config.get_whisper_model_config()
            model_size = model_config["model_size"]
            model_path = model_config["model_path"]

            # 创建字幕生成器
            language_setting = model_config.get("language", None)
            log_callback(f"DEBUG: 语言设置: {language_setting}")
            
            # 清理之前的 generator 对象
            if _global_generator is not None:
                log_callback("DEBUG: 清理之前的 generator 对象")
                _global_generator = None
            
            generator = SubtitleGenerator(
                model_size=model_size,
                model_path=model_path,
                device="auto",
                language=language_setting,
                allow_download=model_config.get("allow_download", False)
            )
            log_callback(f"DEBUG: generator.language = {generator.language}")

            try:
                # 初始化模型
                generator.initialize_model(log_callback=log_callback)

                # 检测已生成的字幕文件
                mp3_files = []
                for root, _, files in os.walk(target_dir):
                    for file in files:
                        if file.lower().endswith(".mp3"):
                            mp3_files.append(os.path.join(root, file))

                existing_files = []
                new_files = []

                for mp3_file in mp3_files:
                    base_name = os.path.splitext(os.path.basename(mp3_file))[0]
                    dir_name = os.path.dirname(mp3_file)

                    has_subtitle = False
                    for file in os.listdir(dir_name):
                        if file.startswith(f"{base_name}.whisper.[") and file.endswith(".srt"):
                            has_subtitle = True
                            break

                    if has_subtitle:
                        existing_files.append(mp3_file)
                    else:
                        new_files.append(mp3_file)

                skip_existing = True
                if existing_files:
                    log_callback(f"检测到 {len(existing_files)} 个文件已生成字幕")
                    # 暂时跳过对话框，直接跳过已存在的文件
                    skip_existing = True
                    log_callback(f"将跳过 {len(existing_files)} 个已存在的字幕文件")

                if skip_existing:
                    log_callback(f"将跳过 {len(existing_files)} 个已存在的字幕文件")
                else:
                    log_callback(f"将覆盖 {len(existing_files)} 个已存在的字幕文件")

                # 批量处理
                results = generator.batch_process(
                    input_dir=target_dir,
                    progress_callback=progress_callback,
                    log_callback=log_callback,
                    skip_existing=skip_existing
                )

                # 统计结果
                success_count = sum(1 for _, _, success in results if success)
                fail_count = len(results) - success_count

                log_callback(f"\n✅ 处理完成: 成功 {success_count} 个，失败 {fail_count} 个")

                log_callback("--- AutoSub任务完成 ---")
                
                # 不调用 cleanup()，让 Python 的垃圾回收器自动处理
                log_callback("DEBUG: [A] 跳过模型清理，让 GC 自动处理")
                log_callback("DEBUG: [B] AutoSub 任务块完成")
                
            except Exception as e:
                log_callback(f"❌ AutoSub模式处理失败: {e}")
                import traceback
                log_callback(f"详细错误: {traceback.format_exc()}")
                log_callback("DEBUG: [E] AutoSub 异常捕获")
                return False
        
        # 任务完成日志
        log_callback("DEBUG: [F] 准备输出完成日志")
        log_callback("✅ 任务流处理完毕。")
        log_callback("--- execute_task函数返回 ---")
        
        # 不做任何清理操作，让 Python 的垃圾回收器自然处理
        # 自动模式下 Whisper 的析构函数会卡死，所以不能显式清理
        if task_mode == "AutoSub" and model_config.get("language") is None:
            log_callback("DEBUG: 自动模式，跳过模型清理（避免析构函数卡死）")
        
        # 强制刷新所有输出
        sys.stdout.flush()
        sys.stderr.flush()
        
        log_callback("DEBUG: [G] execute_task 函数即将返回")
        
        # 将 generator 对象保存到全局变量中，防止它被清理
        if 'generator' in locals():
            _global_generator = generator
            log_callback("DEBUG: generator 对象已保存到全局变量")
        
        # 不使用 return 语句，直接让函数结束
        # Python 会自动返回 None
        # 调用者需要检查 None 并视为 True        
    except Exception as e: 
        log_callback(f"❌ 出错: {e}")
        import traceback
        log_callback(f"详细错误: {traceback.format_exc()}")
        return False