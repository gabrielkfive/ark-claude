---
name: kit-conceito-cinema
description: Use for any conceptual strategic plan, creative concept, visual identity, film aesthetic or creative script for an ARK client (cafés, restaurants, clinics, brands). It brings the local GitHub kit (design tokens, screenwriting in Fountain, film emulation and LUTs), the cinema references that become camera rules, the JEV ad X-ray method, and the structure of the Attraversiamo conceptual plan that Gabriel approved on 01/10/2026 ("trabalho de profissional").
---

# Kit conceito e cinema (ARK)

Approved model: the Attraversiamo conceptual plan, 01/10/2026.
- Source and builders: `Documents\ARK CONTENT\CLIENTES\ATRAVERSSIAMO\PLANEJAMENTO\outubro-conceitual\` (`plano-conceitual.src.html`, `conteudo.py`, `pesquisa\*.json`).
- Full internal version (Gabriel only): see that client's memory.

## Structure that worked (copy it)

1. **Thesis.** What the client really sells, in one sentence. Prove it with a real number from the client's own profile.
2. **Manifesto.** A short text built from the meaning of the brand name. Use only true facts.
3. **Concept as a system.** Three "travessias" or pillars. Every post, event and product belongs to one of them.
4. **Recurring series with its own name.** Example: "verbos da travessia", an Italian verb per action, written in Cinzel.
5. **Ritual of every action in 4 pieces.** Invite three days before, countdown the day before, live on the day, memory film the day after.
6. **Cinema that becomes a camera rule.** For each film, name the concrete element that a phone can replicate.
7. **References from Brazil of the same aesthetic and size.** 15 or more, each with a profile print, followers read on the day, a link, "what they do" and "what to steal".
8. **JEV X-ray.** Mine the Meta Ad Library and classify hook, offer, proof and format. An ad that runs for a long time is an ad that sells.
9. **Calendar, expansion in 3 horizons with cases that have sources, scripts, a capture map, and a kit.**

Run the research for items 7, 8 and 9 as three parallel agents. Only the references agent uses Chrome (it is logged in to Instagram). The JEV agent uses Playwright on the public Ad Library.

## Local GitHub kit (`C:\Users\USER\ark-claude\refs-github\`)

| Repo | Use |
|---|---|
| `style-dictionary` (CLI `npx style-dictionary`, global v5.5.5) | Brand palette, fonts and spacing as tokens in JSON, then generate CSS for HTML, menus and posts |
| `community-group` (DTCG) | Official naming standard for tokens |
| `awesome-design-systems` | Brand manual models (voice, color, type, photo rules) |
| `Fountain` + `afterwriting-labs` (CLI `afterwriting`, global) | Write scripts in Fountain text and export a film-style PDF: `afterwriting --source roteiro.fountain --pdf roteiro.pdf` |
| `t3mujinpack` | Film-stock emulation for photos (darktable styles) |
| `spectral_film_lut` | Generate a film LUT for phone video ("Italian summer") |
| `glsl-film-grain` | Real film grain |

Do not cite in a client deck: "awesome-screenwriting" and "awesome-cinematography" do not exist (404).

## Cinema that became a camera rule (confirmed sources)

- **Comer, Rezar, Amar (2010).** The last line is "Attraversiamo. It means: let's cross over". In the book it is the author's favorite Italian word.
- **Il Postino (1994).** Luis Bacalov won the Oscar for the score, which uses mandolin and bandoneon and has a track called "In Bicicletta".
- **Call Me By Your Name.** Shot with one 35mm lens and natural light. On a phone, lock the 1x lens and use no zoom.
- **Chef's Table.** Slow motion at 120 fps plus Vivaldi recomposed by Max Richter.
- **Ratatouille.** The bite that turns into a memory. Show the face before the dish.
- **Big Night (1996).** The final shot is about 5 minutes long, one fixed take. On a phone, use a tripod and a single shot.
- **Grand Budapest Hotel.** Center symmetry and the box as a character.
- **Amélie.** Remove blue, keep green, red and amber. The cinematographer was inspired by Juarez Machado.

## Rules

- Never invent a number. Every follower count, price or metric needs a source and the date it was read.
- Never use a dash as a separator. Use a comma or a period.
- The client version can be limited: render only the open part, and put a lock with titles only on the rest. Locked content never goes into the HTML that the client receives.
- Deliver as a local HTML file plus a Worker. Use the deploy-verificado skill.
