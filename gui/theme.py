from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
import sys
import io

# 设置标准输出为 UTF-8（只在非打包环境下）
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 全局变量：保存程序启动时的默认样式名称
_original_style = None


def apply_theme(mode):
    """
    应用主题设置到整个应用程序（基础版）
    
    Args:
        mode: 主题模式，可选值: 
              - "System": 系统默认主题
              - "Light": 浅色主题
              - "Dark": 深色主题
    """
    global _original_style
    
    # 获取当前运行的QApplication实例
    app = QApplication.instance()
    
    # 首次调用时保存原始样式名称
    if _original_style is None:
        _original_style = app.style().objectName()
    
    # 创建全新的调色板
    palette = QPalette()
    
    # 根据传入的主题模式应用不同的主题设置
    if mode == "System":
        # 应用系统默认主题（Win11 下为 Win11 样式）
        app.setStyle(None)  # 清除自定义样式，使用系统默认样式
        app.setPalette(palette)  # 应用默认调色板
    elif mode == "Light":
        # 应用浅色主题（使用系统默认样式，Win11 下为 Win11 样式）
        app.setStyle(None)  # 使用系统默认样式（如Windows11）
        app.setPalette(palette)  # 应用默认调色板
    elif mode == "Dark":
        # 应用深色主题
        app.setStyle(None)  # 使用系统默认样式（如Windows11），与Light模式保持一致

        # 设置深色主题的各种颜色
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))  # 窗口背景色
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)  # 窗口文本色
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))  # 基础背景色
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))  # 交替基础色
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))  # 工具提示背景色
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)  # 工具提示文本色
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)  # 文本色
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))  # 按钮背景色
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)  # 按钮文本色
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))  # 链接色
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))  # 高亮色
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(180, 180, 180))  # 占位符文本色（深色模式下更亮）

        app.setPalette(palette)  # 应用深色调色板
    
    # 强制刷新所有控件，确保主题更改立即生效
    app.processEvents()
    for widget in QApplication.allWidgets():
        widget.style().unpolish(widget)  # 移除旧样式
        widget.style().polish(widget)  # 应用新样式
        widget.update()  # 更新控件


def apply_theme_enhanced(mode):
    """
    应用主题设置到整个应用程序（增强版）
    确保只需点击一次就能完全切换主题

    Args:
        mode: 主题模式，可选值:
              - "System": 系统默认主题
              - "Light": 浅色主题
              - "Dark": 深色主题
    """
    app = QApplication.instance()

    # 创建全新的调色板
    palette = QPalette()

    # 根据传入的主题模式应用不同的主题设置
    if mode == "System":
        # 应用系统默认主题
        app.setStyle(None)  # 清除自定义样式，使用系统默认样式
        app.setPalette(palette)  # 应用默认调色板

        # 清除 QMessageBox 的样式表，使用系统默认样式
        app.setStyleSheet("")
    elif mode == "Light":
        # 应用浅色主题（使用系统默认样式，Win11 下为 Win11 样式）
        app.setStyle(None)  # 使用系统默认样式（如Windows11）

        # 显式设置浅色调色板，确保颜色正确
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))  # 窗口背景色
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)  # 窗口文本色
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # 基础背景色
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))  # 交替基础色
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 222))  # 工具提示背景色
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)  # 工具提示文本色
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)  # 文本色
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))  # 按钮背景色
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)  # 按钮文本色
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.white)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))  # 链接色
        palette.setColor(QPalette.ColorRole.Highlight, QColor(51, 153, 255))  # 高亮色
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(128, 128, 128))  # 占位符文本色（浅色模式下更深）

        app.setPalette(palette)  # 应用浅色调色板

        # 清除 QMessageBox 的样式表，使用系统默认样式
        app.setStyleSheet("")
    elif mode == "Dark":
        # 应用深色主题
        app.setStyle(None)  # 使用系统默认样式（如Windows11），与Light模式保持一致

        # 设置深色主题的各种颜色
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))  # 窗口背景色
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)  # 窗口文本色
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))  # 基础背景色
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))  # 交替基础色
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))  # 工具提示背景色
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)  # 工具提示文本色
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)  # 文本色
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))  # 按钮背景色
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)  # 按钮文本色
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))  # 链接色
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))  # 高亮色
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)  # 高亮文本色
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(180, 180, 180))  # 占位符文本色（深色模式下更亮）

        app.setPalette(palette)  # 应用深色调色板

        # 设置 QMessageBox 的样式表，确保深色模式下内容区域和按钮也显示为深色
        app.setStyleSheet("""
            QMessageBox {
                background-color: #353535;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #353535;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #454545;
            }
            QMessageBox QPushButton:pressed {
                background-color: #555555;
            }
        """)
    app.processEvents()

    # 更新所有控件的样式
    widget_count = 0
    for widget in QApplication.allWidgets():
        widget_count += 1
        # 保存当前的样式表
        current_stylesheet = widget.styleSheet()

        # 移除旧样式
        widget.style().unpolish(widget)
        # 应用新样式
        widget.style().polish(widget)

        # 如果有样式表，重新应用它（确保样式表优先级高于调色板）
        if current_stylesheet:
            widget.setStyleSheet(current_stylesheet)

        # 更新控件
        widget.update()

    # 再次处理事件，确保所有更新都完成
    app.processEvents()

    # 特殊处理：更新硬编码颜色的标签（在所有模式下都执行）
    fixed_labels = 0
    for widget in QApplication.allWidgets():
        if hasattr(widget, 'objectName'):
            obj_name = widget.objectName()
            if obj_name in ['VolumeLabel', 'AssPatternLabel', 'WhisperModelLabel', 'WhisperLanguageLabel']:
                # 移除硬编码的颜色，让它跟随主题
                current_style = widget.styleSheet()
                if 'color: rgb(0, 0, 0);' in current_style:
                    widget.setStyleSheet(current_style.replace('color: rgb(0, 0, 0);', 'color: palette(text);'))
                    fixed_labels += 1

    # 最后再次处理事件，确保所有更新都完成
    app.processEvents()


def refresh_all_widget_styles():
    """
    通用函数：刷新所有控件的样式，确保 [theme="light"] 和 [theme="dark"] 选择器正确应用
    这个函数可以自动检测并应用UI文件中定义的主题相关样式
    """
    app = QApplication.instance()

    # 遍历所有控件并重新应用样式表以确保主题选择器生效
    for widget in QApplication.allWidgets():
        # 重新应用控件的样式表
        current_stylesheet = widget.styleSheet()
        if current_stylesheet:
            # 重新设置样式表以确保主题选择器生效
            widget.setStyleSheet(current_stylesheet)

        # 强制控件更新样式
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()

    # 处理事件，确保所有更改都生效
    app.processEvents()
