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
| **EXP-06** | Sobretensión $V_{CE,\text{peak}}$ por inductancia parásita: con vs sin diodo co-pack (50 A) | `FGW50XS65` vs `FGW50XS65C` | `esquemas/DPT_Fuji_50A.asc` | `simulaciones/netlists/dpt_fuji_50a.cir` | **VALIDADO** | Fig. 6 generada (Sobretensión 50A) |
| **EXP-07** | Sobretensión $V_{CE,\text{peak}}$ por inductancia parásita: con vs sin diodo co-pack (75 A) | `FGW75XS65` vs `FGW75XS65C` | `esquemas/DPT_Fuji_75A.asc` | `simulaciones/netlists/dpt_fuji_75a.cir` | **VALIDADO** | Fig. 7 generada (Sobretensión 75A) |
| **EXP-08** | Escalamiento de Área de Silicio (50 A vs 75 A): pérdidas estáticas y dinámicas | `FGW50XS65` vs `FGW75XS65` | `esquemas/DPT_Fuji_Area.asc` | `simulaciones/netlists/dpt_fuji_area.cir` | **VALIDADO** | Fig. 8 generada (Área 50A vs 75A) |
| **EXP-09** | Sensibilidad a $R_G$: impacto de duplicar $R_G$ ($10\ \Omega \to 20\ \Omega$) en retardo y $E_{\text{off}}$ | `FGW50XS65C` | `esquemas/DPT_RG_Sweep.asc` | `simulaciones/netlists/dpt_rg_sweep.cir` | **VALIDADO** | Fig. 9 generada (Sensibilidad RG) |
| **REQ-TAB**| Consolidación de Tabla de Resultados Completa | Todos los modelos evaluados | — | `tablas/tabla_resultados_ld3.md` | **VALIDADO** | Tablas 1 y 2 en PDF Landscape |
| **REQ-CON**| Conclusiones Técnicas Fundamentadas con Física ($\ge 1$ página física) | Análisis de N vs P, área y diodo | — | `informe/conclusiones.md` | **VALIDADO** | Conclusiones exhaustivas |
| **REQ-EXP**| Exposición Oral de Principales Hallazgos (21/10/2026) | Presentación individual | — | `informe/exposicion_21oct.md` | **PREPARADO** | Sustentación el 21/10/2026 |

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

### `[PILOTO-FUJI-50A]` — Validación Metodológica y Energética (G4.2-R)
* **Requisito Metodológico:** Línea base experimental para modelos Fuji Electric Serie X. Desacoplamiento de corriente terminal de colector $I_C$, eliminación de distorsión por corriente de compuerta en shunt, y cierre del balance energético de Tellegen/Poynting.
* **Modelo Evaluado:** `FGW50XS65` (Fuji Electric Serie X, discreto sin diodo co-empaquetado).
* **Condiciones de Banco DPT:** $V_{bus} = 400\text{ V}$, $I_C \approx 50\text{ A}$ ($t_{p1} = 11.54\ \mu\text{s}$), $R_G = 10\ \Omega$, $V_{GE} = 15\text{ V} / 0\text{ V}$, $\text{temp} = 27\ ^\circ\text{C}$ (efectiva en SPICE), $\text{maxstep} = 1.0\text{ ns}$ (Gear).
* **Netlists y Logs de Evidencia:**
  * [`simulaciones/netlists/g42_ref_L0_1ns.cir`](simulaciones/netlists/g42_ref_L0_1ns.cir) / [`.log`](simulaciones/netlists/g42_ref_L0_1ns.log) — Referencia ideal $L_\sigma = 0\text{ nH}$.
  * [`simulaciones/netlists/g42_ref_L25_1ns.cir`](simulaciones/netlists/g42_ref_L25_1ns.cir) / [`.log`](simulaciones/netlists/g42_ref_L25_1ns.log) — Referencia física inductiva $L_\sigma = 25\text{ nH}$ (sin $R_{\text{par}}$).
  * [`simulaciones/netlists/g42_diag_L25_rpar50_1ns.cir`](simulaciones/netlists/g42_diag_L25_rpar50_1ns.cir) / [`.log`](simulaciones/netlists/g42_diag_L25_rpar50_1ns.log) — Variante diagnóstica ($R_{\text{par}} = 50\ \Omega$).
  * [`simulaciones/netlists/g42_ref_L0_05ns.cir`](simulaciones/netlists/g42_ref_L0_05ns.cir) y [`g42_ref_L25_05ns.cir`](simulaciones/netlists/g42_ref_L25_05ns.cir) — Pruebas de convergencia a $0.5\text{ ns}$.
