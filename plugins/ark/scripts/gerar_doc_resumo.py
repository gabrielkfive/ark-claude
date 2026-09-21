"""Gera o documento-resumo do plugin (skills, hooks, rotas, como usar) em HTML único.
Uso: python scripts/gerar_doc_resumo.py [saida.html]"""
import glob
import html
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
rotas = json.load(open('rotas.json', encoding='utf-8'))['rotas']
cat = json.load(open('catalogo-skills.json', encoding='utf-8'))
versao = json.load(open('.claude-plugin/plugin.json', encoding='utf-8'))['version']

skills = []
for d in sorted(glob.glob('skills/*/SKILL.md')):
    t = open(d, encoding='utf-8').read()
    fm = re.match(r'^---\n(.*?)\n---', t, re.S).group(1)
    nome = re.search(r'name:\s*(.+)', fm).group(1).strip()
    desc = re.search(r'description:\s*(.+)', fm).group(1).strip()
    novo = nome in ('proposta', 'relatorio-dia', 'all-hands', 'carrossel')
    faz, quando = (desc.split('. Use quando', 1) + [''])[:2]
    skills.append((nome, faz, ('Use quando' + quando) if quando else '', novo))

lin_sk = "".join(
    f"<tr><td><b>/{n}</b>{' <span class=tag>nova</span>' if v else ''}</td><td>{html.escape(f)}.</td><td class=mut>{html.escape(q)}</td></tr>"
    for n, f, q, v in skills)
lin_rt = "".join(
    f"<tr><td>{html.escape(x['quando'])}</td><td>{', '.join('<b>' + html.escape(s) + '</b>' for s in x['skills'])}</td></tr>"
    for x in rotas)

