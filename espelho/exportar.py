"""Exporta o Claude Code deste PC para um kit que outra máquina importa (importar.py).

Gera dois destinos:
  <kit>/            vai para o repo PRIVADO gabrielkfive/ark-maquina (sem nenhum segredo)
  <segredos.json>   fica fora do git; passa para a outra máquina por pendrive ou RustDesk

Uso: python espelho/exportar.py [kit] [segredos.json]
"""
import json
import re
import shutil
import sys
from pathlib import Path

CASA = Path.home()
CLAUDE = CASA / '.claude'
KIT = Path(sys.argv[1]) if len(sys.argv) > 1 else CASA / 'ark-maquina'
SEGREDOS = Path(sys.argv[2]) if len(sys.argv) > 2 else CASA / 'Desktop' / 'segredos-claude.json'

# Caminhos deste PC viram marcadores; o importar.py troca pelos da máquina nova.
JARVIS_PC = 'C:/Users/USER/Documents/ARK CONTENT/SOFTWARE/ark-jarvis'
TROCAS = [(JARVIS_PC, '{JARVIS}'), (JARVIS_PC.replace('/', '\\'), '{JARVIS}'),
          (str(CASA).replace('\\', '/'), '{CASA}'), (str(CASA), '{CASA}')]
# MCP que só faz sentido aqui (programa ou pasta que o notebook não tem).
SO_NESTE_PC = {'davinci-resolve', 'obsidian'}


def marcar(texto):
    for de, para in TROCAS:
        texto = texto.replace(de, para)
    return texto


def ler(p):
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    if KIT.exists():
        for filho in KIT.iterdir():
            if filho.name != '.git':
                shutil.rmtree(filho) if filho.is_dir() else filho.unlink()
    KIT.mkdir(parents=True, exist_ok=True)
    segredos = {}

    # Skills soltas (links resolvidos) e hooks
    shutil.copytree(CLAUDE / 'skills', KIT / 'skills', symlinks=False,
                    ignore=shutil.ignore_patterns('.claude-flow', '__pycache__', 'node_modules'))
    shutil.copytree(CLAUDE / 'hooks', KIT / 'hooks', ignore=shutil.ignore_patterns('__pycache__'))
    for md in ('CLAUDE.md', 'RTK.md'):
        if (CLAUDE / md).exists():
            shutil.copy2(CLAUDE / md, KIT / md)
    rtk = shutil.which('rtk')
    if rtk:
        (KIT / 'bin').mkdir(exist_ok=True)
        shutil.copy2(rtk, KIT / 'bin' / 'rtk.exe')

    # Plugins: marketplaces de GitHub mais o ark-claude local
    mercados = {}
    for nome, m in ler(CLAUDE / 'plugins' / 'known_marketplaces.json').items():
        src = m.get('source', {})
        mercados[nome] = src.get('repo') or src.get('url') or marcar(src.get('path', ''))
    plugins = list(ler(CLAUDE / 'plugins' / 'installed_plugins.json')['plugins'].keys())
    (KIT / 'plugins.json').write_text(json.dumps({'marketplaces': mercados, 'plugins': plugins},
                                                 indent=2, ensure_ascii=False), encoding='utf-8')

    # MCP de usuário: valores de env, headers e token em URL saem para segredos.json
    mcps = {}
    for nome, cfg in ler(CASA / '.claude.json').get('mcpServers', {}).items():
        if nome in SO_NESTE_PC:
            continue
        cfg = json.loads(json.dumps(cfg))
        for campo in ('env', 'headers'):
            for k, v in (cfg.get(campo) or {}).items():
                if re.search(r'KEY|TOKEN|SECRET|Authorization', k, re.I):
                    segredos[f'{nome}.{campo}.{k}'] = v
                    cfg[campo][k] = f'{{SEGREDO:{nome}.{campo}.{k}}}'
        url = cfg.get('url', '')
        m = re.search(r'([?&](?:token|key)=)([^&]+)', url)
        if m:
            segredos[f'{nome}.url'] = m.group(2)
            cfg['url'] = url.replace(m.group(2), f'{{SEGREDO:{nome}.url}}')
        mcps[nome] = json.loads(marcar(json.dumps(cfg, ensure_ascii=False)))
    (KIT / 'mcp.json').write_text(json.dumps(mcps, indent=2, ensure_ascii=False), encoding='utf-8')

    # settings.json com caminhos marcados
    (KIT / 'settings.json').write_text(marcar((CLAUDE / 'settings.json').read_text(encoding='utf-8')),
                                       encoding='utf-8')

    # Arquivos de token soltos
    for rel in ('.config/ark-brain/token',):
        p = CASA / rel
        if p.exists():
            segredos[f'arquivo:{rel}'] = p.read_text(encoding='utf-8').strip()

    # Prova: nenhum valor secreto dentro do kit
    for arq in KIT.rglob('*'):
        if arq.is_file() and arq.suffix in ('.json', '.md', '.py', '.ps1', '.mjs', '.txt'):
            texto = arq.read_text(encoding='utf-8', errors='ignore')
            for v in segredos.values():
                if v and len(v) > 8 and v in texto:
                    sys.exit(f'PARADO: segredo vazou em {arq}')
    SEGREDOS.write_text(json.dumps(segredos, indent=2), encoding='utf-8')
    n_skills = sum(1 for _ in (KIT / 'skills').glob('*/'))
    print(f'kit: {KIT} | skills soltas {n_skills} | plugins {len(plugins)} | mcp {len(mcps)} | segredos {len(segredos)} em {SEGREDOS}')


if __name__ == '__main__':
    main()
