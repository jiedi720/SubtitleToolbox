@echo off
chcp 65001 >nul
echo 正在添加文件...
git add .
echo.

echo 正在提交更改...
set /p msg="请输入更新内容(直接回车默认'日常更新'): "
if "%msg%"=="" set msg=日常更新
git commit -m "%msg%"
echo.

echo 正在强制推送到 GitHub (覆盖远程)...
:: 注意：这里加了 --force，确保不会出现 [rejected] 错误
git push -u origin main --force
echo.

if %errorlevel% == 0 (
    echo ✅ 更新完成！
) else (
    echo ❌ 更新失败，请检查网络或 OneDrive 是否占用文件。
)
pause