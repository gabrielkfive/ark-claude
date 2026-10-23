---
name: spy
description: /spy, o espião de concorrentes. Use quando pedirem pra ver o que um concorrente está anunciando, abrir a Biblioteca de Anúncios da Meta, "espiar" anúncio, descobrir gancho, oferta, CTA e há quanto tempo um anúncio está rodando. Parte do fluxo trafego-pago.
---

# /spy: espião de concorrentes

Entrada: nome ou @ do concorrente (ou página do Facebook) e país (padrão BR).

1. Achar a página: Pipeboard Meta Ads `search_pages_by_name` ou o @ informado.
2. Abrir a Biblioteca de Anúncios: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=<nome>` pelo navegador (Playwright) ou WebFetch. Se a página não carregar, pedir print ou link dos anúncios.
3. Para cada anúncio ativo, anotar:
   - data de início e dias rodando (rodando há 30+ dias = provavelmente funciona)
   - formato (vídeo, imagem, carrossel) e posicionamentos
   - gancho (primeira frase ou primeiros 3 segundos)
   - oferta, CTA e destino (WhatsApp, site, perfil)
   - quantas variações do mesmo criativo existem (muitas = estão testando ou escalando)
4. Entregar tabela por anúncio + 3 conclusões: o que repetem, o que está há mais tempo no ar, que brecha sobra pro nosso cliente.

Só dado visto na biblioteca. Gasto e resultado do concorrente não aparecem lá: não estimar.
Próximo passo natural: `competitive-ads-extractor` (vários concorrentes) ou `bulk-creative`.
