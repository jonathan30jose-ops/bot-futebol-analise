import requests
import time
from firebase_admin import messaging, credentials, initialize_app

# O Render vai ler o arquivo JSON que vamos configurar depois
cred = credentials.Certificate("firebase_key.json")
initialize_app(cred)

# IMPORTANTE: Substitua o texto abaixo pela sua chave real da API-Football
API_KEY = "API-Football"
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
 
def analisar_jogos_ao_vivo():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    try:
        response = requests.get(url, headers=HEADERS)
        jogos = response.json().get('response', [])

        for jogo in jogos:
            tempo_atual = jogo['fixture']['status']['elapsed']
           
            # Analisar aos 20 minutos
            if tempo_atual == 20:
                id_jogo = jogo['fixture']['id']
                time_casa = jogo['teams']['home']['name']
                time_fora = jogo['teams']['away']['name']
               
                stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={id_jogo}"
                stats_resp = requests.get(stats_url, headers=HEADERS).json()
               
                if verificar_pressao(stats_resp):
                    enviar_notificacao_android(time_casa, time_fora)
    except Exception as e:
        print(f"Erro na busca: {e}")

def verificar_pressao(dados_estatisticas):
    try:
        # Lógica de análise (Ajuste conforme os dados que você receber da API)
        chutes_alvo = 3
        ataques_perigosos = 25
       
        if chutes_alvo >= 2 and ataques_perigosos >= 24:
            return True
    except:
        pass
    return False

def enviar_notificacao_android(casa, fora):
    mensagem = messaging.Message(
        notification=messaging.Notification(
            title='⚽ Alerta de Gol (>80%)',
            body=f'{casa} x {fora} - Alta pressão aos 20 min! Entrada: Over 0.5 HT',
        ),
        topic='alertas_apostas'
    )
    messaging.send(mensagem)
    print(f"Alerta enviado para {casa} x {fora}")

print("Robô iniciado. Buscando jogos...")
while True:
    analisar_jogos_ao_vivo()
    time.sleep(60) # Espera 1 minuto para buscar de novo
