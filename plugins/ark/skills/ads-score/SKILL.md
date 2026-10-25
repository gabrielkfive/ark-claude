---
name: ads-score
description: /ads-score, o analista de criativos. Use quando pedirem pra avaliar, dar nota ou revisar um anúncio ou criativo antes de investir ou publicar ("esse criativo tá bom?", "qual desses sobe?", "por que esse anúncio não converte"). Pontua 6 elementos e aponta o que corrigir. Parte do fluxo trafego-pago.
---

# /ads-score: analista de criativos

Entrada: o criativo (imagem, vídeo, print ou texto) + objetivo e público. Vídeo: assistir com a skill `assistir` antes de dar nota. Criativo já no ar: puxar métricas reais pelo Pipeboard (`get_ad_creatives`, `get_insights` do anúncio) e citar o período.

Nota de 0 a 10 em cada elemento, com uma frase de motivo:

1. **Gancho**: para o dedo em 1 a 3 segundos? Fala com o público certo?
2. **Copy**: clara, curta, um benefício principal, linguagem do cliente final.
3. **CTA**: um só, claro, combina com o destino (WhatsApp, site, perfil).
4. **Apelo emocional**: dor ou desejo real do público, não genérico.
5. **Oferta**: existe, é concreta e tem motivo pra agir agora (sem urgência falsa).
6. **Alinhamento visual**: identidade do cliente, texto legível no celular, formato certo (9:16 / 4:5), área segura de story.

Nota final = média, arredondada a uma casa. Abaixo de 7: não sobe sem corrigir.
Entregar: tabela das 6 notas, os 3 pontos fracos em ordem de impacto e a versão corrigida (copy reescrita ou instrução objetiva pro designer). Saúde/farmácia: checar também as regras de `marketing-farmaceutico` e política de anúncios da Meta.
Comparando vários criativos: ranking final e qual sobe primeiro.
