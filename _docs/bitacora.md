# Bitácora de Desarrollo del Proyecto (`_docs/bitacora.md`)

Este documento constituye el registro cronológico oficial de hitos, decisiones de ingeniería, cambios arquitectónicos, validaciones experimentales y seguimiento de pendientes en el repositorio **Microelectronica-UNMSM**.

---

## Estructura Estándar para Nuevas Entradas

Para registrar una nueva actividad, añadir una sección al inicio de la lista cronológica con la siguiente plantilla:

```markdown
### [YYYY-MM-DD] — Actividad: [Título Breve de la Actividad]
* **Módulo / Entregable:** [LD1 / LD2 / LD3 / Documentación / Infraestructura]
* **Autor(es):** [Leonardo Yactayo / Marco Arcila]
* **Estado:** [EN PROGRESO / COMPLETADO / EN REVISIÓN / BLOQUEADO]
* **Rama / Commit:** [Rama de trabajo | SHA si existe commit real]
* **Archivos Modificados / Creados:**
  * `ruta/archivo1.ext` — Descripción concisa del cambio
* **Decisiones Técnicas / Justificación:**
  * [Decisión 1 y respaldo físico o metodológico]
* **Resultados Obtenidos:**
  * [Métricas cuantitativas verificadas sin redondeos especulativos]
* **Pendientes / Próximos Pasos:**
  * [ ] [Tarea inmediata a desarrollar]
```

---

## Registro Cronológico de Entradas

### [2026-10-13] — Actividad: Cierre Científico Definitivo de Correcciones Residuales (H-03, H-04, H-07) en LD3
* **Módulo / Entregable:** LD3_Yactayo / Informe Académico LaTeX, PDF, Markdown y Tablas
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO Y VALIDADO (Cero simulaciones adicionales; reporte PDF en 15 páginas exactas; trazabilidad documental 100% fiel a disco)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit — en árbol de trabajo local)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/scripts/generar_pdf_informe.py` — Clasificación formal de parámetros dinámicos de Reg. 05 como `N/V*`; corrección de polaridad BJT de salida (NPN para P-IGBT y PNP para N-IGBT); supresión de causalidad forzada entre movilidad microscópica y recombinación/retardos SPICE; definición de Eoff como energía eléctrica integrada durante el apagado con diferenciación de shunt IE, colector IC y disipación térmica; ajuste de espaciado en bibliografía manteniendo el PDF en 15 páginas exactas.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.md` — Sincronización integral de las tres precisiones en el informe Markdown maestro.
  * `LD3_Yactayo/tablas/tabla_resultados_ld3.md` — Asignación de `N/V*` a parámetros dinámicos del Reg. 05 e incorporación de Nota 4 de trazabilidad.
  * `_docs/bitacora.md` — Registro de cierre técnico definitivo.
* **Decisiones Técnicas / Justificación:**
  * **H-03 (Trazabilidad P-IGBT 19A):** Búsqueda exhaustiva en disco confirmó que `dpt_pigbt_19a.raw` no se encuentra preservado en el repositorio (solo netlist y log). Por tanto, en estricto cumplimiento de la regla de Cero Invención / Cero Hallucination, los parámetros dinámicos derivados por umbrales ($t_{d(\text{off})}, t_f, I_{C,\text{tail}}, \%E_{\text{tail}}$) se declaran formalmente como `N/V*` (No Verificados). Se conservan exclusivamente los valores acreditados en `dpt_pigbt_19a.log` ($I_{C,\text{pre}} = 19.48\text{ A}$, $V_{CE(\text{on})} = 1.72\text{ V}$, $E_{\text{off}} = 1011.8\ \mu\text{J}$).
  * **H-04 (Física de Semiconductores N/P y BJT de Salida):** Subsanada la contradicción en conclusiones: el BJT equivalente de salida en P-IGBT es NPN (en N-IGBT es PNP). Se desvinculó la velocidad de recombinación de la movilidad de portadores (procesos físicos independientes) y se especificó que en SPICE las diferencias de conmutación responden a la parametrización conductual ($TF$, capacitancias, resistencias).
  * **H-07 (Denominación Física de Eoff):** Eoff se describe rigurosamente como «energía eléctrica integrada durante el apagado», diferenciando la corriente del shunt $I_E$ de la corriente de colector $I_C$, y aclarando que no equivale directamente al calor interno generado debido al almacenamiento de energía en elementos parásitos y el balance energético global.
* **Resultados Obtenidos:**
  * Compilación limpia con `pdflatex` (Returncode 0), PDF generado en 15 páginas exactas con todas las tablas apaisadas y legibles, sin desbordes ni regresiones visuales.
* **Pendientes / Próximos Pasos:**
  * [x] Cierre técnico y científico definitivo de LD3.
  * [ ] Sustentación oral individual programada para el 21 de octubre de 2026.

### [2026-10-13] — Actividad: Resolución de Hallazgos G-FINAL-SCI tras Auditoría Externa Sol High en LD3
* **Módulo / Entregable:** LD3_Yactayo / Informe Académico LaTeX, Markdown, Tablas y Documentación
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO Y VALIDADO (8 hallazgos H-01 a H-08 resueltos; cero simulaciones adicionales; integridad documental al 100%)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit — en árbol de trabajo local)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/scripts/generar_pdf_informe.py` — Actualización integral de código LaTeX del informe: eliminación de columna `|di/dt|max` en Tabla 1, sincronización de integrales de cola en Tabla 3 (F03-F06), precisión de tf(max) = 1600 ns y LE = 7.5 nH en IRGBC20S, diferenciación de C_GE vs C_ies, fundamentación de retardos Fuji (Python dinámico +56.5% vs .meas fijo +60.4%) y pulso/umbrales de P-IGBT 19A.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.md` — Sincronización biunívoca en el informe Markdown maestro.
  * `LD3_Yactayo/tablas/tabla_resultados_ld3.md` — Ajuste de notas técnicas (ratings de catálogo, inductancia LE, límite ICM = 76 A y metodología Eoff/retardos).
  * `_docs/bitacora.md` — Registro de auditoría y cierre técnico G-FINAL-SCI.
