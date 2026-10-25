"""Acorda o PC do Gabriel por Wake on LAN.

Roda numa máquina que fica ligada (notebook central ou Mac), disparado pelo
TriggerCMD dela com a frase "LIGAR PC".
Uso: python acordar_pc.py [MAC]
"""
import socket, sys

MAC_PC = '74:56:3C:F5:A6:C7'  # Realtek 2.5GbE do COMPUTADOR


def pacote_magico(mac):
    b = bytes.fromhex(mac.replace(':', '').replace('-', ''))
    if len(b) != 6:
        raise ValueError('MAC inválido: %s' % mac)
    return b'\xff' * 6 + b * 16


def acordar(mac=MAC_PC):
    p = pacote_magico(mac)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for porta in (9, 7):
            s.sendto(p, ('255.255.255.255', porta))
            s.sendto(p, ('192.168.0.255', porta))


if __name__ == '__main__':
    acordar(sys.argv[1] if len(sys.argv) > 1 else MAC_PC)
    print('pacote enviado')
