---
name: carrossel
description: Gera carrossel de Instagram pra ARK (@arkcontentt) ou cliente em lâminas 1080x1350 na identidade ARK (foto real + véu, kicker amarelo, Sora com uma palavra amarela, Inter no corpo, CTA WhatsApp) usando o gerador gerar.py + spec.py com Playwright no Chrome. Use quando o Gabriel pedir carrossel, "post em lâminas", "caso real pro Instagram", "conteúdo institucional da ARK", ou quando o perfil da ARK estiver sem post. Não use para Reel ou vídeo (roteiro) nem legenda solta.
---

# Carrossel ARK

Regras que vieram de feedback e não mudam: **post da ARK é conceitual, não relatório** (ensina uma ideia com um caso real, não lista o que foi entregue); **sempre mostra material real** com nome do cliente; sem traço ou travessão; amarelo em uma palavra do título; CTA com o WhatsApp do Saulo `5561995506006`.

Gerador e três carrosséis aprovados (Café, Nutrição Brasil, Novo Gama): `Documents/ARK CONTENT/CLIENTES/ARK INSTITUCIONAL/CARROSSEIS/2026-09/`.

## Checklist

```
- [ ] 1. Escolher o caso real e o conceito (uma ideia por carrossel)
- [ ] 2. Extrair quadros dos vídeos pra _fotos/
- [ ] 3. Escrever a entrada no spec.py (7 lâminas)
- [ ] 4. python gerar.py <slug> e conferir os PNG
- [ ] 5. Legenda em legendas.md + preview.html
- [ ] 6. Entregar pasta; agendar só se ele pedir (agendar-post)
```

## 1. Conceito

Estrutura que funcionou nos três: capa (a ideia em uma frase), o erro comum, o que a gente fez, quem/o que virou conteúdo, a regra, o calendário ou os números, CTA. Sete lâminas, formato 4:5. O caso é sempre trabalho real já publicado (ver acervo em [[ark-acervo-instagram-portfolio]]); se a lâmina cita data de publicação futura, o carrossel espera a data passar.

## 2. Fotos

Quadros dos próprios Reels: `ffmpeg -ss <t> -i <video> -frames:v 1 _fotos/<nome>.jpg`. Legenda queimada no vídeo se corta com `pos` (object-position) na lâmina, nunca editando a foto.

## 3. spec.py

Uma chave por carrossel: `"04-<slug>": {"kicker": "Caso real · <Cliente>", "slides": [...]}`. Tipos de lâmina: `capa`, `foto`, `lista` (itens com `<small>`), `passos`, `cta`. Campos: `foto`, `pos`, `veu` ("forte" quando o texto fica em cima de área clara), `kicker`, `titulo` (`<em>` = amarelo, uma palavra), `corpo`, `h1class: "m"` pra título médio. Modelo completo: as entradas `01-cafe`, `02-feira` e `03-inauguracao` no mesmo arquivo.

## 4. Gerar

```bash
cd "Documents/ARK CONTENT/CLIENTES/ARK INSTITUCIONAL/CARROSSEIS/<AAAA-MM>"
python gerar.py 04-<slug>
```

Usa `chromium.launch(channel="chrome")` porque o chromium do Playwright não está instalado neste PC; fontes de `MARCAS/ARK/ark-fontes-embutidas.css`. Abrir os 7 PNG e conferir: texto não corta, foto não mostra legenda queimada, amarelo só onde deve. Mês novo = copiar `gerar.py`, `spec.py` e `preview.html` pra pasta `<AAAA-MM>` nova.

## 5 e 6. Entrega

`legendas.md` com a legenda de cada carrossel (mesmo tom das aprovadas, sem frase de efeito), `preview.html` atualizado, `LEIA-ME.md` com ordem sugerida de publicação e pendências. Publicação ou agendamento é ação externa: só com pedido dele, via skill agendar-post.
