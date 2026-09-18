# Actividad 2: Compartición de Carga (Charge Sharing) en NAND3 Dinámica Footed
**Documentación Técnica y Cuantitativa de Resultados**  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Curso:** Microelectrónica y Sistemas Nanoelectrónicos — FIEE UNMSM (2026-II)  
**Tecnología:** PTM 45 nm HP Metal Gate / High-κ / Strained-Si ($V_{DD} = 1.0\text{ V}$, $T = 27\ ^\circ\text{C}$)  
**Fecha:** 17 de septiembre de 2026  

---

## 1. Introducción y Fundamentos Físicos

En la compuerta NAND3 CMOS dinámica footed con inversor dominó de salida, la red de descenso (PDN) serie contiene tres nodos internos intermedios: $n_1$ (entre $M_1$ y $M_2$), $n_2$ (entre $M_2$ y $M_3$) y $n_3$ (entre $M_3$ y el footer $M_f$). 

Cuando un ciclo de evaluación previo activa todas las entradas ($A=B=C=1$), todos los nodos internos descargan completamente a $0\text{ V}$. Si en el ciclo siguiente la compuerta evalúa una condición lógica en la que la PDN debe permanecer abierta a tierra pero los transistores superiores conducen (patrón de peor caso: $A=1$, $B=1$, $C=0$):
1. El transistor de precarga $M_p$ se corta ($CLK = 1$), dejando al nodo dinámico `dyn` **flotante** en $V_{DD}$.
2. El transistor $M_3$ permanece en corte ($C=0$), manteniendo abierta la conexión a tierra a través de $M_f$.
3. Los transistores superiores $M_1$ ($A=1$) y $M_2$ ($B=1$) entran en conducción, conectando el nodo dinámico cargado con las capacitancias parásitas de difusión de $n_1$ y $n_2$.
4. La carga electrostática almacenada en $C_{dyn}$ se redistribuye hacia $C_{n1}$ y $C_{n2}$, provocando una caída transitoria de tensión $\Delta V$ en el nodo dinámico.

---

## 2. Geometría de Difusión y Cálculo de Capacitancias

Conforme a la Sección 6.2 y 6.3 de la Guía Oficial, las geometrías de difusión se modelan explícitamente mediante:
* $L_{diff} = 90\text{ nm}$
* $W_{PDN} = 3 \times W_n = 3 \times 90\text{ nm} = 270\text{ nm}$
* Área de difusión: $Ad = W \times L_{diff} = 270\text{ nm} \times 90\text{ nm} = 0.0243\ \mu\text{m}^2 = 2.430 \times 10^{-14}\text{ m}^2$
* Perímetro de difusión: $Pd = W + 2 L_{diff} = 270\text{ nm} + 180\text{ nm} = 450\text{ nm} = 4.500 \times 10^{-7}\text{ m}$

### Parámetros Extraídos de `ptm45hp.lib`:
* $c_j = c_{js} = c_{jd} = 0.0005\text{ F/m}^2 = 0.500\text{ fF}/\mu\text{m}^2$ ($PB=1\text{ V}$, $MJ=0.50$)
* $c_{jsw} = c_{jsws} = c_{jswd} = 5.00 \times 10^{-10}\text{ F/m} = 0.500\text{ fF}/\mu\text{m}$ ($PBSW=1\text{ V}$, $MJSW=0.33$)

### Componentes de Capacitancia por Contacto de Difusión ($C_{diff,1}$):
* Fondo: $C_{bottom} = c_j \times Ad = 0.01215\text{ fF}$ ($5.1\%$)
* Borde (Sidewall): $C_{sidewall} = c_{jsw} \times Pd = 0.22500\text{ fF}$ ($94.9\%$)
* Total por contacto: $C_{diff,1} = 0.23715\text{ fF}$

### Capacitancias Nodal Interna y Dinámica:
* Nodo $n_1$ (2 contactos: $M_1$ y $M_2$): $C_{n1} = 2 \times 0.23715 = 0.4743\text{ fF}$
* Nodo $n_2$ (2 contactos: $M_2$ y $M_3$): $C_{n2} = 2 \times 0.23715 = 0.4743\text{ fF}$
* **Capacitancia agregada interna:** $C_a \equiv C_{n1} + C_{n2} = 0.9486\text{ fF}$
* Capacitancia parásita fija sobre `dyn`:
  * Solapamiento PMOS: $C_{gd}(M_p) = cgdo \times W_p = 0.0149\text{ fF}$
  * Entrada inversor dominó: $C_g(\text{inversor}) = 0.3292\text{ fF}$
  * Difusión $M_1$ en `dyn`: $C_{diff,M1} = 0.2372\text{ fF}$
  * Total parásitas en `dyn`: $C_{par,dyn} = 0.5812\text{ fF}$ (o $0.3441\text{ fF}$ excluyendo difusión de $M_1$ según fórmula abreviada de la guía).

