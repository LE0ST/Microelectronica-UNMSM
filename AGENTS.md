# Context Engineering & Agent Operating Guidelines: Microelectronica-UNMSM

Este archivo define la infraestructura de contexto, reglas de operación, comandos predefinidos y rutas de documentación viva que todo agente de inteligencia artificial (incluyendo **Antigravity** y agentes autónomos) debe leer e incorporar de inmediato al iniciar una sesión de trabajo en este repositorio.

---

## 1. Identidad y Misión del Proyecto

* **Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — Facultad de Ingeniería Electrónica y Eléctrica (FIEE).
* **Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II).
* **Docente:** MsC. Luz Adanaqué Infante.
* **Autores:**
  * **Leonardo Sait Yactayo Tolentino** (`23190214`) — Coautor de LD1 y LD2; Autor individual de LD3.
  * **Marco Antonio Arcila Santander** (`23190140`) — Coautor de LD1 y LD2.
* **Propósito:** Diseño, simulación física SPICE (BSIM4 / PTM nanométrico y transistores de potencia IGBT en LTspice), post-procesamiento analítico cuantitativo en Python y redacción de informes técnicos de alto impacto.

---

## 2. Mapa Arquitectónico del Repositorio

```
MicroNano/
├── AGENTS.md                              # [ESTE ARCHIVO] Context Engineering y reglas operativas del agente
├── CLAUDE.md                              # Interoperabilidad con Claude Code y LLM harnesses
├── README.md                              # Descripción general pública del repositorio
│
├── _docs/                                 # DOCUMENTACIÓN VIVA DEL PROYECTO
│   ├── bitacora.md                        # Bitácora cronológica global de desarrollo
│   ├── process.md                         # Protocolo de laboratorio, simulación y QA
│   └── plan.md                            # Cronograma semestral y estado de entregables
│
├── LD1_Arcila_Yactayo/                    # LABORATORIO DIRIGIDO N.° 1: Lógica CMOS Estática (Cerrado)
│   ├── informe_latex/                     # Documento maestro IEEE (12 págs.) y figuras vectoriales
│   │   └── LD1_Arcila_Yactayo.pdf         # Reporte oficial final compilado
│   ├── simulaciones/                      # Netlists SPICE por actividad (A1 a A5)
│   ├── modelos/                           # Modelos predictivos PTM (BSIM4)
│   └── scripts/                           # Generadores Python de curvas y esquemas
│
├── LD2_Arcila_Yactayo/                    # LABORATORIO DIRIGIDO N.° 2: Lógica CMOS Dinámica (Cerrado)
│   ├── informe_latex/                     # Código LaTeX y reporte oficial (20 págs. IEEE)
│   │   └── main.pdf                       # Reporte oficial final compilado
│   ├── act1/ a act5/                      # Actividades desarrolladas de dominó, fugas, keeper y NTV
│   ├── modelos/                           # Librerías PTM concurrentes (45nm HP/LP, 130nm)
│   └── trazabilidad_figuras.txt           # Matriz biunívoca de reproducibilidad
│
├── LD3_Yactayo/                           # LABORATORIO DIRIGIDO N.° 3: Transistores IGBT en LTspice (Individual)
│   ├── esquemas/                          # Archivos esquemáticos interactivos .asc de LTspice
│   ├── simulaciones/                      # Netlists .cir y resultados trazables de simulación
│   ├── modelos/                           # Registro y notas de procedencia de modelos SPICE
│   ├── scripts/                           # Scripts Python para extracción de métricas y figuras
│   ├── figuras/                           # Formas de onda y gráficas comparativas a 300 DPI
│   ├── tablas/                            # Tablas de resultados cuantitativos
│   ├── informe/                           # Documento del reporte técnico (conclusiones >= 1 pág.)
│   ├── README.md                          # Guía rápida de reproducción LD3
│   └── TRAZABILIDAD.md                    # Matriz biunívoca de experimentos y figuras
│
├── Semana_01/ a Semana_05/                # Fundamentos CMOS, guías oficiales LD1 y LD2, teoría y ejercicios
├── Semana_07/                             # Guía oficial LD3 (LabDirigidoNro03.pdf) y notas de aplicación IGBT
└── Semana_09/ a Semana_12/                # Microsensores, actuadores, DFT y confiabilidad
```

---

## 3. Comandos Predefinidos (Runbooks & Execution)

Todo agente que opere en este repositorio debe utilizar exclusivamente las siguientes herramientas verificadas en el entorno local (Windows PowerShell / Python 3.14):

### A. Simulación SPICE (LTspice en Windows)
Ubicación del ejecutable: `G:\LTspice\LTspice.exe` (o ejecutable disponible en `PATH`).

* **Ejecutar simulación en modo batch (silencioso):**
  ```powershell
  & "G:\LTspice\LTspice.exe" -b "ruta\al\archivo.cir"
  ```
* **Inspeccionar mediciones cuantitativas (`.meas` en el `.log`):**
  ```powershell
  Get-Content "ruta\al\archivo.log" | Select-String -Pattern "vm|tphl|tplh|tp|tosc|fosc|tpd|iavg|ileak|td_off|eoff|itail|vce_max"
  ```

### B. Generación de Gráficas Científicas y Métricas (Python)
Todos los scripts emplean `matplotlib`, `numpy`, `scipy` y guardan figuras a 300 DPI con ejes rotulados.

