# Plan Experimental y Arquitectura Metodológica — Actividad 3
**Fugas y Dimensionamiento del Transistor Keeper (45nm HP vs LP, 130nm Bulk; 27°C vs 85°C)**  
**Curso:** Microelectrónica y Sistemas Nanoelectrónicos — FIEE UNMSM (2026-II)  
**Docente:** MsC. Luz Adanaqué Infante  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Estado:** PLAN PREVIO CONGELADO — SIN EJECUCIÓN SPICE (En espera de confirmación docente)

---

### 1. Mapeo Riguroso de Requisitos Docentes (REQ-14 a REQ-18)

Conforme a la Sección 7 de la Guía Oficial (`LabDirigido2.pdf`), la Actividad 3 se estructura en cinco tareas vinculantes:

| Requisito | Sección Guía | Tarea Oficial | Objetivo Físico | Variables Clave | Entregable / Evidencia |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **REQ-14** | §7 | Tarea 1 | Retención a reloj detenido ($T_{stop} = 1\,\mu\text{s}$) en 45nm HP a $27^\circ\text{C}$ con PDN abierta ($A=B=C=0$, $CLK=1$). Barrido de $W_{kp} \in [1\text{ nm}, 180\text{ nm}]$. Aislamiento de mecanismos de fuga. | $W_{kp}$, $V_{dyn,\text{end}}$, $t_{hold}$, $I_{net}(dyn) = -C_{dyn} \frac{dV}{dt}$ (solo válido con $W_{kp} \to 0$ en $t=t_0^+$). Componentes: subumbral $M_1$, compuerta $M_p/M_k$, GIDL. | Tabla de barrido; transitorio de descarga; mediciones in situ y caracterización DC de componentes individuales. |
| **REQ-15** | §7 | Tarea 2 | Dependencia térmica de fugas en 45nm HP a $85^\circ\text{C}$. Cuantificación del factor de incremento de fugas vs modelo analítico subumbral ($I_{sub} \propto T^2 \exp[-V_{th}/(n U_T)]$), parámetros térmicos BSIM4 (`kt1`, `kt2`) y aproximación orientativa ($V_{th} \approx V_{th0} - 1\,\text{mV}/^\circ\text{C}$). | $I_{leak}(85^\circ\text{C}) / I_{leak}(27^\circ\text{C})$, $\Delta V_{th}(T)$, identificación del mecanismo dominante. | Razón simulada vs teórica; análisis de sensibilidad térmica. |
| **REQ-16** | §7 | Tarea 3 | Comparativa tecnológica multidécada: 45nm LP ($V_{DD}=1.1\,\text{V}$) y 130nm bulk ($V_{DD}=1.3\,\text{V}$). Tabla comparativa de fugas, retención y $W_{kp,\text{min}}$ para $V_{dyn}(1\,\mu\text{s}) > 0.90 V_{DD}$ (estrictamente mayor). | Proceso, Temp, $I_{leak}$, $t_{hold}$ sin keeper, $W_{kp,\text{min}}$. | Tabla comparativa oficial (5 o 6 filas según resolución de ambigüedad). |
| **REQ-17** | §7 | Tarea 4 | Compromiso de contención en velocidad: con $W_{kp,\text{min}}$ de HP/85°C, medir retardo de evaluación $t_{pHL,dyn}$ vs $W_{kp}$ con entradas conmutando a nivel alto ($A=B=C=1$). | $t_{pHL,dyn}(W_{kp})$, ratio $r = \frac{(W/L)_{kp}}{(W/L)_{PDN,eq}}$, umbral de degradación estricta $< 10.0\%$. | Curva de contención $t_{pHL}$ vs $r$; cota de velocidad admisible. |
| **REQ-18** | §7 | Tarea 5 | Pregunta de diseño e hipótesis de keeper condicional: determinar si existe ventana viable (retención $> 0.90 V_{DD}$ y contención $< 10.0\%$) en HP y LP. Si no existe, diseñar keeper condicional con línea retardada. | Ventana de coexistencia estricta; topología de keeper condicional gobernado por 3 inversores. | Esquema circuital, cronograma de control y validación de apertura de ventana. |

