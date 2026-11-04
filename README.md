# Sistemas en Tiempo Real — SoilSense Control (ESP32-S3)

Repositorio de la pareja para **Sistemas en Tiempo Real** (4101137), Universidad Nacional de Colombia, sede Manizales, 2026-2.

| Integrante | Labs 1–6 |
|---|---|
| Camilo Yela | Pareja |
| Camilo Obando | Pareja |

**El informe es [`RET.md`](RET.md)** (Timing Evidence Report): requisitos, tareas, ADRs y la evidencia medida de las semanas 1 a 6, con cada captura enlazada.

## Organización

| Carpeta / archivo | Contenido |
|---|---|
| [`RET.md`](RET.md) | El RET, según la [plantilla del curso](https://github.com/saacifuentesmu/4101137-real-time-systems/blob/main/templates/ret.md) |
| [`img/lab1/`](img/lab1/) … [`img/lab6/`](img/lab6/) | Evidencia de cada lab: capturas de WaveForms (AD2), consola, trazas y fotos |
| [`logs/lab6/`](logs/lab6/) | Transcripciones de consola y salidas de scripts (semana 6) |
| [`scripts/`](scripts/) | Scripts propios de medición y análisis |
| [`firmware/`](firmware/) | Lo que escribimos de firmware que no está en el repo del curso: el overlay del port al ESP32-S3 y las apps de la semana 6 (`lab06/fig413`, `lab06/node_w6`) |
| [`presentacion/`](presentacion/) | Presentación de la revisión de diseño (workshop, semana 7) |

El firmware base, las guías y los SOP están en el [repo del curso](https://github.com/saacifuentesmu/4101137-real-time-systems). Aquí solo va lo que producimos nosotros.

## Montaje

- **Placa del nodo:** ESP32-S3-DevKitC-1, ESP32-S3 rev. v0.2, 240 MHz.
- **Toolchain:** Zephyr v4.4.0-14199-g4c6971ba90a3 sobre WSL2/Ubuntu, con VS Code.
- **Instrumento:** Analog Discovery 2 + WaveForms, con Logic, Scope y Patterns. Los seis GPIO de instrumentación (4, 5, 6, 7, 15 y 17) van a DIO 0–5, y los pulsos de flujo salen de DIO 7 a GPIO16. El cableado completo está en el [RET, §1.3](RET.md#13-montaje-de-medición).

## Reglas

- Nombres de archivo en minúsculas, sin espacios ni tildes, con prefijo de evidencia (por ejemplo `img/lab4/e05_persistencia_cambio_contexto.png`).
- Toda afirmación de tiempo en el RET cita una medición y su instrumento (*"show me the trace"*).
- Un commit por cambio lógico, con un mensaje que diga qué semana o sección se actualizó.
- Para el workshop (semana 7), el RET se congela con el tag `workshop`.
