# Deixa o notebook como servidor da ARK: não dorme na tomada, tampa fechada continua ligado,
# acesso remoto (Tailscale + RustDesk) e Jarvis subindo no logon.
# Uso (PowerShell como admin, FORA do app Claude Desktop): powershell -ExecutionPolicy Bypass -File servidor.ps1 [-Desfazer]
param([switch]$Desfazer)

$adm = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole('Administrators')
if (-not $adm) { Write-Host 'Abra o PowerShell como administrador e rode de novo.' -ForegroundColor Yellow; exit 1 }

$tampa = '4f971e89-eebd-4455-a8de-9e59040e7347'; $acao = '5ca83367-6e45-459f-a27b-476b1d01c936'
$inicio = [Environment]::GetFolderPath('Startup')
$jarvis = Join-Path $env:USERPROFILE 'ark-jarvis'

if ($Desfazer) {
    powercfg /change standby-timeout-ac 30
    powercfg /setacvalueindex SCHEME_CURRENT $tampa $acao 1; powercfg /setactive SCHEME_CURRENT
    Remove-Item "$inicio\ARK Jarvis.vbs" -ErrorAction SilentlyContinue
    Write-Host 'Desfeito: volta a dormir em 30 min e tampa fechada suspende.' -ForegroundColor Green
    exit 0
}

# 1. Energia: na tomada nunca dorme; tela apaga em 10 min; tampa fechada não faz nada
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 10
powercfg /setacvalueindex SCHEME_CURRENT $tampa $acao 0
powercfg /setactive SCHEME_CURRENT
Write-Host 'Energia: não dorme na tomada, tampa fechada continua ligado'

# 2. Acesso remoto
foreach ($id in 'Tailscale.Tailscale', 'RustDesk.RustDesk') {
    if (-not (winget list --id $id --accept-source-agreements 2>$null | Select-String $id)) {
        winget install --id $id -e --silent --accept-package-agreements --accept-source-agreements
    }
}
Write-Host 'Tailscale e RustDesk instalados. Entre no Tailscale com a mesma conta Google do PC.'

# 3. Jarvis no logon (o mesmo vigia do PC, que religa o Node se cair)
if (Test-Path "$jarvis\jarvis-oculto.vbs") {
    # o vbs traz a pasta do PC fixa; aqui aponta para a pasta desta máquina
    (Get-Content "$jarvis\jarvis-oculto.vbs" -Raw).Replace('C:\Users\USER\Documents\ARK CONTENT\SOFTWARE\ark-jarvis', $jarvis) |
        Set-Content "$inicio\ARK Jarvis.vbs" -Encoding Default
    Write-Host 'Jarvis: sobe sozinho no logon'
} else { Write-Host "Jarvis não achado em $jarvis" -ForegroundColor Yellow }

Write-Host "`nFalta: Windows Update em dia e o Claude Code com Remote Control ligado (remoteControlAtStartup já vem no settings.json)." -ForegroundColor Cyan
