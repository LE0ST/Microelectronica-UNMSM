# Informe de Calibración, Caracterización y Validación — Fase 2 (LD2)

**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
**Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Docente:** MsC. Luz Adanaqué Infante  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Fecha de ejecución:** 16 de septiembre de 2026  

---

## 1. Objetivo General de la Fase 2

Validar exhaustiva y empíricamente la infraestructura de simulación, modelos renombrados, extractores automáticos y criterios numéricos en LTspice antes de comenzar el desarrollo de las Actividades 1 a 5 de LD2.

---

## 2. Resultados por Objetivo Específico

### Objetivo 1: Validación de Modelos PTM Renombrados
* **Netlist:** [`auxiliares/validaciones_modelos/val_modelos_concurrente.cir`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/validaciones_modelos/val_modelos_concurrente.cir)
* **Log:** [`auxiliares/validaciones_modelos/val_modelos_concurrente.log`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/validaciones_modelos/val_modelos_concurrente.log)
* **Verificación:** Se incluyeron concurrentemente `ptm45hp.lib`, `ptm45lp.lib` y `ptm130.lib` en un único esquemático polarizando 6 transistores activos (NMOS y PMOS en cada tecnología).
* **Evidencia cuantitativa de conducción:**
  * 45nm HP ($V_{DD}=1.0\text{ V}$): $I_{on,n} = 112.08\,\mu\text{A}$, $I_{on,p} = 122.86\,\mu\text{A}$ ($W_n=90\text{n}, W_p=135\text{n}$).
  * 45nm LP ($V_{DD}=1.1\text{ V}$): $I_{on,n} = 43.04\,\mu\text{A}$, $I_{on,p} = 38.95\,\mu\text{A}$ ($W_n=90\text{n}, W_p=135\text{n}$).
  * 130nm bulk ($V_{DD}=1.3\text{ V}$): $I_{on,n} = 252.86\,\mu\text{A}$, $I_{on,p} = 177.26\,\mu\text{A}$ ($W_n=260\text{n}, W_p=390\text{n}$).
* **Estado:** **PASS**. Cero colisiones de nombres `.model`, convergencia Newton limpia en 0.199 s.

---

### Objetivo 2: Caracterización del Inversor de Salida de Referencia
* **Directorio:** [`auxiliares/caracterizacion_inversor/`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/caracterizacion_inversor/)
* **Dimensionamiento oficial LD2 (§4.3):** $L_n = 45\text{ nm}, W_n = 90\text{ nm}, W_p = 135\text{ nm}$ ($\beta = 1.5$, a diferencia de $\beta = 2.5$ en LD1). Para 130nm: $L_n = 130\text{ nm}, W_n = 260\text{ nm}, W_p = 390\text{ nm}$.
* **Criterio matemático de extracción:**
  * $V_M$: Voltaje de entrada donde $V_{out} = V_{in}$ (`.meas dc VM FIND V(in) WHEN V(out)=V(in)`).
  * $V_{IL}$: Voltaje de entrada con $V_{in} < V_M$ donde la pendiente $d(V_{out})/d(V_{in}) = -1$.
  * $V_{IH}$: Voltaje de entrada con $V_{in} > V_M$ donde la pendiente $d(V_{out})/d(V_{in}) = -1$.
  * Márgenes de ruido: $NM_L = V_{IL} - V_{OL}$, $NM_H = V_{OH} - V_{IH}$.

#### Tabla Resumen de Umbrales del Inversor
| Proceso / Temp | $V_{DD}$ (V) | $V_M$ (V) | $V_{IL}$ (V) | $V_{IH}$ (V) | $NM_L$ (V) | $NM_H$ (V) | Ganancia Máx |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **45nm HP @ 27°C** | 1.0 | **0.4797** | 0.3675 | 0.5785 | 0.3675 | 0.4215 | 6.13 |
| **45nm HP @ 85°C** | 1.0 | **0.4762** | 0.3545 | 0.5820 | 0.3545 | 0.4180 | 5.76 |
| **45nm LP @ 27°C** | 1.1 | **0.5503** | 0.4890 | 0.6095 | 0.4890 | 0.4905 | 13.22 |
| **45nm LP @ 85°C** | 1.1 | **0.5495** | 0.4830 | 0.6135 | 0.4830 | 0.4865 | 12.69 |
| **130nm bulk @ 27°C** | 1.3 | **0.5833** | 0.4055 | 0.6790 | 0.4055 | 0.6210 | 8.91 |
| **130nm bulk @ 85°C** | 1.3 | **0.5636** | 0.3685 | 0.6635 | 0.3685 | 0.6364 | 8.17 |

