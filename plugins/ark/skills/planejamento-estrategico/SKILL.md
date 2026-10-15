---
name: planejamento-estrategico
description: Use quando o Gabriel pedir planejamento estratégico, plano trimestral, plano de 90 dias, diagnóstico de cliente, "onde o <cliente> está e pra onde vai", reunião de alinhamento com decisor, ou revisão de metas (4DX, MCI). Junta dados reais (Meta e Google Ads, Instagram, WorkFlowArk, reuniões, contrato) e entrega um deck HTML na identidade da ARK mais o registro na aba Planejamentos do WorkFlowArk.
---

> **Aviso 15/10/2026: Pipeboard em cancelamento.** O Gabriel cancelou o teste do Pipeboard (o pago limita a 3 contas). Enquanto o conector responder, segue valendo o que está abaixo. Se ele cair: anúncios e métricas pelo `meta-ads-mcp` local (`mcp__meta-ads__*`) com token próprio do Business Manager; o pacote aberto NÃO tem `publish_instagram_media` nem `get_instagram_posts`, então publicação e posts orgânicos vão direto pela Instagram Graph API com o mesmo token. Google Ads: MCP oficial do Google, depende do developer token da MCC.

# Planejamento estratégico de cliente

Diagnóstico com números de verdade, decisão de foco, metas mensuráveis e plano de 90
dias que a equipe consegue executar. Entrega como HTML local na pasta do cliente e como
item da aba Operacional > Planejamentos do WorkFlowArk.

## Defaults

- Horizonte: 90 dias a partir do primeiro dia do próximo mês.
- Público do deck: o decisor do cliente (nome vem do brief). Linguagem simples.
- Formato: HTML de rolagem, identidade ARK (fundo #0D0D0D, Sora nos títulos, Inter no
  texto, amarelo #FEEF02, cards arredondados). Kit em
  `Documents\ARK CONTENT\MARCAS\ARK\` (ark.css, montar.py, logo). Nunca Artifact.

## Passo 1: coleta (tudo desta sessão, nada de memória de cabeça)

1. Brief: `src/integrations/clientes.ts`. Sem brief, rodar `briefing-cliente` antes.
2. Contrato: valor, escopo e vencimento (pasta CONTRATOS do cliente, memória
   radar-contratos-carteira-ark).
3. Mídia paga, últimos 90 dias: Meta `get_insights` por campanha (gasto, resultado, custo
   por conversa) e Google `get_google_ads_campaign_metrics`. Se não houver conta, dizer.
4. Orgânico, últimos 90 dias: Pipeboard `get_instagram_posts` (top 10 por alcance, top 5
   por salvamento, formato que mais rende) e `get_instagram_account_insights`.
5. Operação: MCP `W` `read_block` em `wfa-tarefas` e `wfa-producao` (entregue x
   prometido, atrasos, captações feitas), `wfa-cobranca` (inadimplência).
6. Voz do cliente: Tactiq `search_meetings` pelo nome, `get_transcript_excerpts` nos
   trechos de reclamação, meta e pedido.
7. Concorrência: Meta `ads_library_search` com 3 concorrentes da praça e `WebSearch`
   para novidades do segmento. Só o que for útil para a decisão.
8. Para farmácia e saúde, ler também a skill `marketing-farmaceutico`.

## Passo 2: diagnóstico em uma página

- 3 números que resumem os 90 dias (só os que mudam a decisão).
- O que funcionou (com a peça ou campanha nomeada) e o que não funcionou.
- Gargalo principal em uma frase (atenção, conversão, retenção ou operação).

## Passo 3: decisão e metas

- Uma Meta Crucialmente Importante (MCI) no padrão 4DX, com número e data.
- Duas ou três medidas de direção que a equipe controla toda semana (captações,
  peças publicadas, conversas iniciadas, receitas recebidas).
- Placar: onde a medida vai ser lida toda semana (Vivenda Hub, WorkFlowArk, planilha).

## Passo 4: plano de 90 dias

Mês 1 a 3, cada um com foco, campanha, entregas numeradas, responsável e orçamento de
mídia. Escrever "Mês 1 a 2", nunca com traço. Incluir a régua de reunião (quinzenal ou
mensal, com quem) e os riscos com plano B.

## Passo 5: entrega

1. HTML em `CLIENTES\<CLIENTE>\PLANEJAMENTO\plano-estrategico-<AAAA-MM>.html`, montado
   pelo `montar.py` do kit (ele barra traço proibido, recurso externo e classe "ad").
2. Antes de fechar: buscar travessão (U+2014), meio-traço (U+2013) e traços de desenho (U+2500, U+2501) no arquivo e remover; abrir no Playwright
   em 1440 e 390 de largura e tirar screenshot; conferir que nenhum número foi inventado
   (cada número aparece em alguma fonte do passo 1).
3. Registrar no WorkFlowArk: item em `wfa-planejamentos` pela aba Operacional >
   Planejamentos (campos de lista em texto, um item por linha, separador " | "). Se for
   preencher por código, a chave já está no STATE_KEYS do servidor.
4. Tarefas do mês 1 no Kanban via MCP `W` `create_task`, uma por entrega, com
   responsável do organograma (tráfego Danilo, social Maria Luiza, account Lucas Rosi,
   design M. Portela, edição Samuel Magalhães, captação Omar, comercial Saulo).
5. LEIA-ME.txt da pasta do cliente atualizado e Explorer aberto na pasta.

## Proibições

Sem traço ou travessão como separador. Sem autonarração no deck (o deck não fala de si,
memória feedback-documento-sem-autonarracao). Sem número sem fonte. Sem repetir o plano
do trimestre anterior. Sem entregar como Artifact.
