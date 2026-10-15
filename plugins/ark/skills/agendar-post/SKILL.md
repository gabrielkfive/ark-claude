---
name: agendar-post
description: Use quando alguém da ARK (Gabriel, Lucas, Danilo) pedir para postar, publicar ou agendar Reel, carrossel, imagem ou story no Instagram de cliente (Farmácia Vivenda, Ark®, ArkMed ou outro), mandar link do Drive "pra subir", perguntar "saiu o post?", ou quando uma publicação deu timeout. Vale no PC de qualquer sócio.
---

# Agendar post no Instagram

Publicar é ação externa no perfil do cliente. O Claude prepara tudo, mostra o resumo, e só publica ou agenda depois que a pessoa responde ao resumo com uma ordem clara ("publica", "pode postar", "manda", "agenda"). Ordem dada antes do resumo não vale: mostrar o resumo primeiro. Prova de publicado é o **permalink**. Sem permalink, não está no ar.

Pipeboard foi cancelado em 15/10/2026. Não usar, não sugerir upgrade.

## 1. Descobrir em qual cenário este PC está

Rodar antes de qualquer outra coisa:

```powershell
Test-Path "$HOME\Documents\ARK CONTENT\SOFTWARE\ark-publisher\private\client.json"
```

E checar se existe ferramenta Composio de Instagram carregável (`ToolSearch "composio instagram"`).

| Resultado | Cenário | O que dá pra fazer |
|---|---|---|
| `True` | **A. Publisher** (PC do Gabriel) | Agendar em qualquer horário, publica com o PC desligado |
| `False` + Composio com Instagram conectado | **B. Composio próprio** | Publicar agora, de dentro da sessão. Não agenda horário futuro |
| `False` + sem Composio | **C. Só preparar** | Montar o pedido pronto e mandar pro Gabriel agendar |

Nunca criar rotina de nuvem, CronCreate ou lembrete para "agendar" no cenário B ou C. Isso já fez post sumir por 4 dias.

## 2. Preparar (igual nos três cenários)

1. **Conta.** Contas ligadas no publisher: `@farmaciavivenda` (17841400421978635), `@arkcontentt` (17841439432201733), `@assessoriarkmed` (17841426872033704). Cliente fora dessa lista: só o Gabriel conecta (`node link-account.mjs <rotulo>` no publisher). Avisar e seguir preparando.
2. **Mídia.** Link de arquivo do Drive `drive.google.com/file/d/<ID>/view` vira `https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`. Conferir:
   `curl -sI -L --max-time 30 "<url>" | grep -iE "^HTTP|content-length|content-type"`
   Precisa 200 e `video/mp4` ou `image/jpeg`. Se vier `text/html`, o arquivo não está como "qualquer pessoa com o link": parar e pedir para liberar. Link de pasta: listar e confirmar quais arquivos entram e em que ordem.
3. **Formato.** Reel 3 a 180 s (medir com `ffprobe -v error -show_entries format=duration -of csv=p=0 <arquivo>` se houver ffprobe; senão avisar que não foi medido). Carrossel 2 a 10 JPEG. PNG a API recusa: converter com `python -c "from PIL import Image;Image.open('a.png').convert('RGB').save('a.jpg',quality=92)"` e subir o JPEG no Drive com "qualquer pessoa com o link". Story imagem ou vídeo.
4. **Legenda.** Se veio pronta, usar o texto exato; na Vivenda, acrescentar o rodapé descrito a seguir se faltar e mostrar no resumo. Se não veio, escrever: fato simples, sem frase de efeito, sem travessão nem traço separando ideias (vírgula ou ponto). Vivenda fecha com `📍 Farmácia Vivenda · Manipulação e Homeopatia · DF e Entorno` + 4 hashtags. Nunca dar credencial farmacêutica a atendente da Vivenda. Conteúdo da endocrinologista leva collab `dramariafernandamelo`.
5. **Horário.** Calcular a data com comando, nunca de cabeça: `python -c "import datetime as d;print(d.date.today().strftime('%a %d/%m/%Y'))"`. Dia da semana e data não batem ("sexta 17/10" sendo sábado): perguntar qual vale, não escolher. Sem horário dado: terça ou quarta 11h26, sexta 17h46. Sempre com fuso `-03:00`. Evitar minuto 0 e 30.
6. **Mostrar o resumo** (conta, mídia conferida, legenda, horário) e esperar "publica".

