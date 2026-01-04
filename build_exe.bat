@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   SubtitleToolbox 自动化打包程序
echo ============================================

if not exist "SubtitleToolbox.py" (
    echo [Error] SubtitleToolbox.py not found!
    pause
    exit
)

python -m PyInstaller --noconfirm --onefile --windowed --name="SubtitleToolbox" --collect-all "send2trash" --icon="resources\SubtitleToolbox.ico" --add-data "logic;logic" --add-data "control;control" --add-data "function;function" --add-data "gui;gui" --add-data "font;font" --add-data "config;config" --add-data "resources\SubtitleToolbox.ico;." --hidden-import="reportlab" --hidden-import="reportlab.platypus" --hidden-import="reportlab.lib.styles" --hidden-import="pysrt" --hidden-import="pysubs2" --hidden-import="docx" --hidden-import="pypdf" --hidden-import="send2trash" --distpath="." --workpath="C:/Temp_Build" --clean SubtitleToolbox.py

echo.
echo --------------------------------------------
echo 打包执行完毕！
echo 已启用 --windowed 模式。
echo 输出目录: 当前目录
echo --------------------------------------------
pause