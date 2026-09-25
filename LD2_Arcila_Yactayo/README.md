# Laboratorio Dirigido N.° 2: Lógica CMOS Dinámica Submicrométrica

**Universidad Nacional Mayor de San Marcos (UNMSM)**  
**Facultad de Ingeniería Electrónica y Eléctrica (FIEE)**  
**Escuela Profesional de Ingeniería Electrónica**  
*Curso:* Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
*Docente:* MsC. Luz Adanaqué Infante  

**Autores:**
* **Leonardo Sait Yactayo Tolentino** (Código: 23190214)
* **Marco Antonio Arcila Santander** (Código: 23190140)

*Documento Maestro Oficial:* [informe_latex/main.pdf](informe_latex/main.pdf) (20 páginas físicas, formato IEEE Transactions)

---

## 1. Resumen Ejecutivo

El presente repositorio contiene la investigación física, simulación circuital SPICE (LTspice / modelos PTM BSIM4 Nivel 54), post-procesamiento analítico en Python y memoria técnica del **Laboratorio Dirigido N.° 2**. La práctica aborda el diseño, vulnerabilidades físicas y optimización de celdas en lógica CMOS dinámica y dominó sobre tecnologías de 45 nm (High-Performance y Low-Power) y 130 nm Bulk CMOS:

1. **Actividad 1 — Caracterización Básica y Comparación Estática:**  
   Implementación de una celda NAND3 dinámica con transistor de pie (*footed*) a $V_{DD} = 1.0\text{ V}$. Verificación de las fases de precarga y evaluación. Reducción experimental de la capacitancia de entrada en **42.4 %** frente a la NAND3 CMOS estática equivalente ($0.3417\text{ fF}$ vs $0.5936\text{ fF}$) por eliminación de la red de pull-up (PUN). El retardo de propagación en la salida dominó es de $35.89\text{ ps}$ medido desde el flanco del reloj ($CLK\uparrow$), frente a los $9.61\text{ ps}$ de la compuerta estática disparada por datos ($A\uparrow$).
2. **Actividad 2 — Compartición de Carga (*Charge Sharing*):**  
   Identificación del peor caso sincrónico de redistribución de carga hacia capacidades parásitas de difusión intermedias ($\Delta V_{dyn} = 164.29\text{ mV}$ con $C_L = 2.0\text{ fF}$, $V_{dyn,\text{min}} = 0.8357\text{ V}$). Evaluación comparativa de técnicas de mitigación: precarga interna con $W_p = 45\text{ nm}$ (suprime el droop generando sobreimpulso capacitivo de $+50.47\text{ mV}$), reordenamiento de entradas C-A-B ($72.08\text{ mV}$ de droop en el vector B) e inserción de *keeper* PMOS convencional ($69.68\text{ mV}$ con restauración activa a $0.9996\text{ V}$).
3. **Actividad 3 — Fugas Subumbral, Retención y Dimensionamiento del Keeper:**  
   Caracterización del tiempo de retención bajo estrés térmico ($27\text{ }^\circ\text{C}$ vs $85\text{ }^\circ\text{C}$). En 45 nm HP a $85\text{ }^\circ\text{C}$, se define una ventana de viabilidad del *keeper* de $W_{kp} \in [10.5, 38.0]\text{ nm}$ ($r = W_{kp}/67.5\text{ nm} \in [0.156, 0.563]$) con penalización de contención de retardo $\le 10\%$. La configuración de referencia de $W_{kp} = 22\text{ nm}$ ($r = 0.326$) exhibe una penalización de $+5.25\%$, mientras que la alternativa de *keeper* condicional ($W_{kp}=45\text{ nm}$ con 3 inversores) logra $+5.11\%$. Consolidación frente a 45 nm LP (retención censurada $>1.0\text{ }\mu\text{s}$) y 130 nm Bulk ($t_{hold} = 167.53\text{ ns}$ bajo el criterio estricto de $0.90\,V_{DD}$ a $85\text{ }^\circ\text{C}$).
4. **Actividad 4 — Monotonicidad y Skew de Reloj en Cascada:**  
   Demostración analítica y experimental de la regla de monotonicidad dominó mediante inversores estáticos inter-etapa, impidiendo la pérdida irreversible de carga por transiciones $1 \to 0$. Evaluación de cascadas de 3 etapas bajo desfase temporal de reloj (*clock skew*), contrastando la robustez de topologías *footed* frente a corrientes de cortocircuito en celdas *unfooted*.