* **Ejecutar script de post-procesamiento:**
  ```powershell
  python ruta\al\script.py
  ```

### C. Flujo Seguro de Control de Versiones (Git)
Queda prohibido el uso de `git add .` indiscriminado o confirmaciones directas sobre `main` en desarrollo activo.

* **Comprobar estado del árbol:**
  ```powershell
  git status
  ```
* **Adición selectiva y commit estructurado en rama de desarrollo:**
  ```powershell
  git add archivo1.ext archivo2.ext
  git commit -m "tipo(alcance): descripcion clara en presente"
  ```

---

## 4. Reglas Operativas e Innegociables

### A. Reglas Globales (Obligatorias en Todo el Repositorio)

1. **Cero Invención / Cero Fabricación de Datos (Zero Hallucination):**
   * Queda estrictamente prohibido reportar retardos, frecuencias, corrientes, energías o sobretensiones inventadas o estimadas a ojo.
   * Todo valor numérico debe provenir de una simulación real ejecutada en LTspice (`.meas` comprobable) o de una deducción analítica respaldada por fórmulas.
2. **Trazabilidad Experimental Biunívoca:**
   * Toda figura y tabla debe asociarse a su esquema, netlist y comando de medición en la matriz de trazabilidad del módulo correspondiente.
3. **Inmutabilidad de Modelos de Referencia:**
   * No editar directamente las tarjetas de modelo provistas por fabricantes o centros de investigación (PTM de NIMO, macro-modelos de Fuji Electric o Duncan Electronics).
4. **Respaldo Físico Riguroso:**
   * Los análisis técnicos y cuestionarios deben explicarse mediante los fenómenos físicos de semiconductores involucrados (saturación de velocidad, portadores minoritarios en región de deriva, tiempo de recombinación, modulación de conductividad, inductancias parásitas $L \cdot di/dt$, etc.).
5. **Higiene Estricta del Repositorio:**
   * Prohibido cometer archivos binarios pesados (`.raw`, `.op.raw`, `.db`, `.tmp`) a Git. Mantener `.gitignore` riguroso.
6. **Desarrollo en Ramas Temáticas:**
   * Todo trabajo nuevo en curso se realiza en una rama dedicada (ej. `feat/ld3-igbt`) antes de cualquier integración a `main`.

---

### B. Requisitos Específicos por Laboratorio

* **Laboratorio Dirigido N.° 1 (CMOS Estático):**
  * Calibración de $\beta_{\text{ópt}} = 2.50$ para centrado estático ($V_M = 0.4989\text{ V}$); compuerta compleja con $\beta = 2.0$.
  * Límite estricto de 12 páginas en informe IEEE.
* **Laboratorio Dirigido N.° 2 (CMOS Dinámico):**
  * 5 actividades desarrolladas (NAND3 dinámica, charge sharing, balance causal de fugas y keeper, monotonicidad y NTV). Actividad 6 opcional no desarrollada.
  * Informe técnico oficial de 20 páginas físicas IEEE.
* **Laboratorio Dirigido N.° 3 (Transistores IGBT):**
  * **Autor:** Leonardo Sait Yactayo Tolentino (*Modalidad Individual*).
  * **Fuente Oficial:** [`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`](file:///G:/Proyectos/MicroNano/Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf).
  * **Modelos:** Duncan Electronics (`nigbt.lib`, `pigbt.lib`) y Fuji Electric Serie X (`FGW50XS65/C`, `FGW75XS65/C`).
  * **Ensayos:** Banco *Double Pulse Test* (DPT), corriente de cola (*tail current*), retardo de apagado ($t_{d(\text{off})}$ 90% a 90%), energía de apagado ($E_{\text{off}}$), sobretensión pico por inductancia parásita ($V_{CE,\text{peak}}$) e influencia de $R_G$.
  * **Entregables:** Tabla de resultados completa, gráficas comparativas de transitorios ($V_{GE}, V_{CE}, I_C$), conclusiones técnicas fundamentadas ($\ge 1$ página) y exposición oral programada para el **21 de octubre de 2026**.
  * **Reglas particulares:** No aplican reglas de $\beta$ CMOS ni límites arbitrarios de 12 páginas; el desarrollo se rige estrictamente por su guía oficial.

---

## 5. Rutas a la Documentación Viva

El agente debe consultar y mantener actualizados los siguientes documentos de referencia:

* [**`_docs/bitacora.md`**](file:///G:/Proyectos/MicroNano/_docs/bitacora.md): Registro cronológico global de desarrollo y decisiones de diseño.
* [**`_docs/process.md`**](file:///G:/Proyectos/MicroNano/_docs/process.md): Protocolo detallado de simulación SPICE, generación de figuras y QA.
* [**`_docs/plan.md`**](file:///G:/Proyectos/MicroNano/_docs/plan.md): Hoja de ruta del curso y estado de avance de entregables.
* [**`Semana_02/Guia_Oficial_LD1/LabDirigidoNro01.pdf`**](file:///G:/Proyectos/MicroNano/Semana_02/Guia_Oficial_LD1/LabDirigidoNro01.pdf): Enunciado oficial del Laboratorio Dirigido N.° 1.
* [**`Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf`**](file:///G:/Proyectos/MicroNano/Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf): Enunciado oficial del Laboratorio Dirigido N.° 2.
* [**`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`**](file:///G:/Proyectos/MicroNano/Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf): Enunciado oficial del Laboratorio Dirigido N.° 3.
