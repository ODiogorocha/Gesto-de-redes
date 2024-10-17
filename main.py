#importacao  de bibliotecas necessarias 
import nmap
import time
import json
import socket
import struct
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

# Funcao para descobrir dispositivos na rede
def descobrir_dispositivos(rede="192.168.0.0/24"):  
    scanner_nmap = nmap.PortScanner()
    print(f"Escaneando a rede {rede}...")

    try:
        scanner_nmap.scan(hosts=rede, arguments='-sn')  
    except Exception as e:
        print(f"Erro ao escanear a rede: {e}")
        return []

    dispositivos_encontrados = []
    for host in scanner_nmap.all_hosts():
        # Obter o nome do dispositivo via DNS reverso
        try:
            nome_dispositivo = socket.gethostbyaddr(host)[0]  # DNS reverso para obter o nome
        except socket.herror:
            nome_dispositivo = "Desconhecido"  # Caso não consiga obter o nome via DNS

        # Obter o endereço MAC e o fabricante
        mac_address = scanner_nmap[host]['addresses'].get('mac', 'Desconhecido')
        fabricante = scanner_nmap[host]['vendor'].get(mac_address, 'Desconhecido')

        dispositivo = {
            "ip": host,
            "nome": nome_dispositivo,
            "mac": mac_address,
            "fabricante": fabricante,
            "primeira_descoberta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        dispositivos_encontrados.append(dispositivo)

        # Exibir informações no terminal
        print(f"Dispositivo encontrado: IP: {host}, Nome: {nome_dispositivo}, MAC: {mac_address}, Fabricante: {fabricante}")

    print(f"Dispositivos encontrados nesta varredura: {dispositivos_encontrados}")  
    return dispositivos_encontrados

# Funcao para obter o gateway padrão (roteador) da rede
def obter_gateway():
    try:
        with open("/proc/net/route") as arquivo_rotas:
            for linha in arquivo_rotas:
                campos = linha.strip().split()  
                if campos[1] != '00000000' or not int(campos[3], 16) & 2:
                    continue
                return socket.inet_ntoa(struct.pack("<L", int(campos[2], 16)))
    except Exception as e:
        print(f"Erro ao obter gateway: {e}")
        return None

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
        print("Arquivo de histórico não encontrado, criando novo.")
        return []
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON. Criando um novo arquivo.")
        return []

# Detectar dispositivos novos e offline
def detectar_mudancas(dispositivos_atualizados, dispositivos_antigos):
    novos_dispositivos = [dispositivo for dispositivo in dispositivos_atualizados if dispositivo not in dispositivos_antigos]
    dispositivos_offline = [dispositivo for dispositivo in dispositivos_antigos if dispositivo not in dispositivos_atualizados]

    return novos_dispositivos, dispositivos_offline

# Exibir lista de dispositivos descobertos na interface
def exibir_dispositivos_na_interface(dispositivos, titulo="Dispositivos Descobertos"):
    if not dispositivos:
        area_texto.insert(tk.END, f"{titulo}: Nenhum dispositivo encontrado.\n")
    else:
        area_texto.insert(tk.END, f"{titulo}:\n")
        for dispositivo in dispositivos:
            area_texto.insert(tk.END, f"IP: {dispositivo['ip']}, Nome: {dispositivo['nome']}, MAC: {dispositivo['mac']}, "
                                        f"Fabricante: {dispositivo['fabricante']}, "
                                        f"Primeira Descoberta: {dispositivo['primeira_descoberta']}\n")
    area_texto.insert(tk.END, "\n")  # Adiciona uma linha vazia para separar os grupos
    area_texto.yview(tk.END)  # Move a barra de rolagem para o final

# Coordena o programa de monitoramento
def executar_monitoramento():
    # Carrega histórico de descobertas anteriores
    historico_dispositivos = carregar_historico()

    # Obtém o gateway (roteador) de rede
    gateway = obter_gateway()
    if not gateway:
        print("Gateway não encontrado. Encerrando.")
        return
    print(f"Gateway (roteador) da rede: {gateway}")

    try:
        while True:
            # Descobre novos dispositivos
            dispositivos_atualizados = descobrir_dispositivos()

            # Classifica os dispositivos entre roteador e host
            dispositivos_atualizados = classificar_dispositivos(dispositivos_atualizados, gateway)

            # Detecta mudança de histórico
            if historico_dispositivos:
                novos_dispositivos, dispositivos_offline = detectar_mudancas(dispositivos_atualizados, historico_dispositivos)

                if novos_dispositivos:
                    print("\nNovos dispositivos detectados:")
                    exibir_dispositivos_na_interface(novos_dispositivos, titulo="Novos Dispositivos")

                if dispositivos_offline:
                    print("\nDispositivos offline:")
                    exibir_dispositivos_na_interface(dispositivos_offline, titulo="Dispositivos Offline")

            # Exibe todos os dispositivos atualizados na interface
            exibir_dispositivos_na_interface(dispositivos_atualizados, titulo="Todos os Dispositivos Atuais")

            # Atualiza o histórico e salva no arquivo
            historico_dispositivos = dispositivos_atualizados
            salvar_historico(historico_dispositivos)

            # Timer entre scans 
            time.sleep(60)

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")

# Funcao para iniciar o monitoramento em uma thread separada
def iniciar_monitoramento():
    threading.Thread(target=executar_monitoramento, daemon=True).start()

# Funcao para fechar o programa
def fechar_programa():
    root.quit()

# Criação da interface gráfica
root = tk.Tk()
root.title("Scanner de Rede")

# Botão para iniciar o monitoramento
botao_monitoramento = tk.Button(root, text="Iniciar Monitoramento", command=iniciar_monitoramento)
botao_monitoramento.pack(pady=10)

# Botão para fechar o programa
botao_fechar = tk.Button(root, text="Fechar Programa", command=fechar_programa)
botao_fechar.pack(pady=10)

# Área de texto para exibir os dispositivos encontrados
area_texto = scrolledtext.ScrolledText(root, width=80, height=20)
area_texto.pack(pady=10)

root.mainloop()
