# Criterios de Medición y Protocolo Numérico — Actividad 3
**Fugas y Dimensionamiento del Transistor Keeper (45nm HP vs LP, 130nm Bulk; 27°C vs 85°C)**  
**Curso:** Microelectrónica y Sistemas Nanoelectrónicos — FIEE UNMSM (2026-II)  
**Docente:** MsC. Luz Adanaqué Infante  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Estado:** PROTOCOLO METODOLÓGICO CONGELADO PREVIO A SIMULACIÓN

---

## 1. Opciones del Solver y Configuración Numérica

Para todos los netlists de la Actividad 3, es mandatorio incluir en el bloque de opciones:
```spice
.options gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear
```
### Justificación Técnica en Medición de Fugas
* **`gmin = 1e-15` (1 fS):** Con $V_{DD} = 1.1\,\text{V}$ (45nm LP), la conductancia estándar por defecto de LTspice (`1e-12`, 1 pS) inyectaría una fuga espuria artificial a masa de $I_{gmin} = 1.1\,\text{pA}$. Dado que en 45nm LP a 27°C las fugas subumbral reales se sitúan en el orden de picoamperios, la conductancia por defecto falsearía los resultados en más del $10\%$. Fijar `gmin = 1e-15` reduce esta fuga artificial a $1.1\,\text{aA}$ ($1.1 \times 10^{-18}\,\text{A}$), garantizando que se mida la física del semiconductor y no el simulador.
* **`abstol = 1e-14` (10 fA) y `reltol = 1e-4`:** Evita oscilaciones numéricas espurias en transitorios lentos de descarga de compuertas flotantes ($1.0\,\mu\text{s}$).
* **`method = gear`:** Amortigua el falso ringing numérico del integrador trapezoidal ante capacitancias nodales en femtofaradios.

---

## 2. Protocolo de Extracción Desacoplado para Retención ($t_{hold}$)

Ante la consulta formal **PENDIENTE-DOCENTE-02** sobre la definición oficial de $t_{hold}$, todo netlist de retención transitoria transcurrirá durante $T_{stop} = 1.0\,\mu\text{s}$ con directivas `.meas` independientes para cada hipótesis métrica:

```spice
* 1. Tension residual final al agotar la ventana de 1 us
.meas TRAN vdyn_end_1us FIND V(dyn) AT=1.0u

* 2. Cruce de umbral de 90% de VDD (Criterio de retencion segura)
.meas TRAN t_cross_0p9vdd WHEN V(dyn)={0.90*VDD} FALL=1

* 3. Cruce de VDD/2 (Criterio estatico clasico)
.meas TRAN t_cross_vdd2 WHEN V(dyn)={0.50*VDD} FALL=1

* 4. Cruce de VM calibrado (Criterio dinamico de conmutacion con VM especifico del proceso y temperatura)
.meas TRAN t_cross_vm WHEN V(dyn)={VM_proc_T} FALL=1

* 5. Derivada inicial de caida del nodo dinamico (evaluada tras extinguirse el feedthrough a 10 ns)
.meas TRAN dvd_dt DERIV V(dyn) AT=10n
.meas TRAN inet_dyn_init PARAM {-Cdyn_tot*dvd_dt}
```

### Reglas de Tratamiento de Datos, Tiempos y Censura Temporal
1. **Diferenciación entre Tiempo Absoluto y Tiempo de Retención:**  
   El tiempo absoluto de cruce $t_{cross}$ medido por `WHEN` incluye la fase de precarga inicial ($t < t_{eval\_start}$). El tiempo de retención real efectivo es el tiempo transcurrido desde el inicio de la evaluación:
   $$t_{hold} = t_{cross} - t_{eval\_start}$$
   Se reportarán ambos valores para garantizar máxima trazabilidad.
2. **Calibración Obligatoria de $V_M(proc, T)$:**  
   El umbral $V_M$ de conmutación estática del inversor dominó depende de la tecnología y de la temperatura. Queda terminantemente prohibido reutilizar el valor $0.4797\,\text{V}$ (obtenido a 45nm HP / 27°C) para 85°C, 45 LP o 130nm. Cada combinación $\{ \text{tecnología, temperatura} \}$ contará con su valor específico calibrado previo.
