# Firmware propio

| Archivo | Va en (repo del curso) | Qué es |
|---|---|---|
| `esp32s3_devkitc_esp32s3_procpu.overlay` | `firmware/superloop/boards/` | El port al ESP32-S3 (semana 3, Tarea A): pines de instrumentación en `&gpio0`, válvula en GPIO21, pulsos de flujo en GPIO16 y la OLED en `&i2c0`. Sin cambios en C. |

Los cambios de C de las semanas 2–4 (TASK 1–3, hilo de muestreo, migración completa) están en el fork del curso, carpeta `firmware/superloop/src/main.c`, y descritos con sus fragmentos en el [RET, §3](../RET.md#3-evidencia-por-semana).
