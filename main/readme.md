# ☁️ Módulo de Telemetría IoT para Proyecto ViveroSmart  
**Proyecto base:** `viverosmarth-viveroitt`  
**Autor:** Equipo Vivero ITT  
**Plataforma:** ESP32 / ESP8266 con MicroPython  

---

## 🎯 Objetivo

Desarrollar un módulo de comunicación IoT para el sistema **ViveroSmart**, encargado de enviar lecturas de sensores ambientales y del suelo a la plataforma central a través del protocolo **MQTT**, utilizando una conexión WiFi local.  
Este componente permite la integración del diagnóstico TinyML embebido con los datos ambientales del vivero, proporcionando un monitoreo integral del entorno de las plantas.

---

## 🧠 Descripción General

El sistema simula un conjunto de sensores ambientales y de suelo que envían datos en tiempo real mediante MQTT hacia el *broker* configurado (por ejemplo, **Flespi** o **Mosquitto en AWS**).  
Cada lectura incluye variables de temperatura, humedad, calidad del aire, luminosidad y nivel de agua, las cuales son publicadas en tópicos específicos bajo la jerarquía del proyecto.

El módulo puede ejecutarse tanto en modo real (con sensores físicos) como en **modo simulado** para pruebas de integración y conectividad.

---

## 🧩 Componentes y Dependencias

| Componente | Descripción |
|-------------|-------------|
| ESP32 / ESP8266 | Microcontrolador con WiFi integrado compatible con MicroPython |
| MicroPython | Entorno ligero de ejecución en Python para sistemas embebidos |
| MQTT Broker (Flespi / Mosquitto) | Servidor que recibe y distribuye los mensajes publicados por los dispositivos |
| Librería `umqtt.simple` | Cliente MQTT nativo para MicroPython |
| Archivo `password.py` | Archivo local con credenciales WiFi y del broker MQTT |

---

## ⚙️ Código Principal
~~~
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

# --- Conexión WiFi ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Conectando a WiFi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nWiFi conectado:", wlan.ifconfig())

# --- Conexión MQTT ---
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

# --- Inicio del sistema ---
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
~~~
---
## 🔍 Flujo de Trabajo

Conexión WiFi:
El microcontrolador se conecta a la red WiFi utilizando las credenciales del archivo password.py.

Inicialización MQTT:
Se establece la comunicación con el broker MQTT remoto (por ejemplo, Flespi.io).

Lectura / Simulación de sensores:
Se generan valores aleatorios que simulan datos reales de un entorno de vivero.

Publicación de datos:
Cada variable se publica en su tópico MQTT correspondiente (ej. plantcare/1/temp).

Monitoreo continuo:
El ciclo se repite cada 5 segundos, enviando nuevas lecturas.

---

## ☁️ Integración con ViveroSmart

Los tópicos publicados por este módulo pueden ser suscritos desde:

La plataforma central del ViveroSmart Dashboard

Scripts Python de visualización (por ejemplo, en Grafana o Node-RED)

Sistemas TinyML locales que correlacionen condiciones ambientales con diagnóstico foliar






 