3. **Detección de No Cruce (`Measurement FAIL`) y Censura:**  
   Si la tensión $V(dyn)$ no desciende hasta el umbral en la ventana de $1\,\mu\text{s}$, LTspice reportará `Measurement FAIL`.
   * En archivos JSON estructurados, los campos `t_cross_*` y `t_hold_*` registrarán estrictamente `null` (None en Python).
   * En tablas y textos de presentación científica, se etiquetarán explícitamente como **`> 1.0 µs (Censurado)`**.
   * **Prohibición:** Queda terminantemente prohibido sustituir los valores no alcanzados por infinito ($\infty$), por $0\,\text{s}$, o por valores numéricos inventados.

---

## 3. Protocolo de Aislamiento de Corrientes de Fuga

### A. Corriente Suministrada por la Fuente (`Vdd`)
```spice
.meas TRAN isupply_avg AVG -I(Vdd) FROM=10n TO=1.0u
.meas TRAN isupply_max MAX -I(Vdd) FROM=10n TO=1.0u
```
* **Signo Físico:** Se antepone el signo negativo a `I(Vdd)` conforme a la convención receptora de LTspice, extrayendo la corriente que **sale** de la fuente hacia el circuito.
* **Advertencia Metodológica Fundamental:** $I_{\text{supply}}$ alimenta conjuntamente la compuerta dinámica, el transistor keeper y el inversor dominó de salida ($M_{pi}, M_{ni}$). No debe confundirse bajo ningún concepto con la fuga neta que descarga el nodo `dyn`:
  $$I_{\text{supply}} \neq I_{\text{leak,tot}}$$

### B. Corriente Neta del Nodo Dinámico vs Corriente de Reposición del Keeper
El balance capacitivo del nodo `dyn` obedece a:
$$I_{net}(dyn)(t) = - C_{dyn}(V_{dyn}) \frac{dV(dyn)}{dt} = I_{\text{descarga}} - I_{\text{reposición}}$$
donde:
* $I_{\text{reposición}} = I_D(M_k)$ es la corriente suministrada activamente por el keeper.
* $I_{\text{descarga}}$ es la suma de corrientes de fuga que extraen carga del nodo (PDN, precarga, inversor).
* **Precaución Crítica:** Cuando $W_{kp} > 0$, el keeper inyecta carga para compensar las pérdidas. En esa condición, la corriente neta $-C_{dyn} \frac{dV}{dt}$ es el remanente no compensado ($I_{\text{descarga}} - I_{kp}$), y **no puede identificarse como la corriente física de fuga**.
* **Distinción Rigurosa Sin Keeper vs $W_{kp} = 1\,\text{nm}$:**  
  La condición "Sin Keeper" se modela eliminando la instancia $M_k$. Una aproximación con $W_{kp} = 1\,\text{nm}$ introduce capacitancias parásitas de difusión/compuerta y opera en un régimen de extrapolación no validado físicamente en BSIM4 45nm ($W \ll W_{min}$). No deben tratarse como físicamente equivalentes.
* **Comprobación Empírica del Signo de $I_{kp}$:**  
  La sonda de terminal de LTspice para el drenaje de $M_k$ mide con convención de corriente entrante al terminal. Dado que el keeper inyecta corriente hacia $dyn$ desde su drenaje (corriente saliente), la corriente neta inyectada $I_{kp,\text{inyectada}}$ debe definirse a partir del signo observado empíricamente en simulación ($I_{kp,\text{inyectada}} = -I_D(M_k)$ si la corriente saliente se registra como negativa).
* **Condición de Validez para $I_{\text{leak,tot}} \approx -C_{nodo} \frac{dV}{dt}$:**  
  Solo se aplicará esta aproximación bajo las siguientes hipótesis explícitas:
  1. $W_{kp} \to 0$ ($W_{kp} = 1\,\text{nm}$ o keeper ausente), garantizando $I_{kp} \to 0$;
  2. Evaluación inicial en $t = 10\,\text{ns}$ tras amortiguarse el transitorio de conmutación de reloj e inyección de carga;
  3. Estimación precisa de la capacitancia nodal efectiva $C_{dyn} = C_L + C_{par,dyn}$.

