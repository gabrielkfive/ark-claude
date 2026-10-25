---
name: replica-fiel
description: Use when the user provides a visual reference to replicate or match (print, screenshot, Figma, site como Apple/ramp.com, "quero igual a isso", "replica fielmente", "no padrão Apple") or complains the design "não mudou nada", "não ficou parecido", "ficou amador".
---

# Réplica Fiel de Referência Visual

## Regra central

Nunca iterar design às cegas. Cada rodada precisa de PROVA VISUAL: referência e resultado lado a lado. Horas de iteração sem screenshot terminaram em "o design não mudou NADA".

## Pré-condição: o olho tem que funcionar

Antes de qualquer edição de design, tire UM screenshot de teste da página atual e confirme que o arquivo foi salvo e aberto. Se o screenshot falhar (EPERM, allowed roots, browser fechado), PARE e conserte a ferramenta primeiro. Iterar sem enxergar é o modo de falha número 1.

## Réplica fiel é cópia, não inspiração (Gabriel, 25/10/2026)

Quando ele manda um exemplo, a entrega é aquele exemplo com a marca dele: mesmas cenas na mesma ordem, mesmo tempo de cada cena, mesmas transições, mesma escala de tipografia, mesmo tipo de mockup e mesma densidade. Só muda o que ele mandou mudar (marca, cor, texto, fotos). Versão "no espírito de", com roteiro e estrutura inventados, é falha, mesmo que fique bonita.

Vídeo de referência: baixar, quebrar em quadros (`ffmpeg -vf fps=2`), anotar cena por cena (segundo, o que aparece, como entra, como sai) e montar a cópia nessa mesma tabela. Prova = os dois vídeos lado a lado no mesmo segundo. Vídeo e motion se fazem no PC (fontes, material real, Remotion, render pesado); na nuvem só se não houver PC, e avisando que é rascunho.

## Fluxo

1. **Capturar a referência.** Baixe/screenshot a referência para um arquivo local e ABRA para ver. Se for Figma e o MCP falhar (rate limit do plano), peça um print ao usuário em vez de seguir de memória.
2. **Extrair tokens.** Liste por escrito: paleta exata (hex), fonte e pesos, espaçamentos, raio de borda, sombras, densidade do layout. Design "parecido" vem de tokens iguais, não de impressão geral.
3. **Uma tela piloto.** Aplique os tokens em UMA tela só.
4. **Prova lado a lado.** Screenshot da tela piloto no mesmo viewport da referência. Compare os dois arquivos você mesmo e aponte 3 diferenças restantes.
5. **Mostrar antes de escalar.** Apresente o lado a lado ao usuário e só replique para o sistema inteiro depois do "é isso".

## Desculpas que não valem

| Desculpa | Realidade |
|---|---|
| "Sei como é o estilo Apple" | Impressão de memória gerou "design de dev iniciante". Extraia tokens reais. |
| "Screenshot está quebrado, sigo assim" | Sem olho, cada iteração é aposta. Conserte a ferramenta primeiro. |
| "Vou aplicar no sistema todo de uma vez" | Errar em 40 telas custa 40x mais que errar em 1. |
| "O CSS mudou, então mudou" | O usuário vê pixel, não diff. Prova é screenshot. |