* **Script de Validación Automatizada:** [`scripts/auditoria_g42_fuji.py`](scripts/auditoria_g42_fuji.py).
* **Métricas Cuantitativas Validadas (Ventana $[27.740\ \mu\text{s}, 32.840\ \mu\text{s}]$):**
  * **Ref. 1 ($L_0$):** $I_{C,\text{pre}} = 50.044\text{ A}$, $V_{CE,\text{on}} = 1.365\text{ V}$, $V_{CE,\text{peak}} = 401.33\text{ V}$, $t_{d(\text{off})} = 228.67\text{ ns}$, $t_f = 35.19\text{ ns}$, $E_{C,\text{net}} = 987.37\ \mu\text{J}$, Residuo Tellegen: $-34\text{ pJ}$ ($-0.000001\%$).
  * **Ref. 2 ($L_{25}$, sin $R_{\text{par}}$):** $I_{C,\text{pre}} = 50.009\text{ A}$, $V_{CE,\text{on}} = 1.364\text{ V}$, $V_{CE,\text{peak}} = 442.08\text{ V}$ (Sobretensión inducida respecto al bus: $+42.08\text{ V}$), $t_{d(\text{off})} = 233.24\text{ ns}$, $t_f = 31.44\text{ ns}$, $E_{C,\text{net}} = 1089.68\ \mu\text{J}$, Residuo Tellegen: $-33\text{ pJ}$ ($-0.000001\%$).
  * **Variante Diagnóstica ($L_{25}, R_{\text{par}}=50\ \Omega$):** $V_{CE,\text{peak}} = 441.14\text{ V}$, $t_{d(\text{off})} = 232.98\text{ ns}$, $E_{C,\text{net}} = 1088.21\ \mu\text{J}$, $E_{Rpar} = 0.758\ \mu\text{J}$ ($0.070\%$ de $E_C$).
* **Aserciones Superadas:** AS-01 a AS-07 al 100% (cero doble conteo, suma exacta de componentes, residuo $< 0.5\%$, concordancia Python vs SPICE $< 0.05\%$).
* **Estado de Ensayos Previos:** Ensayos exploratorios de G4.1 clasificados como **HISTÓRICO** (superados por G4.2-R al corregir sensor terminal de colector y polaridad de $R_G$).
* **Estado:** **VALIDADO CON LIMITACIONES (Línea Base G4.2-R)**

---

### `[EXP-06]` — Sobretensión $V_{CE,\text{peak}}$ y Diodo Co-Pack (Módulo 50 A)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.5. Pico de sobretensión por inductancias parásitas comparando modelos con y sin diodo de marcha libre integrado.
* **Modelos Evaluados:** `FGW50XS65` (F01, discreto) vs `FGW50XS65C` (F02, co-pack con diodo `DFGW50XS65C_sp`).
* **Condiciones:** $V_{bus} = 400\text{ V}$, $I_C = 50.0\text{ A}$, $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$, $T = 25\ ^\circ\text{C}$.
* **Datos Numéricos Obtenidos:**
  * **F01 (Discreto):** $V_{CE(\text{on})} = 1.362\text{ V}$, $V_{CE,\text{peak}} = 442.36\text{ V}$ ($+42.36\text{ V}$ vs bus), $t_{d(\text{off})} = 231.10\text{ ns}$, $t_f = 31.38\text{ ns}$, $di/dt_{\text{max}} = 1669.5\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 1066.98\ \mu\text{J}$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
  * **F02 (Co-Pack):** $V_{CE(\text{on})} = 1.362\text{ V}$, $V_{CE,\text{peak}} = 442.36\text{ V}$ ($+42.36\text{ V}$ vs bus), $t_{d(\text{off})} = 231.09\text{ ns}$, $t_f = 31.38\text{ ns}$, $di/dt_{\text{max}} = 1669.6\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 1066.98\ \mu\text{J}$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
