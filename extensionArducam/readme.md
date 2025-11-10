# 🌿 Extensión TinyML con Cámara para Proyecto ViveroSmart

**Proyecto base:** viverosmarth-viveroitt  
**Autor:** Equipo Vivero ITT
**Objetivo:** Añadir visión artificial y aprendizaje automático embebido (TinyML) para diagnóstico de salud vegetal.

Este módulo añade soporte de cámara e inferencia TinyML al proyecto [viverosmarth-viveroitt](https://github.com/tectijuana/viverosmarth-viveroitt/tree/feedback), utilizando el **Raspberry Pi Pico W** y el **Arduino Tiny Machine Learning Kit**.

## 🔧 Componentes principales

- **Microcontrolador:** Raspberry Pi Pico W  
- **Cámara:** TinyML Kit (OV7670 o Himax HM01B0)  
- **Modelo ML:** TensorFlow Lite Micro  
- **Comunicación:** WiFi + MQTT (Broker Flespi)  
- **Dashboard:** Integración directa con el dashboard actual de Flespi

---

## 📁 Estructura del Proyecto

/vivero_camera_extension/
│
├── main.ino
├── camera_handler.h
├── camera_handler.cpp
├── mqtt_flespi.h
├── mqtt_flespi.cpp
└── plant_model_data.h // Modelo TinyML (.tflite convertido a C array)

arduino
Copiar código

---

## 🔹 main.ino

```
#include <WiFi.h>
#include <PubSubClient.h>
#include "camera_handler.h"
#include "mqtt_flespi.h"
#include "plant_model_data.h"

#define WIFI_SSID "TU_SSID"
#define WIFI_PASS "TU_PASSWORD"

// Flespi MQTT
#define MQTT_SERVER "mqtt.flespi.io"
#define MQTT_PORT 1883
#define FLESPI_TOKEN "TU_TOKEN_FLESPI"   // En formato "FlespiToken TU_TOKEN"

unsigned long lastCapture = 0;
const unsigned long captureInterval = 3600000; // 1 hora

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(115200);
  delay(1000);

  connectWiFi(WIFI_SSID, WIFI_PASS);
  setupMQTT(client, MQTT_SERVER, MQTT_PORT, FLESPI_TOKEN);
  initCamera();
  initTinyMLModel();
}

void loop() {
  client.loop();
  
  if (millis() - lastCapture > captureInterval) {
    lastCapture = millis();
    
    Serial.println("📸 Capturando imagen...");
    uint8_t* image = captureImage();

    float confidence = runInference(image);
    String plantStatus = (confidence > 0.8) ? "healthy" : "unhealthy";

    sendToFlespi(client, plantStatus, confidence);
    
    Serial.println("✅ Resultado enviado al dashboard Flespi");
  }
}

```

🔹 camera_handler.h
```
#pragma once
#include <Arduino.h>

void initCamera();
uint8_t* captureImage();
void initTinyMLModel();
float runInference(uint8_t* img);
```

🔹 camera_handler.cpp
```
#include "camera_handler.h"
#include <TensorFlowLite.h>
#include "plant_model_data.h"

void initCamera() {
  // Inicialización de cámara OV767X o Himax
  Serial.println("Inicializando cámara...");
  // TODO: usar librería Arduino_OV767X o Himax driver según módulo
}

uint8_t* captureImage() {
  // Simulación temporal
  static uint8_t dummyImage[96*96];
  memset(dummyImage, 128, sizeof(dummyImage));
  return dummyImage;
}

void initTinyMLModel() {
  Serial.println("Inicializando modelo TensorFlow Lite Micro...");
  // TODO: Cargar modelo plant_model_data
}

float runInference(uint8_t* img) {
  // Simulación de inferencia
  return random(70, 100) / 100.0;  // valor aleatorio [0.7 - 1.0]
}
```
🔹 mqtt_flespi.h
```
#pragma once
#include <PubSubClient.h>

void connectWiFi(const char* ssid, const char* pass);
void setupMQTT(PubSubClient &client, const char* server, int port, const char* token);
void sendToFlespi(PubSubClient &client, String status, float confidence);
```
🔹 mqtt_flespi.cpp
```
#include "mqtt_flespi.h"
#include <WiFi.h>

void connectWiFi(const char* ssid, const char* pass) {
  WiFi.begin(ssid, pass);
  Serial.print("Conectando WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado ✅");
}

void setupMQTT(PubSubClient &client, const char* server, int port, const char* token) {
  client.setServer(server, port);
  while (!client.connected()) {
    Serial.print("Conectando a Flespi MQTT...");
    if (client.connect("PicoWClient", "FlespiToken", token)) {
      Serial.println(" conectado ✅");
    } else {
      Serial.print(" fallo, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void sendToFlespi(PubSubClient &client, String status, float confidence) {
  String payload = "{\"timestamp\":\"" + String(millis()) + 
                   "\",\"status\":\"" + status + 
                   "\",\"confidence\":" + String(confidence, 2) + "}";
  client.publish("vivero/planta01/camera/inferencia", payload.c_str());
}
```
☁️ Configuración MQTT en Flespi
Crear un token de acceso con permiso mqtt:publish.

Tópico usado:
vivero/planta01/camera/inferencia

Formato del payload JSON:
```
{
  "timestamp": "2025-11-04T10:00:00Z",
  "status": "healthy",
  "confidence": 0.92,
  "camera_temp": 28.5
}
```
🧩 Arquitectura del Sistema
```
graph TD
A[Camara TinyML Kit] -->|I2C| B[Raspberry Pi Pico W]
B -->|WiFi MQTT| C[Flespi MQTT Broker]
C --> D[Dashboard viverosmarth]
D --> E[Grafana/Prometheus Layer]
```
⚙️ Consideraciones Técnicas
- Almacenamiento: usar SD o buffer circular de imágenes (últimas 10).
- Optimización de energía:
  - Pico W entra en modo sleep entre capturas.
  - Alimentación solar (batería 18650).
- Seguridad: usar TLS + token Flespi.
- OTA opcional: firmware actualizable por MQTT.

