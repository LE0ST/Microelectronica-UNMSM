# Actividad 3 — Restauración y Robustez: Dimensionamiento de Keeper y Contención

**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
**Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Docente:** MsC. Luz Adanaqué Infante  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Directorio de Trabajo:** [`LD2_Arcila_Yactayo/act3/`](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act3/)  
**Tecnologías Evaluadas:** PTM 45nm HP, PTM 45nm LP, PTM 130nm Bulk  

---

## 1. Topología del Circuito y Función del Keeper PMOS

En la compuerta NAND3 dinámica dominó, el nodo dinámico `dyn` queda flotante durante la fase de evaluación ($CLK = 1$) cuando las entradas no activan la red de descenso (PDN abierta). En tecnologías submicrométricas profundas (45 nm), las corrientes de fuga subumbral ($I_{sub}$) y de túnel de compuerta ($I_{gate}$) descargan progresivamente el nodo, amenazando la integridad del estado lógico.

Para contrarrestar esta pérdida de carga sin comprometer la velocidad de conmutación:
* Se conecta un transistor **keeper PMOS** ($M_k$) con su fuente a $V_{DD}$, su drenaje a `dyn` y su compuerta gobernada por la salida invertida `out`.
* Cuando `dyn` está alto, `out = 0`, encendiendo $M_k$ para reinyectar corriente compensatoria ($I_{kp} \ge I_{leak,tot}$).
* Si la PDN evalúa a tierra ($A=B=C=1$), la PDN debe vencer la corriente inyectada por $M_k$ hasta forzar la conmutación de `out` a alto (bloqueando a $M_k$). Esta contención dinámica introduce una penalización de retardo $\Delta t_{pHL}$.

---

## 2. Campaña de Retención Temporal (Ventana de $1.0\ \mu\text{s}$)

Se evaluó la retención de carga bajo el criterio normativo de la guía ($V_{dyn}(1\,\mu\text{s}) > 0.90\,V_{DD}$) a $27^\circ\text{C}$ y $85^\circ\text{C}$:

