import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PySide6.QtWidgets import QLabel, QMessageBox


def vtt_to_srt(vtt_path, log_callback=None):
    """
    将VTT文件转换为SRT格式
    
    Args:
        vtt_path: VTT文件路径
        log_callback: 日志回调函数，用于输出转换结果
    
    Returns:
        bool: 转换是否成功
        str: 转换后的SRT文件路径
    """
    srt_path = vtt_path.rsplit('.', 1)[0] + '.srt'
    try:
        with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
            lines = vtt_file.readlines()

        srt_lines = []
        counter = 1
        temp_block = []
        in_subtitle = False

        for line in lines:
            stripped = line.strip()
            # 跳过空行、WEBVTT头部和元数据
            if stripped == '' or stripped == 'WEBVTT' or stripped.startswith('Kind:') or stripped.startswith(
                    'Language:'):
                continue

            if '-->' in stripped:
                # 如果之前有字幕块，先写入
                if in_subtitle and temp_block:
                    srt_lines.append(str(counter))
                    srt_lines.extend(temp_block)
                    srt_lines.append('')
                    counter += 1
                    temp_block = []
                
                # 处理时间戳
                parts = stripped.split('-->')
                start_time = parts[0].strip().replace('.', ',')
                end_time = parts[1].strip().replace('.', ',')
                temp_block.append(f"{start_time} --> {end_time}")
                in_subtitle = True
            else:
                # 跳过纯数字行（VTT的序号行）
                if stripped.isdigit():
                    continue
                # 添加文本行
                if in_subtitle:
                    temp_block.append(stripped)

        # 写入最后一个字幕块
        if in_subtitle and temp_block:
            srt_lines.append(str(counter))
            srt_lines.extend(temp_block)
            srt_lines.append('')

        with open(srt_path, 'w', encoding='utf-8') as srt_file:
            for line in srt_lines:
                srt_file.write(line + '\n')
        
        if log_callback:
            log_callback(f"✅ VTT转换为SRT成功: {os.path.basename(vtt_path)} -> {os.path.basename(srt_path)}")
        
        return True, srt_path
        
    except Exception as e:
        error_msg = f"❌ 转换失败 {os.path.basename(vtt_path)}: {str(e)}"
        if log_callback:
            log_callback(error_msg)
        else:
            QMessageBox.critical(None, "转换错误", error_msg)
        return False, None


def handle_drop_event(event, log_callback=None):
    """
    处理Qt拖放事件
    
    Args:
        event: QDropEvent事件对象
        log_callback: 日志回调函数
    """
    if event.mimeData().hasUrls():
        event.acceptProposedAction()
        valid_files = []
        invalid_files = []
        
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path.lower().endswith('.vtt'):
                valid_files.append(file_path)
            else:
                invalid_files.append(file_path)
        
        # 处理有效文件
        for file_path in valid_files:
            vtt_to_srt(file_path, log_callback)
        
        # 处理无效文件
        for file_path in invalid_files:
            error_msg = f"⚠️ 跳过无效文件: {os.path.basename(file_path)} (不是有效的.vtt文件)"
            if log_callback:
                log_callback(error_msg)
            else:
                QMessageBox.warning(None, "警告", error_msg)
    

def setup_vtt2srt_drop_area(drop_widget, log_callback=None):
    """
    设置VTT到SRT的拖放区域
    
    Args:
        drop_widget: 用于拖放的QLabel或其他QWidget
        log_callback: 日志回调函数
    """
    # 设置拖放属性
    drop_widget.setAcceptDrops(True)
    
    # 定义事件处理函数
    def drag_enter_event(event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # 设置active属性为true，触发悬浮样式
            drop_widget.setProperty("active", "true")
            drop_widget.style().unpolish(drop_widget)
            drop_widget.style().polish(drop_widget)
        
    def drag_leave_event(event):
        # 设置active属性为false，恢复默认样式
        drop_widget.setProperty("active", "false")
        drop_widget.style().unpolish(drop_widget)
        drop_widget.style().polish(drop_widget)
    
    def drop_event(event: QDropEvent):
        handle_drop_event(event, log_callback)
        # 拖放完成后恢复默认样式
        drop_widget.setProperty("active", "false")
        drop_widget.style().unpolish(drop_widget)
        drop_widget.style().polish(drop_widget)
    
    # 绑定事件
    drop_widget.dragEnterEvent = drag_enter_event
    drop_widget.dragLeaveEvent = drag_leave_event
    drop_widget.dropEvent = drop_event
    
    return drop_widget


class Vtt2SrtConverter:
    """
    VTT到SRT转换器类，用于与Qt UI集成
    """
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
    
    def convert(self, vtt_path):
        """
        转换单个VTT文件
        
        Args:
            vtt_path: VTT文件路径
            
        Returns:
            bool: 转换是否成功
        """
        return vtt_to_srt(vtt_path, self.log_callback)[0]
    
    def handle_drop(self, event):
        """
        处理拖放事件
        
        Args:
            event: QDropEvent事件对象
        """
        handle_drop_event(event, self.log_callback)
    
    def setup_drop_widget(self, drop_widget):
        """
        设置拖放组件
        
        Args:
            drop_widget: 用于拖放的QLabel或其他QWidget
        """
        return setup_vtt2srt_drop_area(drop_widget, self.log_callback)