* **Hallazgo Físico:** En switch low-side, el diodo co-pack está en polarización inversa ($V_C > V_E$), con corriente directa nula. Su capacitancia parásita ($0.45\text{ nF}$) no modifica mediblemente el pico inductivo ni las pérdidas en el interruptor bajo prueba.
* **Figura Asociada:** [`figuras/fig6_sobretension_copack_50a.png`](figuras/fig6_sobretension_copack_50a.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-07]` — Sobretensión $V_{CE,\text{peak}}$ y Diodo Co-Pack (Módulo 75 A)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.5. Pico de sobretensión para la serie de 75 A.
* **Modelos Evaluados:** `FGW75XS65` (F03, discreto) vs `FGW75XS65C` (F04, co-pack con diodo `DFGW75XS65C_sp`).
* **Condiciones:** $V_{bus} = 400\text{ V}$, $I_C = 75.0\text{ A}$ ($t_{p1} = 17.84\ \mu\text{s}$), $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$, $T = 25\ ^\circ\text{C}$.
* **Datos Numéricos Obtenidos:**
  * **F03 (Discreto):** $I_{C,\text{pre}} = 75.230\text{ A}$, $V_{CE(\text{on})} = 1.356\text{ V}$, $V_{CE,\text{peak}} = 445.98\text{ V}$ ($+45.98\text{ V}$ vs bus), $t_{d(\text{off})} = 293.18\text{ ns}$, $t_f = 40.48\text{ ns}$, $di/dt_{\text{max}} = 1818.0\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 2052.75\ \mu\text{J}$, $E_{\text{tail}} = 7.56\ \mu\text{J}$ ($0.37\%$).
  * **F04 (Co-Pack):** $I_{C,\text{pre}} = 75.233\text{ A}$, $V_{CE(\text{on})} = 1.356\text{ V}$, $V_{CE,\text{peak}} = 445.98\text{ V}$ ($+45.98\text{ V}$ vs bus), $t_{d(\text{off})} = 293.16\text{ ns}$, $t_f = 40.48\text{ ns}$, $di/dt_{\text{max}} = 1818.4\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 2052.74\ \mu\text{J}$, $E_{\text{tail}} = 7.57\ \mu\text{J}$ ($0.37\%$).
* **Hallazgo Físico:** Se comprueba idéntica respuesta en la serie de 75 A: el diodo antiparalelo no influye en las pérdidas de corte del propio conmutador.
* **Figura Asociada:** [`figuras/fig7_sobretension_copack_75a.png`](figuras/fig7_sobretension_copack_75a.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-08]` — Escalamiento de Área de Silicio (50 A vs 75 A)
* **Requisito Oficial de la Guía:** Acápite 6 (Conclusiones). Justificar con física cómo el incremento de área impacta en pérdidas de conducción y conmutación.
* **Modelos Evaluados:** `FGW50XS65` (F01) vs `FGW75XS65` a 50 A (F05) y a nominal 75 A (F03).
* **Datos Numéricos Obtenidos:**
  * **A corriente igualada ($50\text{ A}$ constantes, F01 vs F05):**
    * Mayor área reduce $V_{CE(\text{on})}$ de $1.362\text{ V}$ a **$1.181\text{ V}$** ($-181\text{ mV}$, $-13.3\%$ en pérdidas de conducción).
    * Mayor capacitancia ($C_{ies} = 9.5\text{ nF}$ vs $6.77\text{ nF}$) incrementa $t_{d(\text{off})}$ de $231.10\text{ ns}$ a **$324.75\text{ ns}$** ($+40.5\%$) y $E_{C,\text{net}}$ de $1066.98\ \mu\text{J}$ a **$1367.85\ \mu\text{J}$** ($+28.2\%$).
    * Menor $di/dt_{\text{max}}$ ($1429.8$ vs $1669.5\text{ A}/\mu\text{s}$) reduce el sobreimpulso pico de $442.36\text{ V}$ a **$436.37\text{ V}$** ($+36.37\text{ V}$ sobre bus).
  * **A corriente nominal ($50\text{ A}$ vs $75\text{ A}$, F01 vs F03):**
    * Caída similar en conducción ($1.362\text{ V}$ vs $1.356\text{ V}$).
    * $E_{\text{off}}$ se duplica: de $1066.98\ \mu\text{J}$ a **$2052.75\ \mu\text{J}$** ($+92.4\%$) debido al corte de $50\%$ más corriente con mayor tiempo de tránsito BJT ($TF = 3.0\text{ ns}$ vs $0.1\text{ ns}$).
* **Figura Asociada:** [`figuras/fig8_comparativa_area_50vs75.png`](figuras/fig8_comparativa_area_50vs75.png) (300 DPI)
* **Estado:** **VALIDADO**

---