---

## 2. Decisiones Metodológicas Pendientes de Respuesta Docente

Actualmente se encuentran formalmente formuladas dos consultas técnicas a la docente MsC. Luz Adanaqué Infante. Para garantizar imparcialidad, el pipeline se diseña desacoplado de la decisión final:

### PENDIENTE-DOCENTE-01: Evaluación de 130 nm a 85 °C
* **Conflicto:** La tabla de la Sección 7 Tarea 3 contiene explícitamente 5 filas (45 HP a 27°C y 85°C; 45 LP a 27°C y 85°C; y 130nm solo a 27°C). Sin embargo, el texto de la Rúbrica de Evaluación (§12) exige textualmente *"Tabla HP/LP/130nm a dos T"*.
* **Estrategia Desacoplada:**
  1. El pipeline y los netlists se preparan para soportar ambas condiciones (130nm a 27°C y 130nm a 85°C).
  2. No se declara obligatoria la corrida de 130nm a 85°C ni se descarta prematuramente.
  3. No se ejecutará ninguna simulación física hasta recibir la instrucción oficial o definir el protocolo definitivo.

### PENDIENTE-DOCENTE-02: Definición Formal y Calibración de $t_{hold}$
* **Conflicto:** La guía menciona el tiempo de retención $t_{hold}$ en varias secciones sin explicitar unívocamente el umbral de tensión de disparo:
  * Umbral de conmutación estática del inversor: $V(dyn) = V_M(proc, T)$.
  * Umbral de retención segura de nivel alto: $V(dyn) = 0.90 V_{DD}$.
  * Umbral de mitad de excursión: $V(dyn) = 0.50 V_{DD}$.
* **Estrategia Desacoplada y Rigor Numérico:**
  Para evitar re-simulaciones o sesgos interpretativos, el sistema de extracción capturará de forma simultánea e independiente cuatro observables directos:
  1. `Vdyn_end_1us`: Tensión residual exacta en $t = t_{eval\_start} + 1.0\,\mu\text{s}$.
  2. `t_cross_0p9VDD`: Instante temporal absoluto en el que $V(dyn)$ desciende a $0.90 \times V_{DD}$.
  3. `t_cross_VDD2`: Instante temporal absoluto en el que $V(dyn)$ desciende a $0.50 \times V_{DD}$.
  4. `t_cross_VM`: Instante temporal absoluto en el que $V(dyn)$ cruza el umbral de conmutación estática calibrado **específico del proceso y temperatura**: $V_M(proc, T)$.
     * **Nota Crítica:** Queda estrictamente prohibido reutilizar $V_M = 0.4797\,\text{V}$ (obtenido para 45 HP a 27°C) en 85°C, 45 LP o 130nm. Cada tecnología y temperatura contará con su propio $V_M$ calibrado.
  5. `t_hold`: Tiempo transcurrido efectivo desde el inicio de la evaluación, diferenciado del tiempo absoluto de simulación:
     $$t_{hold} = t_{cross} - t_{eval\_start}$$
  * **Tratamiento estricto de eventos no ocurridos (Censura):** Si durante la ventana de retención la tensión no desciende hasta el umbral en cuestión, la métrica se registrará unívocamente como valor censurado temporalmente (`> 1.0 us` / `Censurado` / `null` en JSON), quedando **terminantemente prohibido registrar valores arbitrarios como infinito ($\infty$) o $0$**.

---

## 3. Inspección Analítica de Modelos PTM (ptm45hp, ptm45lp, ptm130)

Una inspección estática del código fuente de las tarjetas de modelo en `LD2_Arcila_Yactayo/modelos/` revela la presencia real y contrastada de los siguientes parámetros físicos:

