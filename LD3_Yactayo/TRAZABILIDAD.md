# Matriz de Trazabilidad Experimental: LD3 (Transistores IGBT en LTspice)

**Universidad Nacional Mayor de San Marcos** — Facultad de Ingeniería Electrónica y Eléctrica<br>
**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (2026-II)<br>
**Autor:** Leonardo Sait Yactayo Tolentino (Código: `23190214`) — *Modalidad Individual*<br>
**Herramientas:** LTspice 24 | Python 3.14<br>
**Guía Oficial:** [`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`](../Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf)<br>
**Fecha de Exposición:** 21 de octubre de 2026

---

## 1. Matriz Resumen de Requisitos y Experimentos Oficiales

| ID Exp. | Requisito Oficial de la Guía | Dispositivo / Modelo | Esquema .asc | Netlist .cir | Estado | Verificación |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **EXP-01** | Banco DPT N-IGBT (Low-Side, $0\to 15\text{ V}$), formas de onda $V_{GE}, V_{CE}, I_C$ | NIGBT (`XIRGBC20S`, 600V 19A) | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDADO** | Fig. 1 generada (300 DPI) |
| **EXP-02** | Banco DPT P-IGBT (High-Side, $0\to -15\text{ V}$), formas de onda $V_{GE}, V_{CE}, I_C$ | PIGBT (`XPIGBT`, 600V 40A) | `esquemas/DPT_PIGBT_nom.asc` | `simulaciones/netlists/dpt_pigbt_nom.cir` | **VALIDADO** | Fig. 2 generada (300 DPI) |
| **EXP-03** | Extracción de Corriente de Cola (*Tail Current*) en 2do pulso de apagado | N-IGBT vs P-IGBT | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDADO** | Fig. 3 generada ($I_{tail}$ detectada) |
| **EXP-04** | Medición de Retardo de Apagado $t_{d(\text{off})}$ (90% $V_{GE} \to$ 90% $I_C$) y cotejo con Datasheet | N-IGBT vs P-IGBT | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDADO** | Fig. 4 generada (Cursores 90% a 90%) |
| **EXP-05** | Cálculo de Energía de Apagado $E_{\text{off}} = \int V_{CE} I_C dt$ y % debido a corriente de cola | N-IGBT vs P-IGBT | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDADO** | Fig. 5 generada ($E_{off}$ y $E_{tail}$) |
| **EXP-06** | Sobretensión $V_{CE,\text{peak}}$ por inductancia parásita: con vs sin diodo co-pack (50 A) | `FGW50XS65` vs `FGW50XS65C` | `esquemas/DPT_Fuji_50A.asc` | `simulaciones/netlists/dpt_fuji_50a.cir` | *PENDIENTE* | Por simular |
| **EXP-07** | Sobretensión $V_{CE,\text{peak}}$ por inductancia parásita: con vs sin diodo co-pack (75 A) | `FGW75XS65` vs `FGW75XS65C` | `esquemas/DPT_Fuji_75A.asc` | `simulaciones/netlists/dpt_fuji_75a.cir` | *PENDIENTE* | Por simular |
| **EXP-08** | Escalamiento de Área de Silicio (50 A vs 75 A): pérdidas estáticas y dinámicas | `FGW50XS65` vs `FGW75XS65` | `esquemas/DPT_Fuji_Area.asc` | `simulaciones/netlists/dpt_fuji_area.cir` | *PENDIENTE* | Por simular |
| **EXP-09** | Sensibilidad a $R_G$: impacto de duplicar $R_G$ ($10\ \Omega \to 20\ \Omega$) en retardo y $E_{\text{off}}$ | `FGW50XS65C` | `esquemas/DPT_RG_Sweep.asc` | `simulaciones/netlists/dpt_rg_sweep.cir` | *PENDIENTE* | Por simular |
| **REQ-TAB**| Consolidación de Tabla de Resultados Completa | Todos los modelos evaluados | — | `tablas/tabla_resultados_ld3.md` | *PENDIENTE* | Por compilar |
| **REQ-CON**| Conclusiones Técnicas Fundamentadas con Física ($\ge 1$ página física) | Análisis de N vs P, área y diodo | — | `informe/conclusiones.md` | *PENDIENTE* | Por redactar |
| **REQ-EXP**| Exposición Oral de Principales Hallazgos (21/10/2026) | Presentación individual | — | `informe/exposicion_21oct.md` | *PENDIENTE* | Por preparar |