### C. Medición Directa In Situ de Terminales en LTspice
Para superar las limitaciones de los balances netos, se deben registrar las corrientes de terminal de cada dispositivo individualmente durante la simulación `.tran` de retención usando la sintaxis nativa de LTspice para primitivos (`Is`, `Id`, `Ig`, `Ib`):
```spice
* Corrientes de terminal in situ en la celda completa
.meas TRAN is_m1_avg  AVG Is(M1) FROM=10n TO=1.00052u   ; Terminal Source conectado a dyn
.meas TRAN id_mp_avg  AVG Id(Mp) FROM=10n TO=1.00052u   ; Terminal Drain conectado a dyn
.meas TRAN id_mk_avg  AVG Id(Mk) FROM=10n TO=1.00052u   ; Terminal Drain conectado a dyn (saliente < 0)
.meas TRAN ikp_inj    PARAM {-id_mk_avg}                 ; Corriente inyectada por el keeper (> 0)
.meas TRAN ig_inv_n   AVG Ig(Mni) FROM=10n TO=1.00052u  ; Terminal Gate conectado a dyn
.meas TRAN ig_inv_p   AVG Ig(Mpi) FROM=10n TO=1.00052u  ; Terminal Gate conectado a dyn
.meas TRAN i_cl_avg   AVG I(CL) FROM=10n TO=1.00052u    ; Corriente capacitiva externa
```

### D. Conclusiones y Limitaciones de la Auditoría Eléctrica (A3.1.1)
1. **Caso Sin Keeper (Piloto A):**  
   El balance nodal presenta un residual instantáneo positivo de $+13.1\text{ a }+18.3\,\text{pA}$ ($I_{\text{residual}} = Is(M1) + Id(Mp) + I_{\text{inv}} + I(CL)$). Este remanente permite estimar una capacitancia parásita nodal equivalente de $C_{par,dyn} \approx 0.19\,\text{fF}$, pero **no constituye una medición experimental independiente** de dicha capacitancia. La separación microscópica de componentes conserva esta limitación documental.
2. **Caso Con Keeper (Piloto B):**  
   El balance nodal instantáneo arroja un residual que varía en el tiempo: $+0.77\,\text{pA}$ (a $10\,\text{ns}$), $+5.36\,\text{pA}$ (a $100\,\text{ns}$), $+2.10\,\text{pA}$ (a $500\,\text{ns}$) y $+0.26\,\text{pA}$ (a $900\,\text{ns}$). No debe declararse un "error inferior al 0.1% cerrado al 100%", sino documentar el residual instantáneo exacto.
3. **Corriente Global de Alimentación ($I_{\text{supply}}$):**  
   El incremento de $I_{\text{supply}}$ en la celda sin keeper a medida que $V(dyn)$ cae (de $301\,\text{pA}$ a $2.6\,\text{nA}$) se interpreta como una **hipótesis físicamente plausible** de corriente de cortocircuito (crowbar) en el inversor dominó debido a la conducción subumbral incipiente de $M_{pi}$, hasta contar con mediciones dedicadas de rama en $M_{pi}/M_{ni}$. No debe confundirse la corriente de alimentación con la fuga del nodo dinámico.

### E. Caracterización Mediante Ensayos DC Auxiliares
Para desglosar los mecanismos físicos (subumbral, túnel de compuerta, GIDL) conforme a REQ-14 y REQ-15, se emplean ensayos DC dedicados de dispositivos individuales:
1. **Fuga Subumbral ($I_{sub}$):** NMOS unitario de ancho $3W_n = 270\,\text{nm}$ polarizado con $V_{GS} = 0$, $V_{SB} = 0$, barriendo $V_{DS} \in [0, V_{DD}]$.  
   *Nota Metodológica:* En la PDN real, el apilamiento de 4 transistores introduce un efecto de cuerpo ($V_{SB} > 0$ en $M_1, M_2, M_3$) que reduce la corriente subumbral respecto al transistor unitario aislado (stack effect).
