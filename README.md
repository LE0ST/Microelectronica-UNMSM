# Microelectrónica y Sistemas Nanoelectrónicos

**Universidad Nacional Mayor de San Marcos**  
*Facultad de Ingeniería Electrónica y Eléctrica (FIEE)*  
*Escuela Profesional de Ingeniería Electrónica*  
*Semestre Académico 2026-II | Horario: Lunes 18:00 – 20:00*

---

### Información Académica
* **Docente Responsable:** MsC. Luz Adanaqué Infante
* **Autores e Investigadores:**
  * **Leonardo Sait Yactayo Tolentino** — Código: `23190214` (LD1, LD2; Autor individual de LD3)
  * **Marco Antonio Arcila Santander** — Código: `23190140` (LD1, LD2)
* **Rama Principal Oficial:** `main`
* **Rama Activa de Desarrollo (LD3):** `feat/ld3-igbt`

---

## 1. Presentación y Alcance del Repositorio

Este repositorio reúne las investigaciones, simulaciones físicas SPICE, desarrollos analíticos y reportes técnicos generados para el curso de **Microelectrónica y Sistemas Nanoelectrónicos** de la UNMSM.

El proyecto abarca dos grandes dominios tecnológicos:
1. **Lógica Digital Submicrométrica CMOS:** Análisis estático y dinámico empleando modelos físicos predictivos BSIM4 (**Predictive Technology Model - PTM** de 130 nm, 90 nm, 45 nm y 22 nm en variantes *HP* y *LP*), abordando curvas VTC, retardo FO4, fugas causales, compartición de carga y régimen Near-Threshold Voltage (LD1 y LD2).
2. **Dispositivos Electrónicos de Potencia (IGBT):** Caracterización estática y dinámica de transistores bipolares de compuerta aislada (IGBT) de canal N y canal P, así como módulos comerciales Trench-FS de 650 V (Fuji Electric Serie X de 50 A y 75 A), mediante bancos *Double Pulse Test* (DPT) para el análisis de corriente de cola, pérdidas de apagado $E_{\text{off}}$ y sobretensiones transitorias (LD3).

