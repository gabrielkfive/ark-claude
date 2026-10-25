# Pendências das sessões na nuvem (5/9 a 25/10/2026)

Levantado em 25/10 lendo as 143 sessões de nuvem. Só o que ficou parado e depende do PC ou do Gabriel.

## Instalação (resolvido pelo atualizador automático, plugin 1.5.0)

Tudo que ele pediu pra instalar e não chegou ao PC está em `plugins/ark/skills-equipe.json`: skills de design, as do ranking de setembro, as 5 de tráfego (claude-ads e skills da ARK, que estavam paradas no ramo `claude/bom-dia-traffic-skill-hxh6ix` desde 23/10), Remotion, watch/video-analyzer, taste-skill, replica-skill, last30days, marketingskills, instagram-skills, social-media-research-skills.

Fica de fora de propósito: OpenClaw (segurança fraca), WhatsApp por API não oficial (número banido em 10/09).

## Pede o PC ou o Mac

| Data | Pedido | O que falta |
|---|---|---|
| 24/10 | Vídeo da ARK e do WorkFlowArk igual ao reel do Nubank (De4J0fexm9s) | Refazer no PC como réplica fiel cena por cena (ver replica-fiel) |
| 22/10 | 10 repos do post @aiagently | Agora no atualizador; conferir o log no PC |
| 22/10 | PR #40 do WorkFlowArk (layout de contrato em PDF) | Merge pendente |
| 20/10 | Paridade de skills PC e Mac (ramo `sync/skills-pc-2026-10-20` no ark-cerebro) | Instalar o plugin ark no Mac: o atualizador cuida do resto |
| 20/10 | Mac servidor 24/7 (Jarvis OS) | Passos com sudo (`pmset`) e Sessão Remota no Mac |
| 18/10 | phone-harness (controlar o celular) | Só no Mac com adb ou espelhamento do iPhone |
| 17/10 | vibe-coding-toolkit no WorkFlowArk (prompt 12) | Rodar no PC |
| 15/10 | Software pra ele narrar vídeos | VoiceStudio já instalado no PC (19/10): usar ele |
| 05/10 | Alexa + JARVIS (ramo `claude/alexa-claude-integration-ynmnqa` no ark-brain, HANDOFF-PC.md) | Publicar do PC |
| 28/09 | Deploy automático do Ark Brain (PR ark-brain#1) | Rodar do PC |

## Rodado no PC em 25/10 (madrugada)

- Atualizador: 26 de 26 itens de `skills-equipe.json` instalados.
- Ark Brain no ar em `20261025a-ponte-ditado`: PR ark-brain#1 e modo ditado da Alexa. O deploy automático segue falhando por falta do segredo `CLOUDFLARE_API_TOKEN` no GitHub.
- PR #40 do WorkFlowArk já estava mesclado em 22/10.
- vibe-coding-toolkit no PC: pnpm, fd, Codex CLI, Graphify e Ponytail. As skills de projeto já estavam no main.
- Reel do Nubank, versão Ark®, em `ENTREGAS/2026-10-25/ark/reel-replica-nubank`, com prova lado a lado. A versão WorkFlowArk espera o ok.
