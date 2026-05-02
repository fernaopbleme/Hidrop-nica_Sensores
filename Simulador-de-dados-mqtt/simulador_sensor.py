import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 8883
TOPIC = "aeroponia/sensores/dados"


def random_between(min_val, max_val, decimals=2):
    return round(random.uniform(min_val, max_val), decimals)


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


def on_connect(client, userdata, flags, rc):
    print(f"on_connect simulador. Código: {rc}", flush=True)

    if rc == 0:
        print("Simulador conectado ao broker MQTT com TLS!", flush=True)
        print(f"Publicando no tópico: {TOPIC}", flush=True)
    else:
        print(f"Erro ao conectar simulador: {rc}", flush=True)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.tls_set()
client.on_connect = on_connect

print("Iniciando simulador...", flush=True)
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        dados = gerar_dados()
        payload = json.dumps(dados)

        result = client.publish(TOPIC, payload)

        print("Dados enviados:", payload, "Resultado:", result.rc, flush=True)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulador finalizado.", flush=True)
    client.loop_stop()
    client.disconnect()
