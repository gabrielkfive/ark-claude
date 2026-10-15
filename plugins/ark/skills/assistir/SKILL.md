---
name: assistir
description: Use quando o Gabriel mandar link de vídeo (Instagram Reel, YouTube, TikTok) ou arquivo de vídeo para assistir, entender, transcrever, copiar a ideia ou "aprender com quem já sabe". Assiste quadro a quadro com /watch, transcreve offline com faster-whisper (sem chave, sem custo) e, se houver GEMINI_API_KEY, pergunta ao Gemini direto pelo link do YouTube. Fecha com o que a ARK aplica.
---

# Assistir vídeo e aprender com ele

Pipeline em 3 camadas, como o reel do @_eduardojcruz ensinou (13/10/2026): /watch, Gemini e agentes.

## 1. Quadros (sempre)

```bash
python "$HOME/.claude/plugins/cache/claude-video/watch/0.1.3/scripts/watch.py" "<url>" --no-whisper --max-frames 40
```
Se a versão do plugin mudar, achar o watch.py com Glob em `~/.claude/plugins/cache/claude-video`.
Ler os quadros em paralelo (pode pular de 3 em 3 em vídeo falado). Usar `--resolution 1024` só se precisar ler texto na tela.

## 2. Transcrição local (sempre que tiver fala)

```bash
python "$HOME/.claude/skills/assistir/scripts/transcrever.py" "<work dir>/download/video.mp4" --idioma pt
```
Offline, faster-whisper modelo small em CPU, cerca de 25 s para 1 minuto. Grava `transcricao.txt` ao lado do vídeo. A Whisper API do /watch não é usada (sem chave Groq/OpenAI, e não precisa).

## 3. Gemini (só YouTube, chave ligada, modelo gemini-3.8-flash)

```bash
python "$HOME/.claude/skills/assistir/scripts/gemini_video.py" "<url-youtube>" "<pergunta>"
```
Bom para vídeo longo (aula, palestra) onde quadros ficam esparsos. Saída 3 = sem chave: seguir só com 1 e 2 e avisar em uma linha.

## 4. Entregar

- Resumo do vídeo com timestamps (o que mostra e o que fala).
- O que a ARK aplica: qual cliente, qual skill ou agente executa (roteiro, edicao-cinematografica, carrossel, marketing-farmaceutico...).
- Se o vídeo ensina um método repetível, propor virar skill nova (perguntar antes de criar).
- Apagar o work dir no fim se não houver pergunta de continuação.
