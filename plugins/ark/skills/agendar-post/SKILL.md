---
name: agendar-post
description: Agenda publicação de Reel/post no Instagram da Farmácia Vivenda (ou outro cliente) a partir de um link do Drive. Cria rotina de nuvem que publica sozinha, sem depender do PC ligado.
---

# Agendar Post (Instagram via rotina de nuvem)

## O que este comando faz

Gabriel joga o link do Drive do vídeo editado (ou da pasta da captação), diz dia e hora (ou deixa que eu proponho), e eu:
1. Resolvo o arquivo no Drive e monto a URL pública de download.
2. Escrevo ou recupero a legenda.
3. Crio uma rotina de nuvem (RemoteTrigger) que publica no horário certo via Pipeboard.
4. Confirmo a rotina criada (next_run_at + URL da rotina) e reporto.

A publicação acontece na nuvem da Anthropic + API da Meta. Não depende do PC do Gabriel.

## Constantes (Farmácia Vivenda)

| Campo | Valor |
|---|---|
| instagram_user_id | 17841400421978635 (@farmaciavivenda) |
| account_id | act_1679063009779975 |
| environment_id da rotina | env_011RyGRdo7HaqhxsCx9PubsX |
| Conector MCP | Pipeboard-Meta-Ads, connector_uuid b931795d-4b71-450b-9c3c-31870c9cf9e7, url https://meta-ads.mcp.pipeboard.co |
| Collab da endocrinologista | dramariafernandamelo (só em conteúdo dela) |
| Legendas prontas | Documents\ARK CONTENT\CLIENTES\FARMÁCIA VIVENDA\CONTEUDO\legendas-vivenda-doutora.md |

## Passo a passo

### 1. Resolver o vídeo
- Link de arquivo: extrair o `id` do padrão `drive.google.com/file/d/<id>/view`.
- Link de pasta: listar com `search_files` (`parentId = '<id>'`) e confirmar com Gabriel quais vídeos entram e em que ordem, a menos que ele já tenha dito.
- URL de publicação: `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`
- O arquivo precisa estar compartilhado como "qualquer pessoa com o link". Vídeos enviados pelo editor (_andradedlima@assessorialpha.com) costumam já estar. Se houver dúvida, testar com `curl -sI` e conferir que responde 200/303 sem página de login.

### 2. Legenda
- Se existir legenda pronta no arquivo de legendas, usar exatamente.
- Se não, escrever seguindo a régua do /roteiro: fato simples, sem frase de efeito inventada, sem travessão, fechar com a assinatura `📍 Farmácia Vivenda · Manipulação e Homeopatia · DF e Entorno` + 4 hashtags.
- Salvar a legenda nova no arquivo de legendas antes de agendar.

### 3. Horário
- Se Gabriel não deu horário: propor o padrão da conta (terça ou quarta 11h30, sexta 17h45) e seguir sem esperar resposta se ele pediu pra tocar.
- Converter pra UTC: Brasília + 3h. Ex.: 17h46 local = 20h46Z. Evitar minuto 0 e 30 (usar 11h26, 17h46).

### 4. Criar a rotina (RemoteTrigger action create)

Body do POST:

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

O `<PROMPT>` segue o modelo validado (publicou o post da clínica 17/08 e o do lipedema 19/08):

```
Você é o agente de publicação da ARK Content. Sua única tarefa: publicar AGORA um Reel no Instagram da Farmácia Vivenda usando a ferramenta publish_instagram_media do conector Pipeboard-Meta-Ads (carregue as ferramentas do conector se necessário).

Parâmetros EXATOS da chamada:
- instagram_user_id: 17841400421978635
- account_id: act_1679063009779975
- media_type: REELS
- share_to_feed: true
- collaborators: ["dramariafernandamelo"]   (só se for conteúdo da doutora; senão omitir a linha)
- video_url: <URL do passo 1>
- caption (copie exatamente, com as quebras de linha):

<LEGENDA>

REGRA ANTI-DUPLICATA (importante): se a chamada der timeout ou erro ambíguo, NÃO repita imediatamente. Espere 3 minutos e verifique com get_instagram_posts (instagram_account_id 17841400421978635, account_id act_1679063009779975, time_range last_7d) se um post com essa legenda já apareceu. Só chame publish de novo se tiver certeza de que NÃO saiu. O vídeo tem ~<N>MB e o processamento do container pode demorar alguns minutos: isso é normal.

Ao final, informe o permalink do post publicado como resultado.
```

### 5. Verificar (obrigatório, é o deploy-verificado do agendamento)
- `RemoteTrigger action get` na rotina criada: conferir `enabled: true` e `next_run_at` igual ao horário pedido.
- Reportar pro Gabriel: nome da rotina, horário local, e a URL claude.ai/code/routines que o create retorna.
- No dia seguinte ao disparo (ou quando Gabriel perguntar): `get_instagram_posts` pra confirmar que saiu, e `RemoteTrigger list_runs` se não saiu.

## Armadilhas conhecidas

- `publish_instagram_media` dá timeout no MCP mas PUBLICA. Nunca repetir às cegas, sempre conferir com get_instagram_posts primeiro.
- mLabs é beco sem saída pra vídeo grande: import do Drive falha acima de 100MB e upload da extensão tem teto de 10MB. Não usar.
- Agendamento nativo do Meta Business Suite é alternativa válida quando o Gabriel pedir de dentro do gerenciador, mas o caminho padrão é a rotina de nuvem, que já tem collab e legenda validados por API.
- Rotina one-shot se desativa sozinha depois de disparar (`ended_reason: run_once_fired`). Isso é sinal de sucesso, não de problema.
- Cron local (CronCreate) morre com a sessão. NUNCA usar pra agendamento de post.
