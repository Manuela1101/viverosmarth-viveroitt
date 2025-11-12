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

## 📁 Estructura del Proyecto



 