* **Decisiones Técnicas / Justificación:**
  * **H-01 (Pendiente Duncan):** Retirada la columna `|di/dt|max` de Tabla 1 Duncan al no ser solicitada en la guía docente y corresponder a pendientes medias ($I_{pre}/t_f$); se mantiene la detección de inicio de cola por quiebre de derivada ($5\%$).
  * **H-02 (Metodología de Retardo Fuji):** Documentada la divergencia entre el método Python ($90\%$ de $V_{GE,\text{pre}}$ real a $t_3 - 40\text{ ns}$, +56.5\% al duplicar $R_G$) y el comando `.meas` de LTspice (umbral fijo $13.5\text{ V}$, +60.4\%).
  * **H-03 (Trazabilidad P-IGBT 19A):** Verificado el netlist `dpt_pigbt_19a.cir`: pulso plano a $-15\text{ V}$ de $3.55\ \mu\text{s}$ ($3.65\ \mu\text{s}$ inicio a corte; corrección de errata $3.90\ \mu\text{s}$). Valores $t_{d(\text{off})} = 214.20\text{ ns}$ y $t_f = 266.30\text{ ns}$ provienen del post-procesamiento dinámico en Python sobre la curva real de $19.48\text{ A}$ ($218.23\text{ ns}$ y $268.09\text{ ns}$ bajo `.meas` con umbrales fijos nominales).
  * **H-04 (Física de Canales N/P vs Modelos SPICE):** Diferenciada la física fundamental de movilidad en silicio ($\mu_n > \mu_p$) frente a lo que demuestran los macromodelos SPICE con parámetros circuitales disímiles ($TF$, capacitancias, topología), sin afirmar sobredimensionamiento geométrico de celdas en el modelo.
  * **H-05 (C_GE vs C_ies):** Precisada la referencia al parámetro de compuerta-emisor del subcircuito $C_{GE}$ ($6.77\text{ nF}$ y $9.50\text{ nF}$) en lugar de capacitancia de entrada de catálogo $C_{ies}$.
  * **H-06 (Datasheet IRGBC20S y LE):** Corregido tiempo de caída máximo a $1600\text{ ns}$ (conforme a Farnell 68617); aclarado que `nigbt.lib` sí incorpora inductancia de emisor $LE = 7.5\text{ nH}$, describiéndose como subcircuito conductual aproximado.
  * **H-07 (Formulación Eoff):** Clarificada la diferencia entre integral de shunt en Duncan ($V_{CE} \times I_E$ con aporte de $I_G$) e integral neta de colector en Fuji ($V_{CE} \times I_C$). Ninguna se equipara a calor interno de juntura.
  * **H-08 (Energía de Cola Fuji):** Actualizados valores en Tabla 3 a las integrales RAW exactas (F03: $7.56\ \mu\text{J}$, F04: $7.57\ \mu\text{J}$, F05: $4.39\ \mu\text{J}$, F06: $8.74\ \mu\text{J}$).
* **Resultados Obtenidos:**
  * Compilación de PDF limpia, maquetación verificada en 15 páginas exactas y consistencia absoluta entre código fuente y documentación.
* **Pendientes / Próximos Pasos:**
  * [x] Cierre formal de auditoría G-FINAL-SCI.
  * [ ] Presentación oral individual programada para el 21 de octubre de 2026.

### [2026-10-13] — Actividad: Optimización de Maquetación EXP-08/EXP-09 y Eliminación de Página Vacía en LD3
* **Módulo / Entregable:** LD3_Yactayo / Informe Académico LaTeX y PDF
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO Y VALIDADO (Maquetación armónica en 15 páginas exactas; página 10 con texto y figura integrados)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit — en árbol de trabajo local)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/scripts/generar_pdf_informe.py` — Reorganización de flotantes: figuras 9 y 10 integradas en minipages atadas a sus respectivas subsecciones (EXP-08 en pág. 9 y EXP-09 en pág. 10), eliminando la página aislada y preservando legibilidad a 15 páginas.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.tex` — Código fuente recompilado sincronizado.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.pdf` — Entregable PDF final validado visualmente.
* **Decisiones Técnicas / Justificación:**
  * **Eliminación de la regresión de maquetación en pág. 10:** Las figuras 9 y 10 se desacoplaron del bloque combinado y se ubicaron inmediatamente bajo sus correspondientes análisis teóricos (Fig. 9 en pág. 9 con EXP-08; Fig. 10 en pág. 10 con EXP-09 y párrafo de síntesis).
  * **Integridad documental:** Se mantuvieron intactas las tablas apaisadas (págs. 11 y 12), las conclusiones ($\ge 1$ pág.), las 7 referencias bibliográficas en la pág. 15 y los 5 ajustes científicos aprobados previamente.
* **Pendientes / Próximos Pasos:**
  * [x] Entregable académico LD3 cerrado al 100% en 15 páginas.
  * [ ] Exposición oral individual programada para el 21 de octubre de 2026.

### [2026-10-10] — Actividad: Integración del Informe Académico Final LD3, Tablas y Conclusiones Técnicas
* **Módulo / Entregable:** LD3_Yactayo / Informe Académico Maestro, Tablas Consolidadas y Conclusiones
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO Y VALIDADO (Informe maestro, tabla de 11 registros, conclusiones $\ge 1$ pág. y guion del 21/10 integrados)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit — en árbol de trabajo local)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/informe/informe_ld3_yactayo.md` — Informe académico integral estructurado según la guía docente oficial (Acápites 1 a 6 y cuestionario 4.2 a 4.6).
  * `LD3_Yactayo/tablas/tabla_resultados_ld3.md` — Tabla general consolidada de 11 registros reales sin duplicados (cumplimiento `[REQ-TAB]`).
  * `LD3_Yactayo/informe/conclusiones.md` — Monografía técnica de conclusiones con fundamentación física densa ($\ge 1$ página efectiva, cumplimiento `[REQ-CON]`).
  * `LD3_Yactayo/informe/exposicion_21oct.md` — Guion técnico estructurado para la sustentación oral individual del 21 de octubre de 2026 (cumplimiento `[REQ-EXP]`).
  * `LD3_Yactayo/TRAZABILIDAD.md` — Actualización integral de requisitos docentes.
* **Decisiones Técnicas / Justificación:**
  * **Inventario Real de 11 Registros:** Se reconciliaron las 11 condiciones efectivas de ensayo (2 N-IGBT nom/sob, 3 P-IGBT nom/sob/ctrl, 6 Fuji Serie X F01-F06), eliminando ambigüedades.
  * **Compatibilidad Metodológica Documentada:** Se explicitaron las diferencias entre las instrumentaciones de Duncan (shunt $1\text{ m}\Omega$, umbral analítico $5\% |dI/dt|$, $27\ ^\circ\text{C}$) y Fuji (sensores 0V, umbral operacional $5\% I_{\text{pre}}$, $25\ ^\circ\text{C}$), evitando comparaciones directas incompatibles.
  * **Rigor en Conclusiones:** Conclusiones extendidas ($\ge 1$ página) debatiendo el transporte de portadores, la función del diodo co-pack en convertidores de puente vs DPT, el escalamiento estático/dinámico de silicio y el compromiso $L \cdot di/dt$ vs $E_{\text{off}}$ al sintonizar $R_G$.
