import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# =========================
# CONFIGURAÇÕES MQTT
# =========================

BROKER = "broker.hivemq.com"
PORT = 8883  # TLS
TOPIC = "aeroponia/sensores/dados"


# =========================
# FUNÇÕES AUXILIARES
# =========================

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


# =========================
# CALLBACK DE CONEXÃO
# =========================

def on_connect(client, userdata, flags, rc):
    print(f"on_connect chamado. Código: {rc}", flush=True)

    if rc == 0:
        print("Conectado ao broker MQTT com TLS!", flush=True)
        print(f"Publicando no tópico: {TOPIC}", flush=True)
    else:
        print(f"Erro ao conectar: {rc}", flush=True)


# =========================
# CLIENTE MQTT
# =========================

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Ativa TLS/SSL
client.tls_set()

client.on_connect = on_connect


# =========================
# CONEXÃO MQTT
# =========================

print("Iniciando simulador...", flush=True)
print(f"Broker: {BROKER}", flush=True)
print(f"Porta: {PORT}", flush=True)
print(f"Tópico: {TOPIC}", flush=True)

client.connect(BROKER, PORT, 60)

# Mantém conexão ativa em background
client.loop_start()


# =========================
# LOOP PRINCIPAL
# =========================

try:
    while True:
        dados = gerar_dados()

        resultado = client.publish(TOPIC, json.dumps(dados))

        if resultado.rc == mqtt.MQTT_ERR_SUCCESS:
            print("Dados enviados:", dados, flush=True)
        else:
            print(f"Erro ao publicar MQTT: {resultado.rc}", flush=True)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulador finalizado.", flush=True)
    client.loop_stop()
    client.disconnect()
