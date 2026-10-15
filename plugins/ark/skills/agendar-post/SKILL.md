---
name: agendar-post
description: Use quando alguém da ARK (Gabriel, Lucas, Danilo) pedir para postar, publicar ou agendar Reel, carrossel, imagem ou story no Instagram de cliente (Farmácia Vivenda, Ark®, ArkMed ou outro), mandar link do Drive "pra subir", perguntar "saiu o post?", ou quando uma publicação deu timeout. Vale no PC de qualquer sócio.
---

# Agendar post no Instagram

Publicar é ação externa no perfil do cliente. O Claude prepara tudo, mostra o resumo, e só publica ou agenda depois que a pessoa responde ao resumo com uma ordem clara ("publica", "pode postar", "manda", "agenda"). Ordem dada antes do resumo não vale: mostrar o resumo primeiro. Prova de publicado é o **permalink**. Sem permalink, não está no ar.

**Ordem dos caminhos (regra do Gabriel, 15/10/2026): agendar é pelo Composio. Pipeboard é sempre a segunda opção.**

1. **Composio pelo publisher da ARK** (agenda qualquer dia e hora, sai com o PC desligado). Worker `ark-publisher` com cron, publica pela conexão Composio do Gabriel. Qualquer PC com o arquivo de acesso agenda.
2. **Composio direto na sessão** (publica agora, não agenda). Quando não há acesso ao publisher mas há Instagram conectado num Composio da pessoa.
3. **Pipeboard** (segunda opção). Só se o Composio falhar ou não estiver disponível e o conector Pipeboard responder.
4. **Bloco pro Gabriel.** Nenhum dos três disponível neste PC.

## 1. Descobrir o que este PC tem

```powershell
node "<pasta desta skill>\publisher.mjs" status
```

Resposta com `publish_enabled` = acesso ao publisher (caminho 1). "Sem acesso ao publisher" = não tem. O arquivo de acesso fica em `Documents\ARK CONTENT\SOFTWARE\ark-publisher\private\client.json` (PC do Gabriel) ou `%USERPROFILE%\.ark\publisher.json` (sócios; o Gabriel entrega em mãos, nunca por chat).

Sem publisher: `ToolSearch "composio instagram"` (caminho 2), depois `ToolSearch "pipeboard instagram"` (caminho 3).

Nunca criar rotina de nuvem, CronCreate ou lembrete para "agendar". Isso já fez post sumir por 4 dias.

## 2. Preparar (igual em todos os caminhos)

1. **Conta.** Contas ligadas no publisher: `@farmaciavivenda` (17841400421978635), `@arkcontentt` (17841439432201733), `@assessoriarkmed` (17841426872033704). Cliente fora dessa lista: só o Gabriel conecta (`node link-account.mjs <rotulo>` no publisher). Avisar e seguir preparando.
2. **Mídia.** Link de arquivo do Drive `drive.google.com/file/d/<ID>/view` vira `https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`. Conferir:
   `curl.exe -sI -L --max-time 30 "<url>"` (no PowerShell use `curl.exe`; na ferramenta Bash, `curl`) e ler `HTTP`, `content-type` e `content-length`.
   Precisa 200 e `video/mp4` ou `image/jpeg`. Se vier `text/html`, o arquivo não está como "qualquer pessoa com o link": parar e pedir para liberar. Link de pasta: listar e confirmar quais arquivos entram e em que ordem.
