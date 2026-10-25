import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import servidor as s

ACOES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'acoes.json'), encoding='utf-8'))


def ids(texto):
    a = s.casar(texto, ACOES)
    return a and a['id']


def test_desliga_nao_casa_com_liga():
    assert ids('Jarvis, desliga o ar-condicionado') == 'ar-desligar'
    assert ids('jarvis liga o ar') == 'ar-ligar'


def test_acento_e_maiuscula():
    assert ids('LIGA O PC') == 'pc-ligar'
    assert ids('O que tem na fila?') == 'fila'


def test_frase_livre_vira_pedido():
    assert ids('Jarvis, coloca na agenda: aqui é o Lucas, demanda da Vivenda') is None


def test_expandir_sem_variavel_fica_vazio():
    assert s.expandir('${NAO_EXISTE}', {}) == ''


def test_url_nao_configurada_avisa():
    try:
        s.executar({'id': 'x', 'tipo': 'url', 'url': '${VAZIO}'}, {})
        assert False
    except RuntimeError as e:
        assert 'não configurada' in str(e)
