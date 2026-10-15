"""Pergunta ao Gemini sobre um vídeo do YouTube (o Gemini assiste o vídeo nativamente).

Uso: python gemini_video.py <url-youtube> "<pergunta>"
Chave: GEMINI_API_KEY no ambiente ou em ~/.config/watch/.env (gerar em aistudio.google.com/apikey).
Sem chave, sai com código 3 e a skill segue só com /watch + transcrição local.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODELO = os.environ.get("GEMINI_MODELO", "gemini-3.8-flash")


def chave():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    env = Path.home() / ".config" / "watch" / ".env"
    if env.exists():
        for linha in env.read_text(encoding="utf-8").splitlines():
            if linha.strip().startswith("GEMINI_API_KEY="):
                return linha.split("=", 1)[1].strip().strip('"')
    return None


def main():
    if len(sys.argv) < 3:
        sys.exit("uso: gemini_video.py <url-youtube> <pergunta>")
    k = chave()
    if not k:
        print("[gemini] sem GEMINI_API_KEY; gere em aistudio.google.com/apikey e grave em ~/.config/watch/.env", file=sys.stderr)
        sys.exit(3)
    url, pergunta = sys.argv[1], sys.argv[2]
    corpo = {"contents": [{"parts": [{"file_data": {"file_uri": url}}, {"text": pergunta}]}]}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent",
        data=json.dumps(corpo).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": k},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            dados = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"[gemini] HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
    sys.stdout.reconfigure(encoding="utf-8")
    for c in dados.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            print(p.get("text", ""))


if __name__ == "__main__":
    main()
