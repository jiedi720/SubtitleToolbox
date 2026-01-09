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

# 添加 CUDA 库路径到系统 PATH
if getattr(sys, 'frozen', False):
    # 打包后的程序
    base_dir = os.path.dirname(sys.executable)
    internal_dir = os.path.join(base_dir, '_internal')
    
    # 优先使用打包后内部的 NVIDIA CUDA 库
    cuda_paths = []
    
    # 添加内部 NVIDIA 库路径
    internal_nvidia_path = os.path.join(internal_dir, 'nvidia')
    if os.path.exists(internal_nvidia_path):
        # 添加 nvidia 目录下的所有 bin 目录
        for item in os.listdir(internal_nvidia_path):
            item_path = os.path.join(internal_nvidia_path, item)
            if os.path.isdir(item_path):
                bin_path = os.path.join(item_path, 'bin')
                if os.path.exists(bin_path):
                    cuda_paths.append(bin_path)
    
    # 如果内部没有找到，再尝试外部路径
    if not cuda_paths:
        # 默认使用 ../Faster_Whisper_Model/nvidia（相对于 SubtitleToolbox 目录）
        default_cuda_path = os.path.join(os.path.dirname(base_dir), 'Faster_Whisper_Model', 'nvidia')
        
        if os.path.exists(default_cuda_path):
            # 添加 nvidia 目录下的所有子目录
            for item in os.listdir(default_cuda_path):
                item_path = os.path.join(default_cuda_path, item)
                if os.path.isdir(item_path):
                    bin_path = os.path.join(item_path, 'bin')
                    if os.path.exists(bin_path):
                        cuda_paths.append(bin_path)
else:
    # 开发环境
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 优先从配置文件读取 CUDA 库路径
    cuda_paths = []
    try:
        from function.settings import ConfigManager
        config = ConfigManager()
        config.load_settings()
        if config.cuda_library_path and os.path.exists(config.cuda_library_path):
            cuda_paths.append(config.cuda_library_path)
    except Exception as e:
        pass
    
    # 如果配置文件中没有设置，使用默认路径
    if not cuda_paths:
        # 默认使用 ../Faster_Whisper_Model/nvidia（相对于 SubtitleToolbox 目录）
        default_cuda_path = os.path.join(os.path.dirname(base_dir), 'Faster_Whisper_Model', 'nvidia')
        
        if os.path.exists(default_cuda_path):
            # 添加 nvidia 目录下的所有子目录
            for item in os.listdir(default_cuda_path):
                item_path = os.path.join(default_cuda_path, item)
                if os.path.isdir(item_path):
                    bin_path = os.path.join(item_path, 'bin')
                    if os.path.exists(bin_path):
                        cuda_paths.append(bin_path)

# 使用 os.add_dll_directory 添加 DLL 搜索路径（Windows 10+）
# 同时也添加到 PATH 以兼容旧版本
for cuda_path in cuda_paths:
    if os.path.exists(cuda_path):
        # Windows 10+ 推荐的方法
        try:
            os.add_dll_directory(cuda_path)
        except AttributeError:
            # Windows 7 或更早版本不支持 add_dll_directory
            pass
        
        # 同时也添加到 PATH
        current_path = os.environ.get('PATH', '')
        if cuda_path not in current_path:
            os.environ['PATH'] = cuda_path + os.pathsep + current_path

# 在导入其他模块之前，先导入 ctranslate2 以确保 DLL 正确加载
try:
    import ctranslate2
except Exception as e:
    pass

# 添加 _internal 目录到 DLL 搜索路径（用于打包后的程序，torch DLL 在这里）
if getattr(sys, 'frozen', False):
    internal_dir = os.path.join(base_dir, '_internal')
    if os.path.exists(internal_dir):
        try:
            os.add_dll_directory(internal_dir)
        except AttributeError:
            pass

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
        pass  # 静默处理字体初始化失败
    
    # 创建控制器实例，初始化主窗口
    controller = UnifiedApp(None)
    
    # 显示主窗口
    controller.gui.show()
    
    # 运行应用程序，进入事件循环
    sys.exit(app.exec())