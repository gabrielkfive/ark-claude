"""Stop: se a resposta final diz que algo está "no ar" / "deployado" e nesta rodada
não houve nenhuma conferência de produção (curl ou fetch em *.workers.dev ou domínio próprio),
devolve a rodada para o Claude medir antes de afirmar. Roda uma vez só (stop_hook_active)."""
import json
import re
from _common import ler_entrada

entrada = ler_entrada()
if entrada.get("stop_hook_active"):
    raise SystemExit(0)

ultima = entrada.get("last_assistant_message") or ""
transcript = entrada.get("transcript_path") or ""

AFIRMA = re.compile(r"\b(no ar|deployado|deployei|deploy feito|subiu|está publicad[oa]|publiquei|já está em produção)\b", re.I)
MEDIU = re.compile(r"(curl|Invoke-WebRequest|iwr|wget|fetch\()[^\n]{0,200}(workers\.dev|arkcontent|pages\.dev|https?://)", re.I)

comandos = []
if transcript:
    try:
        with open(transcript, encoding="utf-8", errors="replace") as f:
            linhas = f.readlines()
        # só a rodada atual: do último prompt humano até o fim
        inicio = 0
        for i, l in enumerate(linhas):
            if '"type":"user"' in l or '"type": "user"' in l:
                try:
                    d = json.loads(l)
                    conteudo = d.get("message", {}).get("content")
                    if isinstance(conteudo, str) or (isinstance(conteudo, list) and conteudo and conteudo[0].get("type") == "text"):
                        inicio = i
                except Exception:
                    pass
        for l in linhas[inicio:]:
            if '"tool_use"' not in l:
                continue
            try:
                d = json.loads(l)
            except Exception:
                continue
            for bloco in d.get("message", {}).get("content", []) or []:
                if isinstance(bloco, dict) and bloco.get("type") == "tool_use":
                    inp = bloco.get("input") or {}
                    comandos.append(inp.get("command") or inp.get("url") or "")
            if not ultima and d.get("type") == "assistant":
                for bloco in d.get("message", {}).get("content", []) or []:
                    if isinstance(bloco, dict) and bloco.get("type") == "text":
                        ultima = bloco.get("text", "")
    except Exception:
        pass

if AFIRMA.search(ultima) and not any(MEDIU.search(c or "") for c in comandos):
    print(json.dumps({
        "decision": "block",
        "reason": "[ark] Você afirmou que algo está no ar sem medir a URL de produção nesta rodada. "
                  "Regra do Gabriel: 'pronto' só depois de conferir a URL real (marcador de versão + screenshot se for UI). "
                  "Rode o curl/fetch na URL de produção, confira o marcador, e só então reporte. Se não é deploy, reformule sem 'no ar'."
    }, ensure_ascii=False))
    raise SystemExit(0)
