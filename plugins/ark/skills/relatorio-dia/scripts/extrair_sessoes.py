"""Extrai o que aconteceu num dia a partir das sessões do Claude Code desta máquina.
Uso: python extrair_sessoes.py 2026-09-17 [--json]
Lê ~/.claude/projects/*/*.jsonl e usa o timestamp de cada linha (UTC, convertido pra hora local),
então sessão que atravessa a meia-noite entra nos dois dias. Por sessão devolve:
primeiro pedido do usuário, último texto do assistente, arquivos escritos, URLs conferidas
(curl/fetch), comandos de deploy, commits. Resumos de compactação entram como 'compactacao'.
Também lista memórias gravadas no dia. Saída em texto (padrão) ou JSON."""
import glob
import json
import os
import re
import sys
from datetime import datetime, date, timezone

for f in (sys.stdout, sys.stderr):
    try:
        f.reconfigure(encoding="utf-8")
    except Exception:
        pass

if len(sys.argv) < 2:
    print(__doc__); sys.exit(2)
dia = date.fromisoformat(sys.argv[1])
como_json = "--json" in sys.argv
HOME = os.path.expanduser("~")

def no_dia(ts):
    return datetime.fromtimestamp(ts).date() == dia

def linha_no_dia(d):
    ts = d.get("timestamp")
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone().date() == dia
    except Exception:
        return None

sessoes = []
for arq in glob.glob(os.path.join(HOME, ".claude", "projects", "*", "*.jsonl")):
    # filtro barato: arquivo tocado no dia ou depois (uma sessão de ontem pode ter linhas de hoje e vice-versa)
    if datetime.fromtimestamp(os.path.getmtime(arq)).date() < dia:
        continue
    s = {"arquivo": arq, "hora": "", "projeto": os.path.basename(os.path.dirname(arq)), "primeiro_pedido": "", "ultimo_texto": "",
         "arquivos": set(), "urls": set(), "deploys": [], "commits": [], "skills": [], "compactacao": False, "turnos": 0}
    try:
        with open(arq, encoding="utf-8", errors="replace") as f:
            for linha in f:
                try:
                    d = json.loads(linha)
                except Exception:
                    continue
                nd = linha_no_dia(d)
                if nd is False:
                    continue
                if nd and not s["hora"]:
                    s["hora"] = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).astimezone().strftime("%H:%M")
                t = d.get("type")
                msg = d.get("message") or {}
                cont = msg.get("content")
                if t == "user":
                    if isinstance(cont, str):
                        txt = cont
                    elif isinstance(cont, list) and cont and isinstance(cont[0], dict) and cont[0].get("type") == "text":
                        txt = cont[0].get("text", "")
                    else:
                        continue
                    s["turnos"] += 1
                    if "PRIOR-SESSION SUMMARY" in txt or "compact" in txt.lower()[:200]:
                        s["compactacao"] = True
                    if not s["primeiro_pedido"]:
                        s["primeiro_pedido"] = txt.strip()[:220]
                elif t == "assistant" and isinstance(cont, list):
                    for b in cont:
                        if not isinstance(b, dict):
                            continue
                        if b.get("type") == "text" and b.get("text", "").strip():
                            s["ultimo_texto"] = b["text"].strip()[:300]
                        if b.get("type") == "tool_use":
                            nome = b.get("name", "")
                            inp = b.get("input") or {}
                            if nome in ("Write", "Edit") and inp.get("file_path"):
                                s["arquivos"].add(inp["file_path"])
                            if nome == "Skill" and inp.get("skill"):
                                s["skills"].append(inp["skill"])
                            cmd = inp.get("command") or ""
                            if cmd:
                                for u in re.findall(r"https?://[^\s'\"]+", cmd):
                                    if "curl" in cmd or "iwr" in cmd.lower() or "fetch" in cmd:
                                        s["urls"].add(u)
                                if "wrangler deploy" in cmd or "wrangler pages deploy" in cmd:
                                    s["deploys"].append(cmd[:120])
                                m = re.search(r'git commit[^\n]*-m\s+["\']([^"\'\n]{3,80})', cmd)
                                if m:
                                    s["commits"].append(m.group(1))
    except Exception as e:
        s["erro"] = str(e)
    s["arquivos"] = sorted(s["arquivos"]); s["urls"] = sorted(s["urls"])
    if s["turnos"] or s["arquivos"] or s["ultimo_texto"]:
        sessoes.append(s)

sessoes.sort(key=lambda x: x["hora"])

memorias = []
for arq in glob.glob(os.path.join(HOME, ".claude", "projects", "*", "memory", "*.md")):
    if no_dia(os.path.getmtime(arq)) and os.path.basename(arq) != "MEMORY.md":
        txt = open(arq, encoding="utf-8", errors="replace").read()
        m = re.search(r"^description:\s*(.+)$", txt, re.M)
        memorias.append({"arquivo": os.path.basename(arq), "descricao": (m.group(1) if m else "").strip('"')[:200]})

if como_json:
    print(json.dumps({"dia": str(dia), "sessoes": sessoes, "memorias": memorias}, ensure_ascii=False, indent=1))
    sys.exit(0)

print(f"== {dia}: {len(sessoes)} sessões ({sum(1 for s in sessoes if s['compactacao'])} com resumo de compactação), {len(memorias)} memórias ==\n")
for i, s in enumerate(sessoes, 1):
    print(f"[{i}] {s['hora'] or '??:??'} · {s['projeto']} · {s['turnos']} turnos" + (" · COMPACTAÇÃO" if s["compactacao"] else ""))
    print(f"    pedido: {s['primeiro_pedido']}")
    if s["ultimo_texto"]:
        print(f"    último: {s['ultimo_texto'][:200]}")
    if s["skills"]:
        print(f"    skills: {', '.join(dict.fromkeys(s['skills']))}")
    if s["arquivos"]:
        print(f"    arquivos ({len(s['arquivos'])}): " + "; ".join(os.path.basename(a) for a in s["arquivos"][:8]))
    if s["deploys"]:
        print(f"    deploys: {len(s['deploys'])}")
    if s["urls"]:
        print(f"    urls conferidas: " + ", ".join(s["urls"][:4]))
    if s["commits"]:
        print(f"    commits: " + " | ".join(s["commits"][:4]))
    print()
if memorias:
    print("== memórias do dia ==")
    for m in memorias:
        print(f"  {m['arquivo']}: {m['descricao']}")