| Tecnología | Temp | $V_{dyn}(1\,\mu\text{s})$ Sin Keeper | $t_{\text{hold}}$ a $0.90\,V_{DD}$ | Estado Sin Keeper | Con Keeper ($W_{kp}=22\text{ nm}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **PTM 45nm HP** | $27^\circ\text{C}$ | $0.9370\text{ V}$ | $> 1.0\ \mu\text{s}$ | Cumple retención | $0.999994\text{ V}$ (Estable) |
| **PTM 45nm HP** | $85^\circ\text{C}$ | $0.7836\text{ V}$ | **$608.17\text{ ns}$** | **Falla retención** | $0.999975\text{ V}$ (Estable) |
| **PTM 45nm LP** | $85^\circ\text{C}$ | $0.9997\text{ V}$ | $> 1.0\ \mu\text{s}$ | Cumple retención | $1.000000\text{ V}$ (Estable) |
| **PTM 130nm** | $85^\circ\text{C}$ | $0.9985\text{ V}$ | $> 1.0\ \mu\text{s}$ | Cumple retención | $1.000000\text{ V}$ (Estable) |

### Diagnóstico Físico:
1. En 45nm HP a $85^\circ\text{C}$, el incremento térmico de corriente subumbral ($I_{sub} \propto T^2 \exp(-qV_{th}/mkT)$) reduce el tiempo de retención a $608.17\text{ ns}$, exigiendo obligatoriamente un keeper activo.
2. En 45nm LP y 130nm Bulk, las tensiones de umbral más elevadas y espesores de óxido mayores reducen las fugas en varios órdenes de magnitud, haciendo que el keeper sea prescindible desde el punto de vista puramente estático a baja frecuencia.

---

## 3. Compromiso de Contención y Ventana de Viabilidad Conjunta

La guía oficial exige que la penalización relativa de retardo introducida por el keeper sea estrictamente inferior al 10%:
$$\Delta t_{pHL} = \frac{t_{pHL}(W_{kp}) - t_{pHL}(W_{kp}=0)}{t_{pHL}(W_{kp}=0)} \times 100\% < 10.00\%$$

Se realizó una malla fina de simulación con paso de $1\text{ nm}$ en 45nm HP a $85^\circ\text{C}$:

| $W_{kp}$ (nm) | Razón $r = W_{kp}/(67.5\text{ nm})$ | $V_{dyn}(1\,\mu\text{s})$ | Retención ($>0.9V_{DD}$) | $\Delta t_{pHL}$ (%) | Contención ($<10\%$) | Viabilidad Conjunta |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10.5** | 0.156 | 0.999968 V | SÍ | +3.64% | SÍ | **VIABLE (Mínimo)** |
| **15.0** | 0.222 | 0.999971 V | SÍ | +4.18% | SÍ | **VIABLE** |
| **22.0** | 0.326 | 0.999975 V | SÍ | +5.34% | SÍ | **VIABLE (Referencia)** |
| **30.0** | 0.444 | 0.999981 V | SÍ | +6.82% | SÍ | **VIABLE** |
| **38.0** | 0.563 | 0.999985 V | SÍ | **+9.94%** | SÍ | **VIABLE (Máximo)** |
| **39.0** | 0.578 | 0.999986 V | SÍ | +10.23% | **NO** | NO VIABLE |
| **45.0** | 0.667 | 0.999988 V | SÍ | +12.90% | **NO** | NO VIABLE |
| **60.0** | 0.889 | 0.999992 V | SÍ | +20.43% | **NO** | NO VIABLE |

### Límites de Diseño Rigurosamente Verificados:
* **Ventana Viable en 45nm HP @ $85^\circ\text{C}$:**
  $$W_{kp} \in [10.5\text{ nm},\ 38.0\text{ nm}] \quad \iff \quad r \in [0.156,\ 0.563]$$
* El punto de referencia convencional ($W_{kp} = 22\text{ nm}$, $W_{eff} = 12\text{ nm}$, $r = 0.326$) opera holgadamente dentro de la ventana con $\Delta t_{pHL} \approx +5.34\%$, garantizando $V_{dyn}(1\,\mu\text{s}) = 0.999975\text{ V}$.

---

## 4. Alternativa Avanzada: Keeper Condicional

Para desacoplar el conflicto entre retención estática y contención dinámica:
* Se ensayó una topología de **keeper condicional con línea de retardo** (dos inversores CMOS auxiliares).
* Durante la conmutación rápida, el keeper permanece inicialmente inactivo por el retardo de compuerta, activándose únicamente si el nodo no conmuta tras el periodo de guarda.
* **Resultado:** La penalización de retardo se redujo a solo **$+5.11\%$** (frente a $+12.90\%$ en keeper convencional unitario), a cambio de una sobrecarga moderada en área y consumo de conmutación.

---

## 5. Inventario de Figuras Generadas (Actividad 3)

* [**`fig1_act3_retencion_formas_onda.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act3/figuras/fig1_act3_retencion_formas_onda.png): Evolución transitoria de $V(dyn)$ durante $1.0\ \mu\text{s}$ a $27^\circ\text{C}$ y $85^\circ\text{C}$ con y sin keeper.
* [**`fig2_act3_consolidacion_hp_lp_130.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act3/figuras/fig2_act3_consolidacion_hp_lp_130.png): Comparativa multitecnológica tridimensional de retención (HP vs LP vs 130nm).
* [**`fig3_act3_contencion_penalizacion.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act3/figuras/fig3_act3_contencion_penalizacion.png): Curvas de penalización $\Delta t_{pHL}$ frente a $W_{kp}$ y razón de aspecto $r$.
* [**`fig4_act3_ventana_viabilidad.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act3/figuras/fig4_act3_ventana_viabilidad.png): Delimitación de la ventana de viabilidad conjunta (retención $>0.9V_{DD}$ vs contención $<10\%$).
* [**`fig5_act3_keeper_condicional.png`**](file:///g:/Proyectos/MicroNano/LD2_Arcila_Yactayo/act3/figuras/fig5_act3_keeper_condicional.png): Formas de onda y análisis temporal del keeper condicional con línea de retardo.
