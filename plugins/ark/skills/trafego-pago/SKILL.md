---
name: trafego-pago
description: Maestro de tráfego pago da ARK. Use SEMPRE que Gabriel, Danilo ou Rosiron falarem de qualquer coisa de tráfego pago, mídia paga, Meta Ads, Google Ads, gerenciador, campanha, conjunto, anúncio, criativo, verba, orçamento de mídia, CPM, CPC, CTR, CPA, ROAS, frequência, pixel, público, lookalike, impulsionar, biblioteca de anúncios ou concorrente anunciando. Junta as 5 funções (spy, competitive-ads-extractor, bulk-creative, ads-score, ads meta) num fluxo só, junto com as demais skills de marketing.
---

# Tráfego pago (maestro)

Fluxo das 5 funções, na ordem que faz sentido pro pedido. Não precisa rodar as 5:
escolha as que respondem ao que foi pedido e diga quais vai usar numa linha.

| Pedido | Função | Onde está |
|---|---|---|
| "o que o concorrente tá anunciando", "biblioteca de anúncios", "espiar" | `/spy` | skill `spy` (ARK) |
| comparar 3 a 5 concorrentes, padrões, brechas | `competitive-ads-extractor` | skill da ARK |
| "faz copies", "variações de anúncio", "20 criativos" | `/bulk-creative` | skill `bulk-creative` (ARK) |
| "esse criativo tá bom?", "avalia antes de subir" | `/ads-score` | skill `ads-score` (ARK) |
| "audita a conta", "por que caiu", fadiga, frequência, sobreposição | `/ads meta` | plugin `claude-ads` (skill `claude-ads:ads`, comando `/ads meta`; Google: `/ads google`) |

Fluxo completo (quando pedirem "do zero" ou "campanha nova"):
spy -> competitive-ads-extractor -> bulk-creative -> ads-score -> sobe (só com ok) -> ads meta pra acompanhar.

## Antes de tudo

1. Cliente: puxar contexto real (skill `briefing-cliente`; Vivenda: `marketing-farmaceutico` e a memória `vivenda-trafego-performance`).
2. Dados reais pelos conectores: **Pipeboard Meta Ads** (`get_ad_accounts`, `get_campaigns`, `get_insights`, `bulk_get_insights`, `get_ad_creatives`, `get_campaign_audience_overlap`) e **Pipeboard Google Ads** (`get_google_ads_campaign_metrics`, `get_google_ads_search_terms_report`). Se o conector não responder, pedir export (CSV ou print) com período, moeda e fuso.
3. Junto com as demais skills que o roteador indicar (`marketing-arsenal`, `ecc:marketing-campaign`, `saas-marketing-suite`, `local-business-growth`): elas dão o repertório, esta dá o fluxo.

## Regras que não mudam

- Nenhum número inventado. Métrica sem fonte (conector, export ou print) não entra.
- Nada é alterado na conta (pausar, subir, mudar verba, criar público) sem a pessoa ver o resumo e responder com ordem clara ("sobe", "pausa", "pode mudar"). Ordem dada antes do resumo não vale.
- Responsável de tráfego no organograma: Danilo de Lima. Sugestão de tarefa vai como sugestão, nunca criada sozinha.
- Sem travessão nos textos entregues. Entregável é HTML local ou mensagem, nunca Artifact.
- Fechar sempre com: o que foi visto (com período), o que fazer primeiro, quem faz, e como medir em 7 dias.
