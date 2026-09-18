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
