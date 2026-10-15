# Agendar post para os sócios: plano

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Lucas e Danilo conseguem usar `/agendar-post` no Claude deles sem travar, e entendem como pelo guia.

**Architecture:** A skill deixa de depender do Pipeboard (cancelado 15/10/2026). Ela detecta em qual dos três cenários o PC está (pasta ark-publisher com client.json, conector Composio próprio, nenhum dos dois) e segue o caminho certo. O guia HTML explica os três cenários com frases prontas.

**Tech Stack:** Markdown (SKILL.md), plugin ark-claude, HTML estático, Cloudflare Worker com assets.

**Spec:** levantamento `ENTREGAS/2026-10-15/socios-claude/levantamento/03-postagem-automatica.md` + baseline RED desta sessão.

## Global Constraints

- Sem traço, travessão ou meio-traço separando ideias em texto entregue (`—`, `–`, `─`, `━` proibidos).
- Nenhum token, bearer ou chave em skill, guia ou repo.
- "No ar" só com permalink; publicar só com "publica" de quem manda.
- Pipeboard não é caminho nem sugestão de upgrade.

## Review Focus

1. Sócio sem pasta ark-publisher pede horário futuro: a skill tem que parar e orientar, não inventar rotina.
2. Timeout na publicação: nunca republicar sem conferir o feed.
3. Cliente fora das 3 contas ligadas: a skill manda pedir conexão ao Gabriel.
4. Link do Drive privado: curl devolve HTML, a skill para antes de agendar.
5. Guia aberto no celular: sem rolagem horizontal.

---

### Task 1: Reescrever a skill (GREEN)

**Files:** Modify `plugins/ark/skills/agendar-post/SKILL.md`, `plugins/ark/.claude-plugin/plugin.json` (1.2.0 para 1.2.1). Copiar para `~/.claude/skills/agendar-post/SKILL.md`.

- [ ] Reescrever com: detecção de cenário, caminho A (ark-publisher), caminho B (Composio próprio, publicar agora), caminho C (sem nada: preparar pacote e mandar pro Gabriel), contas ligadas, erros comuns.
- [ ] Teste GREEN: subagente com o mesmo cenário do Lucas (sem pasta, sem Composio) e um cenário com a pasta. Esperado: nenhuma menção a Pipeboard como caminho, para e entrega pacote no primeiro, monta job e pede "publica" no segundo.
- [ ] Commit e push.

### Task 2: Guia HTML para os sócios

**Files:** Create `Documents/ARK CONTENT/ENTREGAS/2026-10-15/socios-claude/agendar-post/index.html`.

- [ ] Página de rolagem na identidade ARK: o que é, os três cenários, frases prontas, o que o Claude pergunta, prova, o que não fazer, o que depende do Gabriel.
- [ ] Busca por `—`, `–`, `─`, `━` retorna zero. Screenshot 1440 e 390.

### Task 3: Deploy e prova

- [ ] Worker `socios-agendar-post` com assets, marcador de versão no HTML, curl 200 + marcador, screenshot da URL.

### Task 4: Revisão e fechamento

- [ ] Code review por subagente da skill e do guia. Corrigir.
- [ ] `memoria_guardar` no Ark Brain, link da pasta e pasta aberta.
