"""UserPromptSubmit: lê o pedido do Gabriel e injeta as skills que casam, pra eu invocar antes de responder.
Camada 1: rotas curadas (rotas.json, vocabulário dele). Camada 2: nome da skill citado literalmente no pedido.
Camada 3: palavras do pedido batendo com a descrição no catálogo (catalogo-skills.json)."""
import json
import os
import re
import sys
import unicodedata

for _f in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8")
    except Exception:
        pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_SKILLS = 6

def normalizar(t):
    t = unicodedata.normalize("NFKD", t or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.lower()

try:
    entrada = json.load(sys.stdin)
except Exception:
    entrada = {}
prompt = entrada.get("prompt") or ""
if not prompt or prompt.startswith("/") or len(prompt.split()) < 3:
    raise SystemExit(0)

p = normalizar(prompt)
achadas = []  # (skill, motivo)
vistas = set()

def add(skill, motivo):
    if skill not in vistas and len(achadas) < MAX_SKILLS:
        vistas.add(skill)
        achadas.append((skill, motivo))

# Camada 1: rotas curadas
try:
    rotas = json.load(open(os.path.join(RAIZ, "rotas.json"), encoding="utf-8"))["rotas"]
except Exception:
    rotas = []
for r in rotas:
    try:
        if re.search(r["gatilho"], p):
            for s in r["skills"][:3]:
                add(s, r.get("quando", ""))
    except re.error:
        continue

# Camadas 2 e 3: catálogo
try:
    catalogo = json.load(open(os.path.join(RAIZ, "catalogo-skills.json"), encoding="utf-8"))
except Exception:
    catalogo = {}

STOP = set("para com uma umas uns dos das que nao não isso esse essa este esta aqui pode vamos faz fazer quero queria como mais menos muito bem tudo todo toda cada sobre pela pelo the and for with this that from into your when use uses used skill skills claude code user ask asks asked".split())
palavras = {w for w in re.findall(r"[a-z0-9][a-z0-9\-]{3,}", p) if w not in STOP}

if len(achadas) < 3 and catalogo:
    pontuadas = []
    for chave, v in catalogo.items():
        nome = v["nome"]
        plug = v.get("plugin", "")
        ref = f"{plug}:{nome}" if plug and plug not in ("ark-claude",) else nome
        if plug == "thedotmack":
            continue  # claude-mem desligado
        if plug == "claude-plugins-official":
            ref = f"{'superpowers' if 'superpowers' in v['caminho'] else 'frontend-design'}:{nome}"
        if plug == "claude-video":
            ref = f"watch:{nome}"
        if plug == "ruflo":
            continue
        # Camada 2: nome citado
        tokens_nome = [t for t in nome.split("-") if len(t) > 3]
        if nome in p or nome.replace("-", " ") in p or (len(tokens_nome) >= 2 and all(t in p for t in tokens_nome)):
            add(ref, "nome citado no pedido")
            continue
        # Camada 3: sobreposição com a descrição
        desc = normalizar(v.get("descricao", ""))
        dwords = set(re.findall(r"[a-z0-9][a-z0-9\-]{3,}", desc))
        inter = palavras & dwords
        if len(inter) >= 3:
            pontuadas.append((len(inter), ref, ", ".join(sorted(inter)[:4])))
    for n, ref, motivo in sorted(pontuadas, reverse=True)[:2]:
        add(ref, f"descrição bate em: {motivo}")

# Processo obrigatório (pipeline superpowers e afins) quando o pedido é construção, bug ou entregável
processo = None
try:
    for pr in json.load(open(os.path.join(RAIZ, "rotas.json"), encoding="utf-8")).get("processos", []):
        if re.search(pr["gatilho"], p):
            processo = pr
            break
except Exception:
    processo = None

if not achadas and not processo:
    raise SystemExit(0)

NL = "\n"
partes = []
if achadas:
    linhas = NL.join(f"  {s_}  ({m})" for s_, m in achadas)
    partes.append("[ark roteador] Skills instaladas que casam com este pedido. Invoque a que se aplica ANTES de responder "
                  "(Gabriel quer as skills usadas; não ignorar):" + NL + linhas)
if processo:
    passos = NL.join(f"  {i}. {t}" for i, t in enumerate(processo["passos"], 1))
    partes.append(f"[ark processo] Pedido de {processo['nome']}. Processo obrigatório, nesta ordem, cada skill invocada de verdade:"
                  + NL + passos + NL +
                  "  Regras acima de tudo: sem traço ou travessão; nada criado automaticamente (tarefa, notificação, cartão); "
                  "nenhum número inventado; entregável é HTML local ou Worker, nunca Artifact; resposta em caveman lite.")
ctx = (NL + NL).join(partes)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": ctx}}, ensure_ascii=False))