---

## 2. Fichas de Detalle de Requisitos y Experimentos

### `[EXP-01]` — Banco Double Pulse Test N-IGBT (Low-Side)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 1. Configurar esquema N-IGBT con emisor a tierra mediante resistencia de prueba $R = 0.001\ \Omega$. Inductor de carga en serie con $V_{DC}$ alta conectado al colector y diodo en paralelo. Excitación de compuerta en serie con $R_G$ en modo PULSE ($0\to 15\text{ V}$).
* **Modelo Utilizado:** `XIRGBC20S` en `nigbt.lib` (Duncan Electronics / IR, 600 V, 19 A).
* **Fuente del Modelo:** `Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/nigbt.lib`.
* **Condiciones Experimentales:**
  * Tensión de barraje: $V_{DC} = 400\text{ V}$
  * Inductor de carga: $L = 100\ \mu\text{H}$ ($R_{ser} = 1\text{ m}\Omega$)
  * Resistencia de compuerta: $R_G = 10\ \Omega$ (nominal de guía)
  * Resistencia sensora en emisor: $R_E = 0.001\ \Omega$
  * Diodo de marcha libre: Diodo rápido en paralelo con el inductor ($DMOD$)
  * Perfil calibrado nominal: Primer pulso $t_{p1} = 3.65\ \mu\text{s}$, tiempo muerto $5.0\ \mu\text{s}$, segundo pulso $t_{p2} = 1.0\ \mu\text{s}$.
* **Archivos Asignados:**
  * Esquema Nominal: `LD3_Yactayo/esquemas/DPT_NIGBT_nom.asc`
  * Netlist Nominal: `LD3_Yactayo/simulaciones/netlists/dpt_nigbt_nom.cir`
  * Esquema Histórico 80A: `LD3_Yactayo/esquemas/DPT_NIGBT.asc`
  * Netlist Histórico 80A: `LD3_Yactayo/simulaciones/netlists/dpt_nigbt.cir`
* **Datos Numéricos Obtenidos (Condición Nominal $19\text{ A}$):**
  * $I_{C,\text{on}} = 19.00\text{ A}$ (exacto al 2do apagado; error $+0.02\%$)
  * $V_{CE,\text{on}} = 1.88\text{ V}$ (conducción estática de saturación)
  * $V_{CE,\text{peak}} = 400.99\text{ V}$ (fijación por diodo de marcha libre $D_1$)
  * $V_{GE,\text{peak}} = +18.63\text{ V}$ (sobreimpulso Miller inducido en compuerta)
