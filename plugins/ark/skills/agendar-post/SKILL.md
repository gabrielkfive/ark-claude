---
name: agendar-post
description: Publica ou agenda Reel/post no Instagram da Farmácia Vivenda (ou outro cliente) a partir de um link do Drive. REGRA DO GABRIEL (21/09/2026): o jeito que funciona é publicar direto pelo conector Pipeboard na sessão, com account_id, esperar o timeout, conferir o feed e reportar o permalink. Rotina de nuvem só pra horário futuro explícito, e sempre com conferência no dia.
---

# Publicar / Agendar Post (Instagram da Vivenda e outros clientes)

## A regra (Gabriel, 21/09/2026: "é assim que você posta, dos outros jeitos não dá certo")

O único caminho que publica de verdade, todas as vezes, é este:

1. `publish_instagram_media` do conector **Pipeboard-Meta-Ads**, chamado **direto da sessão**, com `account_id` preenchido.
2. A chamada **dá timeout** quase sempre. Isso é normal, ela publica mesmo assim.
3. Esperar **3 minutos** (`python -c "import time; time.sleep(180)"`).
4. Conferir com `get_instagram_posts` (`time_range last_7d`) que a legenda apareceu.
5. Só então dizer "no ar", **com o permalink**. Nunca antes.

Nunca repetir o `publish` sem ter conferido o feed. Um timeout não é falha, é espera.

### O que NÃO funciona (já testado, não insistir)

| Caminho | Por que não |
|---|---|
| Rotina de nuvem (RemoteTrigger) como caminho principal | Depende da cota semanal do Pipeboard Free. Em 17/09 a rotina disparou, o Pipeboard recusou ("weekly limit on your Free plan"), o push de aviso passou batido e o post ficou 4 dias sem sair. |
| `publish_instagram_media` sem `account_id` | Erro "Access is restricted to specific ad accounts". O parâmetro não aparece no schema da ferramenta, mas é obrigatório. |
| Repetir o publish depois do timeout | Duplica o post. |
| mLabs | Import do Drive falha acima de 100 MB, upload da extensão tem teto de 10 MB. |
| CronCreate local | Morre com a sessão. |
| Meta Business Suite manual | Só se o Gabriel pedir de dentro do gerenciador; não é o padrão. |

## Constantes (Farmácia Vivenda)

