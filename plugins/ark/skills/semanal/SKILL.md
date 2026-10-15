---
name: semanal
description: Use when Gabriel asks to start the week's client tasks ("/Semanal", "bora dar início nas tarefas da semana", "roda o semanal", "monta a semana"). Measures the week's temperature from real data (team tasks, WhatsApp Comercial, ads) and posts task SUGGESTIONS to WorkFlowArk notifications for approval. Never creates tasks directly.
---

# /Semanal · Início da semana dos clientes

## O que é

Rodada semanal que mede a temperatura como se tudo tivesse zerado e propõe as tarefas da semana por cliente. As sugestões vão para as NOTIFICAÇÕES do WorkFlowArk, onde o Gabriel aprova ("✓ Criar tarefa") ou descarta. NUNCA criar tarefa direto no board (regra do sem-flood).

## Fontes de dados (nesta ordem)

1. **Tarefas da equipe**: via Playwright logado em https://workflowark.arkcontent.workers.dev/app (o perfil do navegador tem a sessão/credenciais do Gabriel salvas). Pegar o token do Supabase no localStorage (chave contendo `auth-token`, campo `access_token`) e chamar `GET /api/workflowark/state` com `Authorization: Bearer`. Ler `wfa-tarefas` (abertas + concluídas do mês), `wfa-rotinas`, `wfa-jornada`, `wfa-clientes-custom`. Foco nos integrantes: Danilo de Lima, Lucas Rosi, Samuel Magalhães, Saulo e Maria Luiza (Malu).
2. **WhatsApp (temperatura dos leads)**: `GET /api/workflowark/state?key=wfa-whatsapp` (estrutura: `{conversas: {tel: {nome, msgs:[{ts,dir,text,sender}]}}}`). Ler os grupos "COMERCIAL GERAL - ALPHA", "ARK Comercial" e conversas com leads dos últimos 10 dias. Procurar: leads para reativar, follow-ups combinados com data, perguntas de proposta sem resposta, relatórios do Danilo.
3. **Meta Ads + Google Ads (MCP)**: conta Meta "Vivendas" `act_1679063009779975`, Google "[E] Vivenda ON" `1522033694`. Últimos 7 dias por campanha: gasto, conversas iniciadas (`onsite_conversion.messaging_conversation_started_7d`), custo por conversa. Sinalizar saldo baixo e campanha cara vs campeã.

## Como montar as sugestões (defaults)

- Máximo ~10 sugestões por rodada. Qualidade > quantidade.
- Nem todo cliente tem tudo do sprint semanal: olhar as tarefas ABERTAS de cada um e propor só os BURACOS (cliente sem nenhuma tarefa na semana, sem criativo na fila, sem otimização de tráfego, onboarding parado, lead com data combinada).
- Responsável por função (padrão da casa): tráfego/otimização = Danilo de Lima; account/status/reunião = Lucas Rosi; edição/captação = Samuel Magalhães; criativos = Maria Luiza; comercial/leads = Saulo.
- Datas dentro da semana corrente (fuso America/Sao_Paulo), prio `alta` só para dinheiro parado, lead quente ou cliente abandonado.

## Formato da sugestão (chave `wfa-notificacoes`)

Ler o array atual, dar append (nunca sobrescrever sem reler) e salvar com `POST {action:'save-state', key:'wfa-notificacoes', data: arr}`:

```js
{ id: 'sem'+Date.now()+'_'+i, ts: Date.now()+i, tipo: 'semanal',
  texto: 'Semanal · <resumo com o dado que motivou>',
  clienteId: '<id>',
  tarefaProposta: { title, desc: '<contexto + fonte (grupo/dado) + o que fazer>',
    funcao: 'Account Manager|Gestor de Tráfego|Criador|Editor|Captação',
    clienteId, resp: '<nome exato do TEAM_BASE>', data: 'AAAA-MM-DD',
    prio: 'alta|media', tags: ['semanal'], origem: 'semanal' } }
```

O botão "✓ Criar tarefa" da tela de notificações converte a proposta em cartão no backlog (função `notifAprovarTarefa` no monolito). `texto` sem traço/travessão (regra do Gabriel).

## Verificação (obrigatória)

1. Reler `wfa-notificacoes` do servidor e confirmar os ids `sem...` gravados.
2. No iframe do /app, `document.querySelector('[data-nav="notificacoes"]').click()` (o item fica num submenu invisível, clicar via JS) e contar os cards "Semanal" após o sync (~10 a 20s). Screenshot de prova.
3. Reportar ao Gabriel: quantas sugestões, para quem, e o que motivou cada uma (1 linha cada).

## Extras da rodada

- Se houver reunião semanal do time no dia, gerar também o resumo de tráfego (Meta+Google) e salvar em Obsidian `ARK\Clientes\` + enviar o arquivo.
- Registrar a rodada no Diário do Obsidian.