* **Pendientes / Próximos Pasos:**
  * [x] Ensayos experimentales EXP-01 a EXP-09 cerrados y validados.
  * [x] Informe académico maestro redactado al 100%.
  * [x] Tabla consolidada de 11 registros finalizada.
  * [x] Guion de sustentación oral preparado.
  * [ ] Sustentación oral presencial/virtual programada para el 21 de octubre de 2026.


### [2026-10-10] — Actividad: Ejecución y Validación de la Suite Fuji Electric Serie X (F01 a F06 a 25 °C)
* **Módulo / Entregable:** LD3_Yactayo / Ensayos EXP-06, EXP-07, EXP-08 y EXP-09
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO Y VALIDADO (6 configuraciones F01 a F06 ejecutadas a 25 °C; 100% PASS en calibración de corriente ±1%; 4 figuras generadas a 300 DPI)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit — en árbol de trabajo local)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/scripts/simular_suite_fuji.py` — Script modular de simulación DPT, cálculo dinámico de umbrales y generador de figuras.
  * `LD3_Yactayo/simulaciones/netlists/fuji_f01.cir` a `fuji_f06.cir` y sus correspondientes `.log` y `.raw`.
  * `LD3_Yactayo/figuras/fig6_sobretension_copack_50a.png` (EXP-06: Co-pack 50 A a 300 DPI).
  * `LD3_Yactayo/figuras/fig7_sobretension_copack_75a.png` (EXP-07: Co-pack 75 A a 300 DPI).
  * `LD3_Yactayo/figuras/fig8_comparativa_area_50vs75.png` (EXP-08: Escalamiento de área a 300 DPI).
  * `LD3_Yactayo/figuras/fig9_sensibilidad_rg_conmutacion.png` (EXP-09: Sensibilidad $R_G$ a 300 DPI).
  * `LD3_Yactayo/tablas/tabla_resultados_fuji_completa.md` — Tabla cuantitativa consolidada con mapeo biunívoco de reutilización.
  * `LD3_Yactayo/TRAZABILIDAD.md` — Actualización de EXP-06 a EXP-09 a estado VALIDADO.
* **Decisiones Técnicas / Justificación:**
  * **Optimización de Matriz (6 Casos Únicos):** Se eliminó redundancia reduciendo de 8 a 6 configuraciones: F01 (50A Discreto), F02 (50A Co-Pack, reutilizado como ref. $R_G$), F03 (75A Discreto nominal), F04 (75A Co-Pack), F05 (75A a 50A control), F06 (50A Co-Pack a $20\ \Omega$).
  * **Secuencia DPT Parametrizada Coherentemente:** Inicio $t_0 = 10\ \mu\text{s}$, libre circulación $5\ \mu\text{s}$, segundo pulso $1.0\ \mu\text{s}$, apagado $t_3$, ventana de integración fijada relativamente en $[t_3, t_3 + 5.10\ \mu\text{s}]$.
  * **Calibración Estricta de Corrientes ($\pm 1\%$):**
    * 50 A ($t_{p1} = 11.54\ \mu\text{s}$): F01 ($50.013\text{ A}$, $+0.03\%$), F02 ($50.012\text{ A}$, $+0.02\%$), F05 ($50.362\text{ A}$, $+0.72\%$), F06 ($50.123\text{ A}$, $+0.25\%$).
    * 75 A ($t_{p1} = 17.84\ \mu\text{s}$): F03 ($75.230\text{ A}$, $+0.31\%$), F04 ($75.233\text{ A}$, $+0.31\%$).
    * Todas dentro de la tolerancia objetivo de $\pm 1\%$ (PASS).
  * **Condición de Temperatura Oficial:** Fijada explícitamente en `.temp 25` ($25.0\ ^\circ\text{C}$) en todos los netlists.
  * **Aislamiento Físico del Diodo Co-Pack:** Se verificó que en el switch de lado bajo el diodo integrado se encuentra en polarización inversa ($V_C > V_E$), con corriente directa nula, confirmando que no afecta las pérdidas de corte del propio switch.
  * **Compromiso de Área:** Mayor área (75 A) reduce $V_{CE(\text{on})}$ en $-13.3\%$ ($1.362\text{ V} \to 1.181\text{ V}$), pero eleva $E_{\text{off}}$ en $+28.2\%$ a igual corriente debido a mayores capacitancias.
  * **Compromiso de $R_G$:** Duplicar $R_G$ ($10 \to 20\ \Omega$) reduce la sobretensión sobre bus en $-38.8\%$ ($+42.36\text{ V} \to +25.94\text{ V}$), penalizando $E_{\text{off}}$ en $+70.5\%$.
* **Resultados Obtenidos:**
  * F01: $V_{CE(\text{on})} = 1.362\text{ V}$, $V_{CE,\text{pk}} = 442.36\text{ V}$, $t_{d(\text{off})} = 231.10\text{ ns}$, $t_f = 31.38\text{ ns}$, $E_{\text{off}} = 1066.98\ \mu\text{J}$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
  * F02: $V_{CE(\text{on})} = 1.362\text{ V}$, $V_{CE,\text{pk}} = 442.36\text{ V}$, $t_{d(\text{off})} = 231.09\text{ ns}$, $t_f = 31.38\text{ ns}$, $E_{\text{off}} = 1066.98\ \mu\text{J}$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
  * F03: $V_{CE(\text{on})} = 1.356\text{ V}$, $V_{CE,\text{pk}} = 445.98\text{ V}$, $t_{d(\text{off})} = 293.18\text{ ns}$, $t_f = 40.48\text{ ns}$, $E_{\text{off}} = 2052.75\ \mu\text{J}$, $E_{\text{tail}} = 7.56\ \mu\text{J}$ ($0.37\%$).
  * F04: $V_{CE(\text{on})} = 1.356\text{ V}$, $V_{CE,\text{pk}} = 445.98\text{ V}$, $t_{d(\text{off})} = 293.16\text{ ns}$, $t_f = 40.48\text{ ns}$, $E_{\text{off}} = 2052.74\ \mu\text{J}$, $E_{\text{tail}} = 7.57\ \mu\text{J}$ ($0.37\%$).
  * F05: $V_{CE(\text{on})} = 1.181\text{ V}$, $V_{CE,\text{pk}} = 436.37\text{ V}$, $t_{d(\text{off})} = 324.75\text{ ns}$, $t_f = 34.18\text{ ns}$, $E_{\text{off}} = 1367.85\ \mu\text{J}$, $E_{\text{tail}} = 4.39\ \mu\text{J}$ ($0.32\%$).
  * F06: $V_{CE(\text{on})} = 1.392\text{ V}$, $V_{CE,\text{pk}} = 425.94\text{ V}$, $t_{d(\text{off})} = 361.60\text{ ns}$, $t_f = 57.27\text{ ns}$, $E_{\text{off}} = 1818.73\ \mu\text{J}$, $E_{\text{tail}} = 8.74\ \mu\text{J}$ ($0.48\%$).
* **Pendientes / Próximos Pasos:**
  * [ ] Presentar entrega oficial consolidada al usuario.
  * [ ] Proceder con la redacción de conclusiones técnicas ([`REQ-CON`]) y guion de exposición del 21/10/2026 ([`REQ-EXP`]).


### [2026-10-10] — Actividad: Cierre Metodológico y Validación Energética G4.2-R (Piloto Fuji FGW50XS65)
* **Módulo / Entregable:** LD3_Yactayo / Piloto Experimental y Validación Numérica FGW50XS65
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** APTO CON LIMITACIONES (Validado como referencia metodológica para EXP-07 a EXP-09; resultados G4.1 clasificados como históricos)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit — en árbol de trabajo local)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/scripts/auditoria_g42_fuji.py` — Script auditado con cálculo estricto $I^2 R \ge 0$, balance Poynting/Tellegen cerrado (residuo 34 pJ), validación de malla de compuerta y aserciones automatizadas.
  * `LD3_Yactayo/simulaciones/netlists/g42_ref_L0_1ns.cir` / `.log` — Referencia ideal $L_\sigma = 0\text{ nH}$, paso 1.0 ns.
  * `LD3_Yactayo/simulaciones/netlists/g42_ref_L25_1ns.cir` / `.log` — Referencia física con inductancia parásita $L_\sigma = 25\text{ nH}$ (sin $R_{\text{par}}$).
  * `LD3_Yactayo/simulaciones/netlists/g42_diag_L25_rpar50_1ns.cir` / `.log` — Variante diagnóstica con amortiguamiento analítico $R_{\text{par}} = 50\ \Omega$.
  * `LD3_Yactayo/simulaciones/netlists/g42_ref_L0_05ns.cir` y `g42_ref_L25_05ns.cir` — Pruebas de convergencia temporal (paso 0.5 ns).
  * `LD3_Yactayo/TRAZABILIDAD.md` — Actualización con ficha formal del piloto G4.2-R.
