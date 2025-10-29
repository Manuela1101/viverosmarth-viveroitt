import network
import time
import ubinascii
import machine
import random
from umqtt.simple import MQTTClient
from password import WIFI_SSID, MQTT_BROKER, FLESPI_TOKEN, WIFI_PASSWORD

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPICS = {
    "temp": "plantcare/1/temp",
    "hum": "plantcare/1/hum",
    "soil": "plantcare/1/soil",
    "air": "plantcare/1/air",
    "light": "plantcare/1/light",
    "water": "plantcare/1/water"
}

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Conectando a WiFi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nWiFi conectado:", wlan.ifconfig())

# --- MQTT ---
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=FLESPI_TOKEN, password="")
    client.connect()
    print("Conectado a MQTT:", MQTT_BROKER)
    return client

# --- Simulador de sensores ---
def read_sensors():
    # Simula lecturas realistas
    temp = round(random.uniform(20, 35), 1)
    hum = round(random.uniform(30, 90), 1)
    soil = random.randint(0, 100)
    air = random.randint(0, 100)
    light = random.randint(100, 1000)
    water = random.choice([0, 1])

    return {
        "temp": temp,
        "hum": hum,
        "soil": soil,
        "air": air,
        "light": light,
        "water": water
    }

# --- Inicio ---
connect_wifi()
client = connect_mqtt()

print("Iniciando envío de datos simulados...\n")

while True:
    data = read_sensors()
    for key, topic in TOPICS.items():
        value = str(data[key])
        client.publish(topic, value)
        print(f"Publicado {topic}: {value}")
    print("---- Ciclo completado ----\n")
    time.sleep(5)