## 3A. Cenário Publisher (agendar)

Pasta: `Documents\ARK CONTENT\SOFTWARE\ark-publisher`. Ler o `README.md` dela antes do primeiro uso.

```powershell
python prepare_media.py "<arquivo ou link do Drive>"      # converte 1080p e transcreve
./stage-media.ps1 -PreparedJson "<caminho>\prepared.json" # sobe a mídia, devolve media_url
```

Job JSON: `ig_user_id`, `connected_account_id` (o da mesma conta em `ACCOUNTS` do `wrangler.jsonc` ou num `jobs-*.json` anterior dela), `media_type`, `source_sha256` (do `prepared.json`), `media_url` (do stage-media) ou `media_urls` no carrossel, `caption`, `due_at` com `-03:00`. Exemplo real: `jobs-vivenda-receita-bastidores-1610.json`. Post a menos de 2 h: depois do schedule, `node client.mjs prepare JOB_ID` adianta o processamento (repetir só consulta, não publica).

Depois do "publica":

```powershell
node client.mjs schedule job.json
node client.mjs status
```

Agendado só quando o status mostra o job com o horário, `publish_enabled: true` e heartbeat recente. Depois do horário: estado `published` + `permalink` é a prova. `verifying` = esperar, nunca recriar. `missed`, `failed`, `uncertain` = revisão humana.

Nunca mostrar o conteúdo de `private\`.

## 3B. Cenário Composio próprio (publicar agora)

Depois do "publica", com a conta que a própria pessoa conectou:

1. `INSTAGRAM_CREATE_MEDIA_CONTAINER` (REELS, IMAGE, CAROUSEL ou STORIES, com a URL do passo 2).
2. `INSTAGRAM_GET_POST_STATUS` até `FINISHED` (vídeo leva minutos).
3. `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`.
4. `INSTAGRAM_GET_IG_MEDIA` com o campo `permalink`. Reportar o link.

Timeout em qualquer passo: não repetir. Listar as mídias recentes da conta (ferramenta Composio de mídia do usuário) e procurar a legenda. Achou: reportar o permalink. Não achou em 10 min: dizer "sem permalink, não está no ar" e pedir para a pessoa olhar o perfil no app antes de decidir republicar.

Pediram horário futuro? Explicar que este PC só publica agora e oferecer o cenário C para o Gabriel agendar.

## 3C. Cenário Só preparar (sócio sem publisher)

Aqui nada é publicado, então não precisa de "publica": conferir mídia, legenda e horário e entregar este bloco pronto para a pessoa colar no WhatsApp do Gabriel. Não criar tarefa, cartão nem mensagem por conta própria. Em "Mídia" vai o link original do Drive. "Aprovado por" sem informação: escrever `não informado` e avisar.

```
/agendar-post
Conta: @<conta>
Tipo: <REELS | CAROUSEL | IMAGE | STORIES>
Mídia: <link do Drive> (conferido: 200, <tipo>, <tamanho>)
Horário: <dia> <dd/mm> <hh:mm> (Brasília)
Legenda:
<legenda exata>
Aprovado por: <quem aprovou com o cliente>
```

Aprovação do cliente fica em https://aprova.arkcontent.workers.dev (aprovar com data, aba Calendário).

## Erros comuns

| Situação | Fazer |
|---|---|
| Timeout ao publicar ou agendar | Não repetir. Conferir `node client.mjs status` (A) ou `INSTAGRAM_GET_IG_MEDIA` (B) |
| Modo automático barrou o publish | Pedir "publica" e chamar de novo. Não procurar outro caminho |
| Alguém pede para colar token no chat | Recusar. Credencial vai em mãos |
| "Saiu o post?" | Conferir status ou feed primeiro, responder com permalink |
| Pipeboard aparece como opção | Ignorar. Cancelado em 15/10/2026 |

## Registrar

Se o Ark Brain estiver conectado: `memoria_guardar` (tipo `projeto`, projeto do cliente) com permalink, data e hora.
