# CONCLUSIONES TÉCNICAS
## LABORATORIO DIRIGIDO N.° 3: CARACTERIZACIÓN Y SIMULACIÓN COMPARATIVA DE TRANSISTORES IGBT EN LTSPICE

* **Asignatura:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
* **Docente:** MsC. Luz Adanaqué Infante  
* **Alumno:** Leonardo Sait Yactayo Tolentino (Código: `23190214`) — *Modalidad Individual*  
* **Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
* **Requisito Oficial Asociado:** Acápite 6 de la guía oficial de laboratorio (`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`, documento docente local excluido del repositorio público). Extensión efectiva $\ge 1$ página.

---

### 1. Asimetría Fundamental entre Canales N y P: Transporte de Portadores y Dinámica de Conmutación

La comparación en simulación entre el N-IGBT (`XIRGBC20S`) y el P-IGBT (`XPIGBT`) muestra las diferencias de desempeño derivadas de la estructura interna del semiconductor:

1. **Influencia de las Propiedades de Transporte y Matiz Metodológico:**
   En el silicio, la movilidad de los electrones ($\mu_n \approx 1400\text{ cm}^2/\text{V}\cdot\text{s}$) es significativamente mayor que la de los huecos ($\mu_p \approx 450\text{ cm}^2/\text{V}\cdot\text{s}$), con una relación aproximada de $\mu_n / \mu_p \approx 3.1$.
   * En el **N-IGBT**, el canal MOSFET es de electrones y comanda la base de un transistor bipolar PNP de salida. La modulación de conductividad en la región de deriva $N^-$ se produce por la inyección de huecos desde el substrato colector $P^+$, mientras que los electrones circulan a través del canal MOS de alta movilidad.
   * En el **P-IGBT**, el canal MOSFET es de huecos y comanda un BJT NPN con región de deriva $P^-$. La menor movilidad de los huecos reduce la transconductancia intrínseca del canal MOS ($KP \propto \mu$). Para lograr capacidades de corriente comparables a las de un N-IGBT, los fabricantes recurren a compromisos de diseño geométrico en el canal y en la densidad de celdas, lo que incrementa las capacitancias parásitas de compuerta y la cantidad de carga espacial que debe desplazarse durante la conmutación.
   * **Matiz Metodológico de Simulación:** Debe subrayarse que las simulaciones SPICE comparativas no aíslan la movilidad microscópica como una variable única independiente. Los macromodelos conductuales contrastados (`nigbt.lib` frente a `pigbt.lib`) difieren simultáneamente en parámetros de tránsito bipolar ($TF = 16.8\text{ ns}$ frente a $300\text{ ns}$ implícito), formulaciones capacitivas no lineales y dimensiones de celda, por lo que el retardo y disipación mayores medidos corresponden a la respuesta compuesta del modelo y no exclusivamente a la constante de transporte de los portadores.
2. **Comparación Cuantitativa a Corriente Controlada ($19\text{ A}$):**
   Al evaluar ambos dispositivos bajo una corriente de prueba similar ($I_C \approx 19.0 - 19.5\text{ A}$) y una tensión de bus de $400\text{ V}$, se observó que el P-IGBT presenta una respuesta notablemente más lenta y mayor disipación:
   * El retardo de apagado medido fue de **$t_{d(\text{off})} = 214.20\text{ ns}$ frente a $150.83\text{ ns}$ en el N-IGBT** (+42.0% más lento en la medición directa de LTspice).
   * El tiempo de caída de corriente resultó de **$t_f = 266.30\text{ ns}$ frente a $185.24\text{ ns}$** (+43.8% más prolongado).
   * La integral de energía de apagado alcanzó **$E_{\text{off}} = 1011.8\ \mu\text{J}$ frente a $691.5\ \mu\text{J}$** (+46.3% mayor energía entregada al dispositivo).
3. **Mecanismos Físicos de la Corriente de Cola (*Tail Current*):**
   Durante el apagado, la corriente de colector no desciende instantáneamente a cero debido a la secuencia física del proceso:
   * **Fase inicial de corte del canal MOS:** Al caer $V_{GE}$ por debajo de la tensión de umbral $V_{th}$, el canal de inversión se extingue con relativa rapidez (decenas de nanosegundos), interrumpiendo la componente de corriente controlada por compuerta. Esto causa la primera caída pronunciada observada en la forma de onda de $I_C$.
   * **Fase de recombinación y barrido en la base flotante:** Una vez cortado el canal MOS, la base del BJT de salida queda sin conexión eléctrica externa. Parte de los portadores minoritarios almacenados en la región de deriva es barrida inicialmente por el campo eléctrico al expandirse la zona de agotamiento ($dv/dt > 0$), pero la carga remanente en la región neutra debe extinguirse por **recombinación espontánea electrón-hueco**. Este proceso decae de forma cuasi-exponencial regido por la vida media de portadores minoritarios a alto nivel ($\tau_{HL}$), generando la característica corriente de cola (*tail current*).
   * En el P-IGBT, la mayor cantidad de carga acumulada y la dinámica de recombinación en una región de deriva $P^-$ más ancha prolongan la duración de esta cola, aumentando la energía total de apagado.

