---
name: maratona
description: Use when the user gives a batch of features or fixes to complete autonomously ("sem parar", "só pare quando finalizar tudo", "marcha", "faz tudo", list of 3+ deliverables), or keeps typing "continua" to push work forward.
---

# Maratona de Features

## Objetivo

Executar uma lista de entregas de ponta a ponta sem o usuário precisar digitar "continua", e sem entregar coisa quebrada. Qualidade por item vale mais que quantidade: o histórico mostra que itens entregues sem verificação voltam como bug e custam o dobro.

## Fluxo

1. **Registrar a lista.** Crie uma tarefa (TaskCreate) por entrega, ordenada por dependência e por impacto. Mostre a lista uma vez e comece. Não pergunte por onde começar, decida.
2. **Por item:** implementar, verificar de verdade (para deploy use a skill deploy-verificado; para UI use screenshot), marcar a tarefa como concluída e escrever 1 linha de progresso.
3. **Bloqueou?** Se um item travar (permissão negada, serviço fora, falta chave), NÃO pare a maratona: anote o bloqueio na tarefa, pule para o próximo item e liste os bloqueados no relatório final.
4. **Erro repetido?** O mesmo comando falhou 2 vezes pelo mesmo motivo: pare de repetir e mude a abordagem. Quatro tentativas idênticas já desperdiçaram horas.
5. **Relatório final:** tabela com cada item, status (no ar e verificado / feito sem deploy / bloqueado + motivo) e a URL de produção.

## Regras

- Zero AskUserQuestion durante a maratona, salvo ação destrutiva ou gasto de dinheiro.
- Deploy incremental: suba por item verificado, não um deploy gigante no fim.
- Se os créditos ou o contexto estiverem acabando, escreva o handoff (o que falta, onde parou) em `docs/` ou no Obsidian ANTES de parar.
