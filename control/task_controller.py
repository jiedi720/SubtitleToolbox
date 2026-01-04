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
                if self.do_pdf:
                    run_pdf_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, batch, final_out, volume_pattern)
                if self.do_word:
                    run_word_creation_task(target_dir, lambda m, **kwargs: self.log(m, **kwargs), self.update_progress, self.root, batch, final_out, volume_pattern)
                if self.do_txt:
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
            dict: 包含韩文字幕样式和中文字幕样式的字典
        """
        if hasattr(self, 'kor_panel_ui'):
            # 如果有UI面板，从面板获取样式
            kor_style = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, "KOR")
            chn_style = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN")
            return {"kor": kor_style, "chn": chn_style}
        # 否则返回解析后的默认样式
        return {"kor": self.kor_parsed["raw"], "chn": self.chn_parsed["raw"]}