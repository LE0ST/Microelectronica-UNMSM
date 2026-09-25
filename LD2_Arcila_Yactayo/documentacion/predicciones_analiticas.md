# Predicciones Analíticas Previas a la Simulación — LD2

**Autores:** Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander  
**Requisito Rúbrica:** *"El informe se rechaza si no incluye la predicción analítica de la Act. 2"* (Pág. 13 de la guía).

---

## 1. Actividad 2 — Deducción Analítica de la Compartición de Carga

### 1.1. Planteamiento Físico y Conservación de Carga
Considérese la compuerta NAND3 dinámica footed con nodos internos $n_1, n_2, n_3$ en la PDN serie:
* **Ciclo 1:** Con $A=B=C=1$ durante la evaluación, la PDN conduce a tierra y descarga completamente el nodo dinámico $dyn$ y todos los nodos internos ($V_{n1} = V_{n2} = V_{n3} = 0\text{ V}$).
* **Fase de precarga:** $CLK=0$ recarga el nodo dinámico a $V(dyn) = V_{DD}$. Los nodos internos $n_1, n_2$ permanecen en $0\text{ V}$ si la PDN se abre.
* **Ciclo 2 (Evaluación con $A=1, B=1, C=0$):** Al activarse $M_1$ y $M_2$ (con $M_3$ cortado), el nodo dinámico $dyn$ se conecta directamente con los nodos parásitos $n_1$ y $n_2$. Como no existe camino a tierra ($C=0$), la carga almacenada en $C_L$ se redistribuye entre $C_L$ y las capacitancias de los nodos $n_1$ y $n_2$.

Aplicando el principio de conservación de carga electrostática entre el estado inicial ($t_0$) y el estado de equilibrio redistribuido ($t_f$):
$$Q_{inicial} = Q_{final}$$
$$C_L V_{DD} + C_a \cdot 0 = (C_L + C_a) V_{final}$$
donde $C_a \equiv C_{n1} + C_{n2}$ es la capacitancia parásita total de los nodos internos involucrados.

Despejando la tensión final de equilibrio $V_{final}$:
$$V_{final} = V_{DD} \frac{C_L}{C_L + C_a}$$

Por consiguiente, la caída de tensión predicha en el nodo dinámico es:
$$\Delta V_{pred} = V_{DD} - V_{final} = V_{DD} \left(1 - \frac{C_L}{C_L + C_a}\right) = V_{DD} \frac{C_a}{C_a + C_L}$$

---

### 1.2. Extracción y Cálculo Numérico de Parámetros de Capacitancia (PTM 45nm HP)

#### A. Capacitancia de unión de difusión ($C_{diff}$)
Para los transistores de la PDN ($M_1, M_2, M_3$), las dimensiones asignadas en el netlist oficial son:
* Ancho de canal: $W = 3 W_n = 3 \times 90\text{ nm} = 270\text{ nm} = 0.27\,\mu\text{m}$.
* Longitud de difusión estipulada por la guía: $L_{diff} = 90\text{ nm} = 0.09\,\mu\text{m}$.
* Área de difusión:
  $$A_d = A_s = W \cdot L_{diff} = 0.27\,\mu\text{m} \times 0.09\,\mu\text{m} = 0.0243\,\mu\text{m}^2$$
* Perímetro de difusión:
  $$P_d = P_s = W + 2 L_{diff} = 0.27\,\mu\text{m} + 2(0.09\,\mu\text{m}) = 0.45\,\mu\text{m}$$

Parámetros extraídos de la tarjeta `45nm_HP.pm`:
* Capacitancia de fondo por unidad de área: $c_{jd} = c_{js} = 0.0005\text{ F/m}^2 = 0.5\text{ fF/\mu m}^2$.
* Capacitancia perimetral de pared lateral: $c_{jswd} = c_{jsws} = 5 \times 10^{-10}\text{ F/m} = 0.5\text{ fF/\mu m}$.

