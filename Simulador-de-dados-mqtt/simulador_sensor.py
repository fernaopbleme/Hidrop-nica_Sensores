import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# Configurações MQTT
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "aeroponia/sensores/dados"

# Função para gerar valores aleatórios
def random_between(min_val, max_val, decimals=2):
    return round(random.uniform(min_val, max_val), decimals)

# Função que simula os sensores
def gerar_dados():
    return {
        "ph": random_between(5.4, 7.2),
        "ec": random_between(0.8, 2.2),
        "temperaturaAgua": random_between(18, 28, 1),
        "temperaturaAmbiente": random_between(20, 34, 1),
        "umidadeRelativa": random_between(45, 90, 0),
        "nivelAgua": random_between(20, 100, 0),
        "timestamp": datetime.now().isoformat()
    }

# Callback de conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
    else:
        print(f"Erro ao conectar: {rc}")

# Criando cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conectar ao broker
client.connect(BROKER, PORT, 60)

# Loop principal
client.loop_start()

try:
    while True:
        dados = gerar_dados()
        
        client.publish(TOPIC, json.dumps(dados))
        
        print("Dados enviados:", dados)
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulador finalizado.")
    client.loop_stop()
    client.disconnect()