El flujo de trabajo integra modelamiento SPICE en **LTspice**, post-procesamiento cuantitativo en **Python 3.14** (gráficas vectoriales a 300 DPI y tablas de datos) y redacción técnica de alto impacto.

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
│   ├── bitacora.md                             # Bitácora cronológica global de desarrollo
│   ├── plan.md                                 # Hoja de ruta del curso y estado de avance de entregables
│   ├── process.md                              # Protocolo de simulación SPICE, generación de figuras y QA
│   └── recursos/                               # Manuales auxiliares y tutoriales de herramientas
│       └── Tutorial_Rapido_de_LTSpice.pdf      # Guía rápida de uso de LTspice para el curso
│
├── LD1_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 1: Lógica CMOS Estática (Finalizado)
│   ├── informe_latex/                          # Documento maestro IEEE (12 págs.) y figuras vectoriales
│   │   └── LD1_Arcila_Yactayo.pdf              # Documento PDF compilado oficial de LD1
│   ├── simulaciones/                           # Netlists SPICE (A1: VTC, A2: Retardos, A3: NAND/NOR, A4: Compleja, A5: RO)
│   ├── modelos/                                # Tarjetas de modelo PTM BSIM4 (45nm HP/LP, 90nm, 22nm)
│   ├── scripts/                                # Scripts Python de post-procesamiento y curvas
│   └── README.md                               # Documentación técnica específica de LD1
│
├── LD2_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 2: Lógica CMOS Dinámica (Finalizado)
│   ├── informe_latex/                          # Código LaTeX y reporte maestro final (20 págs. IEEE)
│   │   └── main.pdf                            # Documento PDF compilado oficial de LD2
│   ├── act1/                                   # Actividad 1: Caracterización NAND3 Dinámica vs. Estática
│   ├── act2/                                   # Actividad 2: Compartición de Carga (Charge Sharing) y Mitigaciones
│   ├── act3/                                   # Actividad 3: Balance Causal de Fugas, Retención y Keeper
│   ├── act4/                                   # Actividad 4: Monotonicidad y Skew de Reloj en Dominó Cascada
│   ├── act5/                                   # Actividad 5: Régimen NTV, Feedthrough y Eficiencia Energética
│   ├── modelos/                                # Librerías PTM centralizadas y subcircuitos auxiliares
│   ├── trazabilidad_figuras.txt                # Matriz biunívoca de reproducibilidad: Figuras -> Netlists -> Scripts
│   ├── verificacion_modelos.txt                # Verificación de parámetros físicos BSIM4 Level 54
│   └── README.md                               # Documentación técnica exhaustiva de LD2
│
├── LD3_Yactayo/                                # LABORATORIO DIRIGIDO N.° 3: Transistores IGBT en LTspice (Individual)
│   ├── esquemas/                               # Archivos .asc esquemáticos interactivos de LTspice
│   ├── simulaciones/                           # Netlists .cir y resultados trazables de simulación
│   ├── modelos/                                # Documentación de procedencia y licenciamiento de modelos
│   │   └── NOTAS_MODELOS.md                    # Registro de modelos Fuji Serie X y Duncan Electronics
│   ├── scripts/                                # Scripts Python para extracción de métricas y figuras
│   ├── figuras/                                # Formas de onda y gráficas comparativas a 300 DPI
│   ├── tablas/                                 # Tablas cuantitativas consolidadas (Markdown y CSV)
│   ├── informe/                                # Documento del reporte técnico (conclusiones >= 1 pág.)
│   ├── README.md                               # Guía de reproducción y metodología de LD3
│   └── TRAZABILIDAD.md                         # Matriz de trazabilidad experimental biunívoca
│
├── Semana_01/                                  # Inversor CMOS Básico y Fundamentos de Conmutación
├── Semana_02/                                  # Guía Oficial LD1, Tecnologías PTM y Dispositivos de Potencia
│   ├── Guia_Oficial_LD1/                       # Guía docente oficial de LD1
│   ├── Teoria_y_Lecturas/                      # Lecturas de fabricación de películas delgadas y gruesas
│   └── Material_Adicional_Semestre/            # Módulos complementarios y modelos de referencia IGBT
│       └── 05_Laboratorio_IGBT/                # Circuitos base y librerías SPICE de IGBTs
├── Semana_03/                                  # Modelamiento CMOS Avanzado y Dimensionamiento
├── Semana_04/                                  # Guía Oficial LD2 y Lógica CMOS Dinámica
│   └── Guia_Oficial_LD2/                       # Guía oficial del Laboratorio Dirigido N.° 2
├── Semana_05/                                  # Dispositivos Submicrométricos y Ejercicios Prácticos
├── Semana_07/                                  # Guía Oficial LD3 y Dispositivos Submicrométricos II
│   ├── Guia_Oficial_LD3/                       # Guía oficial del Laboratorio Dirigido N.° 3 (LabDirigidoNro03.pdf)
│   └── Teoria_y_Lecturas/                      # Notas de aplicación y lectura técnica sobre IGBTs
├── Semana_09/                                  # Microsensores de Estado Sólido
├── Semana_10/                                  # Microactuadores y Sistemas MEMS
├── Semana_11/                                  # Modelos de Fallos y Prueba de Circuitos Integrados (DFT)
└── Semana_12/                                  # Ejercicios y Casos Avanzados de Test y Confiabilidad
```

---

## 3. Investigaciones de Laboratorio Desarrolladas

### [Laboratorio Dirigido N.° 1: Lógica CMOS Estática](LD1_Arcila_Yactayo/)
* **Autores:** Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander.
* **Objetivo:** Caracterización estática y dinámica exhaustiva de compuertas lógicas elementales y complejas en el nodo de 45 nm PTM BSIM4, estableciendo la correlación entre dimensionamiento físico ($\beta = W_p / W_n$) y figuras de mérito.
* **Aspectos Investigados:** Curva de transferencia de tensión (VTC, $\beta_{\text{ópt}} = 2.50$), retardo FO4, compuertas estándar NAND2/NOR2, compuerta compleja AOI ($\beta = 2.0$), oscilador en anillo de 5 etapas ($f_{osc} = 21.94\text{ GHz}$) y compromiso velocidad/fuga entre procesos 45 nm HP y LP.
* **Informe Técnico Oficial:** [`LD1_Arcila_Yactayo/informe_latex/LD1_Arcila_Yactayo.pdf`](LD1_Arcila_Yactayo/informe_latex/LD1_Arcila_Yactayo.pdf) (12 páginas formato IEEE).

---

### [Laboratorio Dirigido N.° 2: Lógica CMOS Dinámica Submicrométrica](LD2_Arcila_Yactayo/)
* **Autores:** Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander.
* **Objetivo:** Análisis físico-circuital y cuantitativo de lógica CMOS dinámica y circuitos dominó en nodos tecnológicos PTM BSIM4 (45 nm HP, 45 nm LP y 130 nm Bulk).
* **Actividades Realizadas:**
  1. *Actividad 1:* Caracterización NAND3 Dinámica footed vs. Estática (reducción de capacitancia de entrada en $-42.4\%$).
  2. *Actividad 2:* Compartición de carga (*charge sharing*) y mitigaciones (precarga interna, reordenamiento PDN y keeper activo).
  3. *Actividad 3:* Balance causal de fugas y ventana de viabilidad del keeper a 27 °C y 85 °C.
  4. *Actividad 4:* Monotonicidad y tolerancia a skew de reloj en cascada dominó.
  5. *Actividad 5:* Operación en régimen Near-Threshold Voltage (NTV) y supresión de feedthrough capacitivo.
  *(Nota: Actividad 6 de lógica multietapa constituyó un módulo de extensión opcional no desarrollado).*
* **Informe Técnico Oficial:** [`LD2_Arcila_Yactayo/informe_latex/main.pdf`](LD2_Arcila_Yactayo/informe_latex/main.pdf) (20 páginas físicas exactas bajo estándar IEEE).

---

### [Laboratorio Dirigido N.° 3: Transistores IGBT en LTspice](LD3_Yactayo/) *(EN DESARROLLO)*
* **Autor:** Leonardo Sait Yactayo Tolentino (*Modalidad Individual*).
* **Estado:** **EN DESARROLLO** (fase inicial de configuración de bancos DPT; simulaciones y resultados en proceso de ejecución).
* **Objetivo:** Caracterización y simulación comparativa de transistores bipolares de compuerta aislada (IGBT) de canal N y canal P, así como dispositivos comerciales Trench de alta velocidad de conmutación (Fuji Electric Serie X de 650 V), mediante el banco de pruebas *Double Pulse Test* (DPT) en LTspice.
* **Aspectos Investigados:**
  1. *Banco Double Pulse Test:* Configuración de lado bajo (N-IGBT con emisor a tierra) y lado alto (P-IGBT con polarización negativa de compuerta $0\to -15\text{ V}$).
  2. *Corriente de Cola (Tail Current):* Identificación analítica del punto de inicio de la fase asintótica de cola y justificación basada en recombinación de portadores minoritarios en la región de deriva.
  3. *Retardo de Apagado ($t_{d(\text{off})}$):* Medición cuantitativa del intervalo temporal entre el 90% de $V_{GE}$ y el 90% de $I_C$, contrastando con hojas de datos de fabricante.
  4. *Pérdidas de Conmutación ($E_{\text{off}}$):* Cálculo numérico de la integral $\int V_{CE} I_C dt$ y porcentaje energético disipado durante la corriente de cola.
  5. *Sobretensión Transitoria por Inductancia Parásita ($V_{CE,\text{peak}}$):* Evaluación del pico de sobretensión al comparar modelos con y sin diodo de marcha libre integrado (*co-pack*).
  6. *Sensibilidad a la Resistencia de Compuerta ($R_G$):* Análisis del impacto de duplicar $R_G$ sobre la velocidad de conmutación y pérdidas dinámicas.
  7. *Escalamiento de Área de Silicio:* Comparación entre modelos de 50 A (`FGW50XS65/C`) y 75 A (`FGW75XS65/C`).
* **Entregables Oficiales:** Tabla de resultados cuantitativa completa, gráficas transitorias ordenadas ($V_{GE}, V_{CE}, I_C$), conclusiones técnicas fundamentadas ($\ge 1$ página) y exposición oral programada para el **21 de octubre de 2026**.

---

## 4. Requisitos y Herramientas del Entorno

Para replicar íntegramente las simulaciones y compilar los reportes técnicos se requiere:

* **Simulador SPICE:** [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html) (versión 24 o superior instalada localmente, ejecutable en `G:\LTspice\LTspice.exe` o en el `PATH` del sistema).
* **Entorno de Programación:** Python 3.10 o superior (verificado con Python 3.14 local):
  ```bash
  pip install numpy scipy matplotlib
  ```
* **Sistema Tipográfico:** TeX Live o MiKTeX con `pdflatex` y paquetes IEEE (`IEEEtran`, `amsmath`, `booktabs`, `graphicx`, `siunitx`).

---

## 5. Control de Versiones y Políticas de Integridad

* **Políticas de Ramas:**
  * La rama `main` refleja únicamente entregables concluidos, auditados e integrados.
  * Todo desarrollo activo en curso se realiza en ramas de funcionalidad específicas (ej. `feat/ld3-igbt`).
* **Estándar de Mensajes de Confirmación:**
  * Se aplica estrictamente la convención Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
* **Políticas de Exclusión (.gitignore):**
  * Quedan excluidos del repositorio remoto los archivos binarios pesados (`*.raw`, `*.op.raw`, `*.db`), temporales del compilador LaTeX (`*.aux`, `*.fls`), entornos virtuales (`.venv`), áreas temporales (`scratch/`) y evaluaciones privadas locales (`LC1*`).
  * Los resultados cuantitativos se registran y versionan preferentemente en tablas Markdown, archivos JSON o CSV trazables.
