# Documentação do Agente SNMP para Descoberta de Dispositivos

## Descrição
Este projeto implementa um agente SNMP que utiliza as funções de descoberta de dispositivos da `main.py` para fornecer informações sobre dispositivos na rede. O agente SNMP expõe dados de dispositivos descobertos e parâmetros de estado do sistema, permitindo consultas via SNMP.

## Estrutura do Projeto
- **`main.py`**: Contém a lógica de descoberta de dispositivos na rede, carregamento de listas de fabricantes e gerenciamento de histórico de dispositivos.
- **`agente_snmp.py`**: Implementa um agente SNMP que importa e utiliza as funções da `main.py` para expor informações SNMP.
- **`mac.txt`**: Arquivo de texto contendo a lista de fabricantes de endereços MAC.
- **`main.mib`**: Arquivo MIB usado para definir a estrutura e os OIDs (Object Identifiers) que o agente SNMP responde.

## Instalação e Pré-requisitos
1. **Instalação de bibliotecas**:
   Certifique-se de ter o Python instalado e as bibliotecas necessárias:
   ```bash
   pip install python-nmap
   ```

2. **Bibliotecas adicionais**:
   - `tkinter`: Para a interface gráfica na `main.py`.
   - `pysnmp`: Para a criação do agente SNMP.

## Descrição do Agente SNMP (`agente_snmp.py`)

### Importações
```python
from snmp_agent import SnmpAgent, MIBEntry
from main import carregar_lista_fabricantes, descobrir_dispositivos, obter_total_dispositivos_descobertos, obter_rede_local
```
- **`SnmpAgent` e `MIBEntry`**: Importados de um módulo hipotético `snmp_agent`, responsáveis por criar e gerenciar o agente SNMP.
- **Funções da `main.py`**: Importadas para integrar a lógica de descoberta de dispositivos.

### Variável Global `estado_ferramenta`
```python
estado_ferramenta = {
    "status_sistema": 1,
    "intervalo_descoberta": 60000,
    "total_dispositivos_descobertos": 0,
    "contato_admin": "admin@exemplo.com"
}
```
- Armazena o estado do sistema, incluindo:
  - **`status_sistema`**: Status da ferramenta (1 para ativo).
  - **`intervalo_descoberta`**: Intervalo de tempo em milissegundos para a descoberta de dispositivos.
  - **`total_dispositivos_descobertos`**: Contagem total de dispositivos descobertos.
  - **`contato_admin`**: Informações de contato do administrador.

### Função `atualizar_dispositivos`
```python
def atualizar_dispositivos():
    global dispositivos_descobertos
    lista_fabricantes = carregar_lista_fabricantes('./mac.txt')
    rede_local = obter_rede_local()
    dispositivos_descobertos = descobrir_dispositivos(rede=rede_local, lista_fabricantes=lista_fabricantes)
    estado_ferramenta["total_dispositivos_descobertos"] = obter_total_dispositivos_descobertos(dispositivos_descobertos)
```
- **Objetivo**: Atualizar a lista de dispositivos descobertos.
- **Fluxo**:
  - Carrega a lista de fabricantes de `mac.txt`.
  - Obtém a rede local.
  - Descobre os dispositivos usando `descobrir_dispositivos`.
  - Atualiza o total de dispositivos descobertos.

### Função `configurar_agente_snmp`
```python
def configurar_agente_snmp():
    agente = SnmpAgent(
        host="0.0.0.0",
        port=161,
        community="publico"
    )
```
- **Objetivo**: Configurar e iniciar o agente SNMP.
- **Parâmetros**:
  - **`host`**: O agente escuta em todas as interfaces (0.0.0.0).
  - **`port`**: Porta padrão SNMP (161).
  - **`community`**: Nome da comunidade SNMP.

### Adicionando Entradas MIB
```python
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.1", lambda oid: estado_ferramenta["status_sistema"]))
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.2", lambda oid: estado_ferramenta["intervalo_descoberta"]))
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.3", lambda oid: estado_ferramenta["total_dispositivos_descobertos"]))
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.4", lambda oid: estado_ferramenta["contato_admin"]))
```
- **Objetivo**: Adicionar entradas MIB para responder a consultas SNMP.
- **Explicação**: Cada `MIBEntry` representa um OID e a função lambda que retorna o valor correspondente.

### Adicionando Dispositivos Descobertos
```python
    for i, dispositivo in enumerate(dispositivos_descobertos, start=1):
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.1", lambda oid, d=dispositivo: d["ip"]))
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.2", lambda oid, d=dispositivo: d["nome"]))
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.3", lambda oid, d=dispositivo: d["status"]))
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.4", lambda oid, d=dispositivo: d["uptime"]))
```
- **Objetivo**: Adicionar informações de dispositivos descobertos à árvore MIB.
- **Explicação**: Para cada dispositivo, são criadas entradas MIB exclusivas que expõem o IP, nome, status e tempo de atividade.

### Execução do Agente
```python
    print("Agente SNMP em execução...")
    agente.serve_forever()
```
- **Objetivo**: Iniciar o agente SNMP para aguardar e responder a consultas indefinidamente.

## Utilizando o Agente SNMP
1. **Iniciar o agente**:
   ```bash
   python agente_snmp.py
   ```

2. **Consultar o agente com `snmpwalk`**:
   ```bash
   snmpwalk -v2c -c publico <endereço_ip_do_agente> 1.3.6.1.4.1.888
   ```

## Arquivo MIB (`main.mib`)
Este arquivo MIB define a estrutura de OIDs e tipos de dados que o agente SNMP responde. Ele é usado para traduzir e consultar informações sobre o estado do sistema e dispositivos descobertos.

## Expansão Futuras
- Adicionar autenticação e segurança ao agente SNMP.
- Melhorar a interface gráfica de `main.py` para maior controle e personalização.
- Implementar suporte a SNMPv3.

## Conclusão
Este projeto integra uma ferramenta de descoberta de dispositivos em rede com um agente SNMP, permitindo monitorar e consultar informações sobre dispositivos de forma padronizada usando SNMP.

