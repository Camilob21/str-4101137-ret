# Firmware propio

| Archivo | Va en (repo del curso) | Qué es |
|---|---|---|
| `esp32s3_devkitc_esp32s3_procpu.overlay` | `firmware/superloop/boards/` | El port al ESP32-S3 (semana 3, Tarea A): pines de instrumentación en `&gpio0`, válvula en GPIO21, pulsos de flujo en GPIO16 y la OLED en `&i2c0`. Sin cambios en C. |
| `lab06/fig413/` | `firmware/fig413/` | Semana 6, Tarea A: Fig. 4.13 de Buttazzo. RM por defecto, EDF con `-DEXTRA_CONF_FILE=edf.conf`. |
| `lab06/node_w6/` | `firmware/node_w6/` | Semana 6, Tareas B y C: nodo con candado `k_sem`/`k_mutex` (`lock sem|mutex`), comando `inv`, marcador del e-stop en GPIO15, sección crítica en GPIO17 y el ADR-005 aplicado. |

Compilar desde el fork del curso (Ubuntu/WSL):

```bash
west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/fig413 -d build_fig413_rm
west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/fig413 -d build_fig413_edf -- -DEXTRA_CONF_FILE=edf.conf
west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/node_w6 -d build_node
```

Los cambios de C de las semanas 2–4 (TASK 1–3, hilo de muestreo, migración completa) están en el fork del curso, carpeta `firmware/superloop/src/main.c`, y descritos con sus fragmentos en el [RET, §3](../RET.md#3-evidencia-por-semana).
