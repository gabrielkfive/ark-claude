# Instala as ferramentas do vibe-coding-toolkit e as skills de projeto do WorkFlowArk no PC (Windows).
# Fontes conferidas em 18/10/2026: guias 04, 07, 15, 16, 18, 20 e 21 do toolkit (revisao de66fe3).
# Uso (PowerShell normal, nao precisa ser admin):
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\ark-claude\instalar-ferramentas.ps1"
# Pode rodar de novo: o que ja existe e pulado.

$ErrorActionPreference = "Continue"
$WFA = @("$env:USERPROFILE\gest-odeagencia", "$env:USERPROFILE\Documents\ARK CONTENT\SOFTWARE\gest-odeagencia") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $WFA) { $WFA = "$env:USERPROFILE\gest-odeagencia" }
$resultado = @()

function Tem($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Passo($nome, $teste, $instalar) {
  Write-Host "== $nome" -ForegroundColor Yellow
  if (& $teste) { Write-Host "   ja estava"; $script:resultado += "$nome : ja estava"; return }
  & $instalar
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
  if (& $teste) { Write-Host "   instalado" -ForegroundColor Green; $script:resultado += "$nome : instalado" }
  else { Write-Host "   FALHOU (veja a mensagem acima)" -ForegroundColor Red; $script:resultado += "$nome : FALHOU" }
}

Passo "pnpm" { Tem "pnpm" } { npm install -g pnpm }
Passo "fd" { Tem "fd" } { winget install --id sharkdp.fd -e --accept-source-agreements --accept-package-agreements }
Passo "Codex CLI" { Tem "codex" } { npm install -g @openai/codex }
Passo "uv (para o Graphify)" { Tem "uv" } { winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements }
Passo "Graphify" { Tem "graphify" } { uv tool install graphifyy }
Passo "Ponytail (plugin do Claude Code)" { (claude plugin list 2>$null | Out-String) -match "ponytail" } {
  claude plugin marketplace add DietrichGebert/ponytail
  claude plugin install ponytail@ponytail
}

# Skills de projeto: ficam dentro do WorkFlowArk (.claude/skills), vao pro git e valem em qualquer maquina.
# --copy porque no Windows o link simbolico aponta pra caminho absoluto e quebra no Mac.
Write-Host "== Skills do WorkFlowArk" -ForegroundColor Yellow
if (Test-Path $WFA) {
  Push-Location $WFA
  $skills = @(
    @("supabase/agent-skills", "supabase-postgres-best-practices"),
    @("shadcn/ui", "shadcn"),
    @("https://github.com/trailofbits/skills/tree/main/plugins/differential-review", "differential-review"),
    @("vercel-labs/agent-skills", "vercel-react-best-practices"),
    @("vercel-labs/skills", "find-skills")
  )
  foreach ($s in $skills) {
    if (Test-Path ".claude\skills\$($s[1])\SKILL.md") { Write-Host "   $($s[1]) ja estava"; continue }
    npx --yes skills@latest add $s[0] --skill $s[1] --agent claude-code --copy --yes
    if (Test-Path ".claude\skills\$($s[1])\SKILL.md") { $resultado += "skill $($s[1]) : instalada" } else { $resultado += "skill $($s[1]) : FALHOU" }
  }
  Write-Host "   Confira com 'git status' e leia os SKILL.md novos antes de commitar." -ForegroundColor Cyan
  Pop-Location
} else {
  Write-Host "   pasta do WorkFlowArk nao encontrada em $WFA (ajuste a variavel no topo)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Resumo:" -ForegroundColor Yellow
$resultado | ForEach-Object { Write-Host "  $_" }
Write-Host ""
Write-Host "Falta so voce:"
Write-Host "  1. Ponytail: abra o Claude Code, rode /hooks e confie nos hooks do plugin. Depois abra uma sessao nova."
Write-Host "  2. Codex: rode 'codex' uma vez para entrar com a sua conta."
Write-Host "  3. xtool (app de iPhone): veja docs/xtool.md. No Mac e bem mais simples."
Write-Host "  Docker ficou de fora de proposito: pesa e o PC ja trava com carga."
