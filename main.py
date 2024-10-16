import nmap
import time
import json
import socket
import struct
from datetime import datetime

# Função para descobrir dispositivos na rede
def descobrir_dispositivos(rede="192.168.1.0/24"):
    scanner_nmap = nmap.PortScanner()
    print(f"Escaneando a rede {rede}...")

    # Scaneia a rede com o argumento '-sn' (ping scan)
    scanner_nmap.scan(hosts=rede, arguments='-sn')

    dispositivos_encontrados = []
    for host in scanner_nmap.all_hosts():
        if 'mac' in scanner_nmap[host]['addresses']:  # Verifica se o dispositivo tem o endereço MAC
            dispositivo = {
                "ip": host,
                "mac": scanner_nmap[host]['addresses']['mac'],
                "fabricante": scanner_nmap[host]['vendor'].get(scanner_nmap[host]['addresses']['mac'], "Desconhecido"),
                "primeira_descoberta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            dispositivos_encontrados.append(dispositivo)
    return dispositivos_encontrados

# Função para obter o Gateway padrão (roteador) da rede
def obter_gateway():
    with open("/proc/net/route") as arquivo_rotas:
        for linha in arquivo_rotas:
            campos = linha.strip().split()
            if campos[1] != '00000000' or not int(campos[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(campos[2], 16)))

# Função para classificar dispositivos entre roteador e host
def classificar_dispositivos(dispositivos, ip_gateway):
    for dispositivo in dispositivos:
        if dispositivo['ip'] == ip_gateway:
            dispositivo['tipo'] = "Roteador"
        else:
            dispositivo['tipo'] = "Host"
    return dispositivos

# Função para salvar o histórico de dispositivos em um arquivo JSON
def salvar_historico(dispositivos, arquivo_historico="historico.json"):
    with open(arquivo_historico, 'w') as arquivo:
        json.dump(dispositivos, arquivo, indent=4)

# Função para carregar o histórico salvo do arquivo JSON
def carregar_historico(arquivo_historico="historico.json"):
    try:
        with open(arquivo_historico, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

# Função para detectar novos dispositivos e dispositivos offline
def detectar_mudancas(dispositivos_atualizados, dispositivos_antigos):
    novos_dispositivos = [dispositivo for dispositivo in dispositivos_atualizados if dispositivo not in dispositivos_antigos]
    dispositivos_offline = [dispositivo for dispositivo in dispositivos_antigos if dispositivo not in dispositivos_atualizados]

    if novos_dispositivos:
        print("\nNovos dispositivos detectados:")
        exibir_dispositivos(novos_dispositivos)

    if dispositivos_offline:
        print("\nDispositivos offline:")
        exibir_dispositivos(dispositivos_offline)

# Função para exibir a lista de dispositivos descobertos
def exibir_dispositivos(dispositivos):
    for dispositivo in dispositivos:
        print(f"IP: {dispositivo['ip']}, MAC: {dispositivo['mac']}, FABRICANTE: {dispositivo['fabricante']}, PRIMEIRA DESCOBERTA: {dispositivo['primeira_descoberta']}")

# Função principal que coordena o programa
def executar_monitoramento():
    # Carrega o histórico de descobertas anteriores
    historico_dispositivos = carregar_historico()

    # Obtém o gateway (roteador) da rede
    gateway = obter_gateway()
    print(f"Gateway (roteador) da rede: {gateway}")

    try:
        while True:
            # Descobre novos dispositivos
            dispositivos_atualizados = descobrir_dispositivos()

            # Classifica os dispositivos entre roteador e hosts
            dispositivos_atualizados = classificar_dispositivos(dispositivos_atualizados, gateway)

            # Detecta mudanças em relação ao histórico anterior
            if historico_dispositivos:
                detectar_mudancas(dispositivos_atualizados, historico_dispositivos)

            # Exibe os dispositivos descobertos
            exibir_dispositivos(dispositivos_atualizados)

            # Atualiza o histórico e salva no arquivo
            historico_dispositivos = dispositivos_atualizados
            salvar_historico(historico_dispositivos)

            # Timer entre scans
            time.sleep(60)

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")

if __name__ == "__main__":
    executar_monitoramento()
