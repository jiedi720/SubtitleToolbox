#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SubtitleToolbox 主入口文件

该文件负责初始化应用程序，设置Python路径，加载资源文件，
创建应用实例和控制器，并启动GUI界面。
"""

import os
import sys

# 获取当前文件所在目录和GUI目录
base_dir = os.path.dirname(os.path.abspath(__file__))
gui_dir = os.path.join(base_dir, "gui")

# 添加项目目录到Python路径，确保模块能正确导入
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
if gui_dir not in sys.path:
    sys.path.insert(0, gui_dir)

from PySide6.QtWidgets import QApplication
from function.controllers import UnifiedApp

if __name__ == "__main__":
    # 创建PySide6应用实例
    app = QApplication(sys.argv)
    
    # 初始化字体设置（在创建控制器之前）
    try:
        from logic.pdf_logic import init_fonts
        init_fonts()
    except Exception as e:
        print(f"字体初始化失败: {e}")
    
    # 创建控制器实例，初始化主窗口
    controller = UnifiedApp(None)
    
    # 显示主窗口
    controller.gui.show()
    
    # 运行应用程序，进入事件循环
    sys.exit(app.exec())
