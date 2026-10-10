# Microelectrónica y Sistemas Nanoelectrónicos

**Universidad Nacional Mayor de San Marcos**  
*Facultad de Ingeniería Electrónica y Eléctrica (FIEE)*  
*Escuela Profesional de Ingeniería Electrónica*  
*Semestre Académico 2026-II | Horario: Lunes 18:00 – 20:00*

---

### Información Académica
* **Docente Responsable:** MsC. Luz Adanaqué Infante
* **Autores e Investigadores:**
  * **Leonardo Sait Yactayo Tolentino** — Código: `23190214`
  * **Marco Antonio Arcila Santander** — Código: `23190140`
* **Rama Principal Oficial:** `main`

---

## 1. Presentación y Alcance del Repositorio

Este repositorio reúne las investigaciones, simulaciones físicas SPICE submicrométricas, desarrollos analíticos y reportes técnicos generados para el curso de **Microelectrónica y Sistemas Nanoelectrónicos** de la UNMSM.

El propósito central es el análisis de celdas digitales y topologías nanométricas avanzadas utilizando modelos físicos predictivos BSIM4 (**Predictive Technology Model - PTM** de 130 nm, 90 nm, 45 nm y 22 nm en variantes de alto desempeño *HP* y bajo consumo *LP*), integrando:
1. **Modelamiento físico y simulación SPICE de precisión** en LTspice (análisis transitorio `.tran`, barrido en continua `.dc`, análisis de punto de operación `.op` y mediciones automáticas `.meas`).
2. **Post-procesamiento y validación analítica en Python** (extracción cuantitativa de métricas, análisis de compromisos de diseño, balance de fugas y generación de figuras a 300 DPI).
3. **Redacción de informes técnicos de alto impacto en LaTeX** bajo el estándar y tipografía de IEEE (*IEEE Transactions*), cumpliendo restricciones estrictas de extensión, balance de ecuaciones y trazabilidad matemática-experimental biunívoca.

---

## 2. Mapa Arquitectónico del Repositorio

