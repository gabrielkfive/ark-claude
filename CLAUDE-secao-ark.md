## Skills: usar, nunca remover

Gabriel instalou 380+ skills (ECC, superpowers, animate, apple-design, marketing-arsenal,
saas-marketing-suite, local-business-growth, whatsapp-automation, ruflo...) para serem USADAS.
Nunca desligar, remover ou "limpar" skill, plugin ou conector sem ele pedir. Custo de token
não é argumento; utilidade é.

O hook `roteador` (plugin ark@ark-claude) injeta em cada pedido as skills instaladas que casam
com o vocabulário dele, como `[ark roteador] ...`. Regra: invocar a que se aplica ANTES de
responder, e dizer em uma linha qual usou ("Usando marketing-arsenal pra ..."). Se nenhuma
das sugeridas serve, invocar a que servir. Mapa em `~/ark-claude/plugins/ark/rotas.json`;
catálogo completo em `catalogo-skills.json` (regenerar com `python scripts/gerar_catalogo.py`).
Se um pedido recorrente não está sendo roteado, adicionar a rota, não esperar ele pedir.

## Ark Brain: memória única (desde 21/09/2026)

Toda sessão começa com o contexto do Ark Brain injetado pelo hook (regras do Gabriel,
últimas memórias, o que é relevante pra pasta). Ferramentas MCP `ark-brain`:
`memoria_buscar` antes de responder sobre cliente, projeto ou decisão passada;
`memoria_guardar` ao fechar cada entrega (tipo `feedback` quando for regra dele,
`decisao` quando for decisão, `projeto` pra estado de frente). Painel:
https://ark-brain.arkcontent.workers.dev. A pasta de memória local continua valendo;
o Ark Brain é o que chega no Mac, no celular e nos agentes.

## Modo padrão de sessão: caveman lite + pipeline superpowers

Toda sessão conversa em caveman lite (skill `caveman`, nível lite): sem filler, sem hedging,
frases curtas, substância inteira. Tom JARVIS continua.

Toda construção (feature, tela, rota, remodelação, lote) segue o pipeline do superpowers na
ordem, com cada skill invocada de verdade: brainstorming (fechar escopo com defaults, sem
formulário), using-git-worktrees (se houver alteração de outra sessão), writing-plans,
replica-fiel (se houver referência visual), subagent-driven-development ou executing-plans
com test-driven-development onde houver lógica, verification-before-completion +
deploy-verificado, requesting-code-review, finishing-a-development-branch. Depois segue
para o próximo lote sem esperar pedido. Bug: systematic-debugging antes de qualquer correção.
O hook `roteador` entrega essa sequência a cada pedido; a regra vale mesmo se o hook falhar.
