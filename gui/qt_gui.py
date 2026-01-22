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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "icons")
        self.setWindowIcon(QIcon(os.path.join(icons_dir, "SubtitleToolbox.ico")))
        
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
        
        # 路径设置保存按钮（不再自动保存配置，只更新内存中的变量）
        self.ReadPathSet.clicked.connect(self._update_path_from_input)
        self.SavePathSet.clicked.connect(self._update_path_from_input)
        
        # 路径输入框信号 - 不再在文本改变时立即更新控制器
        # self.ReadPathInput.textChanged.connect(self._on_source_path_changed)
        # self.SavePathInput.textChanged.connect(self._on_output_path_changed)
        
        # 设置所有图标
        self._set_all_icons()
    
    def _set_all_icons(self):
        """设置所有按钮图标"""
        # 获取图标目录
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "icons")
        
        # 图标映射（根据 ui_SubtitleToolbox.py 中的图标设定）
        icon_map = {
            'open-folder2.png': [self.ReadPathOpen, self.SavePathOpen],
            'search2.png': [self.ReadPathSelect, self.SavePathSelect, self.SelectWhisperModel],
            'refresh.png': [self.ReadPathSet, self.SavePathSet],
            'PDF.png': [self.Output2PDF, self.MergePDF],
            'Word.ico': [self.Output2Word, self.MergeWord],
            'txt.png': [self.Output2Txt, self.MergeTxt],
            'Markdown.png': [self.Output2Md, self.MergeMd],
            'shuttle.png': [self.Start],
            'stop.png': [self.Stop],
            'broom.png': [self.ClearLogs],
            'delete.png': [self.DeleteFiles],
        }
        
        # 设置图标
        for icon_file, widgets in icon_map.items():
            icon_path = os.path.join(icons_dir, icon_file)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                for widget in widgets:
                    widget.setIcon(icon)
        
        # 主功能按钮
        self.Start.clicked.connect(self.app.start_thread)
        self.Stop.clicked.connect(self.app.stop_task)
        self.ClearLogs.clicked.connect(self._clear_log)
        self.DeleteFiles.clicked.connect(self._delete_files)
        
        # Srt2Ass选项卡中的下拉框
        self.AssPatternSelect.currentIndexChanged.connect(self._on_ass_pattern_changed)
        
        # Script选项卡中的输出选项
        self.Output2PDF.toggled.connect(self._on_pdf_state_changed)
        self.Output2Word.toggled.connect(self._on_word_state_changed)
        self.Output2Txt.toggled.connect(self._on_txt_state_changed)
        self.Output2Md.toggled.connect(self._on_md_state_changed)
        
        # Merge选项卡中的输出选项
        self.MergePDF.toggled.connect(self._on_merge_pdf_state_changed)
        self.MergeWord.toggled.connect(self._on_merge_word_state_changed)
        self.MergeTxt.toggled.connect(self._on_merge_txt_state_changed)
        self.MergeMd.toggled.connect(self._on_merge_md_state_changed)
        
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
        self.actionOpenSettings.triggered.connect(self.app.open_config_file)
        self.actionReadSettings.triggered.connect(self.app.refresh_config_file)
        
        # AutoSub标签页中的按钮
        self.SelectWhisperModel.clicked.connect(self._select_whisper_model_dir)
        
        # Whisper模型选择下拉框信号
        self.WhisperModelSelect.currentIndexChanged.connect(self._on_whisper_model_changed)

        # Whisper语言选择下拉框信号
        self.WhisperLanguageSelect.currentIndexChanged.connect(self._on_whisper_language_changed)
        
        # Whisper引擎选择下拉框信号
        self.WhisperEngineSelect.currentIndexChanged.connect(self._on_whisper_engine_changed)
        
        # VTT to SRT 拖放区域设置
        from function.vtt2srt import setup_vtt2srt_drop_area
        setup_vtt2srt_drop_area(self.Vtt2SrtDrop, self.log)

        # 连接控制器信号到GUI槽函数（线程安全更新）
        if hasattr(self.app, 'update_log'):
            self.app.update_log.connect(self.log)
        if hasattr(self.app, 'update_progress'):
            self.app.update_progress.connect(self.ProgressBar.setValue)
        if hasattr(self.app, 'enable_start_button'):
            self.app.enable_start_button.connect(self.Start.setEnabled)
        self.actionSaveSettings.triggered.connect(self.app.save_settings)
    
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
        import os
        from PySide6.QtWidgets import QFileDialog
        # 获取当前读取目录作为默认路径
        default_dir = self.app.path_var.strip() if hasattr(self.app, 'path_var') else ""
        dir_path = QFileDialog.getExistingDirectory(self, "选择源文件目录", default_dir)
        if dir_path:
            # 标准化路径分隔符
            normalized_dir_path = os.path.normpath(dir_path)
            self.ReadPathInput.setText(normalized_dir_path)
            # 自动更新控制器中的路径变量，无需手动点击"更新目录"
            self.app.path_var = normalized_dir_path

            # 根据当前任务模式更新对应的路径变量
            if hasattr(self.app, 'task_mode'):
                if self.app.task_mode == "Script":
                    self.app.script_dir = normalized_dir_path
                elif self.app.task_mode == "Merge":
                    self.app.merge_dir = normalized_dir_path
                elif self.app.task_mode == "Srt2Ass":
                    self.app.srt2ass_dir = normalized_dir_path
                elif self.app.task_mode == "AutoSub":
                    self.app.autosub_dir = normalized_dir_path

            # 添加日志提示
            self.log(f"📁 源目录已选择: {normalized_dir_path}")
    
    def _browse_output_dir(self):
        """浏览并选择输出目录"""
        import os
        from PySide6.QtWidgets import QFileDialog
        # 获取当前输出目录作为默认路径，如果没有则使用读取目录
        default_dir = self.app.output_path_var.strip() if hasattr(self.app, 'output_path_var') and self.app.output_path_var.strip() else ""
        if not default_dir and hasattr(self.app, 'path_var'):
            default_dir = self.app.path_var.strip()
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出位置", default_dir)
        if dir_path:
            # 标准化路径分隔符
            normalized_dir_path = os.path.normpath(dir_path)
            self.SavePathInput.setText(normalized_dir_path)
            # 自动更新控制器中的路径变量，无需手动点击"更新目录"
            self.app.output_path_var = normalized_dir_path

            # 根据当前任务模式更新对应的路径变量
            if hasattr(self.app, 'task_mode'):
                if self.app.task_mode == "Script":
                    self.app.script_output_dir = normalized_dir_path
                elif self.app.task_mode == "Merge":
                    self.app.merge_output_dir = normalized_dir_path
                elif self.app.task_mode == "Srt2Ass":
                    self.app.srt2ass_output_dir = normalized_dir_path
                elif self.app.task_mode == "AutoSub":
                    self.app.autosub_output_dir = normalized_dir_path

            # 添加日志提示
            self.log(f"📁 输出目录已选择: {normalized_dir_path}")
    
    def _on_source_path_changed(self, text):
        """源路径输入框变化时同步到控制器"""
        self.app.path_var = text
    
    def _on_output_path_changed(self, text):
        """输出路径输入框变化时同步到控制器"""
        self.app.output_path_var = text
    
    def _update_path_from_input(self):
        """从输入框更新路径到控制器（不再自动保存配置）"""
        # 从输入框获取路径并更新到控制器
        source_path = self.ReadPathInput.text().strip()
        output_path = self.SavePathInput.text().strip()

        # 更新控制器中的路径变量
        self.app.path_var = source_path
        self.app.output_path_var = output_path

        # 根据当前任务模式更新对应的路径变量
        if hasattr(self.app, 'task_mode'):
            if self.app.task_mode == "Script":
                self.app.script_dir = source_path
                self.app.script_output_dir = output_path
            elif self.app.task_mode == "Merge":
                self.app.merge_dir = source_path
                self.app.merge_output_dir = output_path
            elif self.app.task_mode == "Srt2Ass":
                self.app.srt2ass_dir = source_path
                self.app.srt2ass_output_dir = output_path
            elif self.app.task_mode == "AutoSub":
                self.app.autosub_dir = source_path
                self.app.autosub_output_dir = output_path

        # 添加日志提示
        self.log(f"📁 源目录已更新: {source_path if source_path else '(未设置)'}")
        if output_path:
            self.log(f"📁 输出目录已更新: {output_path}")
        else:
            self.log(f"📁 输出目录已更新: (使用源目录)")
    
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
    
    def _on_md_state_changed(self, checked):
        """Md输出选项变化时同步到控制器"""
        if hasattr(self.app, 'output2md'):
            self.app.output2md = checked
    
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
    
    def _on_merge_md_state_changed(self, checked):
        """Merge Md选项变化时同步到控制器"""
        if hasattr(self.app, 'merge_md'):
            self.app.merge_md = checked
    
    def _open_source_dir(self):
        """打开源文件目录"""
        import os
        # 优先使用输入框中的路径，如果输入框为空则使用控制器中的路径
        path = self.ReadPathInput.text().strip()
        if not path and hasattr(self.app, 'path_var'):
            path = self.app.path_var.strip()
        if path and os.path.exists(path):
            os.startfile(path)

    def _open_output_dir(self):
        """打开输出目录"""
        import os
        # 优先使用输入框中的路径，如果输入框为空则使用控制器中的路径
        path = self.SavePathInput.text().strip()
        if not path and hasattr(self.app, 'output_path_var'):
            path = self.app.output_path_var.strip()
        if path and os.path.exists(path):
            os.startfile(path)
    
    def _delete_files(self):
        """删除生成的文件"""
        # 直接调用删除方法，保留trash.py中的确认提示
        self.app.delete_generated_files()
    
    def theme_change(self, mode):
        """
        切换主题（增强版，确保只需点击一次就能完全切换）

        Args:
            mode: 主题模式（"Light"或"Dark"）
        """
        # 使用增强的主题切换函数
        from .theme import apply_theme_enhanced, refresh_all_widget_styles
        apply_theme_enhanced(mode)

        # 设置主题属性，使控件能够根据主题应用不同的样式
        theme_value = mode.lower()
        self.setProperty("theme", theme_value)  # 为主窗口设置主题属性，使 QToolTip 样式生效
        self.Function.setProperty("theme", theme_value)
        self.menuBar.setProperty("theme", theme_value)

        # 为所有子控件设置主题属性，确保主题选择器生效
        self._set_theme_property_recursive(self, theme_value)

        # 强制刷新所有部件的样式表
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()

        # 刷新所有标签部件（移除硬编码颜色）
        label_widgets = [
            self.VolumeLabel,
            self.AssPatternLabel,
            self.WhisperModelLabel,
            self.WhisperLanguageLabel,
            self.WhisperEngineLabel
        ]

        for label in label_widgets:
            if label:
                current_style = label.styleSheet()
                if 'color: rgb(0, 0, 0);' in current_style:
                    label.setStyleSheet(current_style.replace('color: rgb(0, 0, 0);', 'color: palette(text);'))

        # 刷新 Log 控件，重新设置样式表以保持圆角效果
        self.Log.setStyleSheet(self.Log.styleSheet())

        # 刷新菜单栏
        self.menuBar.setStyleSheet(self.menuBar.styleSheet())

        # 刷新 TabWidget
        self.Function.setStyleSheet(self.Function.styleSheet())

        # 通用刷新：确保所有带 [theme="light"] 和 [theme="dark"] 选择器的样式正确应用
        refresh_all_widget_styles()

        # 保存主题设置
        if hasattr(self.app, 'save_theme_setting'):
            self.app.save_theme_setting(mode)

    def _set_theme_property_recursive(self, widget, theme_value):
        """
        递归设置控件及其所有子控件的主题属性
        """
        from PySide6.QtWidgets import QWidget

        # 为当前控件设置主题属性
        widget.setProperty("theme", theme_value)

        # 如果控件有子控件，递归设置它们的主题属性
        for child in widget.findChildren(QWidget):
            child.setProperty("theme", theme_value)
            # 递归处理子控件的子控件
            self._set_theme_property_recursive(child, theme_value)

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
        # 同时输出到终端
        print(message)
        
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
        cursor.movePosition(QTextCursor.End)
        
        if text_color:
            # 只有特殊日志才设置颜色
            format = QTextCharFormat()
            format.setForeground(text_color)
            cursor.insertText(message + "\n", format)
        else:
            # 默认日志不设置颜色，使用调色板的默认文本颜色
            default_format = QTextCharFormat()
            cursor.insertText(message + "\n", default_format)
        
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
            "英上中下": "eng_chn",
            "韩上日下": "kor_jpn"
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
        import os
        from PySide6.QtWidgets import QFileDialog

        # 获取当前设置的目录作为默认路径
        # 优先使用控制器中的模型路径（已从配置文件加载）
        default_dir = ""
        if hasattr(self.app, 'whisper_model_path') and self.app.whisper_model_path:
            # 检查路径是否存在，如果不存在则使用其父目录
            model_path = self.app.whisper_model_path
            if os.path.exists(model_path):
                default_dir = model_path
            else:
                # 如果路径不存在，尝试使用其父目录
                parent_dir = os.path.dirname(model_path)
                if os.path.exists(parent_dir):
                    default_dir = parent_dir
                else:
                    # 如果父目录也不存在，尝试使用用户 AppData 目录作为更通用的默认位置
                    # 如果这些都不存在，最后使用源目录下的 models 文件夹
                    appdata_path = os.path.expanduser("~/AppData/Roaming")
                    if os.path.exists(appdata_path):
                        default_dir = appdata_path
                    elif hasattr(self.app, 'path_var') and self.app.path_var:
                        default_dir = os.path.join(self.app.path_var.strip(), "models")
                    else:
                        # 如果都没有，使用当前工作目录
                        default_dir = os.getcwd()
        elif hasattr(self.app, 'path_var') and self.app.path_var:
            # 如果没有设置过，使用源目录下的 models 文件夹
            default_dir = os.path.join(self.app.path_var.strip(), "models")
        else:
            # 如果都没有，使用当前工作目录
            default_dir = os.getcwd()

        # 弹出目录选择对话框
        dir_path = QFileDialog.getExistingDirectory(self, "选择 Whisper 模型目录", default_dir)
        if dir_path:
            # 标准化路径分隔符
            normalized_dir_path = os.path.normpath(dir_path)

            # 检查是否是 Hugging Face 缓存目录结构（包含 blobs, refs, snapshots）
            dir_items = []
            try:
                dir_items = os.listdir(normalized_dir_path)
            except Exception as e:
                self.log(f"❌ 无法读取目录: {e}")
                return

            hf_cache_dirs = ['blobs', 'refs', 'snapshots']
            is_hf_cache = all(item in dir_items for item in hf_cache_dirs)

            if is_hf_cache:
                # 这是 Hugging Face 缓存目录，自动定位到 snapshots 目录下的实际模型目录
                snapshots_dir = os.path.join(normalized_dir_path, "snapshots")
                if os.path.exists(snapshots_dir):
                    # 获取 snapshots 下的第一个子目录（通常是哈希值）
                    try:
                        snapshot_items = os.listdir(snapshots_dir)
                        snapshot_dirs = [item for item in snapshot_items
                                       if os.path.isdir(os.path.join(snapshots_dir, item))]
                        if snapshot_dirs:
                            # 使用第一个 snapshot 目录
                            actual_model_dir = os.path.join(snapshots_dir, snapshot_dirs[0])
                            normalized_dir_path = actual_model_dir
                            self.log(f"✓ 检测到 Hugging Face 缓存目录，自动定位到模型目录")
                            self.log(f"📂 实际模型目录: {normalized_dir_path}")

                            # 直接使用该目录，不再检测子目录
                            self.app.whisper_model_path = normalized_dir_path
                            # 从原始路径中提取模型名称
                            original_dir_name = os.path.basename(dir_path)
                            self.app.whisper_model = original_dir_name
                            self.log(f"✓ 已选择 Whisper 模型目录: {normalized_dir_path}")
                            self.log(f"🔍 模型名称: {original_dir_name}")
                            return
                        else:
                            self.log(f"❌ snapshots 目录为空: {snapshots_dir}")
                            return
                    except Exception as e:
                        self.log(f"❌ 读取 snapshots 目录时出错: {e}")
                        return
                else:
                    self.log(f"❌ 未找到 snapshots 目录: {snapshots_dir}")
                    return

            # 检测目录中的模型（根据文件夹名称）
            model_dirs = []
            for item in os.listdir(normalized_dir_path):
                item_path = os.path.join(normalized_dir_path, item)
                if os.path.isdir(item_path):
                    # 检查文件夹名称是否包含常见的模型关键词
                    item_lower = item.lower()
                    if any(keyword in item_lower for keyword in [
                        'large', 'medium', 'small', 'tiny', 'base',
                        'distil', 'turbo', 'v1', 'v2', 'v3', 'model',
                        'whisper', 'faster', 'large-v', 'medium-v', 'small-v'
                    ]):
                        model_dirs.append(item)

            # 根据检测结果输出日志
            if model_dirs:
                self.app.whisper_model_path = normalized_dir_path
                self.log(f"已选择 Whisper 模型目录: {normalized_dir_path}")

                if len(model_dirs) == 1:
                    # 如果只检测到一个模型，假设用户选择了具体模型目录
                    self.app.whisper_model = model_dirs[0]
                    self.log(f"🔍 检测到模型: {model_dirs[0]}")
                else:
                    # 如果检测到多个模型，说明用户选择了模型主目录
                    # 自动选择第一个模型
                    self.app.whisper_model = model_dirs[0]
                    self.log(f"🔍 检测到 {len(model_dirs)} 个模型: {', '.join(model_dirs)}")
                    self.log(f"✓ 自动选择第一个模型: {model_dirs[0]}")
            else:
                # 检查当前目录名称是否包含模型关键词（用户可能选择了具体模型目录）
                current_dir_name = os.path.basename(normalized_dir_path)
                current_dir_lower = current_dir_name.lower()

                if any(keyword in current_dir_lower for keyword in [
                    'large', 'medium', 'small', 'tiny', 'base',
                    'distil', 'turbo', 'v1', 'v2', 'v3', 'model',
                    'whisper', 'faster', 'large-v', 'medium-v', 'small-v'
                ]):
                    # 用户选择了具体模型目录
                    self.app.whisper_model_path = normalized_dir_path
                    # 自动设置 whisper_model 为目录名称
                    self.app.whisper_model = current_dir_name
                    self.log(f"已选择 Whisper 模型目录: {normalized_dir_path}")
                    self.log(f"🔍 检测到模型: {current_dir_name}")
                else:
                    # 没有检测到任何模型
                    self.log(f"❌ 选择的目录中未检测到任何模型: {normalized_dir_path}")
                    # 仍然保存路径，但给出警告
                    self.app.whisper_model_path = normalized_dir_path
    
    def _on_whisper_model_changed(self, value):
        """
        Whisper 模型选择变化时的处理

        Args:
            value: 模型索引
        """
        import os

        # 获取当前选中的模型名称
        model_name = self.WhisperModelSelect.currentText()

        # 更新控制器的模型设置
        if hasattr(self.app, 'whisper_model'):
            self.app.whisper_model = model_name

        # 验证模型是否存在
        if model_name.startswith("本地: "):
            local_model_name = model_name.replace("本地: ", "")
            model_dir = os.path.join(self.app.path_var.strip(), "models", local_model_name)

            # 检查模型目录是否存在
            if os.path.exists(model_dir):
                # 检查目录中是否有模型文件
                model_files = [f for f in os.listdir(model_dir)
                             if f.endswith(('.bin', '.safetensors', '.onnx', '.onnx_data')) or
                                f == 'config.json' or f == 'tokenizer.json' or
                                f.startswith('model.')]

                if model_files:
                    self.log(f"✓ 已切换 Whisper 模型: {model_name}")
                    self.log(f"🔍 检测到模型文件: {len(model_files)} 个")
                else:
                    self.log(f"❌ 选中的模型目录中未检测到模型文件: {model_dir}")
            else:
                self.log(f"❌ 选中的模型目录不存在: {model_dir}")
        else:
            # 对预定义模型也进行验证
            if model_name != "默认":
                # 检查用户设置的模型路径中是否存在对应模型
                if hasattr(self.app, 'whisper_model_path') and self.app.whisper_model_path:
                    model_path = self.app.whisper_model_path
                    # 检查模型路径下是否有与模型名称匹配的子目录
                    model_subdir = os.path.join(model_path, model_name)

                    if os.path.exists(model_subdir):
                        self.app.whisper_model = model_name  # 确保模型被设置
                        self.log(f"✓ 已切换 Whisper 模型: {model_name}")
                    else:
                        # 检查模型路径本身是否存在
                        if os.path.exists(model_path):
                            self.log(f"❌ 本地未找到模型: {model_subdir}")
                        else:
                            # 模型路径不存在
                            self.log(f"❌ 模型路径不存在: {model_path}")
                else:
                    # 没有设置模型路径
                    self.log(f"❌ 未设置模型路径")

                # 总是设置模型，但只在找到本地模型时显示成功信息
                self.app.whisper_model = model_name
            else:
                self.log(f"✓ 已切换为默认模型")

    def _on_whisper_language_changed(self, value):
        """
        Whisper 语言选择变化时的处理

        Args:
            value: 语言索引
        """
        # 获取当前选中的语言名称
        language_name = self.WhisperLanguageSelect.currentText()

        # 语言代码映射
        language_map = {
            "自动": "auto",
            "韩语": "ko",
            "日语": "ja",
            "英语": "en",
            "中文": "zh"
        }

        # 获取语言代码
        language_code = language_map.get(language_name, None)

        # 更新控制器的语言设置
        if hasattr(self.app, 'whisper_language'):
            self.app.whisper_language = language_code
        
        # 保存到配置
        if hasattr(self.app, 'config'):
            self.app.config.whisper_language = language_code
            self.app.config.save_settings()

        # 记录日志
        if language_name == "自动":
            self.log(f"✓ 已切换为自动语言检测 (auto)")
        else:
            self.log(f"✓ 已切换 Whisper 语言: {language_name} ({language_code})")
    
    def _on_whisper_engine_changed(self, value):
        """
        Whisper 引擎选择变化时的处理

        Args:
            value: 引擎索引
        """
        # 获取当前选中的引擎类型
        engine_type = self.WhisperEngineSelect.currentText()

        # 更新控制器的引擎设置
        if hasattr(self.app, 'whisper_engine'):
            self.app.whisper_engine = engine_type
        
        # 保存到配置
        if hasattr(self.app, 'config'):
            self.app.config.whisper_engine = engine_type
            self.app.config.save_settings()

        # 记录日志
        self.log(f"✓ 已切换 Whisper 引擎: {engine_type}")
    

    
    def _update_gui_from_settings(self):
        """从控制器更新GUI字段"""
        # 临时阻止信号发射，避免触发不必要的信号
        self.ReadPathInput.blockSignals(True)
        self.SavePathInput.blockSignals(True)
        self.Output2PDF.blockSignals(True)
        self.Output2Word.blockSignals(True)
        self.Output2Txt.blockSignals(True)
        self.Output2Md.blockSignals(True)
        self.MergePDF.blockSignals(True)
        self.MergeWord.blockSignals(True)
        self.MergeTxt.blockSignals(True)
        self.MergeMd.blockSignals(True)
        
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
        if hasattr(self.app, 'output2md'):
            self.Output2Md.setChecked(self.app.output2md)
        
        # 更新Merge选项卡复选框
        if hasattr(self.app, 'merge_pdf'):
            self.MergePDF.setChecked(self.app.merge_pdf)
        if hasattr(self.app, 'merge_word'):
            self.MergeWord.setChecked(self.app.merge_word)
        if hasattr(self.app, 'merge_txt'):
            self.MergeTxt.setChecked(self.app.merge_txt)
        if hasattr(self.app, 'merge_md'):
            self.MergeMd.setChecked(self.app.merge_md)
        
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

        # 更新Whisper语言选择
        if hasattr(self.app, 'whisper_language'):
            # 阻止信号发射
            self.WhisperLanguageSelect.blockSignals(True)
            # 语言代码到语言名称的映射
            language_map = {
                "auto": "自动",
                None: "自动",
                "ko": "韩语",
                "ja": "日语",
                "en": "英语",
                "zh": "中文"
            }
            # 获取语言名称
            language_name = language_map.get(self.app.whisper_language, "自动")
            # 查找语言在下拉框中的索引
            language_index = self.WhisperLanguageSelect.findText(language_name)
            if language_index >= 0:
                self.WhisperLanguageSelect.setCurrentIndex(language_index)
            # 恢复信号发射
            self.WhisperLanguageSelect.blockSignals(False)
        
        # 更新Whisper引擎选择
        if hasattr(self.app, 'whisper_engine'):
            # 阻止信号发射
            self.WhisperEngineSelect.blockSignals(True)
            # 查找引擎在下拉框中的索引
            engine_index = self.WhisperEngineSelect.findText(self.app.whisper_engine)
            if engine_index >= 0:
                self.WhisperEngineSelect.setCurrentIndex(engine_index)
            # 恢复信号发射
            self.WhisperEngineSelect.blockSignals(False)

        # 更新ASS字体方案选择
        if hasattr(self.app, 'ass_pattern'):
            # 阻止信号发射
            self.AssPatternSelect.blockSignals(True)
            
            # 将英文格式转换为中文格式用于UI显示
            preset_mapping = {
                "kor_chn": "韩上中下",
                "jpn_chn": "日上中下",
                "eng_chn": "英上中下",
                "kor_jpn": "韩上日下"
            }
            pattern_name_cn = preset_mapping.get(self.app.ass_pattern, "韩上中下")
            
            # 根据中文方案名称设置选中项
            # 选项为：0=韩上中下, 1=日上中下, 2=英上中下, 3=韩上日下
            preset_to_index = {
                "韩上中下": 0,
                "日上中下": 1,
                "英上中下": 2,
                "韩上日下": 3
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
        self.Output2Md.blockSignals(False)
        self.MergePDF.blockSignals(False)
        self.MergeWord.blockSignals(False)
        self.MergeTxt.blockSignals(False)
        self.MergeMd.blockSignals(False)
    
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
