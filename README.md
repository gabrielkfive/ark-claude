# ark-claude

Plugin do Claude Code com as rotinas e regras de qualidade da ARK Content. Um repositório, instalado no Mac e no PC. Atualizar é `git pull` + `claude plugin marketplace update ark-claude`.

## O que tem

Skills (em `plugins/ark/skills/`): cópia sincronizável de maratona, deploy-verificado, agendar-post, roteiro, retomar. As originais continuam em `~/.claude/skills`; este plugin existe pra levar hooks e skills pro Mac, não pra substituir nada.

Hooks (em `plugins/ark/hooks/`):

| Hook | Evento | O que faz |
|---|---|---|
| sem_travessao | PostToolUse Write/Edit em .html/.md/.txt | Bloqueia travessão, meio-traço e linha de desenho em entregável e manda corrigir |
| sem_cdn | PostToolUse Write/Edit em .html | Avisa se a página depende de script/CSS de CDN externo |
| sem_artifact | PreToolUse Artifact | Nega publicação como Artifact (leitura e listagem seguem liberadas) |
| pronto_medido | Stop | Se a resposta diz "no ar" sem curl/fetch na URL de produção na rodada, devolve pra medir |

Os hooks ignoram tudo dentro de `.claude/`, `.agents/`, `ark-claude/`, `node_modules/` e da pasta temporária do Claude.

## Instalar

```bash
git clone https://github.com/gabrielkfive/ark-claude ~/ark-claude   # ou o remoto que estiver em uso
claude plugin marketplace add ~/ark-claude
claude plugin install ark@ark-claude
```

Precisa de `bash` e `python` ou `python3` no PATH (o `run.sh` escolhe).

## Testar um hook na mão

```bash
echo '{"tool_input":{"file_path":"C:/caminho/arquivo.html"}}' | bash plugins/ark/hooks/run.sh sem_travessao; echo $?
```

Exit 2 = bloqueou. Exit 0 sem saída = passou.

## Regras de criação de skill nova

1. Nasce de uma entrega real que acabou de ser feita, nunca de tarefa imaginada.
2. Descrição em terceira pessoa, com "use quando..." e termos que o Gabriel realmente usa.
3. Corpo curto. Modelo em `assets/`, validador em `scripts/`, detalhe em `references/`.
4. Testada na próxima entrega real antes de ser considerada pronta.
5. Zero uso em 60 dias = eu estou deixando de invocar. Ajustar o gatilho, não apagar.
