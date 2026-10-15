"""Transcreve um vídeo local com faster-whisper (offline, sem chave de API).

Uso: python transcrever.py <video> [--modelo small] [--idioma pt]
Saída: linhas "[MM:SS] texto" no stdout e transcricao.txt ao lado do vídeo.
"""
import argparse
import sys
from pathlib import Path

from faster_whisper import WhisperModel


def mmss(s):
    s = int(s)
    return f"{s // 60:02d}:{s % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--idioma", default=None)
    a = ap.parse_args()
    video = Path(a.video)
    modelo = WhisperModel(a.modelo, device="cpu", compute_type="int8")
    segs, info = modelo.transcribe(str(video), language=a.idioma, vad_filter=True)
    linhas = [f"[{mmss(s.start)}] {s.text.strip()}" for s in segs]
    saida = video.with_name("transcricao.txt")
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"# idioma: {info.language} ({info.language_probability:.2f})")
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
