"""Painel JARVIS do escritório: tela touch, iPad, Ulanzi e Alexa apertam o mesmo botão.

Roda no notebook central (Yoga). Serve a página e executa as ações de acoes.json.
  GET  /                 painel
  GET  /api/acoes        lista de botões
  GET|POST /api/acao/ID  executa (GET existe para o Ulanzi, que só abre URL)
  POST /api/falar        {"texto": "..."}: frase que bate com um botão executa; resto vira pedido do JARVIS

Segredos em casa/painel/painel.env (fora do git). acoes.json usa ${NOME} para lê-los.
  PAINEL_CHAVE=...        exigida em ?chave= ou cabeçalho X-Chave (vazia = rede local livre)
  ARK_BRAIN_URL=https://ark-brain.arkcontent.workers.dev
  ARK_BRAIN_TOKEN=...
  VM_AR_LIGAR=https://api-v3.voicemonkey.io/trigger?token=...&device=ar-ligar
Uso: python servidor.py [porta]   (padrão 8095)
"""
import json, os, re, socket, subprocess, sys, unicodedata, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
from acordar_pc import acordar  # noqa: E402
from tv_som import ler_env  # noqa: E402


def normalizar(t):
    t = unicodedata.normalize('NFD', t.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = re.sub(r'^\s*(ok\s+)?jarvis[\s,]*', '', t)
    return re.sub(r'[^a-z0-9 ]', ' ', t).split()


def expandir(valor, env):
    return re.sub(r'\$\{(\w+)\}', lambda m: env.get(m.group(1), ''), valor)


def casar(texto, acoes):
    """Ação cuja frase aparece inteira no que foi dito; a frase mais longa ganha."""
    falado = ' %s ' % ' '.join(normalizar(texto))
    melhor, tam = None, 0
    for a in acoes:
        for f in a.get('frases', []):
            f = ' '.join(normalizar(f))
            if f and ' %s ' % f in falado and len(f) > tam:
                melhor, tam = a, len(f)
    return melhor


def http(url, corpo=None, token=None):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode() if corpo is not None else None)
    req.add_header('content-type', 'application/json')
    if token:
        req.add_header('authorization', 'Bearer ' + token)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


def pedido_jarvis(texto, env):
    base = env.get('ARK_BRAIN_URL', '').rstrip('/')
    if not base or not env.get('ARK_BRAIN_TOKEN'):
        raise RuntimeError('ARK_BRAIN_URL ou ARK_BRAIN_TOKEN faltando no painel.env')
    http(base + '/api/acao/pedido_criar', {'texto': '[Painel do escritório] ' + texto}, env['ARK_BRAIN_TOKEN'])
    return 'Anotado. O JARVIS já recebeu.'


def executar(acao, env):
    tipo = acao['tipo']
    if tipo == 'url':
        url = expandir(acao['url'], env)
        if not url.startswith('http'):
            raise RuntimeError('URL da ação %s não configurada no painel.env' % acao['id'])
        http(url)
    elif tipo == 'wol':
        acordar(expandir(acao['mac'], env))
    elif tipo == 'cmd':
        subprocess.Popen(expandir(acao['cmd'], env), shell=True)
    elif tipo == 'jarvis':
        return pedido_jarvis(acao['texto'], env)
    else:
        raise RuntimeError('tipo desconhecido: %s' % tipo)
    return acao.get('resposta', 'Feito.')


def carregar():
    with open(os.path.join(AQUI, 'acoes.json'), encoding='utf-8') as f:
        return json.load(f)


class Painel(BaseHTTPRequestHandler):
    env = {}

    def log_message(self, *a):
        pass

    def responder(self, cod, obj, tipo='application/json; charset=utf-8'):
        corpo = obj if isinstance(obj, bytes) else json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(cod)
        self.send_header('content-type', tipo)
        self.send_header('cache-control', 'no-store')
        self.end_headers()
        self.wfile.write(corpo)

    def autorizado(self):
        chave = self.env.get('PAINEL_CHAVE', '')
        q = re.search(r'[?&]chave=([^&]+)', self.path)
        return not chave or self.headers.get('x-chave') == chave or (q and q.group(1) == chave)

    def rota(self):
        p = self.path.split('?')[0]
        if p in ('/', '/index.html'):
            with open(os.path.join(AQUI, 'index.html'), 'rb') as f:
                return self.responder(200, f.read(), 'text/html; charset=utf-8')
        if not self.autorizado():
            return self.responder(401, {'erro': 'chave do painel errada'})
        acoes = carregar()
        try:
            if p == '/api/acoes':
                return self.responder(200, [{k: a.get(k) for k in ('id', 'nome', 'icone', 'aparelho')} for a in acoes])
            m = re.match(r'^/api/acao/([\w-]+)$', p)
            if m:
                a = next((x for x in acoes if x['id'] == m.group(1)), None)
                if not a:
                    return self.responder(404, {'erro': 'ação não existe'})
                return self.responder(200, {'ok': True, 'fala': executar(a, self.env)})
            if p == '/api/falar' and self.command == 'POST':
                n = int(self.headers.get('content-length') or 0)
                texto = (json.loads(self.rfile.read(n) or b'{}').get('texto') or '').strip()
                if not texto:
                    return self.responder(400, {'erro': 'texto vazio'})
                a = casar(texto, acoes)
                fala = executar(a, self.env) if a else pedido_jarvis(texto, self.env)
                return self.responder(200, {'ok': True, 'acao': a and a['id'], 'fala': fala})
        except Exception as e:  # erro vira fala na tela, servidor segue de pé
            return self.responder(500, {'erro': str(e)})
        self.responder(404, {'erro': 'rota'})

    do_GET = do_POST = rota


def ip_local():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]


if __name__ == '__main__':
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8095
    Painel.env = {**os.environ, **ler_env(os.path.join(AQUI, 'painel.env'))}
    print('painel em http://%s:%d' % (ip_local(), porta))
    ThreadingHTTPServer(('0.0.0.0', porta), Painel).serve_forever()
