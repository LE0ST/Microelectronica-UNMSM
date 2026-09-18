# Matriz de Requisitos y Trazabilidad — LD2

**Curso:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)  
**Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Docente:** MsC. Luz Adanaqué Infante  
**Autores:** Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)  
**Documento base:** `Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf` (14 de septiembre de 2026)

---

## 1. Clasificación Metodológica

Cada ítem de esta matriz distingue explícitamente entre:
* **[REQ-EXP-OBL]:** Requisito explícito y obligatorio de la guía oficial o rúbrica docente.
* **[REQ-EXP-OPC]:** Requisito explícito y opcional de la guía oficial (actividad de bonificación de +2 puntos).
* **[DEC-ING]:** Decisión de ingeniería o recomendación metodológica del equipo para garantizar trazabilidad, reproducibilidad y robustez numérica.

---

## 2. Matriz Completa de Requisitos

| ID | Origen (Guía) | Actividad / Módulo | Tipo | Categoría | Descripción Técnica del Requisito | Evidencia Requerida | Sección Futura del Informe |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-01** | §4.1 | Preparación | Configuración | [REQ-EXP-OBL] | Renombrar modelos PTM (`ptm45hp.lib`, `ptm45lp.lib`, `ptm130.lib`) para evitar colisiones `.model nmos/pmos`. | Salida de `grep "^.model"` con 6 modelos únicos. | Sección 2 / Anexo A |
| **REQ-02** | §4.3, Rúbrica | Preparación | Simulación | [REQ-EXP-OBL] | Configurar solver: `gmin=1e-15`, `abstol=1e-14`, `reltol=1e-4`, `method=gear`. Justificar necesidad física. | Línea `.options` en netlists y texto justificativo. | Sección 2 |
| **REQ-03** | §5 (Tarea 1) | Actividad 1 | Simulación | [REQ-EXP-OBL] | Simular NAND3 dinámica footed (45nm HP, 1V, 500MHz) y capturar en una sola gráfica `V(clk)`, `V(a)`, `V(dyn)`, `V(out)`. | Gráfica 4 paneles/trazas anotando fases y estado flotante. | Sección 3 (Fig. 1) |
| **REQ-04** | §5 (Tarea 2) | Actividad 1 | Simulación / Análisis | [REQ-EXP-OBL] | Medir `tpHL` (evaluación) y `tpLH` (precarga). Explicar asimetría y por qué `tpLH` no cuenta como retardo lógico dominó. | Valores numéricos (.meas) y justificación de temporización. | Sección 3 |
| **REQ-05** | §5 (Tarea 3) | Actividad 1 | Simulación / Comparación | [REQ-EXP-OBL] | Diseñar NAND3 estática equivalente ($W_n=3W_n$, $W_p=135$nm) y completar tabla comparativa (6 métricas). | Tabla 1 completa: transistores, `tpHL`, `tpLH`, `Cin`, $P_{avg}$ conmutando, $P_{avg}$ estático. | Sección 3 (Tabla 1) |
| **REQ-06** | §5 (Tarea 4) | Actividad 1 | Cálculo / Simulación | [REQ-EXP-OBL] | Calcular potencia dinámica $P = \alpha C_{dyn} V_{DD}^2 f$ ($\alpha=1$) y comparar con simulación con entradas fijas en 1. | Cálculo analítico vs valor `.meas Pavg`; explicación física del exceso. | Sección 3 |
| **REQ-07** | §5 (Tarea 5) | Actividad 1 | Simulación | [REQ-EXP-OBL] | Abrir PDN ($V_c=0$) y comparar retención con $T_{clk}=2$ns vs $T_{clk}=400$ns ($t_{tran}=200$ns). Punto de partida para fugas. | Formas de onda comparativas de caída en $V(dyn)$. | Sección 3 (Fig. 2) |
| **REQ-08** | §6.2, Rúbrica | Actividad 2 | Cálculo Analítico | [REQ-EXP-OBL] | Predecir analíticamente $C_a = C_{n1} + C_{n2}$ con difusión BSIM4 ($L_{diff}=90$nm, $c_j, c_{jsw}$) y $\Delta V_{pred} = V_{DD} C_a / (C_a + C_L)$. | Deducción paso a paso previa a simular; comparación con márgenes de ruido. | Sección 4 (Pre-cálculo) |
| **REQ-09** | §6.3 (Tarea 1) | Actividad 2 | Simulación / Análisis | [REQ-EXP-OBL] | Simular peor caso (ciclo 1 descarga, ciclo 2 comparte con $A=B=1, C=0$) con `AS/AD/PS/PD`. Medir $\Delta V$ y explicar discrepancia. | Valor `.meas dV` vs $\Delta V_{pred}$; explicación de corte en $V_{GS} \le V_{th}$. | Sección 4 |
| **REQ-10** | §6.3 (Tarea 2) | Actividad 2 | Simulación / Gráfica | [REQ-EXP-OBL] | Barrido $C_L \in [0.5, 4]$ fF. Graficar $\Delta V$ vs $C_L$ con curva teórica superpuesta; rango de falla lógica en $V(out)$. | Gráfica $\Delta V(C_L)$ con umbrales lógicos $V_M$. | Sección 4 (Fig. 3) |
| **REQ-11** | §6.3 (Tarea 3) | Actividad 2 | Simulación / Diseño | [REQ-EXP-OBL] | Mitigación 1: Precarga de nodos internos $n_1, n_2$ con PMOS a CLK. Medir $\Delta V$, evaluar costo en reloj y área, justificar por qué no $n_3$. | Netlist, curvas mitigadas, balance área/carga de reloj. | Sección 4 |
| **REQ-12** | §6.3 (Tarea 4) | Actividad 2 | Simulación / Diseño | [REQ-EXP-OBL] | Mitigación 2: Reordenar PDN (entrada crítica $C$ arriba vs abajo). Justificar por qué el apilamiento es decisión en dominó. | Formas de onda comparativas y tiempos de respuesta. | Sección 4 |
| **REQ-13** | §6.3 (Tarea 5) | Actividad 2 | Simulación / Diseño | [REQ-EXP-OBL] | Mitigación 3: Incorporar keeper $W_{kp}=45$nm. Evaluar si recupera $V(dyn)$ y tiempo de restablecimiento. | Curvas transitorias con keeper vs sin keeper. | Sección 4 |
| **REQ-14** | §7 (Tarea 1) | Actividad 3 | Simulación / Análisis | [REQ-EXP-OBL] | Retención a reloj detenido ($T_{stop}=1\mu$s, 45nm HP, 27°C). Barrido $W_{kp} \in [1\text{n}, 180\text{n}]$. Medir $V_{dyn,end}, t_{hold}, I_{leak,tot}$. | Tabla de barrido; gráfica de descarga; aislamiento .dc de subumbral/compuerta/GIDL. | Sección 5 |
| **REQ-15** | §7 (Tarea 2) | Actividad 3 | Simulación / Análisis | [REQ-EXP-OBL] | Repetir a 85°C. Cuantificar factor de aumento de $I_{leak}$ vs fórmula teórica de corriente subumbral y corrimiento de $V_{th}(T)$. | Razón $I_{leak}(85)/I_{leak}(27)$ simulada vs analítica. | Sección 5 |
| **REQ-16** | §7 (Tarea 3) | Actividad 3 | Simulación / Tabla | [REQ-EXP-OBL] | Caracterizar 45nm LP (1.1V) y 130nm bulk (1.3V). Completar tabla de fugas, $t_{hold}$ y $W_{kp,min}$ para retención $>0.9V_{DD}$. | Tabla comparativa de 5 filas (o 6 filas con 130nm a 85°C). | Sección 5 (Tabla 2) |
| **REQ-17** | §7 (Tarea 4) | Actividad 3 | Simulación / Gráfica | [REQ-EXP-OBL] | Evaluación de contención: con $W_{kp,min}$ de HP/85°C, medir $t_{pHL}$ vs $W_{kp}$ y graficar frente a razón $r$. Marcar punto de degradación 10%. | Gráfica $t_{pHL}(W_{kp})$ con asíntota del 10% de penalización. | Sección 5 (Fig. 4) |
| **REQ-18** | §7 (Tarea 5) | Actividad 3 | Diseño / Simulación | [REQ-EXP-OBL] | Pregunta de diseño: ¿Existe $W_{kp}$ para retención $>0.9V_{DD}$ y contención $<10$% en HP y LP? Proponer y simular keeper condicional. | Esquema y simulación de keeper condicional con 3 inversores de retardo. | Sección 5 |
| **REQ-19** | §8.1 (Tareas 1-2) | Actividad 4 | Simulación / Análisis | [REQ-EXP-OBL] | Demostrar violación de monotonicidad en cascada directa $dyn1 \to etapa2$; medir descarga errónea de $dyn2$. Corregir con inversor dominó. | Formas de onda $V(dyn1), V(dyn2)$ con y sin inversor intermedio. | Sección 6 (Fig. 5) |
| **REQ-20** | §8.1 (Tarea 3) | Actividad 4 | Simulación / Análisis | [REQ-EXP-OBL] | Simular entrada $X$ con pulso descendente en evaluación. Analizar por qué la regla aplica a todas las entradas y ligar con flip-flops (TGFF). | Formas de onda de falla y análisis de flip-flops de interfaz. | Sección 6 |
| **REQ-21** | §8.2 (Tareas 1-3) | Actividad 4 | Simulación / Análisis | [REQ-EXP-OBL] | Cascada dominó de 3 etapas footed vs unfooted bajo barrido $T_{skew} \in [-50\text{p}, 200\text{p}]$. Medir $I_{pk}$ de cortocircuito y retardo. | Tabla/gráfica de $I_{pk}(T_{skew})$ y retardo; condición numérica para omitir footer. | Sección 6 (Fig. 6) |
| **REQ-22** | §9.1 (Tareas 1-2) | Actividad 5 | Simulación / Análisis | [REQ-EXP-OBL] | Medir sobreimpulso y subimpulso por clock feedthrough ($C_L=0.5$fF, flancos 5ps). Correlacionar con $C_{gd}/(C_{gd}+C_L)$ y recorte por diodo D-B. | Formas de onda de feedthrough, cálculo analítico de amplitud y análisis de diodo. | Sección 7 (Fig. 7) |
| **REQ-23** | §9.2 (Tareas 1-2) | Actividad 5 | Simulación / Gráfica | [REQ-EXP-OBL] | Barrido $V_{DD} \in [0.35, 1.0]$V en 45nm HP. Medir $t_{eval}$ y $t_{hold}$; calcular $f_{max}, f_{min}$; graficar ventana y hallar $V_{DD,min}$ de cierre. | Gráfica semi-logarítmica de $f_{max}, f_{min}$ vs $V_{DD}$ reproduciendo Fig. 9. | Sección 7 (Fig. 8) |
| **REQ-24** | §9.2 (Tareas 3-4) | Actividad 5 | Simulación / Análisis | [REQ-EXP-OBL] | Evaluar efecto del keeper ($W_{kp}=45, 90$nm) y proceso 45nm LP en NTV. Comparar razón $I_{on}/I_{off}$. | Curvas de ventana con keeper y análisis de viabilidad subumbral en LP. | Sección 7 |
| **REQ-25** | §9.2 (Tarea 5) | Actividad 5 | Redacción Conclusión | [REQ-EXP-OBL] | Conclusión obligatoria sobre viabilidad de lógica dominó en NTV (máximo 10 líneas, condiciones de $T, f$, keeper, proceso). | Texto estructurado de máx. 10 líneas en sección Conclusiones. | Sección 8 / Conclusiones |
| **REQ-26** | §10, Rúbrica | Actividad 6 | Simulación Opcional | [REQ-EXP-OPC] | Actividad opcional (+2 pts): NP-domino (zipper) $F=(A\cdot B+C)\cdot \overline{D}$ (etapa n alimentando etapa p sin inversor). | Esquema, verificación funcional, medición de retardo y discusión de fases. | Sección 9 (Anexo B) |
| **REQ-27** | §11, Rúbrica | Cuestionario | Análisis Teórico | [REQ-EXP-OBL] | Responder 20 preguntas teóricas cortas (máx. 5 líneas c/u) con rigor físico y sin copias directas. | Cuestionario resuelto de 20 preguntas numeradas P1 a P20. | Sección 10 (Cuestionario) |
| **REQ-28** | §12, Rúbrica | Informe | Formato | [REQ-EXP-OBL] | Informe técnico en PDF de máximo 20 páginas. Ejes rotulados con unidades; tablas numéricas; referencia al esquemático/netlist generador. | Documento PDF compilado $\le 20$ páginas. | Informe Maestro |
| **REQ-29** | §12, Rúbrica | Entregables | Empaquetado | [REQ-EXP-OBL] | Archivo `.zip` con carpetas `act1/`...`act6/`, archivos `.lib` renombrados y `README.txt` reproducible. | Archivo comprimido verificado y ejecutable. | `entregables/` |
| **REQ-30** | Buenas Prácticas | General | Metodología | [DEC-ING] | Trazabilidad completa: netlist $\to$ simulación $\to$ log $\to$ CSV/JSON $\to$ figura $\to$ tabla LaTeX. Cero valores hardcodeados. | Scripts automatizados de extracción en `scripts/`. | Arquitectura global |
