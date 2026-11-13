# Plan de Trabajo y Estado de Entregables (`_docs/plan.md`)

Este documento registra la planificación general del curso, el estado de los entregables de laboratorio dirigido (LD) y el seguimiento de tareas pendientes en el repositorio **Microelectronica-UNMSM**.

---

## 1. Cronograma General de Laboratorios Dirigidos

| Entregable | Tema Principal | Autores | Estado | Hito / Fecha Clave |
| :--- | :--- | :--- | :---: | :--- |
| **LD1** | Inversor CMOS, márgenes de ruido, retardo transitorio, compuertas lógicas (NAND2/NOR2/AOI), fuga y oscilador de anillo | Leonardo Yactayo & Marco Arcila | **COMPLETO (100%)** | Entregado en LaTeX (12 págs.) + SPICE verificado |
| **LD2** | Lógica CMOS Dinámica: Dominó Footed/Unfooted, Compartición de Carga, Balance Causal de Fugas, Keeper y Operación NTV (5 actividades) | Leonardo Yactayo & Marco Arcila | **COMPLETO (100%)** | Integrado en `main`, informe oficial (20 págs. IEEE) |
| **LD3** | Caracterización y Simulación Comparativa de Transistores IGBT en LTspice (DPT, corriente de cola, $t_{d(\text{off})}$, $E_{\text{off}}$, $V_{CE,\text{peak}}$, $R_G$) | **Leonardo Yactayo** *(Individual)* | **EN PREPARACIÓN (Fase G1)** | Exposición de hallazgos: **21/10/2026** |
| **LD4** | Amplificadores y Diseños Avanzados (Tema por confirmar según calendario docente) | Por definir | *Planificado* | Post-Examen Parcial |

---

## 2. Estado Detallado: Laboratorio Dirigido N.° 3 (LD3) — *En Preparación*

* **Guía Oficial de Referencia:** [`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`](../Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf)
* **Modalidad:** Individual (Leonardo Sait Yactayo Tolentino).
* **Entregables Exigidos:**
  1. Tabla de resultados cuantitativos consolidada.
  2. Gráficas comparativas transitorias claras ($V_{GE}, V_{CE}, I_C$) en LTspice / Python.
  3. Análisis técnico y conclusiones fundamentadas con física de dispositivos ($\ge 1$ página física).
  4. Exposición oral de hallazgos el 21 de octubre de 2026.
* **Modelos y Circuitos Involucrados:**
  - Teóricos / Genéricos: `nigbt.lib` (`XIRGBC20S`), `pigbt.lib` (`XPIGBT`).
  - Comerciales Fuji Electric Serie X (650 V): `FGW50XS65`, `FGW50XS65C` (50 A), `FGW75XS65`, `FGW75XS65C` (75 A).
  - Banco *Double Pulse Test* (DPT): Lado bajo (N-IGBT) y lado alto (P-IGBT).
* **Hitos de Trabajo:**
  - [x] **Fase G0 (Auditoría Integral):** Identificación de fuente de verdad, modelos existentes y dependencias.
  - [x] **Fase G1 (Normalización y Trazabilidad):** Actualización documental, reglas operativas y matriz de trazabilidad.
  - [ ] **Fase G2 (Banco DPT y Simulación N vs P):** Configuración de circuitos DPT, barridos transitorios de doble pulso y extracción de corriente de cola y $t_{d(\text{off})}$.
  - [ ] **Fase G3 (Caracterización Fuji Serie X):** Evaluación comparativa 50 A vs 75 A, impacto de diodo co-empaquetado y sensibilidad a $R_G$.
  - [ ] **Fase G4 (Post-procesamiento y Redacción):** Generación de figuras a 300 DPI, consolidación de tabla de resultados y redacción de conclusiones ($\ge 1$ página).
  - [ ] **Fase G5 (Cierre y Preparación de Exposición):** Auditoría final y preparación de diapositivas/puntos clave para el 21/10/2026.

---

## 3. Estado Detallado: Laboratorio Dirigido N.° 2 (LD2) — *Completado*

