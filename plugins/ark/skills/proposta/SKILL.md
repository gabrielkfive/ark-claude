---
name: proposta
description: Monta proposta comercial da ARK Content em HTML único na identidade real (Sora + Inter, #FEEF02, fundo #0A0A0A) usando o kit em MARCAS/ARK e o montar.py, e publica em Worker próprio. Use quando o Gabriel pedir proposta, orçamento, "monta a proposta pro <cliente>", documento comercial, ou quando um lead novo precisar de material pra fechar. Não use para planejamento estratégico (planejamento-estrategico) nem contrato (gerador de contratos do WorkFlowArk).
---

# Proposta comercial ARK

Proposta é produto, não texto novo. Nasce de uma pasta modelo, ganha CONFIG do cliente, passa no montador e sobe pra um Worker. Regra da casa: **toda proposta mostra material real com nome do cliente** ("somos uma produtora").

## Checklist

```
- [ ] 1. Escolher o modelo e copiar a pasta
- [ ] 2. Preencher CONFIG (cliente, briefing, preços, CTA WhatsApp)
- [ ] 3. Montar com montar.py e abrir
- [ ] 4. Montar com --final (trava se faltar cliente ou CTA)
- [ ] 5. Deploy em Worker + deploy-verificado
- [ ] 6. Registrar (memória + WorkFlowArk Comercial)
```

## 1. Modelos existentes (em `Documents/ARK CONTENT/PROPOSTAS/`)

| Pasta | Serve para |
|---|---|
| `proposta-audiovisual/` | produção de vídeo recorrente (R$ 2.000 com 1 produtor, R$ 3.000 com 2) |
| `proposta-cobertura-evento/` | evento pontual, com quadro "O que entendemos do seu evento" |
| `proposta-advocacia/` | serviço mensal com posicionamento (base para nichos) |
| `proposta-lider/`, `proposta-profox/` | exemplos completos já enviados, com deploy |

Copiar a pasta inteira: `proposta-<cliente-slug>/` com o `.src.html` renomeado.

## 2. CONFIG

Fica no fim do `.src.html`, bloco `const CONFIG = {...}`. Só isso muda por cliente: nome, data, briefing (o que entendemos), preços, e o CTA. CTA é sempre o WhatsApp do Saulo `5561995506006` com mensagem pronta, nunca `href="#"` (já saiu proposta assim, virou correção de emergência).

Texto: sem traço ou travessão (vírgula ou ponto), sem frase de efeito inventada, sem biografia do cliente que não veio do briefing. Amarelo é bisturi: uma palavra do título, o número, a tag.

## 3 e 4. Montar

```bash
cd "Documents/ARK CONTENT/PROPOSTAS/proposta-<slug>"
python "../../MARCAS/ARK/montar.py" proposta-<slug>.src.html            # rascunho, abre com duplo clique
python "../../MARCAS/ARK/montar.py" proposta-<slug>.src.html --final    # antes de enviar
```

O montador embute fonte, CSS, logo e imagens (base64, porque o Chrome bloqueia woff2 em file://) e **trava** em: travessão, recurso externo, classe começando com "ad", marcador solto, imagem faltando. Com `--final` recusa sem nome de cliente e sem link de CTA. Se travar, corrigir o `.src.html`, não o HTML gerado.

Conferir visual com screenshot (Playwright ou Chrome) antes do passo 5. Comparar com `proposta-lider/public/index.html`, que é a referência aprovada.

## 5. Deploy

Padrão: `public/index.html` + `wrangler.jsonc` com `{"name":"proposta-<slug>","assets":{"directory":"./public"}}`, deploy em `proposta-<slug>.arkcontent.workers.dev`. Marcador de build no HTML (`build-proposta-<slug>-AAAAMMDD-vN`). Depois, **usar a skill deploy-verificado**: curl na URL, conferir o marcador, screenshot. Só aí é "no ar".

## 6. Registrar

Memória do projeto (`proposta-<slug>.md`: valores, decisor, status, URL) e cartão na aba Comercial do WorkFlowArk (`/comercial`, propostas). PDF só se o cliente pedir: imprimir do Chrome, guardar em `public/`.

## Referências

Identidade e regras completas: `Documents/ARK CONTENT/MARCAS/ARK/MANUAL.md`. Acervo obrigatório de portfólio: Obsidian `ARK/Proposta sempre mostra material.md`. Histórico de rejeições que não podem voltar: fonte Syne ("fonte horrível"), Axiforma/#FFAA00 (nunca existiu), CTA vazio, proposta sem peça real.