```
MicroNano/
│
├── AGENTS.md                                   # Context Engineering y reglas operativas del agente
├── CLAUDE.md                                   # Guía de interoperabilidad para LLMs y asistentes
├── README.md                                   # Portada y documentación general del repositorio
│
├── _docs/                                      # Documentación viva y recursos generales
│   ├── plan.md                                 # Hoja de ruta del curso y estado de avance de entregables
│   ├── process.md                              # Protocolo de simulación SPICE, generación de figuras y QA
│   └── recursos/                               # Manuales auxiliares y tutoriales de herramientas
│       └── Tutorial_Rapido_de_LTSpice.pdf      # Guía rápida de uso de LTspice para el curso
│
├── LD1_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 1: Lógica CMOS Estática
│   ├── informe_latex/                          # Documento maestro IEEE (máx 12 págs) y figuras vectoriales
│   ├── simulaciones/                           # Netlists SPICE (A1: VTC, A2: Retardos, A3: NAND/NOR, A4: Compleja, A5: RO)
│   ├── modelos/                                # Tarjetas de modelo PTM BSIM4 (45nm HP/LP, 90nm, 22nm)
│   ├── scripts/                                # Scripts Python de post-procesamiento y generación de curvas
│   └── README.md                               # Documentación técnica específica de LD1
│
├── LD2_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 2: Lógica CMOS Dinámica
│   ├── informe_latex/                          # Código LaTeX y reporte maestro final (20 págs físicas)
│   │   └── main.pdf                            # Documento PDF compilado oficial
│   ├── act1/                                   # Actividad 1: Caracterización NAND3 Dinámica vs. Estática
│   ├── act2/                                   # Actividad 2: Compartición de Carga (Charge Sharing) y Mitigaciones
│   ├── act3/                                   # Actividad 3: Balance de Fugas, Retención y Ventana de Keeper
│   ├── act4/                                   # Actividad 4: Monotonicidad y Skew de Reloj en Dominó Cascada
│   ├── act5/                                   # Actividad 5: Régimen NTV, Feedthrough y Eficiencia Energética
│   ├── act6/                                   # Actividad 6: Lógica Dinámica Multietapa (Módulo de extensión)
│   ├── modelos/                                # Librerías PTM centralizadas y subcircuitos auxiliares
│   ├── trazabilidad_figuras.txt                # Matriz biunívoca de reproducibilidad: Figuras -> Netlists -> Scripts
│   ├── verificacion_modelos.txt                # Verificación de parámetros físicos BSIM4 Level 54
│   └── README.md                               # Documentación técnica exhaustiva de LD2
│
├── Semana_01/                                  # Inversor CMOS Básico y Fundamentos de Conmutación
│   ├── Teoria/                                 # Diapositivas de introducción y modelado SPICE elemental
│   └── Practica_Inversor_NOT/                  # Esquemáticos `.asc` y netlists de inversores iniciales
│
├── Semana_02/                                  # Guía Oficial LD1, Tecnologías PTM y Dispositivos Especiales
│   ├── Guia_Oficial_LD1/                       # Guía docente oficial y librería multitecnológica PTM
│   ├── Teoria_y_Lecturas/                      # Lecturas de fabricación de películas delgadas y gruesas
│   └── Material_Adicional_Semestre/            # Módulos complementarios (SRAM 6T, Muxes, IGBTs)
│
├── Semana_03/                                  # Modelamiento CMOS Avanzado y Lógica CMOS Estática
│   ├── Teoria_y_Lecturas/                      # Modelos de corriente, velocidad de saturación y esfuerzo lógico
│   └── Ejercicios/                             # Ejercicios resueltos de dimensionamiento de transistores
│
├── Semana_04/                                  # Guía Oficial LD2 y Lógica CMOS Dinámica
│   ├── Guia_Oficial_LD2/                       # Guía oficial del Laboratorio Dirigido N.° 2
│   └── Teoria_y_Lecturas/                      # Diapositivas y fundamentos de lógica dinámica y pre-carga
│
├── Semana_05/                                  # Dispositivos Submicrométricos y Lógica Dinámica Avanzada
│   ├── 5. Submetric Devices.pdf                # Teoría de efectos de canal corto (SCE, DIBL, GIDL)
│   ├── Ejercicios_CMOSDinamica.pdf             # Colección de ejercicios de diseño en lógica dinámica
│   ├── Ejercicios_CMOSEstatica.pdf             # Ejercicios de análisis estático y dimensionamiento óptimo
│   └── Referencia_PC1.pdf                      # Material de estudio y problemas de práctica calificada
│
├── Semana_07/                                  # Guía Oficial LD3 y Dispositivos Submicrométricos II
│   ├── Guia_Oficial_LD3/                       # Guía oficial del Laboratorio Dirigido N.° 3
│   └── Teoria_y_Lecturas/                      # Apuntes y notas de aplicación de dispositivos nanométricos
│
│   # [Semana 08: Receso académico de exámenes de medio ciclo según calendario UNMSM]
│
├── Semana_09/                                  # Microsensores de Estado Sólido
│   ├── 9. Microsensores.pdf                    # Principios físicos de transducción y microsensores MEMS
│   ├── 9. Perfomance Sensores.pdf              # Métricas de sensibilidad, resolución, ruido y ancho de banda
│   └── 9. ReferenciaMicrosensores.pdf          # Lecturas de referencia en integración de sensores en silicio
│
├── Semana_10/                                  # Microactuadores y Sistemas Microelectromecánicos
│   └── 10. MicroActuadores.pdf                 # Actuadores electrostáticos, térmicos, piezoeléctricos y magnéticos
│
├── Semana_11/                                  # Modelos de Fallos y Prueba de Circuitos Integrados (Test en CI)
│   ├── 11.ModeloDeFallos.pdf                   # Modelos de fallos lógicos: stuck-at, bridging, open, delay
│   ├── 11.TestEnCI.pdf                         # Metodologías de prueba, testabilidad y arquitectura DFT
│   ├── 11.TestEnCI-apuntes.pdf                 # Apuntes de clase y resolución de esquemas de test
│   └── Referencia_VectoresDeTest.pdf           # Algoritmos de generación de vectores (D-algorithm, PODEM)
│
└── Semana_12/                                  # Ejercicios y Casos Avanzados de Test y Confiabilidad
    └── S12-Ejercicios.pdf                      # Problemas integradores de diseño para testabilidad (Scan, BIST)
```

