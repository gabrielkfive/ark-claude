"""Utilidades compartilhadas pelos hooks da ARK."""
import json
import os
import sys

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Pastas onde a regra de entregável NÃO se aplica (config, memória, código de plugin, scratch).
IGNORAR_TRECHOS = (
    "/.claude/", "\\.claude\\", "/.agents/", "\\.agents\\",
    "/node_modules/", "\\node_modules\\", "/ark-claude/", "\\ark-claude\\",
    "/Temp/claude/", "\\Temp\\claude\\",
)

EXT_ENTREGAVEL = (".html", ".htm", ".md", ".txt")


def ler_entrada():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def caminho_do_arquivo(entrada):
    ti = entrada.get("tool_input") or {}
    return ti.get("file_path") or ti.get("path") or ""


def eh_entregavel(caminho):
    if not caminho:
        return False
    c = caminho.replace("\\", "/")
    if any(t.replace("\\", "/") in c for t in IGNORAR_TRECHOS):
        return False
    return c.lower().endswith(EXT_ENTREGAVEL)


def ler_texto(caminho):
    try:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def avisar(evento, texto):
    """Devolve contexto para o Claude sem bloquear."""
    print(json.dumps({"hookSpecificOutput": {"hookEventName": evento, "additionalContext": texto}}, ensure_ascii=False))
    sys.exit(0)


def bloquear_pos(texto):
    """PostToolUse: exit 2 devolve o stderr ao Claude como erro a corrigir."""
    sys.stderr.write(texto)
    sys.exit(2)


def negar_pre(texto):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": texto}}, ensure_ascii=False))
    sys.exit(0)
