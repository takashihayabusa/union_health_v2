$ProjectDir = "C:\Users\maruk\Desktop\union_health_v2"
$PythonExe  = "$ProjectDir\venv\Scripts\python.exe"

while ($true) {

    # Django (port 8000) check
    $django = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue

    if (-not $django) {

        # Windowsに保存してある秘密情報を毎回読み込む
        $env:DJANGO_SECRET_KEY = [Environment]::GetEnvironmentVariable("DJANGO_SECRET_KEY", "User")
        $env:LINE_CHANNEL_ACCESS_TOKEN = [Environment]::GetEnvironmentVariable("LINE_CHANNEL_ACCESS_TOKEN", "User")
        $env:LINE_CHANNEL_SECRET = [Environment]::GetEnvironmentVariable("LINE_CHANNEL_SECRET", "User")
        $env:UNION_LINE_CHANNEL_ACCESS_TOKEN = [Environment]::GetEnvironmentVariable("UNION_LINE_CHANNEL_ACCESS_TOKEN", "User")

        # PowerShellから直接Djangoを起動
        Start-Process -FilePath $PythonExe `
            -ArgumentList "manage.py runserver 0.0.0.0:8000" `
            -WorkingDirectory $ProjectDir

        Start-Sleep -Seconds 5
    }

    # ngrok process check
    $ngrok = Get-Process ngrok -ErrorAction SilentlyContinue

    if (-not $ngrok) {
        Start-Process -FilePath "ngrok.exe" `
            -ArgumentList "http 8000" `
            -WorkingDirectory $ProjectDir

        Start-Sleep -Seconds 5
    }

    Start-Sleep -Seconds 30
}