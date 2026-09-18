# Predicción Analítica Previa de Compartición de Carga (Charge Sharing) — Actividad 2
**Documento de Predicción Pre-Simulación (Fase 4 - LD2)**  
**Fecha y Hora de Registro:** 2026-09-17T01:25:00-05:00  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Curso:** Microelectrónica y Sistemas Nanoelectrónicos — FIEE UNMSM (2026-II)  
**Docente:** MsC. Luz Adanaqué Infante  
**Estado:** REGISTRO FORMAL CONGELADO PRE-SIMULACIÓN (Cumplimiento de Rúbrica de Predicción Previa)

---

## 1. Topología del Circuito y Dimensionamiento

Se analiza la compuerta **NAND3 CMOS dinámica footed con inversor dominó de salida**, construida sobre el nodo predictivo **PTM 45 nm HP** ($V_{DD} = 1.0\text{ V}$, $T = 27\ ^\circ\text{C}$).

### Dimensiones Geométricas
* **Longitud de canal de referencia:** $L = 45\text{ nm}$ para todos los dispositivos.
* **Transistor de precarga PMOS ($M_p$):** $W_p = 135\text{ nm}$ ($1.5 \times W_n$).
* **Red de Descenso NMOS (PDN) y Footer:**
  * Dispositivos: $M_1$ (entrada $A$), $M_2$ (entrada $B$), $M_3$ (entrada $C$) y $M_f$ (reloj $CLK$).
  * Ancho equivalente para igualar resistencia a NMOS mínimo: $W_{PDN} = 3 \times W_n = 3 \times 90\text{ nm} = 270\text{ nm}$.
* **Inversor Dominó Estático de Salida:**
  * PMOS ($M_{pi}$): $W_{pi} = W_p = 135\text{ nm}$, $L = 45\text{ nm}$.
  * NMOS ($M_{ni}$): $W_{ni} = W_n = 90\text{ nm}$, $L = 45\text{ nm}$.
  * Carga de salida: $C_{out} = 1.0\text{ fF}$.
* **Carga externa en nodo dinámico:** $C_L = 2.0\text{ fF}$ (nominal); se realiza barrido en $C_L \in [0.5, 1.0, 2.0, 4.0]\text{ fF}$.

### Conectividad Nodal
* $V_{DD}$ alimenta la fuente de $M_p$ y $M_{pi}$.
* **Nodo Dinámico (`dyn`):** Conecta el drenaje de $M_p$, el terminal superior de $M_1$, la entrada del inversor estático y la capacitancia de carga $C_L$.
* **Nodo Interno $n_1$:** Conecta el terminal inferior de $M_1$ con el terminal superior de $M_2$.
* **Nodo Interno $n_2$:** Conecta el terminal inferior de $M_2$ con el terminal superior de $M_3$.
* **Nodo Interno $n_3$:** Conecta el terminal inferior de $M_3$ con el drenaje del footer $M_f$.
* **Tierra ($0\text{ V}$):** Fuente de $M_f$ y fuente de $M_{ni}$.

---

## 2. Definición del Escenario de Peor Caso de Charge Sharing

El fenómeno de redistribución de carga destructivo ocurre bajo la siguiente secuencia en dos ciclos de reloj:

### Ciclo 1 ($t \in [0, T_{clk}]$, con $T_{clk} = 2\text{ ns}$): Descarga Completa
* En la fase de evaluación ($CLK = 1$, $t \in [1\text{ ns}, 2\text{ ns}]$), las entradas se configuran en $A = 1$, $B = 1$, $C = 1$.
* La rama completa conduce hacia tierra, descargando totalmente el nodo dinámico `dyn` y todos los nodos intermedios:
  $$V(dyn) \rightarrow 0\text{ V}, \quad V(n_1) \rightarrow 0\text{ V}, \quad V(n_2) \rightarrow 0\text{ V}, \quad V(n_3) \rightarrow 0\text{ V}$$

### Ciclo 2 ($t \in [T_{clk}, 2 T_{clk}]$): Precarga y Evaluación con PDN Abierta a Tierra
1. **Fase de Precarga ($t \in [2.0\text{ ns}, 3.0\text{ ns}]$):**
   * $CLK = 0$: $M_p$ conduce fuertemente, recargando `dyn` a $V_{DD} = 1.0\text{ V}$.
   * El footer $M_f$ permanece en corte ($CLK = 0$).
   * Los nodos internos $n_1, n_2, n_3$ permanecen descargados a $0\text{ V}$ (o tensión residual prácticamente nula, pues no existe camino a $V_{DD}$).
