# Actividad 1 — NAND3 Dinámica Footed: Fases, Asimetría y Consumo

**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
**Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Docente:** MsC. Luz Adanaqué Infante  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Directorio de Trabajo:** [`LD2_Arcila_Yactayo/act1/`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act1/)  
**Tecnología Principal:** PTM 45nm HP ($V_{DD} = 1.0\text{ V}$, $T = 27^\circ\text{C}$)

---

## 1. Topología y Dimensionamiento de Circuitos

### A. NAND3 Dinámica Footed con Inversor Dominó (Guía Oficial, Sec. 5)
* **Red de Descarga (PDN) y Footer ($M_f$):**
  * 4 transistores NMOS en serie ($M_1, M_2, M_3, M_f$) dimensionados según la guía con $W = 3 W_n = 3 \times 90\text{ nm} = 270\text{ nm}$, $L = 45\text{ nm}$.
  * La resistencia equivalente de descarga emula la corriente de un NMOS unitario de referencia ($W_n = 90\text{ nm}$).
* **Transistor de Precarga ($M_p$):**
  * PMOS conectado a $V_{DD}$ con $W = W_p = 135\text{ nm}$, $L = 45\text{ nm}$ ($\beta = 1.5$ por compensación de movilidad de huecos).
* **Inversor Dominó de Salida:**
  * $M_{pi}$: PMOS con $W = W_p = 135\text{ nm}$, $L = 45\text{ nm}$.
  * $M_{ni}$: NMOS con $W = W_n = 90\text{ nm}$, $L = 45\text{ nm}$.
* **Condiciones de Carga Capacitiva (Especificación de la Guía):**
  * Carga externa en el nodo dinámico: $C_L = 2\text{ fF}$ (especificada en el encabezado oficial `.param CL=2f`).
  * Carga de compuerta del inversor dominó conectada al nodo $dyn$ ($W_p = 135\text{ nm}, W_n = 90\text{ nm}$).
  * Carga de salida dominó: $C_{out} = 1\text{ fF}$ (especificada como `Cout out 0 1f`).
* **Conteo de Transistores:**
  * Núcleo dinámico footed solo: **5 transistores** (4 NMOS + 1 PMOS).
  * Etapa dominó completa (incluyendo inversor restaurador): **7 transistores**.

### B. NAND3 CMOS Estática Equivalente
* **PUN:** 3 transistores PMOS en paralelo ($M_{Pa}, M_{Pb}, M_{Pc}$) con $W = W_p = 135\text{ nm}$, $L = 45\text{ nm}$.
* **PDN:** 3 transistores NMOS en serie ($M_{Na}, M_{Nb}, M_{Nc}$) con $W = 3 W_n = 270\text{ nm}$, $L = 45\text{ nm}$.
* **Carga de Salida:** $C_{out} = 1\text{ fF}$.
* **Conteo Total de Transistores:** 3 (PUN) + 3 (PDN) = **6 transistores**.

---

## 2. Tabla Comparativa Oficial: Dinámica vs Estática (Tarea 3)

Todas las métricas numéricas fueron extraídas mediante el pipeline automatizado validado (`parse_spice_log.py` y `parse_spice_raw.py`) a partir de simulaciones en LTspice 26.0.2:

