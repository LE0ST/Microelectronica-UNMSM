# Proceso Operativo y Protocolo de Laboratorio (`_docs/process.md`)

Este documento establece el protocolo estándar de ingeniería para la ejecución de simulaciones SPICE, extracción cuantitativa de parámetros, generación de figuras de alta resolución, redacción técnica y control de calidad académico en el repositorio **Microelectronica-UNMSM**.

---

## 1. Ciclo de Vida Estándar de una Actividad de Laboratorio

Todo laboratorio en este repositorio sigue un flujo secuencial riguroso de 5 fases:

```
[ 1. Pre-Lab Teórico ] ──> [ 2. Netlist / Esquema SPICE ] ──> [ 3. Simulación & .meas ]
                                                                       │
[ 5. Auditoría & Cierre ] <── [ 4. Gráficas & Redacción ] <────────────┘
```

1. **Fase 1: Análisis Teórico y Pre-Lab:**
   * Consultar la guía docente oficial en `Semana_XX/Guia_Oficial_*/`.
   * Deducir analíticamente los puntos de operación, ecuaciones constitutivas y transitorios esperados.
   * Identificar la física subyacente: regímenes de transporte (saturación de velocidad, portadores minoritarios en base ancha, tiempo de recombinación, modulación de conductividad).
2. **Fase 2: Configuración Circuital SPICE:**
   * Diseñar esquemas interactivos (`.asc`) o netlists limpios (`.cir`).
   * Incluir modelos de componentes mediante rutas relativas reproducibles (`.include`).
   * Configurar estímulos limpios y realistas (tiempos de subida/bajada $t_r, t_f$ no nulos para evitar discontinuidades matemáticas).
3. **Fase 3: Simulación por Lote y Medición Automática:**
   * Ejecutar simulaciones en modo batch o interactivo en LTspice.
   * Utilizar directivas `.meas` para todas las magnitudes cuantitativas clave (retardos, corrientes, energías, picos de sobretensión).
   * Inspeccionar el archivo `.log` generado. **Queda terminantemente prohibido inventar o estimar cifras a ojo.**
4. **Fase 4: Post-procesamiento y Redacción:**
   * Extraer métricas a formatos estructurados y trazables (CSV, JSON o tablas Markdown).
   * Generar figuras vectoriales o PNG a 300 DPI mediante scripts en Python (`matplotlib`), con ejes completamente rotulados, unidades físicas claras y anotaciones de puntos críticos.
   * Redactar el informe correspondiente cumpliendo las pautas docentes (ej. conclusiones justificadas físicamente).
5. **Fase 5: Auditoría, QA y Control de Versiones:**
   * Verificar la correspondencia biunívoca entre la matriz de trazabilidad, las tablas y las gráficas.
   * Validar que ningún archivo binario pesado (`.raw`, `.op.raw`) sea incorporado a Git.
   * Confirmar mediante commits estructurados en la rama de desarrollo correspondiente (`feat/...`).

---

## 2. Reglas Globales e Innegociables (Aplica a Todos los Laboratorios)

Las siguientes 6 directivas rigen de forma universal en el repositorio y **NUNCA** deben ser vulneradas:

1. **Cero Invención / Cero Fabricación de Datos (Zero Hallucination):**
   * Todo valor numérico, retardo, energía o corriente reportada debe provenir de una simulación real ejecutada en LTspice o de un cálculo analítico formalmente documentado.
2. **Trazabilidad Experimental Biunívoca:**
   * Cada figura, tabla y afirmación cuantitativa debe estar mapeada a su esquema, netlist y registro de medición en la matriz de trazabilidad del laboratorio respectivo.
3. **Inmutabilidad de Modelos de Referencia:**
   * Los archivos de modelos provistos por fabricantes o instituciones (modelos PTM de NIMO, macro-modelos Fuji Electric o Duncan Electronics) son de solo lectura. No deben alterarse sus parámetros internos para forzar resultados.
4. **Respaldo Físico Riguroso:**
   * Las preguntas y análisis no se responden con generalidades. Deben explicarse los mecanismos físicos de semiconductores involucrados (saturación de velocidad, recombinación de portadores, modulación de conductividad, DIBL, inductancias parásitas $L \cdot di/dt$, etc.).
