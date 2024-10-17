
# Documentação do Scanner de Rede

## Visão Geral

Este projeto é um **Scanner de Rede** desenvolvido em Python que descobre dispositivos na rede local e monitora mudanças ao longo do tempo. Ele utiliza a biblioteca `nmap` para varredura de redes, e fornece uma interface gráfica usando `tkinter`. Os dispositivos encontrados são salvos em um arquivo JSON para referência futura, e o programa é capaz de detectar novos dispositivos e aqueles que saíram da rede.

## Índice
1. [Bibliotecas Utilizadas](#bibliotecas-utilizadas)
2. [Funções do Programa](#funções-do-programa)
3. [Componentes Principais](#componentes-principais)
4. [Como o Programa Funciona](#como-o-programa-funciona)
5. [Interface Gráfica (GUI)](#interface-gráfica-gui)

## Bibliotecas Utilizadas

### 1. `nmap`
- **Propósito**: Esta biblioteca é utilizada para realizar varreduras na rede, permitindo que o programa detecte todos os dispositivos conectados.
- **Instalação**: Você pode instalar a biblioteca usando o comando:
  ```bash
  pip install python-nmap
  ```

### 2. `time`
- **Propósito**: Fornece funções relacionadas ao controle de tempo, como fazer o programa "dormir" por um determinado período de tempo entre varreduras.

### 3. `json`
- **Propósito**: Utilizada para trabalhar com dados no formato JSON, permitindo salvar e carregar informações de dispositivos em arquivos.

### 4. `socket` e `struct`
- **Propósito**: Utilizadas para obter informações da rede local, como o gateway (roteador) e converter dados em endereços IP.

### 5. `datetime`
- **Propósito**: Fornece funcionalidades para trabalhar com datas e horas, usadas no registro da hora da primeira descoberta de um dispositivo.

### 6. `tkinter`
- **Propósito**: Biblioteca padrão para criar interfaces gráficas em Python, utilizada aqui para criar uma interface que mostra os dispositivos detectados e permite interações como iniciar e fechar o programa.

### 7. `threading`
- **Propósito**: Permite que o programa execute o monitoramento de dispositivos em uma thread separada, permitindo que a interface gráfica continue responsiva.

## Funções do Programa

### 1. `descobrir_dispositivos(rede="192.168.0.0/24")`
- **Descrição**: Realiza a varredura da rede usando o `nmap` para detectar dispositivos conectados. Retorna uma lista de dicionários contendo informações como IP, MAC, fabricante e a data/hora da primeira descoberta.
- **Entrada**: Um intervalo de IPs (rede).
- **Saída**: Lista de dispositivos encontrados.

### 2. `obter_gateway()`
- **Descrição**: Obtém o endereço IP do gateway (roteador) da rede local lendo as rotas do sistema em `/proc/net/route`.
- **Saída**: Retorna o IP do gateway.

### 3. `classificar_dispositivos(dispositivos, ip_gateway)`
- **Descrição**: Classifica os dispositivos entre **roteador** e **host** com base no IP do gateway.
- **Entrada**: Lista de dispositivos e o IP do gateway.
- **Saída**: Lista de dispositivos classificados.

### 4. `salvar_historico(dispositivos, arquivo_historico="historico.json")`
- **Descrição**: Salva a lista de dispositivos em um arquivo JSON para que o histórico seja preservado entre execuções do programa.
- **Entrada**: Lista de dispositivos e o nome do arquivo JSON.

### 5. `carregar_historico(arquivo_historico="historico.json")`
- **Descrição**: Carrega os dispositivos salvos anteriormente em um arquivo JSON.
- **Saída**: Lista de dispositivos carregados do arquivo JSON.

### 6. `detectar_mudancas(dispositivos_atualizados, dispositivos_antigos)`
- **Descrição**: Compara a lista de dispositivos atualizados com a lista antiga para detectar novos dispositivos ou aqueles que saíram da rede.
- **Saída**: Retorna dois conjuntos: novos dispositivos e dispositivos offline.

### 7. `exibir_dispositivos_na_interface(dispositivos, titulo="Dispositivos Descobertos")`
- **Descrição**: Exibe os dispositivos encontrados na área de texto da interface gráfica.

### 8. `executar_monitoramento()`
- **Descrição**: Função principal de monitoramento que executa o loop de descoberta de dispositivos e exibe na interface os dispositivos encontrados, novos dispositivos e aqueles offline.
- **Saída**: Atualiza a interface gráfica e o histórico de dispositivos.

### 9. `iniciar_monitoramento()`
- **Descrição**: Inicia o processo de monitoramento em uma thread separada.

### 10. `fechar_programa()`
- **Descrição**: Fecha o programa e a janela principal da interface gráfica.

## Componentes Principais

- **Interface Gráfica**: Criada com `tkinter`, fornece uma maneira visual de interagir com o programa. Inclui botões para iniciar o monitoramento e fechar o programa, além de uma área de texto para exibir informações dos dispositivos.
- **Histórico**: Dispositivos descobertos são salvos em um arquivo JSON, o que permite que o programa detecte mudanças na rede, como novos dispositivos ou dispositivos offline.
- **Multithreading**: O monitoramento da rede é executado em uma thread separada, o que permite que a interface gráfica continue responsiva enquanto o programa realiza varreduras na rede.

## Como o Programa Funciona

1. **Carregamento do Histórico**: Ao iniciar, o programa tenta carregar um arquivo JSON que contém o histórico de dispositivos descobertos anteriormente.
2. **Descoberta de Dispositivos**: O programa usa a biblioteca `nmap` para escanear a rede local e descobrir dispositivos conectados.
3. **Classificação de Dispositivos**: Dispositivos são classificados como **roteador** ou **host** com base no IP do gateway da rede.
4. **Monitoramento Contínuo**: O programa entra em um loop onde continuamente escaneia a rede, detecta novos dispositivos e identifica aqueles que saíram da rede.
5. **Interface Gráfica**: Os dispositivos encontrados, novos e offline são exibidos na interface gráfica em uma área de texto.

## Interface Gráfica (GUI)

A interface gráfica permite ao usuário:
- **Iniciar o Monitoramento**: Um botão que inicia o processo de escaneamento e monitoramento de dispositivos em uma thread separada.
- **Fechar o Programa**: Um botão que encerra o programa de forma limpa.
- **Área de Texto**: Exibe os dispositivos encontrados, categorizados como "Dispositivos Atuais", "Novos Dispositivos" e "Dispositivos Offline".

## Como Executar

1. Certifique-se de que as bibliotecas necessárias estão instaladas:
   ```bash
   pip install python-nmap
   ```
2. Execute o script principal:
   ```bash
   python main.py
   ```
3. A interface gráfica será aberta, e o monitoramento da rede pode ser iniciado clicando no botão "Iniciar Monitoramento".

---

Esse formato de documentação ajuda a explicar detalhadamente o funcionamento do programa e pode ser colocado no repositório como `DOCUMENTAÇÃO.md` para complementar o `README.md`.