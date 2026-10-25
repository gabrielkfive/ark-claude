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
| roteador | UserPromptSubmit | Lê o pedido e injeta as skills instaladas que casam (rotas.json + catalogo-skills.json), pra serem invocadas antes da resposta |
| pronto_medido | Stop | Se a resposta diz "no ar" sem curl/fetch na URL de produção na rodada, devolve pra medir |
| atualizar | SessionStart (startup) | Em segundo plano, no máximo a cada 6h: git pull do ~/ark-claude, atualiza o plugin ark e instala o que faltar de `plugins/ark/skills-equipe.json`. Nunca remove nada. Log em `~/.claude/ark-atualizar.log`; o resultado aparece na sessão seguinte |

Os hooks ignoram tudo dentro de `.claude/`, `.agents/`, `ark-claude/`, `node_modules/` e da pasta temporária do Claude.

## Tráfego pago (23/10/2026)

As 5 funções do reel do Matheus Hunoff, ligadas sozinhas pelo roteador sempre que Gabriel, Danilo ou Rosiron falam de tráfego (campanha, anúncio, criativo, CPM, ROAS, gerenciador, verba...), junto com marketing-arsenal, ecc:marketing-campaign e saas-marketing-suite:

| Função | Skill |
|---|---|
| /spy (espião de concorrentes) | `spy` |
| Competitive Ads Extractor (estrategista) | `competitive-ads-extractor` |
| /bulk-creative (copywriter, 20 variações) | `bulk-creative` |
| /ads-score (nota de 6 elementos antes de subir) | `ads-score` |
| /ads meta (auditoria da conta) | plugin `claude-ads` (AgriciDaniel, MIT), instalado pelo `instalar.sh` |

O maestro `trafego-pago` escolhe a ordem e puxa dado real pelos conectores Pipeboard (Meta e Google Ads). Nada muda na conta sem ok explícito.

## Roteador de skills

Mapa curado em `plugins/ark/rotas.json` (vocabulário do Gabriel em regex -> skills). Catálogo de todas as skills da máquina em `plugins/ark/catalogo-skills.json`, regenerado com `python scripts/gerar_catalogo.py`. Testar: `printf '{"prompt":"..."}' | bash plugins/ark/hooks/run.sh roteador`.

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

## Ferramentas do toolkit e xtool (18/10/2026)

Um comando instala pnpm, fd, Codex, Graphify, Ponytail e as skills de projeto do WorkFlowArk
(supabase-postgres-best-practices, shadcn, differential-review, vercel-react-best-practices,
find-skills). Pula o que já existe e mostra um resumo no fim.

- PC: `powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\ark-claude\instalar-ferramentas.ps1"`
- Mac: `bash ~/ark-claude/instalar-ferramentas.sh` (também instala o xtool)

xtool (app de iPhone pelo Claude Code): `docs/xtool.md`.