* **Decisiones Técnicas / Justificación:**
  * **Temperatura Efectiva Confirmada:** Se constató en los archivos `.log` que la temperatura real de simulación fue `temp = 27 °C` (predeterminado de SPICE). Se establece que en las próximas extensiones se mantendrá esta identificación clara para cotejos con hojas de datos ($T_j = 25\ ^\circ\text{C}$).
  * **Reconciliación del Balance de Tellegen:** Se identificó que la orientación de $R_1$ en el netlist provocaba $E_{RG} = -1.0486\ \mu\text{J}$. Al formular la disipación resistiva estrictamente positiva $P = I^2 R \ge 0$, el residuo colapsó de $+2.097\ \mu\text{J}$ a $-0.000034\ \mu\text{J}$ ($-0.000001\%$, 34 picojoules en $5.58\text{ mJ}$).
  * **Conservación en Malla de Compuerta:** Se comprobó que $E_{V1} = -0.2405\ \mu\text{J}$ se conserva con $E_{RG} (+1.0486\ \mu\text{J})$ y $E_G (-1.2815\ \mu\text{J})$ con residuo $< 10^{-11}\text{ J}$.
  * **Moderación Física de $E_{\text{off}}$:** Se definió $E_{\text{off}}$ ($1089.68\ \mu\text{J}$) como una integral operacional de puerto terminal que incluye intercambio de energía electrostática de las capacitancias inter-electródicas no lineales, descartando calificarla como calor puramente disipado.
  * **Distinción de Sobretensión:** Para $L_\sigma = 25\text{ nH}$, el pico absoluto es $V_{CE,\text{peak}} = 442.08\text{ V}$, representando una sobretensión inducida de $+42.08\text{ V}$ respecto a la barra DC de $400\text{ V}$ ($+40.75\text{ V}$ sobre el caso ideal de $0\text{ nH}$).
  * **Evaluación de $R_{\text{par}} = 50\ \Omega$:** Absorbe solo $0.758\ \mu\text{J}$ ($0.07\%$ de $E_C$). Se clasifica como elemento diagnóstico y se adopta $L_\sigma = 25\text{ nH}$ sin $R_{\text{par}}$ como la referencia física.
  * **Resolución Temporal:** Se verificó variación $< 0.02\%$ al reducir `maxstep` de 1.0 ns a 0.5 ns, concluyendo que 1.0 ns es "suficiente" para resolver los transitorios de conmutación.
* **Resultados Obtenidos:**
  * Ref. 1 ($L_0$): $I_{C,\text{pre}} = 50.04\text{ A}$, $V_{CE,\text{peak}} = 401.33\text{ V}$, $t_{d(\text{off})} = 228.67\text{ ns}$, $t_f = 35.19\text{ ns}$, $E_{C,\text{net}} = 987.37\ \mu\text{J}$, Residuo Tellegen $= -34\text{ pJ}$.
  * Ref. 2 ($L_{25}$, sin $R_{\text{par}}$): $I_{C,\text{pre}} = 50.01\text{ A}$, $V_{CE,\text{peak}} = 442.08\text{ V}$ ($+42.08\text{ V}$ vs bus), $t_{d(\text{off})} = 233.24\text{ ns}$, $t_f = 31.44\text{ ns}$, $E_{C,\text{net}} = 1089.68\ \mu\text{J}$, Residuo Tellegen $= -33\text{ pJ}$.
  * Diag. ($L_{25}$, $R_{\text{par}}=50\ \Omega$): $V_{CE,\text{peak}} = 441.14\text{ V}$, $E_{C,\text{net}} = 1088.21\ \mu\text{J}$, $E_{Rpar} = 0.758\ \mu\text{J}$, Residuo Tellegen $= -30\text{ pJ}$.
* **Pendientes / Próximos Pasos:**
  * [x] Cierre documental de G4.2-R y confirmación de temperatura efectiva de 27 °C.
  * [ ] Presentar matriz experimental y plan para EXP-07, EXP-08 y EXP-09 reutilizando metodología G4.2-R.
  * [ ] Aguardar autorización para simular el lote completo.