2. **Fuga de Túnel de Compuerta ($I_{gate}$):** Medición de corriente de compuerta en terminal aislado con $V_{GD} = -V_{DD}$ o $V_{GS} = V_{DD}$.
3. **Fuga GIDL ($I_{gidl}$):** Extracción de la corriente de drenaje a altos campos reversos compuerta-drenaje.
* **Principio de Integridad:** Un ensayo auxiliar de un transistor aislado proporciona cotas y curvas constitutivas de referencia, pero no reemplaza la medición in situ de la red completa.

### F. Precisiones Epistemológicas y Correcciones de Retención Tri-Nodo (A3.4)
1. **Fallo de Criterio de Retención vs Error Lógico en Salida:**  
   Incumplir la condición $V_{dyn}(1\,\mu\text{s}) > 0.90 V_{DD}$ significa estrictamente **fallar el criterio de retención segura** normado por la guía. Esto **no equivale necesariamente a un error lógico** en la salida `out`. La salida solo conmuta al estado erróneo si $V_{dyn}$ desciende por debajo del umbral de conmutación estática $V_M$ del inversor dominó; mientras $V_M < V_{dyn} < 0.90 V_{DD}$, la salida lógica permanece en nivel bajo (`0`), conservando margen de ruido pero violando la especificación de diseño dinámico.
2. **Dominio Discreto de Validación de $W_{kp}$ vs Continuidad:**  
   No debe afirmarse que "cualquier ancho $W_{kp}$ con $W_{eff} > 0$ satisface retención". Las simulaciones físicas solo han validado puntos discretos específicos ($10.5\,\text{nm}, 11\text{--}15\,\text{nm}, 30\,\text{nm}, \dots, 390\,\text{nm}$). Cualquier interpolación continua en el dominio intermedio es una hipótesis que requiere confirmación.
3. **Ausencia de Reglas DRC Fabricables en Modelos Académicos PTM:**  
   Los modelos BSIM4 submicrométricos de la plataforma PTM son parametrizaciones predictivas académicas que carecen de manual de reglas de diseño de layout (DRC) de fundición comercial asociada. Por ello, no deben invocarse reglas DRC de fabricación que no estén formalmente documentadas en las librerías, distinguiendo siempre ancho nominal de nodo ($45\,\text{nm}$), ancho dibujado ($W_{drawn}$) y ancho efectivo matemático del modelo ($W_{eff} = W - 2 W_{int}$).
4. **Naturaleza Terminal de $I_s(M_1)$:**  
   La corriente `Is(M1)` extraída de LTspice es la **corriente terminal total** que entra por el Source de $M_1$ desde el nodo $dyn$. Esta incluye la corriente de canal subumbral, pero también desplazamientos capacitivos ($C_{gd}, C_{gs}$), corrientes túnel de compuerta y mecanismos GIDL. No debe identificarse de forma reduccionista como "fuga subumbral pura aislada".
5. **Feedthrough Capacitivo y Elevación Inicial de $V_{dyn}$:**  
   El incremento de tensión inicial por encima de la fuente ($V_{dyn}(t_0^+) > V_{DD}$), observado prominentemente en LP ($1.13\,\text{V}$ vs $1.1\,\text{V}$) y 130nm ($1.39\,\text{V}$ vs $1.3\,\text{V}$), no representa generación de carga interna ni violación física de conservación de energía, sino **acoplamiento capacitivo (feedthrough)** a través de las capacidades de solapamiento compuerta-drenaje ($C_{gd}$) de $M_p$ y $M_1$ durante el flanco de subida de $CLK$ ($0 \to V_{DD}$).
6. **Separación Estricta entre Observación Directa e Inferencia:**  
   En todos los entregables, se separarán de forma explícita las mediciones directas de simulación (lecturas temporales, tensiones, corrientes terminales) de las inferencias analíticas derivadas (resistencias equivalentes, corrientes de cortocircuito, regímenes de operación de transistores).

---


## 4. Protocolo de Evaluación de Contención en Velocidad

Conforme a §7 Tarea 4, para evaluar la contención impuesta por el keeper:

### Circuito y Estímulo
* Topología de evaluación completa de Actividad 1: entradas en nivel alto ($A=B=C=1$).
* Reloj periódico a $500\,\text{MHz}$ ($T_{clk} = 2.0\,\text{ns}$, flancos de $20\,\text{ps}$).
* Conexión del keeper PMOS gobernado por la salida dominó `out`.

