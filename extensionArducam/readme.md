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

## ⚙️ Código Base (TinyML Loop)

```cpp
#include <Arduino_TensorFlowLite.h>
#include <TensorFlowLite.h>
#include <OV767X.h>
#include "model.h"

int32_t frame_buffer[96*96];
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;

void setup() {
  Serial.begin(115200);
  Camera.begin(QVGA, RGB565, 1);
  tflite_setup(model_tflite);
}

void loop() {
  if (Camera.available()) {
    Camera.readFrame(frame_buffer);
    preprocess(frame_buffer, input);
    tflite_invoke();
    
    int state = argmax(output);
    Serial.print("Estado vegetal: "); Serial.println(state);
    updateLED(state);
  }
}
```

---

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
