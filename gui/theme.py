from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


# 全局变量：保存程序启动时的默认样式名称
_original_style = None


def apply_theme(mode):
    """
    应用主题设置到整个应用程序
    
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
    from PySide6.QtGui import QPalette
    palette = QPalette()
    
    # 根据传入的主题模式应用不同的主题设置
    if mode == "System":
        # 应用系统默认主题
        app.setStyle(None)  # 清除自定义样式，使用系统默认样式
        app.setPalette(palette)  # 应用默认调色板
    elif mode == "Light":
        # 应用浅色主题
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
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(128, 128, 128))  # 占位符文本色（浅灰色）
        
        app.setPalette(palette)  # 应用深色调色板
    
    # 强制刷新所有控件，确保主题更改立即生效
    app.processEvents()
    for widget in QApplication.allWidgets():
        widget.style().unpolish(widget)  # 移除旧样式
        widget.style().polish(widget)  # 应用新样式
        widget.update()  # 更新控件