| Mecanismo Físico | Parámetros BSIM4 Realmente Presentes | Valores Extraídos (NMOS / PMOS) | Observable SPICE Medible | Limitación Metodológica y Rigor |
| :--- | :--- | :--- | :--- | :--- |
| **Corriente Subumbral ($I_{sub}$)** | `vth0`, `voff`, `nfactor`, `eta0`, `dsub` | **45 HP:** $V_{th0} = +0.469 / -0.492\,\text{V}$, $n = 2.22 / 2.10$, $\eta_0 = 0.0055$<br>**45 LP:** $V_{th0} = +0.623 / -0.587\,\text{V}$, $n = 1.60 / 1.80$, $\eta_0 = 0.0125$<br>**130nm:** $V_{th0} = +0.378 / -0.321\,\text{V}$, $n = 1.50 / 1.50$, $\eta_0 = 0.0092$ | Corriente de drenaje en reposo $I_D(V_{GS}=0, V_{DS}=V_{DD})$. Medible in situ mediante `Ix(M1:D)` o sweep DC auxiliar. | La presencia de DIBL ($\eta_0$) hace que la corriente subumbral dependa de $V_{DS}$, variando conforme $dyn$ se descarga. En un stack, $V_{SB} > 0$ eleva el umbral efectivo. |
| **Fuga de Túnel de Compuerta ($I_{gate}$)** | `toxe`, `aigc`, `bigc`, `cigc`, `nigbinv`, `eigbinv` | **45 HP:** $t_{oxe} = 1.25 / 1.30\,\text{nm}$, $a_{igc} = 0.020 / 0.011$<br>**45 LP:** $t_{oxe} = 1.80 / 1.82\,\text{nm}$, $a_{igc} = 0.015 / 0.010$<br>**130nm:** $t_{oxe} = 2.25 / 2.35\,\text{nm}$, $a_{igc} = 0.012 / 0.690$ | Corrientes de compuerta $I_G = I_{gc} + I_{gs} + I_{gd}$. Medibles in situ mediante `Ix(M:G)`. | En transitorios con compuertas conectadas a nodos dinámicos, la corriente de compuerta drena carga directamente del nodo `dyn`. |
| **Fuga por Drenaje Inducido por Compuerta (GIDL)** | `agidl`, `bgidl`, `cgidl` | **Común a los 3 nodos:**<br>$a_{gidl} = 2.0 \times 10^{-4}\,\text{mho}$<br>$b_{gidl} = 2.1 \times 10^{9}\,\text{V/m}$<br>$c_{gidl} = 2.0 \times 10^{-4}\,\text{V}^3$ | Incremento de corriente de drenaje a altos campos reversos compuerta-drenaje ($V_{GD} < 0$). | GIDL se manifiesta a tensiones de drenaje elevadas ($V_{DG} \approx V_{DD}$); al caer $V(dyn)$, la componente se apaga exponencialmente. |
| **Sensibilidad Térmica ($V_{th}(T), \mu(T)$)** | `kt1`, `kt2`, `kt1l`, `ute`, `tnom` | **Común a los 3 nodos:**<br>$k_{t1} = -0.11\,\text{V}$, $k_{t2} = 0.022\,\text{V}$, $k_{t1l} = 0$, $ute = -1.5$, $T_{nom} = 27^\circ\text{C}$ | Desplazamiento de umbral $\Delta V_{th}(T)$ y degradación de movilidad $\mu(T)$. | **Distinción analítica fundamental:** Véase subsección siguiente para separación entre parámetros reales, ecuación BSIM4, aproximación orientativa y simulación. |
| **Fuga de Unión Reversa ($I_{junc}$)** | `cjs`, `cjd`, `cjsws`, `cjswgs`, `pb`, `mj` | $c_j = 0.5\,\text{fF}/\mu\text{m}^2$, $c_{jsw} = 0.5\,\text{fF}/\mu\text{m}$, $c_{jswg} = 0.3\,\text{fF}/\mu\text{m}$, $PB = 1.0\,\text{V}$ | Corriente reversa de diodo difusor drenaje-sustrato. | Órdenes de magnitud menor que la fuga subumbral en tecnologías nanométricas. |