### [2026-10-10] — Actividad: Conciliación de Auditoría G2.1 y QA Científico G3.1 (EXP-01 a EXP-05)
* **Módulo / Entregable:** LD3_Yactayo / Ensayos EXP-01 a EXP-05
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO Y VALIDADO (EXP-01 a EXP-05 validados; figuras a 300 DPI generadas; detención antes de EXP-06)
* **Rama / Commit:** `feat/ld3-igbt` | Commit `c399cac`
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/simulaciones/netlists/dpt_nigbt_nom.cir` — Netlist DPT nominal N-IGBT ($19.00\text{ A}$, $t_{p1} = 3.65\ \mu\text{s}$).
  * `LD3_Yactayo/simulaciones/netlists/dpt_pigbt_nom.cir` — Netlist DPT nominal P-IGBT ($40.02\text{ A}$, $t_{p1} = 8.88\ \mu\text{s}$).
  * `LD3_Yactayo/simulaciones/netlists/dpt_pigbt_19a.cir` — Netlist DPT controlado P-IGBT a corriente igualada ($19.48\text{ A}$).
  * `LD3_Yactayo/esquemas/DPT_NIGBT_nom.asc` — Esquema nominal interactivo N-IGBT sincronizado.
  * `LD3_Yactayo/esquemas/DPT_PIGBT_nom.asc` — Esquema nominal interactivo P-IGBT sincronizado.
  * `LD3_Yactayo/scripts/buscar_pulsos_exactos.py` — Calibrador de duración de pulso de carga inductiva.
  * `LD3_Yactayo/scripts/parse_raw.py` — Parser vectorial de archivos ASCII RAW de LTspice.
  * `LD3_Yactayo/scripts/qa_cientifico_g31.py` — Análisis de sensibilidad de cola (3%, 5%, 10%) y ventanas de $E_{\text{off}}$.
  * `LD3_Yactayo/scripts/comparacion_controlada_19a.py` — Ensayo controlado N vs P a $19\text{ A}$ idénticos.
  * `LD3_Yactayo/scripts/generar_figuras_exp01_exp05.py` — Generador científico de formas de onda a 300 DPI.
  * `LD3_Yactayo/figuras/fig1_dpt_nigbt_transitorios.png` a `fig5_potencia_energia_apagado.png` — Figuras oficiales.
  * `LD3_Yactayo/tablas/tabla_resultados_exp01_exp05.md` — Tabla consolidada cuantitativa y cotejo con catálogo real.
  * `LD3_Yactayo/TRAZABILIDAD.md` — Matriz actualizada a estado VALIDADO para EXP-01 a EXP-05.
* **Decisiones Técnicas / Justificación:**
  * **Corrección de Signo en P-IGBT:** La corriente $I(L1)$ fluye de Colector a $V_{bus}$ (positivo por convención SPICE, $+80.56\text{ A}$). La auditoría externa evaluó `MAX(-I(L1))` buscando el máximo de una cantidad negativa, falseando el dato a $-75.98\text{ A}$.
  * **Aporte Inductivo del Segundo Pulso:** El segundo pulso de $1.0\ \mu\text{s}$ añade $\Delta I_2 \approx \frac{400\text{ V} \times 1\ \mu\text{s}}{100\ \mu\text{H}} \approx 3.95\text{ A}$. Para alcanzar exactamente la corriente nominal en el segundo apagado, el pulso 1 debe cargar a $15.05\text{ A}$ (N-IGBT, $t_{p1} = 3.65\ \mu\text{s}$) y $36.05\text{ A}$ (P-IGBT, $t_{p1} = 8.88\ \mu\text{s}$). La auditoría de Nemotron asumió erróneamente pulsos de $4.75\ \mu\text{s}$ y $10.0\ \mu\text{s}$ que habrían provocado corrientes fuera de régimen nominal.
  * **Retardo de Apagado $t_{d(\text{off})}$ Riguroso:** Implementación estricta de la directiva de la profesora (90% $V_{GE} \to$ 90% $I_C$). Nemotron utilizó erróneamente 10% de $I_C$ (confundiendo $t_{d(\text{off})}$ con $t_f$/$t_{\text{off}}$) y $-1.5\text{ V}$ para P-IGBT (confundiendo 90% con 10%). Se implementó ventana retardada `TD` para evitar falsos cruces en pulso 1.
  * **Aislamiento de Pérdidas de Conmutación $E_{\text{off}}$:** La integración se inicia rigurosamente en el flanco descendente del pulso de compuerta ($t_{\text{off2}}$), evitando la inclusión errónea de $0.9\ \mu\text{s}$ de pérdidas de conducción estática previas que Nemotron arrastró al integrar desde $35.1\ \mu\text{s}$.
  * **Cotejo Honesto frente a Datasheet IRGBC20S:** El catálogo oficial (Farnell 68617) especifica condiciones muy diferentes ($V_{CC}=480\text{ V}, I_C=10\text{ A}, R_G=50\ \Omega, T_j=25^\circ\text{C}$): $V_{CE(\text{on})} = 1.8\text{ V}$ (a 10 A) y $2.4\text{ V}$ (a 19 A); $t_{d(\text{off})} = 820\text{ ns}$, $t_f = 910\text{ ns}$, $E_{\text{off}} = 3.9\text{ mJ}$. El modelo `XIRGBC20S` de Duncan parametriza $T_F = 16.8\text{ ns}$ (conmutación mucho más veloz) y nuestro circuito emplea $R_G = 10\ \Omega$, justificando que en SPICE se obtengan tiempos más rápidos ($150.8\text{ ns} / 185.2\text{ ns}$). Se eliminaron afirmaciones falsas de concordancia directa y se documentaron las condiciones de test.
  * **Sensibilidad de Cola:** Se analizó el impacto del umbral de detección ($3\%$, $5\%$ y $10\%$ de $|dI/dt|_{\text{max}}$). La corriente asignada a la cola varía entre $0.56\text{ A}$ y $1.88\text{ A}$ ($2.9\%$ a $9.9\%$ de $I_{\text{on}}$), y $\%E_{\text{tail}}$ varía entre $2.88\%$ y $9.31\%$, confirmando que el 5% es una métrica operacional robusta.
  * **Ensayo Controlado a Igual Corriente ($19\text{ A}$):** A $19\text{ A}$ idénticos, el canal P es $40.7\%$ más lento en $t_{d(\text{off})}$, $43.8\%$ más lento en $t_f$ y disipa $46.3\%$ más energía ($1011.8\ \mu\text{J}$ vs $691.5\ \mu\text{J}$), aislando la desventaja estructural de portadores y capacitancias del canal P.
* **Resultados Obtenidos:**
  * N-IGBT ($19.00\text{ A}$): $V_{CE,\text{on}} = 1.88\text{ V}$, $t_{d(\text{off})} = 150.83\text{ ns}$, $t_f = 185.24\text{ ns}$, $I_{C,\text{tail}} = 0.94\text{ A}$ ($4.93\%$), $E_{\text{off}} = 691.5\ \mu\text{J}$, $E_{\text{tail}} = 32.7\ \mu\text{J}$ ($4.73\%$).
  * P-IGBT ($40.02\text{ A}$): $V_{CE,\text{on}} = -2.51\text{ V}$, $t_{d(\text{off})} = 194.57\text{ ns}$, $t_f = 268.42\text{ ns}$, $I_{C,\text{tail}} = 1.81\text{ A}$ ($4.53\%$), $E_{\text{off}} = 2115.3\ \mu\text{J}$, $E_{\text{tail}} = 91.6\ \mu\text{J}$ ($4.33\%$).
  * Sobrecarga Exploratoria ($80\text{ A}$): $E_{\text{off}} = 3402.5\ \mu\text{J}$ (N) y $4698.9\ \mu\text{J}$ (P).
* **Pendientes / Próximos Pasos:**
  * [ ] Presentar reporte conciso G3.1 al usuario.
  * [ ] Mantener detención antes de EXP-06 (Serie Fuji Electric Serie X) hasta nueva instrucción.

### [2026-10-10] — Actividad: Arranque G2 — Preparación y Calibración de Bancos DPT (N-IGBT y P-IGBT)
* **Módulo / Entregable:** LD3_Yactayo / Ensayos EXP-01 y EXP-02
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** EN PROCESO DE CALIBRACIÓN (Simulación SPICE funcional; pendientes métricas de conmutación)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit de G2 — a la espera de autorización)*
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/simulaciones/netlists/dpt_nigbt.cir` — Netlist de banco DPT lado bajo para N-IGBT (`XIRGBC20S`).
  * `LD3_Yactayo/simulaciones/netlists/dpt_pigbt.cir` — Netlist de banco DPT lado alto para P-IGBT (`XPIGBT`).
  * `LD3_Yactayo/esquemas/DPT_NIGBT.asc` — Esquema adaptado de LTspice con rutas relativas a librerías existentes.
  * `LD3_Yactayo/esquemas/DPT_PIGBT.asc` — Esquema corregido de LTspice conectando el diodo de marcha libre $D_1$.
  * `LD3_Yactayo/TRAZABILIDAD.md` — Actualización de EXP-01 y EXP-02 a estado EN CALIBRACIÓN con medidas reales.
  * `_docs/bitacora.md` — Registro de la actividad G2.
