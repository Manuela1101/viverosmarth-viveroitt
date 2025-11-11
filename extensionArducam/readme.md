# 🌿 Extensión TinyML con Cámara para Proyecto ViveroSmart  
**Proyecto base:** `viverosmarth-viveroitt`  
**Autor:** Equipo Vivero ITT  
**Plataforma:** Arduino Tiny Machine Learning Kit (Arduino Nano 33 BLE Sense + OV7675 Camera)

---

## 🎯 Objetivo
Implementar una extensión de **visión artificial embebida** con **TinyML** para el proyecto *ViveroSmart*, permitiendo el **diagnóstico de salud vegetal** mediante la detección temprana de estrés o enfermedad en hojas de plantas.

---

## 🧠 Descripción General

El sistema toma imágenes de hojas usando la cámara del **TinyML Kit** y las procesa localmente para clasificar el estado de la planta:

- 🌱 **Sana**  
- 🍂 **Estrés hídrico**  
- 🦠 **Infección fúngica o bacteriana**

El modelo de **aprendizaje automático** se entrena con TensorFlow Lite y se despliega en el microcontrolador para inferencias en tiempo real sin conexión a internet.

---

## 🧩 Componentes

| Componente | Descripción |
|-------------|--------------|
| Arduino Nano 33 BLE Sense | MCU con procesador ARM Cortex-M4F y sensor IMU, micrófono y BLE |
| Cámara OV7675 | Sensor VGA para capturar imágenes (TinyML Kit) |
| TensorFlow Lite Micro | Librería para inferencia de modelos ML embebidos |
| LED RGB | Indicador de estado (verde = sano, rojo = enfermo, azul = estrés) |
| Sensor DHT11 / BME280 | Medición de temperatura y humedad |
| MQTT o Serial | Comunicación de resultados a la plataforma ViveroSmart |

---

## 🧰 Software y Librerías

- Arduino IDE o Arduino Web Editor  
- TensorFlow Lite for Microcontrollers  
- Arduino_TensorFlowLite  
- Arduino_OV767X  
- Arduino_LSM9DS1 (IMU)  
- ArduinoBLE (para comunicación)  

---

## 🔍 Flujo de Trabajo

1. **Captura de Imagen:**  
   La cámara toma una imagen 96x96 px RGB.

2. **Preprocesamiento:**  
   Reducción de tamaño y normalización.

3. **Inferencia TinyML:**  
   El modelo ejecuta la predicción localmente.

4. **Visualización / Alerta:**  
   LED indica el estado de la planta.  
   Los resultados se envían a ViveroSmart vía BLE o Serial.

---

## 🧪 Entrenamiento del Modelo

1. Recolectar dataset de hojas sanas y enfermas.  
   - Ejemplo: `data/healthy/`, `data/diseased/`, `data/stressed/`
2. Entrenar en TensorFlow con CNN ligera (MobileNetV1 adaptada).  
3. Convertir modelo:  
   ```bash
   tflite_convert --output_file=model.tflite --saved_model_dir=plant_model/
   ```
4. Cuantizar para microcontroladores:  
   ```python
   converter.optimizations = [tf.lite.Optimize.DEFAULT]
   ```

---

## 📸 Código Arduino

``` cpp
#include <Arduino_OV767X.h>

#define FRAME_WIDTH 160
#define FRAME_HEIGHT 120

// Buffer para la imagen (grayscale)
uint8_t frame_buffer[FRAME_WIDTH * FRAME_HEIGHT];

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("📷 Iniciando cámara OV7675...");

  if (!Camera.begin(QQVGA, GRAYSCALE, 1)) {
    Serial.println("❌ Error al iniciar cámara OV7675");
    while (true);
  }

  Serial.println("✅ Cámara inicializada correctamente");
  delay(1000);
}

void loop() {
  // Captura directa del frame
  Camera.readFrame(frame_buffer);

  // Enviar una marca de inicio
  Serial.write(0xFF);
  Serial.write(0xD8);

  // Enviar los datos de la imagen (160x120 bytes)
  Serial.write(frame_buffer, FRAME_WIDTH * FRAME_HEIGHT);

  // Marca de fin
  Serial.write(0xFF);
  Serial.write(0xD9);

  delay(200); // Aproximadamente 5 FPS
}
```

