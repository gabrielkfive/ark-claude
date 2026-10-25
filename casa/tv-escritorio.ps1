# TV do escritório como 2º monitor do PC: Chrome em tela cheia no WorkFlowArk, sozinho no logon.
# Instalar (uma vez, no PC):
#   powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\ark-claude\casa\tv-escritorio.ps1 -Registrar
# Primeira vez: fazer login no WorkFlowArk na janela da TV (perfil próprio do Chrome, fica salvo).
# Windows: Configurações > Sistema > Tela > "Estender estas telas" (espelhado não funciona).
param([switch]$Registrar, [string]$Url = 'https://workflowark.arkcontent.workers.dev/workflowark')

if ($Registrar) {
  $g = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME; $g.Delay = 'PT30S'
  $a = New-ScheduledTaskAction -Execute "$env:windir\System32\WindowsPowerShell\v1.0\powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSCommandPath`""
  Register-ScheduledTask -TaskName 'ARK TV escritorio' -Force -Trigger $g -Action $a `
    -Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -ExecutionTimeLimit 0) | Out-Null
  Start-ScheduledTask -TaskName 'ARK TV escritorio'
  Write-Host 'ARK TV escritorio registrada: abre no próximo logon e agora, se a TV estiver ligada.'
  return
}

Add-Type -AssemblyName System.Windows.Forms
$tv = $null
# TV pode demorar a acordar no HDMI: espera até 5 min
for ($i = 0; $i -lt 60 -and -not $tv; $i++) {
  $tv = [System.Windows.Forms.Screen]::AllScreens | Where-Object { -not $_.Primary } | Select-Object -First 1
  if (-not $tv) { Start-Sleep 5 }
}
if (-not $tv) { return }  # sem 2ª tela: não toma o monitor principal do Gabriel

$chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe") |
  Where-Object { Test-Path $_ } | Select-Object -First 1
# perfil separado: sem ele o Chrome aberto só ganha uma aba nova, sem tela cheia
& $chrome --kiosk --no-first-run --noerrdialogs --disable-session-crashed-bubble `
  "--window-position=$($tv.Bounds.X),$($tv.Bounds.Y)" "--user-data-dir=$env:LOCALAPPDATA\tv-escritorio" $Url
