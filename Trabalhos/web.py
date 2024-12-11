from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    # Carregar os dispositivos do arquivo JSON
    try:
        with open("dispositivos.json", "r") as file:
            dispositivos = json.load(file)
    except FileNotFoundError:
        dispositivos = []
    
    return render_template('index.html', dispositivos=dispositivos)

if __name__ == "__main__":
    app.run(debug=True, port=5007)