5. **Higiene Estricta del Repositorio:**
   * Queda prohibido cometer a Git archivos binarios de simulación masiva (`*.raw`, `*.op.raw`, `*.db`, `*.tmp`). Mantener `.gitignore` riguroso.
6. **Flujo Seguro de Control de Versiones:**
   * El desarrollo activo se realiza en ramas temáticas dedicadas (ej. `feat/ld3-igbt`), no directamente sobre `main`.
   * Prohibido el uso de `git add .` indiscriminado. Se deben añadir archivos explícitamente (`git add <archivo>`).

---

## 3. Requisitos Específicos por Laboratorio

### A. Laboratorio Dirigido N.° 1 (Lógica CMOS Estática) — *Cerrado*
* **Autores:** Leonardo Yactayo & Marco Arcila.
* **Tecnología:** PTM BSIM4 45 nm HP/LP, 90 nm Bulk y 22 nm HP.
* **Parámetro $\beta$:** Calibración en Actividad 1 con $\beta_{\text{ópt}} = 2.50$ ($V_M \approx V_{DD}/2 = 0.500\text{ V}$); propagado a compuertas estándar y oscilador en anillo; compuerta compleja con $\beta = 2.0$.
* **Extensión del Informe:** Máximo 12 páginas bajo estándar IEEE.

### B. Laboratorio Dirigido N.° 2 (Lógica CMOS Dinámica) — *Cerrado*
* **Autores:** Leonardo Yactayo & Marco Arcila.
* **Tecnología:** PTM BSIM4 45 nm HP/LP y 130 nm Bulk.
* **Alcance:** 5 actividades desarrolladas (Dinámica vs. Estática, Charge Sharing y Mitigaciones, Fugas y Keeper a 27 °C/85 °C, Monotonicidad y Skew en Cascada, Régimen NTV). Actividad 6 opcional no desarrollada.
* **Extensión del Informe:** 20 páginas físicas exactas bajo estándar IEEE.

### C. Laboratorio Dirigido N.° 3 (Transistores IGBT en LTspice) — *En Preparación*
* **Autor:** Leonardo Sait Yactayo Tolentino (*Modalidad Individual*).
* **Tecnología:** Transistores bipolares de compuerta aislada (IGBT):
  - Modelos teóricos: `NIGBT` (`XIRGBC20S`), `PIGBT` (`XPIGBT`).
  - Modelos comerciales: Fuji Electric Serie X 650 V (`FGW50XS65`, `FGW50XS65C`, `FGW75XS65`, `FGW75XS65C`).
* **Circuito de Prueba:** Banco *Double Pulse Test* (DPT) para lado bajo (N) y lado alto (P).
* **Métricas Clave:** Corriente de cola (*tail current*), retardo de apagado ($t_{d(\text{off})}$ entre 90% $V_{GE}$ y 90% $I_C$), energía de conmutación de apagado ($E_{\text{off}}$), sobretensión pico por inductancia parásita ($V_{CE,\text{peak}}$ con y sin diodo integrado) e influencia de $R_G$ (nominal vs. duplicado).
* **Entregables:**
  - Tabla de resultados comparativa completa.
  - Gráficas transitorias ordenadas ($V_{GE}, V_{CE}, I_C$) en LTspice / Python.
  - Conclusiones de mínimo una página física con fundamentos físicos detallados.
  - Exposición técnica programada para el **21 de octubre de 2026**.
* **Nota Operativa:** No aplican reglas de $\beta$ CMOS ni límites arbitrarios de 12 páginas. El laboratorio se rige estrictamente por su guía oficial.

---

## 4. Protocolo de Modelos y Datos Cuantitativos

1. **Modelos Predictivos PTM (BSIM4):** Empleados en celdas lógicas CMOS integradas. Requieren definición de parámetros $W_n, W_p, L_{min}$.
2. **Macromodelos Discretos de Potencia (IGBT):** Emplean subcircuitos (`.SUBCKT`) de fabricantes o modelos teóricos. En LTspice se instancian con prefijo de componente `X` (no `Z`), asignando el nombre del subcircuito en el atributo `Value`.
3. **Persistencia de Métricas:** Para evitar depender de archivos `.log` ignorados por Git, se promueve la extracción automatizada de resultados hacia tablas en Markdown (`.md`), archivos `.csv` o `.json` dentro del directorio del laboratorio.