* **Figura Asociada:** [`figuras/fig1_dpt_nigbt_transitorios.png`](figuras/fig1_dpt_nigbt_transitorios.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-02]` — Banco Double Pulse Test P-IGBT (High-Side)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 2. Configurar P-IGBT en lado alto. Fuente de disparo $V_{GE}$ entre compuerta (con $R_G$) y emisor, con niveles de 0 V (apagado) a $-15\text{ V}$ (encendido).
* **Modelo Utilizado:** `XPIGBT` en `pigbt.lib` (Duncan Electronics, 600 V, 40 A).
* **Fuente del Modelo:** `Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/pigbt.lib`.
* **Condiciones Experimentales:**
  * Tensión de bus negativo: $V_{bus} = -400\text{ V}$ (referenciado a emisor en tierra)
  * Inductor de carga: $L = 100\ \mu\text{H}$ ($R_{ser} = 1\text{ m}\Omega$)
  * Resistencia de compuerta: $R_G = 10\ \Omega$
  * Diodo de marcha libre: Ánodo a $V_{bus}$, Cátodo a $VC$ (corregido vs esquema original docente)
  * Perfil calibrado nominal: Primer pulso $t_{p1} = 8.88\ \mu\text{s}$, tiempo muerto $5.0\ \mu\text{s}$, segundo pulso $t_{p2} = 1.0\ \mu\text{s}$.
* **Archivos Asignados:**
  * Esquema Nominal: `LD3_Yactayo/esquemas/DPT_PIGBT_nom.asc`
  * Netlist Nominal: `LD3_Yactayo/simulaciones/netlists/dpt_pigbt_nom.cir`
  * Esquema Histórico 80A: `LD3_Yactayo/esquemas/DPT_PIGBT.asc`
  * Netlist Histórico 80A: `LD3_Yactayo/simulaciones/netlists/dpt_pigbt.cir`
* **Datos Numéricos Obtenidos (Condición Nominal $40\text{ A}$):**
  * $I_{C,\text{on}} = 40.02\text{ A}$ (magnitud al 2do apagado; error $+0.03\%$)
  * $V_{CE,\text{on}} = -2.51\text{ V}$ ($V_{EC} = +2.51\text{ V}$ en conducción)
  * $V_{CE,\text{peak}} = -401.22\text{ V}$ ($V_{EC} = +401.22\text{ V}$ pico)
  * $V_{GE,\text{peak}} = -17.47\text{ V}$ (sobreimpulso Miller)
  * *Corrección comprobada de signo:* $I(L1)$ fluye de Colector a $V_{bus}$, siendo positiva ($+80.56\text{ A}$ en 80A; $+40.02\text{ A}$ en nominal).
* **Figura Asociada:** [`figuras/fig2_dpt_pigbt_transitorios.png`](figuras/fig2_dpt_pigbt_transitorios.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-03]` — Caracterización de Corriente de Cola (Tail Current)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.2. Acercamiento al segundo pulso de apagado para determinar $I_C$ en el punto exacto donde inicia la fase asintótica de cola. Justificación basada en la física del dispositivo.
* **Modelos Evaluados:** `XIRGBC20S` (Canal N, 19A) vs `XPIGBT` (Canal P, 40A).
* **Método de Detección:** Localización analítica del punto de inflexión donde $|dI_C/dt|$ cae al 5% de su pendiente máxima (extinción del canal MOS y transición a recombinación bipolar en la base $N^-$).
* **Datos Numéricos Obtenidos:**
  * **N-IGBT ($19\text{ A}$):** $t_{\text{tail}} = 20.258\ \mu\text{s}$, $I_{C,\text{tail}} = 0.94\text{ A}$ ($4.93\%$ de $I_{C,\text{on}}$).
  * **N-IGBT ($80\text{ A}$):** $t_{\text{tail}} = 36.340\ \mu\text{s}$, $I_{C,\text{tail}} = 2.65\text{ A}$ ($3.22\%$ de $I_{C,\text{on}}$).
  * **P-IGBT ($40\text{ A}$):** $t_{\text{tail}} = 25.655\ \mu\text{s}$, $I_{C,\text{tail}} = 1.81\text{ A}$ ($4.53\%$ de $I_{C,\text{on}}$).
  * **P-IGBT ($80\text{ A}$):** $t_{\text{tail}} = 36.510\ \mu\text{s}$, $I_{C,\text{tail}} = 3.88\text{ A}$ ($4.66\%$ de $I_{C,\text{on}}$).