Calculando las componentes de una unión de difusión individual:
$$C_{j,area} = c_{jd} \cdot A_d = (0.5\text{ fF/\mu m}^2)(0.0243\,\mu\text{m}^2) = 0.01215\text{ fF}$$
$$C_{j,sw} = c_{jswd} \cdot P_d = (0.5\text{ fF/\mu m})(0.45\,\mu\text{m}) = 0.22500\text{ fF}$$
$$C_{diff} = C_{j,area} + C_{j,sw} = 0.01215\text{ fF} + 0.22500\text{ fF} = 0.23715\text{ fF}$$

#### B. Capacitancias de los nodos internos $n_1$ y $n_2$
* **Nodo $n_1$:** Conectado a la fuente de $M_1$ y al drenador de $M_2$:
  $$C_{n1} \approx C_{diff}(S_1) + C_{diff}(D_2) = 2 \times 0.23715\text{ fF} \approx 0.4743\text{ fF}$$
* **Nodo $n_2$:** Conectado a la fuente de $M_2$ y al drenador de $M_3$:
  $$C_{n2} \approx C_{diff}(S_2) + C_{diff}(D_3) = 2 \times 0.23715\text{ fF} \approx 0.4743\text{ fF}$$
* **Capacitancia interna total $C_a$:**
  $$C_a = C_{n1} + C_{n2} \approx 0.4743\text{ fF} + 0.4743\text{ fF} \approx 0.9486\text{ fF} \approx 0.95\text{ fF}$$

#### C. Capacitancia total conectada al nodo dinámico ($C_L$)
La guía define:
$$C_L = C_{ext} + C_{gd}(M_p) + C_g(inversor)$$
con:
* $C_{ext} = 2.0\text{ fF}$ (nominal).
* $C_{gd}(M_p) = c_{gdo} \cdot W_p = (1.1 \times 10^{-10}\text{ F/m})(0.135\,\mu\text{m}) \approx 0.0149\text{ fF}$.
* $C_g(inversor) = C_{ox} (W_{ni} + W_{pi}) L_n$:
  * $t_{oxe} = 1.25\text{ nm} \implies C_{ox} = \frac{\epsilon_{ox}}{t_{oxe}} = \frac{3.9 \times 8.854 \times 10^{-12}}{1.25 \times 10^{-9}} \approx 27.6\text{ fF/\mu m}^2$.
  * Área de compuerta inversor: $(W_{ni} + W_{pi}) L_n = (0.09\,\mu\text{m} + 0.135\,\mu\text{m}) \times 0.045\,\mu\text{m} \approx 0.0101\,\mu\text{m}^2$.
  * $C_{g}(inversor) \approx 27.6\text{ fF/\mu m}^2 \times 0.0101\,\mu\text{m}^2 \approx 0.279\text{ fF}$.
* Suma de parásitos fijos en el nodo dinámico:
  $$C_{par,dyn} = C_{gd}(M_p) + C_g(inv) + C_{diff}(D_p) + C_{diff}(D_1) \approx 0.015 + 0.279 + 0.119 + 0.237 \approx 0.65\text{ fF}$$
* Para el caso nominal $C_{ext} = 2.0\text{ fF}$, la carga efectiva es $C_{L,tot} \approx 2.65\text{ fF}$.
* **Aclaración Metodológica de Sobrecarga de Reloj (Corrección A3.8.3):**
  La capacitancia $C_g(inversor) \approx 0.279\text{ fF}$ corresponde a la entrada del inversor dominó conectada al nodo `dyn`. No debe confundirse con la sobrecarga sobre la red de reloj. La red de reloj base maneja $M_p$ y $M_f$ ($C_{clk,base} \approx 0.503\text{ fF}$). En el keeper condicional, el reloj maneja además el primer inversor de retardo ($W_n=90\text{ nm}, W_p=135\text{ nm}$), cuya capacitancia de entrada es análogamente $\approx 0.279\text{ fF}$, representando un incremento geométrico estimado de $\Delta C_{clk}/C_{clk,base} \approx +55.5\%$, retirándose formalmente la cifra errónea de 14% (que resultaba de dividir $0.279\text{ fF}$ entre $C_{ext}=2.0\text{ fF}$).