| Métrica Evaluada | NAND3 Dinámica (Domino) | NAND3 Estática Equivalente | Cociente (Dyn / Stat) | Notas / Procedencia |
| :--- | :---: | :---: | :---: | :--- |
| **N.º de Transistores** | **5** (núcleo) / **7** (total) | **6** | **0.833** / **1.167** | Guía oficial Sec. 5 |
| **$t_{pHL}$ (Evaluación en nodo $dyn$)** | **22.17 ps** | **9.61 ps** | **2.307** | $t_{pHL,dyn}$ oficial vs $t_{pHL,stat}$ (ENS-A1-07) |
| **$t_{pLH}$ (Precarga en nodo $dyn$)** | **25.13 ps** | **12.40 ps** | **2.027** | $t_{pLH,dyn}$ oficial vs $t_{pLH,stat}$ (ENS-A1-07) |
| **Retardo en Salidas Lógicas (Triggers Asimétricos)** | **35.89 ps** (salida $out$<br>desde flanco $CLK\uparrow$) | **9.61 ps** (salida $out\_stat$<br>desde flanco $A\uparrow$) | **3.734** | Ambos observados en salida lógica ($C_{out}=1\text{ fF}$); eventos de disparo distintos ($CLK\uparrow$ vs $A\uparrow$, cociente descriptivo) |
| **Control sin carga externa $C_L$ en $dyn$ (ENS-A1-08)** | $t_{pHL,dyn}=11.26\text{ ps}$<br>$t_{pd,\text{eval}}=21.27\text{ ps}$ | — | — | Control con $C_L=0$; el nodo $dyn$ conserva difusiones, capacidades MOS y compuerta del inversor |
| **Capacitancia de Entrada $C_{in}(A)$** | **0.3415 fF** | **0.5936 fF** | **0.5753** (-42.5%) | Integración $Q=\int I\,dt$ (ENS-A1-04) |
| **$P_{\text{avg}}$ con $A$ conmutando ($T_A=8\text{ ns}$)** | **1.2393 $\mu$W** | **0.2692 $\mu$W** | **4.604** | Estímulo idéntico de $125\text{ MHz}$ (ENS-A1-07) |
| *$P_{\text{avg}}$ Estática con $A$ a 500 MHz (Histórico)* | *1.2393 $\mu$W* | *0.8206 $\mu$W* | *1.510* | *Referencia histórica preliminar (ENS-A1-02)* |
| **$P_{\text{avg}}$ @ 500 MHz (Entradas fijas en 1)** | **2.7255 $\mu$W** | **1.7004 nW** | **1602.9** | Trampa de potencia: $\alpha=1$ vs $\alpha=0$ (ENS-A1-03) |

#### Precisiones Metodológicas sobre la Comparación de Retardos:
1. **Eventos de Disparo (Triggers) Asimétricos:**
   * En la **NAND3 dominó**, el retardo medido es:
     $$\text{Retardo de evaluación desde } CLK\uparrow \text{ hasta } OUT\uparrow = \mathbf{35.89\text{ ps}}$$
     (dado que la entrada $A$ ya se encuentra estabilizada en alto durante la fase de precarga).
   * En la **NAND3 estática**, el retardo medido es:
     $$\text{Retardo de propagación desde } A\uparrow \text{ hasta } OUT\_STAT\downarrow = \mathbf{9.61\text{ ps}}$$
   * *Aclaración:* Si bien ambos tiempos se miden en los terminales lógicos finales con carga de $1\text{ fF}$, los eventos de disparo físico son de distinta naturaleza ($CLK\uparrow$ sincrónico frente a $A\uparrow$ asíncrono de dato). Por tanto, el cociente ($3.734\times$) es de carácter descriptivo sobre la respuesta temporal de cada topología y no constituye una comparación estrictamente idéntica de camino de datos (*data-to-output*).
2. **Control de Retardo Sin Carga Externa $C_L$ (ENS-A1-08):**
   * Al fijar $C_L = 0\text{ fF}$ en el nodo $dyn$, el retardo de evaluación se reduce a $t_{pHL,dyn} = 11.26\text{ ps}$ y $t_{pd,\text{eval}} = 21.27\text{ ps}$.
   * *Aclaración:* Este ensayo se denomina rigurosamente **control de retardo sin carga externa $C_L$**. Aun sin el condensador concentrado de $2\text{ fF}$, el nodo $dyn$ no carece de capacitancia: retiene las capacitancias parásitas de difusión de $M_p$ y $M_1$, las capacitancias parásitas MOS inherentes a la tecnología BSIM4/PTM 45nm y la capacitancia de compuerta de entrada de los transistores del inversor dominó ($M_{pi}$, $M_{ni}$).

---

## 3. Análisis de Fases y Formas de Onda (Tarea 1)

En la simulación oficial de la guía (`nand3_dinamica_base.cir`), el reloj conmuta a $500\text{ MHz}$ ($T_{clk} = 2\text{ ns}$) y la entrada $A$ tiene un retardo intencional de $1.1\text{ ns}$ ($0.55 T_{clk}$). Esto permite observar las cuatro fases operativas fundamentales (ver Figura 1):