2. **Fase de Evaluación ($t \in [3.0\text{ ns}, 4.0\text{ ns}]$, es decir $t > 1.5 T_{clk}$):**
   * $CLK \rightarrow 1$: $M_p$ se apaga; el nodo `dyn` queda **flotante** en $V_{DD}$.
   * Estímulos de entrada:
     $$A = 1, \quad B = 1, \quad C = 0$$
   * Condición de los transistores:
     * $M_1$ conduce ($V_A = 1.0\text{ V}$).
     * $M_2$ conduce ($V_B = 1.0\text{ V}$).
     * $M_3$ en corte ($V_C = 0.0\text{ V}$).
     * Footer $M_f$ conduce ($CLK = 1$).
   * **Mecanismo:** Dado que $M_3$ está en corte, no existe camino conductivo a tierra ($n_3$ y tierra quedan aislados). La función booleana correcta es $\text{NAND3}(1, 1, 0) = 1$, por lo que la salida dominó ideal debe ser `out = 0`.
   * **Problema:** Los canales de $M_1$ y $M_2$ conectan inmediatamente el nodo dinámico cargado (`dyn`) con los nodos internos descargados $n_1$ y $n_2$. La carga acumulada en `dyn` se redistribuye hacia las capacitancias parásitas de difusión de $n_1$ y $n_2$, provocando una caída instantánea de potencial $\Delta V$.

---

## 3. Parámetros Tecnológicos y Deducción de Capacitancias de Difusión

De acuerdo con la Sección 6.2 y 6.3 de la Guía Oficial de Laboratorio N.° 2, las geometrías de difusión deben modelarse explícitamente con:
$$L_{diff} = 90\text{ nm}$$

Para los transistores de la PDN ($W = 3 W_n = 270\text{ nm}$):
* **Área de difusión ($Ad$):**
  $$Ad = W \times L_{diff} = 270\text{ nm} \times 90\text{ nm} = 0.0243\ \mu\text{m}^2 = 2.430 \times 10^{-14}\text{ m}^2$$
* **Perímetro de difusión exterior ($Pd$):**
  $$Pd = W + 2 L_{diff} = 270\text{ nm} + 2(90\text{ nm}) = 450\text{ nm} = 0.450\ \mu\text{m} = 4.500 \times 10^{-7}\text{ m}$$

### Parámetros Extraídos de la Tarjeta PTM 45nm HP (`ptm45hp.lib`)
* Capacitancia de unión de fondo a cero sesgo:
  $$c_j = c_{js} = c_{jd} = 0.0005\text{ F/m}^2 = 0.500\text{ fF}/\mu\text{m}^2$$
  $$PB = 1.0\text{ V}, \quad MJ = 0.50$$
* Capacitancia de sidewall perimetral a cero sesgo:
  $$c_{jsw} = c_{jsws} = c_{jswd} = 5.00 \times 10^{-10}\text{ F/m} = 0.500\text{ fF}/\mu\text{m}$$
  $$PBSW = 1.0\text{ V}, \quad MJSW = 0.33$$

### Cálculo de la Capacitancia por Región de Difusión ($C_{diff,1}$)
$$C_{bottom} = c_j \times Ad = (5.0 \times 10^{-4}\text{ F/m}^2) \times (2.43 \times 10^{-14}\text{ m}^2) = 1.215 \times 10^{-17}\text{ F} = 0.01215\text{ fF}$$
$$C_{sidewall} = c_{jsw} \times Pd = (5.0 \times 10^{-10}\text{ F/m}) \times (4.50 \times 10^{-7}\text{ m}) = 2.250 \times 10^{-16}\text{ F} = 0.22500\text{ fF}$$
$$C_{diff,1} = C_{bottom} + C_{sidewall} = 0.01215\text{ fF} + 0.22500\text{ fF} = 0.23715\text{ fF}$$

> **Observación Física Clave:** En tecnología de 45 nm, la capacitancia de borde (*sidewall*) representa el **$94.9\%$** de la capacitancia de unión total de difusión ($0.225\text{ fF}$ vs $0.012\text{ fF}$). El efecto tridimensional de borde domina sobre el área plana.

