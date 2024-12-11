from flask import Flask, render_template
import json
from agente_snmp import estado_ferramenta, dispositivos_descobertos, atualizar_dispositivos

app = Flask(__name__)

# Carregar dados do SNMP
atualizar_dispositivos()

@app.route('/')
def home():
    # Carregar dispositivos do arquivo JSON
    try:
        with open("dispositivos.json", "r") as file:
            dispositivos_json = json.load(file)
    except FileNotFoundError:
        dispositivos_json = []

    # Passar as informações de dispositivos e estado para o template
    return render_template('index.html', dispositivos_json=dispositivos_json, 
                           estado_ferramenta=estado_ferramenta, dispositivos_snmp=dispositivos_descobertos)

if __name__ == "__main__":
    app.run(debug=True, port=5007)
