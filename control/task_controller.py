import os
import threading
from PySide6.QtWidgets import QMessageBox
from logic.txt_logic import run_txt_creation_task
from logic.pdf_logic import run_pdf_task
from logic.word_logic import run_word_creation_task
from font.srt2ass import run_ass_task
from function.volumes import get_batch_size_from_volume_pattern


class TaskController:
    """
    任务控制器类，负责管理应用程序的各种任务执行
    支持多线程执行，避免阻塞GUI界面
    """
    
    def start_thread(self): 
        """启动任务线程"""
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        """
        处理任务的主方法，根据任务模式执行不同的任务
        """
        # 验证源目录
        target_dir = self.path_var.strip()
        if not target_dir or not os.path.exists(target_dir):
            QMessageBox.critical(None, "错误", "源目录无效")
            return
        
        # 获取输出目录
        final_out = self.get_output_dir()
            
        # 更新GUI状态：禁用开始按钮，重置进度条
        self.enable_start_button.emit(False)
        self.update_progress.emit(0)
        
        self.log(f"--- 任务启动 ---")
        try:
            # 根据任务模式执行不同的任务
            if self.task_mode == "Srt2Ass":
                # 执行SRT转ASS任务
                run_ass_task(target_dir, self._get_current_styles(), self.log, self.update_progress, self.root, output_dir=final_out)
            elif self.task_mode == "Script":
                # 根据分卷模式获取batch_size
                batch = 0
                if hasattr(self, 'volume_pattern'):
                    batch = get_batch_size_from_volume_pattern(self.volume_pattern)
                
                # 获取当前分卷模式
                volume_pattern = self.volume_pattern if hasattr(self, 'volume_pattern') else "智能"
                
                # 执行各类输出任务
                if self.output2pdf:
                    run_pdf_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, batch, final_out, volume_pattern)
                if self.output2word:
                    run_word_creation_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, batch, final_out, volume_pattern)
                if self.output2txt:
                    run_txt_creation_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, batch, final_out, volume_pattern)
            elif self.task_mode == "Merge":
                # 执行合并任务
                # 检查Merge标签页中的复选框状态
                try:
                    # 获取Merge标签页中的复选框状态
                    merge_pdf = self.gui.MergePDF.isChecked()
                    merge_word = self.gui.MergeWord.isChecked()
                    merge_txt = self.gui.MergeTxt.isChecked()
                    
                    # 检查是否至少选中了一个合并选项
                    if not merge_pdf and not merge_word and not merge_txt:
                        self.log("❌ 请至少选择一个合并选项")
                        return
                    
                    # 根据选中的选项执行相应的合并任务
                    if merge_pdf:
                        from function.merge import run_pdf_merge_task
                        run_pdf_merge_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, output_dir=final_out)
                    
                    if merge_word:
                        from function.merge import run_win32_merge_task
                        run_win32_merge_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, output_dir=final_out)
                    
                    if merge_txt:
                        from function.merge import run_txt_merge_task
                        run_txt_merge_task(target_dir, self.log, self.update_progress, self.root, output_dir=final_out)
                except Exception as e:
                    self.log(f"❌ Merge模式处理失败: {e}")
            elif self.task_mode == "AutoSub":
                # 执行自动字幕生成任务
                try:
                    from function.AutoSubtitles import SubtitleGenerator
                    
                    # 获取模型配置
                    model_config = self.get_whisper_model_config()
                    model_size = model_config["model_size"]
                    model_path = model_config["model_path"]
                    
                    # 创建字幕生成器
                    generator = SubtitleGenerator(
                        model_size=model_size,
                        model_path=model_path,
                        device="auto"
                    )
                    
                    # 初始化模型
                    generator.initialize_model(progress_callback=lambda m: self.log(m))
                    
                    # 批量处理
                    results = generator.batch_process(
                        input_dir=target_dir,
                        output_format="srt",
                        progress_callback=lambda m: self.log(m)
                    )
                    
                    # 统计结果
                    success_count = sum(1 for _, _, success in results if success)
                    fail_count = len(results) - success_count
                    
                    self.log(f"\n✓ 处理完成: 成功 {success_count} 个，失败 {fail_count} 个")
                    
                except Exception as e:
                    self.log(f"❌ AutoSub模式处理失败: {e}")
                    import traceback
                    self.log(f"详细错误: {traceback.format_exc()}")
            
            self.log("✅ 任务流处理完毕。")
        except Exception as e: 
            self.log(f"❌ 出错: {e}")
        finally:
            # 任务完成后恢复GUI状态
            self.enable_start_button.emit(True)
            self.update_progress.emit(0)

    def _get_current_styles(self):
        """
        获取当前样式设置
        
        Returns:
            dict: 包含外语字幕样式和中文字幕样式的字典
        """
        # 根据当前预设确定外语键名
        lang_key_mapping = {
            "kor_chn": "kor",
            "jpn_chn": "jpn",
            "eng_chn": "eng"
        }
        lang_key = lang_key_mapping.get(self.ass_pattern, "kor")
        
        if hasattr(self, 'kor_panel_ui'):
            # 如果有UI面板，从面板获取样式
            lang_style = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, lang_key.upper())
            chn_style = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN")
            return {lang_key: lang_style, "chn": chn_style}
        # 否则返回解析后的默认样式
        return {lang_key: self.kor_parsed["raw"], "chn": self.chn_parsed["raw"]}