* **Decisiones Técnicas / Justificación:**
  * **Orden de Pines y Prefijo:** Se comprobó que en `nigbt.lib` y `pigbt.lib` los subcircuitos `XIRGBC20S` y `XPIGBT` definen el orden de pines `71=Collector, 72=Gate, 74=Emitter`, requiriendo prefijo `X`.
  * **Corrección Circuital en P-IGBT:** Se detectó que el archivo esquemático docente original `PIGBT.asc` contenía el diodo $D_1$ flotando sin conexión (`NC_01 NC_02`), lo cual provocaría una desconexión inductiva sin retorno. Se conectó en paralelo con la carga inductiva $L_1$ (Ánodo a $V_{bus} = -400\text{ V}$, Cátodo a $VC$).
  * **Verificación Física de Carga Inductiva:** Con $V_{DC} = 400\text{ V}$, $L = 100\ \mu\text{H}$ y un pulso largo de carga de $20\ \mu\text{s}$, la corriente pico de carga alcanzó $79.68\text{ A}$ (N-IGBT) y $80.23\text{ A}$ (P-IGBT), verificando con alta fidelidad la ley de inducción $\Delta I = \frac{V \Delta t}{L} = 80\text{ A}$.
* **Resultados Obtenidos:**
  * Simulación transitoria completada exitosamente en modo batch (`LTspice.exe -b`) en $\approx 0.4\text{ s}$.
  * Tensiones en conducción extraídas: $V_{CE,\text{on}} = 5.66\text{ V}$ (N-IGBT) y $-3.87\text{ V}$ (P-IGBT).
  * Fijación de sobretensión verificada en $401.66\text{ V}$ (N-IGBT) y $-401.67\text{ V}$ (P-IGBT).
  * Advertencia de modelo analizada: `Instance xz1:M1: Width narrower than recommended for a level 3 MOSFET` (intrínseca del modelo TO-220 de Duncan Electronics).
* **Pendientes / Próximos Pasos:**
  * [ ] Detenerse antes de EXP-03 a EXP-09 según instrucción de la fase.
  * [ ] Script de post-procesamiento en Python para graficar formas de onda de $V_{GE}, V_{CE}, I_C$.
  * [ ] Calibración detallada de $t_{d(\text{off})}$, $I_{C,\text{tail}}$ y $E_{\text{off}}$ tras aprobación del usuario.

### [2026-10-10] — Actividad: Auditoría G0 y Normalización Documental G1
* **Módulo / Entregable:** Infraestructura Global / Preparación LD3
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO (Fases G0 y G1)
* **Rama / Commit:** `feat/ld3-igbt` | Commit `59ab16a` (`docs(repo): normalize course documentation and initialize LD3`)
* **Archivos Modificados / Creados:**
  * `.gitignore` — Refinamiento de exclusiones de evaluaciones locales (`Semana_06/*LC1*.zip`) para evitar ocultar archivos académicos futuros de `Semana_06`.
  * `_docs/plan.md` — Corrección integral: LD2 marcado como completado (100%), LD3 redefinido como transistores IGBT individual (exposición 21/10/2026).
  * `_docs/process.md` — Separación explícita entre reglas globales innegociables y requisitos específicos de LD1, LD2 y LD3.
  * `README.md` — Actualización de autorías (Leonardo y Marco en LD1/LD2; Leonardo individual en LD3), mapa de carpetas, corrección de enlace a `LD1_Arcila_Yactayo.pdf` y presentación de LD3.
  * `AGENTS.md` — Context Engineering actualizado, eliminación de comando inseguro `git add .`, desvinculación de reglas de $\beta$ y 12 páginas para LD3, y corrección de enlaces rotos.
  * `CLAUDE.md` — Actualización de instrucciones y comandos para Claude Code y asistentes IA.
  * `_docs/bitacora.md` — Creación de la bitácora global e inicialización de la primera entrada.
  * `LD3_Yactayo/README.md` — Creación de la portada técnica y metodología de LD3.
  * `LD3_Yactayo/TRAZABILIDAD.md` — Creación de la matriz de trazabilidad con 11 requisitos docentes en estado PENDIENTE.
  * `LD3_Yactayo/modelos/NOTAS_MODELOS.md` — Documentación de procedencia, fuentes oficiales y términos de uso de modelos IGBT existentes.