### Directivas de Medición de Retardo
```spice
.meas TRAN tphl_dyn TRIG V(clk) VAL={VDD/2} RISE=2 TARG V(dyn) VAL={VDD/2} FALL=1
.meas TRAN tplh_out TRIG V(clk) VAL={VDD/2} RISE=2 TARG V(out) VAL={VDD/2} RISE=1
```

### Cálculo de Ratios y Penalizaciones
* **Definición Literal de la Guía (§7 Tarea 4):**
  $$r = \frac{(W/L)_{kp}}{(W/L)_{PDN,eq}} \quad \text{con} \quad (W/L)_{PDN,eq} = \frac{(W/L)_n}{4}$$
* **Aproximación por Resistencias en Serie de Primer Orden:**
  Cuatro NMOS idénticos de $270\,\text{nm}$ en serie equivalen resistivamente en primer orden a:
  $$W_{PDN,eq} = \frac{3 W_n}{4} = \frac{270\text{ nm}}{4} = 67.5\text{ nm}$$
  resultando en:
  $$r = \frac{W_{kp}}{67.5\text{ nm}} = \frac{4 \cdot W_{kp}}{3 \cdot W_n}$$
  *Limitación:* Esta equivalencia lineal omite la saturación de velocidad, el efecto de cuerpo en los nodos internos y la diferencia de movilidad NMOS/PMOS en BSIM4.
* **Penalización de Retardo Relativa:**
  $$\Delta t_{pHL} (\%) = \frac{t_{pHL}(W_{kp}) - t_{pHL}(W_{kp}=0)}{t_{pHL}(W_{kp}=0)} \times 100\%$$
* **Criterio de Viabilidad Estricto:**  
  La guía exige que la degradación sea **estrictamente inferior al 10%**:
  $$\Delta t_{pHL} < 10.0\%$$
  Un valor de $\Delta t_{pHL} = 10.0\%$ está en la frontera y no satisface la cota estricta. El límite admisible de diseño es $\Delta t_{pHL} < 10.00\%$.

---

## 5. Protocolo de Aislamiento DC y Caracterización de Mecanismos (Fase A3.8.3)

Conforme a los dictámenes de auditoría conciliados, se establecen los siguientes bancos ortogonales:

### A. NMOS de PDN Desacoplado (`ENS-A3-DC-01A`)
* **Topología de Polarización Flotante:** Para evaluar el efecto de cuerpo sin falsear $V_{GS} = 0\text{ V}$, la fuente $V_{GS}$ se conecta entre compuerta y fuente flotante (`Vgs g s 0`), $V_{DS}$ entre drenaje y fuente (`Vds d s 1.0`), y una única fuente $V_{SB}$ entre fuente y masa (`Vsb s 0 {Vsb_val}`).
* **Observables:** Se registra la corriente terminal $I_D$ (que integra canal subumbral con DIBL, túnel de solapamiento compuerta-drenaje y uniones) a $V_{DS} = 0.05\text{ V}$ (DIBL atenuado) y $V_{DS} = 1.00\text{ V}$ (DIBL pleno), barriendo $V_{SB} \in [0.0, 0.3, 0.6]\text{ V}$ a $27^\circ\text{C}$ y $85^\circ\text{C}$.

### B. Investigación Experimental de GIDL por Ablación Controlada (`ENS-A3-DC-01B`)
* **Modelo Auxiliar:** Se emplea `modelos/ptm45hp_aux.lib` con tarjeta `.model nmos_45hp_nogidl`, verificada 100% idéntica a `nmos_45hp` salvo `agidl = 0.0`.
* **Criterio de Resolución:** Ambos DUTs se conectan en paralelo sobre los mismos nodos de excitación en el rango nominal $V_{DS} \in [0.01, 1.00\text{ V}]$. La contribución GIDL se evalúa como $\Delta I_D = I_D(\text{canónico}) - I_D(\text{nogidl})$. La diferencia atribuible a la ablación de AGIDL no resultó significativamente resoluble frente al ruido numérico del solver ($\Delta I_D = 0.0\text{ A}, |\Delta I_B| \sim 2.5 \times 10^{-20}\text{ A}$ bajo $V_{DD} = 1.0\text{ V}, V_{GS} = 0\text{ V}$). Por tanto, no tiene impacto práctico medible en la descarga de $V_{dyn}$ en el régimen ensayado, sin postular un cero físico absoluto ni fijar una cota universal que exceda la resolución del método.