### `[EXP-09]` — Sensibilidad a la Resistencia de Compuerta $R_G$
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.6. Relación entre $R_G$ y $t_{d(\text{off})}$. Impacto de duplicar $R_G$ ($10\ \Omega \to 20\ \Omega$) sobre pérdidas de conmutación y velocidad.
* **Modelo Evaluado:** `FGW50XS65C` ($50\text{ A}$, $400\text{ V}$): F02 ($R_G = 10\ \Omega$) vs F06 ($R_G = 20\ \Omega$).
* **Datos Numéricos Obtenidos:**
  * **$R_G = 10\ \Omega$ (F02):** $t_{d(\text{off})} = 231.09\text{ ns}$, $t_f = 31.38\text{ ns}$, $di/dt_{\text{max}} = 1669.6\text{ A}/\mu\text{s}$, $V_{CE,\text{peak}} = 442.36\text{ V}$ (Sobretensión $+42.36\text{ V}$), $E_{C,\text{net}} = 1066.98\ \mu\text{J}$.
  * **$R_G = 20\ \Omega$ (F06):** $t_{d(\text{off})} = 361.60\text{ ns}$ ($+56.5\%$), $t_f = 57.27\text{ ns}$ ($+82.5\%$), $di/dt_{\text{max}} = 1019.4\text{ A}/\mu\text{s}$ ($-38.9\%$), $V_{CE,\text{peak}} = 425.94\text{ V}$ (Sobretensión $+25.94\text{ V}$, reducción de $-38.8\%$), $E_{C,\text{net}} = 1818.73\ \mu\text{J}$ ($+70.5\%$).
* **Compromiso Físico Clave:** Duplicar $R_G$ mitiga fuertemente el estrés por sobretensión inductiva ($-16.4\text{ V}$ en pico absoluto, $-38.8\%$ en sobretensión sobre bus), a costa de una penalización severa de $+70.5\%$ en la energía de apagado disipada.
* **Figura Asociada:** [`figuras/fig9_sensibilidad_rg_conmutacion.png`](figuras/fig9_sensibilidad_rg_conmutacion.png) (300 DPI)
* **Estado:** **VALIDADO**

---


### `[REQ-TAB]` — Consolidación de Tabla de Resultados Completa
* **Requisito Oficial de la Guía:** Acápite 1. «La entrega principal de este laboratorio consta de la tabla de resultados completa y las gráficas comparativas.»
* **Contenido de la Tabla:** 11 condiciones reales sin duplicados (2 N-IGBT, 3 P-IGBT y 6 Fuji Serie X).
* **Archivo de Destino:** [`tablas/tabla_resultados_ld3.md`](tablas/tabla_resultados_ld3.md).
* **Estado:** **VALIDADO**

---

### `[REQ-CON]` — Conclusiones Técnicas Fundamentadas con Física
* **Requisito Oficial de la Guía:** Acápite 6. Redactar análisis técnico de **mínimo una página** debatiendo diferencias fundamentales entre canales N y P, impacto del diodo co-empaquetado y escalamiento de área (50 A vs 75 A).
* **Física Desarrollada:**
  1. Asimetría de movilidad de electrones vs huecos ($\mu_n \approx 3.1 \mu_p$) y su impacto en capacitancias, retardo ($+40.7\%$) y pérdidas ($+46.3\%$).
  2. Modulación de conductividad en la base $N^-$ y dinámica de recombinación en base flotante (origen del *tail current*).
  3. Polarización inversa permanente del diodo co-pack en el conmutador low-side DPT vs su función de retorno en inversores de puente.
  4. Escalamiento de área de silicio: reducción de $V_{CE(\text{on})}$ en $-13.3\%$ a costa de un incremento de $+28.2\%$ en $E_{\text{off}}$ por mayores capacitancias parásitas.
  5. Compromiso de $R_G$: mitigación del estrés por sobretensión inductiva ($-38.8\%$) frente a penalización de pérdidas por apagado ($+70.5\%$).
* **Archivos Asociados:** [`informe/conclusiones.md`](informe/conclusiones.md) y Sección 7 de [`informe/informe_ld3_yactayo.md`](informe/informe_ld3_yactayo.md).
* **Estado:** **VALIDADO**

---

### `[REQ-EXP]` — Exposición Oral de Hallazgos Principales
* **Requisito Oficial de la Guía:** Acápite 1. «El día 21 se realizará una breve exposición con los principales hallazgos en su experiencia de laboratorio, en base a ello se ponderará la calificación.»
* **Fecha Programada:** **21 de octubre de 2026**.
* **Modalidad:** Individual (Leonardo Sait Yactayo Tolentino).
* **Entregable de Apoyo Preparado:** Guion técnico estructurado diapositiva por diapositiva y banco de preguntas de sustentación en [`informe/exposicion_21oct.md`](informe/exposicion_21oct.md).
* **Estado:** **PREPARADO / PENDIENTE DE SUSTENTACIÓN ORAL EL 21/10/2026**