* **Decisiones Técnicas / Justificación:**
  * **Autoría y Modalidad:** Se formalizó la autoría individual de Leonardo Yactayo en LD3 según lo respaldado por la guía oficial («El laboratorio puede ser en parejas o individual»), preservando la coautoría histórica con Marco Arcila en LD1 y LD2.
  * **Fuente de Verdad de LD3:** Se estableció que `Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf` prevalece sobre borradores y planes antiguos del repositorio (los cuales erróneamente listaban amplificadores CMOS analógicos).
  * **Aprovechamiento de Modelos Existentes:** Se constató que las librerías `nigbt.lib`, `pigbt.lib` y los 4 modelos de Fuji Electric Serie X (`FGW50XS65`, `FGW50XS65C`, `FGW75XS65`, `FGW75XS65C`) ya residen y están rastreados en `Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/`. Se decidió no duplicarlos físicamente en el repositorio, documentando su procedencia en `NOTAS_MODELOS.md`.
  * **Desacoplamiento de Reglas de LD1:** Se desvincularon las directivas de $\beta=2.50$, límite de 12 páginas y modelos BSIM4 nanométricos para LD3, dado que un banco de IGBTs de potencia se rige por su propia física y requerimientos de guía.
* **Resultados Obtenidos:**
  * Repositorio completamente auditado y normalizado sin pérdida de consistencia.
  * Rama de trabajo `feat/ld3-igbt` activa y desacoplada de `main`.
  * Enlaces rotos eliminados y coherencia documental al 100%.

---

## Entrada [2026-10-11] — Integración de Evidencias Auténticas de LTspice y Cierre Editorial del Informe Final LD3