5. **Actividad 5 — Régimen Near-Threshold (NTV), Feedthrough y Escalado Energético:**  
   Operación en escalado agresivo de tensión de alimentación ($V_{DD} = 1.0\text{ V} \to 0.35\text{ V}$). Análisis del sobreimpulso por acoplamiento capacitivo de reloj (*feedthrough* de $+64.31\text{ mV}$, amortiguado en $23.3\%$ a $+49.31\text{ mV}$ por el *keeper*). Determinación de la ventana de frecuencia operable: a $V_{DD} = 0.40\text{ V}$, la celda presenta $f_{\max} \approx 420\text{ MHz}$ y $f_{\min} \approx 1.12\text{ MHz}$ a $85\text{ }^\circ\text{C}$, preservando una amplia ventana operable con un ahorro del $85.2\%$ en energía de conmutación ($0.1076\text{ fJ}$ vs $0.7259\text{ fJ}$ a $1.0\text{ V}$).

---

## 2. Resultados Cuantitativos Clave

| Actividad | Métrica Evaluada | Configuración / Condición | Valor Medido (SPICE) | Referencia / Observación |
|---|---|---|---|---|
| **A1** | Capacitancia de entrada ($C_{in}$) | NAND3 Dinámica vs Estática | $0.3417\text{ fF}$ vs $0.5936\text{ fF}$ | Reducción del **42.4 %** por eliminación de red PUN |
| **A1** | Retardo en terminal de salida | $C_{out} = 1.0\text{ fF}$, PTM 45 nm HP | Dinámica: $35.89\text{ ps}$ ($CLK\uparrow$)<br>Estática: $9.61\text{ ps}$ ($A\uparrow$) | Triggers asimétricos evaluados en terminal $out$ |
| **A2** | Droop de peor caso síncrono | Caso base sin mitigación ($C_L = 2.0\text{ fF}$) | $\Delta V_{dyn} = 164.29\text{ mV}$ | Margen seguro ($V_{dyn,\text{min}} = 0.8357\text{ V}$, $NM_H = +257.2\text{ mV}$) |
| **A2** | Mitigación: Precarga interna | Transistores de precarga $W_p = 45\text{ nm}$ | Suprime droop (sobreimpulso $+50.47\text{ mV}$) | $V_{dyn} = 1.0505\text{ V}$, sobrecoste de reloj $+0.127\text{ fF}$ |
| **A2** | Mitigación: Reordenamiento C-A-B | Desacoplo de nodos internos (Vector B) | $\Delta V_{dyn} = 72.08\text{ mV}$ | Droop acotado a $72.08\text{ mV}$ sin área adicional |
| **A2** | Mitigación: Keeper PMOS | Transistor convencional $W_{kp} = 45\text{ nm}$ | $\Delta V_{dyn} = 69.68\text{ mV}$ | Restaura a $0.9996\text{ V}$; penalización $+14.65\%$ en $t_{pHL,dyn}$ |
| **A3** | Retención 45 nm HP @ $85\text{ }^\circ\text{C}$ | Sin keeper ($T_{\text{stop}} = 1.0\,\mu\text{s}$, $C_L=2\text{ fF}$) | $t_{hold} = 608.17\text{ ns}$ | Cruce con $0.90\,V_{DD}$; retiene nivel lógico ($V_{dyn} > V_M$) |
| **A3** | Ventana de viabilidad keeper | 45 nm HP @ $85\text{ }^\circ\text{C}$ ($\Delta t_{pHL} \le 10\%$) | $W_{kp} \in [10.5, 38.0]\text{ nm}$ | Razón geométrica $r = \frac{W_{kp}}{67.5\,\text{nm}} \in [0.156, 0.563]$ |
| **A3** | Keeper convencional de referencia | 45 nm HP @ $85\text{ }^\circ\text{C}$ ($W_{kp} = 22\text{ nm}$, $r=0.326$) | $\Delta t_{pHL} = +5.25\%$ | Retención garantizada $>1.0\,\mu\text{s}$ ($V_{dyn} > 0.999\,\text{V}$) |
| **A3** | Alternativa keeper condicional | 45 nm HP @ $85\text{ }^\circ\text{C}$ ($W_{kp} = 45\text{ nm}$ + 3 inv.) | $\Delta t_{pHL} = +5.11\%$ | Mitigación de contención frente a keeper unitario ($+12.90\%$) |
| **A3** | Retención 130 nm Bulk @ $85\text{ }^\circ\text{C}$ | Sin keeper ($V_{DD} = 1.3\text{ V}$, $C_L = 2\text{ fF}$) | $t_{hold} = 167.53\text{ ns}$ | Criterio estricto $0.90\,V_{DD}$ ($1.17\text{ V}$); $V_{dyn}(1\,\mu\text{s}) = 0.877\text{ V}$ |
| **A4** | Rechazo de entrada espuria | Pulso $1 \to 0$ durante evaluación | Salida out2 retenida en $1.0\text{ V}$ errónea | Violación de monotonicidad $\implies$ falla irreversible |
| **A4** | Skew tolerable en cascada | 3 etapas dominó *footed* | $t_{skew} \approx 18.5\text{ ps}$ | Aislamiento eficaz contra corrientes de cortocircuito |
| **A5** | Clock feedthrough en precarga | $V_{DD} = 1.0\text{ V}$, PMOS precarga $W_p=135\text{ nm}$ | $+64.31\text{ mV}$ ($+49.31\text{ mV}$ con keeper) | Amortiguación pasiva del $23.3\%$ con keeper |
| **A5** | Ventana operable en NTV ($0.40\text{ V}$) | PTM 45 nm HP @ $85\text{ }^\circ\text{C}$, $C_L = 0.5\text{ fF}$ | $f_{\max} \approx 420\text{ MHz}$, $f_{\min} \approx 1.12\text{ MHz}$ | Holgura $t_{hold}/t_{eval} \gg 10$; energía reducida en $85.2\%$ |