### Rigor en la Dependencia Térmica de $V_{th}$: Separación de Niveles
Queda terminantemente prohibido asumir automáticamente $dV_{th}/dT = -1\,\text{mV}/^\circ\text{C}$ como si fuera un valor medido del modelo. Se establecen cuatro niveles epistemológicos:
1. **Parámetros presentes en las tarjetas de modelo:**  
   `kt1 = -0.11`, `kt2 = 0.022`, `kt1l = 0`, `ute = -1.5`, `tnom = 27`.
2. **Ecuación analítica de BSIM4 y sus hipótesis:**  
   $$V_{th}(T) = V_{th}(T_{nom}) + \left( k_{t1} + \frac{k_{t1l}}{L_{eff}} + k_{t2} \cdot V_{bseff} \right) \left( \frac{T}{T_{nom}} - 1 \right)$$
   Para $V_{BS} = 0$ y $k_{t1l} = 0$, la pendiente analítica teórica es:
   $$\frac{\Delta V_{th}}{\Delta T} = \frac{k_{t1}}{T_{nom}} = \frac{-0.11\,\text{V}}{300.15\,\text{K}} \approx -0.366\,\text{mV}/^\circ\text{C}$$
   lo que para $\Delta T = 58^\circ\text{C}$ ($85^\circ\text{C} - 27^\circ\text{C}$) predice un corrimiento intrínseco de $\Delta V_{th} \approx -21.2\,\text{mV}$.
3. **Aproximación orientativa de la literatura docente:**  
   La guía cita como orden de magnitud clásico $V_{th}(T) \approx V_{th0} - 1\,\text{mV}/^\circ\text{C} \cdot (T - 27)$. Esta es una heurística pedagógica de referencia para contrastar, no el comportamiento exacto de BSIM4.
4. **Magnitudes a determinar en simulación:**  
   El corrimiento efectivo real de $V_{th}$, la variación del factor de idealidad subumbral $n(T)$, y el incremento resultante de fuga $I_{leak}(85^\circ\text{C})/I_{leak}(27^\circ\text{C})$ se obtendrán exclusivamente tras las simulaciones posteriores en LTspice.

---

## 4. Formalización y Aislamiento de Corrientes de Fuga

### Distinción Fundamental de Corrientes en el Circuito
Para evitar confusiones entre balances de carga y mecanismos físicos de fuga:

1. **Corriente de Alimentación ($I_{\text{supply}}$):**
   $$I_{\text{supply}} = -I(V_{DD})$$
   Mide la potencia global extraída de la fuente $V_{DD}$. Alimenta conjuntamente:
   * La compuerta dinámica (a través de $M_p$ y $M_k$);
   * El inversor dominó de salida ($M_{pi}, M_{ni}$);
   * Corrientes túnel de compuerta en terminales conectados a $V_{DD}$.
   * **Regla innegociable:** $I_{\text{supply}} \neq I_{\text{leak,tot}}$.

2. **Corriente Neta del Nodo Dinámico ($I_{net}(dyn)$):**
   $$I_{net}(dyn)(t) = - C_{dyn}(V_{dyn}) \cdot \frac{dV(dyn)}{dt}$$
   Representa el balance neto capacitivo que descarga o carga el nodo:
   $$I_{net}(dyn) = I_{\text{descarga}} - I_{\text{reposición}}$$
   donde $I_{\text{reposición}} = I_D(M_k)$ es la corriente provista por el keeper, e $I_{\text{descarga}}$ es la suma de fugas que extraen carga del nodo.