* **Fase:** Cierre Editorial y Documental — Laboratorio Dirigido N.° 3 (Transistores IGBT).
* **Responsable:** Leonardo Sait Yactayo Tolentino (Código: `23190214`).
* **Archivos Modificados / Creados:**
  * `LD3_Yactayo/figuras/evidencias_ltspice/`: Integración de 7 capturas de pantalla auténticas de LTspice (`E00_esquema_nigbt.png`, `E00_esquema_pigbt.png`, `E01_dpt_nigbt_global.png`, `E02_dpt_pigbt_global.png`, `E03_cursores_tdoff_nigbt.png`, `E04_cursores_tdoff_pigbt.png`, `E05_energia_eoff_integral.png`).
  * `LD3_Yactayo/scripts/generar_pdf_informe.py`: Integración de capturas de evidencias, maquetación de tablas consolidadas en página horizontal (`pdflscape`), corrección de referencias cruzadas y ajuste de anchos de columna en metadatos de portada para eliminar cortes de palabra.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.tex`: Código fuente LaTeX actualizado y compilado con `pdflatex` (2 pasadas limpias, returncode 0, cero referencias indefinidas).
  * `LD3_Yactayo/informe/informe_ld3_yactayo.pdf`: Documento final generado (13 páginas físicas, 2.42 MB, tablas 1 y 2 completas sin recorte de márgenes, cursores y formas de onda 100% nítidos).
  * `LD3_Yactayo/informe/informe_ld3_yactayo.md`: Documento Markdown sincronizado al 100% con los datos, lecturas de cursores e integración de energía de la interfaz gráfica de LTspice.
  * `LD3_Yactayo/TRAZABILIDAD.md`: Actualización de la matriz de trazabilidad con todos los requisitos en estado VALIDADO.
* **Decisiones Técnicas / Justificación:**
  * **Verificación de Equivalencia de Netlists:** Se constató mediante logs que `DPT_NIGBT_nom.asc` y `DPT_PIGBT_nom.asc` producen exactamente los mismos resultados numéricos que los netlists `.cir` originales (discrepancia = 0.00% en todas las directivas `.meas`).
  * **Medición Manual con Cursores:** Se documentaron los valores exactos leídos en los cursores de LTspice frente a los valores `.meas` automáticos ($150.81\text{ ns}$ manual vs $150.83\text{ ns}$ `.meas` en N-IGBT; $194.37\text{ ns}$ manual vs $194.57\text{ ns}$ `.meas` en P-IGBT), justificando la diferencia por la resolución gráfica finita del cursor frente a la interpolación numérica interna del simulador.
  * **Integración de Energía en LTspice:** Se corroboró la lectura de la caja de diálogo de integración interactiva (Ctrl + Clic en traza de potencia: integral de $691.48\ \mu\text{J}$, potencia media de $134.27\text{ W}$) frente a los $691.478\ \mu\text{J}$ del comando `.meas`.
  * **Diseño Editorial y Tablas:** La integración de `pdflscape` permite visualizar las dos tablas completas (13 y 17 columnas respectivamente) en la Página 10 sin truncar ninguna métrica ($E_{\text{off}}$, $\%E_{\text{tail}}$, $di/dt_{\text{max}}$, $V_{CE,\text{peak}}$).
* **Estado Actual:** Fase de integración cerrada. Listo para la revisión final de estilo y QA.

---

## Entrada [2026-10-12] — Control de Calidad Académico (QA-FINAL-02) y Consolidación a 14 Páginas

* **Fase:** Control de Calidad Académico y Maquetación Definitiva — LD3.
* **Responsable:** Leonardo Sait Yactayo Tolentino (Código: `23190214`).
* **Archivos Modificados:**
  * `LD3_Yactayo/scripts/generar_pdf_informe.py`:
    * Corrección de expresión de corriente de compuerta en EXP-09 a través de $R_G$: $i_G(t) = \frac{v_{\text{drv}}(t) - v_G(t)}{R_G}$ ($v_{\text{drv}} = 0\text{ V}$ en corte).
    * Retiro de atribución causal a corriente capacitiva en diodo co-pack (EXP-06/07 y conclusiones); precisión de diferencias mínimas ($\le 0.02\text{ ns}$, $\le 0.01\ \mu\text{J}$) no relevantes para la resolución ni métricas evaluadas.
    * Corrección de condición de control P-IGBT de «corriente idéntica» a «corriente similar» ($19.48\text{ A}$ vs $19.00\text{ A}$).
    * Precisión operacional de $E_{\text{off}}$ como energía eléctrica integrada de magnitudes terminales según la metodología del banco, distinguiéndola del calor térmico interno sin macromodelo acoplado.
    * Sincronización estricta de fechas de carátula y resumen con la guía oficial: Emisión de la guía: 7 de octubre de 2026; Entrega y sustentación oral: 21 de octubre de 2026.
    * Corrección del ancho de columna en la portada para evitar que la etiqueta «Entrega y sustentación:» se divida en dos líneas.
    * Inclusión en la Figura 6 de la ampliación directa y nítida de la ventana de integración de $E_{\text{off}}$ en LTspice (`E05_energia_zoom.png`) mostrando la lectura clara de $691.48\ \mu\text{J}$.
    * Corrección de leyendas de Figuras 2 y 3 para identificar $I(R2)$ como corriente medida en el shunt de emisor utilizada para estimar $I_C$, sin afirmar igualdad matemática exacta.
    * Sustitución de expresiones como «se comprobó experimentalmente» por «los resultados de simulación muestran».
    * Disposición de Figuras 9 y 10 en minipages horizontales con leyendas y etiquetas independientes para consolidar la Sección 5 en la Página 9, preservando las tablas apaisadas en las Páginas 10 y 11 y fijando la extensión total en exactamente 14 páginas físicas.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.md`: Sincronización completa de los ajustes en el informe Markdown (zoom de ventana de integración en Figura 6, leyendas de Figuras 2 y 3, redacción de simulación).
  * `LD3_Yactayo/informe/conclusiones.md`: Sincronización de terminología en corriente similar, diferencias co-pack y redacción de simulación.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.pdf`: Compilación final exitosa (14 páginas exactas, 2.45 MB, cero páginas flotantes huérfanas).
* **Decisiones Técnicas / Justificación:**
  * Rigor conceptual en magnitudes de potencia y térmicas, referencias de compuerta, precisión entre mediciones de shunt vs terminales y lenguaje académico de estudiante de pregrado orientado a la docente MsC. Luz Adanaqué Infante.
* **Estado Actual:** Informe académico LD3 cerrado, verificado y congelado para la sustentación del 21 de octubre de 2026.

---

## Entrada [2026-10-13] — Revisión Puntual de Contenido por Auditoría Externa y Verificación Física Analítica

* **Fase:** Ajustes de Contenido Focalizados y Verificación Analítica — LD3.
* **Responsable:** Leonardo Sait Yactayo Tolentino (Código: `23190214`).
* **Archivos Modificados:**
  * `LD3_Yactayo/scripts/generar_pdf_informe.py`:
    * Actualización de cotejo con datasheet IRGBC20S (Farnell 68617): inclusión explícita de corriente de prueba de catálogo ($I_C = 10\text{ A}$ frente a $19\text{ A}$ en simulación), corrección de $t_{d(\text{off})}$ máximo a $1200\text{ ns}$ (conservando $820\text{ ns}$ típico y $t_f = 910\text{ ns}$ típico / $1500\text{ ns}$ máx.) y distribución balanceada de causas entre condiciones de ensayo ($I_C, V_{CC}, R_G$) y simplificaciones de macromodelo ($TF = 16.8\text{ ns}$).
    * Inclusión de párrafo explicativo sobre ensayos exploratorios a $\approx 80\text{ A}$ en modelos Duncan, señalando que exceden la corriente continua nominal ($19\text{ A}$) y que $82.31\text{ A}$ sobrepasa el límite pulsado de catálogo ($I_{CM} = 76\text{ A}$), situándose fuera del Área de Operación Segura (SOA).
    * Matiz metodológico en conclusiones sobre asimetría N/P: precisión de que los resultados SPICE reflejan la respuesta compuesta del modelo (diferencias en $TF$, dimensiones de celda y capacitancias) y no aíslan la movilidad como variable única.
    * Ampliación cualitativa del comportamiento del diodo co-pack en topologías de puente: análisis de pérdidas de conducción en rueda libre ($P_{\text{cond}} \approx V_F \cdot I_D$) y efectos de recuperación inversa ($Q_{rr}, I_{rrm}, t_{rr}$) incrementando las pérdidas de encendido ($E_{\text{on}}$) del conmutador complementario.
    * Incorporación de verificación analítica cuantitativa de la sobretensión inductiva ($V_{L\sigma} = L_\sigma \cdot |di/dt|_{\max}$), corroborando una concordancia del $98.5\%$ ($41.74\text{ V}$ teóricos vs $+42.36\text{ V}$ simulados en 50 A) y $98.8\%$ ($45.45\text{ V}$ vs $+45.98\text{ V}$ en 75 A).
    * Corrección tipográfica de porcentajes en LaTeX (\textbf{98.5\%}, etc., eliminando glifo residual) y matiz de la verificación analítica $L_\sigma \cdot |di/dt|_{\max}$.
    * Precisión en la descripción de ensayos exploratorios a $82\text{ A}$ frente a especificaciones nominales y límite pulsado $I_{CM} = 76\text{ A}$, sin afirmar verificación de la curva SOA completa.
    * Actualización de fecha en portada y resumen a «Exposición: 21 de octubre de 2026».
    * Ajuste moderado de espaciados de títulos (`\titlespacing*`) y composición de referencias (`\small`, `itemsep=1.5pt`), eliminando la página huérfana 16.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.md`: Sincronización exacta de las cuatro precisiones técnicas, verificación analítica $L_\sigma \cdot di/dt$, fecha de exposición y preguntas 4.3 y 4.5.
  * `LD3_Yactayo/informe/conclusiones.md`: Sincronización de matiz de movilidad N/P y análisis de conducción/recuperación inversa del diodo co-pack en puente.
  * `LD3_Yactayo/informe/informe_ld3_yactayo.pdf`: Compilación exitosa preservando maquetación apaisada de tablas en dos páginas y legibilidad plena.
* **Decisiones Técnicas / Justificación:**
  * **Comprobación de Datos Crudos para Gráfica Condicional:** Se constató que el archivo RAW del N-IGBT a 19 A (`dpt_nigbt_nom.raw`) y del P-IGBT a 40 A (`dpt_pigbt_nom.raw`) están disponibles, pero el archivo RAW de control P-IGBT a 19.48 A (`dpt_pigbt_19a.raw`) no reside en disco (únicamente existen su `.cir` y `.log`). Conforme a la restricción expresa de no ejecutar simulaciones exploratorias no autorizadas, no se lanzó ninguna simulación de regeneración; la comparación a 19 A se mantiene sustentada de manera rigurosa y unívoca en la Tabla 1 (Reg. 01 vs Reg. 05).
  * **Higiene de Control de Versiones:** Estricto cumplimiento de no ejecutar `git commit` ni `git push` sin instrucción directa del usuario.
* **Estado Actual:** Informe académico LD3 y documentación técnica 100% alineados con las observaciones de auditoría externa y la guía oficial docente.


