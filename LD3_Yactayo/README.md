# Laboratorio Dirigido N.° 3: Transistores IGBT en LTspice

**Universidad Nacional Mayor de San Marcos**<br>
*Facultad de Ingeniería Electrónica y Eléctrica (FIEE)*<br>
*Escuela Profesional de Ingeniería Electrónica*<br>
*Curso: Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)*

---

## 1. Información General del Laboratorio

* **Título Oficial:** *Caracterización y Simulación Comparativa de Transistores IGBT en LTspice*
* **Docente Responsable:** MsC. Luz Adanaqué Infante
* **Autor / Investigador:** **Leonardo Sait Yactayo Tolentino** (Código: `23190214`)
* **Modalidad:** **Individual** (respaldado por la guía oficial: *«El laboratorio puede ser en parejas o individual»*)
* **Estado:** **EN DESARROLLO** (fase de configuración de bancos DPT e inicialización de pruebas; simulaciones y resultados cuantitativos en proceso de ejecución)
* **Fecha de Exposición:** **21 de octubre de 2026**
* **Guía Oficial de Referencia:** [`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`](../Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf)

---

## 2. Objetivos y Alcance Técnico

El propósito de este laboratorio es la caracterización estática y dinámica de transistores bipolares de compuerta aislada (IGBT) en el entorno de simulación LTspice, analizando los compromisos de conmutación de potencia en régimen inductivo mediante el banco *Double Pulse Test* (DPT).

### Fenómenos Físicos y Métricas Investigadas:
1. **Dinámica de Conmutación en Canal N vs. Canal P:** Implementación del banco DPT en configuración de lado bajo (N-IGBT, polarización $0\to 15\text{ V}$) y lado alto (P-IGBT, polarización $0\to -15\text{ V}$).
2. **Corriente de Cola (Tail Current):** Identificación del inicio de la fase asintótica de cola en el segundo pulso de apagado y justificación física basada en la recombinación de portadores minoritarios en la región de deriva no modulada.
3. **Retardo de Apagado ($t_{d(\text{off})}$):** Medición con cursores y directivas `.meas` entre el 90% de $V_{GE}$ y el 90% de $I_C$, contrastando los resultados frente a las hojas de datos de fabricante.
4. **Energía de Apagado ($E_{\text{off}}$):** Integración numérica del producto $V_{CE} \cdot I_C$ durante el periodo de conmutación y cálculo del porcentaje de energía disipada atribuible a la corriente de cola.
5. **Sobretensión Transitoria por Inductancia Parásita:** Análisis del pico de voltaje $V_{CE,\text{peak}}$ provocado por $L \cdot di/dt$ durante el apagado brusco, contrastando los modelos con y sin diodo de marcha libre integrado (*co-pack*).
6. **Sensibilidad a la Resistencia de Compuerta ($R_G$):** Evaluación del impacto de duplicar $R_G$ (de $10\ \Omega$ a $20\ \Omega$) sobre las pérdidas de energía y la velocidad de respuesta.
7. **Escalamiento de Área de Silicio:** Contraste de pérdidas estáticas y dinámicas entre los módulos de 50 A (`FGW50XS65/C`) y 75 A (`FGW75XS65/C`) de la Serie X de Fuji Electric.

---

## 3. Dispositivos y Modelos SPICE

1. **Modelos Teóricos / Genéricos (Duncan Electronics):**
   * `N-IGBT`: Subcircuito `XIRGBC20S` (600 V, 19 A) en `nigbt.lib`.
   * `P-IGBT`: Subcircuito `XPIGBT` (600 V, 40 A) en `pigbt.lib`.
2. **Modelos Comerciales (Fuji Electric — Serie X Trench-FS 650 V):**
   * `FGW50XS65`: 650 V, 50 A (sin diodo co-empaquetado).
   * `FGW50XS65C`: 650 V, 50 A (con diodo rápido co-empaquetado).
   * `FGW75XS65`: 650 V, 75 A (sin diodo co-empaquetado).
   * `FGW75XS65C`: 650 V, 75 A (con diodo rápido co-empaquetado).

*Nota de procedencia:* Los modelos se encuentran alojados en `Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/` y se documentan en [`modelos/NOTAS_MODELOS.md`](modelos/NOTAS_MODELOS.md).

---

## 4. Estructura de Directorios de LD3

```
LD3_Yactayo/
├── esquemas/                               # Archivos .asc interactivos de LTspice
├── simulaciones/                           # Netlists .cir por lote y resultados (.log / .meas)
├── modelos/                                # Documentación de modelos y atribución de fuentes
│   └── NOTAS_MODELOS.md                    # Registro oficial de modelos Fuji y Duncan
├── scripts/                                # Post-procesamiento automatizado en Python
├── figuras/                                # Curvas y formas de onda vectoriales (300 DPI)
├── tablas/                                 # Tablas de resultados en Markdown y CSV
├── informe/                                # Reporte técnico (conclusiones >= 1 pág.)
├── README.md                               # [ESTE ARCHIVO] Presentación y runbooks de LD3
└── TRAZABILIDAD.md                         # Matriz de trazabilidad experimental biunívoca
```

---

## 5. Entregables Oficiales Según la Guía

* [ ] **Tabla de Resultados Completa:** Matriz cuantitativa con todas las métricas de conmutación ($I_{C,\text{tail}}$, $t_{d(\text{off})}$, $E_{\text{off}}$, $\%E_{\text{tail}}$, $V_{CE,\text{peak}}$).
* [ ] **Gráficas Comparativas de Transitorios:** Formas de onda claras de $V_{GE}$, $V_{CE}$ e $I_C$ priorizando la resolución temporal de conmutación.
* [ ] **Conclusiones Técnicas Fundamentadas:** Mínimo una página física analizando las diferencias entre canal N y P, impacto del diodo co-pack e influencia del área de silicio con física de semiconductores.
* [ ] **Exposición Oral de Hallazgos:** Presentación técnica programada para el **21 de octubre de 2026**.
