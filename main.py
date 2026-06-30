
import os
import json
import requests
import time
from firebase_admin import credentials, initialize_app

# Carrega a configuração do Firebase da variável de ambiente que configuramos no Render
firebase_config = json.loads(os.environ.get("FIREBASE_CONFIG_JSON"))
cred = credentials.Certificate(firebase_config)
initialize_app(cred)

# Lê a API_KEY da variável de ambiente
API_KEY = os.environ.get("API_KEY")
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def analisar_jogos_ao_vivo():
    URL = "https://v3.football.api-sports.io/fixtures?live=all"
    try:
        resposta = requests.get(URL, headers=HEADERS)
        jogos = resposta.json().get('response', [])
       
        for jogo in jogos:
            status = jogo['fixture']['status']['elapsed']
            print(f"Jogo encontrado, tempo: {status}")
           
    except Exception as e:
        print(f"Erro ao buscar jogos: {e}")

if __name__ == "__main__":
    while True:
        analisar_jogos_ao_vivo()
        time.sleep(60)