---

## 3. Discrepancia Física: Reparto Puro vs Corte Subumbral del Transistor Pasante

La ecuación analítica estándar de redistribución de carga pura asume transistores ideales sin caída de umbral:
$$\Delta V_{pred} = V_{DD} \cdot \frac{C_a}{C_a + C_{dyn}}$$

Sin embargo, en simulación SPICE real con modelos BSIM4, la caída real es significativamente menor ($\approx 2.5\times$ a $3\times$ inferior a la predicción teórica):

1. **Corte Subumbral de $M_2$:**  
   El transistor $M_2$ actúa como un transistor de paso (*pass-transistor*) cuyo terminal de compuerta está en $V_B = 1.0\text{ V}$. A medida que la carga fluye hacia el nodo $n_2$, la tensión $V(n_2)$ se eleva. Debido a que el sustrato está a $0\text{ V}$, el terminal de fuente experimenta efecto de cuerpo ($V_{SB2} = V_{n2} > 0$). Evaluando la formulación clásica de primer orden con el parámetro BSIM4 $k_1 = 0.4\text{ V}^{1/2}$ (extraído de `ptm45hp.lib`, con $k_2 = 0$) y un potencial de superficie $2\phi_F \approx 0.8\text{ V}$, ante una polarización de fuente $V_{SB2} \approx 0.5\text{ V} - 0.66\text{ V}$ el incremento de umbral se estima analíticamente en $\Delta V_{th} \approx k_1 (\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F}) \approx 0.4(\sqrt{1.3} - \sqrt{0.8}) \approx 0.10\text{ V}$, situando el umbral efectivo en un rango orientativo aproximado de $V_{th,eff} \approx 0.55\text{ V} - 0.60\text{ V}$ (frente a $V_{th0} = 0.469\text{ V}$ a cero sesgo). Cabe enfatizar que este valor es una **estimación analítica aproximada de referencia** y no una extracción directa de punto de operación de LTspice, pues el modelo completo BSIM4 incorpora dependencias físicas adicionales (DIBL mediante `eta0`, modulación de longitud de canal y efectos de canal estrecho).  
   Cuando $V(n_2)$ alcanza $\approx 0.66\text{ V}$ en la simulación, la tensión compuerta-fuente cae a $V_{GS2} = 1.0 - 0.66 = 0.34\text{ V} \ll V_{th,eff}$. En este punto, $M_2$ entra en **corte subumbral**, su resistencia de canal se dispara a decenas de megaohmios y el flujo de carga hacia $C_{n2}$ se detiene drásticamente durante la ventana de evaluación ($t < 1\text{ ns}$).
2. **Capacitancia de Unión No Lineal:**  
   Al cargarse los nodos internos $n_1$ y $n_2$, la tensión inversa $V_R$ de las uniones p-n aumenta, lo cual reduce la capacitancia de difusión efectiva respecto al valor a cero sesgo ($C_j(V_R) = C_{j0} / (1 + V_R/PB)^M$).

---

## 4. Barrido Paramétrico de Carga $C_L$ y Márgenes de Ruido

A continuación se contrastan las predicciones analíticas con las mediciones reales transitorias para el barrido $C_L \in [0.5, 1.0, 2.0, 4.0]\text{ fF}$ (referencia: umbrales del inversor dominó de Fase 2: $V_M = 0.4797\text{ V}$, $V_{IH} = 0.5785\text{ V}$, $NM_H = 0.4215\text{ V}$, $\Delta V_{crit,M} = 0.5203\text{ V}$):