---

### 1.3. Predicciones Numéricas de Caída $\Delta V_{pred}$

| $C_{ext}$ (fF) | $C_{L,tot} \approx C_{ext} + 0.65$ (fF) | $C_a$ (fF) | $\Delta V_{pred} = V_{DD} \frac{C_a}{C_a + C_L}$ (V) | $V_{final,pred}$ (V) | ¿Supera Margen de Ruido ($V_{DD}-V_M \approx 0.50$V)? | Estado Lógico Esperado |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.5** | 1.15 | 0.95 | **0.452 V** | 0.548 V | **Cercano / En riesgo crítico** | **Falla lógica / Glitch en out** |
| **1.0** | 1.65 | 0.95 | **0.365 V** | 0.635 V | No ($0.365 < 0.50$) | En zona de degradación de ruido |
| **2.0** | 2.65 | 0.95 | **0.264 V** | 0.736 V | No ($0.264 < 0.50$) | Operación correcta, margen reducido |
| **4.0** | 4.65 | 0.95 | **0.170 V** | 0.830 V | No ($0.170 < 0.50$) | Robusto frente a compartición |

---

### 1.4. Condición de Discrepancia Física (Por qué la fórmula pura sobrestima)
La ecuación de conservación pura asume que los transistores $M_1$ y $M_2$ se comportan como interruptores ideales de resistencia lineal hasta alcanzar la equipotencialidad total. Sin embargo:
1. Al fluir carga desde $dyn$ hacia $n_1$ y $n_2$, la tensión en el nodo fuente de $M_2$ ($V_{n2}$) se eleva desde $0\text{ V}$ hacia valores positivos.
2. La tensión compuerta-fuente de $M_2$ es $V_{GS2} = V(b) - V_{n2} = V_{DD} - V_{n2}$.
3. En cuanto $V_{n2}$ alcanza $V_{DD} - V_{th2}$, el transistor $M_2$ entra en **corte**:
   $$V_{GS2} \le V_{th2} \implies I_{D2} \to 0$$
4. El efecto de cuerpo amplifica este corte, pues $V_{SB2} = V_{n2} > 0$ eleva el voltaje de umbral:
   $$V_{th2}(V_{SB}) = V_{th0} + \gamma (\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F})$$
5. Como consecuencia, el trasvase de carga se interrumpe antes de la equipotencialidad completa. **Por lo tanto, la caída real simulada $\Delta V_{sim}$ será estrictamente menor que la predicción analítica lineal $\Delta V_{pred}$**.

---

## 2. Actividad 1 — Potencia Dinámica y Frecuencia de Conmutación

### 2.1. Potencia Dinámica Teórica
Para una compuerta con nodo dinámico de capacitancia $C_{dyn} \approx C_L + C_{par} \approx 2.65\text{ fF}$, conmutando a $f = 500\text{ MHz}$ bajo $V_{DD} = 1.0\text{ V}$ con factor de actividad $\alpha = 1$:
$$P_{din,teor} = \alpha C_{dyn} V_{DD}^2 f = (1)(2.65 \times 10^{-15}\text{ F})(1.0\text{ V})^2 (500 \times 10^6\text{ Hz}) = 1.325\,\mu\text{W}$$

