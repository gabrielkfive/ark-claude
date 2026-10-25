from tv_som import transicao


def test_estado_igual_nao_dispara():
    assert transicao('off', 'off', 0) == ('off', 0, None)


def test_uma_leitura_nao_basta():
    assert transicao('off', 'on', 0) == ('off', 1, None)


def test_duas_leituras_ligou():
    assert transicao('off', 'on', 1) == ('on', 0, 'ligou')


def test_duas_leituras_desligou():
    assert transicao('on', 'off', 1) == ('off', 0, 'desligou')


def test_oscilacao_zera_contagem():
    assert transicao('off', 'off', 1) == ('off', 0, None)