| $C_L$ (fF) | $\Delta V_{pred}$ (Guía) | $\Delta V_{pred}$ (Full) | $\Delta V_{sim}$ (eval max) | $V_{dyn,min}$ (V) | $V_{out,max}$ (mV) | Margen Lógico | Error Teórico (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.5** | 529.15 mV | 467.34 mV | **175.92 mV** | **0.8241 V** | 0.678 mV | Seguro ($V_{dyn} > V_{IH}$) | +200.8% |
| **1.0** | 413.75 mV | 374.97 mV | **138.26 mV** | **0.8617 V** | 0.389 mV | Seguro ($V_{dyn} > V_{IH}$) | +199.3% |
| **2.0** | 288.09 mV | 268.74 mV | **101.03 mV** | **0.8990 V** | 0.149 mV | Seguro ($V_{dyn} > V_{IH}$) | +185.1% |
| **4.0** | 179.23 mV | 171.54 mV | **67.62 mV** | **0.9324 V** | 0.008 mV | Seguro ($V_{dyn} > V_{IH}$) | +165.0% |

### Diagnóstico de Fallo Lógico:
* En ningún caso del barrido se produce conmutación errónea en la salida dominó ($V_{out,max} \le 0.68\text{ mV} \ll V_{IL} = 0.3675\text{ V}$).
* Si la redistribución hubiese seguido la fórmula analítica pura sin corte de umbral, para $C_L = 0.5\text{ fF}$ la caída predicha ($\Delta V_{pred} = 529.2\text{ mV}$) habría llevado $V(dyn)$ a $0.4708\text{ V} < V_M$, provocando un fallo lógico espurio masivo. El corte subumbral intrínseco del NMOS protege a la compuerta.

---

## 5. Evaluación Cuantitativa de las Tres Técnicas de Mitigación

Se implementaron y compararon las tres técnicas de mitigación bajo la condición nominal de peor caso ($C_L = 2.0\text{ fF}$, $T_{clk} = 2\text{ ns}$):

| Configuración | Ensayo | $\Delta V_{eval}$ Máx | $V_{dyn,min}$ | $V_{out,max}$ | Tiempo Rest. ($t_{rec}$) | Coste en Área | Sobrecarga de Reloj |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Base (Sin Mitigación)** | `ENS-A2-02` | **101.03 mV** | 0.8990 V | 0.149 mV | Sin recup. en eval. | Base (7 transistores) | $C_{clk} = C_{g,Mp} + C_{g,Mf}$ |
| **Mitigación 1: Precarga Nodos $n_1, n_2$** | `ENS-A2-04` | **$\le 0\,$mV** | 1.0120 V | 0.267 mV | Inmediato ($t=0$) | +2 PMOS ($W_p=135\,$nm) | $\Delta C_{clk,gate} \approx 0.34\,$fF (+67% comp.) |
| **Mitigación 2: Reordenamiento PDN ($C$ tope)** | `ENS-A2-05` | **0.014 mV** | 0.99999 V | 0.294 mV | Intransitorio | **0 transistores** (solo routing) | **0 fF** (idéntica a base) |
| **Mitigación 3: Keeper $W_{kp} = 45\,$nm** | `ENS-A2-06` | **42.18 mV** | 0.9578 V | 0.384 mV | **80.30 ps** | +1 PMOS ($W=45\,$nm) | 0 fF en $CLK$ |

### Análisis Comparativo de Mitigaciones:

0. **Caso Base (Sin Mitigación):**
   * **Dinámica de Recuperación:** En la configuración base (`ENS-A2-02`), **no existe recuperación durante la ventana de evaluación; el nodo se restaura en la siguiente fase de precarga** cuando el transistor $M_p$ se enciende ($CLK=0$). Durante toda la fase de evaluación, el nodo dinámico permanece degradado en $V(dyn) = 0.899\text{ V}$.
1. **Mitigación 1 (Precarga Interna):**
   * **Mecanismo:** Precarga $n_1$ y $n_2$ a $V_{DD}$ durante la fase de precarga ($CLK=0$). Al iniciar la evaluación, la diferencia de potencial entre `dyn`, $n_1$ y $n_2$ es nula ($\Delta V = 0$), suprimiendo la fuerza electromotriz de redistribución.
   * **Sobrecarga de Línea de Reloj:** La adición de dos PMOS ($W_p = 135\text{ nm}$, $L = 45\text{ nm}$) gobernados por $CLK$ introduce una capacitancia de compuerta adicional estimada en $\Delta C_{clk,gate} = 2 \times (W_p \cdot L \cdot C_{ox}) = 2 \times (135\text{ nm} \times 45\text{ nm} \times 27.62\text{ fF}/\mu\text{m}^2) \approx 0.336\text{ fF} \approx 0.34\text{ fF}$. Comparada con la carga base de compuerta en $CLK$ ($C_{g,Mp} + C_{g,Mf} \approx 0.168\text{ fF} + 0.335\text{ fF} = 0.503\text{ fF}$), esto representa un incremento relativo de compuerta del $+66.8\% \approx +67\%$. Cabe precisar que esta cifra corresponde estrictamente a la estimación de carga intrínseca de compuerta (*gate-only*); la inclusión de las capacitancias parásitas de solapamiento compuerta-drenaje/fuente ($C_{gdo}, C_{gso}$) incrementaría ligeramente la capacitancia efectiva total.
   * **Observación de Overshoot / Clock Feedthrough:** En la simulación `ENS-A2-04`, las tensiones nodales exhiben un ligero sobreimpulso por encima de $V_{DD}$ ($V(dyn)_{eval,min} = 1.012\text{ V}$, $V(n_1) \approx 1.069\text{ V}$, $V(n_2) \approx 1.062\text{ V}$, con $\Delta V_{eval} \le 0$). Este fenómeno se atribuye prudentemente a un *overshoot* transitorio debido al acoplamiento capacitivo asociado a la transición de reloj (*clock feedthrough / bootstrap-like behavior*). Si bien en este ensayo dicho sobreimpulso no ocasionó ningún fallo funcional ni conmutación espuria ($V_{out,max} \le 0.27\text{ mV}$), constituye un efecto no ideal relevante a considerar en diseño.
   * **¿Por qué no se precarga $n_3$?** El nodo $n_3$ está conectado directamente al drenaje del transistor footer $M_f$. Al entrar en evaluación ($CLK \rightarrow 1$), $M_f$ conmuta inmediatamente a conducción. Si $n_3$ se encontrara precargado a $V_{DD}$, descargaría a tierra en cada ciclo de evaluación sin importar las entradas, provocando una disipación dinámica parásita $C_{n3} V_{DD}^2 f_{clk}$ inútil, ya que cuando $C=0$, $M_3$ está en corte y $n_3$ nunca interactúa con `dyn`.
2. **Mitigación 2 (Reordenamiento de Entradas en la PDN):**
   * **Mecanismo:** Al colocar la entrada crítica tardía o nula ($C=0$) en el transistor superior ($M_3$ adyacente a `dyn`), el canal de $M_3$ se mantiene abierto en el propio contorno del nodo dinámico. Como consecuencia, las capacitancias parásitas de $n_1$ y $n_2$ quedan físicamente desconectadas de `dyn`. La caída es prácticamente nula ($14\ \mu\text{V}$).
   * **Decisión en Dominó vs Estática:** En lógica estática, el orden de transistores en la PDN no modifica la función lógica ni los niveles lógicos estáticos finales en corriente continua. En lógica dominó, el nodo dinámico es una **memoria capacitiva flotante** durante la evaluación; por ello, la ubicación de las entradas en la pila determina directamente qué nodos parásitos pueden drenar carga desde $C_{dyn}$, convirtiendo el apilamiento en un parámetro de diseño primordial de integridad de señal.
3. **Mitigación 3 (Transistor Keeper $W_{kp} = 45\text{ nm}$ y Contención):**
   * **Mecanismo:** El keeper realimentado detecta el estado dinámico y suministra corriente de reposición desde $V_{DD}$. Amortigua la caída transitoria de $101.03\text{ mV}$ a $42.18\text{ mV}$ (reducción del **$58.2\%$**) y restaura activamente $V(dyn)$ al $99\%$ de $V_{DD}$ en **$80.30\text{ ps}$**.
   * **Compromiso de Contención (`ENS-A2-07`):** Cuando la compuerta evalúa una transición legítima a "0" ($A=B=C=1$), la PDN debe descargar $C_{dyn}$ venciendo la corriente del keeper hasta que la salida dominó supere el umbral y desconecte el PMOS.
     * Retardo sin keeper: $t_{pHL,dyn} = 23.95\text{ ps}$, $t_{pLH,out} = 37.58\text{ ps}$.
     * Retardo con keeper ($W_{kp}=45\text{ nm}$): $t_{pHL,dyn} = 27.46\text{ ps}$, $t_{pLH,out} = 43.09\text{ ps}$.
     * **Penalización de contención:** $\Delta t_{pHL} = +3.51\text{ ps}$ (**$+14.65\%$**); $\Delta t_{pLH,out} = +5.52\text{ ps}$ (**$+14.69\%$**).

---

## 6. Inventario de Figuras Generadas (300 DPI)

* [**`fig1_act2_peor_caso_formas_onda.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act2/figuras/fig1_act2_peor_caso_formas_onda.png): Formas de onda sincronizadas del peor caso (control, nodos internos, nodo dinámico y salida).
* [**`fig2_act2_dv_vs_cl_analitico_simulado.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act2/figuras/fig2_act2_dv_vs_cl_analitico_simulado.png): Curvas paramétricas de $\Delta V \text{ vs } C_L$ y $V_{dyn,min} \text{ vs } C_L$, mostrando el desajuste analítico/simulado y la delimitación de la zona lógica segura.
* [**`fig3_act2_comparacion_mitigaciones.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act2/figuras/fig3_act2_comparacion_mitigaciones.png): Comparación transitoria de las 3 mitigaciones en evaluación y cuantificación del compromiso de contención en velocidad.
