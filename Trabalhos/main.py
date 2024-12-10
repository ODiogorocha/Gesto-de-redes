import nmap
import socket
import json
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

# Função para carregar a lista de fabricantes OUI a partir do arquivo "mac.txt"
def carregar_lista_fabricantes(arquivo_oui="mac.txt"):
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
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo de fabricantes OUI: {e}")
    else:
        print(f"Arquivo {arquivo_oui} não encontrado.")
        messagebox.showerror("Erro", f"Arquivo {arquivo_oui} não encontrado.")
    
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
    print(f"Dispositivos encontrados nesta varredura: {dispositivos_encontrados}")  
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

# Função para carregar o histórico de dispositivos de um arquivo JSON
def carregar_historico(arquivo="dispositivos.json"):
    if os.path.isfile(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return []

# Função para verificar o histórico e atualizar o status
def atualizar_historico(dispositivos_encontrados, historico):
    historico_atualizado = {d['ip']: d for d in historico}

    # Atualiza o status de dispositivos encontrados
    for dispositivo in dispositivos_encontrados:
        historico_atualizado[dispositivo['ip']] = dispositivo

    # Atualiza o status dos dispositivos que não foram encontrados
    for ip in historico_atualizado:
        if historico_atualizado[ip]['status'] == 'Online':
            historico_atualizado[ip]['status'] = 'Offline'
    
    return list(historico_atualizado.values())

# Função para exibir os dispositivos, incluindo histórico
def exibir_dispositivos(dispositivos, texto):
    texto.delete(1.0, tk.END)
    for dispositivo in dispositivos:
        texto.insert(tk.END, f"IP: {dispositivo['ip']}\n")
        texto.insert(tk.END, f"MAC: {dispositivo['mac']}\n")
        texto.insert(tk.END, f"Fabricante: {dispositivo['fabricante']}\n")
        texto.insert(tk.END, f"Status: {dispositivo['status']}\n") 
        texto.insert(tk.END, f"Primeira descoberta: {dispositivo['primeira_descoberta']}\n")
        texto.insert(tk.END, "-"*40 + "\n")

def executar_varredura(texto):
    lista_fabricantes = carregar_lista_fabricantes('./mac.txt') 
    rede_local = obter_rede_local()
    dispositivos = descobrir_dispositivos(rede=rede_local, lista_fabricantes=lista_fabricantes)
    
    historico = carregar_historico()
    dispositivos_historico = atualizar_historico(dispositivos, historico)

    exibir_dispositivos(dispositivos_historico, texto)
    salvar_em_json(dispositivos_historico)
    messagebox.showinfo("Varredura Concluída", "Varredura finalizada e dados salvos em dispositivos.json")

def finalizar_varredura():
    if messagebox.askokcancel("Finalizar", "Você deseja finalizar a varredura?"):
        janela.destroy()

def iniciar_interface():
    global janela
    janela = tk.Tk()
    janela.title("Scanner de Rede")

    texto = scrolledtext.ScrolledText(janela, width=60, height=20)
    texto.pack(padx=10, pady=10)

    botao_iniciar = tk.Button(janela, text="Iniciar Varredura", command=lambda: threading.Thread(target=executar_varredura, args=(texto,)).start())
    botao_iniciar.pack(pady=10)

    botao_finalizar = tk.Button(janela, text="Finalizar", command=finalizar_varredura)
    botao_finalizar.pack(pady=10)

    janela.mainloop()


if __name__ == "__main__":
    iniciar_interface()
