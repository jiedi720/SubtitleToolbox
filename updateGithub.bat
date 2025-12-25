@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 🔄 正在强制切换至 main 分支...
git checkout main

echo 📥 正在添加文件...
git add -A

echo 💾 正在提交更改...
set /p msg="请输入更新内容(回车默认'日常更新'): "
if "%msg%"=="" set msg=日常更新
git commit -m "%msg%"

echo 📤 正在强制推送到 GitHub...
git push origin main --force

if %errorlevel% == 0 (
    echo.
    echo ✅ 更新完成！项目已在 main 分支同步。
) else (
    echo.
    echo ❌ 推送失败，请检查 VPN 网络。
)
pause