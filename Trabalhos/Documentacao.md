
# Documentação do Scanner de Rede

## Visão Geral

Este projeto é um **Scanner de Rede** desenvolvido em Python que descobre dispositivos na rede local. Ele utiliza a biblioteca `nmap` para varredura de redes e fornece uma interface gráfica usando `tkinter`. Os dispositivos encontrados são salvos em um arquivo JSON para referência futura.

## Índice
1. [Bibliotecas Utilizadas](#bibliotecas-utilizadas)
2. [Funções do Programa](#funções-do-programa)
3. [Componentes Principais](#componentes-principais)
4. [Como o Programa Funciona](#como-o-programa-funciona)
5. [Interface Gráfica (GUI)](#interface-gráfica-gui)

## Bibliotecas Utilizadas

### 1. `nmap`
- **Propósito**: Realiza varreduras na rede, permitindo que o programa detecte todos os dispositivos conectados.
- **Instalação**: 
  ```bash
  pip install python-nmap
  ```

### 2. `socket`
- **Propósito**: Para obter informações da rede local, como o endereço IP do dispositivo.

### 3. `json`
- **Propósito**: Utilizada para trabalhar com dados no formato JSON, permitindo salvar e carregar informações de dispositivos em arquivos.

### 4. `datetime`
- **Propósito**: Fornece funcionalidades para trabalhar com datas e horas, usadas no registro da hora da primeira descoberta de um dispositivo.

### 5. `tkinter`
- **Propósito**: Biblioteca padrão para criar interfaces gráficas em Python, utilizada para criar a interface que mostra os dispositivos detectados.

### 6. `threading`
- **Propósito**: Permite que o programa execute a varredura em uma thread separada, mantendo a interface gráfica responsiva.

## Funções do Programa

### 1. `carregar_lista_fabricantes(arquivo_oui)`
- **Descrição**: Carrega a lista de fabricantes OUI a partir do arquivo especificado.
- **Parâmetros**: 
  - `arquivo_oui` (str): Caminho do arquivo contendo a lista de OUI.
- **Retorno**: Dicionário onde as chaves são os OUI e os valores são os nomes dos fabricantes.

### 2. `obter_fabricante_por_mac(mac, lista_fabricantes)`
- **Descrição**: Obtém o fabricante associado a um endereço MAC.
- **Parâmetros**: 
  - `mac` (str): O endereço MAC do dispositivo.
  - `lista_fabricantes` (dict): Dicionário contendo OUI e fabricantes.
- **Retorno**: Nome do fabricante ou "Desconhecido" se não for encontrado.

### 3. `descobrir_dispositivos(rede, lista_fabricantes)`
- **Descrição**: Descobre dispositivos na rede especificada.
- **Parâmetros**: 
  - `rede` (str): Endereço da rede a ser escaneada.
  - `lista_fabricantes` (dict): Dicionário contendo OUI e fabricantes.
- **Retorno**: Lista de dicionários com informações sobre os dispositivos encontrados.

### 4. `obter_rede_local()`
- **Descrição**: Obtém automaticamente o endereço da rede local.
- **Retorno**: Endereço da rede local no formato CIDR (ex: "192.168.0.0/24").

### 5. `salvar_em_json(dispositivos, arquivo)`
- **Descrição**: Salva os dispositivos descobertos em um arquivo JSON.
- **Parâmetros**: 
  - `dispositivos` (list): Lista de dispositivos a serem salvos.
  - `arquivo` (str): Caminho do arquivo onde os dados serão salvos.

### 6. `exibir_dispositivos(dispositivos, texto)`
- **Descrição**: Exibe os dispositivos descobertos na interface gráfica.
- **Parâmetros**: 
  - `dispositivos` (list): Lista de dispositivos a serem exibidos.
  - `texto` (ScrolledText): O campo de texto onde os dados serão exibidos.

### 7. `executar_varredura(texto)`
- **Descrição**: Executa a varredura de rede e exibe os resultados na interface gráfica.
- **Parâmetros**: 
  - `texto` (ScrolledText): O campo de texto onde os resultados serão exibidos.

### 8. `finalizar_varredura()`
- **Descrição**: Finaliza a aplicação quando solicitado.

### 9. `iniciar_interface()`
- **Descrição**: Cria e inicia a interface gráfica do programa.

## Componentes Principais

- **Interface Gráfica**: Criada com `tkinter`, fornece uma maneira visual de interagir com o programa. Inclui botões para iniciar a varredura e fechar o programa, além de uma área de texto para exibir informações dos dispositivos.
- **Histórico**: Dispositivos descobertos são salvos em um arquivo JSON, permitindo que os dados sejam mantidos entre execuções.
- **Multithreading**: A varredura de rede é executada em uma thread separada, permitindo que a interface gráfica continue responsiva.

## Como o Programa Funciona

1. **Carregamento de Fabricantes**: O programa carrega a lista de fabricantes OUI a partir de um arquivo texto.
2. **Obtenção da Rede Local**: O programa identifica automaticamente a rede local em que está conectado.
3. **Descoberta de Dispositivos**: Utiliza a biblioteca `nmap` para escanear a rede local e descobrir dispositivos conectados.
4. **Exibição dos Resultados**: Os resultados da varredura são exibidos na interface gráfica e salvos em um arquivo JSON.

## Interface Gráfica (GUI)

A interface gráfica permite ao usuário:
- **Iniciar a Varredura**: Um botão que inicia o processo de escaneamento da rede.
- **Fechar o Programa**: Um botão que encerra o programa de forma limpa.
- **Área de Texto**: Exibe os dispositivos encontrados com informações detalhadas.

## Como Executar

1. Certifique-se de que as bibliotecas necessárias estão instaladas:
   ```bash
   pip install python-nmap
   ```
2. Execute o script principal:
   ```bash
   python main.py
   ```
3. A interface gráfica será aberta, e a varredura da rede pode ser iniciada clicando no botão "Iniciar Varredura".

---
```