3. **Corriente Suministrada por el Keeper ($I_{kp}$):**
   $$I_{kp} = I_D(M_k)$$
   Cuando $V(dyn) \approx V_{DD}$ y la salida `out` $\approx 0\,\text{V}$, el PMOS keeper opera en región de triodo ($V_{GS} = -V_{DD}$, $V_{DS} \approx 0\,\text{V}$) reponiendo carga activamente. Cuando hay keeper activo, la corriente neta $-C_{dyn} \frac{dV}{dt}$ **no puede identificarse como la corriente física de fuga**, sino como la diferencia entre la fuga y la reposición:
   $$I_{net}(dyn) = I_{leak,tot} - I_{kp}$$
   Si el keeper compensa perfectamente, $\frac{dV}{dt} \approx 0 \implies I_{net} \approx 0$, aunque las fugas físicas sigan existiendo.

4. **Hipótesis Explícitas para la Aproximación $-C_{nodo} \frac{dV}{dt}$:**
   La aproximación $I_{\text{leak,tot}} \approx -C_{nodo} \left.\frac{dV}{dt}\right|_{t=t_0^+}$ **solo es válida** bajo las siguientes condiciones estrictas:
   * **$W_{kp} \to 0$ (o $W_{kp} = 1\,\text{nm}$ / keeper ausente):** Se anula la corriente de reposición ($I_{kp} \to 0$).
   * **Instante $t = t_0^+$:** Medición efectuada tras la extinción del transitorio de conmutación de reloj y feedthrough capacitivo ($t \approx 10\,\text{ns}$), pero antes de que la caída de $V(dyn)$ reduzca significativamente $V_{DS}$ y el DIBL.
   * **Capacitancia concentrada efectiva ($C_{dyn}$):** Requiere modelar la capacitancia nodal no lineal $C_{dyn}(V) = C_L + C_{par,dyn}(V)$ (incluyendo difusiones `AS`, `AD`, `PS`, `PD` y capacidades de compuerta).
   * **Sin inyección de carga:** La pendiente no debe estar contaminada por acoplamientos parásitos residuales.

5. **Corrientes de Dispositivos Individuales y Aislamiento de Mecanismos:**
   * **Medición Directa In Situ:** LTspice permite registrar las corrientes de terminal de cada dispositivo en el transitorio de retención completo:
     * `Ix(M1:D)`: Corriente total que drena hacia la PDN;
   ### Distinción Rigurosa: Celda Sin Keeper vs Keeper de 1 nm ($W_{kp} = 1\,\text{nm}$)
   * **Sin Keeper (Instancia `Mk` Ausente):** El nodo dinámico `dyn` no tiene conectado ningún terminal de keeper. No existe capacitancia parásita de compuerta ($C_{gd}, C_{db}$) asociada a $M_k$, ni fuga inversa de unión drenaje-sustrato de dicho transistor. Esta es la condición física genuina de "ausencia de keeper".
   * **Keeper con $W_{kp} = 1\,\text{nm}$ (Aproximación Numérica):** Se incluye la instancia `Mk` con un ancho geométrico de $1\,\text{nm}$.
     * **Advertencia Metodológica Crítica:** $W = 1\,\text{nm}$ está severamente por debajo del límite de fabricación y de la regla de diseño de la tecnología de 45 nm ($W_{min} \approx 45\text{--}90\,\text{nm}$). A $1\,\text{nm}$, las ecuaciones de BSIM4 operan en régimen de **extrapolación matemática no validada físicamente** por el consorcio PTM. Además, persisten parásitos de difusión y corrientes residuales de borde.
     * **Regla Operativa:** Queda terminantemente prohibido declarar ambas condiciones como físicamente idénticas. En los ensayos piloto y definitivos se evaluará la condición pura "Sin Keeper" eliminando la instancia `Mk`.

   ### Convención de Signo de la Corriente del Keeper ($I_{kp}$)
   * Conforme a la convención estándar SPICE, las corrientes de terminal de un dispositivo se definen positivas cuando ingresan al terminal correspondiente ($I_{\text{terminal}} > 0$).
   * Para el transistor keeper $M_k$ (PMOS con fuente a $V_{DD}$ y drenaje a $dyn$):
     * La corriente que fluye desde $V_{DD}$ por el canal y sale por el drenaje hacia el nodo $dyn$ (corriente restauradora inyectada) sale del terminal de drenaje de $M_k$.
     * Si la sonda de LTspice mide corriente entrando al drenaje, la corriente inyectada hacia $dyn$ corresponderá al valor negativo:
       $$I_{kp,\text{inyectada}} = - I_D(M_k)$$
     * Si la sonda mide en sentido saliente, se preservará el signo positivo.
     * **Directiva:** El signo algebraico de $I_{kp,\text{inyectada}}$ se fijará empíricamente a partir de la simulación piloto de validación en LTspice, documentando unívocamente la convención adoptada.
   * **No mezclar balance neto con descomposición física:** Un balance neto de carga $\Delta Q / \Delta t$ no sustituye la descomposición física en $I_{sub}$, $I_{gate}$, $I_{gidl}$ e $I_{junc}$.

