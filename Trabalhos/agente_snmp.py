from pysnmp.hlapi import *
from main import carregar_lista_fabricantes, descobrir_dispositivos, obter_rede_local, total_dispositivos

# Estado inicial da ferramenta
estado_ferramenta = {
    "status_sistema": 1,
    "intervalo_descoberta": 60000,
    "total_dispositivos_descobertos": 0,  # Inicialmente como 0
    "contato_admin": "admin@exemplo.com"
}

# Inicializa a variável de dispositivos descobertos
dispositivos_descobertos = []

# Atualiza a lista de dispositivos descobertos
def atualizar_dispositivos():
    global dispositivos_descobertos
    lista_fabricantes = carregar_lista_fabricantes('./mac.txt')
    rede_local = obter_rede_local()
    dispositivos_descobertos = descobrir_dispositivos(rede=rede_local, lista_fabricantes=lista_fabricantes)
    
    # Atualiza o total de dispositivos descobertos após a descoberta
    estado_ferramenta["total_dispositivos_descobertos"] = total_dispositivos(dispositivos_descobertos)

# Função para criar e configurar o agente SNMP
def configurar_agente_snmp():
    # Criando o motor SNMP
    snmp_engine = SnmpEngine()

    # Adicionando transporte para o SNMP (escutando na porta 161)
    transport = UdpTransportTarget(('0.0.0.0', 161))

    # Configuração da comunidade SNMP
    config.addV1System(snmp_engine, 'publico', 'publico')

    # MIB entries principais
    def add_mib_entry(oid, value):
        setCmd(
            snmp_engine,
            transport,
            CommunityData('publico'),
            ContextData(),
            ObjectType(ObjectIdentity(oid), value)
        )

    add_mib_entry('1.3.6.1.4.1.888.1.1', estado_ferramenta["status_sistema"])
    add_mib_entry('1.3.6.1.4.1.888.1.2', estado_ferramenta["intervalo_descoberta"])
    add_mib_entry('1.3.6.1.4.1.888.1.3', estado_ferramenta["total_dispositivos_descobertos"])
    add_mib_entry('1.3.6.1.4.1.888.1.4', estado_ferramenta["contato_admin"])

    # Adicionando dispositivos descobertos às MIBs
    for i, dispositivo in enumerate(dispositivos_descobertos, start=1):
        add_mib_entry(f"1.3.6.1.4.1.888.1.5.1.{i}.1", dispositivo["ip"])
        add_mib_entry(f"1.3.6.1.4.1.888.1.5.1.{i}.2", dispositivo["nome"])
        add_mib_entry(f"1.3.6.1.4.1.888.1.5.1.{i}.3", dispositivo["status"])
        add_mib_entry(f"1.3.6.1.4.1.888.1.5.1.{i}.4", dispositivo["uptime"])

    print("Agente SNMP em execução...")
    snmp_engine.transportDispatcher.runDispatcher()

if __name__ == "__main__":
    atualizar_dispositivos()  # Atualiza a lista de dispositivos e o total
    configurar_agente_snmp()  # Inicia o agente SNMP
