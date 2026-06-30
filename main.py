import os
import json
import requests
import time
import threading
from flask import Flask
from firebase_admin import credentials, initialize_app

# --- 1. O Servidor Web (mantém o Render satisfeito) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot de Futebol está rodando!"

def run_web_server():
    # O Render atribui uma porta automaticamente na variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. O Robô (sua lógica de análise) ---
firebase_config = json.loads(os.environ.get("FIREBASE_CONFIG_JSON"))
cred = credentials.Certificate(firebase_config)
initialize_app(cred)

API_KEY = os.environ.get("API_KEY")
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def analisar_jogos_ao_vivo():
    while True:
        try:
            print("Verificando jogos...")
            resposta = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=HEADERS)
            jogos = resposta.json().get('response', [])
            for jogo in jogos:
                status = jogo['fixture']['status']['elapsed']
                print(f"Jogo encontrado, tempo: {status}")
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(60)

if __name__ == "__main__":
    # Inicia o servidor web em uma thread separada
    threading.Thread(target=run_web_server).start()
    # Inicia o robô
    analisar_jogos_ao_vivo()
