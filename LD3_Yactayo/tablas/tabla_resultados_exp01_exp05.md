# Tabla Comparativa de Resultados Experimentales: EXP-01 a EXP-05 (G3.1)
**Módulo:** Transistores IGBT en LTspice — LD3  
**Autor:** Leonardo Sait Yactayo Tolentino (`23190214`)  
**Fecha de Actualización:** 10 de octubre de 2026 (Revisión Científica G3.1)  
**Condición Base de Ensayo:** Doble Pulso (DPT), $V_{bus} = 400\text{ V}$, $L = 100\ \mu\text{H}$ ($R_{ser} = 1\text{ m}\Omega$), $R_G = 10\ \Omega$, $R_E = 0.001\ \Omega$, $T = 27^\circ\text{C}$.

---

## 1. Tabla Consolidada Cuantitativa (Valores Verificados SPICE / Python)

> [!NOTE]
> Los ensayos a $80\text{ A}$ corresponden a la parametrización del banco docente histórico de $20\ \mu\text{s}$ y deben interpretarse estrictamente como **ensayos exploratorios de sobrecarga severa** ($4.2\times$ sobre la corriente nominal continua del N-IGBT y $2.0\times$ del P-IGBT), fuera del área de operación segura (SOA) continuo.

| Parámetro / Métrica | N-IGBT Nominal | N-IGBT Sobrecarga | P-IGBT Nominal | P-IGBT Sobrecarga | Unidad | Definición Física / Procedencia |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Modelo SPICE** | `XIRGBC20S` | `XIRGBC20S` | `XPIGBT` | `XPIGBT` | — | Duncan Electronics / IR |
| **Corriente Nominal Continua** | 19.0 | 19.0 | 40.0 | 40.0 | A | Cabecera `.SUBCKT` ($25^\circ\text{C}$) |
| **Duración Pulso 1 ($t_{p1}$)** | 3.65 | 20.00 | 8.88 | 20.00 | $\mu$s | PWL $V_{pulse}$ |
| **Tiempo Muerto ($t_{dead}$)** | 5.00 | 5.00 | 5.00 | 5.00 | $\mu$s | PWL $V_{pulse}$ ($0\text{ V}$) |
| **Duración Pulso 2 ($t_{p2}$)** | 1.00 | 1.00 | 1.00 | 1.00 | $\mu$s | PWL $V_{pulse}$ |
| **$I_C$ antes del 2do Apagado ($I_{C,\text{on}}$)** | **19.00** | **82.31** | **40.02** | **83.22** | A | Medido a $t_{\text{off2}} - 50\text{ ns}$ |
| **$V_{CE}$ en Conducción ($V_{CE,\text{on}}$)** | **1.88** | **6.57** | **2.51** | **4.25** | V | Caída directa de saturación |
| **Pico de Sobretensión ($V_{CE,\text{peak}}$)** | **400.99** | **401.66** | **401.22** | **401.67** | V | Fijación de diodo $D_1$ ($L \cdot di/dt$) |
| **Sobreimpulso de Compuerta ($V_{GE,\text{peak}}$)** | **+18.63** | **+17.06** | **-17.47** | **-17.80** | V | Acoplamiento capacitivo Miller ($C_{GD}$) |
| **Instante 90% $V_{GE}$ ($t_{vge90}$)** | 19.862 | 36.011 | 25.093 | 36.013 | $\mu$s | Flanco de apagado $V_{GE} = \pm 13.5\text{ V}$ |
| **Instante 90% $I_C$ ($t_{ic90}$)** | 20.012 | 36.115 | 25.288 | 36.185 | $\mu$s | Flanco de caída $I_C = 0.90 \cdot I_{C,\text{on}}$ |
| **Retardo de Apagado ($t_{d(\text{off})}$)** | **150.83** | **103.32** | **194.57** | **172.32** | ns | Intervalo 90% $V_{GE} \to$ 90% $I_C$ (Guía 5.1.4.3) |
| **Instante 10% $I_C$ ($t_{ic10}$)** | 20.198 | 36.311 | 25.556 | 36.460 | $\mu$s | Flanco de caída $I_C = 0.10 \cdot I_{C,\text{on}}$ |
| **Tiempo de Caída ($t_f$)** | **185.24** | **196.03** | **268.42** | **275.03** | ns | Intervalo 90% $I_C \to$ 10% $I_C$ |
| **Tiempo de Apagado Total ($t_{\text{off}}$)** | **336.07** | **299.35** | **463.00** | **447.36** | ns | $t_{d(\text{off})} + t_f$ |
| **Energía de Apagado Total ($E_{\text{off}}$)** | **691.5** | **3402.5** | **2115.3** | **4698.9** | $\mu$J | $\int v_{CE} \cdot i_C dt$ en ventana de apagado |

