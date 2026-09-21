"""Avisa quando um HTML entregável carrega biblioteca essencial de CDN externo.
Fontes do Google são toleradas; script/CSS de terceiros que a página precisa para funcionar, não."""
import re
from _common import ler_entrada, caminho_do_arquivo, eh_entregavel, ler_texto, avisar

entrada = ler_entrada()
caminho = caminho_do_arquivo(entrada)
if not eh_entregavel(caminho) or not caminho.lower().endswith((".html", ".htm")):
    raise SystemExit(0)

texto = ler_texto(caminho)
externos = re.findall(r'<(?:script|link)[^>]+(?:src|href)=["\'](https?://[^"\']+)', texto, flags=re.I)
externos = [u for u in externos if "fonts.googleapis.com" not in u and "fonts.gstatic.com" not in u]
if externos:
    lista = "\n".join(f"  {u}" for u in externos[:6])
    avisar("PostToolUse",
           f"[ark] AVISO: {caminho} depende de CDN externo:\n{lista}\n"
           "Regra: página entregável não pode quebrar se o CDN cair ou for bloqueado. "
           "Embutir a biblioteca no arquivo ou servir do próprio Worker. Se for só ícone/decoração, tolerável, mas diga isso ao Gabriel.")
