@echo off
chcp 65001 >nul
echo 正在添加文件...
git add .
echo 正在提交更改...
set /p msg="请输入更新内容(直接回车默认'日常更新'): "
if "%msg%"=="" set msg=日常更新
git commit -m "%msg%"
echo 正在推送到 GitHub...
git push
echo.
echo ✅ 更新完成！
pause