* **Conclusión para LD2:**
  En 45nm HP, el umbral estático de referencia para conmutación del inversor es $V_M = 0.4797\text{ V} \approx 0.48\text{ V}$. En consecuencia, una degradación estática prolongada o caída sostenida donde $V(dyn) \le V_M$ conducirá a la conmutación de la salida lógica $out$. No obstante, en régimen dinámico, una perturbación o glitch transitorio que cruce instantáneamente por debajo de $V_M$ no garantiza un fallo lógico definitivo si su duración es inferior al retardo de respuesta del inversor, por lo que su propagación temporal debe verificarse explícitamente en la salida.

---

### Objetivo 3: Validación de Criterios Temporales
* **Netlist:** [`auxiliares/validacion_temporizacion/val_temporizacion.cir`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/validacion_temporizacion/val_temporizacion.cir)
* **Log:** [`auxiliares/validacion_temporizacion/val_temporizacion.log`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/validacion_temporizacion/val_temporizacion.log)
* **Resultados numéricos comparativos (Ciclo 2, $T_{clk}=2\text{ ns}$):**
  * Conteo absoluto de flancos (§5 de la guía):
    * $t_{pHL} = 22.563\text{ ps}$ (TRIG $clk$ RISE=2 en $2.01\text{ ns}$, TARG $dyn$ FALL=1 en $2.0326\text{ ns}$).
    * $t_{pLH} = 25.135\text{ ps}$ (TRIG $clk$ FALL=2 en $3.03\text{ ns}$, TARG $dyn$ RISE=1 en $3.0551\text{ ns}$).
  * Ventanas temporales aisladas (`TD=1.5n` y `TD=2.5n`):
    * $t_{pHL} = 22.563\text{ ps}$ (coincidencia idéntica a 12 decimales).
    * $t_{pLH} = 25.135\text{ ps}$ (coincidencia idéntica a 12 decimales).
  * Retardo de propagación dominó global ($clk \to out$):
    * $t_{pd,eval} = 36.165\text{ ps}$.
* **Conclusión:** Las mediciones temporales pertenecen inequívocamente al mismo ciclo de reloj (Ciclo 2). El uso de `TD` garantiza inmunidad total ante transitorios previos o perturbaciones de flanco.

---

### Objetivo 4: Validación de Convención de Corriente y Potencia
* **Netlist:** [`auxiliares/validacion_corriente/val_corriente.cir`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/validacion_corriente/val_corriente.cir)
* **Log:** [`auxiliares/validacion_corriente/val_corriente.log`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/validacion_corriente/val_corriente.log)
* **Comprobación experimental:**
  * Corriente directa LTspice: $\text{AVG}(I(V_{dd})) = -10.00\text{ mA}$.
  * Corriente suministrada: $\text{AVG}(-I(V_{dd})) = +10.00\text{ mA}$.
  * Potencia suministrada por la fuente: $\text{AVG}(-I(V_{dd}) \cdot V(vdd)) = +10.00\text{ mW}$.
  * Potencia absorbida por la carga: $\text{AVG}(I(R_1) \cdot V(vdd)) = +10.00\text{ mW}$.
* **Regla a propagar a Actividades 1 a 5:**
  1. La potencia media consumida se medirá siempre como `AVG -I(Vdd)*V(vdd)`.
  2. La corriente pico suministrada en precarga (Actividad 4, §8.2) se medirá como `MAX -I(Vdd)`.

---

### Objetivo 5: Experimento Controlado sobre $g_{min}$
* **Netlists:** [`auxiliares/experimento_gmin/test_gmin_gmin_1e12.cir`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/auxiliares/experimento_gmin/test_gmin_gmin_1e12.cir) y `test_gmin_gmin_1e15.cir`.
* **Circuito de prueba:** NAND3 dinámica footed en 45nm LP con reloj detenido en evaluación ($CLK=1, V_{DD}=1.1\text{ V}$) y PDN abierta ($A=B=C=0$), en ventana de retención de $1\,\mu\text{s}$.

