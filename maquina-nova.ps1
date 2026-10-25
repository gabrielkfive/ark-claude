# Maquina nova da ARK: primeiro passo em qualquer PC ou notebook recem formatado.
# Regra do Gabriel (25/10/2026): trocou de computador, roda isto antes de tudo.
# Uso (PowerShell como admin):
#   powershell -ExecutionPolicy Bypass -File maquina-nova.ps1 -Verificar   so diagnostica
#   powershell -ExecutionPolicy Bypass -File maquina-nova.ps1              diagnostica e instala o basico
# Depois dele: ark-claude\instalar-ferramentas.ps1 e jarvis-ark\instalar.ps1.
param([switch]$Verificar)
$ErrorActionPreference = "Continue"
function T($m) { Write-Host "`n== $m" -ForegroundColor Yellow }
function Ok($m) { Write-Host "  [ok] $m" -ForegroundColor Green }
function Ruim($m) { Write-Host "  [!!] $m" -ForegroundColor Red }

T "Maquina"
$cs = Get-CimInstance Win32_ComputerSystem
$bios = Get-CimInstance Win32_BIOS
$os = Get-CimInstance Win32_OperatingSystem
$cpu = (Get-CimInstance Win32_Processor | Select-Object -First 1).Name
$ram = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1)
"  Fabricante : $($cs.Manufacturer)"
"  Modelo     : $($cs.Model)"
"  BIOS       : $($bios.Manufacturer) $($bios.SMBIOSBIOSVersion)"
"  CPU        : $cpu"
"  RAM        : $ram GB"
"  Windows    : $($os.Caption) build $($os.BuildNumber)"
if ($ram -lt 8) { Ruim "Menos de 8 GB de RAM: Claude Code e navegador juntos vao arrastar." }

$chromebook = ($cs.Manufacturer -match "Google") -or ($bios.Manufacturer -match "coreboot|MrChromebox") -or ($bios.SMBIOSBIOSVersion -match "MrChromebox")
if ($chromebook) {
  Ruim "Chromebook com Windows: touchpad, teclado e som precisam dos drivers do CoolStar."
  "       Abra https://coolstar.org/chromebook/windows-install.html e siga pelo modelo."
}

T "Disco"
Get-PhysicalDisk | ForEach-Object {
  $gb = [math]::Round($_.Size / 1GB)
  "  $($_.FriendlyName) | $($_.MediaType) | $($_.BusType) | $gb GB"
  if ($_.BusType -match "MMC|SD" -or $_.MediaType -eq "HDD") { Ruim "Disco lento (eMMC ou HDD): essa e a causa provavel da lentidao." }
}
$c = Get-PSDrive C
$livre = [math]::Round($c.Free / 1GB, 1)
"  C: livre $livre GB"
if ($livre -lt 20) { Ruim "Menos de 20 GB livres no C:." }

T "Dispositivos sem driver"
$falhos = Get-CimInstance Win32_PnPEntity | Where-Object { $_.ConfigManagerErrorCode -ne 0 }
if ($falhos) { $falhos | ForEach-Object { Ruim "$($_.Name) (codigo $($_.ConfigManagerErrorCode))" } } else { Ok "nenhum" }

T "Touchpad"
$tp = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object { $_.FriendlyName -match "touch ?pad|precision|I2C HID|ELAN|Synaptics" }
if ($tp) { $tp | ForEach-Object { "  $($_.Status) | $($_.FriendlyName)" } } else { Ruim "nenhum touchpad reconhecido: falta driver do fabricante (ou do CoolStar se for Chromebook)." }

if ($Verificar) { T "So diagnostico. Rode sem -Verificar para instalar."; exit }

T "Energia: plano de alto desempenho"
powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null
if ($LASTEXITCODE -eq 0) { Ok "ativo" } else { "  (plano nao existe nesta maquina, mantido o atual)" }

T "Windows Update: buscar drivers e atualizacoes"
Start-Process "ms-settings:windowsupdate"
UsoClient StartScan 2>$null
"  Janela aberta. Instale tudo, inclusive 'Atualizacoes opcionais > Drivers', e reinicie."

T "Programas base (winget)"
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
  Ruim "winget ausente. Instale 'Instalador de Aplicativo' pela Microsoft Store e rode de novo."
} else {
  foreach ($id in "Git.Git","OpenJS.NodeJS.LTS","Python.Python.3.13","GitHub.cli","jqlang.jq","Google.Chrome") {
    winget install --id $id -e --silent --accept-source-agreements --accept-package-agreements | Out-Null
    if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq -1978335189) { Ok $id } else { Ruim "$id (codigo $LASTEXITCODE)" }
  }
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
  if (-not (Get-Command claude -ErrorAction SilentlyContinue)) { npm install -g @anthropic-ai/claude-code | Out-Null }
  if (Get-Command claude -ErrorAction SilentlyContinue) { Ok "Claude Code" } else { Ruim "Claude Code nao instalou" }
}

T "Proximos passos"
"  1. gh auth login"
"  2. gh repo clone <dono>/ark-claude `$env:USERPROFILE\ark-claude  e  jarvis-ark"
"  3. ark-claude\instalar-ferramentas.ps1  e  jarvis-ark\instalar.ps1"
if ($os.BuildNumber -lt 22000) { "  4. Windows 10: atualizar para o 11 pelo Assistente de Instalacao, se o hardware aceitar." }
