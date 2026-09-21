#!/usr/bin/env bash
# Instala ou atualiza o plugin ark-claude nesta máquina (Mac, Linux ou Git Bash no Windows).
# Uso: bash instalar.sh
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

echo "== 1. código atualizado"
git -C "$DIR" pull --ff-only || true

echo "== 2. marketplace + plugin"
claude plugin marketplace add "$DIR" >/dev/null 2>&1 || claude plugin marketplace update ark-claude >/dev/null 2>&1 || true
claude plugin install ark@ark-claude >/dev/null 2>&1 || claude plugin update ark@ark-claude >/dev/null 2>&1 || true
claude plugin details ark@ark-claude 2>/dev/null | grep -E "^ark|Skills \(|Hooks \(" || echo "AVISO: 'claude plugin details' não respondeu; confira com 'claude plugin list'"

echo "== 3. seção da ARK no CLAUDE.md"
mkdir -p "$HOME/.claude"
if ! grep -q "Skills: usar, nunca remover" "$CLAUDE_MD" 2>/dev/null; then
  printf '\n' >> "$CLAUDE_MD"; cat "$DIR/CLAUDE-secao-ark.md" >> "$CLAUDE_MD"; echo "  seção adicionada em $CLAUDE_MD"
else
  echo "  já estava"
fi

echo "== 4. python"
if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then echo "  ok"; else echo "  FALTA python3 (Mac: brew install python)"; fi

echo "== 5. teste do roteador"
printf '{"prompt":"monta a proposta pro cliente novo"}' | bash "$DIR/plugins/ark/hooks/run.sh" roteador | head -c 200; echo
echo
echo "Pronto. Feche e abra o Claude Code pra carregar hooks e skills."
