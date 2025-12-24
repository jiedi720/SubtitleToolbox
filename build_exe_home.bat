@echo off
:: 设置编码为 UTF-8 解决显示乱码
chcp 65001 >nul

echo ============================================
echo   SubtitleToolbox 自动化打包程序
echo ============================================

:: 执行 PyInstaller 
:: 注意：^ 符号后严禁有任何空格
python -m PyInstaller --noconfirm --onefile --windowed ^
--name="SubtitleToolbox" ^
--collect-all "tkinter" ^
--collect-all "customtkinter" ^
--collect-all "send2trash" ^
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
echo 已启用 --windowed 模式。
echo --------------------------------------------
pause