#### Resultados Cuantitativos a 27 °C
| Parámetro / Métrica | $g_{min} = 10^{-12}\text{ S}$ (Default) | $g_{min} = 10^{-15}\text{ S}$ (LD2) | $\Delta$ Absoluto | Impacto Observado |
| :--- | :---: | :---: | :---: | :---: |
| Tensión $V(dyn)$ inicial | 1.131690 V | 1.131690 V | $0.23\,\mu\text{V}$ | 0.00 % |
| Tensión $V(dyn)$ final ($1\,\mu\text{s}$) | 1.126655 V | 1.127156 V | $0.50\text{ mV}$ | 0.04 % |
| Caída $\Delta V$ en retención | 5.0349 mV | 4.5344 mV | $0.5004\text{ mV}$ | **+11.04 %** |
| Corriente media total suministrada por $V_{DD}$ durante retención | **2.5770 pA** | **1.4163 pA** | **+1.1606 pA** | **+81.95 %** |

#### Resultados Cuantitativos a 85 °C
| Parámetro / Métrica | $g_{min} = 10^{-12}\text{ S}$ (Default) | $g_{min} = 10^{-15}\text{ S}$ (LD2) | $\Delta$ Absoluto | Impacto Observado |
| :--- | :---: | :---: | :---: | :---: |
| Caída $\Delta V$ en retención ($1\,\mu\text{s}$) | 7.85 mV | 7.35 mV | 0.50 mV | **+6.77 %** |
| Corriente media total suministrada por $V_{DD}$ durante retención | **8.53 pA** | **7.27 pA** | **+1.26 pA** | **+17.31 %** |

* **Conclusiones del experimento:**
  1. La corriente espuria introducida por el solver con $g_{min}=10^{-12}\text{ S}$ es casi constante: $\Delta I \approx 1.16\text{ pA}$ a 27°C y $1.26\text{ pA}$ a 85°C, en concordancia directa con la estimación analítica $G_{min} \cdot V_{DD} = (1\text{ pS})(1.1\text{ V}) = 1.10\text{ pA}$.
  2. A 27°C, donde la corriente media total suministrada por $V_{DD}$ en 45nm LP bajo $g_{min}=10^{-15}\text{ S}$ es de apenas $1.42\text{ pA}$, la conductancia parásita por defecto falsea dicha corriente en un **+81.95%** (y la caída $\Delta V$ en el nodo dinámico en un **+11.04%**).
  3. A 85°C, la corriente física crece por activación térmica a $7.27\text{ pA}$ ($\approx 5\times$), diluyendo el impacto relativo de $g_{min}$ a un **+17.31%**.
  4. Queda empírica y numéricamente demostrada la necesidad de fijar `gmin=1e-15` en todas las actividades de LD2 para evitar medir conductancias artificiales del solver.

---

### Objetivo 6: Validación de Extracción Automática
* **Parsers implementados:**
  * [`scripts/lectura_resultados/parse_spice_raw.py`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/scripts/lectura_resultados/parse_spice_raw.py): Detección automática de codificación de cabecera UTF-16-LE vs ASCII, conteo dinámico de variables y puntos, y lectura binaria/ascii sin offsets fijos.
  * [`scripts/lectura_resultados/parse_spice_log.py`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/scripts/lectura_resultados/parse_spice_log.py): Extracción automática de mediciones `.meas` (escalares y tabulares con `.step`), filtrado estricto de opciones del solver, detección de `FAIL'ed` y captura de advertencias de convergencia.
  * [`scripts/extraccion_metricas/generar_tablas_calibracion.py`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/scripts/extraccion_metricas/generar_tablas_calibracion.py): Script de consolidación que lee JSON/CSV y genera tablas en Markdown/LaTeX sin intervención manual.
* **Estado:** Verificado con 100% de éxito sobre los logs y raws generados en esta fase.

---

### Objetivo 7: Registro de Ensayos
* **Archivo:** [`documentacion/registro_ensayos.csv`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/documentacion/registro_ensayos.csv)
* **Estado:** Actualizado con los 11 ensayos de calibración (`ENS-CAL-01` al `ENS-CAL-11`), todos en estado **PASS**.