---

## 3. Investigaciones de Laboratorio Desarrolladas

### [Laboratorio Dirigido N.° 1: Lógica CMOS Estática](LD1_Arcila_Yactayo/)
* **Objetivo:** Caracterización estática y dinámica exhaustiva de compuertas lógicas elementales y complejas en el nodo de 45 nm PTM BSIM4, estableciendo la correlación entre dimensionamiento físico ($\beta = W_p / W_n$) y figuras de mérito.
* **Aspectos Investigados:**
  1. *Curva de Transferencia de Tensión (VTC):* Determinación del punto de conmutación óptimo estático ($V_M \approx V_{DD}/2 = 0.500\text{ V}$ en $\beta_{\text{ópt}} = 2.50$) y evaluación de márgenes de ruido $NM_H$ y $NM_L$.
  2. *Retardo de Propagación y Carga FO4:* Medición de retardos de conmutación ($t_{pHL}$, $t_{pLH}$, $t_{pd}$) bajo carga normalizada de 4 inversores idénticos, contrastando nodos de 90 nm, 45 nm y 22 nm.
  3. *Compuertas Estándar NAND2 y NOR2:* Comparación de arquitecturas pull-up y pull-down conservando la resistencia equivalente del inversor base.
  4. *Compuerta Compleja multinivel:* Dimensionamiento y simulación de redes AOI/OAI.
  5. *Oscilador en Anillo y Balance de Potencia:* Evaluación de frecuencia libre de oscilación ($f_{osc}$), potencia de conmutación dinámica ($P_{dyn}$) y fuga estática en reposo ($I_{leak}$) entre procesos 45 nm HP y 45 nm LP.
* **Informe Técnico Oficial:** `LD1_Arcila_Yactayo/informe_latex/LD1.pdf` (12 páginas formato IEEE).
* **Comandos de Ejecución y Reproducción:**
  ```powershell
  # Simulación de la curva VTC en modo batch
  & "LTspice.exe" -b .\LD1_Arcila_Yactayo\simulaciones\A1_Inversor_VTC\A1_VTC.cir

  # Generación de gráficas analíticas a 300 DPI
  python .\LD1_Arcila_Yactayo\scripts\generar_graficas.py
  ```

---

### [Laboratorio Dirigido N.° 2: Lógica CMOS Dinámica Submicrométrica](LD2_Arcila_Yactayo/)
* **Objetivo:** Análisis físico-circuital y cuantitativo de lógica CMOS dinámica y circuitos dominó en nodos tecnológicos PTM BSIM4 (45 nm HP, 45 nm LP y 130 nm Bulk).
* **Módulos Experimentales y Resultados Clave:**
  1. *Actividad 1 (Dinámica vs. Estática):* Demostración de la reducción de capacitancia de entrada ($-42.4\%$) y reducción del retardo de propagación al suprimir la red pull-up redundante.
  2. *Actividad 2 (Compartición de Carga - Charge Sharing):* Identificación analítica y experimental del peor caso sincrónico de descarga interna ($\Delta V_{dyn} = 164.29\text{ mV}$ bajo $C_L = 2.0\text{ fF}$) y contraste de técnicas de mitigación (pre-carga pasiva interna vs. sobre-dimensionamiento de $C_L$).
  3. *Actividad 3 (Balance Causal de Fugas, Retención y Keeper):* Aislamiento físico de componentes de fuga (subumbral, túnel de compuerta y GIDL) a 27 °C y 85 °C. Establecimiento formal de la ventana de viabilidad del *keeper* ($W_{kp} \in [10.5, 38.0]\text{ nm}$) resolviendo el compromiso de contención estática (*ratioed fighting*).
  4. *Actividad 4 (Monotonicidad y Skew de Reloj en Cascada Dominó):* Demostración de la falla catastrófica ante entradas no monótonas en cascadas sin inversor de polaridad, y caracterización de la ventana de robustez ante desfase de reloj (*skew*) comparando celdas *footed* y *unfooted*.
  5. *Actividad 5 (Régimen Near-Threshold Voltage y Feedthrough):* Barrido de tensión de alimentación ($V_{DD} \in [0.35, 1.00]\text{ V}$) determinando el punto de energía mínima por ciclo, la ventana de frecuencias admisibles $[f_{min}, f_{max}]$, y la mitigación del acoplamiento capacitivo de reloj (*feedthrough*).
