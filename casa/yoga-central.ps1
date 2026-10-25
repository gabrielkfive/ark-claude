# Transforma o notebook Yoga (Lenovo 80UK) na central do escritório.
# Rodar como admin, depois de maquina-nova.ps1:
#   powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\ark-claude\casa\yoga-central.ps1
# Faz: nunca dormir na tomada, tampa fechada não desliga, Deskflow (mouse entre PC, Mac e Yoga),
# painel JARVIS subindo no logon em tela cheia, n8n no logon se o ark-maquina estiver clonado.
param([int]$Porta = 8095)
$ErrorActionPreference = 'Stop'
$casa = $PSScriptRoot
$painel = Join-Path $casa 'painel'

Write-Host '1. Energia: na tomada nunca dorme nem hiberna; tela apaga em 10 min e volta no toque'
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 10
powercfg /hibernate off
# tampa fechada na tomada = nada (subgrupo botões, LIDACTION)
powercfg /setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 0
powercfg /setactive SCHEME_CURRENT

Write-Host '2. Wi-Fi não desliga para economizar energia'
Get-NetAdapter -Physical | Where-Object Status -eq 'Up' | ForEach-Object {
  try { Set-NetAdapterPowerManagement -Name $_.Name -AllowComputerToTurnOffDevice Disabled -ErrorAction Stop } catch {}
}

Write-Host '3. Deskflow (mouse e teclado passando entre as máquinas)'
winget install --id Deskflow.Deskflow -e --accept-source-agreements --accept-package-agreements

Write-Host '4. Porta do painel liberada só na rede privada'
if (-not (Get-NetFirewallRule -DisplayName 'Painel JARVIS' -ErrorAction SilentlyContinue)) {
  New-NetFirewallRule -DisplayName 'Painel JARVIS' -Direction Inbound -Protocol TCP -LocalPort $Porta -Profile Private -Action Allow | Out-Null
}

Write-Host '5. Tarefas no logon: servidor do painel, Chrome em tela cheia e n8n'
$py = (Get-Command python).Source
$pyw = Join-Path (Split-Path $py) 'pythonw.exe'
$chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
$gatilho = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$cfg = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0 -RestartCount 99 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName 'ARK Painel servidor' -Force -Trigger $gatilho -Settings $cfg `
  -Action (New-ScheduledTaskAction -Execute $pyw -Argument "servidor.py $Porta" -WorkingDirectory $painel) | Out-Null
if ($chrome) {
  $g2 = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME; $g2.Delay = 'PT20S'
  Register-ScheduledTask -TaskName 'ARK Painel tela' -Force -Trigger $g2 -Settings $cfg `
    -Action (New-ScheduledTaskAction -Execute $chrome -Argument "--kiosk --app=http://localhost:$Porta --user-data-dir=$env:LOCALAPPDATA\painel-jarvis") | Out-Null
}
$n8n = Join-Path $env:USERPROFILE 'ark-maquina\n8n\iniciar-servidor.cmd'
if (Test-Path $n8n) {
  Register-ScheduledTask -TaskName 'ARK n8n' -Force -Trigger $gatilho -Settings $cfg `
    -Action (New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$n8n`"") | Out-Null
} else { Write-Host '   n8n: clonar gabrielkfive/ark-maquina em %USERPROFILE% e rodar este script de novo' }

if (-not (Test-Path (Join-Path $painel 'painel.env'))) {
  Write-Host '6. Falta casa\painel\painel.env (copiar do PC; tem as chaves do Ark Brain e do Voice Monkey)'
}
Write-Host '7. Subindo agora (sem esperar o próximo login)'
Get-ScheduledTask -TaskName 'ARK *' | Start-ScheduledTask
Start-Sleep 5
try { Invoke-WebRequest "http://localhost:$Porta/api/acoes" -UseBasicParsing | Out-Null; Write-Host '   painel respondeu' }
catch { Write-Host "   painel NÃO respondeu: $($_.Exception.Message)"; & $py (Join-Path $painel 'servidor.py') $Porta }
Write-Host "Pronto para testar: http://localhost:$Porta  (iPad: http://<ip do Yoga>:$Porta)"
Write-Host 'Login automático: rodar netplwiz e desmarcar a senha (só o Gabriel faz, pede a senha dele).'