### 2.2. Paradoja de la Potencia con Entradas Estáticas en '1'
* En una NAND3 estática, si las entradas se mantienen fijas en $A=B=C=1$, la salida se mantiene estáticamente en $0\text{ V}$. No hay conmutación de carga en $C_L$, por lo que $P_{din,estat} = 0$ (solo disipa fuga estática $\sim\text{pW}$).
* En la NAND3 dinámica, aunque las entradas no cambien de '1', la señal de reloj $CLK$ conmuta periódicamente a 500 MHz:
  * En cada semiciclo de precarga ($CLK=0$), $M_p$ recarga $C_{dyn}$ desde 0 V hasta $V_{DD}$.
  * En cada semiciclo de evaluación ($CLK=1$), la PDN conduce y descarga $C_{dyn}$ desde $V_{DD}$ hasta 0 V.
  * Por tanto, el factor de actividad dinámico es **$\alpha = 1$ en todo momento**, consumiendo potencia dinámica completa en cada ciclo de reloj aunque el circuito no procese datos nuevos.

---

## 3. Actividad 3 — Fugas, Balance Nodal y Dependencia Térmica en 45nm HP

### 3.1. Conciliación de Capacitancias: Estática ($C_{nodo}$) vs Dinámica Aparente ($C_{\text{eff}}$ y $C_{\text{par}}$)

Existe una diferencia metodológica entre la capacitancia estimada teóricamente y la observada en el transitorio de retención:
1. **Estimación Analítica Estática ($C_{nodo} \approx 2.65\text{ fF}$):**  
   Calculada a partir de parámetros geométricos en régimen de pequeña señal e inversión plena:
   $$C_{nodo} = C_{ext} + C_{gd}(M_p) + C_{g}(inversor) + C_{diff}(D_p) + C_{diff}(D_1) \approx 2.0 + 0.015 + 0.279 + 0.119 + 0.237 \approx 2.65\text{ fF}$$
2. **Capacitancias Dinámicas Aparentes Inferidas ($C_{\text{eff}}$ y $C_{\text{par}}$):**  
   $C_L = 2.0\text{ fF}$ es el único parámetro capacitivo explícito del circuito, e $\langle I(C_L) \rangle$ es la variable de corriente integrada directamente del archivo RAW. En contraste, $C_{\text{eff}}$ y $C_{\text{par}}$ son parámetros aparentes inferidos del balance integral de cargas para cerrar formalmente la ley de corrientes. No se formula un "residuo experimental nulo (0.000 pA)" como validación independiente, dado que $C_{\text{par}} \equiv C_{\text{eff}} - C_L$ se despeja por definición.
   Los extremos temporales reales medidos en el transitorio RAW son:
   * **A $27^\circ\text{C}$:** $V_{dyn}(t_0 = 10.0\text{ ns}) = 1.023497\text{ V}$, $V_{dyn}(t_1 = 1000.520\text{ ns}) = 0.936959\text{ V} \implies \Delta V_{dyn} = -86.53768\text{ mV} \approx -86.538\text{ mV}$.
   * **A $85^\circ\text{C}$:** $V_{dyn}(t_0 = 10.0\text{ ns}) = 1.023977\text{ V}$, $V_{dyn}(t_1 = 1000.520\text{ ns}) = 0.830869\text{ V} \implies \Delta V_{dyn} = -193.10813\text{ mV} \approx -193.108\text{ mV}$.
   *(El ligero sobrepaso en $t_0$ por encima de $1.0\text{ V}$ responde al acoplamiento capacitivo de reloj / bootstrap al cortarse el PMOS de precarga; no debe asumirse artificialmente $V_{dyn}(t_0) = 1.000\text{ V}$)*.
   $$C_{\text{eff}} = \frac{\langle I_{\text{net,dev}} \rangle \cdot \Delta t}{|\Delta V_{dyn}|} = \begin{cases} \dfrac{191.021\text{ pA} \times 990.520\text{ ns}}{86.53768\text{ mV}} = 2.18645\text{ fF} \approx 2.1864\text{ fF} & (27^\circ\text{C}) \\[1em] \dfrac{425.281\text{ pA} \times 990.520\text{ ns}}{193.10813\text{ mV}} = 2.18142\text{ fF} & (85^\circ\text{C}) \end{cases}$$