------------------------------------------------------------------------

## 🐍 Script Python: Visualización en tiempo real

Instala dependencias:

``` bash
pip install pyserial numpy opencv-python
```

Ejecuta este script (ajusta el puerto COM según tu caso):

``` python
import serial
import numpy as np
import cv2

PORT = "COM11"   # Cambia al puerto correcto
BAUD = 115200

WIDTH = 160
HEIGHT = 120
FRAME_SIZE = WIDTH * HEIGHT

ser = serial.Serial(PORT, BAUD, timeout=1)
print("Conectado a", PORT)

buffer = bytearray()

while True:
    # Leer hasta tener un frame completo
    if ser.readable():
        buffer += ser.read(FRAME_SIZE + 4)

        # Buscar marca de inicio y fin
        start = buffer.find(b'\xFF\xD8')
        end = buffer.find(b'\xFF\xD9', start + 2)

        if start != -1 and end != -1 and end - start - 2 == FRAME_SIZE:
            frame_bytes = buffer[start + 2:end]
            buffer = buffer[end + 2:]

            # Convertir a numpy array
            frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((HEIGHT, WIDTH))

            # Mostrar imagen
            cv2.imshow("OV7675 Live", frame)
            if cv2.waitKey(1) == 27:  # ESC para salir
                break

ser.close()
cv2.destroyAllWindows()
```

------------------------------------------------------------------------

## ⚙️ Funcionamiento

1.  El Arduino inicializa la cámara OV7675 en resolución **QQVGA
    (160×120)** y modo **grayscale**.\

2.  En cada iteración del `loop()`, captura un frame y lo envía por
    Serial con el siguiente formato:

        [0xFF][0xD8] + 19200 bytes de imagen + [0xFF][0xD9]

3.  El script Python escucha el puerto serial, detecta los marcadores de
    inicio/fin y reconstruye el frame.

4.  OpenCV muestra el flujo de video en una ventana a \~5 FPS.

------------------------------------------------------------------------

## 🧩 Solución de problemas

  -----------------------------------------------------------------------
  Problema                            Solución
  ----------------------------------- -----------------------------------
  ❌ `No device found on COMx`        Verifica el puerto en Arduino IDE o
                                      cambia de cable USB

  ⚫ Imagen distorsionada             Baja la velocidad
                                      `Serial.begin(57600)` o aumenta
                                      `delay(300)`

  🪫 Cámara no inicializa             Usa
                                      `Camera.begin(QQVGA, RGB565, 1)` si
                                      tu sensor no soporta GRAYSCALE

  🧱 No se muestra nada en Python     Revisa que el puerto COM coincida y
                                      que el buffer contenga datos
  -----------------------------------------------------------------------

## 🚀 Resultados Esperados

- Diagnóstico local en menos de **1 segundo** por imagen  
- Clasificación con **precisión >85%**  
- Sin necesidad de conexión constante a internet  
- Integración directa con dashboard *ViveroSmart*

---

## 📚 Referencias

- Arduino TinyML Kit Documentation – [https://docs.arduino.cc/tutorials/](https://docs.arduino.cc/tutorials/)  
- TensorFlow Lite for Microcontrollers – [https://www.tensorflow.org/lite/microcontrollers](https://www.tensorflow.org/lite/microcontrollers)  
- Pete Warden, Daniel Situnayake. *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers* (O'Reilly, 2020)  

---


**© 2025 Equipo Vivero ITT**  
Proyecto académico para extensión del sistema ViveroSmart con visión embebida y TinyML.
