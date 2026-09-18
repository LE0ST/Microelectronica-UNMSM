# Criterios de Medición y Metodología Numérica — LD2

Este documento formaliza las convenciones de medición SPICE, las opciones del solver numérico, los criterios de detección de umbrales y el tratamiento de casos límite en el Laboratorio Dirigido N.° 2.

---

## 1. Opciones del Solver Numérico (Sección 4.3 y Apéndice A)

Para todas las simulaciones de LD2 se establece como directiva obligatoria en el encabezado:
```spice
.options gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear
```

### Justificación Física y Numérica
1. **`gmin = 1e-15` (1 fS):**
   El valor por defecto de LTspice (`gmin = 1e-12`, 1 pS) conecta una conductancia parásita artificial entre cada nodo y tierra. A la tensión nominal de 45nm LP ($V_{DD} = 1.1\text{ V}$), esta conductancia inyecta una corriente espuria constante calculable analíticamente como:
   $$I_{gmin} = G_{min} \cdot V_{DD} = (10^{-12}\text{ S})(1.1\text{ V}) = 1.1\text{ pA}$$
   La Sección 4.3 de la guía oficial advierte textualmente que este valor es *"comparable a las fugas que queremos medir en 45nm LP. Si no los ajustan, medirán el simulador y no el transistor"*. Dado que el proceso 45nm LP cuenta con un voltaje de umbral nominal elevado ($V_{th0} \approx 0.62\text{ V}$) y óxido grueso ($t_{oxe} = 1.80\text{ nm}$), se plantea como **hipótesis teórica y riesgo de simulación para la Fase 2** que la fuga del transistor a 27°C podría ser del orden de magnitud de unidades o decenas de picoamperios; bajo ese escenario teórico, $1.1\text{ pA}$ representaría una fracción significativa (estimada analíticamente entre 5% y 10%) de la corriente total. Fijar `gmin = 1e-15` reduce la conductancia parásita a 1 fS y su corriente espuria a $1.1\text{ aA}$ ($10^{-18}\text{ A}$). Dicha hipótesis de distorsión será evaluada y cuantificada experimentalmente mediante corridas comparativas en la Fase 2 dentro de LD2.
2. **`abstol = 1e-14` (10 fA) y `reltol = 1e-4` (0.01%):**
   Las corrientes subumbral y de compuerta en transistores desconectados alcanzan niveles de femtoamperios. La tolerancia estándar (`abstol=1e-12`) genera oscilaciones espurias de corriente durante la evaluación de nodos flotantes.
3. **`method = gear`:**
   El algoritmo trapezoidal estándar (`method = trap`) introduce ringing numérico no físico (inducción trapezoidal) cuando ocurren saltos rápidos de tensión en nodos de muy baja capacitancia (capacitancias de difusión en femtofaradios excitadas por flancos de reloj de 20 ps). Gear amortigua numéricamente este artefacto sin distorsionar la constante de tiempo RC.
4. **Excepción controlada en régimen NTV (Sección 9.2 y Apéndice A):**
   Si a tensiones ultra-bajas ($V_{DD} \le 0.4\text{ V}$) se presentan fallas de convergencia (*time step too small*), se autoriza temporalmente `method=trap reltol=1e-3` y, en caso extremo, una resistencia de regularización $R_{reg} = 1\text{ T}\Omega$ conectada al nodo dinámico, documentando explícitamente su aporte de corriente ($I_{reg} = V_{DD}/10^{12} \le 0.4\text{ pA}$).

---

## 2. Convención de Signos y Medición de Potencia / Corriente

1. **Signo de corriente en fuentes de tensión (`Vdd`):**
   En SPICE, la corriente `I(Vdd)` se define positiva cuando ingresa por el terminal positivo de la fuente (modo receptor). Cuando la fuente suministra corriente al circuito, `I(Vdd)` resulta negativa.
   * **Potencia media suministrada:**
     ```spice
     .meas TRAN Pavg AVG -I(Vdd)*V(vdd) FROM={t_ini} TO={t_fin}
     ```
   * **Corriente pico de cortocircuito en precarga (Actividad 4, §8.2):**
     Para medir la corriente suministrada por la fuente durante el solapamiento de fases, se debe utilizar:
     ```spice
     .meas TRAN Ipk_sup MAX -I(Vdd) FROM={t_ini} TO={t_fin}
     ```
     *Nota metodológica:* La guía indica `.meas TRAN Ipk MAX I(Vdd)`. Si se ejecuta sin el signo negativo, `MAX I(Vdd)` buscará el valor algebraico máximo (que será cercano a 0 o negativo si toda la corriente sale de la fuente). Ambos valores deben ser evaluados y reportados con indicación explícita de la convención adoptada.

---

## 3. Temporización de Flancos y Aislamiento de Ciclos

Para evitar que las directivas `.meas` capturen flancos pertenecientes a ciclos distintos:

1. **Ventanas de medición estrictas (`TD=`, `FROM=`, `TO=`):**
   Toda directiva `.meas` para retardos debe restringirse a la ventana temporal exacta del ciclo de interés mediante `TD` (Time Delay) o `FROM/TO`.
2. **Nomenclatura de eventos:**
   * Evaluación (descarga del nodo dinámico):
     ```spice
     .meas TRAN tpHL_dyn TRIG V(clk) VAL={VDD/2} RISE=k TARG V(dyn) VAL={VDD/2} FALL=m
     ```
     donde los índices de flanco `k` y `m` deben coincidir exactamente con el evento observado en el visor gráfico.
   * Precarga (recarga del nodo dinámico):
     ```spice
     .meas TRAN tpLH_dyn TRIG V(clk) VAL={VDD/2} FALL=k TARG V(dyn) VAL={VDD/2} RISE=m
     ```

---

## 4. Definición de Criterios de Falla y Retención ($t_{hold}$)

1. **Tiempo de retención $t_{hold}$ (§7 y §9):**
   Se define como el intervalo transcurrido desde el inicio de la evaluación (reloj detenido en 1 o flanco de subida) hasta que la tensión del nodo dinámico cae al umbral estático de referencia para conmutación del inversor de salida:
   $$V(dyn) = V_M \approx \frac{V_{DD}}{2}$$
   ```spice
   .meas TRAN t_hold WHEN V(dyn)={VDD/2} FALL=1
   ```
   *Nota de rigor temporal:* $V_M$ actúa como referencia estática límite. En dinámico, cruces instantáneos sub-umbral (glitches rápidos) no garantizan la conmutación completa de la salida si su duración es inferior al tiempo de respuesta dinámico de la etapa.
2. **Tratamiento estricto de no cruce:**
   Si durante el tiempo de simulación ($T_{stop} = 1\,\mu\text{s}$) el nodo dinámico se mantiene por encima de $V_{DD}/2$ (por ejemplo, en 45nm LP o con keeper dimensionado adecuadamente):
   * La directiva `.meas` reportará `FAIL`.
   * **REGLA AUDITABLE:** Queda terminantemente prohibido inventar o extrapolar un valor de $t_{hold}$. Se registrará como $t_{hold} > T_{stop}$ ($t_{hold} > 1\,\mu\text{s}$) y se reportará la tensión final retenida $V_{dyn}(T_{stop})$.

---

## 5. Medición de Caída por Compartición de Carga ($\Delta V$)

En la Actividad 2 se evalúa la pérdida de tensión en el nodo dinámico ante la redistribución con nodos internos:
1. **Medición puntual según guía (§6.3):**
   ```spice
   .meas TRAN Vdyn_min FIND V(dyn) AT={Tclk*1.95}
   .meas TRAN dV PARAM {VDD}-Vdyn_min
   ```
2. **Medición del mínimo real:**
   Adicionalmente se medirá el mínimo absoluto dinámico dentro del ciclo de evaluación:
   ```spice
   .meas TRAN Vdyn_abs_min MIN V(dyn) FROM={Tclk} TO={Tclk*2}
   .meas TRAN dV_real PARAM {VDD}-Vdyn_abs_min
   ```
   Ambas cifras se cotejarán para identificar si existen perturbaciones dinámicas o rebotes inductivos/capacitivos en el instante puntual $1.95 T_{clk}$.

---

## 6. Modelado de Capacitancias Parásitas de Difusión

Para que BSIM4 compute las capacitancias de unión $C_{db}$ y $C_{sb}$ en los transistores apilados de la PDN (§6.3), es mandatorio incluir en cada instancia de transistor:
```spice
AS={Ad} AD={Ad} PS={Pd} PD={Pd}
```
con:
$$A_d = W \cdot L_{diff} = (3 W_n) \cdot (90\text{ nm}) = 270\text{ nm} \times 90\text{ nm} = 0.0243\,\mu\text{m}^2$$
$$P_d = W + 2 L_{diff} = 270\text{ nm} + 180\text{ nm} = 450\text{ nm} = 0.45\,\mu\text{m}$$

---

## 7. Criterio de Dimensionamiento y Ratios de Keeper

1. **Keeper ausente (§7, Nota):**
   En BSIM4, $W=0$ genera un error de sintaxis en el simulador. Se define como valor de aproximación $W_{kp} = 1\text{ nm}$. Para auditoría cruzada, se comparará con la simulación sin la línea del transistor keeper.
2. **Ratio de contención $r$ (§7, Tarea 4):**
   $$r = \frac{(W/L)_{kp}}{(W/L)_{PDN,eq}}$$
   con $(W/L)_{PDN,eq} = \frac{W_n}{L_n} \cdot \frac{1}{4}$ considerando los 4 transistores apilados de ancho $3W_n$.
