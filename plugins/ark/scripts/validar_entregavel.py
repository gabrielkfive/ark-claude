"""Valida um HTML entregável da ARK antes de ser chamado de pronto.
Uso: python validar_entregavel.py caminho/arquivo.html [--final]
Trava (exit 1) em: travessão/linha de desenho, recurso externo (script/css/img/font de fora),
classe CSS começando com "ad", marcador {{...}} ou <!--ARK:...--> solto, "a preencher".
Com --final também exige <title> e nenhum "TODO"/"XXX"."""
import re
import sys

for f in (sys.stdout, sys.stderr):
    try:
        f.reconfigure(encoding="utf-8")
    except Exception:
        pass

if len(sys.argv) < 2:
    print(__doc__); sys.exit(2)
caminho = sys.argv[1]
final = "--final" in sys.argv
html = open(caminho, encoding="utf-8", errors="replace").read()

erros = []
PROIBIDOS = {"—": "travessão", "–": "meio-traço", "―": "barra horizontal", "─": "linha ─", "━": "linha ━", "═": "linha ═"}
for ch, nome in PROIBIDOS.items():
    n = html.count(ch)
    if n:
        linha = next(i for i, l in enumerate(html.splitlines(), 1) if ch in l)
        erros.append(f"{nome} x{n} (primeira na linha {linha})")

ext = re.findall(r'<(?:script|link|img|source)[^>]+(?:src|href)=["\'](https?://[^"\']+)', html, re.I)
ext += re.findall(r'url\(["\']?(https?://[^)"\']+)', html, re.I)
ext = [u for u in ext if "fonts.googleapis.com" not in u and "fonts.gstatic.com" not in u]
if ext:
    erros.append("recurso externo: " + ", ".join(sorted(set(ext))[:5]))

if re.search(r'class=["\'][^"\']*\bad[a-z0-9_-]*', html, re.I):
    erros.append('classe CSS começando com "ad" (bloqueador de anúncio esconde)')

soltos = re.findall(r"\{\{[A-Z_:. \-]+\}\}|<!--ARK:[A-Z]+-->", html)
if soltos:
    erros.append("marcador solto: " + ", ".join(sorted(set(soltos))[:5]))

if re.search(r"a preencher", html, re.I):
    erros.append('campo "a preencher" no texto')

if final:
    if not re.search(r"<title>\s*\S", html, re.I):
        erros.append("sem <title>")
    # TODO/XXX só em maiúscula: "todo dia" e "todo mês" são português, não pendência.
    if re.search(r"\bTODO\b|\bXXX\b", html) or re.search(r"lorem ipsum", html, re.I):
        erros.append("TODO/XXX/lorem ipsum no texto")

if erros:
    print(f"REPROVADO: {caminho}")
    for e in erros:
        print("  x", e)
    sys.exit(1)
print(f"OK: {caminho} ({len(html)//1024} KB)")
