import nmap
import socket
import json
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import os
import pandas as pd

# Função para carregar a lista de fabricantes OUI a partir do arquivo "mac.txt"
def carregar_lista_fabricantes(arquivo_oui="/home/diogo/Documents/Aulas/G.redes/Gestao-de-redes/Trabalho1/mac.txt"):
    lista_fabricantes = {}
    
    # Verifica se o arquivo existe antes de tentar abri-lo
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

# Função para obter o fabricante a partir do MAC Address
def obter_fabricante_por_mac(mac, lista_fabricantes):
    oui = mac[:8].upper()
    return lista_fabricantes.get(oui, "Desconhecido")

# Função para descobrir dispositivos na rede
def descobrir_dispositivos(rede="192.168.0.0/24", lista_fabricantes={}):  
    scanner_nmap = nmap.PortScanner()
    print(f"Escaneando a rede {rede}...")

    try:
        scanner_nmap.scan(hosts=rede, arguments='-sn')  
    except Exception as e:
        print(f"Erro ao escanear a rede: {e}")
        return []

    dispositivos_encontrados = []
    for host in scanner_nmap.all_hosts():
        print(f"Dispositivo encontrado: {host}")
        mac = scanner_nmap[host]['addresses'].get('mac', 'Desconhecido')
        fabricante = obter_fabricante_por_mac(mac, lista_fabricantes) if mac != 'Desconhecido' else 'Desconhecido'
        dispositivo = {
            "ip": host,
            "mac": mac,
            "fabricante": fabricante,
            "primeira_descoberta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")     
        }
        dispositivos_encontrados.append(dispositivo)
    print(f"Dispositivos encontrados nesta varredura: {dispositivos_encontrados}")  
    return dispositivos_encontrados

# Função para obter o endereço da rede local automaticamente
def obter_rede_local():
    try:
        # Conectando a um socket para descobrir o endereço da interface de rede
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))  # Usa o DNS do Google para descobrir a rede local
        ip_local = sock.getsockname()[0]
        sock.close()

        partes_ip = ip_local.split('.')
        partes_ip[3] = '0'  # Modifica a última parte para 0, obtendo o endereço da rede
        rede = '.'.join(partes_ip) + "/24"
        return rede
    except Exception as e:
        print(f"Erro ao obter a rede local: {e}")
        return "192.168.0.0/24"  # Retorna um valor padrão se houver erro

# Função para salvar os dispositivos descobertos em um arquivo JSON
def salvar_em_json(dispositivos, arquivo="dispositivos.json"):
    try:
        with open(arquivo, 'w') as f:
            json.dump(dispositivos, f, indent=4)
        print(f"Dispositivos salvos em {arquivo}")
    except Exception as e:
        print(f"Erro ao salvar dispositivos no arquivo JSON: {e}")

# Interface gráfica para exibir os dispositivos descobertos
def exibir_dispositivos(dispositivos, texto):
    texto.delete(1.0, tk.END)
    for dispositivo in dispositivos:
        texto.insert(tk.END, f"IP: {dispositivo['ip']}\n")
        texto.insert(tk.END, f"MAC: {dispositivo['mac']}\n")
        texto.insert(tk.END, f"Fabricante: {dispositivo['fabricante']}\n")
        texto.insert(tk.END, f"Primeira descoberta: {dispositivo['primeira_descoberta']}\n")
        texto.insert(tk.END, "-"*40 + "\n")

# Função para executar a varredura de rede
def executar_varredura(texto):
    lista_fabricantes = carregar_lista_fabricantes('./mac.txt')  # Caminho do arquivo
    rede_local = obter_rede_local()
    dispositivos = descobrir_dispositivos(rede=rede_local, lista_fabricantes=lista_fabricantes)
    exibir_dispositivos(dispositivos, texto)
    salvar_em_json(dispositivos)
    messagebox.showinfo("Varredura Concluída", "Varredura finalizada e dados salvos em dispositivos.json")

# Função para parar a varredura (aqui, apenas fecha a aplicação)
def finalizar_varredura():
    if messagebox.askokcancel("Finalizar", "Você deseja finalizar a varredura?"):
        janela.destroy()  # Fechar a janela

# Interface gráfica principal
def iniciar_interface():
    global janela
    janela = tk.Tk()
    janela.title("Scanner de Rede")

    # Campo de texto com scroll
    texto = scrolledtext.ScrolledText(janela, width=60, height=20)
    texto.pack(padx=10, pady=10)

    # Botão para iniciar a varredura
    botao_iniciar = tk.Button(janela, text="Iniciar Varredura", command=lambda: threading.Thread(target=executar_varredura, args=(texto,)).start())
    botao_iniciar.pack(pady=10)

    # Botão para finalizar a varredura
    botao_finalizar = tk.Button(janela, text="Finalizar", command=finalizar_varredura)
    botao_finalizar.pack(pady=10)

    janela.mainloop()

# Iniciar a interface gráfica
if __name__ == "__main__":
    iniciar_interface()
