$ProjectDir = "C:\Users\maruk\Desktop\union_health_v2"
$PythonExe  = "$ProjectDir\venv\Scripts\python.exe"

while ($true) {

    # インターネット接続確認（最大3秒で判定）
    $internet = $false
    $tcp = New-Object System.Net.Sockets.TcpClient

    try {
        $result = $tcp.BeginConnect("1.1.1.1", 443, $null, $null)
        $success = $result.AsyncWaitHandle.WaitOne(3000, $false)

        if ($success -and $tcp.Connected) {
            $tcp.EndConnect($result)
            $internet = $true
        }
    }
    catch {
        $internet = $false
    }
    finally {
        $tcp.Close()
    }

    if (-not $internet) {
        # インターネット切断中はDjango/ngrokを触らず待機
        Start-Sleep -Seconds 30
        continue
    }

    # Django (port 8000) check
    $django = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue

    if (-not $django) {

        # Windowsに保存してある秘密情報を毎回読み込む
        $env:DJANGO_SECRET_KEY = [Environment]::GetEnvironmentVariable("DJANGO_SECRET_KEY", "User")
        $env:LINE_CHANNEL_ACCESS_TOKEN = [Environment]::GetEnvironmentVariable("LINE_CHANNEL_ACCESS_TOKEN", "User")
        $env:LINE_CHANNEL_SECRET = [Environment]::GetEnvironmentVariable("LINE_CHANNEL_SECRET", "User")
        $env:UNION_LINE_CHANNEL_ACCESS_TOKEN = [Environment]::GetEnvironmentVariable("UNION_LINE_CHANNEL_ACCESS_TOKEN", "User")

        # Djangoを起動
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