### Capacitancia Total de los Nodos Internos Descargados ($C_a$)
En la netlist oficial (`M1 n1 a dyn 0`, `M2 n2 b n1 0`, `M3 n3 c n2 0` con `AS=Ad AD=Ad PS=Pd PD=Pd`):
* **Nodo $n_1$:** Conecta una difusión de $M_1$ y una difusión de $M_2$:
  $$C_{n1} = 2 \times C_{diff,1} = 2 \times 0.23715\text{ fF} = 0.4743\text{ fF}$$
* **Nodo $n_2$:** Conecta una difusión de $M_2$ y una difusión de $M_3$:
  $$C_{n2} = 2 \times C_{diff,1} = 2 \times 0.23715\text{ fF} = 0.4743\text{ fF}$$
* **Capacitancia agregada interna ($C_a$):**
  $$C_a \equiv C_{n1} + C_{n2} = 0.4743\text{ fF} + 0.4743\text{ fF} = 0.9486\text{ fF} \approx 0.95\text{ fF}$$

### Capacitancia Parásita Conectada al Nodo Dinámico ($C_{dyn}$)
Además de la carga externa $C_L$, el nodo `dyn` contiene:
1. **Difusión de $M_1$ conectada a `dyn`:**
   $$C_{diff,M1} = C_{diff,1} = 0.2372\text{ fF}$$
2. **Capacitancia de solapamiento compuerta-drenaje de $M_p$:**
   $$C_{gd}(M_p) = cgdo \times W_p = (1.10 \times 10^{-10}\text{ F/m}) \times (135 \times 10^{-9}\text{ m}) = 0.01485\text{ fF} \approx 0.015\text{ fF}$$
3. **Capacitancia de entrada del inversor dominó ($C_{in,inv}$):**
   * Parámetros PTM: $t_{oxe} = 1.25\text{ nm} \implies C_{ox} = \frac{\varepsilon_0 \varepsilon_{SiO2}}{t_{oxe}} = \frac{8.854 \times 10^{-12} \times 3.9}{1.25 \times 10^{-9}} = 27.62\text{ fF}/\mu\text{m}^2$.
   * $C_{gate,pi} = W_{pi} \times L \times C_{ox} = 135\text{ nm} \times 45\text{ nm} \times 27.62\text{ fF}/\mu\text{m}^2 = 0.1678\text{ fF}$.
   * $C_{gate,ni} = W_{ni} \times L \times C_{ox} = 90\text{ nm} \times 45\text{ nm} \times 27.62\text{ fF}/\mu\text{m}^2 = 0.1119\text{ fF}$.
   * Solapamientos: $2 \times cgdo \times (W_{pi} + W_{ni}) = 2(1.1 \times 10^{-10})(225\text{ nm}) = 0.0495\text{ fF}$.
   * $C_g(\text{inversor}) \approx 0.1678 + 0.1119 + 0.0495 = 0.3292\text{ fF} \approx 0.33\text{ fF}$.

---

## 4. Ecuaciones y Deducción del Reparto de Carga

Por el principio de conservación de carga electrostática entre el instante inmediatamente previo a la conmutación ($t = 1.5 T_{clk}^-$) y el equilibrio final de reparto:

### Carga Inicial Almacenada
$$Q_{inicial} = C_{dyn} \cdot V_{DD} + C_{n1} \cdot 0 + C_{n2} \cdot 0 = C_{dyn} V_{DD}$$

### Caso A: Reparto de Carga Puro sin Restricción de Umbral (Formulación Guía Oficial)
Si ambos transistores $M_1$ y $M_2$ actuaran como interruptores ideales bilaterales sin límite de tensión:
$$Q_{final} = (C_{dyn} + C_a) \cdot V_{dyn,final} = Q_{inicial} = C_{dyn} V_{DD}$$
$$V_{dyn,final} = V_{DD} \cdot \frac{C_{dyn}}{C_{dyn} + C_a}$$
$$\Delta V_{pred} = V_{DD} - V_{dyn,final} = V_{DD} \cdot \frac{C_a}{C_{dyn} + C_a}$$