* **Informe Técnico Oficial:** [`LD2_Arcila_Yactayo/informe_latex/main.pdf`](LD2_Arcila_Yactayo/informe_latex/main.pdf) (20 páginas físicas exactas bajo estándar IEEE).
* **Comandos de Ejecución y Reproducción:**
  ```powershell
  # Ejecución de simulaciones SPICE de referencia
  & "LTspice.exe" -b .\LD2_Arcila_Yactayo\act1\circuitos\nand3_dinamica_base.cir
  & "LTspice.exe" -b .\LD2_Arcila_Yactayo\act2\circuitos\nand3_cs_g2b_piloto_cl2f.cir

  # Regeneración automatizada de figuras vectoriales
  python .\LD2_Arcila_Yactayo\act1\scripts\generar_figuras_act1.py
  python .\LD2_Arcila_Yactayo\act2\scripts\generar_figuras_act2.py
  python .\LD2_Arcila_Yactayo\act3\scripts\generar_figura8_editorial.py
  python .\LD2_Arcila_Yactayo\act4\scripts\generar_figuras_act4.py
  python .\LD2_Arcila_Yactayo\act5\scripts\generar_figuras_act5.py
  ```

---

## 4. Requisitos y Herramientas del Entorno

Para replicar íntegramente las simulaciones y compilar los documentos técnicos, se requiere:

* **Simulador SPICE:** [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html) (versión XVII o LTspice 24, instalado en la ruta por defecto o añadido al `PATH` del sistema).
* **Entorno de Programación:** Python 3.10 o superior con las bibliotecas científicas estándar:
  ```bash
  pip install numpy scipy matplotlib
  ```
* **Sistema Tipográfico:** TeX Live 2024 o MiKTeX con `pdflatex` y los paquetes estándar para IEEE:
  * `IEEEtran`, `amsmath`, `amssymb`, `booktabs`, `cite`, `graphicx`, `microtype`, `subcaption`, `siunitx`, `xcolor`.

---

## 5. Control de Versiones y Políticas de Integridad

* **Rama Oficial Única:** El repositorio opera de forma exclusiva sobre la rama principal **`main`**. Todas las contribuciones concluidas se integran mediante commits convencionales en esta rama.
* **Estándar de Mensajes de Confirmación:**
  * `feat(alcance): nueva funcionalidad o actividad de laboratorio`
  * `fix(alcance): corrección analítica, circuital o tipográfica`
  * `docs(alcance): actualización de informes, figuras o README`
  * `chore(alcance): mantenimiento, organización de carpetas y dependencias`
* **Políticas de Higiene y Exclusión (.gitignore):**
  * Quedan excluidos del repositorio remoto los archivos binarios de simulación masiva (`*.raw`, `*.op.raw`, `*.fft`), registros temporales (`*.log`), archivos intermedios de compilación LaTeX (`*.aux`, `*.fls`, `*.fdb_latexmk`), así como evaluaciones y materiales locales privados.
