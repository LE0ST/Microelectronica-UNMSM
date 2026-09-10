# Context Engineering & Agent Operating Guidelines: Microelectronica-UNMSM

Este archivo define la infraestructura de contexto, reglas de operación, comandos predefinidos y rutas de documentación viva que todo agente de inteligencia artificial (incluyendo **Antigravity** y agentes de codificación autónomos) debe leer e incorporar de inmediato al iniciar una sesión de trabajo en este repositorio.

---

## 1. Identidad y Misión del Proyecto

* **Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — Facultad de Ingeniería Electrónica y Eléctrica (FIEE).
* **Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II).
* **Docente:** MsC. Luz Adanaqué Infante.
* **Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140).
* **Propósito:** Diseño, simulación física SPICE (BSIM4 / PTM submicrométrico), post-procesamiento analítico en Python y redacción de informes técnicos de alto impacto en LaTeX bajo estándar IEEE.

---

## 2. Mapa Arquitectónico del Repositorio

```
MicroNano/
├── AGENTS.md                              # [ESTE ARCHIVO] Context Engineering y reglas operativas del agente
├── CLAUDE.md                              # Interoperabilidad con Claude Code y LLM harnesses
├── README.md                              # Descripción general pública del proyecto
│
├── _docs/                                 # DOCUMENTACIÓN VIVA DEL PROYECTO
│   ├── process.md                         # Protocolo de laboratorio, simulación y QA
│   └── plan.md                            # Cronograma semestral y estado de entregables
│
├── LD1_Arcila_Yactayo/                    # LABORATORIO DIRIGIDO N.° 1 (Oficial)
│   ├── informe_latex/                     # Código fuente LaTeX y figuras del reporte
│   │   ├── LD1.tex                        # Documento maestro (máx 12 páginas, formato IEEE)
│   │   └── figuras/                       # Gráficas generadas a 300 DPI con ejes rotulados
│   ├── simulaciones/                      # Netlists SPICE organizadas por actividad (A1 a A5)
│   ├── modelos/                           # Modelos predictivos PTM (BSIM4) y librerías .lib
│   └── scripts/                           # Generadores Python de curvas y esquemas circuitales
│
├── Semana_01/                             # Inversor CMOS elemental y fundamentos
├── Semana_02/                             # Guía oficial LD1, rúbricas y simulaciones base de la docente
└── Semana_03/                             # Modelamiento CMOS avanzado y ejercicios teóricos
```

---

## 3. Comandos Predefinidos (Runbooks & Execution)

Todo agente que opere en este repositorio debe utilizar exclusivamente los siguientes comandos y herramientas verificadas en el entorno local (Windows PowerShell / Python 3.14):

### A. Simulación SPICE (LTspice en Windows)
El ejecutable de LTspice está ubicado en `G:\LTspice\LTspice.exe`.

* **Ejecutar simulación en modo batch (silencioso):**
  ```powershell
  & "G:\LTspice\LTspice.exe" -b "LD1_Arcila_Yactayo\simulaciones\A1_Inversor_VTC\A1_VTC.cir"
  ```
* **Leer resultados cuantitativos (`.meas` en el `.log`):**
  ```powershell
  Get-Content "LD1_Arcila_Yactayo\simulaciones\A1_Inversor_VTC\A1_VTC.log" | Select-String -Pattern "vm|tphl|tplh|tp|tosc|fosc|tpd|iavg|ileak"
  ```

### B. Generación y Regeneración de Figuras Científicas
Todos los scripts emplean `matplotlib` y guardan automáticamente en `LD1_Arcila_Yactayo/informe_latex/figuras/`.

* **Regenerar esquema circuital del inversor CMOS:**
  ```powershell
  python LD1_Arcila_Yactayo\scripts\generar_esquema_inversor.py
  ```
* **Regenerar esquema de la compuerta compleja (topología + dimensionamiento):**
  ```powershell
  python LD1_Arcila_Yactayo\scripts\generar_esquema_compleja.py
  ```
* **Regenerar figuras analíticas de simulación (Fig 1, Fig 2, Fig 3, Fig 4):**
  ```powershell
  python LD1_Arcila_Yactayo\scripts\generar_fig2.py
  python LD1_Arcila_Yactayo\scripts\generar_comparativa_nodos.py
  python LD1_Arcila_Yactayo\scripts\generar_fig3.py
  python LD1_Arcila_Yactayo\scripts\generar_graficas.py
  ```

### C. Verificación y Auditoría de LaTeX
* **Auditoría de balance de entornos y bloques matemáticos:**
  ```powershell
  python -c "
  with open('LD1_Arcila_Yactayo/informe_latex/LD1.tex', 'r', encoding='utf-8') as f:
      text = f.read()
  import re
  begins = re.findall(r'\\begin\{([^}]+)\}', text)
  ends = re.findall(r'\\end\{([^}]+)\}', text)
  diffs = {b: begins.count(b) - ends.count(b) for b in set(begins + ends) if begins.count(b) != ends.count(b)}
  print('Balance OK!' if not diffs else f'Desbalance: {diffs}')
  "
  ```