3. **Comprobación Cuantitativa con $I(C_L)$ en RAW:**  
   La cuadratura numérica del archivo RAW entre los límites exactos de medición $t_0 = 10.000\text{ ns}$ y $t_1 = 1000.520\text{ ns}$ ($\Delta t = 990.520\text{ ns}$) con interpolación lineal en los extremos arroja:
   * A $27^\circ\text{C}$: $\langle I(C_L) \rangle = -174.732\text{ pA}$ (coincidente a 6 cifras con $2.0\text{ fF} \times \frac{-86.53768\text{ mV}}{990.520\text{ ns}} = -174.732\text{ pA}$). Suministra el $91.47\%$ de la corriente neta demandada por los dispositivos ($191.021\text{ pA}$).
   * A $85^\circ\text{C}$: $\langle I(C_L) \rangle = -389.913\text{ pA}$ (coincidente con $2.0\text{ fF} \times \frac{-193.10813\text{ mV}}{990.520\text{ ns}} = -389.913\text{ pA}$). Suministra el $91.68\%$ de la corriente neta ($425.281\text{ pA}$).
   * El remanente capacitivo demandado ($+16.289\text{ pA}$ a $27^\circ\text{C}$ y $+35.368\text{ pA}$ a $85^\circ\text{C}$) corresponde algebraicamente a la capacitancia parásita nodal dinámica aparente:
     $$C_{par,din} = C_{\text{eff}} - C_L = \begin{cases} 0.18645\text{ fF} & (27^\circ\text{C}) \\ 0.18142\text{ fF} & (85^\circ\text{C}) \end{cases}$$
4. **Fundamento Físico de la Discrepancia:**  
   La fórmula analítica sobrestima los parásitos ($0.65\text{ fF}$ vs $\approx 0.186\text{ fF}$) porque asume $C_g(inv) \approx W L C_{ox}$ en inversión fuerte. En retención, $V_{dyn} \approx 1.0\text{ V} \implies M_{pi}$ opera con $V_{GS} \approx 0\text{ V}$ (régimen de agotamiento/subumbral), donde su capacitancia de compuerta cae a la fracción de solapamiento ($C_{ov} \ll C_{ox}$). Asimismo, las capacidades de difusión $C_{diff}$ están polarizadas en reversa plena ($V_R = 1.0\text{ V}$), lo que atenúa la capacitancia de unión en $\approx 30\%$ por ensanchamiento de la zona de carga espacial.

---

### 3.2. Dependencia Térmica y Factores de Incremento

Se distinguen tres niveles analíticos y experimentales:
1. **Predicción Analítica BSIM4 Intrínseca:**  
   A partir del parámetro $k_{t1} = -0.11\text{ V}$ con $T_{nom} = 27^\circ\text{C} = 300.15\text{ K}$:
   $$\frac{\Delta V_{th}}{\Delta T} = \frac{k_{t1}}{T_{nom}} \approx -0.366\text{ mV}/^\circ\text{C} \implies \Delta V_{th}(85^\circ\text{C} - 27^\circ\text{C}) \approx -21.2\text{ mV}$$
   Frente a la regla heurística clásica de la literatura ($\approx -1.0\text{ mV}/^\circ\text{C} \implies \Delta V_{th} \approx -58\text{ mV}$), el modelo BSIM4 presenta un corrimiento intrínseco más suave.
2. **NMOS Aislado en Banco DC ($V_{GS}=0\text{ V}, V_{DS}=1.0\text{ V}$):**  
   * $V_{SB} = 0.0\text{ V}$: $I_D(27^\circ\text{C}) = 5.511\text{ nA}$, $I_D(85^\circ\text{C}) = 17.247\text{ nA} \implies \mathbf{3.13\times}$.
   * $V_{SB} = 0.3\text{ V}$: $I_D(27^\circ\text{C}) = 0.844\text{ nA}$, $I_D(85^\circ\text{C}) = 3.487\text{ nA} \implies \mathbf{4.13\times}$.
   * $V_{SB} = 0.6\text{ V}$: $I_D(27^\circ\text{C}) = 0.180\text{ nA}$, $I_D(85^\circ\text{C}) = 0.834\text{ nA} \implies \mathbf{4.63\times}$.
   *(Se retira formalmente el factor erróneo de 1.38x, originado por una transcripción defectuosa de la corriente terminal $I_S = -1.386 \times 10^{-10}\text{ A}$ a $V_{SB}=0.6\text{ V}$)*.
