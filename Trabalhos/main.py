import nmap
import socket
import json
import os
from datetime import datetime

# Função para carregar a lista de fabricantes OUI a partir do arquivo "mac.txt"
def carregar_lista_fabricantes(arquivo_oui="mac.txt"):
    lista_fabricantes = {}
    if os.path.isfile(arquivo_oui):
        try:
            with open(arquivo_oui, 'r') as arquivo:
                for linha in arquivo:
                    partes = linha.strip().split(maxsplit=1)
                    if len(partes) == 2:
                        oui, fabricante = partes
                        lista_fabricantes[oui.upper()] = fabricante
            print(f"Lista de fabricantes carregada com sucesso. Total: {len(lista_fabricantes)}")
        except Exception as e:
            print(f"Erro ao carregar o arquivo de fabricantes OUI: {e}")
    else:
        print(f"Arquivo {arquivo_oui} não encontrado.")
    return lista_fabricantes

# Função para obter o fabricante a partir do MAC
def obter_fabricante_por_mac(mac, lista_fabricantes):
    oui = mac[:8].upper()
    return lista_fabricantes.get(oui, "Desconhecido")

# Função para descobrir dispositivos na rede
def descobrir_dispositivos(rede="192.168.0.0/24", lista_fabricantes={}): 
    scanner_nmap = nmap.PortScanner()
    print(f"Escaneando a rede {rede}...")

    try:
        scanner_nmap.scan(hosts=rede, arguments='-sn')  # -sn faz um ping scan
    except Exception as e:
        print(f"Erro ao escanear a rede: {e}")
        return []

    dispositivos_encontrados = []
    for host in scanner_nmap.all_hosts():
        status = "Online" if scanner_nmap[host].state() == "up" else "Offline"
        mac = scanner_nmap[host]['addresses'].get('mac', 'Desconhecido')
        fabricante = obter_fabricante_por_mac(mac, lista_fabricantes) if mac != 'Desconhecido' else 'Desconhecido'
        dispositivo = {
            "ip": host,
            "mac": mac,
            "fabricante": fabricante,
            "status": status, 
            "primeira_descoberta": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        }
        dispositivos_encontrados.append(dispositivo)
        print(f"Dispositivo encontrado: {dispositivo}") 
    return dispositivos_encontrados

# Função para obter o endereço da rede local automaticamente
def obter_rede_local():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip_local = sock.getsockname()[0]
        sock.close()

        partes_ip = ip_local.split('.')
        partes_ip[3] = '0'
        rede = '.'.join(partes_ip) + "/24"
        return rede
    except Exception as e:
        print(f"Erro ao obter a rede local: {e}")
        return "192.168.0.0/24"

# Função para salvar os dispositivos descobertos em um arquivo JSON
def salvar_em_json(dispositivos, arquivo="dispositivos.json"):
    try:
        with open(arquivo, 'w') as f:
            json.dump(dispositivos, f, indent=4)
        print(f"Dispositivos salvos em {arquivo}")
    except Exception as e:
        print(f"Erro ao salvar dispositivos no arquivo JSON: {e}")

# Função para rodar a varredura e salvar os dados
def executar_varredura():
    lista_fabricantes = carregar_lista_fabricantes('./mac.txt') 
    rede_local = obter_rede_local()
    dispositivos = descobrir_dispositivos(rede=rede_local, lista_fabricantes=lista_fabricantes)
    salvar_em_json(dispositivos)
    print("Varredura concluída. Dados salvos em dispositivos.json.")

if __name__ == "__main__":
    executar_varredura()
