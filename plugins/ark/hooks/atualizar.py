"""SessionStart: mantém o PC em dia sozinho.
Puxa o ark-claude do GitHub, atualiza o plugin ark e instala o que faltar de skills-equipe.json.
Roda em segundo plano (a sessão abre na hora), no máximo uma vez a cada 6 horas, e nunca remove nada.
O resultado da rodada anterior aparece como aviso no início da sessão seguinte."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8")
    except Exception:
        pass

CASA = Path.home()
ESTADO = CASA / ".claude" / "ark-atualizar.json"
LOG = CASA / ".claude" / "ark-atualizar.log"
INTERVALO = 6 * 3600
WIN = os.name == "nt"
AQUI = Path(__file__).resolve().parent


def ler_estado():
    try:
        return json.loads(ESTADO.read_text(encoding="utf-8"))
    except Exception:
        return {}


def gravar_estado(d):
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    ESTADO.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M ") + msg + "\n")


def rodar(cmd, timeout=600):
    """Roda um comando de texto; no Windows passa pelo shell pra achar claude.cmd e npx.cmd."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        return r.returncode == 0, (r.stdout + r.stderr).strip()[-400:]
    except Exception as e:
        return False, str(e)


def repo_ark():
    for c in (os.environ.get("ARK_CLAUDE_DIR"), CASA / "ark-claude"):
        if c and (Path(c) / ".git").exists():
            return Path(c)
    return None


def plugins_instalados():
    try:
        d = json.loads((CASA / ".claude" / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
        return set((d.get("plugins") or d).keys())
    except Exception:
        return set()


def manifesto(repo):
    for c in ([repo / "plugins" / "ark" / "skills-equipe.json"] if repo else []) + [AQUI.parent / "skills-equipe.json"]:
        if c.exists():
            return json.loads(c.read_text(encoding="utf-8"))
    return {"plugins": [], "skills": []}


def trabalho():
    feito, falhou = [], []
    repo = repo_ark()
    if repo:
        ok, out = rodar(f'git -C "{repo}" pull --ff-only -q', 120)
        log(f"git pull: {'ok' if ok else 'falhou ' + out}")
    if shutil.which("claude"):
        rodar("claude plugin marketplace update ark-claude", 180)
        ok, out = rodar("claude plugin update ark@ark-claude", 180)
        log(f"plugin ark: {out[-120:] if out else ok}")
        tem = plugins_instalados()
        for p in manifesto(repo).get("plugins", []):
            if p["nome"] in tem:
                continue
            rodar(f'claude plugin marketplace add {p["fonte"]}', 300)
            ok, out = rodar(f'claude plugin install {p["nome"]}', 300)
            (feito if ok else falhou).append(p["nome"])
            log(f'{p["nome"]}: {"instalado" if ok else "falhou " + out}')
    if shutil.which("npx"):
        for s in manifesto(repo).get("skills", []):
            if (CASA / ".claude" / "skills" / s["confere"]).exists():
                continue
            ok, out = rodar(f'npx --yes skills@latest add {s["fonte"]} -g --agent claude-code --yes', 600)
            (feito if ok else falhou).append(s["fonte"])
            log(f'{s["fonte"]}: {"instalado" if ok else "falhou " + out}')
    est = ler_estado()
    est.update({"ultima": time.time(), "feito": feito, "falhou": falhou, "rodando": False})
    gravar_estado(est)


def soltar_em_segundo_plano():
    args = [sys.executable, str(Path(__file__).resolve()), "--rodar"]
    kw = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if WIN:
        kw["creationflags"] = 0x00000008 | 0x00000200 | 0x08000000  # DETACHED, NEW_GROUP, NO_WINDOW
    else:
        kw["start_new_session"] = True
    subprocess.Popen(args, **kw)


def main():
    if "--rodar" in sys.argv:
        try:
            trabalho()
        except Exception as e:
            log(f"erro: {e}")
            est = ler_estado()
            est["rodando"] = False
            gravar_estado(est)
        return
    est = ler_estado()
    aviso = ""
    if est.get("feito") or est.get("falhou"):
        partes = []
        if est.get("feito"):
            partes.append("instalado: " + ", ".join(est["feito"]))
        if est.get("falhou"):
            partes.append("falhou: " + ", ".join(est["falhou"]) + f" (detalhe em {LOG})")
        aviso = "[ark atualizar] Na última abertura: " + "; ".join(partes) + ". Avise o Gabriel em uma linha."
        est["feito"], est["falhou"] = [], []
    agora = time.time()
    preso = est.get("rodando") and agora - est.get("inicio", 0) > 3600
    if agora - est.get("ultima", 0) > INTERVALO and (not est.get("rodando") or preso):
        est.update({"rodando": True, "inicio": agora})
        try:
            soltar_em_segundo_plano()
        except Exception as e:
            est["rodando"] = False
            log(f"não consegui soltar: {e}")
    gravar_estado(est)
    if aviso:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": aviso}},
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