* **Figura Asociada:** [`figuras/fig3_detalle_corriente_cola.png`](figuras/fig3_detalle_corriente_cola.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-04]` — Retardo de Apagado $t_{d(\text{off})}$ y Cotejo con Datasheet
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.3. Medición del intervalo entre el 90% de $V_{GE}$ y el 90% de $I_C$. Comparación frente a hojas de datos de fabricante y justificación de discrepancias.
* **Modelos Evaluados:** `XIRGBC20S` (Canal N) vs `XPIGBT` (Canal P).
* **Definición Rigurosa:**
  * N-IGBT: Disparo en $V_{GE} = 13.5\text{ V}$ (bajada); objetivo en $I_C = 0.90 \times 19.00\text{ A} = 17.10\text{ A}$.
  * P-IGBT: Disparo en $V_{GE} = -13.5\text{ V}$ (subida hacia 0V); objetivo en $|I_C| = 0.90 \times 40.02\text{ A} = 36.02\text{ A}$.
* **Datos Numéricos Obtenidos:**
  * **N-IGBT Nominal ($19\text{ A}$):** $t_{d(\text{off})} = 150.83\text{ ns}$ (SPICE) / $152.2\text{ ns}$ (Python); $t_f = 185.24\text{ ns}$; $t_{\text{off}} = 336.07\text{ ns}$.
  * **N-IGBT Sobrecarga ($80\text{ A}$):** $t_{d(\text{off})} = 103.32\text{ ns}$; $t_f = 196.03\text{ ns}$; $t_{\text{off}} = 299.35\text{ ns}$.
  * **P-IGBT Nominal ($40\text{ A}$):** $t_{d(\text{off})} = 194.57\text{ ns}$ (SPICE) / $194.8\text{ ns}$ (Python); $t_f = 268.42\text{ ns}$; $t_{\text{off}} = 463.00\text{ ns}$.
  * **P-IGBT Sobrecarga ($80\text{ A}$):** $t_{d(\text{off})} = 172.32\text{ ns}$; $t_f = 275.03\text{ ns}$; $t_{\text{off}} = 447.36\text{ ns}$.
* **Cotejo Riguroso frente a Datasheet IRGBC20S (Farnell 68617):**
  * *Valores de Catálogo IR (Condiciones: $V_{CC}=480\text{ V}, I_C=10\text{ A}, R_G=50\ \Omega, T_j=25^\circ\text{C}$):*
    * $V_{CE(\text{on})}$ típico: $1.8\text{ V}$ (a $10\text{ A}$); $2.4\text{ V}$ (a $19\text{ A}$).
    * $t_{d(\text{off})}$ típico: $820\text{ ns}$ (máx. $1000\text{ ns}$).
    * $t_f$ típico: $910\text{ ns}$ (máx. $1500\text{ ns}$).
    * $E_{\text{off}}$ típico: $3.9\text{ mJ}$ ($3900\ \mu\text{J}$).
  * *Valores Simulados con Macromodelo Duncan (`XIRGBC20S`, $V_{bus}=400\text{ V}, I_C=19\text{ A}, R_G=10\ \Omega$):*
    * $V_{CE(\text{on})} = 1.88\text{ V}$ (a $19\text{ A}$; subestima los $2.4\text{ V}$ reales de catálogo a nominal).
    * $t_{d(\text{off})} = 150.83\text{ ns}$ (SPICE) / $152.2\text{ ns}$ (Python).
    * $t_f = 185.24\text{ ns}$.
    * $E_{\text{off}} = 0.691\text{ mJ}$ ($691.5\ \mu\text{J}$).
  * *Justificación de Discrepancias Físicas:*
    * El IRGBC20S real es un dispositivo *Standard Speed* lento ($\le 1\text{ kHz}$) caracterizado con una elevada resistencia de compuerta ($R_G = 50\ \Omega$) y tensión de barra mayor ($480\text{ V}$).
    * El macromodelo conductual provisto por Duncan Electronics (`nigbt.lib`, 1995) utiliza un tiempo de tránsito de BJT $T_F = 16.8\text{ ns}$, modelando una velocidad de conmutación sustancialmente más rápida que el componente de silicio físico.
    * Además, la menor $R_G$ del ensayo de laboratorio ($10\ \Omega$ vs $50\ \Omega$) acelera significativamente la descarga capacitiva de compuerta.
    * Por tanto, los resultados SPICE reflejan la física interna del macromodelo provisto y sus condiciones de circuito, pero difieren legítimamente de los valores conservadores de catálogo del silicio estándar.
* **Figura Asociada:** [`figuras/fig4_medicion_cursores_tdoff.png`](figuras/fig4_medicion_cursores_tdoff.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-05]` — Energía de Apagado $E_{\text{off}}$ y Fracción de Cola
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.4. Cálculo de $E_{\text{off}} = \int V_{CE} \cdot I_C dt$ durante el periodo de apagado y porcentaje atribuible a la corriente de cola.
* **Criterio de Ventana:** Integración estrictamente iniciada en el comando de caída de compuerta ($t_{\text{off2}}$) para aislar pérdidas de conmutación sin acumular conducción estática previa.
* **Datos Numéricos Obtenidos:**
  * **N-IGBT Nominal ($19\text{ A}$):** $E_{\text{off}} = 691.5\ \mu\text{J}$ ($0.6915\text{ mJ}$); $E_{\text{tail}} = 32.7\ \mu\text{J}$; $\%E_{\text{tail}} = 4.73\%$.
  * **N-IGBT Sobrecarga ($80\text{ A}$):** $E_{\text{off}} = 3402.5\ \mu\text{J}$ ($3.4025\text{ mJ}$); $E_{\text{tail}} = 76.5\ \mu\text{J}$; $\%E_{\text{tail}} = 2.25\%$.
  * **P-IGBT Nominal ($40\text{ A}$):** $E_{\text{off}} = 2115.3\ \mu\text{J}$ ($2.1153\text{ mJ}$); $E_{\text{tail}} = 91.6\ \mu\text{J}$; $\%E_{\text{tail}} = 4.33\%$.
  * **P-IGBT Sobrecarga ($80\text{ A}$):** $E_{\text{off}} = 4698.9\ \mu\text{J}$ ($4.6989\text{ mJ}$); $E_{\text{tail}} = 140.5\ \mu\text{J}$; $\%E_{\text{tail}} = 2.99\%$.
