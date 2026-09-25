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

Se evalúa el barrido de carga $C_L \in [0.5, 1.0, 2.0, 4.0]\text{ fF}$ contrastando los modelos analíticos con el **Banco Síncrono Canónico de Referencia** (`nand3_cs_g2b_piloto_cl2f.cir`) y las series históricas (referencia: umbrales del inversor dominó: $V_M = 0.4797\text{ V}$, $V_{IH} = 0.5785\text{ V}$, $NM_H = 0.4215\text{ V}$, $\Delta V_{crit,M} = 0.5203\text{ V}$):

| $C_L$ (fF) | $\Delta V_{pred}$ (Guía) | $\Delta V_{pred}$ (Total) | $\Delta V_{\text{sinc}}$ (Ref. Síncrona) | $V_{dyn,min}$ (Sinc) | $\Delta V_{\text{Leo}}$ (Hist) | $\Delta V_{\text{Marco}}$ (Hist) | Margen Lógico ($V_{IH}=0.579\,\text{V}$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.5** | 529.15 mV | 467.34 mV | **364.85 mV** | **0.6351 V** | 175.92 mV | --- | Seguro ($V_{dyn} > V_{IH} + 56\,\text{mV}$) |
| **1.0** | 413.75 mV | 374.97 mV | **265.93 mV** | **0.7341 V** | 138.26 mV | --- | Seguro ($V_{dyn} > V_{IH} + 155\,\text{mV}$) |
| **2.0** | 288.09 mV | 268.74 mV | **164.29 mV** | **0.8357 V** | 101.03 mV | 176.57 mV | Seguro ($V_{dyn} > V_{IH} + 257\,\text{mV}$) |
| **4.0** | 179.23 mV | 171.54 mV | **92.60 mV** | **0.9074 V** | 67.62 mV | --- | Seguro ($V_{dyn} > V_{IH} + 328\,\text{mV}$) |

### Diagnóstico Físico y Trazabilidad Histórica:
* **Inmunidad lógica total:** En ningún caso del banco síncrono se produce conmutación espuria en la salida dominó ($V_{out,max} \le 15.6\text{ mV} \ll V_{IL} = 0.3675\text{ V}$).
* **Protección subumbral:** Si la redistribución hubiese seguido la fórmula ideal sin corte de umbral, para $C_L = 0.5\text{ fF}$ la caída predicha ($\Delta V_{pred} = 529.2\text{ mV}$) habría llevado $V(dyn)$ a $0.4708\text{ V} < V_M$, provocando un fallo lógico espurio masivo. El corte subumbral intrínseco de $M_2$ protege la integridad del circuito.
* **Trazabilidad:** El resultado histórico preliminar ($101.03\text{ mV}$ nominal para $C_L=2\text{ fF}$) procede de `nand3_cs_peor_caso_fisico.cir` y `nand3_cs_barrido_cl.cir` (`dv_eval_max: 0.101034 V`), donde las entradas $A$ y $B$ eran **anticipadas** (conmutaban en $[2.98, 3.00]\text{ ns}$, solapando $20\text{ ps}$ con precarga activa $CLK=0$). En el análisis de causalidad temporal, al contrastar dicha condición frente al banco síncrono canónico (`nand3_cs_g2b_piloto_cl2f.cir` / `nand3_cs_g2b_barrido_cl.cir`, conmutación en $[3.00, 3.02]\text{ ns}$ bajo idéntica topología y geometrías), la supresión de la precarga asistida explicó el incremento a $164.29\text{ mV}$ ($+63.26\text{ mV}$). Por su parte, la discrepancia residual de $12.28\text{ mV}$ frente al ensayo histórico alternativo ($176.5718\text{ mV}$ a $t=2.90\text{ ns}$, $C_L=2\text{ fF}$) coexiste con diferencias documentadas en los estados nodales previos (sesgo inicial en $n_2$ de $-160.8\text{ mV}$ vs $-126.8\text{ mV}$) e instantes de medición ($t=2.90\text{ ns}$ a $900\text{ ps}$ de evaluación frente al mínimo de ventana síncrona), corroborando ambas simulaciones el mismo régimen físico dominado por corte subumbral.

---

## 5. Evaluación Cuantitativa de Técnicas de Mitigación

Se implementaron y caracterizaron las técnicas de mitigación bajo la condición nominal del banco síncrono ($C_L = 2.0\text{ fF}$, $T_{clk} = 2\text{ ns}$, PTM 45 nm HP). Denominadores de área activa declarados: etapa dinámica base $W_{\text{dyn,base}} = 1215\text{ nm}$ ($A=0.0547\,\mu\text{m}^2$), celda completa base $W_{\text{celda,base}} = 1440\text{ nm}$ ($A=0.0648\,\mu\text{m}^2$).

| Configuración | Descripción | $\Delta V_{eval}$ / Extremo | $V_{dyn,min}$ | $V_{out,max}$ | Tiempo Rest. ($t_{rec}$) | Área Activa Extra | Sobrecarga Reloj |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Base Síncrono (Sin Mitigación)** | Ref. Síncrona | **164.29 mV** | 0.8357 V | 0.134 mV | Sin recup. en eval. | Base (5 dyn / 7 celda) | Base ($C_g \approx 0.50\,\text{fF}$) |
| **Mitigación 1a: Precarga $W=45\,$nm** | Precarga Interna | **$-50.47\,$mV** (overshoot) | 1.0505 V | 0.267 mV | Inmediato | +2 PMOS (+7.4% dyn) | $+0.1274\,$fF ($63.7\,$nW) |
| **Mitigación 1b: Precarga $W=135\,$nm**| Precarga Interna | **$-50.47\,$mV** (overshoot) | 1.0505 V | 0.267 mV | Inmediato | +2 PMOS (+22.2% dyn) | $+0.3821\,$fF ($191.1\,$nW) |
| **Mitigación 2: Reordenamiento C-B-A** | Reordenamiento | Vect A: $\le 0\,$ / Vect B: **164.3 mV** | 0.8357 V | 0.134 mV | Depende vector | **0 transistores** (0 nm) | **0 fF** (idéntica a base) |
| **Mitigación 2: Reordenamiento C-A-B** | Reordenamiento | Vect A: $\le 0\,$ / Vect B: **72.1 mV** | 0.9279 V | 0.134 mV | Depende vector | **0 transistores** (0 nm) | **0 fF** (idéntica a base) |
| **Mitigación 3: Keeper $W_{kp} = 45\,$nm** | Keeper PMOS | **69.68 mV** (droop inicial) | 0.9303 V | 0.356 mV | **92.92 ps** (desde mín) | +1 PMOS (+3.7% dyn) | 0 fF en $CLK$ |

### Análisis Detallado de Mecanismos Físicos:

1. **Precarga Interna ($W_p = 45\text{ nm}$ vs $135\text{ nm}$):**
   * Ambos anchos anulan la caída de tensión estática ($V_{dyn,min} = 1.0505\text{ V}$) en la ventana nominal de precarga ($1\text{ ns} \gg 5\tau$).
   * La variante de ancho mínimo ($45\text{ nm}$) reduce en un $66.7\%$ la sobrecarga capacitiva de compuerta sobre el reloj ($0.1274\text{ fF}$ vs $0.3821\text{ fF}$) y su disipación dinámica asociada ($63.69\text{ nW}$ vs $191.07\text{ nW}$ a $500\text{ MHz}$).
   * Ambas introducen un sobreimpulso de $+50.47\text{ mV}$ por acoplamiento capacitivo (*clock feedthrough*).
   * El nodo $n_3$ no se precarga porque el encendido inmediato del footer $M_f$ en evaluación disiparía innecesariamente $C_{n3} V_{DD}^2 f$ a tierra sin aportar protección lógica.
2. **Reordenamiento de Entradas en la PDN (Análisis de Vectores de Entrada):**
   * Bajo el Vector A ($A=B=1, C=0$), ubicar $C=0$ en el transistor superior (adyacente a $dyn$) aísla completamente los nodos internos, anulando el droop.
   * Sin embargo, bajo el Vector B ($A=0, B=C=1$), la topología C-B-A vuelve a conectar dos nodos internos descargados a $dyn$, sufriendo la misma caída del peor caso base ($164.29\text{ mV}$). La topología C-A-B acota la caída a $72.08\text{ mV}$ al colocar $A=0$ en el centro (aislando $n_2$). En los ensayos exploratorios preliminares (con entradas conmutando a $2.98\text{ ns}$), estas caídas fueron de $100.37\text{ mV}$ y $31.26\text{ mV}$.
   * Por tanto, el reordenamiento **no es universal** y acarrea compromisos de enrutamiento y capacitancias parásitas de cableado en layout.
3. **Keeper PMOS ($W_{kp} = 45\text{ nm}$) y Compromiso de Contención Dinámica:**
   * El inversor dominó de salida ya existe en la celda base, por lo que solo se añade un transistor PMOS ($\Delta W = +45\text{ nm}$, $+3.70\%$ en área activa dinámica).
   * Amortigua la caída transitoria a $69.68\text{ mV}$ ($V_{dyn,min} = 0.9303\text{ V}$ a $t=3.0271\text{ ns}$), restaura el nodo al $99\%$ de $V_{DD}$ en $92.92\text{ ps}$ tras el mínimo ($110.02\text{ ps}$ desde el cruce de $0.50\text{ V}$ del reloj; $120.02\text{ ps}$ desde inicio de rampa de reloj) y alcanza $0.9996\text{ V}$ ($99.96\%$ de $V_{DD}$) al final de la fase.
   * **Compromiso de contención dinámica:** Evaluando ambos retardos al $50\%$ de tensión ($V_{in}=0.5\text{ V} \to V_{dyn}=0.5\text{ V}$ y $V_{out}=0.5\text{ V}$):
     * $t_{pHL,dyn}$: pasa de $23.95\text{ ps}$ a $27.46\text{ ps}$ ($\Delta t = +3.51\text{ ps}$, penalización del **$+14.65\%$**).
     * $t_{pLH,out}$: pasa de $37.58\text{ ps}$ a $43.09\text{ ps}$ ($\Delta t = +5.52\text{ ps}$, penalización del **$+14.69\%$**).

---

## 6. Inventario de Figuras Generadas (300 DPI)

* [**`fig1_act2_peor_caso_formas_onda.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act2/figuras/fig1_act2_peor_caso_formas_onda.png): Formas de onda sincronizadas del peor caso (control, nodos internos, nodo dinámico y salida).
* [**`fig2_act2_dv_vs_cl_analitico_simulado.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act2/figuras/fig2_act2_dv_vs_cl_analitico_simulado.png): Curvas paramétricas de $\Delta V \text{ vs } C_L$ y $V_{dyn,min} \text{ vs } C_L$, mostrando el desajuste analítico/simulado y la delimitación de la zona lógica segura.
* [**`fig3_act2_comparacion_mitigaciones.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act2/figuras/fig3_act2_comparacion_mitigaciones.png): Comparación transitoria de las 3 mitigaciones en evaluación y cuantificación del compromiso de contención en velocidad.
