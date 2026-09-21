---
name: relatorio-dia
description: Monta o relatório do dia (ou de um período) da ARK em deck HTML único na identidade ARK, a partir das sessões reais do Claude Code, memórias, git log, disco e curl nas URLs. Use quando o Gabriel pedir "relatório do dia", "compilado de hoje", "o que foi feito ontem", "me mostra tudo que rodou", "as sessões sumiram", ou relatório semanal/mensal de trabalho. Não use para relatório de cliente (planejamento-estrategico) nem All Hands (all-hands).
---

# Relatório do dia

Relatório é prova, não narrativa. Cada slide diz o que foi feito, onde está (link ou pasta) e se foi conferido em produção. Método dos relatórios de 31/08, 14/09 e 17/09 em `Documents/ARK CONTENT/ESTUDOS/relatorio-AAAA-MM-DD/`.

## Checklist

```
- [ ] 1. Extrair as sessões do dia (script)
- [ ] 2. Cruzar com memórias, git log e disco
- [ ] 3. Conferir URLs citadas (curl, marcador de versão)
- [ ] 4. Copiar gerar.py do último relatório, preencher SLIDES
- [ ] 5. Gerar, validar, abrir e conferir
- [ ] 6. LEIA-ME + memória do dia
```

## 1. Extrair

```bash
python scripts/extrair_sessoes.py 2026-09-17          # texto
python scripts/extrair_sessoes.py 2026-09-17 --json   # pra cruzar
```

Lista por sessão: primeiro pedido, último texto, arquivos escritos, skills usadas, deploys, URLs conferidas, commits. **Ler primeiro as sessões marcadas COMPACTAÇÃO**: o resumo de compactação já vem organizado. Carimbos são locais (UTC menos 3 já aplicado pelo sistema).

## 2. Cruzar

- `git -C <repo> log --since="AAAA-MM-DD 00:00" --until="AAAA-MM-DD 23:59" --oneline` nos repos tocados (gest-odeagencia, ark-cerebro, vivenda-hub, ark-claude).
- Memórias do dia já saem no script. Ler as que importam.
- Disco: `find "Documents/ARK CONTENT" -newermt AAAA-MM-DD ! -newermt AAAA-MM-DD+1 -type f` pra pegar entregável que não passou por sessão.
- Se o PC caiu: `Get-WinEvent -FilterHashtable @{LogName='System';Id=41,1001,6008}` explica o sumiço; entra no relatório como fato, sem drama.

## 3. Conferir

Toda URL que o relatório chama de "no ar" recebe curl agora, e o marcador de versão é citado no slide. Sem curl, o slide diz "feito, não conferido em produção".

## 4 e 5. Gerar

Copiar `gerar.py` e `LEIA-ME.txt` do relatório mais recente (`ESTUDOS/relatorio-17-09-2026/`). Estrutura: lista `SLIDES` de tuplas `(tag, título com **negrito**, parágrafo, [bullets], rodapé com links)`. Fontes e logo vêm de `MARCAS/ARK` em base64. Um slide por frente de trabalho, capa com a frase do dia, slide final "o que ficou solto". Depois:

```bash
python gerar.py
python ~/ark-claude/plugins/ark/scripts/validar_entregavel.py index.html --final
```

Abrir `index.html` e rolar tudo. Regras de escrita: sem traço ou travessão, sem autonarração ("este documento apresenta"), sem inflar criticidade, números com fonte.

## 6. Fechar

`LEIA-ME.txt` de 3 linhas (o que é, como regerar, memória correspondente). Memória `relatorio-diario-AAAA-MM-DD.md` com o caminho, o método e o que ficou pendente.