---

## 5. Estrategia de Dimensionamiento del Keeper ($W_{kp}$)

### Requisito Docente vs Decisión de Ingeniería
* **Requisito Docente (§7 Tarea 3 y Tarea 5):** Identificar el valor mínimo de ancho $W_{kp,\text{min}}$ que garantice una retención estrictamente superior al $90\%$ de $V_{DD}$ tras $1.0\,\mu\text{s}$ de evaluación detenida:
  $$V_{dyn}(1\,\mu\text{s}) > 0.90 \times V_{DD}$$
* **Decisión de Ingeniería (Estrategia en Dos Fases):**
  1. **Fase 1 (Barrido Grueso Geométrico):** Evaluar un conjunto representativo acotado que cubra órdenes de magnitud:
     $$W_{kp} \in [1\text{ nm}, 15\text{ nm}, 30\text{ nm}, 45\text{ nm}, 60\text{ nm}, 90\text{ nm}, 135\text{ nm}, 180\text{ nm}]$$
     *Nota:* Incluye $W_{kp} = 45\text{ nm}$ para preservar trazabilidad cruzada y comparación directa con la Actividad 2.
  2. **Fase 2 (Refinamiento Local por Bisección):** Identificado el intervalo $[W_a, W_b]$ donde $V_{dyn}(1\,\mu\text{s})$ cruza el umbral de $0.90\,V_{DD}$, ejecutar un barrido focalizado con resolución de $\le 2\text{ nm}$ para determinar $W_{kp,\text{min}}$ con rigor numérico.

---

## 6. Evaluación del Compromiso de Contención en Velocidad

Conforme a §7 Tarea 4, la adición del keeper penaliza la descarga intencional del nodo dinámico cuando las entradas conmutan a evaluación legítima ($A=B=C=1$):
* **Condición de Control Riguroso:** Mismo proceso (45nm HP), misma temperatura ($85^\circ\text{C}$), misma tensión ($V_{DD}=1.0\,\text{V}$), misma carga ($C_L=2.0\,\text{fF}$) y mismos estímulos que en la Actividad 1.
* **Métrica de Penalización Relativa:**
  $$\text{Penalización } (\%) = \frac{t_{pHL}(W_{kp}) - t_{pHL,\text{base}}}{t_{pHL,\text{base}}} \times 100\%$$
