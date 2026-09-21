"""Nega publicação como Artifact. Gabriel não aceita entregável nesse formato.
Leitura, listagem e abertura continuam liberadas."""
from _common import ler_entrada, negar_pre

entrada = ler_entrada()
ti = entrada.get("tool_input") or {}
acao = (ti.get("action") or "publish").lower()
if acao == "publish" and not ti.get("asset"):
    negar_pre("[ark] Artifact bloqueado: Gabriel não aceita entregável como Artifact. "
              "Salvar como HTML local em Documents/ARK CONTENT (pasta do projeto) e/ou subir em Worker próprio (*.arkcontent.workers.dev).")
