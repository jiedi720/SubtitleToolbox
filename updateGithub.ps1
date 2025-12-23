cd "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SubtitleToolbox"

# 修改当前项目的用户名
git config user.name "jiedi720"

# (可选) 修改全局用户名
git config --global user.name "jiedi720"

# 设置 UTF8 编码以支持中文显示
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "--- 正在准备上传 SubtitleToolbox v3.0 ---" -ForegroundColor Cyan

# 添加更改
git add .

# 获取用户输入
$msg = Read-Host "请输入更新说明 (直接回车默认为 '日常更新')"
if ($msg -eq "") { $msg = "日常更新" }

# 提交
git commit -m $msg

# 推送
Write-Host "正在推送到 GitHub..." -ForegroundColor Yellow
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 更新成功！" -ForegroundColor Green
} else {
    Write-Host "❌ 更新失败，请检查网络。" -ForegroundColor Red
}

pause