* **Definición Literal de $r$ en la Guía Oficial (§7 Tarea 4):**
  La guía establece textualmente:
  $$r = \frac{(W/L)_{kp}}{(W/L)_{PDN,eq}} \quad \text{con} \quad (W/L)_{PDN,eq} = \frac{(W/L)_n}{4}$$
  Para analizar esta relación se distinguen tres interpretaciones:
  a) **Razón geométrica de anchuras:** Razón entre el ancho del keeper $W_{kp}$ y el ancho de un NMOS individual de la PDN ($W_{NMOS} = 3W_n = 270\text{ nm}$): $W_{kp} / 270\text{ nm}$.
  b) **Razón equivalente aproximada mediante resistencias en serie (primer orden):**  
     Cuatro transistores idénticos de $270\,\text{nm}$ en serie presentan una resistencia equivalente $R_{eq} \approx 4 \times R(270\text{ nm})$, lo que equivale a un único transistor de ancho:
     $$W_{PDN,eq} = \frac{3 W_n}{4} = \frac{270\text{ nm}}{4} = 67.5\text{ nm}$$
     Bajo esta aproximación, la razón de dimensionamiento normalizada es:
     $$r = \frac{W_{kp}}{67.5\text{ nm}} = \frac{4 \cdot W_{kp}}{3 \cdot W_n}$$
  c) **Razón efectiva de fuerza eléctrica (BSIM4 submicrométrico):**  
     En nanómetros, esta equivalencia lineal no es exacta debido a:
     * Efecto de cuerpo ($V_{SB} > 0$) en los tres NMOS superiores de la pila, que eleva su $V_{th}$ efectivo;
     * Saturación de velocidad y degradación de movilidad por campo vertical;
     * Diferencia intrínseca de movilidad y corriente de saturación entre NMOS y PMOS ($\mu_n \approx 2\text{--}3 \times \mu_p$).
  * **Definición adoptada para la gráfica de contención:**  
    En estricto apego a la directiva docente de la guía, se empleará la definición (b):
    $$r = \frac{W_{kp}}{67.5\text{ nm}}$$
    explicitando en el texto del informe que se trata de una normalización geométrica de primer orden y detallando las desviaciones introducidas por los efectos de segundo orden en BSIM4.
* **Criterio de Aceptación Estricto:**  
  La guía exige explícitamente una degradación **inferior al 10%**:
  $$\text{Penalización } (\%) < 10.0\%$$
  * **Tratamiento de la Frontera:** Un valor de $\Delta t_{pHL} = 10.0\%$ se considera en el límite; para garantizar el cumplimiento de la condición estricta $< 10\%$, el punto operacional admisible debe verificar $\Delta t_{pHL} < 10.00\%$.

---

## 7. Hipótesis Arquitectural: Keeper Condicional

* **Condición Lógica de Activación:**
  Si para una tecnología y temperatura dadas (ej. 45nm HP a $85^\circ\text{C}$), el ancho mínimo requerido para retención segura no coexiste con el límite de contención admisible:
  $$\{ W_{kp} \mid V_{dyn}(1\,\mu\text{s}) > 0.90\,V_{DD} \} \cap \{ W_{kp} \mid \text{Penalización } < 10.0\% \} = \emptyset$$
  entonces **no existe solución estática convencional**.
* **Propuesta Arquitectural de la Guía (§7 Tarea 5):**
  Implementar un **keeper condicional** gobernado por la señal de reloj retardada mediante una cadena de 3 inversores estáticos:
  * Durante el flanco inicial de evaluación, el keeper se mantiene forzosamente apagado, permitiendo a la PDN descargar $dyn$ sin contención alguna.
  * Si tras el retardo de los 3 inversores el nodo no descargó (PDN abierta), el keeper se habilita para compensar las fugas subumbral y retener la carga.

### Planificación Documental: Evaluación de Contención y Keeper Condicional en 45nm LP (Tarea 5)
Conforme al mandato de desacoplamiento y rigor documental previo a la simulación física de LP:
1. **Contexto Físico de 45nm LP frente a HP:**
   * En 45nm LP ($V_{DD} = 1.1\,\text{V}$), las simulaciones de A3.3 demostraron que la compuerta dinámica retiene $V_{dyn}(1\,\mu\text{s}) = 1.1275\,\text{V}$ a $27^\circ\text{C}$ y $1.1257\,\text{V}$ a $85^\circ\text{C}$ **sin necesidad de keeper** ($W_{kp,\text{min}} = 0$).
   * Esto se debe al elevado umbral intrínseco de los transistores LP ($V_{th0,n} = 0.623\,\text{V}$, $V_{th0,p} = -0.587\,\text{V}$) y al mayor espesor de óxido ($t_{oxe} = 1.80\,\text{nm}$), lo que reduce la fuga subumbral de la PDN a apenas $3.40\,\text{pA}$ a $85^\circ\text{C}$ (frente a $430.9\,\text{pA}$ en HP, una reducción de $126\times$).
   * Por consiguiente, en 45nm LP la condición de retención se cumple trivialmente para cualquier $W_{kp} \ge 0$.
