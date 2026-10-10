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
* **Pendientes / Próximos Pasos:**
  * [ ] Presentar reporte de cierre G1 y aguardar aprobación del usuario antes de cualquier commit o simulación.
  * [ ] Fase G2: Configuración circuital de esquemas DPT en `LD3_Yactayo/esquemas/` y ejecución de simulaciones transitorias SPICE de calibración (NIGBT vs PIGBT).