| Campo | Valor |
|---|---|
| instagram_user_id | 17841400421978635 (@farmaciavivenda) |
| account_id (OBRIGATÓRIO no publish) | act_1679063009779975 |
| Conector MCP | Pipeboard-Meta-Ads (connector_uuid b931795d-4b71-450b-9c3c-31870c9cf9e7, url https://meta-ads.mcp.pipeboard.co) |
| environment_id da rotina (só pra agendamento futuro) | env_011RyGRdo7HaqhxsCx9PubsX |
| Collab da endocrinologista | dramariafernandamelo (só em conteúdo dela) |
| Legendas prontas | Documents\ARK CONTENT\CLIENTES\FARMÁCIA VIVENDA\CONTEUDO\legendas-vivenda-doutora.md |

Pra outro cliente: pegar `instagram_user_id` com `get_instagram_accounts` e o `account_id` com `get_ad_accounts` (o conector só aceita contas da lista do login conectado).

## Passo a passo do publish direto (padrão)

### 1. Resolver o vídeo
- Link de arquivo: extrair o `id` do padrão `drive.google.com/file/d/<id>/view`.
- Link de pasta: listar com `search_files` (`parentId = '<id>'`) e confirmar com Gabriel quais vídeos entram e em que ordem, a menos que ele já tenha dito.
- URL de publicação: `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`
- Testar antes: `curl -sI -L --max-time 30 "<url>" | grep -E "^HTTP|Content-Length"`. Precisa responder 200 com `Content-Length` do tamanho do vídeo. Se vier HTML de login, o arquivo não está como "qualquer pessoa com o link".

### 2. Legenda
- Se existir legenda pronta no arquivo de legendas, usar exatamente.
- Se não, escrever seguindo a régua do /roteiro: fato simples, sem frase de efeito inventada, sem travessão, fechar com a assinatura `📍 Farmácia Vivenda · Manipulação e Homeopatia · DF e Entorno` + 4 hashtags.
- Salvar a legenda nova no arquivo de legendas antes de publicar.

### 3. Se a ferramenta ainda não estiver carregada
`ToolSearch select:mcp__claude_ai_Pipeboard_Meta_Ads__publish_instagram_media,mcp__claude_ai_Pipeboard_Meta_Ads__get_instagram_posts`

Se o publish reclamar de roteamento de conta, rodar `get_ad_accounts` uma vez (atualiza o roteamento) e chamar de novo.

### 4. Publicar

```
publish_instagram_media
  instagram_user_id: 17841400421978635
  account_id: act_1679063009779975        <- sem isso não vai
  media_type: REELS
  share_to_feed: true
  collaborators: ["dramariafernandamelo"]  <- só conteúdo da doutora
  video_url: <URL do passo 1>
  caption: <legenda exata, com quebras de linha>
```

Se o modo automático bloquear a chamada (classificador de "transação real"), parar e pedir ao Gabriel um "publica". Com o "publica" dele, chamar de novo. Não procurar outro caminho.

### 5. Timeout, espera e prova

- Timeout = esperado. `python -c "import time; time.sleep(180)"`.
- `get_instagram_posts` (instagram_account_id 17841400421978635, account_id act_1679063009779975, time_range last_7d, limit 3). O post novo aparece no topo com a legenda.
- Reportar: permalink + horário. Se não apareceu em 3 min, esperar mais 3 e conferir de novo. Só repetir o publish se em 10 min não tiver saído.

### 6. Registrar
- `memoria_guardar` no Ark Brain (tipo `projeto`, projeto do cliente) com permalink, data e hora.
- Se veio de uma rotina que falhou, registrar o motivo.

## Agendamento futuro (exceção, só quando o Gabriel der dia e hora)

Quando ele pedir horário futuro, criar a rotina de nuvem, mas com três obrigações novas:

1. **Avisar a cota**: o Pipeboard Free tem limite semanal de comandos. Se já houve publicação via API na semana, dizer isso antes de agendar. Upgrade é decisão dele (pipeboard.co/pricing).
2. **O prompt da rotina precisa levar `account_id`** (o modelo abaixo já leva).
3. **Conferir no dia**: quando o Gabriel abrir sessão depois do horário (ou perguntar "saiu?"), rodar `get_instagram_posts` primeiro. Se não saiu, `RemoteTrigger list_runs` + `get_run_log`, e publicar direto pelo padrão acima. Não esperar ele reclamar.

Horário padrão da conta se ele não der: terça ou quarta 11h26, sexta 17h46. UTC = Brasília + 3h. Evitar minuto 0 e 30.

### Body do POST (RemoteTrigger action create)

```json
{
  "name": "Vivenda · Post <tema> (<dia> <data> <hora>)",
  "run_once_at": "<ISO UTC>",
  "job_config": {"ccr": {
    "environment_id": "env_011RyGRdo7HaqhxsCx9PubsX",
    "events": [{"data": {"message": {"content": "<PROMPT>", "role": "user"}, "parent_tool_use_id": null, "session_id": "", "type": "user", "uuid": "<uuid novo>"}}],
    "session_context": {"allowed_tools": ["preset:default","Task","Bash","Glob","Grep","Read","Edit","MultiEdit","Write","NotebookEdit","WebFetch","TodoWrite","WebSearch","BashOutput","KillBash","Skill","Tmux","Monitor","SendUserFile","REPL"], "model": "claude-sonnet-5"}
  }},
  "mcp_connections": [{"clear_tool_policy_overrides": false, "connector_uuid": "b931795d-4b71-450b-9c3c-31870c9cf9e7", "name": "Pipeboard-Meta-Ads", "permitted_tools": [], "tool_policy_overrides": [], "url": "https://meta-ads.mcp.pipeboard.co"}]
}
```

### Prompt da rotina

```
Você é o agente de publicação da ARK Content. Sua única tarefa: publicar AGORA um Reel no Instagram da Farmácia Vivenda usando a ferramenta publish_instagram_media do conector Pipeboard-Meta-Ads (carregue as ferramentas do conector se necessário).

Parâmetros EXATOS da chamada (account_id é obrigatório, sem ele a API recusa):
- instagram_user_id: 17841400421978635
- account_id: act_1679063009779975
- media_type: REELS
- share_to_feed: true
- collaborators: ["dramariafernandamelo"]   (só se for conteúdo da doutora; senão omitir a linha)
- video_url: <URL do passo 1>
- caption (copie exatamente, com as quebras de linha):

<LEGENDA>

REGRA ANTI-DUPLICATA: se a chamada der timeout, NÃO repita. Espere 3 minutos e verifique com get_instagram_posts (instagram_account_id 17841400421978635, account_id act_1679063009779975, time_range last_7d) se um post com essa legenda já apareceu. Só chame publish de novo se tiver certeza de que NÃO saiu. O vídeo tem ~<N>MB e o processamento pode demorar alguns minutos.

Se a resposta for erro de cota do Pipeboard ("weekly limit", "trial commands"), NÃO tente de novo. Envie PushNotification com o texto "POST DA VIVENDA NÃO SAIU: cota do Pipeboard. Publicar manual." e encerre.

Ao final, informe o permalink do post publicado como resultado.
```

### Verificar a rotina criada
- `RemoteTrigger action get`: `enabled: true` e `next_run_at` igual ao horário pedido.
- Reportar nome, horário local e a URL claude.ai/code/routines.
- Rotina one-shot se desativa sozinha depois de disparar (`ended_reason: run_once_fired`). Isso NÃO prova que publicou. Só o feed prova.

## Histórico que sustenta a regra
- 17/08 e 19/08: rotina publicou (clínica, lipedema). Funcionava enquanto a cota do Pipeboard sobrava.
- 10/09 a 14/09: 5 rotinas publicaram (Café com Nutri 1 a 3, Dra. Maria Fernanda, Semana do Consumidor).
- 17/09: rotina Café com Nutri 4 (Lara Freire) falhou por cota. Ninguém viu. Publicado manual em 21/09 12h46, permalink https://www.instagram.com/reel/Ddjg2rZjeBH/. Gabriel fixou a regra nesse dia.