1. **Fase I: Evaluación con PDN Abierta ($t \in [0.0, 1.0\text{ ns}]$):**
   * Reloj $CLK = 1$ ($M_p$ en corte, footer $M_f$ en conducción).
   * Entrada $A = 0 \implies$ el transistor $M_1$ está en corte, impidiendo cualquier camino hacia tierra.
   * **Estado del Nodo Dinámico:** El nodo $dyn$ queda **FLOTANTE en nivel alto ($V_{DD} = 1.0\text{ V}$)**.
   * Se aprecia un ligero sobreimpulso a $1.022\text{ V}$ debido al acoplamiento capacitivo (*clock feedthrough*) inducido por el flanco ascendente de $CLK$ a través de $C_{gd}(M_p)$.
2. **Fase II: Precarga con $A=1$ ($t \in [1.0, 2.0\text{ ns}]$):**
   * Reloj $CLK = 0$ ($M_p$ en conducción activa hacia $V_{DD}$, footer $M_f$ en corte).
   * A $t = 1.1\text{ ns}$, la entrada $A$ conmuta a nivel 1. Aunque $A=B=C=1$, el footer $M_f$ permanece cortado por $CLK=0$, por lo que la red a tierra no se activa. El nodo $dyn$ se mantiene conectado a $V_{DD}$ por $M_p$.
3. **Fase III: Evaluación con Descarga Completa ($t \in [2.0, 3.0\text{ ns}]$):**
   * Reloj $CLK = 1$ (flanco de subida en $t = 2.0\text{ ns}$).
   * Como $A=B=C=1$, toda la PDN ($M_1, M_2, M_3, M_f$) conduce simultáneamente.
   * El nodo dinámico $dyn$ se descarga hacia $0\text{ V}$ con un retardo de $t_{pHL,dyn} = 22.17\text{ ps}$.
   * La salida del inversor dominó $out$ conmuta monótonamente de $0$ a $1$ con $t_{pLH,out} = 35.89\text{ ps}$.
4. **Fase IV: Precarga y Restauración ($t \in [3.0, 4.0\text{ ns}]$):**
   * Reloj $CLK = 0$ (flanco de bajada en $t = 3.0\text{ ns}$).
   * $M_p$ se enciende y recarga el nodo $dyn$ desde $0\text{ V}$ hacia $V_{DD}$ con un retardo de precarga $t_{pLH,dyn} = 25.13\text{ ps}$.
   * El inversor dominó restaura la salida $out$ hacia $0\text{ V}$ con $t_{pHL,out} = 38.06\text{ ps}$.

---

## 4. Asimetría Temporal y Rol de $t_{pLH}$ en Lógica Dominó (Tarea 2)

* **¿Por qué $t_{pLH}$ del nodo dinámico "no cuenta" como retardo lógico en dominó?**
  En lógica dominó, el cómputo lógico de propagación de datos ocurre exclusivamente durante la fase de evaluación ($CLK=1$), en la cual las salidas conmutan monótonamente en flanco ascendente ($0 \to 1$). La precarga ($t_{pLH}$ en $dyn$, que se traduce en $t_{pHL}$ en $out$) ocurre mientras el reloj está en nivel bajo ($CLK=0$). Durante este semi-periodo, el circuito se encuentra en fase de restauración global ("tiempo muerto" de cómputo lógico); por tanto, la precarga no pertenece a la ruta crítica combinacional de avance de datos.
* **Restricción que impone sobre el ciclo de reloj ($T_{clk}$):**
  El semi-periodo de precarga ($T_{clk}/2$) debe ser estrictamente suficiente para que $M_p$ restaure el nodo $dyn$ completamente a $V_{DD}$:
  $$\frac{T_{clk}}{2} \ge t_{\text{precarga}} \approx 3 \text{ a } 4 \times \tau_{\text{pre}}$$
  Si la frecuencia de reloj se incrementa excesivamente de modo que $T_{clk}/2 < t_{\text{precarga}}$, la evaluación comenzará con carga incompleta ($V(dyn) < V_{DD}$), degradando el margen de ruido $NM_H$ y provocando disparos espurios en compuertas en cascada.

---