### Caso B: Limitación Física por Corte Subumbral del NMOS Pasante
En un transistor NMOS pasante cuyo terminal de compuerta está a $V_{DD} = 1.0\text{ V}$, la tensión del terminal de fuente (en este caso el nodo interno $n_2$) solo puede subir hasta:
$$V_{n2,max} \approx V_B - V_{th,M2}(V_{n2}) = V_{DD} - V_{th,M2}$$
Con el efecto de cuerpo ($V_{SB} = V_{n2} > 0$), el voltaje de umbral efectivo se eleva conforme a la formulación de primer orden:
$$V_{th}(V_{n2}) = V_{th0} + k_1 \left( \sqrt{2\phi_F + V_{n2}} - \sqrt{2\phi_F} \right)$$
Empleando el parámetro BSIM4 $k_1 = 0.4\text{ V}^{1/2}$ (con $k_2 = 0$ en `ptm45hp.lib`), un potencial de superficie $2\phi_F \approx 0.8\text{ V}$ y $V_{SB} \approx 0.5\text{ V} - 0.66\text{ V}$:
$$\Delta V_{th} \approx 0.4 \left(\sqrt{0.8 + 0.5} - \sqrt{0.8}\right) \approx 0.4(1.140 - 0.894) \approx 0.098\text{ V} \approx 0.10\text{ V}$$
$$V_{th,eff} \approx V_{th0} + \Delta V_{th} \approx 0.469\text{ V} + 0.10\text{ V} \approx 0.57\text{ V} \quad (\text{rango orientativo } \approx 0.55\text{ V} - 0.60\text{ V})$$
*Nota metodológica:* Se declara explícitamente que este rango corresponde a una **estimación analítica aproximada** de referencia y no a una extracción directa del simulador, dado que el modelo físico completo BSIM4 incorpora dependencias bidimensionales adicionales (DIBL mediante `eta0`, efectos de canal estrecho y modulación por $V_{DS}$).

Cuando $V(n_2)$ se aproxima a $\approx 0.50\text{ V} - 0.66\text{ V}$, la tensión $V_{GS2} = V_{DD} - V(n_2)$ cae por debajo de $V_{th,eff}$, provocando que el transistor $M_2$ entre en régimen subumbral ($V_{GS2} \le V_{th}$), reduciendo la corriente de carga a valores insignificantes en la ventana de evaluación ($t < 1\text{ ns}$).
Por ende, la carga cedida al nodo $n_2$ está acotada por:
$$\Delta Q_{n2} \le C_{n2} \cdot (V_{DD} - V_{th2})$$
**Predicción cualitativa:** La fórmula analítica de reparto puro ($\Delta V_{pred} = V_{DD} \frac{C_a}{C_a + C_{dyn}}$) **sobreestimará** la caída real medida en simulación SPICE transitoria.

---

## 5. Tabla de Predicciones Numéricas ($\Delta V_{pred}$ vs $C_L$)

Se evalúan los tres modelos de capacitancia sobre el nodo dinámico:
1. **Modelo 1 (Nominal puro):** $C_{dyn} = C_L$
2. **Modelo 2 (Guía Oficial Sec. 6.2):** $C_{dyn} = C_L + C_{gd}(M_p) + C_g(\text{inversor}) = C_L + 0.344\text{ fF}$
3. **Modelo 3 (Carga Total Completa):** $C_{dyn} = C_L + C_{diff,M1} + C_{gd}(M_p) + C_g(\text{inversor}) = C_L + 0.581\text{ fF}$

Con $C_a = 0.9486\text{ fF}$ y $V_{DD} = 1.0\text{ V}$:

| $C_L$ (fF) | $\Delta V_{pred}$ (Modelo 1: Nominal) | $\Delta V_{pred}$ (Modelo 2: Guía) | $\Delta V_{pred}$ (Modelo 3: Total) | $V_{dyn,pred}$ (Modelo 2) |
| :---: | :---: | :---: | :---: | :---: |
| **0.5 fF** | **654.8 mV** | **529.2 mV** | **467.3 mV** | **0.4708 V** |
| **1.0 fF** | **486.8 mV** | **413.8 mV** | **375.0 mV** | **0.5862 V** |
| **2.0 fF** | **321.7 mV** | **288.1 mV** | **268.7 mV** | **0.7119 V** |
| **4.0 fF** | **191.7 mV** | **179.2 mV** | **171.5 mV** | **0.8208 V** |

