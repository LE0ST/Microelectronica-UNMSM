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
| **EXP-01** | Banco DPT N-IGBT (Low-Side, $0\to 15\text{ V}$), formas de onda $V_{GE}, V_{CE}, I_C$ | NIGBT (`XIRGBC20S`, 600V 19A) | `esquemas/DPT_NIGBT.asc` | `simulaciones/netlists/dpt_nigbt.cir` | *PENDIENTE* | Por simular |
| **EXP-02** | Banco DPT P-IGBT (High-Side, $0\to -15\text{ V}$), formas de onda $V_{GE}, V_{CE}, I_C$ | PIGBT (`XPIGBT`, 600V 40A) | `esquemas/DPT_PIGBT.asc` | `simulaciones/netlists/dpt_pigbt.cir` | *PENDIENTE* | Por simular |
| **EXP-03** | Extracción de Corriente de Cola (*Tail Current*) en 2do pulso de apagado | N-IGBT vs P-IGBT | `esquemas/DPT_NIGBT.asc` | `simulaciones/netlists/dpt_tail_current.cir` | *PENDIENTE* | Por simular |
| **EXP-04** | Medición de Retardo de Apagado $t_{d(\text{off})}$ (90% $V_{GE} \to$ 90% $I_C$) y cotejo con Datasheet | N-IGBT vs P-IGBT | `esquemas/DPT_NIGBT.asc` | `simulaciones/netlists/dpt_tdoff.cir` | *PENDIENTE* | Por simular |
| **EXP-05** | Cálculo de Energía de Apagado $E_{\text{off}} = \int V_{CE} I_C dt$ y % debido a corriente de cola | N-IGBT vs P-IGBT | `esquemas/DPT_NIGBT.asc` | `simulaciones/netlists/dpt_eoff.cir` | *PENDIENTE* | Por simular |
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
  * Diodo de marcha libre: Diodo rápido en paralelo con el inductor
  * Perfil de pulsos $V_{GE}$: $10\ \mu\text{s}$ inicial (carga hasta $I_C$ nominal), $5\ \mu\text{s}$ apagado, $1\ \mu\text{s}$ segundo pulso.
* **Archivos Asignados:**
  * Esquema: `LD3_Yactayo/esquemas/DPT_NIGBT.asc`
  * Netlist: `LD3_Yactayo/simulaciones/netlists/dpt_nigbt.cir`
  * Medición: `.meas tran td_off TRIG V(vge) VAL=13.5 FALL=1 TARG I(L1) VAL=0.9*I_nom FALL=1`
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig1_dpt_nigbt_transitorios.png`
* **Estado:** PENDIENTE

---

### `[EXP-02]` — Banco Double Pulse Test P-IGBT (High-Side)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 2. Configurar P-IGBT en lado alto. Fuente de disparo $V_{GE}$ entre compuerta (con $R_G$) y emisor, con niveles de 0 V (apagado) a $-15\text{ V}$ (encendido).
* **Modelo Utilizado:** `XPIGBT` en `pigbt.lib` (Duncan Electronics, 600 V, 40 A).
* **Fuente del Modelo:** `Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/pigbt.lib`.
* **Condiciones Experimentales:**
  * Tensión de bus: $V_{DC} = 400\text{ V}$
  * Inductor de carga: $L = 100\ \mu\text{H}$
  * Resistencia de compuerta: $R_G = 10\ \Omega$
  * Perfil de disparo: Pulsos negativos $0\to -15\text{ V}$ referenciados a emisor.
* **Archivos Asignados:**
  * Esquema: `LD3_Yactayo/esquemas/DPT_PIGBT.asc`
  * Netlist: `LD3_Yactayo/simulaciones/netlists/dpt_pigbt.cir`
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig2_dpt_pigbt_transitorios.png`
* **Estado:** PENDIENTE

---

### `[EXP-03]` — Caracterización de Corriente de Cola (Tail Current)
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.2. Acercamiento al segundo pulso de apagado para determinar $I_C$ en el punto exacto donde inicia la fase asintótica de cola. Justificación basada en la física del dispositivo.
* **Modelos Evaluados:** `XIRGBC20S` (Canal N) vs `XPIGBT` (Canal P).
* **Condiciones:** Transitorio de conmutación fina ($t_{step} \le 10\text{ ns}$).
* **Medición:** Extracción de $I_{C,\text{tail}}$ en el quiebre de la pendiente $di/dt$.
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig3_detalle_corriente_cola.png`
* **Estado:** PENDIENTE

---

### `[EXP-04]` — Retardo de Apagado $t_{d(\text{off})}$ y Cotejo con Datasheet
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.3. Medición del intervalo entre el 90% de $V_{GE}$ y el 90% de $I_C$. Comparación frente a hojas de datos de fabricante y justificación de discrepancias.
* **Modelos Evaluados:** NIGBT (`XIRGBC20S`), PIGBT (`XPIGBT`), Fuji 50A (`FGW50XS65/C`), Fuji 75A (`FGW75XS65/C`).
* **Condiciones del Banco de Simulación (Esquema de Prueba Docente):**
  * Tensión de bus: $V_{DC} = 400\text{ V}$, Inductor: $L = 100\ \mu\text{H}$, $R_G = 10\ \Omega$, Temperatura nominal: $27^\circ\text{C}$.
* **Condiciones Nominales de Fabricante (Hojas de Datos Oficiales):**
  * **Fuji Electric Serie X (50 A):** $V_{CC} = 400\text{ V}, I_C = 50\text{ A}, V_{GE} = +15\text{ V}/0\text{ V}, R_G = 10\ \Omega, T_j = 25^\circ\text{C}$ / $125^\circ\text{C}$.
  * **Fuji Electric Serie X (75 A):** $V_{CC} = 400\text{ V}, I_C = 75\text{ A}, V_{GE} = +15\text{ V}/0\text{ V}, R_G = 10\ \Omega, T_j = 25^\circ\text{C}$ / $125^\circ\text{C}$.
  * **Duncan / IR (XIRGBC20S):** Tarjeta SPICE / Catálogo TO-220 ($600\text{ V}, 19\text{ A}, T_F = 16.8\text{ ns}$).
  * **Duncan (XPIGBT):** Tarjeta SPICE / Catálogo TO-220 ($600\text{ V}, 40\text{ A}, T_F = 24.3\text{ ns}$).
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN (Cero datos ficticios)*
* **Figura Asociada:** `figuras/fig4_medicion_cursores_tdoff.png`
* **Estado:** PENDIENTE

---

### `[EXP-05]` — Energía de Apagado $E_{\text{off}}$ y Fracción de Cola
* **Requisito Oficial de la Guía:** Acápite 5.1, Numeral 4.4. Cálculo de $E_{\text{off}} = \int V_{CE} \cdot I_C dt$ durante el periodo de apagado y porcentaje atribuible a la corriente de cola.
* **Medición:** Integral de potencia instantánea `.meas tran Eoff INTEG V(vce)*I(c) FROM=t_turnoff TO=t_end`.
* **Datos Numéricos Obtenidos:** *PENDIENTE DE SIMULACIÓN*
* **Figura Asociada:** `figuras/fig5_potencia_energia_apagado.png`
* **Estado:** PENDIENTE

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