---

## 3. Estructura del Repositorio LD2

```
LD2_Arcila_Yactayo/
├── README.md                              # Portada técnica para GitHub
├── README.txt                             # Documentación técnica de entrega y runbook
├── verificacion_modelos.txt               # Auditoría física de parámetros BSIM4 (Level 54)
├── trazabilidad_figuras.txt               # Matriz de correspondencia: Figuras -> Netlists -> Scripts
│
├── modelos/                               # Tarjetas tecnológicas PTM BSIM4 (.lib)
│   ├── ptm45hp.lib                        # 45 nm High-Performance (Vdd = 1.0 V, toxe = 1.25/1.30 nm)
│   ├── ptm45lp.lib                        # 45 nm Low-Power (Vdd = 1.1 V, toxe = 1.80/1.82 nm)
│   ├── ptm130.lib                         # 130 nm Bulk CMOS (Vdd = 1.3 V, toxe = 2.25/2.35 nm)
│   ├── ptm45hp_aux.lib                    # Tarjeta auxiliar para control GIDL
│   └── README_modelos.md                  # Descripción teórica de modelos PTM
│
├── act1/                                  # Actividad 1: Caracterización y Fases Dominó
│   ├── README_act1.md                     # Memoria técnica de Actividad 1
│   ├── circuitos/                         # Netlists SPICE (.cir)
│   ├── scripts/                           # Scripts de graficación y análisis (Python)
│   ├── resultados/                        # Mediciones (.log, .raw, .json)
│   └── figuras/                           # Formas de onda a 300 DPI (.png)
│
├── act2/                                  # Actividad 2: Compartición de Carga (Charge Sharing)
│   ├── README_act2.md                     # Memoria técnica de Actividad 2
│   ├── prediccion_analitica_act2.md       # Deducción analítica a priori de Delta V
│   ├── circuitos/                         # Netlists SPICE (.cir) con difusión AS/AD/PS/PD
│   ├── scripts/                           # Scripts comparativos analítico vs SPICE
│   ├── resultados/                        # Barrido de CL y mitigaciones (.json)
│   └── figuras/                           # Curvas de droop y mitigaciones (.png)
│
├── act3/                                  # Actividad 3: Fugas, Retención y Keeper
│   ├── README_act3.md                     # Memoria técnica de Actividad 3
│   ├── circuitos/                         # Netlists de contención, retención y tri-nodo (.cir)
│   ├── scripts/                           # Scripts de ventana de viabilidad y compromiso
│   ├── resultados/                        # Métricas a 27 °C y 85 °C (.json)
│   └── figuras/                           # Curvas de retención, contención y compromiso (.png)
│
├── act4/                                  # Actividad 4: Monotonicidad y Skew de Reloj en Cascada
│   ├── README_act4.md                     # Memoria técnica de Actividad 4
│   ├── circuitos/                         # Netlists de cascadas de 2 y 3 etapas (.cir)
│   ├── scripts/                           # Scripts de evaluación de monotonicidad y skew
│   ├── resultados/                        # Métricas de skew y formas de onda
│   └── figuras/                           # Curvas temporales y comparación footed/unfooted (.png)
│
├── act5/                                  # Actividad 5: Régimen NTV, Feedthrough y Escalado
│   ├── README_act5.md                     # Memoria técnica de Actividad 5
│   ├── circuitos/                         # Netlists de escalado de VDD (0.35 V a 1.0 V) (.cir)
│   ├── scripts/                           # Script generador de ventana fmin/fmax y energía
│   ├── resultados/                        # Métricas transitorias y consumo estructurado (.json)
│   └── figuras/                           # Gráficas de feedthrough y ventana operable (.png)
│
├── act6/                                  # Actividad 6: Lógica Multietapa Compleja (Opcional)
│   └── README.txt                         # Nota formal: Opcional, no desarrollada
│
└── informe_latex/                         # Código fuente LaTeX del informe maestro oficial
    ├── main.tex                           # Documento maestro (20 páginas físicas exactas)
    ├── main.pdf                           # PDF compilado final
    ├── secciones/                         # Módulos de texto (01 a 09)
    ├── tablas/                            # Tablas académicas normalizadas
    └── figuras/                           # Gráficas integradas en el informe final
```