---

## 6. Criterio de Falla Lógica y Comparación con Umbrales del Inversor

A partir de la caracterización rigurosa de calibración del inversor dominó de salida efectuada en la Fase 2 (**ENS-CAL-02**, 45nm HP, $27\ ^\circ\text{C}$, $V_{DD} = 1.0\text{ V}$):
* **Tensión de conmutación estática:** $V_M = 0.4797\text{ V}$
* **Tensión máxima de nivel bajo reconocida:** $V_{IL} = 0.3675\text{ V}$
* **Tensión mínima de nivel alto reconocida:** $V_{IH} = 0.5785\text{ V}$
* **Margen de ruido de nivel alto:**
  $$NM_H = V_{OH} - V_{IH} = 1.0000\text{ V} - 0.5785\text{ V} = 0.4215\text{ V} = 421.5\text{ mV}$$
* **Caída máxima tolerable para no entrar a la región de conmutación estática:**
  $$\Delta V_{crit,M} = V_{DD} - V_M = 1.0000\text{ V} - 0.4797\text{ V} = 0.5203\text{ V} = 520.3\text{ mV}$$

### Evaluación de Fallo Lógico
1. **Caso $C_L = 2.0\text{ fF}$ (Condición Nominal de la Guía):**
   * $\Delta V_{pred} = 288.1\text{ mV} < NM_H\ (421.5\text{ mV}) < \Delta V_{crit,M}\ (520.3\text{ mV})$.
   * $V_{dyn,pred} = 0.7119\text{ V} > V_{IH}\ (0.5785\text{ V})$.
   * **Diagnóstico:** El nodo dinámico se degrada pero permanece netamente en la región de "1" lógico seguro. La salida del inversor dominó se mantiene en un nivel bajo legítimo ($V_{out} \approx 0\text{ V}$). **No existe fallo lógico.**
2. **Caso $C_L = 0.5\text{ fF}$ (Condición de Baja Carga):**
   * $\Delta V_{pred} = 529.2\text{ mV} > NM_H\ (421.5\text{ mV})$ y supera $\Delta V_{crit,M}\ (520.3\text{ mV})$.
   * $V_{dyn,pred} = 0.4708\text{ V} < V_M\ (0.4797\text{ V})$.
   * **Diagnóstico:** Si la redistribución no estuviera frenada por el corte de $M_2$, $V(dyn)$ caería por debajo de $V_M$, provocando que el inversor de salida conmute a nivel alto ($V_{out} \rightarrow 1$), lo cual representa un **fallo lógico espurio severo** (falsa evaluación a "1" cuando la entrada era $C=0$).

---

## 7. Plan de Mitigaciones a Evaluar en Simulación

1. **Mitigación 1 (Precarga Interna):** Incorporar dos PMOS de precarga gobernados por $CLK$ conectados a los nodos internos $n_1$ y $n_2$. Al precargar $n_1$ y $n_2$ a $V_{DD}$ en fase de precarga, la diferencia de potencial inicial es nula ($\Delta V = 0$), eliminando de raíz la fuerza impulsora de la redistribución. El nodo $n_3$ no se precarga para evitar cortocircuito con el footer en el inicio de la evaluación.
2. **Mitigación 2 (Reordenamiento de Entradas en la PDN):** Colocar la entrada crítica que conmuta tarde ($C$) en la posición más próxima al nodo dinámico (`dyn`), ubicando $A$ y $B$ abajo. Al estar $C=0$ arriba, los nodos internos $n_1$ y $n_2$ quedan físicamente desconectados de `dyn`, impidiendo la cesión de carga desde $C_{dyn}$.
3. **Mitigación 3 (Keeper PMOS Débil $W_{kp} = 45\text{ nm}$):** Conectar un transistor PMOS débil realimentado desde `out` hacia `dyn`. Al producirse la caída inicial por charge sharing, si $V(out)$ no supera el umbral, el keeper suministra corriente desde $V_{DD}$, restaurando dinámicamente el nivel de `dyn` a $1.0\text{ V}$.

---

**Fin del Documento de Predicción Analítica Previa.**  
*Este archivo queda registrado en el repositorio antes de la ejecución de cualquier simulación transitoria de la Actividad 2.*
