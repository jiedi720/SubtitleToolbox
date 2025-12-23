import os
import sys
import customtkinter as ctk
from control.main_controller import UnifiedApp
# 导入你刚刚拆分出的主界面类
from gui.main_gui import ToolboxGUI 

# 确保项目根目录在搜索路径中
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

def center_window(root, width, height):
    """窗口居中逻辑封装"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    # 1. 初始化窗口对象
    root = ctk.CTk()
    root.title("SubtitleToolbox") # 可以在这里统一设置标题
    
    # 2. 设置窗口大小和位置
    window_width = 720  # 根据拆分后的布局微调宽度
    window_height = 580 # 增加高度以确保日志区显示完整
    center_window(root, window_width, window_height)
    
    # 3. 启动逻辑控制器 (Controller)
    # 注意：在 UnifiedApp 的 __init__ 中，你应该实例化 ToolboxGUI
    # 例如：self.gui = ToolboxGUI(self.root, self)
    app = UnifiedApp(root)
    
    # 4. 进入主循环
    root.mainloop()