### D. Flujo de Control de Versiones (Git)
* **Comprobar estado limpio:**
  ```powershell
  git status
  ```
* **Sincronización con GitHub:**
  ```powershell
  git pull origin main
  git add .
  git commit -m "tipo(alcance): descripcion en presente"
  git push origin main
  ```

---

## 4. Reglas Duras e Innegociables (Hard Constraints)

El agente **NUNCA** debe violar las siguientes directivas bajo ninguna circunstancia:

1. **Cero Invención / Cero Fabricación de Datos (Zero Hallucination):**
   * Queda estrictamente prohibido colocar valores de retardo ($t_p$), márgenes de ruido ($NM$), frecuencias ($f_{osc}$) o corrientes de fuga ($I_{leak}$) inventados o estimados al ojo.
   * Todo valor numérico en el informe debe provenir de una simulación real ejecutada en LTspice o de una deducción analítica respaldada por fórmulas.
2. **Jerarquía Rigurosa del Parámetro $\beta$:**
   * **Actividad 1:** Barrido de $\beta \in [1.0, 3.0]$. La simulación concluye un valor óptimo de centrado estático ($V_M \approx V_{DD}/2 = 0.500\text{ V}$) en **$\beta_{\text{ópt}} = 2.50$** ($V_M = 0.4989\text{ V}$).
   * **Actividades 2, 3 y 5:** El inversor de referencia **DEBE** usar $\beta = 2.50$ ($W_n = 180\text{ nm}, W_p = 450\text{ nm}$ en 45nm HP). Las compuertas estándar NAND2 y NOR2 se dimensionan conservando esa resistencia de conmutación ($W_{p,\text{NAND}} = 450\text{ nm}$, $W_{p,\text{NOR}} = 900\text{ nm}$). El oscilador de anillo conecta en cascada inversores con $\beta = 2.50$.
   * **Actividad 4 (Compuerta Compleja):** Adopta $\beta = 2.0$ ($W_{n}=180\text{ nm}, W_{p}=2\beta W_n=720\text{ nm}$) según la especificación de la netlist oficial para razones enteras en layout multinivel. Cualquier diferencia debe estar explícitamente justificada en el texto.
3. **Límite Estricto de 12 Páginas en LaTeX:**
   * El informe oficial no debe superar bajo ningún concepto las 12 páginas impuestas en la rúbrica docente.
   * No reducir márgenes artificialmente (`geometry` está fijado en 1.8 cm). Ajustar la concisión del texto y el tamaño relativo de figuras (`width=0.74\textwidth`).
4. **Respaldo Físico en Cuestionarios:**
   * Las preguntas no se responden con respuestas genéricas ni monosílabos. Deben explicarse los fenómenos físicos subyacentes: saturación de velocidad, DIBL (`eta0`), modulación de longitud de canal (`pclm`), corriente de túnel de compuerta (`aigc`, `toxe`), corriente GIDL (`agidl`), y efecto de cuerpo ($V_{SB} > 0$).
5. **Inmutabilidad de Modelos PTM:**
   * No editar directamente los archivos `.pm` provistos por NIMO. Si se requieren modelos modificados (ej. subcircuitos con prefijos `_hp` y `_lp`), usar archivos `.lib` auxiliares en `modelos/`.
6. **Higiene del Repositorio:**
   * No hacer commit de archivos temporales de simulación (`.raw`, `.op.raw`, `.db`, `.tmp`) en la raíz. Mantener `.gitignore` riguroso.

---

## 5. Rutas a la Documentación Viva

El agente debe consultar y mantener actualizados los siguientes documentos de referencia:

* [**`_docs/process.md`**](file:///g:/Proyectos/MicroNano/_docs/process.md): Protocolo detallado de simulación SPICE, generación de figuras y control de calidad (QA).
* [**`_docs/plan.md`**](file:///g:/Proyectos/MicroNano/_docs/plan.md): Hoja de ruta del curso, estado de avance de cada informe y registro de hitos.
* [**`Semana_02/Guia_Oficial_LD1/LabDirigidoNro01.pdf`**](file:///g:/Proyectos/MicroNano/Semana_02/Guia_Oficial_LD1/LabDirigidoNro01.pdf): Enunciado oficial del Laboratorio Dirigido N.° 1.
* [**`Semana_02/Material_Adicional_Semestre/Rubrica Evaluacion de LD.pdf`**](file:///g:/Proyectos/MicroNano/Semana_02/Material_Adicional_Semestre/Rubrica%20Evaluacion%20de%20LD.pdf): Criterios de evaluación y penalizaciones docentes.
