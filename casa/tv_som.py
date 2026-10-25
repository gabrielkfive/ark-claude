"""Liga o som junto com a TV.

Lê o estado da Samsung pela rede (porta 8001) e, quando ela liga ou desliga,
chama a URL do Voice Monkey que dispara a rotina da Alexa (IR do mini system).

Config em casa/tv_som.env (fora do git):
  TV_IP=192.168.0.33
  URL_LIGOU=https://api-v3.voicemonkey.io/trigger?token=...&device=tv-ligou-l1jb3
  URL_DESLIGOU=https://api-v3.voicemonkey.io/trigger?token=...&device=tv-desligou-vdqjx
"""
import json, os, sys, time, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(AQUI, 'tv_som.log')


def ler_env(caminho):
    cfg = {}
    if os.path.exists(caminho):
        for linha in open(caminho, encoding='utf-8'):
            linha = linha.strip()
            if linha and not linha.startswith('#') and '=' in linha:
                k, v = linha.split('=', 1)
                cfg[k.strip()] = v.strip()
    return cfg


def estado_tv(ip):
    """'on' só com a TV ligada de verdade; standby ou sem resposta = 'off'."""
    try:
        with urllib.request.urlopen('http://%s:8001/api/v2/' % ip, timeout=3) as r:
            dev = json.load(r).get('device', {})
        return 'on' if dev.get('PowerState', 'on') == 'on' else 'off'
    except Exception:
        return 'off'


def transicao(anterior, atual, confirmacoes, precisa=2):
    """Só troca de estado depois de `precisa` leituras iguais seguidas.
    Retorna (novo_estado, confirmacoes, evento ou None)."""
    if atual == anterior:
        return anterior, 0, None
    confirmacoes += 1
    if confirmacoes < precisa:
        return anterior, confirmacoes, None
    return atual, 0, ('ligou' if atual == 'on' else 'desligou')


def log(msg):
    linha = time.strftime('%Y-%m-%d %H:%M:%S ') + msg
    print(linha, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(linha + '\n')


def disparar(url):
    if not url:
        return 'sem URL'
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return 'HTTP %s' % r.status
    except Exception as e:
        return 'erro %s' % e


def main():
    cfg = ler_env(os.path.join(AQUI, 'tv_som.env'))
    ip = cfg.get('TV_IP', '192.168.0.33')
    estado = estado_tv(ip)  # estado inicial não dispara nada
    conf = 0
    log('vigiando %s, TV %s' % (ip, estado))
    while True:
        time.sleep(3)
        estado, conf, ev = transicao(estado, estado_tv(ip), conf)
        if ev:
            log('TV %s: %s' % (ev, disparar(cfg.get('URL_LIGOU' if ev == 'ligou' else 'URL_DESLIGOU'))))


if __name__ == '__main__':
    if sys.argv[1:] == ['estado']:
        print(estado_tv(ler_env(os.path.join(AQUI, 'tv_som.env')).get('TV_IP', '192.168.0.33')))
    else:
        main()