### C. Fugas de Compuerta en Retención (`ENS-A3-DC-01C`)
* Se caracterizan las corrientes terminales de compuerta `Ig` bajo el punto de operación estático de retención ($dyn = 1.0\text{ V}, out = 0.0\text{ V}, clk = 1.0\text{ V}$) para $M_1$, $M_p$, $M_k$, $M_{ni}$ y $M_{pi}$.
* **Balance Nodal de Compuertas:** Se confirma que la fuga de compuerta que extrae portadores directamente del nodo dinámico está dominada por las compuertas del inversor dominó ($M_{pi}$ con $\approx 91.75\text{ pA}$ y $M_{ni}$ con $\approx 30.97\text{--}40.69\text{ pA}$), mientras que la compuerta de $M_1$ conecta a la entrada externa $a$ ($\approx -41.60\text{ pA}$ suministrada por la fuente $V_a$), y $M_p$ presenta corriente de compuerta nula por ausencia de gradiente de potencial ($V_{GD} = V_{GS} = 0\text{ V}$).

### D. Balance Nodal Consolidado en $dyn$ y Partición de Ramas (Fase A3.8.6)
* **Topología Canónica Real de la NAND3 Dinámica Footed:**
  * PDN Footed: $M_1, M_2, M_3, M_f$ en serie con $W = 270\text{ nm}, L = 45\text{ nm}$ ($M_f$ comandado por $CLK$).
  * Transistor de Precarga: $M_p$ con $W_p = 135\text{ nm}, L = 45\text{ nm}$.
  * Inversor Dominó de Salida: $M_{pi}$ con $W_p = 135\text{ nm}, L = 45\text{ nm}$; $M_{ni}$ con $W_n = 90\text{ nm}, L = 45\text{ nm}$.
  * Capacitancia de Carga Externa: $C_L = 2.0\text{ fF}$.
  *(Queda descartada cualquier mezcla con el inversor estático de LD1 de $W_p=450\text{ nm}, W_n=180\text{ nm}$ o precargas de $540\text{ nm}$)*.
* **Promedios Integrales Canónicos en la Ventana de Retención ($10\text{ ns}$ a $1.00052\,\mu\text{s}$):**
  * **A $27^\circ\text{C}$:**
    * $\langle I_s(M_1) \rangle = +110.528\text{ pA}$ (drenaje hacia la PDN footed).
    * $\langle I_d(M_p) \rangle = -12.259\text{ pA}$ (inyección reconstitutiva de precarga en corte desde $V_{DD}$).
    * $\langle I_g(M_{pi}) \rangle = +76.311\text{ pA}$ (drenaje hacia compuerta PMOS inversor).
    * $\langle I_g(M_{ni}) \rangle = +16.441\text{ pA}$ (drenaje hacia compuerta NMOS inversor).
    * Corriente neta demandada a la capacitancia: $\langle I_{\text{net,dev}} \rangle = +191.021\text{ pA}$.
  * **A $85^\circ\text{C}$:**
    * $\langle I_s(M_1) \rangle = +430.888\text{ pA}$ (drenaje hacia la PDN footed, incremento térmico in situ de $3.90\times$).
    * $\langle I_d(M_p) \rangle = -56.081\text{ pA}$ (inyección de precarga en corte).
    * $\langle I_g(M_{pi}) \rangle = +49.862\text{ pA}$ (drenaje hacia compuerta PMOS inversor).
    * $\langle I_g(M_{ni}) \rangle = +0.612\text{ pA}$ (drenaje hacia compuerta NMOS inversor).
    * Corriente neta demandada a la capacitancia: $\langle I_{\text{net,dev}} \rangle = +425.281\text{ pA}$.
