"""Meta Ads + Instagram sem Pipeboard, com token de usuario do sistema do BM.

O token fica fora do repositorio, em ~/.config/ark/meta-token.txt (uma linha).

  python meta.py ligar                 confere o token, lista contas e troca o MCP meta-ads
  python meta.py contas                contas de anuncio e perfis de Instagram que o token enxerga
  python meta.py posts <perfil> [dias] posts organicos com alcance (perfil = @usuario ou id)
  python meta.py reel <perfil> <video.mp4> <legenda.txt>   publica Reel e devolve o permalink
"""
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VERSAO = os.environ.get("META_GRAPH_VERSION", "v23.0")
GRAPH = f"https://graph.facebook.com/{VERSAO}"
PASTA = Path.home() / ".config" / "ark"
TOKEN_ARQ = PASTA / "meta-token.txt"
CONTAS_ARQ = PASTA / "meta-contas.json"


def token():
    if not TOKEN_ARQ.exists():
        sys.exit(f"Falta o token. Cole numa linha so em {TOKEN_ARQ}")
    t = TOKEN_ARQ.read_text(encoding="utf-8").strip()
    if len(t) < 20:
        sys.exit(f"Token em {TOKEN_ARQ} parece incompleto.")
    return t


def chamar(caminho, params=None, metodo="GET", dados=None, cabecalhos=None, url=None):
    params = dict(params or {})
    if url is None:
        params["access_token"] = token()
        url = f"{GRAPH}/{caminho.lstrip('/')}?{urllib.parse.urlencode(params)}"
    corpo = dados
    if isinstance(dados, dict):
        corpo = urllib.parse.urlencode(dados).encode()
    req = urllib.request.Request(url, data=corpo, method=metodo, headers=cabecalhos or {})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        erro = e.read().decode(errors="replace")
        try:
            erro = json.loads(erro)["error"]["message"]
        except Exception:
            pass
        sys.exit(f"Meta recusou ({e.code}): {erro}")


def paginar(caminho, params):
    saida = chamar(caminho, params)
    itens = list(saida.get("data", []))
    while saida.get("paging", {}).get("next"):
        saida = chamar("", url=saida["paging"]["next"])
        itens += saida.get("data", [])
    return itens


def levantar_contas():
    eu = chamar("me", {"fields": "id,name"})
    anuncios = paginar("me/adaccounts", {"fields": "name,account_id,account_status,currency", "limit": 200})
    paginas = paginar("me/accounts", {"fields": "name,instagram_business_account{id,username}", "limit": 200})
    perfis = []
    for p in paginas:
        ig = p.get("instagram_business_account")
        if ig:
            perfis.append({"username": ig.get("username"), "ig_id": ig["id"], "pagina": p["name"]})
    dados = {"usuario": eu, "anuncios": anuncios, "instagram": perfis, "atualizado": time.strftime("%Y-%m-%d %H:%M")}
    PASTA.mkdir(parents=True, exist_ok=True)
    CONTAS_ARQ.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return dados


def mostrar(dados):
    print(f"Usuario do token: {dados['usuario'].get('name')} ({dados['usuario'].get('id')})")
    print(f"\nContas de anuncio: {len(dados['anuncios'])}")
    for a in dados["anuncios"]:
        status = "ativa" if a.get("account_status") == 1 else f"status {a.get('account_status')}"
        print(f"  act_{a['account_id']}  {a.get('name')}  ({status})")
    print(f"\nPerfis de Instagram: {len(dados['instagram'])}")
    for p in dados["instagram"]:
        print(f"  @{p['username']}  {p['ig_id']}  pagina {p['pagina']}")


def trocar_mcp():
    claude = shutil.which("claude")
    if not claude:
        print("\nNao achei o comando claude; o MCP meta-ads nao foi trocado.")
        return
    subprocess.run([claude, "mcp", "remove", "meta-ads", "-s", "user"], capture_output=True)
    r = subprocess.run(
        [claude, "mcp", "add", "meta-ads", "-s", "user",
         "-e", f"META_ACCESS_TOKEN={token()}", "-e", "PYTHONUTF8=1", "-e", "PYTHONIOENCODING=utf-8",
         "--", "uvx", "meta-ads-mcp"],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"Falha ao trocar o MCP: {r.stderr.strip()}")
    print("\nMCP meta-ads agora usa o token proprio (sem Pipeboard). Vale na proxima sessao do Claude.")


def perfil_id(perfil):
    if perfil.isdigit():
        return perfil
    nome = perfil.lstrip("@").lower()
    dados = json.loads(CONTAS_ARQ.read_text(encoding="utf-8")) if CONTAS_ARQ.exists() else levantar_contas()
    for p in dados["instagram"]:
        if (p["username"] or "").lower() == nome:
            return p["ig_id"]
    dados = levantar_contas()
    for p in dados["instagram"]:
        if (p["username"] or "").lower() == nome:
            return p["ig_id"]
    sys.exit(f"@{nome} nao aparece para este token. Adicione a pagina ao usuario do sistema no BM.")


def posts(perfil, dias=90):
    ig = perfil_id(perfil)
    desde = int(time.time()) - int(dias) * 86400
    itens = paginar(f"{ig}/media", {
        "fields": "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count",
        "since": desde, "limit": 100})
    for m in itens:
        metrica = "views" if m.get("media_product_type") == "REELS" else "reach"
        try:
            ins = chamar(f"{m['id']}/insights", {"metric": f"reach,{metrica}" if metrica != "reach" else "reach"})
            m["insights"] = {i["name"]: i["values"][0]["value"] for i in ins.get("data", [])}
        except SystemExit:
            m["insights"] = {}
    itens.sort(key=lambda m: m["insights"].get("reach", 0), reverse=True)
    print(json.dumps(itens, ensure_ascii=False, indent=2))


def reel(perfil, video, legenda_arq):
    ig = perfil_id(perfil)
    video = Path(video)
    legenda = Path(legenda_arq).read_text(encoding="utf-8").strip()
    cont = chamar(f"{ig}/media", metodo="POST", dados={
        "media_type": "REELS", "upload_type": "resumable", "caption": legenda,
        "share_to_feed": "true", "access_token": token()}, url=f"{GRAPH}/{ig}/media")
    cid, uri = cont["id"], cont["uri"]
    bruto = video.read_bytes()
    chamar("", metodo="POST", dados=bruto, url=uri, cabecalhos={
        "Authorization": f"OAuth {token()}", "offset": "0", "file_size": str(len(bruto))})
    for _ in range(60):
        st = chamar(cid, {"fields": "status_code,status"})
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            sys.exit(f"Meta nao processou o video: {st.get('status')}")
        time.sleep(10)
    else:
        sys.exit("Video ainda processando depois de 10 minutos; nada foi publicado.")
    pub = chamar(f"{ig}/media_publish", metodo="POST", dados={"creation_id": cid, "access_token": token()},
                 url=f"{GRAPH}/{ig}/media_publish")
    link = chamar(pub["id"], {"fields": "permalink"}).get("permalink")
    print(json.dumps({"media_id": pub["id"], "permalink": link}, ensure_ascii=False))


def main(args):
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "ligar":
        mostrar(levantar_contas())
        trocar_mcp()
    elif cmd == "contas":
        mostrar(levantar_contas())
    elif cmd == "posts" and len(args) >= 2:
        posts(args[1], args[2] if len(args) > 2 else 90)
    elif cmd == "reel" and len(args) == 4:
        reel(args[1], args[2], args[3])
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