3. **Formato.** Reel 3 a 180 s (medir com `ffprobe -v error -show_entries format=duration -of csv=p=0 <arquivo>` se houver ffprobe; senão avisar que não foi medido). Carrossel 2 a 10 JPEG. PNG a API recusa: converter com `python -c "from PIL import Image;Image.open('a.png').convert('RGB').save('a.jpg',quality=92)"` e pedir para a pessoa subir o JPEG no Drive com "qualquer pessoa com o link". Story imagem ou vídeo.
4. **Legenda.** Se veio pronta, usar o texto exato; na Vivenda, acrescentar o rodapé descrito a seguir se faltar e mostrar no resumo. Se não veio, escrever: fato simples, sem frase de efeito, sem travessão nem traço separando ideias (vírgula ou ponto). Vivenda fecha com `📍 Farmácia Vivenda · Manipulação e Homeopatia · DF e Entorno` + 4 hashtags. Nunca dar credencial farmacêutica a atendente da Vivenda. Conteúdo da endocrinologista pede collab `dramariafernandamelo`, mas nenhum caminho envia collab: avisar no resumo que o convite é feito à mão no app depois de publicar.
5. **Horário.** Calcular a data com comando, nunca de cabeça: `python -c "import datetime as d;print(d.date.today(), d.date(2026,10,17).isoweekday())"` com a data pedida (1 = segunda, 5 = sexta, 6 = sábado). Dia da semana e data não batem ("sexta 17/10" sendo sábado): perguntar qual vale, não escolher. Sem horário dado: terça ou quarta 11h26, sexta 17h46. Sempre com fuso `-03:00`. Evitar minuto 0 e 30.
6. **Mostrar o resumo** (caminho escolhido, conta, mídia conferida, legenda, horário) e esperar "publica".

## 3A. Composio pelo publisher (agendar)

Comandos com `node "<pasta desta skill>\publisher.mjs"` (abaixo, só `publisher.mjs`). Nunca mostrar o conteúdo do arquivo de acesso.

**Antes de tudo:** `publisher.mjs status` e procurar job da mesma peça (mesma legenda ou mesmo `source_sha256`). Existe, mesmo com outro horário? Não criar outro: refazer o resumo com o aviso e perguntar qual horário vale. Trocar horário exige cancelar o job antigo no D1 (seção Incidente do README do publisher), decisão do Gabriel. A chave anti-duplicata é conta + `source_sha256` + horário: reenviar o mesmo JSON é seguro, mudar o horário cria um segundo post.

**Mídia, de qualquer PC:**
- Reel e story em vídeo: `media_url` = link de download do Drive (passo 2). `source_sha256`: `publisher.mjs hash "<link de download>"` (baixa e calcula; recusa link privado).
- Carrossel: `media_urls` = links de download dos JPEG na ordem, `media_url` = o primeiro, `source_sha256` = hash do primeiro.
- Imagem única e story em imagem: o publisher exige URL terminada em `.jpg`, e link do Drive não termina assim. Usar o fluxo de mídia hospedada abaixo (só PC do Gabriel) ou publicar agora pelo 3B.

**Mídia hospedada no publisher (só PC do Gabriel, pasta `Documents\ARK CONTENT\SOFTWARE\ark-publisher`):** vídeo com `python prepare_media.py "<arquivo ou link>"` e `./stage-media.ps1 -PreparedJson "<prepared.json>"`; JPEG copiado para `assets\media\<sha>.jpg` e `wrangler deploy`, conferindo `curl.exe -sI` 200 em `https://ark-publisher.arkcontent.workers.dev/media/<sha>.jpg`. Isso faz deploy de produção do publisher: só com a pasta igual ao que está no ar.

**Job JSON** (um objeto só por arquivo): `ig_user_id`, `media_type` (`REELS`, `IMAGE`, `CAROUSEL`, `STORIES`), `media_url`, `media_urls` (só carrossel, 2 a 10), `source_sha256`, `caption`, `due_at` com `-03:00`. Exemplos reais na pasta do publisher: `jobs-vivenda-receita-bastidores-1610.json` (Reel), `jobs-ark-news-meta-one.json` (carrossel).

Depois da ordem: `publisher.mjs schedule job.json` e `publisher.mjs status`.

Agendado só quando o status mostra o job com o horário, `publish_enabled: true` e heartbeat recente. Post a menos de 2 h: `publisher.mjs prepare JOB_ID` adianta o processamento (repetir só consulta, não publica). Depois do horário: `published` + `permalink` é a prova. `verifying` = esperar, nunca recriar. `missed`, `failed`, `uncertain` = revisão humana, e aí vale o Pipeboard (3C) depois de conferir no feed que não saiu.

## 3B. Composio direto (publicar agora)