* **Partición de Ramas de Drenaje:**
  * Los porcentajes $54.4\% / 45.6\%$ a $27^\circ\text{C}$ ($110.53\text{ pA}$ vs $92.75\text{ pA}$) y $89.5\% / 10.5\%$ a $85^\circ\text{C}$ ($430.89\text{ pA}$ vs $50.47\text{ pA}$) corresponden estrictamente al **reparto de la corriente promedio saliente de $dyn$ entre la rama PDN y las compuertas del inversor antes de descontar la inyección de precarga**.
  * No deben interpretarse como fracciones puras de subumbral vs túnel, dado que $I_s(M_1)$ integra canal subumbral, túnel compuerta-fuente acoplado y uniones de la pila.
  * No se suma $I_{G,\text{total}}(M_1)$ por segunda vez a la descarga nodal.
* **Conciliación de Capacitancias ($C_{nodo}$ estática vs $C_{\text{eff}}$ y $C_{\text{par}}$ aparentes dinámicas):**
  * La estimación analítica histórica $C_{nodo} \approx 2.65\text{ fF}$ se calculó como suma estática en pequeña señal con fórmulas lineales de área de compuerta ($C_{ox} W L$) y uniones a tensión nula.
  * $C_L = 2.0\text{ fF}$ es el único parámetro circuital explícito e independiente. Las magnitudes $\langle I(C_L) \rangle$ se integran directamente del archivo RAW. En cambio, $C_{\text{eff}}$ y $C_{\text{par}}$ son parámetros aparentes inferidos del balance integral de cargas para cerrar algebraicamente la ley de corrientes. No debe postularse un "residuo experimental nulo" como validación independiente, ya que $C_{\text{par}} \equiv C_{\text{eff}} - C_L$ se despeja por definición.
  * Conciliación numérica canónica (cuadratura exacta RAW entre $t_0 = 10.000\text{ ns}$ y $t_1 = 1000.520\text{ ns}$ con interpolación lineal de frontera idéntica al motor SPICE):
    * **A $27^\circ\text{C}$:** $V_{dyn}(t_0) = 1.023497\text{ V}$, $V_{dyn}(t_1) = 0.936959\text{ V} \implies |\Delta V_{dyn}| = 86.538\text{ mV}$, $\langle I(C_L) \rangle = -174.732\text{ pA}$ (coincide con $C_L \Delta V / \Delta t = -174.732\text{ pA}$), $\langle I_{\text{net,dev}} \rangle = +191.021\text{ pA}$, $C_{\text{eff}} = 2.18645\text{ fF} \approx 2.1864\text{ fF}$, y $C_{\text{par,din}} = 0.18645\text{ fF}$ (suministrando el remanente dinámico de $+16.289\text{ pA}$).
    * **A $85^\circ\text{C}$:** $V_{dyn}(t_0) = 1.023977\text{ V}$, $V_{dyn}(t_1) = 0.830869\text{ V} \implies |\Delta V_{dyn}| = 193.108\text{ mV}$, $\langle I(C_L) \rangle = -389.913\text{ pA}$ (coincide con $C_L \Delta V / \Delta t = -389.913\text{ pA}$), $\langle I_{\text{net,dev}} \rangle = +425.281\text{ pA}$, $C_{\text{eff}} = 2.18142\text{ fF}$, y $C_{\text{par,din}} = 0.18142\text{ fF}$ (suministrando el remanente dinámico de $+35.368\text{ pA}$).
    *(Se aclara que $V_{dyn}(t_0) \approx 1.0235\text{ V}$ debido al feedthrough/bootstrap capacitivo del flanco de reloj; no debe asumirse artificialmente $1.000\text{ V}$ como extremo inicial)*.
  * La diferencia entre $C_{\text{par,din}} \approx 0.186\text{ fF}$ y la predicción estática ($0.65\text{ fF}$) se fundamenta físicamente en que durante la retención $M_{pi}$ opera en subumbral/agotamiento ($V_{GS} \approx 0\text{ V}$), donde su capacitancia de compuerta cae al valor de solapamiento ($C_{ov} \ll C_{ox}$), y las uniones PN están polarizadas en reversa plena a $1.0\text{ V}$.

---

**Fin de los Criterios de Medición de la Actividad 3.**
