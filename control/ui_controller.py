import os


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
        preset_name = self.current_preset_name
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