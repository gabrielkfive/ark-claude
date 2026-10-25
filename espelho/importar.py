"""Importa na máquina nova o kit gerado pelo exportar.py (repo privado gabrielkfive/ark-maquina).

Rode num PowerShell FORA do app Claude Desktop (no Windows 10 o app é MSIX e esconde o AppData).
Uso: python espelho/importar.py [kit] [segredos.json]
Sem segredos.json, os MCP que pedem chave ficam de fora e aparecem no relatório.
"""
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

CASA = Path.home()
CLAUDE = CASA / '.claude'
KIT = Path(sys.argv[1]) if len(sys.argv) > 1 else CASA / 'ark-maquina'
SEGREDOS = Path(sys.argv[2]) if len(sys.argv) > 2 else CASA / 'Desktop' / 'segredos-claude.json'
JARVIS = (CASA / 'ark-jarvis').as_posix()
relatorio = []


def trocar(texto):
    return texto.replace('{JARVIS}', JARVIS).replace('{CASA}', CASA.as_posix())


def claude(*args):
    r = subprocess.run(['claude', *args], capture_output=True, text=True, encoding='utf-8', errors='replace',
                       shell=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def main():
    segredos = json.loads(SEGREDOS.read_text(encoding='utf-8')) if SEGREDOS.exists() else {}
    carimbo = time.strftime('%Y%m%d-%H%M%S')

    # Skills, hooks e instruções globais (o que já existe vai para .bak antes)
    CLAUDE.mkdir(exist_ok=True)
    shutil.copytree(KIT / 'skills', CLAUDE / 'skills', dirs_exist_ok=True)
    shutil.copytree(KIT / 'hooks', CLAUDE / 'hooks', dirs_exist_ok=True)
    for md in ('CLAUDE.md', 'RTK.md'):
        if (KIT / md).exists():
            if (CLAUDE / md).exists():
                shutil.copy2(CLAUDE / md, CLAUDE / f'{md}.bak-{carimbo}')
            shutil.copy2(KIT / md, CLAUDE / md)
    relatorio.append(f'skills soltas: {sum(1 for _ in (KIT / "skills").glob("*/"))}')

    # rtk (proxy de comandos usado pelo hook do Bash)
    if (KIT / 'bin' / 'rtk.exe').exists():
        destino = CASA / '.local' / 'bin'
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy2(KIT / 'bin' / 'rtk.exe', destino / 'rtk.exe')
        relatorio.append(f'rtk: {destino} (confira se está no PATH)')

    # settings.json
    if (CLAUDE / 'settings.json').exists():
        shutil.copy2(CLAUDE / 'settings.json', CLAUDE / f'settings.json.bak-{carimbo}')
    (CLAUDE / 'settings.json').write_text(trocar((KIT / 'settings.json').read_text(encoding='utf-8')),
                                          encoding='utf-8')

    # Plugins
    p = json.loads((KIT / 'plugins.json').read_text(encoding='utf-8'))
    for nome, fonte in p['marketplaces'].items():
        fonte = trocar(fonte)
        if nome == 'ark-claude':
            fonte = str(CASA / 'ark-claude')
        ok, saida = claude('plugin', 'marketplace', 'add', fonte)
        if not ok and 'already' not in saida.lower():
            relatorio.append(f'marketplace {nome}: FALHOU {saida[-160:]}')
    for plugin in p['plugins']:
        ok, saida = claude('plugin', 'install', plugin)
        relatorio.append(f'plugin {plugin}: {"ok" if ok or "already" in saida.lower() else "FALHOU " + saida[-160:]}')

    # MCP de usuário
    for nome, cfg in json.loads((KIT / 'mcp.json').read_text(encoding='utf-8')).items():
        texto = trocar(json.dumps(cfg, ensure_ascii=False))
        faltam = [k for k in re.findall(r'\{SEGREDO:([^}]+)\}', texto) if k not in segredos]
        if faltam:
            relatorio.append(f'mcp {nome}: SEM CHAVE ({", ".join(faltam)})')
            continue
        texto = re.sub(r'\{SEGREDO:([^}]+)\}', lambda m: segredos[m.group(1)], texto)
        claude('mcp', 'remove', '-s', 'user', nome)
        ok, saida = claude('mcp', 'add-json', '-s', 'user', nome, texto)
        relatorio.append(f'mcp {nome}: {"ok" if ok else "FALHOU " + saida[-160:]}')

    # Arquivos de token
    for chave, valor in segredos.items():
        if chave.startswith('arquivo:'):
            alvo = CASA / chave.split(':', 1)[1]
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(valor, encoding='utf-8')
            relatorio.append(f'token: {alvo}')

    print('\n'.join(relatorio))
    if segredos:
        print(f'\nApague {SEGREDOS} depois de conferir (tem chaves).')


if __name__ == '__main__':
    main()
