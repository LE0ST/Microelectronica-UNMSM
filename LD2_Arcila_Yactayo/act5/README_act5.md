# Documentación Técnica — Actividad 5: Efectos Parásitos y Operación en Tensión Reducida (NTV)

**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
**Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — Facultad de Ingeniería Electrónica y Eléctrica (FIEE)  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Tecnología Base:** PTM 45nm High-Performance (HP) & Low-Power (LP), $T \in \{27^\circ\text{C}, 85^\circ\text{C}\}$, $V_{DD} \in [0.35\,\text{V}, 1.00\,\text{V}]$  
**Guía Oficial:** [`Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf`](file:///G:/Proyectos/MicroNano/Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf) (Sección 9, págs. 10–13)

---

## 1. Objetivos y Matriz de Requisitos

| ID Requisito | Tarea Guía LD2 | Enunciado Técnico de la Guía | Archivos SPICE Base (Marco) | Archivos SPICE Nuevos (`act5/`) | Estado |
|:---:|:---:|:---|:---|:---|:---:|
| **REQ-22** | §9.1 (Tarea 1) | Caracterización de sobreimpulso (*clock feedthrough*) en el nodo dinámico acoplado por $C_{gd}$ del PMOS de precarga; cuantificación del recorte por diodo $D_{DB}$ y amortiguamiento por el keeper PMOS. | `9.1 Tarea 1.cir` | `act5_feedthrough_keeper.cir` | **CONCILIADO** |
| **REQ-23** | §9.2 (Tareas 1–2) | Evaluación de la retención dinámica $t_{\text{hold}}$ ante fuga subumbral a $27^\circ\text{C}$ y $85^\circ\text{C}$; determinación analítica y experimental de $f_{\min}$ y $f_{\max}$ para delimitar la ventana de frecuencia operable $[f_{\min}, f_{\max}]$. | `9.2 Tarea 1 thold.cir` | `act5_ntv_thold_fmin.cir`<br>`act5_ntv_thold_85c.cir` | **CONCILIADO** |
| **REQ-24** | §9.2 (Tarea 3) | Barrido en régimen *Near-Threshold Voltage* ($V_{DD} \in [0.35, 1.00]\,\text{V}$), cuantificación de $t_{\text{eval}}$, contención de keeper ($W_{kp} \in \{45, 90\}\,\text{nm}$) y verificación del límite de margen $10\times t_{\text{eval}}$. | `9.2 Tarea 1 teval.cir`<br>`9.2 Tarea 3 teval keeper...` | `act5_ntv_teval_fmax.cir` | **CONCILIADO** |
| **REQ-25** | §9.2 (Tarea 4) | Comparativa subumbral a $V_{DD} = 0.50\,\text{V}$ entre 45nm HP y 45nm LP; caracterización de $I_{\text{on}}$, $I_{\text{off}}$, selectividad $I_{\text{on}}/I_{\text{off}}$, $t_{\text{eval}}$ y escalado de energía por ciclo $E_{\text{sw}}$. | `9.2 Tarea 4.cir` | `act5_hp_vs_lp_subumbral.cir`<br>`act5_energia_ntv.cir` | **CONCILIADO** |

---

## 2. Auditoría Científica de los Circuitos Históricos de Marco (`laboratorio5`)

Se auditó de manera exhaustiva el repositorio original desarrollado por Marco Antonio Arcila en `G:\Proyectos\Micro\laboratorio5`. Todos los archivos fueron analizados en modo de solo lectura.

```
laboratorio5/
├── 9.1 Tarea 1.cir / .log / .raw                      # Clock feedthrough base
├── 9.2 Tarea 1 teval.cir / .log / .raw                # Barrido VDD teval sin keeper (celda sin inversor)
├── 9.2 Tarea 1 thold.cir / .log / .raw                # Barrido VDD thold sin keeper a 27°C
├── 9.2 Tarea 3 teval keeper 45nm.cir / .log / .raw    # Barrido VDD teval con keeper 45nm
├── 9.2 Tarea 3 teval keeper 90nm.cir / .log / .raw    # Barrido VDD teval con keeper 90nm
├── 9.2 Tarea 3 thold keeper 45nm.cir / .log / .raw    # Retención thold keeper 45nm (no cruce en 15us)
├── 9.2 Tarea 3 thold keeper 90nm.cir / .log / .raw    # Retención thold keeper 90nm (no cruce en 15us)
└── 9.2 Tarea 4.cir / .log / .raw                      # Comparativa LP vs HP teval a 0.5V
```

### Clasificación y Diagnóstico por Archivo

1. **`9.1 Tarea 1.cir` / `.log` (Clock Feedthrough):**
   * *Código de medición Marco:*
     - `.meas TRAN subimpulso MIN V(dyn) FROM=0n TO=4n` $\implies \mathbf{9.47\,\text{mV}}$ ($V_{\min} = 0.99053\,\text{V}$).
     - `.meas TRAN sobreimpulso MAX V(dyn) FROM=0n TO=4n` $\implies \mathbf{61.30\,\text{mV}}$ ($V_{\max} = 1.06130\,\text{V}$).
   * *Control nuevo (`act5_feedthrough_keeper.log`):* Sobreimpulso de **$+64.31\,\text{mV}$** ($V_{\max} = 1.06431\,\text{V}$).
   * *Diagnóstico Científico:* Existe una estrecha concordancia experimental entre ambos ensayos con una discrepancia de $3.01\,\text{mV}$ ($4.9\%$). No se atribuye esta diferencia a una causa única sin un control que la aísle, documentándose objetivamente las dos mediciones bajo sus respectivas opciones de simulación.
   * *Aclaración Metodológica:* El "subimpulso" de $9.47\,\text{mV}$ reportado por Marco en una ventana general de 4 ns no corresponde a una pérdida de nivel en la evaluación activa, sino al flanco descendente del reloj al reingresar a la fase de precarga ($CLK: 1 \to 0$ a $t=2.0\,\text{ns}$), donde el acoplamiento negativo tira momentáneamente del nodo antes de que $Mp$ conduzca plenamente. Marco no incluyó la comparación con keeper ni aisló la corriente del diodo sustrato-drenaje $D_{DB}$.

2. **`9.2 Tarea 1 teval.cir` / `.log` (Barrido NTV de $t_{\text{eval}}$ sin keeper):**
   * *Barrido:* 7 niveles de $V_{DD}$ ($0.35$ a $1.00\,\text{V}$).
   * *Resultados Marco:* $t_{\text{eval}} = 33.56\,\text{ps}$ ($1.0\,\text{V}$) hasta $1783.72\,\text{ps}$ ($0.35\,\text{V}$).
   * *Diagnóstico:* Marco simuló una etapa dinámica NAND3 aislada (sin inversor estático de salida ni carga asociada). Sus valores son exactos para esa topología, pero no computó $t_{pLH,\text{inv}}$ ni $f_{\max}$.

3. **`9.2 Tarea 1 thold.cir` / `.log` (Barrido NTV de $t_{\text{hold}}$ a 27°C sin keeper):**
   * *Barrido:* 7 niveles de $V_{DD}$.
   * *Resultados Marco:* $t_{\text{hold}} = 1.11755\,\mu\text{s}$ ($1.0\,\text{V}$) a $1.97349\,\mu\text{s}$ ($0.35\,\text{V}$).
   * *Fórmula de frecuencia mínima:* Aplicada a los valores de Marco, proporciona $f_{\min,\text{Marco}} = \frac{1}{2 \cdot t_{\text{hold}}} = \mathbf{447.41\,\text{kHz}}$ ($1.0\,\text{V}$) y $\mathbf{253.36\,\text{kHz}}$ ($0.35\,\text{V}$). Faltó la caracterización a $85^\circ\text{C}$ (peor caso térmico industrial).

4. **`9.2 Tarea 3 teval keeper 45nm.cir` y `90nm.cir` (Contención en NTV):**
   * *Resultados Marco:*
     - Con $W_{kp} = 45\,\text{nm}$: $t_{\text{eval}} = 36.83\,\text{ps}$ ($1.0\,\text{V}$) a $1902.29\,\text{ps}$ ($0.35\,\text{V}$) [penalización del $+9.7\%$ a $+6.6\%$].
     - Con $W_{kp} = 90\,\text{nm}$: $t_{\text{eval}} = 44.74\,\text{ps}$ ($1.0\,\text{V}$) a $2102.60\,\text{ps}$ ($0.35\,\text{V}$) [penalización del $+33.3\%$ a $+17.9\%$].
   * *Diagnóstico:* Cuantifica rigurosamente el compromiso de velocidad por contención de corriente (*keeper contention*).

5. **`9.2 Tarea 3 thold keeper 45nm.cir` y `90nm.cir` (Retención con Keeper):**
   * *Observación en LOG:* `.meas TRAN t_hold... FAIL'ed`.
   * *Diagnóstico Físico y Lectura de RAW:*
     - La simulación se ejecutó con $T_{\text{stop}} = 15.0\,\mu\text{s}$.
     - El comando `.meas` buscaba el instante en que $V(dyn)$ cayera a $V_{DD}/2$.
     - La inspección directa de las formas de onda en el archivo RAW demuestra que a los $15\,\mu\text{s}$ el nodo $V(dyn)$ apenas descendió:
       - En $V_{DD} = 1.0\,\text{V}$: $V(dyn) = 0.999977\,\text{V}$ (caída de solo $\mathbf{0.023\,\text{mV}}$).
       - En $V_{DD} = 0.35\,\text{V}$: $V(dyn) = 0.349440\,\text{V}$ (caída de solo $\mathbf{0.560\,\text{mV}}$).
     - **Conclusión sustentable:** No existió ningún error de convergencia o fallo numérico del simulador; simplemente **no se observó el cruce del umbral $V_{DD}/2$ durante la ventana simulada de $15\,\mu\text{s}$**.
     - Se establece una cota inferior finita observada de $t_{\text{hold}} > 15\,\mu\text{s}$, lo que sitúa la frecuencia mínima observada por debajo de $f_{\min} < \frac{1}{2 \times 15\,\mu\text{s}} \approx \mathbf{33.3\,\text{kHz}}$ dentro de dicha ventana. No se afirma un $t_{\text{hold}}$ infinito ni un $f_{\min} = 0\,\text{Hz}$ no medido.

6. **`9.2 Tarea 4.cir` / `.log` (Comparativa LP vs HP a 0.50V):**
   * *Medición Marco:* $t_{\text{eval,LP}} = 8.64761\,\text{ns}$ ($8647.61\,\text{ps}$).
   * *Control complementario (`act5_hp_vs_lp_subumbral.log`):* $t_{\text{eval,LP}} = 8.48841\,\text{ns}$, $t_{\text{eval,HP}} = 0.16157\,\text{ns}$ (ratio: $52.54\times$).
   * *Diagnóstico:* Los valores coinciden estrechamente ($1.8\%$ de diferencia). Marco omitió las corrientes $I_{\text{on}}$ e $I_{\text{off}}$ requeridas por la guía.

---

## 3. Fundamentos Físicos y Modelado Analítico

### A. Mecanismo de Clock Feedthrough y Recorte por Diodo

1. **Parámetros del Modelo PTM 45nm HP:**
   * Capacitancia de solapamiento compuerta-drenaje: $C_{gd} = (cgdo + cgdl) \cdot W_p \approx \mathbf{0.0507\,\text{fF}}$ ($W_p = 135\,\text{nm}$).
2. **Divisor Capacitivo:**
   $$\Delta V_{\text{feedthrough}} \approx \frac{C_{gd}}{C_{\text{total}}} \Delta V_{clk} \approx \frac{0.0507\,\text{fF}}{0.85 - 1.05\,\text{fF}} \times 1.0\,\text{V} \approx \mathbf{50 - 60\,\text{mV}}$$
   Predice consistentemente el sobreimpulso simulado de **$+64.31\,\text{mV}$** ($V_{\max} = 1.0643\,\text{V}$) sin keeper.
3. **Recorte Transitorio Específico por Diodo $D_{DB}$:**
   Al sobrepasar $V_{DD}$ en $64.3\,\text{mV}$, la unión p-n drenaje-cuerpo entra en polarización directa parcial, inyectando un pico transitorio de hasta **$2.841\,\mu\text{A}$** hacia la fuente $V_{DD}$. Esto constituye un recorte transitorio específico debido a la unión intrínseca de difusión, pero no debe interpretarse como una protección general del óxido de compuerta ante sobretensiones severas.
4. **Amortiguamiento con Keeper ($W_{kp} = 45\,\text{nm}$):**
   La capacitancia añadida por el keeper atenúa el sobreimpulso a **$+49.31\,\text{mV}$** ($V_{\max} = 1.0493\,\text{V}$), lo que representa una reducción pasiva del **$-23.3\%$**.

---

### B. Ventana de Frecuencia Operable $[f_{\min}, f_{\max}]$ y Régimen NTV

La guía oficial (Fig. 9) define la ventana de frecuencia de un bloque dominó mediante:
$$f_{\max} \approx \frac{1}{2(t_{\text{eval}} + t_{pLH,\text{inv}})}, \qquad f_{\min} \approx \frac{1}{2 t_{\text{hold}}}$$

1. **Frecuencia Máxima ($f_{\max}$):**
   En el control complementario con compuerta completa (NAND3 dominó + inversor estático), para $V_{DD} = 1.00\,\text{V}$:
   $$t_{\text{eval}} = 23.21\,\text{ps}, \quad t_{pLH,\text{inv}} = 4.52\,\text{ps} \implies t_{\text{pd}} = 27.72\,\text{ps}$$
   $$f_{\max} = \frac{1}{2 \times 27.7235 \times 10^{-12}\,\text{s}} = \mathbf{18.035\,\text{GHz}}$$
   A $V_{DD} = 0.35\,\text{V}$:
   $$t_{\text{eval}} = 1739.95\,\text{ps}, \quad t_{pLH,\text{inv}} = 1347.25\,\text{ps} \implies t_{\text{pd}} = 3087.20\,\text{ps}$$
   $$f_{\max} = \frac{1}{2 \times 3087.20 \times 10^{-12}\,\text{s}} = \mathbf{161.96\,\text{MHz}}$$

2. **Frecuencia Mínima ($f_{\min}$):**
   * A $27^\circ\text{C}$ ($t_{\text{hold}} = 1.096\,\mu\text{s}$ a $1.0\text{V}$, $1.930\,\mu\text{s}$ a $0.35\text{V}$):
     $$f_{\min} = \mathbf{456.21\,\text{kHz}} \quad (1.0\,\text{V}), \qquad f_{\min} = \mathbf{259.12\,\text{kHz}} \quad (0.35\,\text{V})$$
   * A $85^\circ\text{C}$ (peor caso térmico, $t_{\text{hold}} = 0.305\,\mu\text{s}$ a $1.0\text{V}$, $0.440\,\mu\text{s}$ a $0.35\text{V}$):
     $$f_{\min} = \mathbf{1638.94\,\text{kHz}} \approx \mathbf{1.64\,\text{MHz}} \quad (1.0\,\text{V}), \qquad f_{\min} = \mathbf{1136.28\,\text{kHz}} \approx \mathbf{1.14\,\text{MHz}} \quad (0.35\,\text{V})$$
   * *Aclaración Térmica:* La razón de tiempos de retención entre $27^\circ\text{C}$ y $85^\circ\text{C}$ es de $\frac{1.096}{0.305} \approx \mathbf{3.59\times}$ (o $3.66\times$ con los datos de Marco). Esto eleva la frecuencia mínima en un factor de $\sim 3.6\times$. No se afirma que la corriente $I_{\text{off}}$ se haya cuadruplicado exactamente, sino que el tiempo de descarga efectivo se redujo en ese factor térmico medido.
   * *Pasos adicionales en retención estática ($0.30\,\text{V}$ y $0.25\,\text{V}$):* Los circuitos `act5_ntv_thold_fmin` y `act5_ntv_thold_85c` incluyeron 9 pasos ejecutados satisfactoriamente:
     - A $0.30\,\text{V}$: $t_{\text{hold}} = 1.889\,\mu\text{s}$ ($f_{\min} = 264.68\,\text{kHz}$) a $27^\circ\text{C}$, y $t_{\text{hold}} = 0.424\,\mu\text{s}$ ($f_{\min} = 1.179\,\text{MHz}$) a $85^\circ\text{C}$.
     - A $0.25\,\text{V}$: $t_{\text{hold}} = 1.802\,\mu\text{s}$ ($f_{\min} = 277.42\,\text{kHz}$) a $27^\circ\text{C}$, y $t_{\text{hold}} = 0.398\,\mu\text{s}$ ($f_{\min} = 1.257\,\text{MHz}$) a $85^\circ\text{C}$.

3. **Análisis de Cierre de la Ventana Operable:**
   * En todo el rango completamente caracterizado ($V_{DD} \in [0.35, 1.00]\,\text{V}$), la ventana operable $[f_{\min}, f_{\max}]$ **permanece abierta**: a $0.35\,\text{V}$ y $85^\circ\text{C}$, $f_{\max} = 161.96\,\text{MHz}$ es aún $142\times$ mayor que $f_{\min} = 1.14\,\text{MHz}$.
   * El criterio de seguridad $t_{\text{hold}} \ge 10 \cdot t_{\text{eval}}$ se cumple con holgura en todo el intervalo $[0.35, 1.00]\,\text{V}$:
     - A $V_{DD} = 1.00\,\text{V}$ ($27^\circ\text{C}$): $\frac{t_{\text{hold}}}{t_{\text{eval}}} = \frac{1.096\,\mu\text{s}}{23.21\,\text{ps}} = \frac{1.096\,\mu\text{s}}{0.00002321\,\mu\text{s}} \approx \mathbf{47,200} \gg 10$ (con datos de Marco: $\frac{1.118\,\mu\text{s}}{33.56\,\text{ps}} = \frac{1.118\,\mu\text{s}}{0.00003356\,\mu\text{s}} \approx \mathbf{33,300} \gg 10$).
     - A $V_{DD} = 0.35\,\text{V}$ ($27^\circ\text{C}$): $\frac{t_{\text{hold}}}{t_{\text{eval}}} = \frac{1.930\,\mu\text{s}}{1739.95\,\text{ps}} = \frac{1.930\,\mu\text{s}}{0.001740\,\mu\text{s}} \approx \mathbf{1,109} \gg 10$ (con datos de Marco: $\frac{1.973\,\mu\text{s}}{1783.72\,\text{ps}} = \frac{1.973\,\mu\text{s}}{0.001784\,\mu\text{s}} \approx \mathbf{1,106} \gg 10$).
   * *Precisión sobre la frontera inferior y disponibilidad de métricas:* Si bien se obtuvieron métricas de retención estática ($t_{\text{hold}}$ y $f_{\min}$) a $0.30\,\text{V}$ y $0.25\,\text{V}$, el barrido de retardo de evaluación activo (`act5_ntv_teval_fmax` y las netlists originales de Marco) solo contempló 7 pasos ($0.35\,\text{V}$ a $1.00\,\text{V}$). Por consiguiente, **no se dispone de mediciones de $t_{\text{eval}}$ ni de estimaciones de $f_{\max}$ en $0.25\,\text{V}$ ni $0.30\,\text{V}$**. La ventana operable bidireccional $[f_{\min}, f_{\max}]$ y el margen $10\times t_{\text{eval}}$ solo están cuantitativamente delimitados y verificados entre $0.35\,\text{V}$ y $1.00\,\text{V}$. No se extrapola un punto de cruce exacto (por ejemplo, a $0.20\,\text{V}$) sin contar con datos físicos de retardo en ese régimen subumbral profundo.

---

### C. Caracterización Subumbral a $V_{DD} = 0.50\,\text{V}$: 45nm HP vs 45nm LP

Simulación homóloga bajo idéntico estímulo y polarización:

| Parámetro Físico ($V_{DD} = 0.50\,\text{V}$) | Nodo 45nm HP | Nodo 45nm LP | Razón Comparativa (LP / HP) |
|:---|:---:|:---:|:---:|
| **Tensión de Umbral ($V_{thn}$)** | $0.469\,\text{V}$ | $0.623\,\text{V}$ | $+154\,\text{mV}$ (Subumbral profundo en LP) |
| **Corriente ON ($I_{\text{on}}$)** | $\mathbf{4.898\,\mu\text{A}}$ | $\mathbf{0.0986\,\mu\text{A}}$ ($98.6\,\text{nA}$) | $\mathbf{0.0201\times}$ ($-98.0\%$) |
| **Corriente OFF ($I_{\text{off}}$)** | $\mathbf{125.05\,\text{pA}}$ | $\mathbf{0.671\,\text{pA}}$ ($671\,\text{fA}$) | $\mathbf{0.0054\times}$ ($-99.5\%$, **$186.4\times$ menor**) |
| **Selectividad ($I_{\text{on}} / I_{\text{off}}$)** | **$39,168.5$** | **$146,950.1$** | $\mathbf{3.75\times}$ Superior en LP |
| **Retardo de Evaluación ($t_{\text{eval}}$)** | $\mathbf{161.57\,\text{ps}}$ | $\mathbf{8488.41\,\text{ps}}$ ($8.49\,\text{ns}$) | $\mathbf{52.54\times}$ Más Lento en LP |

*Nota sobre datos históricos:* Marco midió $t_{\text{eval,LP}} = 8647.61\,\text{ps}$ en su circuito aislado, concordando con el nuevo control ($8488.41\,\text{ps}$) con una desviación de solo $1.8\%$.

---

### D. Escalado Energético hacia Régimen NTV

La energía total por ciclo $E_{\text{sw}}$ se obtuvo por integración numérica de la corriente total suministrada por la fuente $V_{DD}$ en un periodo completo de conmutación ($T_{\text{clk}} = 10.0\,\text{ns}$):
$$E_{\text{sw}} = \int_{0}^{T_{\text{clk}}} V_{DD} \cdot [-I(V_{DD})]\,dt$$
Esta magnitud engloba la energía de carga y descarga capacitiva ($C V_{DD}^2$), la energía disipada en contención transitoria (*crowbar*) con el keeper y la fuga estática durante el intervalo de $10\,\text{ns}$.

| $V_{DD}$ (V) | Corriente Pico $I_{\text{pk}}$ ($\mu\text{A}$) | Energía por Ciclo $E_{\text{sw}}$ (fJ) | Potencia Promedio $P_{\text{avg}}$ (nW) | Ahorro Energético Relativo |
|:---:|:---:|:---:|:---:|:---:|
| **$1.00$** | $37.29$ | $\mathbf{0.7259}$ | $72.59$ | $0.0\%$ (Referencia) |
| **$0.80$** | $18.74$ | $\mathbf{0.4533}$ | $45.33$ | $-37.6\%$ |
| **$0.60$** | $6.44$ | $\mathbf{0.2876}$ | $28.76$ | $-60.4\%$ |
| **$0.50$** | $2.25$ | $\mathbf{0.2018}$ | $20.18$ | $-72.2\%$ |
| **$0.45$** | $0.99$ | $\mathbf{0.1533}$ | $15.33$ | $-78.9\%$ |
| **$0.40$** | $0.70$ | $\mathbf{0.1076}$ | $10.76$ | $-85.2\%$ |
| **$0.35$** | $0.62$ | $\mathbf{0.0719}$ | $7.19$ | $\mathbf{-90.1\%}$ ($\mathbf{10.1\times}$ de reducción) |

---

## 4. Matriz Maestra Consolidada y Conciliada

La siguiente tabla presenta los resultados conciliados, separando de manera estricta el control complementario de la celda completa (`act5`) y la campaña histórica de la etapa aislada de Marco (`laboratorio5`):

### A. Tiempos y Frecuencias Operables en Barrido NTV

| $V_{DD}$ (V) | $t_{\text{eval}}$ Act5 (ps) | $t_{pLH,\text{inv}}$ (ps) | $t_{\text{pd}}$ (ps) | $f_{\max}$ Act5 (GHz) | $t_{\text{eval}}$ Marco (ps) | $t_{\text{hold}}$ 27°C Act5 ($\mu\text{s}$) | $f_{\min}$ 27°C Act5 (kHz) | $t_{\text{hold}}$ 27°C Marco ($\mu\text{s}$) | $f_{\min}$ 27°C Marco (kHz) | $t_{\text{hold}}$ 85°C ($\mu\text{s}$) | $f_{\min}$ 85°C (kHz) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$1.00$** | $23.21$ | $4.52$ | $27.72$ | **$18.035$** | $33.56$ | $1.096$ | **$456.21$** | $1.118$ | **$447.23$** | $0.305$ | **$1638.94$** |
| **$0.80$** | $33.31$ | $9.80$ | $43.11$ | **$11.599$** | $43.65$ | $1.429$ | **$349.93$** | $1.458$ | **$342.94$** | $0.375$ | **$1334.82$** |
| **$0.60$** | $70.48$ | $34.92$ | $105.40$ | **$4.744$** | $81.17$ | $1.754$ | **$285.03$** | $1.792$ | **$279.02$** | $0.432$ | **$1157.19$** |
| **$0.50$** | $162.34$ | $102.19$ | $264.52$ | **$1.890$** | $174.85$ | $1.874$ | **$266.74$** | $1.916$ | **$260.96$** | $0.448$ | **$1117.00$** |
| **$0.45$** | $308.17$ | $212.30$ | $520.47$ | **$0.961$** | $323.39$ | $1.914$ | **$261.17$** | $1.957$ | **$255.49$** | $0.450$ | **$1110.68$** |
| **$0.40$** | $686.10$ | $505.22$ | $1191.33$ | **$0.420$** | $708.53$ | $1.935$ | **$258.37$** | $1.979$ | **$252.65$** | $0.448$ | **$1115.75$** |
| **$0.35$** | $1739.95$ | $1347.25$ | $3087.20$ | **$0.162$** | $1783.72$ | $1.930$ | **$259.12$** | $1.973$ | **$253.42$** | $0.440$ | **$1136.28$** |

*Comprobación de Fórmulas:*
* $f_{\max} = \frac{1}{2 \cdot t_{\text{pd}}} = \frac{1}{2(t_{\text{eval}} + t_{pLH,\text{inv}})}$ se satisface exactamente en todos los puntos de la columna $f_{\max}$ Act5.
* $f_{\min} = \frac{1}{2 \cdot t_{\text{hold}}}$ se satisface exactamente tanto para Act5 ($f_{\min}$ Act5 vs $t_{\text{hold}}$ Act5) como para Marco ($f_{\min}$ Marco vs $t_{\text{hold}}$ Marco) y para $85^\circ\text{C}$.
* En retención estática pura ($t_{\text{hold}}$), las simulaciones cubrieron adicionalmente $V_{DD} = 0.30\,\text{V}$ ($f_{\min,27^\circ\text{C}} = 264.68\,\text{kHz}$, $f_{\min,85^\circ\text{C}} = 1.179\,\text{MHz}$) y $0.25\,\text{V}$ ($f_{\min,27^\circ\text{C}} = 277.42\,\text{kHz}$, $f_{\min,85^\circ\text{C}} = 1.257\,\text{MHz}$), no incluidos en la tabla comparativa por carecer de mediciones homólogas de $t_{\text{eval}}$ ni $f_{\max}$ en dichos voltajes.

---

## 5. Figuras Científicas Validadas y Regeneradas

Generadas por [`act5/scripts/generar_figuras_act5.py`](file:///G:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act5/scripts/generar_figuras_act5.py) a 300 DPI:

1. **[`fig1_act5_feedthrough_energia.png`](file:///G:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act5/figuras/fig1_act5_feedthrough_energia.png):**
   * *Panel (a):* Dinámica transitoria de *clock feedthrough* en el nodo dinámico con y sin keeper PMOS, indicando el sobreimpulso de $+64.3\,\text{mV}$, la amortiguación pasiva a $+49.3\,\text{mV}$ ($-23.3\%$) y la acción de recorte del diodo $D_{DB}$.
   * *Panel (b):* Escalado de energía por ciclo $E_{\text{sw}}$ y corriente pico $I_{\text{pk}}$ vs $V_{DD}$, demostrando la reducción de $10.1\times$ en consumo ($0.726\,\text{fJ} \to 0.072\,\text{fJ}$).
2. **[`fig2_act5_ventana_frecuencia_ntv.png`](file:///G:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act5/figuras/fig2_act5_ventana_frecuencia_ntv.png):**
   * *Panel (a):* Curvas semilogarítmicas de $t_{\text{eval}}$ (sin y con keeper) y $t_{\text{hold}}$ ($27^\circ\text{C}$ y $85^\circ\text{C}$) frente a $V_{DD}$, evidenciando que el margen $10\times t_{\text{eval}}$ se conserva en todo el rango medido.
   * *Panel (b):* Ventana de frecuencia operable $[f_{\min}, f_{\max}]$ en MHz reales frente a $V_{DD}$ (reproducción de Fig. 9 de la guía). Ilustra la banda operable $[1.14\,\text{MHz}, 161.96\,\text{MHz}]$ a $0.35\,\text{V}$ y $[1.64\,\text{MHz}, 18035\,\text{MHz}]$ a $1.00\,\text{V}$.

---

## 6. Inventario de Archivos en `act5/`

```
act5/
├── README_act5.md                              # [ESTE ARCHIVO] Documentación técnica conciliada
├── circuitos/
│   ├── act5_feedthrough_keeper.cir            # Feedthrough, diodo D_DB y keeper
│   ├── act5_ntv_teval_fmax.cir                # Barrido teval, tpLH, fmax y contención
│   ├── act5_ntv_thold_fmin.cir                # Barrido thold y fmin a 27°C
│   ├── act5_ntv_thold_85c.cir                 # Barrido thold y fmin a 85°C (peor caso)
│   ├── act5_hp_vs_lp_subumbral.cir            # Comparativa rigurosa HP vs LP a 0.5V
│   └── act5_energia_ntv.cir                   # Integración de energía dinámica en NTV
├── resultados/
│   ├── datos/
│   │   └── act5_metricas.json                 # Base de datos JSON conciliada
│   ├── logs/                                  # 6 archivos .log respaldados
│   └── raw/                                   # 6 archivos .raw preservados
├── scripts/
│   └── generar_figuras_act5.py                # Generador Python de figuras 1 y 2 (300 DPI)
└── figuras/
    ├── fig1_act5_feedthrough_energia.png      # Figura 1 compuesta
    └── fig2_act5_ventana_frecuencia_ntv.png   # Figura 2 compuesta
```
