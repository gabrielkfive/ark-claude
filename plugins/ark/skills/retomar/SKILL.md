---
name: retomar
description: Use when the user opens a session asking to resume work ("voltei", "onde paramos", "até onde fomos ontem", "continua de ontem", "me lembra o que falta") or when reconstructing project state after days away.
---

# Retomar Trabalho

## Objetivo

Reconstruir o estado em menos de 1 minuto, sem perguntar nada ao usuário.

## Fontes (nesta ordem)

1. `MEMORY.md` e os arquivos de memória relevantes ao projeto citado.
2. `git log --oneline -15` e `git status` no repositório do projeto.
3. `git pull` ANTES de qualquer edição (o usuário alterna entre Mac e PC; já houve trabalho em versão velha).
4. Documentos de handoff no repo (`docs/*HANDOFF*`, planos no Obsidian) se existirem.

## Formato da resposta (máximo 8 linhas)

1. Última coisa concluída e deployada.
2. O que ficou em andamento.
3. Bugs ou pendências reportados e não resolvidos.
4. Próximo passo sugerido (escolha você, não pergunte).

Depois do resumo, comece o próximo passo direto. Não faça formulário de perguntas.
