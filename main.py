import os
import requests
import time
from firebase_admin import messaging, credentials, initialize_app

# Configuração Firebase
cred = credentials.Certificate("firebase_key.json")
initialize_app(cred)

# Lê a chave do Render de forma segura
API_KEY = os.environ.get("API_KEY")
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def analisar_jogos_ao_vivo():
    URL = "https://v3.football.api-sports.io/fixtures?live=all"
    try:
        resposta = requests.get(URL, headers=HEADERS)
        jogos = resposta.json().get('response', [])
       
        for jogo in jogos:
            status = jogo['fixture']['status']['elapsed']
            # Continue a lógica do seu código aqui...
            print(f"Jogo encontrado, tempo: {status}")
           
    except Exception as e:
        print(f"Erro ao buscar jogos: {e}")

# Exemplo de loop para rodar o robô
if __name__ == "__main__":
    while True:
        analisar_jogos_ao_vivo()
        time.sleep(60) # Espera 60 segundos antes da próxima verificação