---

## 2. Cotejo Riguroso frente a Hoja de Datos Oficial (IRGBC20S)

> [!IMPORTANT]
> **Fuente de Verdad del Fabricante:** International Rectifier, *IRGBC20S Standard Speed IGBT* ([Datasheet Farnell 68617.pdf](https://www.farnell.com/datasheets/68617.pdf)).  
> Las condiciones de prueba del fabricante difieren sustancialmente del banco de laboratorio y explican las divergencias numéricas observadas entre el componente físico y el macromodelo de Duncan Electronics.

| Parámetro | Hoja de Datos IRGBC20S (Farnell 68617) | Condiciones del Fabricante | Valor Simulado en LTspice (XIRGBC20S) | Condiciones de Simulación LD3 | Análisis Físico y Razón de la Divergencia |
| :--- | :---: | :--- | :---: | :--- | :--- |
| **$V_{CE(\text{on})}$ a $10\text{ A}$** | **$1.80\text{ V}$** (típico), $2.4\text{ V}$ (máx.) | $I_C = 10\text{ A}, V_{GE} = 15\text{ V}, T_j = 25^\circ\text{C}$ | **$1.35\text{ V}$** | $I_C = 10\text{ A}, V_{GE} = 15\text{ V}, T_j = 27^\circ\text{C}$ | El macromodelo presenta una resistencia de modulación ligeramente menor a baja corriente. |
| **$V_{CE(\text{on})}$ a $19\text{ A}$** | **$2.40\text{ V}$** (típico), $3.0\text{ V}$ (máx.) | $I_C = 19\text{ A}, V_{GE} = 15\text{ V}, T_j = 25^\circ\text{C}$ | **$1.88\text{ V}$** | $I_C = 19\text{ A}, V_{GE} = 15\text{ V}, T_j = 27^\circ\text{C}$ | El modelo simula $V_{CE(\text{on})}$ $0.52\text{ V}$ más bajo que el típico de catálogo a corriente nominal. |
| **Retardo Apagado $t_{d(\text{off})}$** | **$820\text{ ns}$** (típico), $1000\text{ ns}$ (máx.) | $V_{CC}=480\text{ V}, I_C=10\text{ A}, R_G=50\ \Omega, L=100\ \mu\text{H}$ | **$150.8\text{ ns}$** | $V_{CC}=400\text{ V}, I_C=19\text{ A}, R_G=10\ \Omega, L=100\ \mu\text{H}$ | **Discrepancia crítica:** El IRGBC20S real es un IGBT *Standard Speed* lento ($\le 1\text{ kHz}$) ensayado con $R_G = 50\ \Omega$. El macromodelo `nigbt.lib` (Duncan 1995) fue calibrado con $T_F = 16.8\text{ ns}$, actuando como un dispositivo mucho más rápido, y la menor $R_G$ ($10\ \Omega$) acelera la descarga de compuerta. |
| **Tiempo de Caída $t_f$** | **$910\text{ ns}$** (típico), $1500\text{ ns}$ (máx.) | $V_{CC}=480\text{ V}, I_C=10\text{ A}, R_G=50\ \Omega, L=100\ \mu\text{H}$ | **$185.2\text{ ns}$** | $V_{CC}=400\text{ V}, I_C=19\text{ A}, R_G=10\ \Omega, L=100\ \mu\text{H}$ | El tiempo de recombinación en el modelo conductual subestima la cola lenta del silicio estándar real. |
| **Energía Apagado $E_{\text{off}}$** | **$3.90\text{ mJ}$** ($3900\ \mu\text{J}$) | $V_{CC}=480\text{ V}, I_C=10\text{ A}, R_G=50\ \Omega, L=100\ \mu\text{H}$ | **$0.69\text{ mJ}$** ($691.5\ \mu\text{J}$) | $V_{CC}=400\text{ V}, I_C=19\text{ A}, R_G=10\ \Omega, L=100\ \mu\text{H}$ | Consecuencia directa de conmutar en $\approx 336\text{ ns}$ vs $\approx 1730\text{ ns}$ en catálogo bajo menor tensión de barra. |

---

## 3. Análisis de Sensibilidad: Corriente y Energía de Cola ($I_{\text{tail}}$, $E_{\text{tail}}$)

El inicio de la corriente de cola no es una discontinuidad matemática abrupta, sino una transición gradual donde la corriente de canal MOS se extingue y predomina la recombinación bipolar. Se evaluó la sensibilidad variando el umbral de detección de quiebre de pendiente $|dI_C/dt|$ al $3\%$, $5\%$ y $10\%$ del valor máximo:

| Dispositivo / Caso | Criterio de Umbral de Pendiente | $t_{\text{tail}}\ [\mu\text{s}]$ | $I_{C,\text{tail}}\ [\text{A}]$ | $\% \text{ de } I_{C,\text{on}}$ | $E_{\text{tail}}\ [\mu\text{J}]$ | $\%E_{\text{tail}} / E_{\text{off}}$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **N-IGBT Nominal ($19\text{ A}$)** | $3\%$ de $|dI/dt|_{\text{max}}$ | 20.3035 | 0.556 | 2.92% | 19.9 | 2.88% |
| | **$5\%$ de $|dI/dt|_{\text{max}}$ (Base)** | **20.2585** | **0.936** | **4.93%** | **32.7** | **4.73%** |
| | $10\%$ de $|dI/dt|_{\text{max}}$ | 20.1985 | 1.881 | 9.90% | 64.3 | 9.31% |
| **P-IGBT Nominal ($40\text{ A}$)** | $3\%$ de $|dI/dt|_{\text{max}}$ | 25.7196 | 1.076 | 2.69% | 55.5 | 2.62% |
| | **$5\%$ de $|dI/dt|_{\text{max}}$ (Base)** | **25.6546** | **1.812** | **4.53%** | **91.6** | **4.33%** |
| | $10\%$ de $|dI/dt|_{\text{max}}$ | 25.5696 | 3.590 | 8.97% | 178.5 | 8.44% |
| **N-IGBT Sobrecarga ($80\text{ A}$)**| $3\%$ de $|dI/dt|_{\text{max}}$ | 36.4570 | 1.447 | 1.76% | 48.5 | 1.43% |
| | **$5\%$ de $|dI/dt|_{\text{max}}$ (Base)** | **36.4170** | **2.307** | **2.80%** | **76.5** | **2.25%** |
| | $10\%$ de $|dI/dt|_{\text{max}}$ | 36.3570 | 4.645 | 5.64% | 152.4 | 4.48% |
| **P-IGBT Sobrecarga ($80\text{ A}$)**| $3\%$ de $|dI/dt|_{\text{max}}$ | 36.6480 | 1.766 | 2.12% | 87.9 | 1.87% |
| | **$5\%$ de $|dI/dt|_{\text{max}}$ (Base)** | **36.5880** | **2.861** | **3.44%** | **140.4** | **2.99%** |
| | $10\%$ de $|dI/dt|_{\text{max}}$ | 36.4980 | 5.908 | 7.10% | 286.3 | 6.09% |

* **Conclusión de Sensibilidad:** Al pasar del $3\%$ al $10\%$, la corriente asignada a la cola se triplica ($\approx 0.56\text{ A} \to 1.88\text{ A}$ en N-IGBT) y la energía atribuida pasa de $2.9\%$ a $9.3\%$. El valor operacional del $5\%$ se sitúa sólidamente en el codo de la transición sin capturar la caída abrupta del canal MOS.

---

## 4. Comparación de Ventanas de Integración de $E_{\text{off}}$

Se verificó numéricamente la ausencia de contaminación con energía de encendido o conducción estática previa:
* **Ventana A:** Desde el inicio del comando de apagado ($t_{\text{off2}}$) hasta el final del transitorio ($25\ \mu\text{s} / 30\ \mu\text{s}$).
* **Ventana B:** Desde el cruce del $90\%$ de $V_{GE}$ hasta el final del transitorio.
* **Ventana C (Estándar IEC 60747-9):** Desde $V_{CE} = 10\% V_{bus} = 40\text{ V}$ hasta $I_C = 2\% I_{C,\text{on}}$.

| Caso Evaluado | Ventana A (Flanco Pulso) | Ventana B (90% $V_{GE}$) | Ventana C (IEC 10% a 2%) | Diferencia C vs A |
| :--- | :---: | :---: | :---: | :---: |
| **N-IGBT Nominal ($19\text{ A}$)** | **$691.5\ \mu\text{J}$** | **$691.0\ \mu\text{J}$** | **$665.2\ \mu\text{J}$** | $-3.8\%$ |
| **P-IGBT Nominal ($40\text{ A}$)** | **$2115.3\ \mu\text{J}$** | **$2113.5\ \mu\text{J}$** | **$2032.6\ \mu\text{J}$** | $-3.9\%$ |
| **N-IGBT Sobrecarga ($80\text{ A}$)** | **$3402.5\ \mu\text{J}$** | **$3394.3\ \mu\text{J}$** | **$3272.3\ \mu\text{J}$** | $-3.8\%$ |
| **P-IGBT Sobrecarga ($80\text{ A}$)** | **$4698.9\ \mu\text{J}$** | **$4693.6\ \mu\text{J}$** | **$4525.7\ \mu\text{J}$** | $-3.7\%$ |

* **Consistencia:** Las Ventanas A y B coinciden con un error inferior al $0.1\%$, confirmando que la conducción previa a la caída de compuerta está completamente excluida. La norma IEC reduce la energía en $\approx 3.8\%$ al omitir las colas asintóticas residuales por debajo del $2\%$.

---

## 5. Ensayo Controlado a Igual Corriente ($19\text{ A}$): N-IGBT vs P-IGBT

Para desambiguar si la diferencia de desempeño se debe a la corriente operativa ($19\text{ A}$ vs $40\text{ A}$) o a la física intrínseca del canal, se simuló el P-IGBT bajo idéntica corriente ($I_C = 19.48\text{ A}$), $V_{bus} = 400\text{ V}$, $R_G = 10\ \Omega$ y $L = 100\ \mu\text{H}$:

| Métrica Dinámica | N-IGBT (`XIRGBC20S`, $19\text{ A}$) | P-IGBT (`XPIGBT`, $19\text{ A}$) | Diferencia Relativa P vs N | Causa Física |
| :--- | :---: | :---: | :---: | :--- |
| **Corriente Conducida $I_{C,\text{on}}$** | $19.00\text{ A}$ | $19.48\text{ A}$ | $+0.48\text{ A}$ | Condición normalizada de ensayo |
| **Tensión Conducción $|V_{CE,\text{on}}|$** | $1.88\text{ V}$ | $1.72\text{ V}$ | $-0.16\text{ V}$ ($-8.5\%$) | Menor densidad de corriente en P (área de $40\text{ A}$) |
| **Retardo Apagado $t_{d(\text{off})}$** | **$152.2\text{ ns}$** | **$214.2\text{ ns}$** | **$+62.0\text{ ns}$ ($+40.7\%$)** | Mayor capacitancia de compuerta en P ($C_{GE} = 1.42\text{ nF}$ vs $0.68\text{ nF}$) |
| **Tiempo de Caída $t_f$** | **$186.3\text{ ns}$** | **$267.9\text{ ns}$** | **$+81.6\text{ ns}$ ($+43.8\%$)** | Mayor tiempo de tránsito BJT en P ($T_F = 24.3\text{ ns}$ vs $16.8\text{ ns}$) |
| **Tiempo Total $t_{\text{off}}$** | **$338.5\text{ ns}$** | **$482.2\text{ ns}$** | **$+143.6\text{ ns}$ ($+42.4\%$)** | Conmutación global significativamente más lenta |
| **Energía Apagado $E_{\text{off}}$** | **$691.5\ \mu\text{J}$** | **$1011.8\ \mu\text{J}$** | **$+320.3\ \mu\text{J}$ ($+46.3\%$)** | Mayor solapamiento $V \cdot I$ debido a la menor velocidad |
| **Fracción de Cola $\%E_{\text{tail}}$** | $4.73\%$ | $5.85\%$ | $+1.12\%$ | Mayor acumulación de carga minoritaria de base |

* **Hallazgo Clave:** A idéntica corriente, **el canal P es $\approx 42\%$ más lento y disipa $\approx 46\%$ más energía de apagado**, confirmando que las limitaciones de movilidad de portadores minoritarios y mayores capacitancias de unión son inherentes a la estructura de canal P.
