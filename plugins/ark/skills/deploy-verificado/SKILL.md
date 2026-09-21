---
name: deploy-verificado
description: Use when deploying to production (wrangler deploy, subir pro ar, colocar no sistema) or before claiming anything is "no ar", "deployado", "atualizado". Also use when the user says the deployed site "não atualizou", "não subiu" or is showing an old version.
---

# Deploy Verificado

## Regra central

"Pronto" significa VERIFICADO NA URL DE PRODUÇÃO, nunca "o comando de deploy rodou sem erro". Dizer "no ar" sem prova já causou incidente em dia de apresentação.

## Checklist obrigatório (na ordem)

1. **Marcador de versão.** Antes de buildar, insira ou atualize um marcador único no HTML/JS entregue, por exemplo `<!-- build 2026-07-02T15:41 -->` ou `const BUILD = "20260702-1541"`. Sem marcador não há como provar que a versão nova subiu.
2. **Build limpo.** Rode o build do projeto. Se o projeto tem pasta de saída (`dist/`, `.output/`), confirme que o arquivo BUILDADO contém o marcador, não só o fonte. Descompasso entre `public/` e a pasta buildada já causou "deployou mas não subiu".
3. **Deploy.** `npx wrangler deploy` (ou o comando do projeto).
4. **Prova na produção.** `curl -s <URL de produção> | grep <marcador>`. Se o marcador não aparecer: NÃO redeploye às cegas. Investigue na ordem: pasta de saída errada, rota/worker errado, cache do Cloudflare.
5. **Prova visual (se mudou UI).** Screenshot da URL de produção (não do localhost) e olhe o screenshot de verdade.
5b. **Prova mobile (se mudou o workflowark.html).** `npm run teste:mobile -- <URL de produção>/workflowark.html`. A equipe usa o sistema pelo celular; a sidebar já ficou presa em produção por uma animação de tema (jul/26) e ninguém viu no desktop.
6. **Só então reporte.** Informe: URL, marcador confirmado, e o que mudou.

## Desculpas que não valem

| Desculpa | Realidade |
|---|---|
| "O wrangler retornou sucesso" | Sucesso do comando não prova que a URL serve a versão nova. |
| "É só uma mudança pequena" | Foi uma "mudança pequena" que quebrou o login em produção. |
| "Sem tempo, o usuário tem pressa" | A verificação leva 30 segundos. O incidente levou uma tarde. |
| "O localhost está certo" | O usuário acessa produção, não o localhost. |

## Sinal vermelho

Se você está prestes a escrever "deployado", "no ar" ou "atualizado" e não tem a saída do `grep` do marcador nesta conversa, PARE e rode o passo 4.
