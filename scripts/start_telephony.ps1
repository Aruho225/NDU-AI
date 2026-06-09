# Start Twilio webhook + LiveKit voice agent (run from project root)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".env")) {
    Write-Host "Copy .env.example to .env and fill in Twilio + LiveKit keys." -ForegroundColor Yellow
}

Write-Host "Starting Twilio webhook on http://0.0.0.0:8000 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PWD'; python -m uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 2

Write-Host "Starting LiveKit agent (ndu-assistant) ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PWD'; python agent.py dev"

Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Expose port 8000:  ngrok http 8000"
Write-Host "  2. Set TWILIO_WEBHOOK_BASE_URL in .env to the ngrok HTTPS URL"
Write-Host "  3. Twilio Console -> Phone number -> Voice POST -> {base}/twilio/voice/inbound"
Write-Host "  4. Twilio Console -> Messaging POST -> {base}/twilio/webhook"
Write-Host "  5. Check http://localhost:8000/telephony/status"
