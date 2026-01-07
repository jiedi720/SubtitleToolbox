import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
import os

from .ui_SubtitleToolbox import Ui_SubtitleToolbox

# 从log_gui.py导入LogComponent类
from .log_gui import LogComponent


class ToolboxGUI(QMainWindow, Ui_SubtitleToolbox):
    """
    主窗口GUI类，继承自QMainWindow和Ui_SubtitleToolbox
    负责处理应用程序的GUI界面和用户交互
    """
    
    def __init__(self, root, controller):
        """
        初始化主窗口
        
        Args:
            root: 根窗口对象（PySide6中不需要，保留为兼容）
            controller: 应用程序控制器
        """
        super().__init__()
        self.root = root
        self.app = controller
        
        # 设置UI
        self.setupUi(self)
        
        # 设置窗口图标
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")
        self.setWindowIcon(QIcon(os.path.join(resources_dir, "SubtitleToolbox.ico")))
        
        # 配置日志区域
        self.Log.setReadOnly(True)
        self.Log.setFont(QFont("Microsoft YaHei", 10))
        
        # 从控制器更新GUI字段
        self._update_gui_from_settings()
        
        # 连接信号和槽
        self.connect_signals()
        
        # 标记初始化完成
        self._initialized = True
    
    @property
    def fonts(self):
        """
        获取应用程序字体设置
        
        Returns:
            dict: 包含不同类型字体的字典
        """
        return {
            "normal": QFont("Microsoft YaHei", 12),
            "bold": QFont("Microsoft YaHei", 12, QFont.Weight.Bold),
            "small": QFont("Microsoft YaHei", 11)
        }
    
    def connect_signals(self):
        """连接所有信号和槽"""
        # 路径设置按钮
        self.ReadPathSelect.clicked.connect(self._browse_source_dir)
        self.SavePathSelect.clicked.connect(self._browse_output_dir)
        self.ReadPathOpen.clicked.connect(self._open_source_dir)
        self.SavePathOpen.clicked.connect(self._open_output_dir)
        
        # 路径设置保存按钮
        self.ReadPathSet.clicked.connect(self.app.save_current_directory_to_config)
        self.SavePathSet.clicked.connect(self.app.save_current_directory_to_config)
        
        # 路径输入框信号
        self.ReadPathInput.textChanged.connect(self._on_source_path_changed)
        self.SavePathInput.textChanged.connect(self._on_output_path_changed)
        
        # 主功能按钮
        self.Start.clicked.connect(self.app.start_thread)
        self.ClearLogs.clicked.connect(self._clear_log)
        self.DeleteFiles.clicked.connect(self._delete_files)
        
        # Srt2Ass选项卡中的按钮
        self.RefreshSettings.clicked.connect(self.app.save_current_directory_to_config)
        self.OpenSettings.clicked.connect(self.app.open_config_file)
        
        # Srt2Ass选项卡中的下拉框
        self.AssPatternSelect.currentIndexChanged.connect(self._on_ass_pattern_changed)
        
        # Script选项卡中的输出选项
        self.Output2PDF.toggled.connect(self._on_pdf_state_changed)
        self.Output2Word.toggled.connect(self._on_word_state_changed)
        self.Output2Txt.toggled.connect(self._on_txt_state_changed)
        
        # Merge选项卡中的输出选项
        self.MergePDF.toggled.connect(self._on_merge_pdf_state_changed)
        self.MergeWord.toggled.connect(self._on_merge_word_state_changed)
        self.MergeTxt.toggled.connect(self._on_merge_txt_state_changed)
        
        # 标签页切换信号
        self.Function.currentChanged.connect(self._on_tab_changed)
        
        # 分卷模式下拉选择框信号
        self.VolumePatternSelect.currentIndexChanged.connect(self._on_volume_mode_changed)
        
        # Merge标签页按钮连接 - 移除直接连接，改为通过Start按钮统一处理
        # self.MergePDF.clicked.connect(self.app.start_pdf_merge_thread)
        # self.MergeWord.clicked.connect(self.app.start_win32_thread)
        # self.MergeTxt.clicked.connect(self.app.start_txt_merge_thread)
        
        # 菜单连接
        self.actionLight.triggered.connect(lambda: self.theme_change("Light"))
        self.actionDark.triggered.connect(lambda: self.theme_change("Dark"))
        self.OpenSettings_2.triggered.connect(self.app.open_config_file)
        
        # AutoSub标签页中的按钮
        self.SelectWhisperModel.clicked.connect(self._select_whisper_model_dir)
        self.OpenWhisperModel.clicked.connect(self._open_whisper_model_dir)
        
        # Whisper模型选择下拉框信号
        self.WhisperModelSelect.currentIndexChanged.connect(self._on_whisper_model_changed)
        
        # 连接控制器信号到GUI槽函数（线程安全更新）
        if hasattr(self.app, 'update_log'):
            self.app.update_log.connect(self.log)
        if hasattr(self.app, 'update_progress'):
            self.app.update_progress.connect(self.ProgressBar.setValue)
        if hasattr(self.app, 'enable_start_button'):
            self.app.enable_start_button.connect(self.Start.setEnabled)
        self.SaveSettings_2.triggered.connect(self.app.save_settings)
    
    def closeEvent(self, event):
        """
        窗口关闭事件处理
        
        Args:
            event: 关闭事件
        """
        # 保存设置
        if hasattr(self.app, 'save_settings'):
            self.app.save_settings()
        # 接受关闭事件
        event.accept()
    
    def _browse_source_dir(self):
        """浏览并选择源文件目录"""
        from PySide6.QtWidgets import QFileDialog
        # 获取当前读取目录作为默认路径
        default_dir = self.app.path_var.strip() if hasattr(self.app, 'path_var') else ""
        dir_path = QFileDialog.getExistingDirectory(self, "选择源文件目录", default_dir)
        if dir_path:
            self.ReadPathInput.setText(dir_path)
    
    def _browse_output_dir(self):
        """浏览并选择输出目录"""
        from PySide6.QtWidgets import QFileDialog
        # 获取当前输出目录作为默认路径，如果没有则使用读取目录
        default_dir = self.app.output_path_var.strip() if hasattr(self.app, 'output_path_var') and self.app.output_path_var.strip() else ""
        if not default_dir and hasattr(self.app, 'path_var'):
            default_dir = self.app.path_var.strip()
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出位置", default_dir)
        if dir_path:
            self.SavePathInput.setText(dir_path)
    
    def _on_source_path_changed(self, text):
        """源路径输入框变化时同步到控制器"""
        self.app.path_var = text
    
    def _on_output_path_changed(self, text):
        """输出路径输入框变化时同步到控制器"""
        self.app.output_path_var = text
    
    def _on_pdf_state_changed(self, checked):
        """PDF输出选项变化时同步到控制器"""
        if hasattr(self.app, 'output2pdf'):
            self.app.output2pdf = checked
    
    def _on_word_state_changed(self, checked):
        """Word输出选项变化时同步到控制器"""
        if hasattr(self.app, 'output2word'):
            self.app.output2word = checked
    
    def _on_txt_state_changed(self, checked):
        """Txt输出选项变化时同步到控制器"""
        if hasattr(self.app, 'output2txt'):
            self.app.output2txt = checked
    
    def _on_merge_pdf_state_changed(self, checked):
        """Merge PDF选项变化时同步到控制器"""
        if hasattr(self.app, 'merge_pdf'):
            self.app.merge_pdf = checked
    
    def _on_merge_word_state_changed(self, checked):
        """Merge Word选项变化时同步到控制器"""
        if hasattr(self.app, 'merge_word'):
            self.app.merge_word = checked
    
    def _on_merge_txt_state_changed(self, checked):
        """Merge Txt选项变化时同步到控制器"""
        if hasattr(self.app, 'merge_txt'):
            self.app.merge_txt = checked
    
    def _open_source_dir(self):
        """打开源文件目录"""
        import os
        path = self.ReadPathInput.text()
        if path and os.path.exists(path):
            os.startfile(path)
    
    def _open_output_dir(self):
        """打开输出目录"""
        import os
        path = self.SavePathInput.text()
        if path and os.path.exists(path):
            os.startfile(path)
    
    def _delete_files(self):
        """删除生成的文件"""
        # 直接调用删除方法，保留trash.py中的确认提示
        self.app.delete_generated_files()
    
    def theme_change(self, mode):
        """
        切换主题
        
        Args:
            mode: 主题模式（"Light"或"Dark"）
        """
        from .theme import apply_theme
        apply_theme(mode)
        
        # 刷新 Log 控件，使其使用新的调色板
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        self.Log.setPalette(app.palette())
        
        # 保存主题设置
        if hasattr(self.app, 'save_theme_setting'):
            self.app.save_theme_setting(mode)
    
    def _clear_log(self):
        """清除日志"""
        self.Log.clear()
    
    def log(self, message, tag=None):
        """
        记录日志
        
        Args:
            message: 日志内容
            tag: 日志标签（可选），用于设置不同的颜色
        """
        from PySide6.QtGui import QColor, QTextCursor, QTextCharFormat, QPalette
        from PySide6.QtWidgets import QApplication
        
        # 获取当前应用程序调色板
        app = QApplication.instance()
        palette = app.palette()
        
        # 定义颜色常量，这些颜色会在两种主题下都清晰可见
        COLOR_WORD_BLUE = QColor(0, 110, 255)  # 蓝色
        COLOR_PDF_RED = QColor(220, 0, 0)       # 红色
        COLOR_ERROR = QColor(255, 0, 0)         # 错误红色
        COLOR_SUCCESS = QColor(0, 170, 0)       # 成功绿色
        
        # 根据主题调整颜色，确保在不同主题下都清晰可见
        # 检查窗口背景色的亮度，判断当前主题
        window_bg = palette.color(QPalette.ColorRole.Window)
        is_dark_mode = window_bg.lightness() < 128
        
        # 直接从调色板获取文本颜色，确保与当前主题一致
        text_color = palette.color(QPalette.ColorRole.Text)
        
        if is_dark_mode:
            # 在深色模式下调整其他颜色，使其更清晰
            COLOR_WORD_BLUE = QColor(100, 149, 237)  # 矢车菊蓝
            COLOR_PDF_RED = QColor(255, 100, 100)    # 浅红色
            COLOR_SUCCESS = QColor(100, 200, 100)    # 浅绿色
        
        # 判断是否需要特殊颜色
        text_color = None
        
        # 检查Word相关日志
        if ("Word生成" in message or 
            "已生成: word\"" in message or
            "📄 已生成: word\\" in message or
            "合并中:" in message and ".docx" in message):
            text_color = COLOR_WORD_BLUE
        # 检查PDF相关日志
        elif ("PDF生成" in message or 
              "已生成: pdf\"" in message or
              "📄 已生成: pdf\\" in message or
              "合并中:" in message and ".pdf" in message):
            text_color = COLOR_PDF_RED
        # 检查错误日志
        elif "❌" in message:
            text_color = COLOR_ERROR
        # 检查成功日志
        elif "✅" in message:
            text_color = COLOR_SUCCESS
        # 其他日志不设置颜色，使用默认的调色板颜色（会自动跟随主题）
        
        # 使用QTextCursor插入文本
        cursor = self.Log.textCursor()
        
        if text_color:
            # 只有特殊日志才设置颜色
            format = QTextCharFormat()
            format.setForeground(text_color)
            cursor.insertText(message + "\n", format)
        else:
            # 默认日志不设置颜色，使用调色板的默认文本颜色
            cursor.insertText(message + "\n")
        
        self.Log.ensureCursorVisible()
    
    def _on_tab_changed(self, index):
        """
        标签页切换时的处理

        Args:
            index: 标签页索引
        """
        # 获取当前标签页文本
        tab_text = self.Function.tabText(index)
        # 记录到日志区域 - 已取消模式切换提示
        # 更新任务模式
        if hasattr(self.app, 'task_mode'):
            # 先保存当前模式的路径
            self._save_current_mode_paths()

            # 根据标签页文本设置对应的任务模式
            if tab_text == "Srt2Ass":
                self.app.task_mode = "Srt2Ass"
            elif tab_text == "Script":
                self.app.task_mode = "Script"
            elif tab_text == "Merge":
                self.app.task_mode = "Merge"
            elif tab_text == "AutoSub":
                self.app.task_mode = "AutoSub"

            # 更新当前路径为新模式的路径
            self._load_current_mode_paths()

            # 不再在切换标签时保存配置，只在关闭程序时保存

    def _save_current_mode_paths(self):
        """保存当前任务模式的路径到对应的变量"""
        if not hasattr(self.app, 'task_mode'):
            return

        # 从GUI获取当前路径
        current_path = self.ReadPathInput.text().strip()
        current_output = self.SavePathInput.text().strip()

        # 根据当前任务模式保存到对应的变量
        if self.app.task_mode == "Script":
            self.app.script_dir = current_path
            self.app.script_output_dir = current_output
        elif self.app.task_mode == "Merge":
            self.app.merge_dir = current_path
            self.app.merge_output_dir = current_output
        elif self.app.task_mode == "Srt2Ass":
            self.app.srt2ass_dir = current_path
            self.app.srt2ass_output_dir = current_output
        elif self.app.task_mode == "AutoSub":
            self.app.autosub_dir = current_path
            self.app.autosub_output_dir = current_output

    def _load_current_mode_paths(self):
        """加载当前任务模式的路径到GUI"""
        if not hasattr(self.app, 'task_mode'):
            return

        # 根据当前任务模式获取对应的路径
        if self.app.task_mode == "Script":
            path = self.app.script_dir if hasattr(self.app, 'script_dir') else ""
            output = self.app.script_output_dir if hasattr(self.app, 'script_output_dir') else ""
        elif self.app.task_mode == "Merge":
            path = self.app.merge_dir if hasattr(self.app, 'merge_dir') else ""
            output = self.app.merge_output_dir if hasattr(self.app, 'merge_output_dir') else ""
        elif self.app.task_mode == "Srt2Ass":
            path = self.app.srt2ass_dir if hasattr(self.app, 'srt2ass_dir') else ""
            output = self.app.srt2ass_output_dir if hasattr(self.app, 'srt2ass_output_dir') else ""
        elif self.app.task_mode == "AutoSub":
            path = self.app.autosub_dir if hasattr(self.app, 'autosub_dir') else ""
            output = self.app.autosub_output_dir if hasattr(self.app, 'autosub_output_dir') else ""
        else:
            path = ""
            output = ""

        # 更新GUI显示
        self.ReadPathInput.setText(path)
        self.SavePathInput.setText(output)

        # 更新app的当前路径变量
        self.app.path_var = path
        self.app.output_path_var = output
    
    def _on_volume_mode_changed(self, value):
        """
        分卷模式变化时的处理
        
        Args:
            value: 分卷模式索引
        """
        # 映射索引到分卷模式名称
        mode_map = {
            0: "整季",
            1: "智能",
            2: "单集"
        }
        mode = mode_map.get(value, f"未知模式({value})")
        
        # 设置控制器的volume_pattern
        if hasattr(self.app, 'volume_pattern'):
            self.app.volume_pattern = mode
            # 已取消分卷模式切换提示
    
    def _on_ass_pattern_changed(self, value):
        """
        ASS 字体方案选择变化时的处理
        
        Args:
            value: 方案索引
        """
        # 获取当前选中的方案名称（中文）
        pattern_name_cn = self.AssPatternSelect.currentText()

        # 将中文选项转换为英文格式用于内部使用
        preset_mapping = {
            "韩上中下": "kor_chn",
            "日上中下": "jpn_chn",
            "英上中下": "eng_chn"
        }
        pattern_name_en = preset_mapping.get(pattern_name_cn, "kor_chn")

        # 更新控制器的当前预设（使用英文格式）
        if hasattr(self.app, 'ass_pattern'):
            self.app.ass_pattern = pattern_name_en
            # 同时更新config中的ass_pattern（使用英文格式）
            if hasattr(self.app, 'config'):
                self.app.config.ass_pattern = pattern_name_en
            # 刷新解析后的样式
            self.app.refresh_parsed_styles()

        # 保存设置
        if hasattr(self.app, 'save_settings'):
            self.app.save_settings()

        # 记录日志
        self.log(f"已选择 ASS 字体方案: {pattern_name_cn}")
    
    def _open_whisper_model_dir(self):
        """打开 Whisper 模型目录"""
        import os
        
        # 优先使用 SelectWhisperModel 选择的目录
        if hasattr(self.app, 'whisper_model_path') and self.app.whisper_model_path:
            model_dir = self.app.whisper_model_path
        else:
            # 默认为源目录下的 models 文件夹
            model_dir = os.path.join(self.app.path_var.strip(), "models")
        
        if not os.path.exists(model_dir):
            # 如果目录不存在，尝试打开源目录
            model_dir = self.app.path_var.strip()
        
        if model_dir and os.path.exists(model_dir):
            os.startfile(model_dir)
    
    def _select_whisper_model_dir(self):
        """选择 Whisper 模型目录"""
        from PySide6.QtWidgets import QFileDialog
        
        # 获取当前设置的目录作为默认路径
        default_dir = ""
        if hasattr(self.app, 'whisper_model_path') and self.app.whisper_model_path:
            default_dir = self.app.whisper_model_path
        elif hasattr(self.app, 'path_var') and self.app.path_var:
            # 如果没有设置过，使用源目录下的 models 文件夹
            default_dir = os.path.join(self.app.path_var.strip(), "models")
        
        # 弹出目录选择对话框
        dir_path = QFileDialog.getExistingDirectory(self, "选择 Whisper 模型目录", default_dir)
        if dir_path:
            self.app.whisper_model_path = dir_path
            self.app.save_settings()
            self.log(f"已选择 Whisper 模型目录: {dir_path}")
    
    def _on_whisper_model_changed(self, value):
        """
        Whisper 模型选择变化时的处理
        
        Args:
            value: 模型索引
        """
        # 获取当前选中的模型名称
        model_name = self.WhisperModelSelect.currentText()
        
        # 更新控制器的模型设置
        if hasattr(self.app, 'whisper_model'):
            self.app.whisper_model = model_name
        
        # 保存模型选择到配置
        if hasattr(self.app, 'save_settings'):
            self.app.save_settings()
        
        # 记录日志
        if model_name != "默认":
            self.log(f"已选择 Whisper 模型: {model_name}")
    

    
    def _update_gui_from_settings(self):
        """从控制器更新GUI字段"""
        # 临时阻止信号发射，避免触发不必要的信号
        self.ReadPathInput.blockSignals(True)
        self.SavePathInput.blockSignals(True)
        self.Output2PDF.blockSignals(True)
        self.Output2Word.blockSignals(True)
        self.Output2Txt.blockSignals(True)
        self.MergePDF.blockSignals(True)
        self.MergeWord.blockSignals(True)
        self.MergeTxt.blockSignals(True)
        
        # 更新路径输入框
        self.ReadPathInput.setText(self.app.path_var)
        self.SavePathInput.setText(self.app.output_path_var)
        
        # 更新输出选项复选框
        if hasattr(self.app, 'output2pdf'):
            self.Output2PDF.setChecked(self.app.output2pdf)
        if hasattr(self.app, 'output2word'):
            self.Output2Word.setChecked(self.app.output2word)
        if hasattr(self.app, 'output2txt'):
            self.Output2Txt.setChecked(self.app.output2txt)
        
        # 更新Merge选项卡复选框
        if hasattr(self.app, 'merge_pdf'):
            self.MergePDF.setChecked(self.app.merge_pdf)
        if hasattr(self.app, 'merge_word'):
            self.MergeWord.setChecked(self.app.merge_word)
        if hasattr(self.app, 'merge_txt'):
            self.MergeTxt.setChecked(self.app.merge_txt)
        
        # 根据task_mode设置当前标签页
        if hasattr(self.app, 'task_mode'):
            # 阻止信号发射，避免触发不必要的保存
            self.Function.blockSignals(True)
            # 映射task_mode到标签页索引
            mode_to_index = {
                "Script": 0,
                "Merge": 1,
                "Srt2Ass": 2,
                "AutoSub": 3
            }
            index = mode_to_index.get(self.app.task_mode, 2)  # 默认显示Srt2Ass标签页
            self.Function.setCurrentIndex(index)
            # 恢复信号发射
            self.Function.blockSignals(False)
        
        # 更新分卷模式选择
        if hasattr(self.app, 'volume_pattern'):
            # 阻止信号发射
            self.VolumePatternSelect.blockSignals(True)
            # 映射volume_pattern到下拉菜单索引
            pattern_to_index = {
                "整季": 0,
                "智能": 1,
                "单集": 2
            }
            index = pattern_to_index.get(self.app.volume_pattern, 0)  # 默认整季模式
            self.VolumePatternSelect.setCurrentIndex(index)
            # 恢复信号发射
            self.VolumePatternSelect.blockSignals(False)
        
        # 更新Whisper模型选择
        if hasattr(self.app, 'whisper_model'):
            # 阻止信号发射
            self.WhisperModelSelect.blockSignals(True)
            # 查找模型在下拉框中的索引
            model_index = self.WhisperModelSelect.findText(self.app.whisper_model)
            if model_index >= 0:
                self.WhisperModelSelect.setCurrentIndex(model_index)
            # 恢复信号发射
            self.WhisperModelSelect.blockSignals(False)
        
        # 更新ASS字体方案选择
        if hasattr(self.app, 'ass_pattern'):
            # 阻止信号发射
            self.AssPatternSelect.blockSignals(True)
            
            # 将英文格式转换为中文格式用于UI显示
            preset_mapping = {
                "kor_chn": "韩上中下",
                "jpn_chn": "日上中下",
                "eng_chn": "英上中下"
            }
            pattern_name_cn = preset_mapping.get(self.app.ass_pattern, "韩上中下")
            
            # 根据中文方案名称设置选中项
            # 选项为：0=韩上中下, 1=日上中下, 2=英上中下
            preset_to_index = {
                "韩上中下": 0,
                "日上中下": 1,
                "英上中下": 2
            }
            index = preset_to_index.get(pattern_name_cn, 0)
            self.AssPatternSelect.setCurrentIndex(index)
            
            # 恢复信号发射
            self.AssPatternSelect.blockSignals(False)
        
        # 恢复信号发射
        self.ReadPathInput.blockSignals(False)
        self.SavePathInput.blockSignals(False)
        self.Output2PDF.blockSignals(False)
        self.Output2Word.blockSignals(False)
        self.Output2Txt.blockSignals(False)
        self.MergePDF.blockSignals(False)
        self.MergeWord.blockSignals(False)
        self.MergeTxt.blockSignals(False)
    
    def set_progress(self, value):
        """
        设置进度条值
        
        Args:
            value: 进度值（0-1）
        """
        self.ProgressBar.setValue(int(value * 100))


# 测试主窗口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolboxGUI(None, None)
    window.show()
    sys.exit(app.exec())
