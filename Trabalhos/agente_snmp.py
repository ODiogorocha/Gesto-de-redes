from snmp_agent import SnmpAgent, MIBEntry
from main import carregar_lista_fabricantes, descobrir_dispositivos, obter_total_dispositivos_descobertos, obter_rede_local

# Estado inicial da ferramenta
estado_ferramenta = {
    "status_sistema": 1,
    "intervalo_descoberta": 60000,
    "total_dispositivos_descobertos": 0,
    "contato_admin": "admin@exemplo.com"
}

# Atualiza a lista de dispositivos descobertos
def atualizar_dispositivos():
    global dispositivos_descobertos
    lista_fabricantes = carregar_lista_fabricantes('./mac.txt')
    rede_local = obter_rede_local()
    dispositivos_descobertos = descobrir_dispositivos(rede=rede_local, lista_fabricantes=lista_fabricantes)
    estado_ferramenta["total_dispositivos_descobertos"] = obter_total_dispositivos_descobertos(dispositivos_descobertos)

# Configura o agente SNMP
def configurar_agente_snmp():
    agente = SnmpAgent(
        host="0.0.0.0",
        port=161,
        community="publico"
    )

    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.1", lambda oid: estado_ferramenta["status_sistema"]))
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.2", lambda oid: estado_ferramenta["intervalo_descoberta"]))
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.3", lambda oid: estado_ferramenta["total_dispositivos_descobertos"]))
    agente.add_mib_entry(MIBEntry("1.3.6.1.4.1.888.1.4", lambda oid: estado_ferramenta["contato_admin"]))

    for i, dispositivo in enumerate(dispositivos_descobertos, start=1):
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.1", lambda oid, d=dispositivo: d["ip"]))
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.2", lambda oid, d=dispositivo: d["nome"]))
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.3", lambda oid, d=dispositivo: d["status"]))
        agente.add_mib_entry(MIBEntry(f"1.3.6.1.4.1.888.1.5.1.{i}.4", lambda oid, d=dispositivo: d["uptime"]))

    print("Agente SNMP em execução...")
    agente.serve_forever()

if __name__ == "__main__":
    atualizar_dispositivos()
    configurar_agente_snmp()