---

### 2. Función del Diodo Co-Empaquetado (*Co-Pack*): Topología DPT frente a Convertidores de Puente

En los ensayos EXP-06 (módulo de 50 A) y EXP-07 (módulo de 75 A) se contrastaron los transistores discretos (`FGW50XS65`, `FGW75XS65`) con sus versiones co-empaquetadas (`FGW50XS65C`, `FGW75XS65C`), obteniéndose formas de onda y valores de conmutación virtualmente coincidentes en el interruptor evaluado (con diferencias mínimas $\le 0.02\text{ ns}$ en retardo y $\le 0.01\ \mu\text{J}$ en energía, no relevantes para la resolución práctica ni las métricas evaluadas):

1. **Estado de Polarización en el Banco DPT de Lado Bajo (*Low-Side*):**
   En el circuito de prueba utilizado, el transistor bajo prueba está conectado entre la inductancia de carga y tierra (emisor a $0\text{ V}$ y colector al nodo de conmutación). El diodo co-pack está integrado en antiparalelo con el ánodo en el emisor y el cátodo en el colector ($V_{AK} = -V_{CE}$).
   * Durante la conducción del IGBT, $V_{CE} \approx 1.36\text{ V} \implies V_{AK} \approx -1.36\text{ V} < 0$ (polarización inversa).
   * Durante el apagado, la tensión $V_{CE}$ se eleva a la tensión del bus ($400\text{ V}$) más el pico inductivo ($442\text{ V}$), imponiendo $V_{AK} \approx -442\text{ V} \ll 0$ (fuerte polarización inversa).
   * En consecuencia, **el diodo co-pack permanece siempre en corte y no conduce corriente directa ($I_{\text{fwd}} = 0$)**. La corriente inductiva conmuta hacia el diodo superior de marcha libre $D_1$ ubicado en paralelo con la carga inductiva.
2. **Influencia de la Capacitancia Parásita del Diodo:**
   La única interacción posible del diodo co-pack en esta configuración es su capacitancia de juntura inversa ($C_{j} \approx 0.45\text{ nF}$ en 50 A), que se añade en paralelo a la capacitancia de salida $C_{oes}$ del IGBT. Dado que $C_{oes}$ ya está presente en el transistor, este pequeño aporte no alteró de forma apreciable ni la sobretensión $V_{CE,\text{peak}}$ ni el retardo de apagado; cualquier variación observada se sitúa dentro de la resolución numérica del solver.
3. **Propósito Práctico y Fenómenos en Topologías de Puente:**
   El diodo integrado no tiene como finalidad proteger al propio transistor en el que reside durante su propio corte, sino operar en **topologías de medio puente, puente completo o convertidores trifásicos** (inversores de tracción y control de motores). En estas topologías, cuando el interruptor complementario conmuta, el diodo co-pack conduce la corriente de carga reactiva, determinando dos fenómenos esenciales:
   * **Pérdidas de conducción:** Durante la fase de rueda libre, la corriente reactiva circula a través del diodo generando calor según $P_{\text{cond}} \approx V_F \cdot I_D$.
   * **Recuperación inversa ($Q_{rr}$):** Al volver a encenderse el interruptor opuesto, el diodo co-pack debe extinguir la carga de minoritarios almacenada, generando una sobrecorriente inversa transitoria ($I_{rrm}$) durante un intervalo $t_{rr}$. Dicho pulso de corriente se suma directamente a la corriente de encendido del transistor opuesto, incrementando sustancialmente sus pérdidas dinámicas de encendido ($E_{\text{on}}$) y acentuando las oscilaciones electromagnéticas de conmutación.

---

### 3. Escalamiento del Área de Silicio: 50 A frente a 75 A (Fuji Serie X)

El análisis del ensayo EXP-08 permitió estudiar cómo influye el tamaño de la pastilla de silicio comparando los modelos `FGW50XS65` y `FGW75XS65`:

1. **Efecto en Conducción en la Comparación a Corriente Igualada ($50\text{ A}$, F01 vs F05):**
   Al operar el chip de 75 A a la misma corriente de $50\text{ A}$ que el chip de 50 A, la caída directa $V_{CE(\text{on})}$ disminuyó de **$1.362\text{ V}$ a $1.181\text{ V}$ (una reducción de $181\text{ mV}$, equivalente al $-13.3\%$ en pérdidas de conducción)**.
   * *Explicación Física:* El chip de 75 A posee una mayor área activa de silicio. En el modelo SPICE esto se refleja en un mayor parámetro de transconductancia del canal MOSFET ($KP = 9.0\text{ A/V}^2$ frente a $4.5\text{ A/V}^2$) y una menor resistencia interna de modulación ($5.23\text{ m}\Omega$ frente a $7.12\text{ m}\Omega$). Para una misma corriente de $50\text{ A}$, la densidad de corriente por unidad de área ($J = I_C / A_{\text{die}}$) es menor, reduciendo la caída óhmica interna.
