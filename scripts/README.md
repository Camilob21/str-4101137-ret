# Scripts

| Script | Semana | Uso (Ubuntu/WSL, con el entorno de Zephyr activado) |
|---|---|---|
| `ciclo.py` | 1 | `python3 scripts/ciclo.py --pristine "texto"` cronometra Enter → `west build -p` → `west flash` → texto en la consola. Sin `--pristine` mide el build incremental. |
| `analizar_lab02.py` | 2–3 | `python3 scripts/analizar_lab02.py captura.csv` analiza un CSV exportado del Logic del AD2: anchos (`C_i`), periodos, jitter y latencia del pulso de flujo. |
| `analizar_traza.py` | 5 | `python3 scripts/analizar_traza.py trace/calib/channel0_0 --metadata trace/metadata --eventos eventos.txt` reconstruye la cadena de preempción, las estadísticas de todos los ticks y la carga de CPU por hilo. |
| `rta.py` | 6 | `python3 scripts/rta.py` calcula U, Liu & Layland, la hiperbólica, la RTA con bloqueo B, el encaje de `calib` y la suma del e-stop. Los datos están en las tablas del inicio (`NODE`, `DANIELA`, `B_US`). `--selftest` lo verifica contra Buttazzo. |
| `calib_cpu.py` | 6 | `python3 scripts/calib_cpu.py trace/channel0_0 --metadata trace/metadata` saca la CPU por settle de `calib` desde la traza CTF y salta los bytes perdidos en el enlace. |
| `trace_diag.py` | 6 | `python3 scripts/trace_diag.py trace/channel0_0 --metadata trace/metadata [--fix]` dice dónde y por qué una traza deja de decodificar. |

`analizar_traza.py` está en `~/4101137-real-time-systems/labs/sops/` en el portátil donde se hizo el lab 5. Hay que copiarlo a esta carpeta antes del primer commit.

**Ojo con la resolución.** `analizar_lab02.py` solo es fiable para pulsos más anchos que el periodo de muestreo del Logic (ver la nota de método en el [RET, §1.3](../RET.md#13-montaje-de-medición)).