2. **Hipótesis y Protocolo de Medición para Contención en LP:**
   * La menor corriente de saturación de la PDN en LP ($I_{on}$ reducida por mayor $V_{th}$ y menor campo) implica que la velocidad intrínseca de descarga será sustancialmente más lenta que en HP.
   * La presencia de un transistor keeper en LP competirá con una PDN de menor fuerza relativa, lo que podría inducir una penalización porcentual apreciable para anchos moderados de keeper.
   * Cuando se autorice la ejecución de la Tarea 5 en LP, se evaluará:
     * Base: $t_{pHL,dyn,\text{sin}}$ con $V_{DD} = 1.1\,\text{V}$, $T = 85^\circ\text{C}$, $A=B=C=1$;
     * Barrido: $W_{kp} \in [10.5, 15, 30, 45, 60, 90, 135, 180]\,\text{nm}$;
     * Penalización porcentual frente al umbral estricto $< 10.0\%$;
     * Delimitación de la ventana admisible en LP.
3. **Criterio de Necesidad del Keeper Condicional:**
   * En **45nm HP a 85°C**, aunque matemáticamente existe una ventana viable con keeper convencional estático para $W_{kp} \in [15, 38]\,\text{nm}$ ($r \in [0.222, 0.563]$), cualquier diseño que emplee transistores con anchos comerciales estándar ($W \ge 45\text{--}90\,\text{nm}$) incurre en contención inadmisible ($\Delta t_{pHL} = 12.9\%\text{ a }42.8\%$).
   * El **keeper condicional** resuelve este compromiso al desacoplar temporalmente la evaluación (keeper apagado, contención $0\%$) de la retención a largo plazo (keeper encendido tras el retardo de 3 inversores, compensando fugas de forma ilimitada).

---

## 8. Presupuesto y Proyección Editorial en LaTeX

* **Estado Actual del Informe Maestro:** 11 páginas totales (1 portada + 10 páginas numeradas).
* **Límite Docente Rúbrica LD2:** Máximo 20 páginas totales.
* **Presupuesto Asignado a Actividad 3:** **2.5 a 3.0 páginas**.
* **Estructura Planificada:**
  1. **Tabla Principal (Tabla 4):** Comparativa multi-tecnológica ($45\text{ HP, } 45\text{ LP, } 130\text{ nm}$) y térmica ($27^\circ\text{C}, 85^\circ\text{C}$) reportando $I_{leak}$, retención $V_{dyn}(1\,\mu\text{s})$, $t_{hold}$ y $W_{kp,\text{min}}$.
  2. **Figura Multipanel 1 (Figura 7):** Formas de onda transitorias de retención a reloj detenido ($1\,\mu\text{s}$) contrastando procesos y temperaturas sin keeper y con keeper.
  3. **Figura Multipanel 2 (Figura 8):** Curvas de contención $t_{pHL}$ vs $W_{kp}$ y frente al ratio $r$, delimitando la ventana de compromiso y el umbral del $+10\%$.
* **Articulación con Cuestionario Teórico:**
  Las preguntas docentes **P8** (dependencia térmica de fugas), **P9** (compromiso retención vs contención) y **P10** (keeper condicional) se responderán analíticamente dentro del cuerpo argumentativo de la sección para optimizar espacio.

---

**Fin del Plan Experimental de la Actividad 3.**
