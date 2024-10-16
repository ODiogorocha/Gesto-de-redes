import nmap
import time
import json
import socket
import struct
from datetime import datetime

# Função para descobrir dispositivos na rede
def descobrir_dispositivos(rede="192.168.0.0/24"):  
    scanner_nmap = nmap.PortScanner()
    print(f"Escaneando a rede {rede}...")

    # Scaneia a rede com o argumento '-sn' (ping scan)
    try:
        scanner_nmap.scan(hosts=rede, arguments='-sn')  
    except Exception as e:
        print(f"Erro ao escanear a rede: {e}")
        return []

    dispositivos_encontrados = []
    for host in scanner_nmap.all_hosts():
        print(f"Dispositivo encontrado: {host}")  
        if 'mac' in scanner_nmap[host]['addresses']: 
            dispositivo = {
                "ip": host,
                "mac": scanner_nmap[host]['addresses']['mac'],
                "fabricante": scanner_nmap[host]['vendor'].get(scanner_nmap[host]['addresses']['mac'], "Desconhecido"),
                "primeira_descoberta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")     
            }
            dispositivos_encontrados.append(dispositivo)
    print(f"Dispositivos encontrados nesta varredura: {dispositivos_encontrados}")  
    return dispositivos_encontrados

# Função para obter o gateway padrão (roteador) da rede
def obter_gateway():
    with open("/proc/net/route") as arquivo_rotas:
        for linha in arquivo_rotas:
            campos = linha.strip().split()  
            if campos[1] != '00000000' or not int(campos[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(campos[2], 16)))

# Classificar dispositivos entre roteador e host
def classificar_dispositivos(dispositivos, ip_gateway):
    for dispositivo in dispositivos:
        if dispositivo['ip'] == ip_gateway:
            dispositivo['tipo'] = "Roteador"
        else:
            dispositivo['tipo'] = "Host"
    return dispositivos 

# Salvar histórico de dispositivos em um JSON 
def salvar_historico(dispositivos, arquivo_historico="historico.json"):
    if dispositivos: 
        try:
            with open(arquivo_historico, 'w') as arquivo:
                json.dump(dispositivos, arquivo, indent=4)
                print(f"Histórico salvo com {len(dispositivos)} dispositivos.")  
        except IOError as e:
            print(f"Erro ao salvar histórico: {e}")
    else:
        print("Nenhum dispositivo para salvar no histórico.")

# Carregar histórico
def carregar_historico(arquivo_historico="historico.json"):
    try:
        with open(arquivo_historico, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

# Detectar dispositivos novos e offline
def detectar_mudancas(dispositivos_atualizados, dispositivos_antigos):
    novos_dispositivos = [dispositivo for dispositivo in dispositivos_atualizados if dispositivo not in dispositivos_antigos]
    dispositivos_offline = [dispositivo for dispositivo in dispositivos_antigos if dispositivo not in dispositivos_atualizados]

    if novos_dispositivos:
        print("\nNovos dispositivos detectados:")
        exibir_dispositivos(novos_dispositivos)

    if dispositivos_offline:
        print("\nDispositivos offline:")
        exibir_dispositivos(dispositivos_offline)

# Exibir lista de dispositivos descobertos
def exibir_dispositivos(dispositivos):
    for dispositivo in dispositivos:
        print(f"IP: {dispositivo['ip']}, MAC: {dispositivo['mac']}, Fabricante: {dispositivo['fabricante']}, Primeira Descoberta: {dispositivo['primeira_descoberta']}")

# Coordena o programa
def executar_monitoramento():
    # Carrega histórico de descobertas anteriores
    historico_dispositivos = carregar_historico()

    # Obtém o gateway (roteador) de rede
    gateway = obter_gateway()
    print(f"Gateway (roteador) da rede: {gateway}")

    try:
        while True:
            # Descobre novos dispositivos
            dispositivos_atualizados = descobrir_dispositivos()

            # Classifica os dispositivos entre roteador e host
            dispositivos_atualizados = classificar_dispositivos(dispositivos_atualizados, gateway)

            # Detecta mudança de histórico
            if historico_dispositivos:
                detectar_mudancas(dispositivos_atualizados, historico_dispositivos)

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