## 5. La Trampa de Potencia y Comparación Analítica vs Medida (Tarea 4)

### A. Explicación de la Trampa
Con las entradas fijas permanentemente en nivel alto ($A=1, B=1, C=1$):
* En la **NAND3 estática**, la salida permanece fija en $0\text{ V}$. Al no existir transiciones en ningún nodo, su factor de actividad dinámico es nulo ($\alpha = 0$). Su consumo se reduce a la corriente de fuga subumbral y de compuerta ($P_{\text{stat}} = 1.7004\text{ nW}$).
* En la **NAND3 dinámica footed**, aunque las entradas de datos sean constantes, el reloj conmuta periódicamente a $500\text{ MHz}$. En cada periodo:
  * Durante precarga ($CLK=0$), $M_p$ carga el nodo dinámico a $V_{DD}$.
  * Durante evaluación ($CLK=1$), la PDN descarga el nodo dinámico a tierra.
  Por lo tanto, la compuerta dinámica conmuta con un **factor de actividad forzado de $\alpha = 1$ en cada periodo de reloj**, consumiendo $2.7255\text{ }\mu\text{W}$ (un factor de **$1602.9\times$** mayor que la estática).

### B. Potencia Teórica de la Carga Nominal vs Potencia Medida
La potencia dinámica teórica requerida para cargar y descargar la capacitancia concentrada explícita impuesta por la guía ($C_L = 2.0\text{ fF}$) con $\alpha = 1$, $V_{DD} = 1.0\text{ V}$ y $f = 500\text{ MHz}$ es:
$$P_{\text{teor}}(C_L) = \alpha \cdot C_L \cdot V_{DD}^2 \cdot f = 1 \times (2.0\text{ fF}) \times (1.0\text{ V})^2 \times (500\times 10^6\text{ s}^{-1}) = \mathbf{1.0000\text{ }\mu\text{W}}$$

La potencia total media suministrada por $V_{DD}$, medida por LTspice mediante `.meas TRAN Pavg AVG -I(Vdd)*V(vdd)`, es:
$$P_{\text{medida,total}} = \mathbf{2.7255\text{ }\mu\text{W}}$$

### C. Justificación Física Cualitativa de la Discrepancia
La diferencia entre la potencia elemental de $C_L$ ($1.000\text{ }\mu\text{W}$) y la potencia total suministrada por la fuente ($2.7255\text{ }\mu\text{W}$) se debe a los siguientes mecanismos físicos no concentrados:
1. **Capacitancias parásitas del nodo dinámico ($C_{par,dyn}$):** Capacitancias de difusión de drenaje de $M_p$ y $M_1$, más la capacitancia de compuerta de los transistores del inversor dominó ($M_{pi}$ y $M_{ni}$).
2. **Conmutación del inversor dominó de salida:** En cada ciclo de reloj, la salida $out$ conmuta entre $0\text{ V}$ y $V_{DD}$, cargando y descargando la capacitancia externa $C_{out} = 1\text{ fF}$ y las difusiones de drenaje del inversor.
3. **Corriente de cortocircuito en el inversor dominó:** Durante las transiciones del nodo $dyn$, existe un intervalo finito en que tanto $M_{pi}$ como $M_{ni}$ conducen simultáneamente entre $V_{DD}$ y tierra.
4. **Carga y descarga parcial de difusiones internas:** Los nodos intermedios de la PDN en serie ($n_1, n_2, n_3$) experimentan redistribución y carga de sus capacidades de difusión.
5. **Fugas estáticas:** Corrientes de fuga subumbral y túnel de compuerta en todos los dispositivos conectados a $V_{DD}$.

*Nota Metodológica:* De acuerdo con el principio de integridad física del laboratorio, no se presentan valores numéricos desagregados inventados o forzados aritméticamente, reconociendo que cada mecanismo contribuye al total medido de $2.7255\text{ }\mu\text{W}$.

---

## 6. Retención con PDN Abierta y Degradación por Fugas (Tarea 5)

En este ensayo se fijó $V_c = 0\text{ V}$ (corte en el transistor inferior $M_3$), abriendo permanentemente la ruta a tierra de la PDN.

