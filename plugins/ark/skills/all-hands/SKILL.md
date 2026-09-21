---
name: all-hands
description: Prepara o All Hands mensal da ARK no WorkFlowArk (rota /allhands, slides em ahBuildSlides, narrativa nas chaves set_* de wfa-allhands) com números medidos na fonte, e a pauta em docs/. Use quando o Gabriel pedir "all hands", "reunião do mês", "fechamento de setembro", "deck do mês pra equipe", "as 5 do Caio", ou virar o mês do All Hands. Não use para relatório de trabalho do dia (relatorio-dia) nem deck de cliente (planejamento-estrategico).
---

# All Hands mensal

O All Hands vive dentro do WorkFlowArk, não em arquivo solto: slides montados por `ahBuildSlides` no app (`gest-odeagencia/public/workflowark-app-*.js`), narrativa editável nas chaves `set_*` da store `wfa-allhands`, rota `/allhands`. Dois All Hands já no ar (agosto: be77fd4; setembro: 4ade5d8, build `20260831-caio-kanban-capacity`, 22 slides).

## Checklist

```
- [ ] 1. git pull e ler o All Hands anterior (rota /allhands em produção)
- [ ] 2. Ler a pauta do mês em docs/ (ex.: NEXT-ALLHANDS-2026-09-30.md)
- [ ] 3. Medir cada número na fonte, com data de corte
- [ ] 4. Atualizar chaves set_* (inclusive set_mes_label) e slides novos
- [ ] 5. Deploy + deploy-verificado + screenshot dos slides
- [ ] 6. Memória do mês
```

## 1 e 2. Base

- Estrutura que se repete: capa (mês fixo em `set_mes_label`), pulse do mês, conquistas, gargalos, funil (leads, reuniões, fechamentos), pipeline por pessoa, OKRs, agenda do mês seguinte com captação datada, ritos (daily, planning, All Hands), trilha das 6 etapas, saídas e compromissos.
- Páginas que já saíram a pedido dele e não voltam: "WorkFlowArk: a casa num lugar só", card "Gabriel operando demais".
- Pauta e painel de métricas do mês, com definição, fórmula, fonte e período de cada indicador: `docs/NEXT-ALLHANDS-<data>.md`. Se não existir, criar a partir do anterior.

## 3. Números

Regra do doc de métricas: **valor vem da fonte, falta de dado é "sem dado", nunca zero.** Fontes: `wfa-tarefas` e `wfa-projetos` (entregas e pontualidade, via `GET /api/workflowark/state` com sessão admin ou Supabase), `wfa-crm` e Comercial (leads, propostas, fechamentos), `gh run list` e `git log` (entregas de produto), Meta e Google Ads (tráfego dos clientes), `/inteligencia`. Comparar setembro inteiro contra agosto inteiro; mês parcial não entra.

Duas armadilhas já pagas: (1) o mês da capa vinha do relógio e o deck de setembro montado em agosto saía "Agosto de 2026", hoje é `set_mes_label` fixo, trocar toda virada; (2) `ahPerPessoa()` tinha "72+", "60+" digitados que ninguém conferia, hoje soma o kanban ao vivo. Não reintroduzir número digitado.

## 4. Editar

Chaves de narrativa: prefixo do mês (`set_`, `out_`...) + nome (`capa_sub`, `pulse_*`, `conq`, `garg`, `fun_*`, `pipe_*`, `okr_*`, `agenda_plano`, `ritos`, `saidas`, `compromisso`, `tl_*`, `novo_caio`, `novo_gui`). Slide novo entra em `ahBuildSlides`. Texto sem traço ou travessão, sem autonarração, uma palavra amarela por título.

## 5. Deploy

Build com marcador (`AAAAMMDD-allhands-<mes>`), deploy pelo fluxo normal do gest-odeagencia (CI), depois **skill deploy-verificado**: curl em `workflowark.arkcontent.workers.dev`, marcador na resposta, screenshot da capa e de 2 slides com número. Só então "no ar".

## 6. Memória

`workflowark-allhands-<mes>26.md`: build, commits, o que entrou e saiu, armadilhas novas. Ver [[workflowark-allhands-setembro26]] e [[workflowark-allhands-agosto26]] como modelo.
