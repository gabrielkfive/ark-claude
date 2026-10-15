---
name: briefing-cliente
description: Use quando um cliente da ARK não tem brief no sistema (docs/clientes/<cliente>.md e BRIEFS em src/integrations/clientes.ts), quando o Gabriel pedir "monta o briefing do <cliente>", "atualiza o contexto do <cliente>", ou antes de rodar producao-conteudo e planejamento-estrategico para um cliente sem brief. Gera o brief a partir de fontes reais (pasta do cliente, reuniões Tactiq, Drive, WorkFlowArk, Instagram) e registra no WorkFlowArk.
---

# Briefing de cliente

O brief é o que faz qualquer agente (roteirista, planejador, legenda, conselho) parar de
ser genérico. Sem brief, tudo que sai é "iazismo". Este fluxo monta o brief com fatos
confirmados e o grava nos dois lugares que o sistema lê.

## Regra número um

Nada de fato inventado. Cada linha do brief vem de uma fonte que você abriu nesta
sessão. Se uma informação (decisor, ticket, praça, @ do Instagram) não apareceu em
nenhuma fonte, escreva "(a confirmar com o Gabriel)" no lugar. Ver a memória
feedback-iazismo-biografia-inventada.

## Fontes, nesta ordem

1. **Pasta do cliente**: `C:\Users\USER\Documents\ARK CONTENT\CLIENTES\<CLIENTE>\`.
   Ler LEIA-ME.txt, propostas, contratos, roteiros, planejamentos e manual de marca.
   Contratos assinados dão valor, escopo e vencimento.
2. **WorkFlowArk** via MCP `W`: `read_block` com `wfa-clientes` (cadastro e status),
   `wfa-tarefas` (o que a equipe fez nos últimos 60 dias), `wfa-crm` (se ainda for lead),
   `wfa-producao` (captações). Filtrar pelo clienteId.
3. **Reuniões**: Tactiq `search_meetings` com o nome do cliente como `query`, depois
   `get_transcript_excerpts` nos trechos de decisão (quem aprova, o que odeiam, metas).
4. **Drive**: `search_files` com o nome do cliente, para achar briefings antigos, planilhas
   de metas e manuais de marca fora da pasta local.
5. **Instagram**: números públicos via
   `https://workflowark.arkcontent.workers.dev/api/ig/perfil?handle=<arroba>`. Se falhar
   (o Instagram bloqueia robô), anotar "(números do IG a conferir)".
6. **Memória do Claude**: `Grep` em `~/.claude/projects/C--Users-USER/memory/` pelo nome
   do cliente. Muita decisão já está lá.

## Estrutura do brief (mesma do VIVENDA em clientes.ts)

Texto corrido, 12 a 25 linhas, sem traço ou travessão como separador. Blocos:

- Cabeçalho: NOME (praça), segmento, ticket mensal, captações por mês, plano.
- POSICIONAMENTO: uma frase de virada (de onde para onde).
- TOM: regra de ouro em uma frase, e o que NUNCA fazer (compliance do setor: OAB para
  advocacia, Anvisa e CFM para saúde e farmácia, sem promessa de resultado).
- PILARES: até 3.
- FORMATOS por prioridade (Reels, carrossel, stories, live, WhatsApp).
- PRODUTOS OU PRATOS EM FOCO AGORA, com o motivo (sazonal, margem, retenção).
- PESSOAS: decisor real, quem executa, quem atrapalha. Papel de cada um.
- MOMENTO: fase do cliente (onboarding, ramp-up, retenção, risco) e o arco dos
  próximos 30 dias.
- CAMPANHA ATIVA, se houver, com meta numérica e regra de oferta.

## Onde gravar

1. `docs/clientes/<slug>.md` no repo `C:\Users\USER\Documents\ARK CONTENT\SOFTWARE\Agency Sync Hub`
   (fazer `git pull` antes). Cabeçalho com data e fontes usadas.
2. `src/integrations/clientes.ts`: nova const com o texto e entrada em `BRIEFS` com o slug
   (a busca é por `includes`, então use o pedaço mais curto e único do nome, tudo minúsculo).
3. Cópia legível em `CLIENTES\<CLIENTE>\BRIEFING\briefing-<slug>-<AAAA-MM>.md` e uma linha
   no LEIA-ME.txt da pasta.
4. Build, deploy e verificação pela skill `deploy-verificado`. Commit com mensagem
   "Brief do cliente <nome>".

## Prova de pronto

- O arquivo em docs/clientes existe e abre.
- `grep -n "<slug>" src/integrations/clientes.ts` mostra a entrada em BRIEFS.
- Deploy verificado na URL de produção.
- Lista das fontes abertas no relatório final, com o que ficou "(a confirmar)".