---

## 4. Reproducibilidad y Ejecución

### A. Simulación SPICE (LTspice)
Todos los circuitos fueron concebidos con rutas relativas hacia la biblioteca de modelos (`../../modelos/*.lib`):

* **Modo Gráfico (GUI):**
  Abrir LTspice, cargar cualquier archivo `.cir` ubicado en `actX/circuitos/` y pulsar `Run`.
* **Modo Batch Silencioso (PowerShell):**
  ```powershell
  # Ejemplo: Ejecución de la celda NAND3 base de Actividad 1
  & "LTspice.exe" -b "LD2_Arcila_Yactayo/act1/circuitos/nand3_dinamica_base.cir"
  
  # Ejemplo: Evaluación de peor caso de charge sharing en Actividad 2
  & "LTspice.exe" -b "LD2_Arcila_Yactayo/act2/circuitos/nand3_cs_g2b_piloto_cl2f.cir"
  ```

### B. Regeneración de Figuras Científicas (Python 3.10+)
Los scripts leen los datos estructurados o formas de onda y regeneran las figuras a 300 DPI en sus respectivas carpetas:

```powershell
# Actividad 1
python LD2_Arcila_Yactayo/act1/scripts/generar_figuras_act1.py

# Actividad 2
python LD2_Arcila_Yactayo/act2/scripts/generar_figuras_act2.py

# Actividad 3
python LD2_Arcila_Yactayo/act3/scripts/generar_figura8_editorial.py
python LD2_Arcila_Yactayo/act3/scripts/regenerar_figura_consolidacion.py

# Actividad 4
python LD2_Arcila_Yactayo/act4/scripts/generar_figuras_act4.py

# Actividad 5
python LD2_Arcila_Yactayo/act5/scripts/generar_figuras_act5.py
```

---

## 5. Nota Técnica: Netlists `.cir` frente a Esquemas `.asc`

Conforme a lo especificado en la Sección 12 de la guía docente, se aclara formalmente que todos los diseños fueron implementados como **netlists SPICE puros (`.cir`)** en lugar de esquemas gráficos `.asc`. 

Esta decisión responde al rigor físico indispensable en tecnología nanométrica (BSIM4 Level 54 sub-45 nm):
1. **Modelado geométrico exacto de difusiones:** Inclusión de parámetros `AS`, `AD`, `PS` y `PD` en cada terminal de drenador y fuente, fundamentales para calcular con exactitud la redistribución de carga y las capacidades parásitas de unión.
2. **Control numérico estricto:** Ajuste explícito de tolerancias de convergencia (`abstol=1e-14`, `gmin=1e-15`, `cshunt=1e-18`) para evitar pérdidas numéricas artificiales de carga en nodos de alta impedancia durante períodos de retención prolongados ($>1.0\text{ }\mu\text{s}$).
3. **Automatización de mediciones:** Sentencias `.meas` directas para la extracción determinista de retardos, droop, integrales de energía y tiempos de retención.

LTspice reconoce y ejecuta de forma nativa e idéntica los archivos `.cir`. La correspondencia completa se encuentra documentada en [trazabilidad_figuras.txt](trazabilidad_figuras.txt).

---

## 6. Estado de la Actividad 6 (Opcional)

Conforme a la estructura solicitada en la guía docente, la carpeta `act6/` está incluida formalmente. La Actividad 6 (*"Lógica CMOS Dinámica Multietapa Compleja"*), al ser de carácter opcional (+2 puntos), no fue desarrollada, focalizando el esfuerzo técnico en la verificación físico-matemática rigurosa, reproducibilidad experimental sin keepers ideales y calidad editorial del informe maestro en las Actividades 1 a 5.
