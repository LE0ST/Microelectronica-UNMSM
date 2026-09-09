# Plan de Trabajo y Estado de Entregables (`_docs/plan.md`)

Este documento registra la planificación general del curso, el estado de los entregables de laboratorio dirigido (LD) y el seguimiento de tareas pendientes en el repositorio **Microelectronica-UNMSM**.

---

## 1. Cronograma de Laboratorios Dirigidos

| Entregable | Tema Principal | Estado | Hito / Fecha Clave |
| :--- | :--- | :---: | :--- |
| **LD1** | Inversor CMOS, márgenes de ruido, retardo transitorio, compuertas lógicas (NAND2/NOR2/AOI), fuga y oscilador de anillo | **COMPLETO (100%)** | Entregado en LaTeX (12 págs.) + SPICE verificado |
| **LD2** | Lógica Dinámica, Celdas de Memoria SRAM y Circuitos Secuenciales | *Planificado* | Semana 4 / 5 |
| **LD3** | Amplificadores CMOS Básicos y Espejos de Corriente (Analógica) | *Planificado* | Semana 7 / 8 |
| **LD4** | Amplificador Operacional CMOS / OTA y Respuesta en Frecuencia | *Planificado* | Post-Parcial |

---

## 2. Estado Detallado: Laboratorio Dirigido N.° 1 (LD1)

- [x] **Marco Teórico (Pre-lab):** Deducción completa de $V_M$, condición de simetría con saturación de velocidad, esquema circuital y ecuaciones dinámicas.
- [x] **Actividad 1 (VTC & Ruido):** Barrido de $\beta \in [1.0, 3.0]$, determinación de $\beta_{\text{ópt}} = 2.50$, extracción de $V_{IL}, V_{IH}, NM_L, NM_H$ y parámetros PTM 45nm HP.
- [x] **Actividad 2 (Retardo Transitorio):** Simulación $t_p$ vs $C_L \in [1, 8]\text{ fF}$, ajuste lineal ($m = 1.846\text{ ps/fF}, t_0 = 2.708\text{ ps}$), y comparación multidécada (90nm, 45nm, 22nm).
- [x] **Actividad 3 (NAND2 vs NOR2):** Dimensionamiento con inversor de referencia ($\beta = 2.5$), análisis de nodo interno $n_x$ y conmutación externa vs interna.
- [x] **Actividad 4 (Compuerta Compleja AOI):** Síntesis planar dual de $Y = \overline{(A \cdot B) + C}$ (6T), dimensionamiento entero $\beta = 2.0$, corrección de estímulos y medición de peor caso $t_{pHL} = 13.19\text{ ps}$.
- [x] **Actividad 5 (Potencia y Fuga):** Compromiso velocidad/fuga entre 45nm HP y 45nm LP ($3.5\times$ velocidad vs $200\times$ fuga), oscilador de anillo de 5 etapas ($f_{osc} = 21.94\text{ GHz}$).
- [x] **Cuestionario:** 20 preguntas analíticas resueltas y justificadas físicamente.
- [x] **Netlists de Referencia:** Anexo A con 5 códigos limpios y comentados en el informe, sincronizados con `LD1_Arcila_Yactayo/simulaciones/`.

---

## 3. Próximos Pasos y Deuda Técnica

1. **Monitoreo de retroalimentación docente:** Incorporar comentarios de la profesora MsC. Luz Adanaqué cuando publique la calificación de LD1.
2. **Plantillas modulares:** Mantener la estructura limpia de scripts Python (`generar_*.py`) para reusarla en LD2.
3. **Control de versiones:** Sincronización continua en GitHub (`LE0ST/Microelectronica-UNMSM`) asegurando que ambos autores (Leonardo Yactayo y Marco Arcila) tengan el árbol al día.
