@echo off
:: 设置编码为 UTF-8 解决显示乱码
chcp 65001 >nul

echo ============================================
echo   SubtitleToolbox v3.0 自动化打包程序 (GUI模式)
echo ============================================

:: 执行 PyInstaller 
:: --windowed: 隐藏控制台黑窗口
:: --distpath: 注意末尾不要直接用 \"，这里改用正斜杠以防转义错误
python -m PyInstaller --noconfirm --onefile --windowed ^
--name="SubtitleToolbox" ^
--collect-all "tkinter" ^
--collect-all "customtkinter" ^
--icon="E:\OneDrive\PythonProject\SubtitleToolbox\resources\SubtitleToolbox.ico" ^
--add-data "logic;logic" ^
--add-data "control;control" ^
--add-data "function;function" ^
--add-data "gui;gui" ^
--add-data "font;font" ^
--add-data "config;config" ^
--add-data "E:\OneDrive\PythonProject\SubtitleToolbox\resources\SubtitleToolbox.ico;." ^
--hidden-import="customtkinter" ^
--hidden-import="reportlab" ^
--hidden-import="reportlab.platypus" ^
--hidden-import="reportlab.lib.styles" ^
--hidden-import="win32timezone" ^
--hidden-import="pysrt" ^
--hidden-import="pysubs2" ^
--hidden-import="docx" ^
--hidden-import="docxcompose" ^
--hidden-import="win32com" ^
--hidden-import="win32com.client" ^
--hidden-import="pythoncom" ^
--hidden-import="pypdf" ^
--hidden-import="send2trash" ^
--distpath="D:/" ^
--workpath="D:/Temp_Build" ^
--clean SubtitleToolbox.py

echo.
echo --------------------------------------------
echo 打包执行完毕！
echo 已启用 --windowed 模式，运行 EXE 将不再弹出黑窗口。
echo --------------------------------------------
pause