doc = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ark-claude {versao}</title>
<style>
:root{{--bg:#0b0b0d;--fg:#ececec;--mut:#9a9aa3;--acc:#f2c94c;--card:#151518;--line:#26262b;--ok:#4ade80}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Inter,system-ui,sans-serif;padding:0 16px}}
main{{max-width:1000px;margin:0 auto;padding:48px 0 96px}}h1{{font-size:36px;margin:0 0 6px;letter-spacing:-.02em}}
h2{{font-size:22px;margin:44px 0 14px;color:var(--acc)}}p{{margin:0 0 12px}}.mut{{color:var(--mut)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:12px 0}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin:10px 0}}th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{color:var(--mut);font-weight:600}}code{{background:#1d1d22;padding:2px 6px;border-radius:6px;font-size:13px}}
pre{{background:#1d1d22;border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:13px;overflow:auto;line-height:1.5}}
ol,ul{{padding-left:22px}}li{{margin:6px 0}}.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:18px 0}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}}.kpi b{{display:block;font-size:32px;letter-spacing:-.02em}}.kpi span{{color:var(--mut);font-size:13px}}
.tag{{display:inline-block;font-size:11px;padding:1px 7px;border-radius:99px;background:var(--acc);color:#000;font-weight:600;margin-left:6px}}
.big{{font-size:18px}}
</style></head><body><main>
<p class="mut">ARK Content · 21/09/2026</p>
<h1>ark-claude {versao}</h1>
<p class="big">O que foi construído, o que ele faz por você, e como usar.</p>

<div class="kpis">
<div class="kpi"><b>{len(skills)}</b><span>skills da ARK no plugin (4 novas)</span></div>
<div class="kpi"><b>5</b><span>hooks: 4 de qualidade + 1 roteador</span></div>
<div class="kpi"><b>{len(rotas)}</b><span>rotas do seu vocabulário</span></div>
<div class="kpi"><b>{len(cat)}</b><span>skills catalogadas, todas ligadas</span></div>
<div class="kpi"><b>0</b><span>skills ou plugins removidos</span></div>
</div>

<h2>1. Em uma frase</h2>
<div class="card"><p class="big">Você fala do seu jeito, o plugin descobre qual das {len(cat)} skills serve, me obriga a usar, e barra o entregável que sair errado (travessão, CDN, Artifact, "no ar" sem medir).</p>
<p>Tudo vive em um repositório só, <code>github.com/gabrielkfive/ark-claude</code> (privado), instalado como plugin no Claude Code. Mac e PC puxam a mesma coisa com <code>git pull</code>.</p></div>

<h2>2. Como usar (a partir da próxima sessão)</h2>
<div class="card">
<ol>
<li><b>Fale normal.</b> "monta a proposta pro Martino", "relatório de hoje", "carrossel do caso da Mazuchi", "prepara o all hands". O roteador injeta as skills que casam e eu abro a resposta com <b>"Usando <i>skill</i> pra ..."</b>.</li>
<li><b>Se eu não abrir com "Usando..."</b> num pedido de trabalho, o roteador não pegou. Me diga e eu adiciono a rota na hora (uma linha em <code>rotas.json</code>).</li>
<li><b>Comando direto ainda funciona:</b> <code>/proposta</code>, <code>/relatorio-dia</code>, <code>/all-hands</code>, <code>/carrossel</code>, <code>/maratona</code>, <code>/retomar</code>, e qualquer outra das {len(cat)} pelo nome.</li>
<li><b>Os hooks trabalham sozinhos.</b> Você não vê nada, exceto quando eu for corrigido por um deles.</li>
</ol></div>

<h2>3. As {len(skills)} skills da ARK</h2>
<div class="card"><table><tr><th>Skill</th><th>O que faz</th><th>Quando dispara</th></tr>{lin_sk}</table>
<p class="mut">As 4 novas nasceram das entregas reais: as propostas em PROPOSTAS/ e o montar.py, os relatórios de 31/08, 14/09 e 17/09, os dois All Hands no WorkFlowArk, e os carrosséis de setembro. Cada uma tem checklist, aponta pra ferramenta real e termina em verificação.</p></div>

<h2>4. Os 5 hooks</h2>
<div class="card"><table>
<tr><th>Hook</th><th>Quando roda</th><th>O que faz</th></tr>
<tr><td><b>roteador</b></td><td>a cada pedido seu</td><td>Casa o pedido com {len(rotas)} rotas curadas, com nomes de skill citados e com as descrições do catálogo. Me entrega até 6 candidatas com o motivo. "ok", "continua" e comandos <code>/</code> passam direto.</td></tr>
<tr><td><b>sem_travessao</b></td><td>depois de eu escrever .html/.md/.txt</td><td>Se tiver travessão, meio-traço ou linha de desenho, devolve como erro e eu corrijo na hora. Acabou a limpeza de emergência antes de apresentação.</td></tr>
<tr><td><b>sem_cdn</b></td><td>depois de eu escrever .html</td><td>Avisa se a página depende de script ou CSS de fora (a página não pode quebrar se o CDN cair).</td></tr>
<tr><td><b>sem_artifact</b></td><td>antes de publicar Artifact</td><td>Nega. Entregável é HTML local ou Worker próprio. Ler e listar Artifact continua liberado.</td></tr>
<tr><td><b>pronto_medido</b></td><td>quando eu termino a resposta</td><td>Se eu disse "no ar" ou "deployado" sem ter dado curl na URL de produção naquela rodada, a resposta volta pra eu medir antes.</td></tr>
</table>
<p class="mut">Os hooks ignoram tudo dentro de <code>.claude/</code>, <code>.agents/</code>, <code>ark-claude/</code>, <code>node_modules/</code> e da pasta temporária. Testados com entrada simulada, inclusive acento e caminho Windows.</p></div>

<h2>5. Ferramentas novas que vieram junto</h2>
<div class="card"><table>
<tr><th>Script</th><th>Uso</th></tr>
<tr><td><code>scripts/validar_entregavel.py arquivo.html --final</code></td><td>Reprova travessão, recurso externo, classe "ad", marcador solto, campo deixado em branco e marcação de pendência esquecida no texto. Rodei no relatório de 17/09 e achou uma pendência esquecida de verdade.</td></tr>
<tr><td><code>skills/relatorio-dia/scripts/extrair_sessoes.py 2026-09-20</code></td><td>Lista tudo que rodou no dia nas sessões do Claude Code: pedido, skills usadas, arquivos, deploys, URLs conferidas, commits, memórias. Era script descartável, virou fixo. Testado: achou as 4 sessões de 20/09.</td></tr>
<tr><td><code>scripts/gerar_catalogo.py</code></td><td>Regenera o índice das {len(cat)} skills da máquina. Rodar depois de instalar skill nova.</td></tr>
<tr><td><code>scripts/gerar_doc_resumo.py</code></td><td>Regenera este documento a partir do plugin.</td></tr>
</table></div>

<h2>6. Mapa de rotas (o que você fala, o que eu chamo)</h2>
<div class="card"><table><tr><th>Quando</th><th>Skills</th></tr>{lin_rt}</table>
<p class="mut">Regex completo em <code>~/ark-claude/plugins/ark/rotas.json</code>. As de cima ganham quando o limite de 6 estoura.</p></div>

<h2>7. O que não mudou</h2>
<div class="card"><ul>
<li>ECC, ruflo, superpowers, frontend-design, watch: todos ligados, como estavam.</li>
<li>Suas 14 skills locais e as 23 de terceiros: no lugar, nenhuma removida.</li>
<li>Memórias, CLAUDE.md, conectores: intactos. No CLAUDE.md entrou só a seção "Skills: usar, nunca remover".</li>
<li>Backup do settings antes de tudo: <code>~/.claude/settings.json.bak-20260921</code>.</li>
</ul></div>

<h2>8. Instalar no Mac</h2>
<div class="card"><pre>git clone https://github.com/gabrielkfive/ark-claude ~/ark-claude
claude plugin marketplace add ~/ark-claude
claude plugin install ark@ark-claude</pre>
<p>Precisa de <code>bash</code> e <code>python3</code> (o <code>run.sh</code> escolhe). Atualizar depois: <code>cd ~/ark-claude && git pull && claude plugin marketplace update ark-claude && claude plugin update ark@ark-claude</code>, e reiniciar a sessão.</p>
<p class="mut">No PC, mudança no plugin exige subir a versão em <code>plugin.json</code> e <code>marketplace.json</code>, <code>claude plugin update ark@ark-claude</code> e sessão nova. Sem o bump o cache fica na versão velha (aconteceu com a 1.0.0).</p></div>

<h2>9. O que vem depois</h2>
<div class="card"><ol>
<li><b>Usar de verdade.</b> A próxima proposta, o próximo relatório e o próximo carrossel são o teste das skills novas. O que falhar, eu ajusto na skill, não na conversa.</li>
<li><b>Rodada 3:</b> memória espelhada no vault do Obsidian (padrão agentcairn), pra ela seguir você entre Mac e PC sem depender da pasta do Claude de cada máquina.</li>
<li><b>Auditoria mensal:</b> <code>extrair_sessoes.py</code> em cada dia do mês mostra quais skills dispararam. Zero uso = eu não estou chamando, e a rota é ajustada.</li>
</ol></div>

<p class="mut">Documentos irmãos nesta pasta: <code>estudo-otimizacao-skills.html</code> (o estudo e a pesquisa) e <code>plano-ativacao-skills.html</code> (o mecanismo de ativação em detalhe).</p>
</main></body></html>'''

saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.expanduser('~'), 'Documents', 'ARK CONTENT', 'ESTUDOS', 'otimizacao-skills-2026-09', f'ark-claude-{versao}.html')
open(saida, 'w', encoding='utf-8').write(doc)
print(saida, '|', len(doc) // 1024, 'KB | travessoes:', sum(doc.count(c) for c in '—–─━'))
