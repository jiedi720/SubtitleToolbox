#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制器模块
整合了所有控制器功能，包括基础控制器、UI控制器、任务控制器和工具控制器
"""

import os
import re
import threading
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QDialog, QInputDialog, QMessageBox
from function.settings import ConfigManager, DEFAULT_KOR_STYLE, DEFAULT_CHN_STYLE
from function.tasks import execute_task
from function.merge import execute_merge_tasks


class BaseController(QObject):
    """
    基础控制器类，提供应用程序的核心功能和状态管理
    继承自QObject以支持信号和槽机制
    """
    # 信号定义：用于线程安全地更新GUI
    update_log = Signal(str)  # 更新日志信号
    update_progress = Signal(int)  # 更新进度条信号
    enable_start_button = Signal(bool)  # 启用/禁用开始按钮信号
    show_overwrite_dialog = Signal(int)  # 显示覆盖对话框信号，参数为已存在文件数量
    
    def __init__(self, root, startup_path=None, startup_out=None):
        """
        初始化基础控制器
        
        Args:
            root: 根窗口对象
            startup_path: 启动时的源目录路径
            startup_out: 启动时的输出目录路径
        """
        super().__init__()
        self.root = root
        
        # 初始化配置管理器
        self.config = ConfigManager()
        
        # 加载设置
        self.config.load_settings()
        
        # 将配置属性同步到控制器实例
        self.config.sync_to_controller(self)
        
        # 用于存储用户选择（是否跳过已存在的文件）
        self.skip_existing = True

    def load_settings(self):
        """从配置文件加载设置"""
        self.config.load_settings()
        self.config.sync_to_controller(self)

    def save_settings(self):
        """保存设置到配置文件"""
        self.config.sync_from_controller(self)
        self.config.save_settings()

    def refresh_parsed_styles(self):
        """刷新解析后的样式"""
        self.config.refresh_parsed_styles()
        self.config.sync_to_controller(self)

    def log(self, message, tag=None):
        """
        记录日志信息
        
        Args:
            message: 日志消息
            tag: 日志标签（可选）
        """
        # 使用信号线程安全地更新日志
        self.update_log.emit(message)
    
    def delete_generated_files(self):
        """删除生成的文件"""
        from function.trash import clear_output_to_trash
        import re
        
        # 获取目标目录
        target_dir = self.output_path_var.strip() or self.path_var.strip()
        if not target_dir:
            self.log("❌ 请先选择源目录或输出目录")
            return
        
        # 检查当前模式
        current_mode = getattr(self, 'task_mode', None)
        
        if current_mode == "AutoSub":
            # AutoSub 模式：只删除 .whisper.[].srt 文件
            self._delete_autosub_files(target_dir)
        else:
            # 其他模式：使用现有的清理功能
            clear_output_to_trash(target_dir, self.log, self.root)
    
    def _delete_autosub_files(self, target_dir):
        """删除 AutoSub 生成的 .whisper.[].srt 文件
        
        Args:
            target_dir: 目标目录
        """
        from send2trash import send2trash
        from PySide6.QtWidgets import QMessageBox
        
        if not os.path.exists(target_dir):
            self.log("[清理] ℹ️ 目录不存在。")
            return
        
        # 查找所有 .whisper.[].srt 文件
        whisper_files = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                # 匹配 .whisper.[xxx].srt 格式
                if re.search(r'\.whisper\.\[[^\]]+\]\.srt$', file, re.IGNORECASE):
                    file_path = os.path.join(root, file)
                    whisper_files.append(file_path)
        
        if not whisper_files:
            self.log("[清理] ℹ️ 未找到 .whisper.[].srt 文件。")
            return
        
        # 确认删除
        if not QMessageBox.question(
            self.root,
            "确认清空",
            f"即将删除 {len(whisper_files)} 个 AutoSub 生成的字幕文件\n确定吗？",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            return
        
        # 删除文件
        deleted_count = 0
        error_count = 0
        
        for file_path in whisper_files:
            try:
                send2trash(file_path)
                deleted_count += 1
                relative_path = os.path.relpath(file_path, target_dir)
                self.log(f"✓ 已删除: {relative_path}")
            except Exception as e:
                error_count += 1
                relative_path = os.path.relpath(file_path, target_dir)
                self.log(f"❌ 删除失败: {relative_path} ({e})", "error")
        
        # 汇总
        if deleted_count > 0:
            self.log(f"✅ 已清理完成，共删除 {deleted_count} 个文件", "success")
        if error_count > 0:
            self.log(f"⚠️ 有 {error_count} 个文件删除失败", "error")
    
    def get_whisper_model_config(self):
        """
        获取 Whisper 模型配置
        
        Returns:
            dict: 包含模型大小和模型路径的字典
        """
        return self.config.get_whisper_model_config()


class UIController:
    """
    UI控制器类，负责处理UI相关的逻辑，如目录管理和预设切换
    """
    
    def open_current_folder(self):
        """打开当前源目录"""
        folder_path = self.path_var.strip()
        if folder_path and os.path.isdir(folder_path): 
            os.startfile(folder_path)

    def get_output_dir(self):
        """
        获取输出目录路径

        Returns:
            str: 输出目录路径
        """
        # 优先使用自定义输出目录
        custom_output = self.output_path_var.strip()
        if custom_output:
            return custom_output

        # 否则直接返回源目录
        return self.path_var.strip()

    def open_output_folder(self):
        """打开输出目录，如果目录不存在则创建"""
        output_dir = self.get_output_dir()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except:
                pass
        if os.path.isdir(output_dir): 
            os.startfile(output_dir)

    def on_preset_change(self, event):
        """
        处理预设切换事件
        
        Args:
            event: 预设切换事件
        """
        preset_name = self.ass_pattern
        if preset_name in self.presets:
            # 刷新解析后的样式
            self.refresh_parsed_styles()
            
            # 如果有UI面板，更新面板上的样式设置
            if hasattr(self, 'kor_panel_ui'):
                # 遍历韩文字幕和中文字幕样式
                for lang, parsed_style in [('kor', self.kor_parsed), ('chn', self.chn_parsed)]:
                    # 获取对应的UI面板
                    ui_panel = getattr(self, f"{lang}_panel_ui")
                    # 更新面板上的样式设置
                    for key, value in parsed_style.items():
                        var_key = f"{key}_var"
                        if var_key in ui_panel:
                            ui_panel[var_key].set(value)


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
        # 更新GUI状态：禁用开始按钮，重置进度条
        self.enable_start_button.emit(False)
        self.update_progress.emit(0)

        # 在子线程中执行任务，避免阻塞主线程
        # 不使用 daemon=True，让线程正常结束
        threading.Thread(
            target=self._run_task_in_thread,
            daemon=False
        ).start()

    def _run_task_in_thread(self):
        """在线程中运行任务"""
        success = False
        try:
            self.log("--- 任务启动 ---")
            # 执行任务
            success = execute_task(
                task_mode=self.task_mode,
                path_var=self.path_var,
                output_path_var=self.output_path_var,
                log_callback=self.log,
                progress_callback=self.update_progress.emit,
                root=self.root,
                gui=self.gui,
                _get_current_styles=self._get_current_styles
            )
            if success is None:
                success = True
        except Exception as e:
            # 捕获任务执行过程中的异常
            import traceback
            self.log(f"❌ 任务执行异常: {e}")
            self.log(f"详细错误: {traceback.format_exc()}")
        finally:
            try:
                # 使用信号在主线程中恢复GUI状态
                if hasattr(self, 'enable_start_button'):
                    self.enable_start_button.emit(True)
                
                if hasattr(self.gui, 'ProgressBar'):
                    self.update_progress.emit(0)
            except Exception as e:
                import traceback
                self.log(f"❌ 恢复GUI状态时出错: {e}")
                self.log(f"详细错误: {traceback.format_exc()}")
    
    def _restore_gui_state(self):
        """恢复GUI状态的方法"""
        try:
            # 使用Qt信号安全地更新GUI组件
            # 直接发送信号，这是最安全的方式
            if hasattr(self, 'enable_start_button'):
                # 简单地发出信号，让Qt处理线程安全
                self.enable_start_button.emit(True)

            if hasattr(self.gui, 'ProgressBar'):
                # 重置进度条
                self.update_progress.emit(0)

            # 发送最终日志
            self.log("--- GUI状态已恢复 ---")
        except Exception as e:
            import traceback
            # 使用日志回调而不是直接打印
            self.log(f"❌ 恢复GUI状态时出错: {e}")
            self.log(f"详细错误: {traceback.format_exc()}")

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


class ToolController:
    """
    工具控制器类，负责处理各种工具任务，如合并任务和清理任务
    """
    
    def start_generic_task(self, task_func, log_callback=None):
        """
        启动通用任务
        
        Args:
            task_func: 要执行的任务函数
            log_callback: 日志回调函数（可选）
        """
        import os
        import threading
        from PySide6.QtWidgets import QMessageBox
        
        # 获取目标目录
        target = self.path_var.strip()
        if not target or not os.path.exists(target):
            QMessageBox.critical(self.root, "错误", "请选择有效目录")
            return
        
        # 设置日志回调
        final_log = log_callback if log_callback else self.log
        
        # 更新进度条
        if hasattr(self.gui, 'ProgressBar'):
            self.gui.ProgressBar.setValue(0)

        # 启动任务线程
        threading.Thread(
            target=task_func,
            args=(target, final_log, self.update_progress, self.root),
            kwargs={'output_dir': self.get_output_dir()},
            daemon=True
        ).start()
    
    def execute_merge_tasks(self):
        """
        执行合并任务
        """
        execute_merge_tasks(
            path_var=self.path_var,
            output_path_var=self.output_path_var,
            log_callback=self.log,
            update_progress=self.update_progress,
            root=self.root,
            gui=self.gui
        )


class UnifiedApp(BaseController, UIController, TaskController, ToolController):
    """
    统一控制器类，整合了所有子控制器的功能
    负责协调GUI、任务执行与配置管理
    """
    
    def __init__(self, root, startup_path=None, startup_out=None):
        """
        初始化统一控制器
        
        Args:
            root: 根窗口对象
            startup_path: 启动时的源目录路径
            startup_out: 启动时的输出目录路径
        """
        # 初始化基础控制器，设置变量、配置和主题
        BaseController.__init__(self, root, startup_path, startup_out)

        # 实例化GUI
        from gui.qt_gui import ToolboxGUI
        self.gui = ToolboxGUI(self.root, self)

        # 应用保存的主题设置（使用增强的主题切换函数）
        from gui.theme import apply_theme_enhanced
        apply_theme_enhanced(self.theme_mode)

        # 设置主题属性，使控件能够根据主题应用不同的样式
        theme_value = self.theme_mode.lower()
        self.gui.setProperty("theme", theme_value)  # 为主窗口设置主题属性，使 QToolTip 样式生效
        self.gui.Function.setProperty("theme", theme_value)
        self.gui.menuBar.setProperty("theme", theme_value)

        # 额外的初始化处理：确保所有部件都正确应用主题
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()

        # 强制刷新所有部件的样式表
        self.gui.Function.setStyleSheet(self.gui.Function.styleSheet())
        self.gui.menuBar.setStyleSheet(self.gui.menuBar.styleSheet())
        self.gui.Log.setStyleSheet(self.gui.Log.styleSheet())

        # 刷新所有标签部件（移除硬编码颜色）
        label_widgets = [
            self.gui.VolumeLabel,
            self.gui.AssPatternLabel,
            self.gui.WhisperModelLabel,
            self.gui.WhisperLanguageLabel
        ]

        for label in label_widgets:
            if label:
                current_style = label.styleSheet()
                if 'color: rgb(0, 0, 0);' in current_style:
                    label.setStyleSheet(current_style.replace('color: rgb(0, 0, 0);', 'color: palette(text);'))

        # 最后一次处理事件，确保所有更新都完成
        app.processEvents()

        # 重置进度条为 0，确保程序启动时进度条显示为空
        if hasattr(self.gui, 'ProgressBar'):
            self.gui.ProgressBar.setValue(0)

        # # 连接覆盖对话框信号
        # self.show_overwrite_dialog.connect(self._on_show_overwrite_dialog)

        # 连接覆盖对话框信号
        self.show_overwrite_dialog.connect(self._on_show_overwrite_dialog)

        # 设置窗口关闭事件处理
        self.gui.closeEvent = self.on_close

    def on_close(self, event):
        """窗口关闭事件处理，退出前保存所有当前设置"""
        try:
            self.save_settings()
        finally:
            event.accept()

    def _on_show_overwrite_dialog(self, existing_count):
        """显示覆盖对话框的槽函数
        
        Args:
            existing_count: 已存在字幕的文件数量
        """
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self.gui,
            "已存在字幕",
            f"检测到 {existing_count} 个文件已生成字幕。\n\n是否覆盖已存在的字幕文件？\n\n选择「是」覆盖所有，「否」跳过已存在的。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        self.skip_existing = (reply == QMessageBox.StandardButton.No)

    def save_theme_setting(self, new_theme):
        """更新主题模式（不自动保存配置）
        
        Args:
            new_theme: 新的主题模式（"Light"或"Dark"）
        """
        self.theme_mode = new_theme
        # 不再自动保存配置，主题设置将在关闭程序或手动点击"保存配置"菜单时保存

    def refresh_config_file(self):
        """刷新配置文件并更新GUI"""
        self.load_settings()
        self.refresh_parsed_styles()
        # 更新GUI界面
        if hasattr(self.gui, '_update_gui_from_settings'):
            self.gui._update_gui_from_settings()
        if hasattr(self.gui, 'log'):
            self.gui.log("配置已刷新")
    
    def save_current_directory_to_config(self):
        """更新配置：按照优先级逻辑更新GUI和配置文件"""
        # 保存当前GUI上的设定
        current_path = self.gui.ReadPathInput.text().strip()
        current_output = self.gui.SavePathInput.text().strip()
        current_ass_pattern = self.gui.AssPatternSelect.currentText()
        current_volume = self.gui.VolumePatternSelect.currentText()
        current_output2pdf = self.gui.Output2PDF.isChecked()
        current_output2word = self.gui.Output2Word.isChecked()
        current_output2txt = self.gui.Output2Txt.isChecked()
        current_merge_pdf = self.gui.MergePDF.isChecked()
        current_merge_word = self.gui.MergeWord.isChecked()
        current_merge_txt = self.gui.MergeTxt.isChecked()

        # 重新加载配置文件
        self.load_settings()
        self.refresh_parsed_styles()

        # 逻辑1和3：如果GUI上没有设定，则读取INI里的设定，如果都没有，那么就空着
        if not current_path:
            current_path = self.path_var
        if not current_output:
            current_output = self.output_path_var
        if not current_ass_pattern:
            # 将英文格式转换为中文格式
            preset_mapping = {
                "kor_chn": "韩上中下",
                "jpn_chn": "日上中下",
                "eng_chn": "英上中下"
            }
            current_ass_pattern = preset_mapping.get(self.ass_pattern, "韩上中下")
        if not current_volume:
            current_volume = self.volume_pattern



        # 逻辑2和4：如果GUI上有设定，则保存到INI（无论INI里是否有设定）
        # 根据当前任务模式保存到对应的路径变量
        if self.task_mode == "Script":
            self.script_dir = current_path
            self.script_output_dir = current_output
        elif self.task_mode == "Merge":
            self.merge_dir = current_path
            self.merge_output_dir = current_output
        elif self.task_mode == "Srt2Ass":
            self.srt2ass_dir = current_path
            self.srt2ass_output_dir = current_output
        elif self.task_mode == "AutoSub":
            self.autosub_dir = current_path
            self.autosub_output_dir = current_output

        # 同时更新当前路径变量
        self.path_var = current_path
        self.output_path_var = current_output

        # 保存预设和分卷模式
        if current_ass_pattern:
            # 将中文选项转换为英文格式
            preset_mapping = {
                "韩上中下": "kor_chn",
                "日上中下": "jpn_chn",
                "英上中下": "eng_chn"
            }
            self.ass_pattern = preset_mapping.get(current_ass_pattern, "kor_chn")
        if current_volume:
            self.volume_pattern = current_volume

        # 不再自动保存配置，只更新内存中的变量
        # 配置将在关闭程序或手动点击"保存配置"菜单时保存

        # 更新GUI界面
        if hasattr(self.gui, '_update_gui_from_settings'):
            self.gui._update_gui_from_settings()

        if hasattr(self.gui, 'log'):
            self.gui.log("配置已更新")
    
    def open_config_file(self):
        """快速打开外部配置文件 SubtitleToolbox.ini"""
        # 获取配置文件路径
        config_file = self.config.config_file
        
        # 如果配置文件不存在，先创建默认配置文件
        if not os.path.exists(config_file): 
            self.save_settings()
        
        try:
            # 使用系统默认关联程序打开配置文件
            os.startfile(config_file)
        except Exception as e:
            if hasattr(self, 'gui'):
                self.gui.log(f"❌ 无法打开配置文件: {e}")