### Comparativa de Retención a 27°C:
1. **Reloj Nominal ($T_{clk} = 2\text{ ns}$, $f = 500\text{ MHz}$):**
   * En la fase de evaluación ($1\text{ ns}$ de duración), el nodo dinámico permanece flotante en nivel alto.
   * Tensión mínima alcanzada: $V(dyn)_{\text{min}} = \mathbf{0.9936\text{ V}}$, lo que representa una caída de apenas $\Delta V = \mathbf{6.41\text{ mV}}$.
   * La salida $out$ se mantiene inalterada en $\approx 0\text{ V}$ ($V_{out,\text{max}} = 0.31\text{ mV}$).
   * **Conclusión:** Para frecuencias del orden de $500\text{ MHz}$, la ventana de evaluación es lo bastante breve como para que las fugas no comprometan la retención.
2. **Reloj Lento ($T_{clk} = 400\text{ ns}$, ventana de evaluación continua de $200\text{ ns}$):**
   * Durante los $200\text{ ns}$ en que el nodo $dyn$ intenta retener el nivel alto flotante, las corrientes de fuga subumbral ($I_{off}$) de la PDN y el footer drenan progresivamente la carga del nodo.
   * La tensión decae monótonamente hasta $V(dyn)_{\text{final}} = \mathbf{0.8837\text{ V}}$, sufriendo una pérdida neta de $\Delta V = \mathbf{116.28\text{ mV}}$.
   * A $27^\circ\text{C}$, la tensión final ($0.884\text{ V}$) aún se encuentra por encima del umbral de conmutación del inversor ($V_M = 0.48\text{ V}$), por lo que la salida $out$ permanece en reposo ($V_{out} \approx 0.04\text{ mV}$).
   * **Conclusión Experimental:** Una ventana de evaluación más prolongada produce una pérdida de carga acumulativa cuantificable. Este comportamiento demuestra experimentalmente que un nodo dinámico flotante no puede retener indefinidamente su estado, motivando el estudio de una frecuencia mínima de operación ($f_{min}$) y el dimensionamiento de transistores de compensación (*keepers*), aspectos que se profundizarán en las Actividades 2 y 3.

---

## 7. Ventaja en Capacitancia de Entrada $C_{in}(A)$

* **Diferencia Estructural:**
  * En la compuerta estática, la entrada $A$ comanda un NMOS de la PDN ($W = 270\text{ nm}$) y un PMOS de la PUN ($W = 135\text{ nm}$), totalizando un ancho de compuerta de $405\text{ nm}$.
  * En la compuerta dinámica footed, la PUN se reemplaza por el PMOS de precarga global gobernado por el reloj. La entrada $A$ comanda únicamente el transistor NMOS de la PDN ($W = 270\text{ nm}$).
* **Resultado Extraído (ENS-A1-04):**
  * $C_{in,\text{dyn}} = \mathbf{0.3415\text{ fF}}$ frente a $C_{in,\text{stat}} = \mathbf{0.5936\text{ fF}}$, logrando una reducción del **$42.5\%$** en la carga capacitiva de entrada.
  * Esta reducción del esfuerzo lógico de entrada favorece la velocidad en etapas combinacionales que alimentan compuertas dominó.

---

## 8. Figuras Oficiales Generadas (300 DPI)

Ubicadas en [`LD2_Arcila_Yactayo/act1/figuras/`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act1/figuras/):
1. `fig1_act1_fases_formas_onda.png`: Formas de onda $V(clk), V(a), V(dyn), V(out)$ con bandas sombreadas y rotulación explícita de las cuatro fases de operación (evaluación con nodo flotante, precarga, evaluación con descarga y precarga final).
2. `fig2_act1_dinamica_vs_estatica.png`: Comparación temporal sincronizada con el **mismo estímulo de entrada** $V(a)$ ($T_A=8\text{ ns}$), mostrando la conmutación dominó goberanda por reloj frente a la conmutación asíncrona estática.
3. `fig3_act1_retencion_pdn_abierta.png`: Pérdida de carga en el nodo dinámico flotante a $T_{clk}=2\text{ ns}$ ($\Delta V = 6.4\text{ mV}$) frente a $T_{clk}=400\text{ ns}$ ($\Delta V = 116.3\text{ mV}$).