1. `INSTAGRAM_GET_USER_INFO` (ig_user_id `me`, campo `username`). O @ tem que ser o do resumo. Não bateu: parar e oferecer o bloco pro Gabriel (3D).
2. Depois da ordem, criar a mídia:
   - Reel: `INSTAGRAM_POST_IG_USER_MEDIA` com `media_type: REELS`, `video_url`, `caption`, `share_to_feed: true`.
   - Imagem ou story: `INSTAGRAM_CREATE_MEDIA_CONTAINER` (`image_url` ou `video_url`; story com `media_type: STORIES`). A URL é o link de download do Drive do passo 2.
   - Carrossel: um `INSTAGRAM_CREATE_MEDIA_CONTAINER` por JPEG com `is_carousel_item: true`, depois `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` com `children` e `caption`.
3. `INSTAGRAM_GET_POST_STATUS` até `FINISHED` (vídeo leva minutos).
4. `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` com o id do container.
5. `INSTAGRAM_GET_IG_MEDIA` com o campo `permalink`. Reportar o link.

Timeout em qualquer passo: não repetir. `INSTAGRAM_GET_IG_USER_MEDIA` da conta e procurar a legenda; story não tem legenda, procurar `media_product_type` STORY com horário dos últimos minutos. Achou: reportar o permalink. Não achou em 10 min: dizer "sem permalink, não está no ar" e pedir para a pessoa olhar o perfil no app antes de decidir republicar.

Pediram horário futuro? Composio direto só publica agora: pedir o acesso ao publisher ao Gabriel ou entregar o bloco 3D.

## 3C. Pipeboard (segunda opção)

Só quando o Composio falhou ou não existe neste PC, e o conector Pipeboard responde. Plano pago limita contas: se recusar por conta ou cota, não sugerir upgrade; ir pro 3D.

1. `ToolSearch select:mcp__claude_ai_Pipeboard_Meta_Ads__publish_instagram_media,mcp__claude_ai_Pipeboard_Meta_Ads__get_instagram_posts`
2. Depois da ordem, `publish_instagram_media` com `instagram_user_id`, `account_id` (obrigatório, não aparece no schema; Vivenda `act_1679063009779975`; outra conta: `get_ad_accounts`), `media_type`, `video_url` ou `image_url`, `caption`, `share_to_feed: true`.
3. Timeout é normal: esperar 3 min (`python -c "import time; time.sleep(180)"`) e conferir com `get_instagram_posts` (`time_range last_7d`). Nunca repetir o publish antes de conferir.
4. Reportar o permalink.

Publica agora; não agenda. Pedido com horário futuro e só Pipeboard no PC: bloco 3D. Trocar de caminho (Composio para Pipeboard) exige resumo novo e ordem nova.

## 3D. Bloco pro Gabriel (nada disponível neste PC)

Aqui nada é publicado, então não precisa de "publica": conferir mídia, legenda e horário e entregar este bloco pronto para a pessoa colar no WhatsApp do Gabriel. Não criar tarefa, cartão nem mensagem por conta própria. Em "Mídia" vai o link original do Drive. "Aprovado por" sem informação: escrever `não informado` e avisar.

```
/agendar-post
Conta: @<conta>
Tipo: <REELS | CAROUSEL | IMAGE | STORIES>
Mídia: <link do Drive> (conferido: 200, <tipo>, <tamanho>)
Horário: <dia> <dd/mm> <hh:mm> (Brasília)
Legenda:
<legenda exata, ou "sem legenda" em story>
Aprovado por: <quem aprovou com o cliente>
```

Aprovação do cliente fica em https://aprova.arkcontent.workers.dev (aprovar com data, aba Calendário).

## Erros comuns

| Situação | Fazer |
|---|---|
| Timeout ao publicar ou agendar | Não repetir nem mudar horário. Conferir `publisher.mjs status` (3A), `INSTAGRAM_GET_IG_USER_MEDIA` (3B) ou `get_instagram_posts` (3C) |
| Modo automático barrou o publish | Pedir "publica" e chamar de novo. Não procurar outro caminho |
| Alguém pede para colar token no chat | Recusar. Credencial vai em mãos |
| "Saiu o post?" | Conferir status ou feed primeiro, responder com permalink |
| Composio falhou (publisher fora, `publish_enabled: false`, job `failed`) | Avisar e ir pro Pipeboard (3C). Nunca nos dois ao mesmo tempo para a mesma peça |

## Registrar

Se o Ark Brain estiver conectado: `memoria_guardar` (tipo `projeto`, projeto do cliente) com permalink, data e hora.
