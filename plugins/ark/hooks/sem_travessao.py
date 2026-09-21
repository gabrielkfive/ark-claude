"""Bloqueia travessão, meio-traço e linha de desenho em entregável (.html/.md/.txt).
Regra do Gabriel: separar ideia com vírgula ou ponto, intervalo com "a". Nunca traço."""
from _common import ler_entrada, caminho_do_arquivo, eh_entregavel, ler_texto, bloquear_pos

PROIBIDOS = {"—": "travessão (—)", "–": "meio-traço (–)", "─": "linha ─", "━": "linha ━", "═": "linha ═"}

entrada = ler_entrada()
caminho = caminho_do_arquivo(entrada)
if not eh_entregavel(caminho):
    raise SystemExit(0)

texto = ler_texto(caminho)
achados = []
for i, linha in enumerate(texto.splitlines(), 1):
    for ch, nome in PROIBIDOS.items():
        if ch in linha:
            achados.append(f"  linha {i}: {nome}: {linha.strip()[:90]}")
            break
    if len(achados) >= 8:
        break

if achados:
    bloquear_pos(
        f"[ark] ENTREGÁVEL COM TRAÇO PROIBIDO: {caminho}\n"
        + "\n".join(achados)
        + "\nRegra: trocar por vírgula ou ponto; intervalo vira 'X a Y'; divisor visual sai. Corrija o arquivo agora.\n"
    )
