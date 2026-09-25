# Documentación Técnica — Actividad 4: Monotonicidad, Cascada Dominó y Skew de Reloj

**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
**Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — Facultad de Ingeniería Electrónica y Eléctrica (FIEE)  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Tecnología Base:** PTM 45nm High-Performance (HP), $V_{DD} = 1.0\,\text{V}$, $T = 27^\circ\text{C}$  
**Guía Oficial:** [`Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf`](file:///G:/Proyectos/MicroNano/Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf) (Sección 8, págs. 8–10)

---

## 1. Objetivos y Matriz de Requisitos

| ID Requisito | Tarea Guía LD2 | Enunciado Técnico | Archivos SPICE Asociados | Estado |
|:---:|:---:|:---|:---|:---:|
| **REQ-19** | §8.1 (Tareas 1–2) | Demostrar experimentalmente la violación de monotonicidad en cascada directa $dyn1 \to \text{PDN2}$ y la prevención de activación prematura mediante inversor estático dominó. | `Tarea 1 Sin Inversor.cir` (Histórico)<br>`Paso 2 y 3 Con Inversor.cir` (Histórico)<br>`a4_control1_bloqueo_inversor.cir` (Validado) | **COMPLETO** |
| **REQ-20** | §8.1 (Tarea 3) | Evaluar entrada externa $X$ con transición descendente ($1 \to 0$) durante evaluación activa; caracterizar el error lógico del ciclo de evaluación e implicancias para flip-flops de interfaz (TGFF). | `a4_control2_pulso_x_descendente.cir`<br>`a4_control3_x_estatico_cero.cir` (Validado) | **COMPLETO** |
| **REQ-21** | §8.2 (Tareas 1–3) | Caracterizar cascada dominó de 3 etapas Footed vs Unfooted bajo barrido de skew $T_{\text{skew}} \in [-50, 200]\,\text{ps}$; cuantificar $t_{\text{del}}$ y picos de corriente $I_{\text{pk}}$, y analizar la condición de temporización de Rabaey. | `Tarea 4 Footed.cir` (Histórico)<br>`Paso 5 Unfooted.cir` (Histórico)<br>`a4_control4_difusion_sensibilidad.cir` (Validado) | **COMPLETO** |

---

## 2. Sección 8.1: Regla de Monotonicidad y Estructura Dominó

### A. Cascada Directa Sin Inversor (Violación de Monotonicidad)
* **Netlist de Marco:** `G:\Proyectos\Micro\laboratorio4\Tarea 1 Sin Inversor.cir`
* **Estímulos:** $V_a = 1.0\,\text{V}$, $V_b = 1.0\,\text{V}$, $V_x = 1.0\,\text{V}$, $T_{clk} = 2.0\,\text{ns}$ ($500\,\text{MHz}$).
* **Resultado del LOG:**  
  $$\mathbf{V_{dyn2,\text{min}} = 0.64624\,\text{V}} \implies \Delta V = 1.00000 - 0.64624 = \mathbf{353.76\,\text{mV}}$$
* **Diagnóstico Físico:**  
  La etapa 1 tiene $A=B=1$, por lo que su salida final en evaluación es $dyn1 \to 0$. La segunda etapa calcula $dyn2 = \overline{dyn1 \cdot X} = \overline{0 \cdot 1} = 1$. Sin embargo, durante la fase previa de precarga ($CLK=0$), $dyn1$ se cargó a $V_{DD} = 1.0\,\text{V}$. Al llegar el flanco de evaluación ($CLK: 0 \to 1$), $dyn1$ tarda un retardo finito $t_{pHL1}$ en descargarse. Durante esa ventana inicial, la entrada de la etapa 2 está en nivel alto mientras $X=1$ y $CLK=1$, abriendo un camino de conducción transitorio a tierra que drena $353.76\,\text{mV}$ de $dyn2$. Cuando $dyn1$ cruza por debajo de $V_{thn}$, la PDN2 se corta, pero al ser un nodo dinámico sin recarga en evaluación ($M_{p2}$ apagado), la carga perdida **no se recupera dentro de ese ciclo**.
* **Impacto en Margen de Ruido:**  
  Con $V_M = 0.4797\,\text{V}$ y $V_{IH} = 0.5785\,\text{V}$, el margen de nivel alto nominal se degrada a $NM_H = 0.6462 - 0.5785 = \mathbf{67.7\,\text{mV}}$ (pérdida del **$84\%$** respecto a los $421.5\,\text{mV}$ nominales). En esta celda aislada bajo condiciones nominales (sin fuentes de ruido externas), dado que $0.6462\,\text{V} > V_M$, la compuerta receptora no llega a invertir su salida lógica, pero opera al límite del colapso funcional ante fluctuaciones térmicas o de alimentación.

---

### B. Prevención de Activación Prematura y Bloqueo con Inversor Estático Dominó

Para analizar el papel del inversor estático dominó se distinguen rigurosamente tres regímenes físicos y operativos:

1. **Prevención de Activación Prematura:**  
   Al insertar el inversor estático intermedio ($out1 = \overline{dyn1}$), durante la precarga ($dyn1=1$) la salida $out1$ se fija en $0\,\text{V}$. Cuando comienza la evaluación, $out1$ inicia en 0 y solo puede realizar una transición **monótona creciente ($0 \to 1$)** una vez que la etapa 1 ha evaluado. Esto garantiza que la PDN de la etapa 2 permanezca estrictamente apagada durante el vaciado inicial de $dyn1$, eliminando la conducción espuria previa.
2. **Descarga Funcional Legítima (Evidencia Histórica de Marco con $X=1$):**  
   En `Paso 2 y 3 Con Inversor.cir`, con $A=B=X=1$, la compuerta dominó evalúa la función booleana no inversora $out2 = out1 \cdot X = 1 \cdot 1 = 1$. En el nodo dinámico, esto exige $dyn2 \to 0\,\text{V}$. El LOG registra:
   $$V_{dyn2,\text{min}} = \mathbf{-0.00584\,\text{V}} \approx 0.00\,\text{V}$$
   Este resultado representa la conmutación activa correcta de la lógica dominó y **no constituye ninguna falla**.
3. **Bloqueo Correcto con $X=0$ (Control 1 de Validación):**  
   En `act4/circuitos/a4_control1_bloqueo_inversor.cir`, se evalúa la condición de bloqueo de la segunda etapa fijando $A=B=1$ (lo que conmuta $out1 \to 1$) y $X=0$. La función booleana esperada es $out2 = out1 \cdot X = 1 \cdot 0 = 0$, requiriendo que el nodo dinámico permanezca en nivel alto ($dyn2 = \overline{out1 \cdot X} = \overline{0} = 1$).
   * **Resultados en LOG:**
     - $V(dyn1)$ final de evaluación ($t=2.99\,\text{ns}$): $3.65\,\mu\text{V} \approx 0.00\,\text{V}$.
     - $V(out1)$ final de evaluación ($t=2.99\,\text{ns}$): $0.999999\,\text{V} \approx 1.00\,\text{V}$.
     - $V(dyn2)$ final de evaluación ($t=2.99\,\text{ns}$): $1.03894\,\text{V}$ (nodo dinámico intacto, con sobreimpulso de reloj).
     - $V(out2)$ final de evaluación ($t=2.99\,\text{ns}$): $26.8\,\text{nV} \approx 0.00\,\text{V}$.
     - **Mínimo absoluto de $V(dyn2)$ en evaluación:** $\mathbf{0.999999\,\text{V}}$ ($\Delta V = 0.77\,\mu\text{V} \approx \mathbf{0.000\,\text{mV}}$).

> **Aclaración Metodológica:**  
> El Control 1 demuestra el bloqueo correcto de la segunda etapa y la preservación del nivel alto en $dyn2$. No debe presentarse como una "reducción cuantitativa del 100% de la caída de 353 mV por comparación directa", ya que el circuito sin inversor operaba con $X=1$ y entradas opuestas, mientras que el Control 1 opera con $X=0$.

---

### C. Error Lógico por Entrada Externa $X$ No Monótona (Control 2 y Control 3)

* **Netlists Evaluados:**  
  - Control 2: `act4/circuitos/a4_control2_pulso_x_descendente.cir` ($X: 1 \to 0$ a mitad de evaluación, $t = 2.50\,\text{ns}$).
  - Control 3: `act4/circuitos/a4_control3_x_estatico_cero.cir` ($X = 0$ estático de referencia).
* **Comparativa Cuantitativa Directa:**

| Variable / Parámetro | Control 3 ($X=0$ Estático) | Control 2 ($X: 1 \to 0$ a $t=2.50\,\text{ns}$) | Comportamiento Físico Demostrado |
|:---|:---:|:---:|:---|
| $V(clk)$ a $t=2.50\,\text{ns}$ | $1.000\,\text{V}$ | $1.000\,\text{V}$ | Fase activa de evaluación ($CLK=1$) |
| $V(x)$ antes de $2.50\,\text{ns}$ | $0.000\,\text{V}$ | $1.000\,\text{V}$ | En Control 2, $X=1$ habilitó la PDN2 al inicio |
| $V(x)$ final ($t=2.99\,\text{ns}$) | $0.000\,\text{V}$ | $0.000\,\text{V}$ | Ambos circuitos terminan con vector $(out1=1, X=0)$ |
| $V(dyn2)$ antes ($t=2.49\,\text{ns}$) | $\mathbf{1.0410\,\text{V}}$ | $\mathbf{3.66\,\mu\text{V}}$ | La descarga en Control 2 ocurrió ANTES de la caída de $X$ |
| $V(dyn2)$ final ($t=2.99\,\text{ns}$) | $\mathbf{1.0389\,\text{V}}$ | $\mathbf{-0.0265\,\text{V}}$ | Imposibilidad de recargar en evaluación ($M_{p2}$ cortado) |
| $V(out2)$ final ($t=2.99\,\text{ns}$) | $\mathbf{26.8\,\text{nV} \approx 0.0\,\text{V}}$ | $\mathbf{0.999997\,\text{V} \approx 1.0\,\text{V}}$ | **Error lógico durante el ciclo de evaluación** |
| $dyn2$ y $out2$ esperados | $dyn2=1,\; out2=0$ | $dyn2=1,\; out2=0$ | Para $out1=1, X=0$: $dyn2 = \overline{1 \cdot 0} = 1 \implies out2 = 1 \cdot 0 = 0$ |
| $dyn2$ y $out2$ obtenidos | $dyn2=1,\; out2=0$ (ÉXITO) | $dyn2 \approx 0,\; out2 \approx 1$ (**ERROR**) | Salida complementaria errónea durante el ciclo |

* **Secuencia Causal del Fenómeno:**
  1. **Descarga Previa a la Transición:** Entre $t=2.00\,\text{ns}$ y $t=2.50\,\text{ns}$, $CLK=1$, $out1=1$ y $X=1$. La PDN de la etapa 2 conduce activamente y drena la carga de $dyn2$ a tierra en menos de $60\,\text{ps}$ ($V_{dyn2} \to 0\,\text{V}$).
  2. **Transición Descendente Externa:** A $t=2.50\,\text{ns}$, la entrada $X$ cae a $0\,\text{V}$, cortando el transistor NMOS inferior.
  3. **Aislamiento Dinámico sin Recarga:** La compuerta dominó se encuentra en evaluación ($CLK=1$), por lo que el PMOS de precarga $M_{p2}$ permanece cortado. No existe camino de conducción hacia $V_{DD}$ para reponer la carga en $dyn2$.
  4. **Error Lógico en el Ciclo:** El inversor de salida detecta $dyn2 \approx 0\,\text{V}$ y mantiene $out2 \approx 1.0\,\text{V}$ durante el resto de la fase de evaluación, en discrepancia con la función lógica requerida ($out2 = 1 \cdot 0 = 0$).

> **Precisiones Terminológicas:**  
> - El fenómeno debe definirse como un **error lógico de la segunda etapa durante el ciclo de evaluación por imposibilidad de recuperar carga después de que $X$ desciende**.  
> - No debe denominarse "bit flip de memoria" (no es una celda biestable de almacenamiento estático ni un cerrojo).  
> - No constituye una falla permanente más allá del ciclo de evaluación: en el siguiente semiciclo de precarga ($CLK=0$), el PMOS conducirá y restaurará $dyn2$ a $V_{DD}$.
> - **Implicancia para Flip-Flops de Interfaz:** Toda entrada externa a un bloque dominó debe provenir de biestables libres de glitches cuya salida sea estrictamente monótona creciente o estable durante la ventana de evaluación (por ejemplo, biestables de compuerta de transmisión, TGFF, sincronizados).

---

## 3. Sección 8.2: Cascada Dominó de 3 Etapas (Footed vs Unfooted)

### A. Matriz Homóloga Completa de Skew ($T_{\text{skew}} \in [-50, 200]\,\text{ps}$)

Datos extraídos directamente de [`Tarea 4 Footed.log`](file:///G:/Proyectos/Micro/laboratorio4/Tarea 4 Footed.log) y [`Paso 5 Unfooted.log`](file:///G:/Proyectos/Micro/laboratorio4/Paso 5 Unfooted.log):

| $T_{\text{skew}}$ (ps) | Retardo Footed ($t_{\text{del}}$) | Retardo Unfooted ($t_{\text{del}}$) | Ahorro Retardo ($\Delta t$) | $I_{\text{pk}}$ Footed ($\mu\text{A}$) | $I_{\text{pk}}$ Unfooted ($\mu\text{A}$) | $\Delta I_{\text{pk}}$ Unfooted | Comportamiento Dinámico Dominante |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **$-50$** | $77.20\,\text{ps}$ | $66.46\,\text{ps}$ | $-10.74\,\text{ps}$ ($-13.9\%$) | $113.80$ | $326.30$ | $+212.50\,\mu\text{A}$ | Precarga adelantada en etapas posteriores coincide con entradas en alto. |
| **$0$** | $77.21\,\text{ps}$ | $66.47\,\text{ps}$ | $-10.74\,\text{ps}$ ($-13.9\%$) | $318.85$ | $332.91$ | $+14.06\,\mu\text{A}$ | Conmutación síncrona: las 3 etapas precargan simultáneamente en paralelo. |
| **$+50$** | $125.47\,\text{ps}$ | $95.12\,\text{ps}$ | $-30.35\,\text{ps}$ ($-24.2\%$) | $110.56$ | $110.57$ | $+0.01\,\mu\text{A}$ | Desacoplo temporal de picos de precarga; corrientes pico esencialmente iguales. |
| **$+100$** | $226.68\,\text{ps}$ | $130.81\,\text{ps}$ | $-95.87\,\text{ps}$ ($-42.3\%$) | $110.56$ | $160.57$ | $+50.01\,\mu\text{A}$ | Aparición de incremento de corriente de alimentación en unfooted. |
| **$+200$** | $426.91\,\text{ps}$ | $171.48\,\text{ps}$ | $-255.43\,\text{ps}$ ($-59.8\%$) | $110.56$ | $214.63$ | $+104.07\,\mu\text{A}$ | Elevación notable de pico de alimentación en unfooted ($+94.1\%$ sobre footed). |

---

### B. Análisis Físico de la Corriente de Pico de Alimentación ($I_{\text{pk}}$)

1. **Definición de Medición:**  
   $I_{\text{pk}}$ se midió mediante `.meas TRAN Ipk MAX -I(Vdd) FROM={Tbase} TO={Tbase+Tclk*2}` ($t \in [0.5, 4.5]\,\text{ns}$). Representa el valor máximo instantáneo en módulo de la corriente total provista por la fuente de alimentación, integrando corrientes capacitivas de carga, corrientes de subumbral/fuga y posibles caminos resistivos de cortocircuito durante las transiciones.
2. **Naturaleza del Incremento de $104.07\,\mu\text{A}$ a $+200\,\text{ps}$:**  
   $$\Delta I_{\text{pk}} = I_{\text{pk,unfooted}}(200\,\text{ps}) - I_{\text{pk,footed}}(200\,\text{ps}) = 214.63\,\mu\text{A} - 110.56\,\mu\text{A} = \mathbf{104.07\,\mu\text{A}}$$
   Esta magnitud es una **diferencia de picos de corriente de alimentación** entre ambas topologías. En la compuerta unfooted, cuando la etapa $i$ inicia la precarga mientras la etapa anterior $i-1$ aún sostiene un nivel alto en la entrada de la PDN, existe una conducción simultánea entre el PMOS de precarga y la PDN conectada a tierra. Sin embargo, no debe etiquetarse como "corriente pura de cortocircuito aislada", ni puede afirmarse experimentalmente que $I_{\text{sc,footed}} = 0$ como una medición directa de canal independiente, pues la simulación no aísla las ramas internas de corriente.
3. **Restricción Energética:**  
   $I_{\text{pk}}$ es un valor pico instantáneo; no es representativo de la energía o potencia promedio disipada sin realizar la integral temporal $\int -I(V_{DD}) V_{DD}\,dt$ en el ciclo.

---

### C. Análisis de la Condición de Temporización de Rabaey

* **Enunciado de la Guía y Marco Teórico de Rabaey:**  
  La guía oficial cita a Jan M. Rabaey (*Digital Integrated Circuits*), quien establece que la omisión del transistor footer en etapas dominó es admisible si el retardo de propagación de la señal de precarga de la etapa previa extingue la conducción en la PDN antes de que la etapa receptora sufra una disipación excesiva por cortocircuito.
* **Evaluación Crítica de los Resultados Experimentales:**
  - En las netlists simuladas (`Tarea 4 Footed.cir` y `Paso 5 Unfooted.cir`), solo se midió el retardo extremo a extremo ($t_{\text{del}}$) y el pico global $I_{\text{pk}}$. **No se realizaron mediciones individuales de los retardos por etapa ($t_{p,\text{inv}}$ ni $t_{pHL,\text{dyn}}$)**.
  - Por consiguiente, **no debe presentarse $T_{\text{skew,max}} = 50\,\text{ps}$ como una frontera experimental exacta**.
  - La evidencia experimental disponible demuestra que:
    1. A $T_{\text{skew}} = +50\,\text{ps}$, el pico de corriente de alimentación en unfooted ($110.57\,\mu\text{A}$) es prácticamente idéntico al de footed ($110.56\,\mu\text{A}$).
    2. A $T_{\text{skew}} = +100\,\text{ps}$ y $+200\,\text{ps}$, la corriente de alimentación en unfooted se incrementa notablemente ($160.57\,\mu\text{A}$ y $214.63\,\mu\text{A}$).
    3. A $T_{\text{skew}} = -50\,\text{ps}$, unfooted también presenta un pico de corriente muy elevado ($326.30\,\mu\text{A}$ vs $113.80\,\mu\text{A}$ en footed), lo que comprueba que un adelanto de fase del reloj también genera severa superposición de conducción.
  - **Conclusión Sustentable:** La condición admisible para eliminar el footer está regida por la **secuencia temporal relativa de precarga y evaluación entre etapas consecutivas**, requiriendo un control estricto de la temporización en ambas direcciones (evitando tanto desfases positivos excesivos como desalineamientos negativos).

---

## 4. Sensibilidad a Parámetros de Difusión (Control 4)

### A. Auditoría Línea por Línea (`Tarea 4 Footed.cir` vs `a4_control4_difusion_sensibilidad.cir`)

| Parámetro / Condición | `Tarea 4 Footed.cir` (Histórico) | `a4_control4_difusion_sensibilidad.cir` (Validado) | Estado de Homología |
|:---|:---|:---|:---:|
| Modelo SPICE | `45nm_HP.pm` | `../../modelos/ptm45hp.lib` (envoltorio de `45nm_HP.pm`) | **Homólogo** |
| Topología circuital | Cascada dominó de 3 etapas Footed | Cascada dominó de 3 etapas Footed | **Homólogo** |
| Geometrías ($W/L$) | $W_n=90\,\text{nm}, W_p=135\,\text{nm}, W_{\text{PDN}}=180\,\text{nm}, L_n=45\,\text{nm}$ | Idénticas dimensiones de canal en todos los transistores | **Homólogo** |
| Capacitancia de carga | $C_1 = C_2 = C_3 = 2.0\,\text{fF}$ | $C_1 = C_2 = C_3 = 2.0\,\text{fF}$ | **Homólogo** |
| Temperatura | $27^\circ\text{C}$ (`.temp 27`) | $27^\circ\text{C}$ (`.temp 27`) | **Homólogo** |
| Reloj ($CLK$) | $V_{DD}=1.0\,\text{V}, T_{clk}=2.0\,\text{ns}, t_r=t_f=20\,\text{ps}, T_{\text{skew}}=0\,\text{ps}$ | Idéntica configuración de fuentes PULSE | **Homólogo** |
| Entradas lógicas | $V_a = V_b = 1.0\,\text{V}$ | $V_a = V_b = 1.0\,\text{V}$ | **Homólogo** |
| Opciones del solver | `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear` | Idénticas tolerancias numéricas y algoritmo | **Homólogo** |
| Definición de retardo | TRIG $V(clk1)=0.5$ RISE=2 TARG $V(out3)=0.5$ RISE=2 | TRIG $V(clk1)=0.5$ RISE=2 TARG $V(out3)=0.5$ RISE=2 | **Homólogo** |
| Ventana de $I_{\text{pk}}$ | `MAX -I(Vdd) FROM 5e-10 TO 4.5e-09` | `MAX -I(Vdd) FROM 5e-10 TO 4.5e-09` | **Homólogo** |
| Parámetros de difusión | **Ausentes** (por defecto de BSIM4) | **Explícitos:** $AS, AD, PS, PD$ ($L_{\text{diff}}=90\,\text{nm}$) | **Variable de Control** |

### B. Resultados Cuantitativos del Control de Difusión
* Retardo extremo a extremo sin difusión explícita: $t_{\text{del}} = \mathbf{77.21\,\text{ps}}$.
* Retardo extremo a extremo con difusión explícita: $t_{\text{del}} = \mathbf{89.90\,\text{ps}}$ ($\Delta t = \mathbf{+12.69\,\text{ps}}$, **$+16.43\%$**).
* Corriente pico de alimentación: $I_{\text{pk}} = 318.85\,\mu\text{A}$ vs $312.66\,\mu\text{A}$ (variación menor al $-2\%$).

> **Conclusiones Respaldadas:**  
> - El incremento de retardo del $16.4\%$ cuantifica el impacto global de las capacitancias parásitas de unión en la cascada footed bajo este control específico.  
> - No debe afirmarse un incremento exacto de $4.23\,\text{ps}$ por etapa sin contar con mediciones individuales por nodo.  
> - Este resultado no debe extrapolarse a la tolerancia de skew de compuertas unfooted.

---

## 5. Inventario de Archivos y Evidencia Primaria

* **Netlists Reutilizados de Marco (en `laboratorio4/`):**
  - `Tarea 1 Sin Inversor.cir` / `.log`
  - `Paso 2 y 3 Con Inversor.cir` / `.log`
  - `Tarea 4 Footed.cir` / `.log`
  - `Paso 5 Unfooted.cir` / `.log`
* **Nuevos Controles Experimentales (en `act4/circuitos/` y `act4/resultados/`):**
  - `a4_control1_bloqueo_inversor.cir` / `.log` / `.raw`
  - `a4_control2_pulso_x_descendente.cir` / `.log` / `.raw`
  - `a4_control3_x_estatico_cero.cir` / `.log` / `.raw`
  - `a4_control4_difusion_sensibilidad.cir` / `.log` / `.raw`
  - `act4/resultados/datos/act4_metricas.json`
* **Documentación Técnica y Guía:**
  - `act4/README_act4.md`
  - `act4/guia_seccion8.txt` y `act4/guia_seccion8_p9.txt`
