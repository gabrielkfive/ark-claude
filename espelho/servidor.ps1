# Deixa o notebook como servidor da ARK: não dorme na tomada, tampa fechada continua ligado,
# acesso remoto (Tailscale + RustDesk) e Jarvis subindo no logon.
# Uso (PowerShell como admin, FORA do app Claude Desktop): powershell -ExecutionPolicy Bypass -File servidor.ps1 [-Desfazer]
param([switch]$Desfazer)

$adm = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)  # nome do grupo muda no Windows pt-BR
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
if (-not (winget list --id Tailscale.Tailscale --accept-source-agreements 2>$null | Select-String Tailscale)) {
    winget install --id Tailscale.Tailscale -e --silent --accept-package-agreements --accept-source-agreements
}
# RustDesk não está no winget: MSI x86_64 da última versão no GitHub oficial
if (-not (Test-Path "$env:ProgramFiles\RustDesk\rustdesk.exe")) {
    $rel = Invoke-RestMethod https://api.github.com/repos/rustdesk/rustdesk/releases/latest
    $msi = $rel.assets | Where-Object name -match 'x86_64\.msi$' | Select-Object -First 1
    if ($msi) {
        $alvo = Join-Path $env:TEMP $msi.name
        Invoke-WebRequest $msi.browser_download_url -OutFile $alvo
        if ((Get-AuthenticodeSignature $alvo).Status -eq 'Valid') { Start-Process msiexec.exe "/i `"$alvo`" /qn" -Wait }
        else { Write-Host 'RustDesk: assinatura do MSI inválida, não instalei' -ForegroundColor Yellow }
    }
}
Write-Host 'Tailscale e RustDesk instalados. Entre no Tailscale com a mesma conta Google do PC.'

# 3. Jarvis no logon (o mesmo vigia do PC, que religa o Node se cair)
if (Test-Path "$jarvis\jarvis-oculto.vbs") {
    # o vbs traz a pasta do PC fixa; aqui aponta para a pasta desta máquina
    $node = (Get-Command node -ErrorAction SilentlyContinue).Source
    (Get-Content "$jarvis\jarvis-oculto.vbs" -Raw).Replace('C:\Users\USER\Documents\ARK CONTENT\SOFTWARE\ark-jarvis', $jarvis).
        Replace('C:\Program Files\nodejs\node.exe', $(if ($node) { $node } else { 'node' })) |
        Set-Content "$inicio\ARK Jarvis.vbs" -Encoding Default
    Write-Host 'Jarvis: sobe sozinho no logon'
} else { Write-Host "Jarvis não achado em $jarvis" -ForegroundColor Yellow }

Write-Host "`nFalta: Windows Update em dia e o Claude Code com Remote Control ligado (remoteControlAtStartup já vem no settings.json)." -ForegroundColor Cyan