* **Figura Asociada:** [`figuras/fig5_potencia_energia_apagado.png`](figuras/fig5_potencia_energia_apagado.png) (300 DPI)
* **Estado:** **VALIDADO**

---

---

### `[EXP-06]` — Sobretensión $V_{CE,\text{peak}}$ y Diodo Co-Pack (Módulo 50 A)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.5. Pico de sobretensión por inductancias parásitas comparando modelos con y sin diodo de marcha libre integrado.
* **Modelos Evaluados:** `FGW50XS65` (sin diodo) vs `FGW50XS65C` (con diodo `DFGW50XS65C_sp`).
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig6_sobretension_copack_50a.png`
* **Estado:** PENDIENTE

---

### `[EXP-07]` — Sobretensión $V_{CE,\text{peak}}$ y Diodo Co-Pack (Módulo 75 A)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.5. Pico de sobretensión para la serie de 75 A.
* **Modelos Evaluados:** `FGW75XS65` (sin diodo) vs `FGW75XS65C` (con diodo `DFGW75XS65C_sp`).
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig7_sobretension_copack_75a.png`
* **Estado:** PENDIENTE

---

### `[EXP-08]` — Escalamiento de Área de Silicio (50 A vs 75 A)
* **Requisito Oficial de la Guía:** Acápite 6 (Conclusiones). Justificar con física cómo el incremento de área impacta en pérdidas de conducción y conmutación.
* **Modelos Evaluados:** `FGW50XS65` ($I_C = 50\text{ A}$) vs `FGW75XS65` ($I_C = 75\text{ A}$).
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig8_comparativa_area_50vs75.png`
* **Estado:** PENDIENTE

---

### `[EXP-09]` — Sensibilidad a la Resistencia de Compuerta $R_G$
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.6. Relación entre $R_G$ y $t_{d(\text{off})}$. Impacto de duplicar $R_G$ ($10\ \Omega \to 20\ \Omega$) sobre pérdidas de conmutación y velocidad.
* **Modelo Evaluado:** `FGW50XS65C`.
* **Condiciones:** Barrido paramétrico `.step param Rg list 10 20`.
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig9_sensibilidad_rg_conmutacion.png`
* **Estado:** PENDIENTE