2. **Efecto en la Dinámica de Conmutación:**
   En contrapartida, el chip de mayor área exhibió una conmutación más lenta y mayores pérdidas dinámicas:
   * El retardo de apagado aumentó de **$t_{d(\text{off})} = 231.10\text{ ns}$ a $324.75\text{ ns}$ (+40.5% más lento)**.
   * La energía de apagado se incrementó de **$E_{\text{off}} = 1066.98\ \mu\text{J}$ a $1367.85\ \mu\text{J}$ (+28.2% más energía en conmutación)**.
   * *Explicación Física:* Una mayor área de chip conlleva mayores capacitancias compuerta-emisor ($C_{ies} = 9.50\text{ nF}$ vs $6.77\text{ nF}$) y compuerta-colector ($C_{res} = 6.70\text{ nF}$ vs $4.00\text{ nF}$), además de un volumen mayor de carga almacenada en la región de deriva. Al descargar la compuerta a través de la misma resistencia externa ($R_G = 10\ \Omega$), la corriente de compuerta disponible tarda más tiempo en evacuar la carga de compuerta y atravesar la meseta de Miller, prolongando el intervalo de solapamiento entre tensión y corriente.
3. **Escalamiento a Régimen Nominal de Catálogo ($50\text{ A}$ vs $75\text{ A}$, F01 vs F03):**
   Al operar cada dispositivo a su respectiva corriente nominal de diseño (50 A en F01 y 75 A en F03), la caída en conducción resulta casi idéntica ($1.362\text{ V}$ frente a $1.356\text{ V}$), confirmando que el fabricante optimizó la geometría para mantener una caída directa similar a plena carga. No obstante, las pérdidas de conmutación en F03 aumentaron a **$2052.75\ \mu\text{J}$ (+92.4% respecto a F01)**, debido a que se interrumpe un $50\%$ más de corriente en presencia de mayores capacitancias y mayor carga almacenada.

---

### 4. Compromiso de Resistencia de Compuerta (*Gate Drive Trade-off*, EXP-09)

Los resultados de simulación al variar la resistencia externa de compuerta de $R_G = 10\ \Omega$ a $20\ \Omega$ en el transistor `FGW50XS65C` (F02 vs F06) muestran el compromiso clásico de sintonización de compuerta:

1. **Atenuación de la Sobretensión Inductiva ($L_\sigma \cdot di/dt$):**
   Al aumentar $R_G$ a $20\ \Omega$, la impedancia del lazo de compuerta se incrementa, reduciendo la corriente de descarga de compuerta y ralentizando el corte del canal MOS:
   * La tasa máxima de caída de corriente disminuyó de **$|di/dt|_{\text{max}} = 1669.6\text{ A}/\mu\text{s}$ a $1019.4\text{ A}/\mu\text{s}$ (reducción de $-38.9\%$)**.
   * De acuerdo con la relación $V_{\text{ind}} = L_\sigma \cdot |di/dt|$ (con $L_\sigma = 25\text{ nH}$), la sobretensión inducida sobre el bus de 400 V se redujo de **$+42.36\text{ V}$ a $+25.94\text{ V}$ ($-38.8\%$)**, disminuyendo el pico absoluto de $442.36\text{ V}$ a $425.94\text{ V}$.
   * Esto amplía el margen de seguridad respecto a la tensión de ruptura nominal del dispositivo ($V_{CES} = 650\text{ V}$) y mitiga las interferencias electromagnéticas (EMI).
2. **Incremento en las Pérdidas de Energía por Conmutación:**
   Como contrapartida, la transición más lenta provocó un aumento importante de las pérdidas:
   * El tiempo de caída de corriente se ensanchó de **$t_f = 31.38\text{ ns}$ a $57.27\text{ ns}$ (+82.5%)** y el retardo total creció a **$t_{d(\text{off})} = 361.60\text{ ns}$ (+56.5%)**.
   * La integral de energía neta de apagado creció de **$E_{\text{off}} = 1066.98\ \mu\text{J}$ a $1818.73\ \mu\text{J}$ (+70.5%)**, debido a que el dispositivo permanece durante más tiempo con tensiones y corrientes simultáneamente altas.
3. **Criterio de Selección en Diseño de Circuitos:**
   La resistencia de compuerta representa una variable de optimización práctica: seleccionar un $R_G$ muy bajo minimiza las pérdidas de conmutación pero expone al transistor a sobretensiones destructivas por inductancias parásitas de barraje ($L \cdot di/dt$) y ruido de alta frecuencia ($dv/dt$); por el contrario, un $R_G$ elevado protege dieléctricamente al conmutador pero penaliza el rendimiento térmico, exigiendo disipadores de calor de mayores dimensiones.