3. **Red Pull-Down Completa In Situ:**  
   La corriente promedio terminal de la PDN footed pasa de $\langle I_s(M_1) \rangle = 110.528\text{ pA}$ a $430.888\text{ pA}$, registrando un factor térmico terminal in situ de **$3.90\times$**. Este valor queda acotado dentro del rango $[3.13\times, 4.13\times]$ del dispositivo aislado, reflejando que los transistores internos de la pila apilada operan con potenciales de fuente-sustrato $V_{SB} \in [0.1\text{ V}, 0.25\text{ V}]$.

---

### 3.3. Investigación de GIDL por Ablación de Parámetros

Bajo las condiciones de retención ($V_{DD} = 1.0\text{ V}, V_{GS} = 0\text{ V}$):
* El ensayo ortogonal comparando el modelo canónico (`agidl = 2e-4`) frente al modelo de control ablativo (`agidl = 0.0`) arroja:
  $$\Delta I_D = I_D(\text{canónico}) - I_D(\text{nogidl}) = 0.000\text{ A}$$
  $$|\Delta I_B| \sim 2.5 \times 10^{-20}\text{ A}$$
* La variación no resulta significativamente resoluble frente al ruido de integración y punto flotante del simulador. Por tanto, no tiene impacto práctico en la pérdida de carga del nodo $dyn$, sin que esto implique afirmar un cero físico cuántico absoluto ni postular una cota universal que no pueda ser resuelta por el solver.

---

### 3.4. Balance Nodal de Corrientes Terminales en $dyn$

La ley de Kirchhoff de corrientes en el nodo $dyn$ en la ventana de retención ($10\text{ ns}$ a $1.00052\,\mu\text{s}$) se formula estrictamente con las corrientes terminales:
$$\langle I_s(M_1) \rangle + \langle I_d(M_p) \rangle + \langle I_g(M_{pi}) \rangle + \langle I_g(M_{ni}) \rangle + \langle I(C_L) \rangle + \langle I(C_{par}) \rangle = 0$$

* **Valores Promedio Canónicos:**
  * A $27^\circ\text{C}$: $I_s(M_1) = +110.53\text{ pA}$, $I_d(M_p) = -12.26\text{ pA}$, $I_g(M_{pi}) = +76.31\text{ pA}$, $I_g(M_{ni}) = +16.44\text{ pA}$.
  * A $85^\circ\text{C}$: $I_s(M_1) = +430.89\text{ pA}$, $I_d(M_p) = -56.08\text{ pA}$, $I_g(M_{pi}) = +49.86\text{ pA}$, $I_g(M_{ni}) = +0.61\text{ pA}$.
* **Partición de Ramas:**  
  La relación entre la corriente drenada por la PDN footed y la absorbida por las compuertas del inversor dominó antes de compensar la inyección de precarga ($M_p$) es:
  * A $27^\circ\text{C}$: PDN footed representa el **$54.4\%$** ($110.53\text{ pA}$ de $203.28\text{ pA}$) y las compuertas del inversor el **$45.6\%$** ($92.75\text{ pA}$).
  * A $85^\circ\text{C}$: PDN footed representa el **$89.5\%$** ($430.89\text{ pA}$ de $481.36\text{ pA}$) y las compuertas del inversor el **$10.5\%$** ($50.47\text{ pA}$).
* La corriente de compuerta de $M_1$ ($\approx -41.604\text{ pA}$) es suministrada por la entrada $a$ y cualquier componente de acoplamiento interno ya se encuentra integrada dentro de la corriente terminal $I_s(M_1)$, por lo que no se adiciona por duplicado al balance nodal.
