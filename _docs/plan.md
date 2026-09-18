# Plan de Trabajo y Estado de Entregables (`_docs/plan.md`)

Este documento registra la planificación general del curso, el estado de los entregables de laboratorio dirigido (LD) y el seguimiento de tareas pendientes en el repositorio **Microelectronica-UNMSM**.

---

## 1. Cronograma de Laboratorios Dirigidos

| Entregable | Tema Principal | Estado | Hito / Fecha Clave |
| :--- | :--- | :---: | :--- |
| **LD1** | Inversor CMOS, márgenes de ruido, retardo transitorio, compuertas lógicas (NAND2/NOR2/AOI), fuga y oscilador de anillo | **COMPLETO (100%)** | Entregado en LaTeX (12 págs.) + SPICE verificado |
| **LD2** | Lógica CMOS Dinámica: Dominó, Compartición de Carga, Keepers y Operación NTV | **EN PROGRESO (Actividades 1 y 2 Cerradas)** | Semana 4 / 5 |
| **LD3** | Amplificadores CMOS Básicos y Espejos de Corriente (Analógica) | *Planificado* | Semana 7 / 8 |
| **LD4** | Amplificador Operacional CMOS / OTA y Respuesta en Frecuencia | *Planificado* | Post-Parcial |

---

## 2. Estado Detallado: Laboratorio Dirigido N.° 2 (LD2)

- [x] **Fase 2 (Calibración e Infraestructura):** Modelos PTM concurrentes (`ptm45hp.lib`, `ptm45lp.lib`, `ptm130.lib`), caracterización VTC inversor ($T=27^\circ\text{C}$ y $85^\circ\text{C}$), confirmación experimental de opciones de solver (`gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`), parsers SPICE LOG/RAW con test de regresión (15/15 PASS).
- [x] **Actividad 1 (NAND3 Dinámica Footed):**
  - Identificación de 4 fases de operación con reloj a 500 MHz y estímulo retrasado ($1.1\text{ ns}$).
  - Asimetría temporal: justificación de $t_{pLH,dyn}$ como tiempo muerto de precarga fuera de la ruta crítica de datos.
  - Tiempos de retardo: $t_{pHL,dyn} = 22.17\text{ ps}$, $t_{pLH,dyn} = 25.13\text{ ps}$, retardo de evaluación desde $CLK\uparrow \to OUT\uparrow = 35.89\text{ ps}$ (frente a $A\uparrow \to OUT\_STAT\downarrow = 9.61\text{ ps}$ en estática).
  - Control sin carga externa $C_L$: $t_{pHL,dyn} = 11.26\text{ ps}$, $t_{pd,\text{eval}} = 21.27\text{ ps}$.
  - Capacitancia de entrada: $C_{in,\text{dyn}} = 0.3415\text{ fF}$ vs $C_{in,\text{stat}} = 0.5936\text{ fF}$ (reducción de $42.5\%$).
  - Potencia bajo estímulo idéntico (125 MHz): $P_{\text{dyn}} = 1.2393\ \mu\text{W}$ vs $P_{\text{stat}} = 0.2692\ \mu\text{W}$ (ratio $4.604\times$).
  - Trampa de potencia con entradas fijas en 1: $P_{\text{dyn}} = 2.7255\ \mu\text{W}$ ($\alpha=1$) vs $P_{\text{stat}} = 1.7004\text{ nW}$ ($\alpha=0$) (ratio $1602.9\times$).
  - Retención con PDN abierta a $27^\circ\text{C}$: caída de $6.41\text{ mV}$ en $1\text{ ns}$ vs $116.28\text{ mV}$ en $200\text{ ns}$.
  - **Estado:** CERRADA (Auditada por Gemini 3.1 Pro High con GATE PASS WITH MINOR FIXES).
