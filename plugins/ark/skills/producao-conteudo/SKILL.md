---
name: producao-conteudo
description: Use quando o Gabriel pedir o conteúdo do mês de um cliente, "monta a produção do <cliente>", "pauta do mês", "plano de conteúdo", "o que a gente grava e posta em <mês>", ou quando uma captação foi marcada e precisa de roteiros, legendas e agendamento. É o pipeline completo da ARK, do brief até o post publicado, com fila de aprovação humana em cada passagem.
---

> **Aviso 15/10/2026: Pipeboard em cancelamento.** O Gabriel cancelou o teste do Pipeboard (o pago limita a 3 contas). Enquanto o conector responder, segue valendo o que está abaixo. Se ele cair: anúncios e métricas pelo `meta-ads-mcp` local (`mcp__meta-ads__*`) com token próprio do Business Manager; o pacote aberto NÃO tem `publish_instagram_media` nem `get_instagram_posts`, então publicação e posts orgânicos vão direto pela Instagram Graph API com o mesmo token. Google Ads: MCP oficial do Google, depende do developer token da MCC.

# Produção de conteúdo, ponta a ponta

Pipeline em 7 estações. Cada estação tem quem faz, com qual ferramenta, e o que prova
que terminou. Nada é publicado sem aprovação do Gabriel ou do decisor do cliente.

```
Brief > Plano do mês > Roteiros > Captação > Edição > Legendas e aprovação > Publicação
```

## Defaults (não perguntar, assumir e dizer no relatório)

- Período: o próximo mês fechado se hoje for depois do dia 20, senão o mês atual.
- Volume: o do plano contratado (Silver 10 vídeos, Gold 15, Plano X 20). Se não souber,
  8 peças.
- Mix padrão: 60% Reels 30 a 60 s, 25% carrossel, 15% stories ou bastidor.
- Praça e tom vêm do brief. Sem brief, rodar primeiro a skill `briefing-cliente`.

## Estação 1: brief e dados reais

1. Ler o brief em `src/integrations/clientes.ts` (ou `docs/clientes/<slug>.md`).
2. O que performou: Pipeboard `get_instagram_posts` com `time_range last_90d` na conta do
   cliente (IDs conhecidos na memória; Vivenda é 17841400421978635 com
   act_1679063009779975). Separar top 5 por alcance e por salvamentos.
3. Se o cliente tem tráfego: `get_insights` do Meta e `get_google_ads_campaign_metrics`
   dos últimos 30 dias, só para saber qual ângulo converteu.
4. Datas do mês: feriados, datas comemorativas do segmento, eventos do cliente (Tactiq
   `search_meetings` pelo nome do cliente, últimos 45 dias).

## Estação 2: plano do mês

Uma tabela com N linhas (N = volume): data de publicação, formato, pilar, gancho em uma
frase, objetivo (alcance, salvamento, conversa no WhatsApp), captação de origem (qual dia
de gravação), responsável pela edição. Regras:

- Ideia original por mês. Repetir o mês anterior é falha grave (memória
  feedback-gabriel-ideias-originais).
- Tudo que entra tem que ser gravável com a equipe real na captação marcada (memória
  feedback-roteiro-viabilidade-operacional).
- Salvar em `CLIENTES\<CLIENTE>\PLANEJAMENTO\<AAAA-MM>\plano-de-conteudo.md`.

## Estação 3: roteiros

Rodar a skill `roteiro` no modo conteúdo, uma peça por linha do plano que for vídeo.
Falas literais entre aspas, lugar e cena, duração alvo. Salvar em
`CLIENTES\<CLIENTE>\ROTEIROS\<AAAA-MM>\` com um arquivo por peça e um índice. Para banco
de takes de captação, usar o modo captação (memória feedback-captacao-volume-linguagem-simples).

## Estação 4: captação (a equipe grava)

Criar no WorkFlowArk uma tarefa por dia de captação com MCP `W` `create_task`:
`title` "Captação <cliente> <data>: <N> roteiros", `resp` Omar (ou quem o brief indicar),
`funcao` "Captação", `clienteId` slug, `data` no formato AAAA-MM-DD, `prio` alta. O link
dos roteiros vai no título. A página Produção do sistema gera as tarefas de edição quando
o produtor conclui o checklist, não duplicar.

## Estação 5: edição

Material bruto chega no Drive (skill `organizar-drive` sabe as pastas). Editar pela skill
`edicao-cinematografica` (baixar, escolher takes, look, legenda, mix, render). Cortes
rápidos e transcrição pelo `ark_editor.py` em `C:\Users\USER\ark-cerebro\repos\`. Peça
com avatar, locução sintética, dublagem ou b-roll gerado: MCP CLAUDIO EDITOR
(`generate_video`, `generate_audio`, `shorts_studio_create`), com a voz Fish do JARVIS
guardada só para o sistema. Antes de dizer pronto, skill `conferir-video`.

## Estação 6: legendas e aprovação

1. Legenda por peça: gancho na primeira linha, corpo curto, CTA, localização, até 5
   hashtags. Sem traço ou travessão. Salvar junto do roteiro.
2. Fila de aprovação: cada peça vira tarefa em "aprovação" pelo MCP `W` `create_task`
   com `resp` do decisor interno (Lucas Rosi para account, Gabriel para Vivenda) e o
   link do vídeo no título. Nunca marcar como aprovado por conta própria.
3. Aprovação externa do cliente, quando o contrato pede: ação `create-approval` do
   WorkFlowArk gera link público (memória workflowark-token-link-publico).

## Estação 7: publicação

Só depois da aprovação. Skill `agendar-post`: sobe o vídeo para o Worker de mídia e cria
a rotina de nuvem que publica sozinha via Pipeboard `publish_instagram_media`. Uma rotina
por peça, com a regra anti-duplicata que a skill já traz. Verificar com
`get_instagram_posts` depois do horário e escrever a URL do post no plano.

## Relatório final (tabela)

Peça | formato | data | roteiro (caminho) | status (planejada, roteirizada, gravada,
editada, aprovada, publicada) | URL. Mais a lista do que ficou bloqueado e por quê.
Abrir a pasta do mês no Explorer no fim (`Start-Process explorer.exe <pasta>`).

## O que este fluxo NÃO faz

Não posta sem aprovação, não cria tarefa em massa sem o Gabriel saber (memória
feedback-sem-flood-automatico), não repete formato do mês anterior, não usa Artifact
para entregar.
