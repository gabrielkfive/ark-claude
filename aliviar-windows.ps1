# Alivia Windows 10/11 de máquina fraca. Tudo reversível: rode com -Desfazer para voltar.
# Uso (PowerShell como admin): powershell -ExecutionPolicy Bypass -File aliviar-windows.ps1 [-Desfazer]
param([switch]$Desfazer)

$adm = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole('Administrators')
if (-not $adm) { Write-Host 'Abra o PowerShell como administrador e rode de novo.' -ForegroundColor Yellow; exit 1 }

$cdm = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager'
$dicas = 'SubscribedContent-338388Enabled','SubscribedContent-338389Enabled','SubscribedContent-353694Enabled',
         'SubscribedContent-353696Enabled','SystemPaneSuggestionsEnabled','SilentInstalledAppsEnabled','SoftLandingEnabled'
$alto = '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
$equilibrado = '381b4222-f694-41f0-9685-ff5bb260df2e'

if ($Desfazer) {
    Set-Service WSearch -StartupType Automatic; Start-Service WSearch -ErrorAction SilentlyContinue
    foreach ($d in $dicas) { Set-ItemProperty $cdm $d 1 -Type DWord -ErrorAction SilentlyContinue }
    powercfg /setactive $equilibrado
    Write-Host 'Desfeito: busca indexada, dicas do Windows e plano Equilibrado de volta.' -ForegroundColor Green
    exit 0
}

# 1. Indexação de busca em Manual (a busca continua funcionando, só mais devagar)
Stop-Service WSearch -Force -ErrorAction SilentlyContinue
Set-Service WSearch -StartupType Manual
Write-Host 'Indexação de busca: Manual'

# 2. Dicas, anúncios e apps sugeridos do Windows
if (-not (Test-Path $cdm)) { New-Item $cdm -Force | Out-Null }
foreach ($d in $dicas) { Set-ItemProperty $cdm $d 0 -Type DWord }
Write-Host 'Dicas e anúncios do Windows: desligados'

# 3. Plano Alto desempenho (cria se não existir)
if (-not (powercfg /list | Select-String $alto)) { powercfg -duplicatescheme $alto | Out-Null }
powercfg /setactive $alto
Write-Host 'Plano de energia: Alto desempenho'

# 4. Programas que abrem com o Windows: só lista, quem decide desligar é você (Gerenciador de Tarefas, aba Inicializar)
Write-Host "`nAbrem junto com o Windows:" -ForegroundColor Cyan
Get-CimInstance Win32_StartupCommand | Select-Object Name, Location | Format-Table -AutoSize

# 5. Windows Update: abre a tela para instalar pendentes e drivers opcionais
Start-Process 'ms-settings:windowsupdate'
Write-Host 'Pronto. Na tela do Windows Update: Verificar atualizações e depois Atualizações opcionais (drivers).' -ForegroundColor Green