---

### `[REQ-TAB]` — Consolidación de Tabla de Resultados Completa
* **Requisito Oficial de la Guía:** Acápite 1. «La entrega principal de este laboratorio consta de la tabla de resultados completa y las gráficas comparativas.»
* **Contenido de la Tabla:**
  1. Dispositivo y tecnología (NIGBT, PIGBT, FGW50XS65, FGW50XS65C, FGW75XS65, FGW75XS65C).
  2. Corriente de cola $I_{C,\text{tail}}$ [A].
  3. Retardo de apagado $t_{d(\text{off})}$ [ns].
  4. Retardo de hoja de datos $t_{d(\text{off}),\text{ds}}$ [ns] y discrepancia [%].
  5. Energía total de apagado $E_{\text{off}}$ [mJ].
  6. Fracción energética en cola $\%E_{\text{tail}}$ [%].
  7. Pico de sobretensión $V_{CE,\text{peak}}$ [V].
* **Archivo de Destino:** `LD3_Yactayo/tablas/tabla_resultados_ld3.md`.
* **Estado:** PENDIENTE

---

### `[REQ-CON]` — Conclusiones Técnicas Fundamentadas con Física
* **Requisito Oficial de la Guía:** Acápite 6. Redactar análisis técnico de **mínimo una página** debatiendo diferencias fundamentales entre canales N y P, impacto del diodo co-empaquetado y escalamiento de área (50 A vs 75 A).
* **Física a Explicar:**
  1. Asimetría de movilidad de electrones ($\mu_n \approx 1400\text{ cm}^2/\text{V}\cdot\text{s}$) vs huecos ($\mu_p \approx 450\text{ cm}^2/\text{V}\cdot\text{s}$) y su repercusión en la resistencia de encendido y tiempo de recombinación en canal P vs N.
  2. Modulación de conductividad en la región de deriva $N^-$ y acumulación de carga almacenada.
  3. Proceso de corte: apagado rápido del MOSFET interno seguido de recombinación lenta de minoritarios no barridos en la base flotante del BJT de salida (origen del *tail current*).
  4. Compromiso entre capacitancias parásitas ($C_{ies}, C_{oes}, C_{res}$) y área de silicio activa.
* **Archivo de Destino:** `LD3_Yactayo/informe/conclusiones.md`.
* **Estado:** PENDIENTE

---

### `[REQ-EXP]` — Exposición Oral de Hallazgos Principales
* **Requisito Oficial de la Guía:** Acápite 1. «El día 21 se realizará una breve exposición con los principales hallazgos en su experiencia de laboratorio, en base a ello se ponderará la calificación.»
* **Fecha Programada:** **21 de octubre de 2026**.
* **Modalidad:** Individual (Leonardo Sait Yactayo Tolentino).
* **Entregable de Apoyo:** Guion técnico y diapositivas de respaldo en `LD3_Yactayo/informe/exposicion_21oct.md`.
* **Puntos Críticos a Exponer:**
  1. Comparativa dinámica y física de canal N vs canal P (asimetría en $t_{d(\text{off})}$ y corriente de cola).
  2. Mecanismo físico de la corriente de cola (recombinación en base BJT vs corte MOS).
  3. Impacto del diodo co-empaquetado en la supresión de la sobretensión $V_{CE,\text{peak}}$.
  4. Compromiso de escalamiento de área (50 A vs 75 A: capacitancias parásitas vs pérdidas de conducción).
  5. Sensibilidad al dimensionamiento de $R_G$ (pérdidas dinámicas $E_{\text{off}}$ vs $di/dt$).
* **Estado:** PENDIENTE
