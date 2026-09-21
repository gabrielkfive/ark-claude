"""Varre todas as skills instaladas na máquina e gera catalogo-skills.json (nome, origem, descrição).
Rodar: python scripts/gerar_catalogo.py  (dentro de plugins/ark)"""
import json, os, re, sys, glob

HOME = os.path.expanduser("~")
RAIZES = {
    "local": os.path.join(HOME, ".claude", "skills"),
    "plugins": os.path.join(HOME, ".claude", "plugins", "cache"),
    "agents": os.path.join(HOME, ".agents", "skills"),
}
sai = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "catalogo-skills.json")

def frontmatter(caminho):
    try:
        txt = open(caminho, encoding="utf-8", errors="replace").read()
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    fm = m.group(1)
    nome = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+?)(?=\n\w+:|\Z)", fm, re.M | re.S)
    d = desc.group(1).strip() if desc else ""
    d = re.sub(r"^[>|]-?\s*", "", d)
    d = re.sub(r"\s+", " ", d).strip().strip('"').strip("'")
    return (nome.group(1).strip() if nome else os.path.basename(os.path.dirname(caminho))), d

itens = {}
for origem, raiz in RAIZES.items():
    if not os.path.isdir(raiz):
        continue
    padrao = os.path.join(raiz, "**", "SKILL.md") if origem != "local" else os.path.join(raiz, "*", "SKILL.md")
    for f in glob.glob(padrao, recursive=True):
        if origem == "plugins" and ("/docs/" in f.replace("\\", "/") or "/tests/" in f.replace("\\", "/")):
            continue  # traduções e testes do ECC
        r = frontmatter(f)
        if not r:
            continue
        nome, desc = r
        if not desc:
            continue
        plug = ""
        if origem == "plugins":
            rel = os.path.relpath(f, raiz).replace("\\", "/").split("/")
            plug = rel[0]
        chave = f"{plug}:{nome}" if plug else nome
        if chave in itens:
            continue
        itens[chave] = {"nome": nome, "plugin": plug, "descricao": desc[:600], "caminho": f}

json.dump(itens, open(sai, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(f"{len(itens)} skills catalogadas em {sai}")
print(Counter(v['plugin'] or 'local/agents' for v in itens.values()))
