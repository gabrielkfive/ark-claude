#!/usr/bin/env bash
# Instala as ferramentas do vibe-coding-toolkit, o xtool e as skills de projeto do WorkFlowArk no Mac.
# Fontes conferidas em 18/10/2026 (toolkit revisao de66fe3; xtool.sh/documentation).
# Uso: bash ~/ark-claude/instalar-ferramentas.sh
# Pode rodar de novo: o que ja existe e pulado.
set -u
WFA="${WFA:-$HOME/gest-odeagencia}"
RESUMO=""

passo() { # nome, comando-de-teste, comando-de-instalar
  echo "== $1"
  if eval "$2" >/dev/null 2>&1; then echo "   ja estava"; RESUMO+="$1: ja estava\n"; return; fi
  eval "$3"
  if eval "$2" >/dev/null 2>&1; then echo "   instalado"; RESUMO+="$1: instalado\n"; else echo "   FALHOU"; RESUMO+="$1: FALHOU\n"; fi
}

command -v brew >/dev/null || { echo "Falta o Homebrew: https://brew.sh"; exit 1; }

passo "pnpm" "command -v pnpm" "brew install pnpm"
passo "fd" "command -v fd" "brew install fd"
passo "Codex CLI" "command -v codex" "npm install -g @openai/codex"
passo "uv" "command -v uv" "brew install uv"
passo "Graphify" "command -v graphify" "uv tool install graphifyy"
passo "Ponytail" "claude plugin list | grep -q ponytail" \
  "claude plugin marketplace add DietrichGebert/ponytail && claude plugin install ponytail@ponytail"
passo "xtool" "command -v xtool" "brew install xtool-org/tap/xtool"

echo "== Skills do WorkFlowArk"
if [ -d "$WFA" ]; then
  cd "$WFA" || exit 1
  while read -r fonte nome; do
    [ -f ".claude/skills/$nome/SKILL.md" ] && { echo "   $nome ja estava"; continue; }
    npx --yes skills@latest add "$fonte" --skill "$nome" --agent claude-code --copy --yes
    [ -f ".claude/skills/$nome/SKILL.md" ] && RESUMO+="skill $nome: instalada\n" || RESUMO+="skill $nome: FALHOU\n"
  done <<'LISTA'
supabase/agent-skills supabase-postgres-best-practices
shadcn/ui shadcn
https://github.com/trailofbits/skills/tree/main/plugins/differential-review differential-review
vercel-labs/agent-skills vercel-react-best-practices
vercel-labs/skills find-skills
LISTA
  echo "   Confira com 'git status' e leia os SKILL.md novos antes de commitar."
else
  echo "   WorkFlowArk nao encontrado em $WFA (rode com WFA=/caminho bash instalar-ferramentas.sh)"
fi

printf "\nResumo:\n$RESUMO"
echo
echo "Falta so voce:"
echo "  1. Ponytail: no Claude Code rode /hooks, confie nos hooks do plugin e abra sessao nova."
echo "  2. Codex: rode 'codex' uma vez para entrar."
echo "  3. xtool: instale o Xcode pela App Store, abra uma vez, e siga docs/xtool.md (passo 'xtool setup')."
