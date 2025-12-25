@echo off
chcp 65001 >nul

echo 正在检查分支状态...
:: 强制切换回 main 分支，确保提交有家可归
git checkout main

echo.
echo 正在添加文件...
git add .

echo.
echo 正在提交更改...
set /p msg="请输入更新内容(直接回车默认'日常更新'): "
if "%msg%"=="" set msg=日常更新

:: 提交更改
git commit -m "%msg%"

echo.
echo 正在强制推送到 GitHub...
:: 推送本地 main 到远程 origin 的 main
git push origin main --force

if %errorlevel% == 0 (
    echo.
    echo ✅ 更新完成！已成功推送到 main 分支。
) else (
    echo.
    echo ❌ 推送失败。
    echo 💡 提示：请检查是否正在使用代理(VPN)，或尝试输入 git pull origin main
)
pause