- [x] **Informe LaTeX (Integración de Actividad 1):** Portada oficial docente, Sección 1 (Metodología) y Sección 2 (Actividad 1) integradas modularmente. Tabla comparativa auto-generada desde JSON con `RaggedRight`. Figuras 1, 2 y 3 escaladas a 0.72\linewidth. Auditoría estructural estática PASS (0 errores de sintaxis; compilación TeX real delegada a TeX Live 2026 / Overleaf). Extensión estimada actual: ~7 páginas (1 Portada + ~6 págs de contenido).
- [x] **Actividad 2 (Compartición de Carga - Charge Sharing):**
  - Predicción analítica registrada previa a simulación (`prediccion_analitica_act2.md`).
  - Cálculo de geometrías de difusión ($Ad = 0.0243\ \mu\text{m}^2, Pd = 0.450\ \mu\text{m}$) y capacitancias ($C_a = C_{n1} + C_{n2} = 0.9486\text{ fF}$).
  - Simulación oficial de peor caso de la guía (ENS-A2-01) y benchmark físico (ENS-A2-02, $\Delta V = 101.03\text{ mV}$).
  - Explicación de la discrepancia de $2.5\times$ a $3.0\times$ entre la predicción analítica de reparto puro y la simulación: corte subumbral del NMOS pasante $M_2$ ($V_{GS} \le V_{th2}$) y capacitancia de unión no lineal.
  - Barrido paramétrico $C_L \in [0.5, 4.0]\text{ fF}$ (ENS-A2-03): comprobación de ausencia de fallo lógico ($V_{dyn,min} > V_{IH} = 0.5785\text{ V}, V_{out,max} \le 0.68\text{ mV}$).
  - Mitigación 1 (Precarga interna $n_1, n_2$, ENS-A2-04): eliminación completa de $\Delta V$ ($\le 0\text{ mV}$), justificación de por qué no precargar $n_3$, coste: $+2\text{ PMOS}, +0.36\text{ fF}$ en reloj.
  - Mitigación 2 (Reordenamiento PDN, ENS-A2-05): $C$ en el tope suprime $\Delta V$ a $14\ \mu\text{V}$ sin coste de área ni sobrecarga de reloj; justificación de decisión de diseño en dominó vs estática.
  - Mitigación 3 (Keeper $W_{kp} = 45\text{ nm}$, ENS-A2-06): amortiguamiento a $\Delta V = 42.18\text{ mV}$ ($-58.2\%$), restauración activa a $0.99\cdot V_{DD}$ en $t_{restore} = 80.30\text{ ps}$.
  - Evaluación de contención (ENS-A2-07): penalización en retardo de evaluación de $+3.51\text{ ps}$ ($+14.65\%$) en $t_{pHL,dyn}$ y $+5.52\text{ ps}$ ($+14.69\%$) en $t_{pLH,out}$.
  - 3 figuras a 300 DPI (`fig1_act2_peor_caso_formas_onda.png`, `fig2_act2_dv_vs_cl_analitico_simulado.png`, `fig3_act2_comparacion_mitigaciones.png`).
  - **Estado:** CERRADA (Auditada con GATE PASS final e integrada en el informe LaTeX).
- [ ] **Actividad 3 (Fugas y Dimensionamiento del Keeper en HP vs LP, 27°C vs 85°C):** No iniciada.
- [ ] **Actividad 4 (Lógica Dominó Multinivel):** No iniciada.
- [ ] **Actividad 5 (Latches y Flip-Flops):** No iniciada.

---

## 3. Estado Detallado: Laboratorio Dirigido N.° 1 (LD1)

- [x] **Marco Teórico (Pre-lab):** Deducción completa de $V_M$, condición de simetría con saturación de velocidad, esquema circuital y ecuaciones dinámicas.
- [x] **Actividad 1 (VTC & Ruido):** Barrido de $\beta \in [1.0, 3.0]$, determinación de $\beta_{\text{ópt}} = 2.50$, extracción de $V_{IL}, V_{IH}, NM_L, NM_H$ y parámetros PTM 45nm HP.
- [x] **Actividad 2 (Retardo Transitorio):** Simulación $t_p$ vs $C_L \in [1, 8]\text{ fF}$, ajuste lineal ($m = 1.846\text{ ps/fF}, t_0 = 2.708\text{ ps}$), y comparación multidécada (90nm, 45nm, 22nm).
- [x] **Actividad 3 (NAND2 vs NOR2):** Dimensionamiento con inversor de referencia ($\beta = 2.5$), análisis de nodo interno $n_x$ y conmutación externa vs interna.
- [x] **Actividad 4 (Compuerta Compleja AOI):** Síntesis planar dual de $Y = \overline{(A \cdot B) + C}$ (6T), dimensionamiento entero $\beta = 2.0$, corrección de estímulos y medición de peor caso $t_{pHL} = 13.19\text{ ps}$.
- [x] **Actividad 5 (Potencia y Fuga):** Compromiso velocidad/fuga entre 45nm HP y 45nm LP ($3.5\times$ velocidad vs $200\times$ fuga), oscilador de anillo de 5 etapas ($f_{osc} = 21.94\text{ GHz}$).
- [x] **Cuestionario:** 20 preguntas analíticas resueltas y justificadas físicamente.
- [x] **Netlists de Referencia:** Anexo A con 5 códigos limpios y comentados en el informe, sincronizados con `LD1_Arcila_Yactayo/simulaciones/`.

---

## 4. Próximos Pasos y Deuda Técnica

1. **Monitoreo de retroalimentación docente:** Incorporar comentarios de la profesora MsC. Luz Adanaqué cuando publique la calificación de LD1.
2. **Plantillas modulares:** Mantener la estructura limpia de scripts Python (`generar_*.py`) para reusarla en LD2.
3. **Control de versiones:** Sincronización continua en GitHub (`LE0ST/Microelectronica-UNMSM`) asegurando que ambos autores (Leonardo Yactayo y Marco Arcila) tengan el árbol al día.