* **Autores:** Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander.
* **Informe Técnico Oficial:** [`LD2_Arcila_Yactayo/informe_latex/main.pdf`](../LD2_Arcila_Yactayo/informe_latex/main.pdf) (20 páginas físicas exactas bajo estándar IEEE).
* **Actividades Realizadas:**
  - [x] **Actividad 1 (NAND3 Dinámica Footed vs. Estática):** Reducción de capacitancia de entrada ($-42.4\%$), asimetría temporal de precarga/evaluación y trampa de consumo dinámico.
  - [x] **Actividad 2 (Compartición de Carga - Charge Sharing):** Análisis analítico y experimental de peor caso sincrónico ($\Delta V = 164.29\text{ mV}$ con $C_L = 2.0\text{ fF}$) y mitigaciones (precarga interna, reordenamiento de PDN, keeper activo).
  - [x] **Actividad 3 (Balance Causal de Fugas y Keeper):** Descomposición física a 27 °C y 85 °C (subumbral, gate tunneling, GIDL) y ventana de viabilidad del keeper frente a contención (*ratioed fighting*).
  - [x] **Actividad 4 (Monotonicidad y Skew de Reloj en Cascada Dominó):** Caracterización de falla lógica por entrada no monótona y ventana admisible de skew para celdas footed y unfooted.
  - [x] **Actividad 5 (Régimen Near-Threshold Voltage y Feedthrough):** Operación a tensión reducida ($V_{DD} \in [0.35, 1.00]\text{ V}$), compromiso energía-retardo y supresión de feedthrough capacitivo.
  - [ ] **Actividad 6 (Lógica Dinámica Multietapa):** Módulo de extensión opcional, no desarrollado en la entrega final.
* **Estado:** CERRADO e integrado en la rama `main`.

---

## 4. Estado Detallado: Laboratorio Dirigido N.° 1 (LD1) — *Completado*

* **Autores:** Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander.
* **Informe Técnico Oficial:** [`LD1_Arcila_Yactayo/informe_latex/LD1_Arcila_Yactayo.pdf`](../LD1_Arcila_Yactayo/informe_latex/LD1_Arcila_Yactayo.pdf) (12 páginas formato IEEE).
* **Actividades Realizadas:**
  - [x] **Actividad 1 (VTC & Ruido):** Barrido de $\beta \in [1.0, 3.0]$, obtención de $\beta_{\text{ópt}} = 2.50$ ($V_M = 0.4989\text{ V}$) y márgenes $NM_L/NM_H$.
  - [x] **Actividad 2 (Retardo Transitorio):** Caracterización $t_p$ vs $C_L$ y escalamiento multidécada (90 nm, 45 nm, 22 nm PTM BSIM4).
  - [x] **Actividad 3 (NAND2 vs NOR2):** Dimensionamiento equivalente de resistencia de conmutación y análisis de nodo interno.
  - [x] **Actividad 4 (Compuerta Compleja AOI):** Síntesis planar dual de $Y = \overline{(A \cdot B) + C}$ (6T) con $\beta = 2.0$.
  - [x] **Actividad 5 (Potencia y Fuga):** Compromiso 45nm HP vs 45nm LP y oscilador en anillo de 5 etapas ($f_{osc} = 21.94\text{ GHz}$).
  - [x] **Cuestionario y Anexos:** 20 preguntas analíticas justificadas físicamente y netlists reproducibles.
* **Estado:** CERRADO e integrado en la rama `main`.

---

## 5. Próximos Pasos y Registro de Tareas Inmediatas

1. **Infraestructura LD3:** Completar la normalización de `README.md`, `AGENTS.md`, `CLAUDE.md`, `process.md` y bitácora.
2. **Matriz de Trazabilidad LD3:** Establecer la plantilla inicial con todos los ensayos en estado PENDIENTE.
3. **Simulaciones DPT (G2):** Ejecutar los circuitos esquemáticos existentes en `Semana_02/.../05_Laboratorio_IGBT/` asegurando rutas relativas reproducibles.
