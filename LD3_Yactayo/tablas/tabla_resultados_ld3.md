# TABLA GENERAL CONSOLIDADA DE RESULTADOS EXPERIMENTALES (LD3)
## CARACTERIZACIÓN Y SIMULACIÓN COMPARATIVA DE TRANSISTORES IGBT EN LTSPICE

* **Proyecto:** Laboratorio Dirigido N.° 3 — Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)
* **Institución:** Universidad Nacional Mayor de San Marcos (UNMSM) — Facultad de Ingeniería Electrónica y Eléctrica (FIEE)
* **Autor:** Leonardo Sait Yactayo Tolentino (`23190214`)
* **Docente:** MsC. Luz Adanaqué Infante
* **Requisito Oficial Asociado:** Acápite 1 y Requisito `[REQ-TAB]` de la guía oficial ([`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`](../../Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf)).
* **Inventario Total de Condiciones:** **11 registros verificados** (5 condiciones para macromodelos Duncan Electronics y 6 condiciones para macromodelos Fuji Electric Serie X).

---

## 1. Advertencia Metodológica sobre Compatibilidad de Ensayos

> [!IMPORTANT]
> **Compatibilidad Instrumental y Metodológica entre Familias de Modelos:**
> Los resultados de la **Parte I (Macromodelos Duncan Electronics: EXP-01 a EXP-05)** y de la **Parte II (Macromodelos Fuji Electric Serie X: EXP-06 a EXP-09)** fueron obtenidos mediante procedimientos de instrumentación numérica diferenciados y adaptados a las particularidades de cada tarjeta de modelo:
> 1. **Sensor de Corriente y Energía:** En Duncan, la corriente se midió en el shunt de emisor de $1\text{ m}\Omega$ (`R2 VE 0 0.001`), integrando $V_{CE} \cdot I_E$ (lo que incluye la corriente capacitiva de compuerta $I_G$). En Fuji, se implementó un sensor ideal de $0\text{ V}$ (`Vsens_C`) en el colector, integrando la potencia neta de puerto. Ninguna de estas integrales se equipara directamente al calor interno del silicio sin un macromodelo térmico.
2. **Criterio de Corriente de Cola y Retardos:** En Duncan se empleó la detección analítica de quiebre de pendiente ($|dI_C/dt| \le 5\% |dI/dt|_{\text{max}}$), prescindiéndose de la columna de derivada máxima por no ser requerida por la guía docente. En Fuji se implementó la convención operacional unívoca del $5\%$ ($I_{C,\text{tail}} = 0.05 \cdot I_{C,\text{pre}}$). Los retardos Fuji de la tabla corresponden al método Python con $90\%$ de $V_{GE,\text{pre}}$ real (incremento de $+56.5\%$ al duplicar $R_G$, frente a $+60.4\%$ bajo directivas `.meas` con umbral fijo de $13.5\text{ V}$).
3. **Inductancia de Lazo:** En Duncan, los ensayos base operaron con lazo inductivo ideal ($L_\sigma = 0\text{ nH}$). En Fuji, todos los casos incorporan la inductancia física de lazo parásito de $L_\sigma = 25\text{ nH}$ ($R_{\text{ser}} = 10\text{ m}\Omega$) sin amortiguamiento paralelo artificial ($R_{\text{par}} = \text{None}$).
4. **Temperatura de Simulación:** Duncan se ejecutó a la temperatura por defecto de SPICE ($27\ ^\circ\text{C}$). Fuji se ejecutó con control térmico explícito a $25.0\ ^\circ\text{C}$ (`.temp 25`).
> 
> *Por tanto, las comparaciones cuantitativas directas deben realizarse estrictamente dentro de cada familia de ensayos.*

---

## 2. Tabla Consolidada Maestra: 11 Condiciones Experimentales

| Reg. | Familia / Ensayo | Caso / Configuración | Modelo SPICE | Encapsulado | $I_{\text{target}}$ [A] | $I_{C,\text{pre}}$ [A] | $V_{CE(\text{on})}$ [V] | $V_{CE,\text{peak}}$ [V] | Sobretensión vs Bus [$+V$] | $t_{d(\text{off})}$ [ns] | $t_f$ [ns] | $t_{d(\text{off}),\text{ds}}$ Catálogo | Discrepancia vs Catálogo | $E_{\text{off}}$ [µJ] | $I_{C,\text{tail}}$ [A] | $\%E_{\text{tail}}$ [%] | Estado QA |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **01** | Duncan (EXP-01/04) | N-IGBT Nominal | `XIRGBC20S` | TO-220 | $19.0$ | $19.00$ | $1.88$ | $400.99$ | $+0.99$ | $150.83$ | $185.24$ | $820\text{ ns}$ | $-81.6\%$ (Nota 1) | $691.5$ | $0.94$ | $4.73\%$ | **PASS** |
| **02** | Duncan (EXP-01/05) | N-IGBT Sobrecarga | `XIRGBC20S` | TO-220 | $80.0$ | $82.31$ | $6.57$ | $401.66$ | $+1.66$ | $103.32$ | $196.03$ | N/A (SOA) | Fuera de SOA | $3402.5$ | $2.31$ | $2.25\%$ | **PASS (Expl.)** |
| **03** | Duncan (EXP-02/04) | P-IGBT Nominal | `XPIGBT` | TO-220 | $40.0$ | $40.02$ | $2.51$ | $401.22$ | $+1.22$ | $194.57$ | $268.42$ | N/A | Genérico Duncan | $2115.3$ | $1.81$ | $4.33\%$ | **PASS** |
| **04** | Duncan (EXP-02/05) | P-IGBT Sobrecarga | `XPIGBT` | TO-220 | $80.0$ | $83.22$ | $4.25$ | $401.67$ | $+1.67$ | $172.32$ | $275.03$ | N/A (SOA) | Fuera de SOA | $4698.9$ | $2.86$ | $2.99\%$ | **PASS (Expl.)** |
| **05** | Duncan (EXP-02 Ctrl) | P-IGBT Control 19A | `XPIGBT` | TO-220 | $19.0$ | $19.48$ | $1.72$ | $401.01$ | $+1.01$ | N/V* | N/V* | N/A | Control vs N | $1011.8$ | N/V* | N/V* | **LOG (N/V*)** |
| **06** | Fuji (F01 / EXP-06) | 50A Discreto | `FGW50XS65` | TO-247 | $50.0$ | $50.013$ | $1.362$ | $442.36$ | $+42.36$ | $231.10$ | $31.38$ | $\approx 220\text{ ns}$ | $+5.0\%$ | $1066.98$ | $2.50$ | $0.44\%$ | **PASS** |
| **07** | Fuji (F02 / EXP-06/09) | 50A Co-Pack ($R_G 10$) | `FGW50XS65C` | TO-247 | $50.0$ | $50.012$ | $1.362$ | $442.36$ | $+42.36$ | $231.09$ | $31.38$ | $\approx 220\text{ ns}$ | $+5.0\%$ | $1066.98$ | $2.50$ | $0.44\%$ | **PASS** |
| **08** | Fuji (F03 / EXP-07/08) | 75A Discreto Nom. | `FGW75XS65` | TO-247 | $75.0$ | $75.230$ | $1.356$ | $445.98$ | $+45.98$ | $293.18$ | $40.48$ | $\approx 280\text{ ns}$ | $+4.7\%$ | $2052.75$ | $3.76$ | $0.37\%$ | **PASS** |
| **09** | Fuji (F04 / EXP-07) | 75A Co-Pack Nom. | `FGW75XS65C` | TO-247 | $75.0$ | $75.233$ | $1.356$ | $445.98$ | $+45.98$ | $293.16$ | $40.48$ | $\approx 280\text{ ns}$ | $+4.7\%$ | $2052.74$ | $3.76$ | $0.37\%$ | **PASS** |
| **10** | Fuji (F05 / EXP-08) | 75A Discreto 50A | `FGW75XS65` | TO-247 | $50.0$ | $50.362$ | $1.181$ | $436.37$ | $+36.37$ | $324.75$ | $34.18$ | N/A | Comparación a corriente igualada vs F01 | $1367.85$ | $2.52$ | $0.32\%$ | **PASS** |
| **11** | Fuji (F06 / EXP-09) | 50A Co-Pack ($R_G 20$) | `FGW50XS65C` | TO-247 | $50.0$ | $50.123$ | $1.392$ | $425.94$ | $+25.94$ | $361.60$ | $57.27$ | N/A | Sensibilidad $R_G$ | $1818.73$ | $2.51$ | $0.48\%$ | **PASS** |

---

## 3. Notas Técnicas y Justificación de Divergencias con Catálogo

1. **Nota 1 — Discrepancia del IRGBC20S frente a Catálogo Oficial Farnell 68617:**
   * Las condiciones de ensayo de la hoja de datos oficial de International Rectifier son: $V_{CC} = 480\text{ V}$, $I_C = 10\text{ A}$, $R_G = 50\ \Omega$, $T_j = 25^\circ\text{C}$, arrojando $t_{d(\text{off})} = 820\text{ ns}$ típico ($1200\text{ ns}$ máx.), $t_f = 910\text{ ns}$ típico ($1600\text{ ns}$ máx.) y $E_{\text{off}} = 3.90\text{ mJ}$.
   * El banco de simulación emplea: $V_{bus} = 400\text{ V}$, $I_C = 19\text{ A}$, $R_G = 10\ \Omega$.
   * La resistencia de compuerta $5\times$ menor ($10\ \Omega$ vs $50\ \Omega$) acelera fuertemente la evacuación de carga de compuerta $Q_G$. Además, el modelo `nigbt.lib` de Duncan parametriza un tiempo de tránsito bipolar rápido ($T_F = 16.8\text{ ns}$) e inductancia interna de emisor $LE = 7.5\text{ nH}$ en un subcircuito simplificado que no modela la totalidad de efectos físicos de recombinación lenta del silicio real.
2. **Nota 2 — Régimen Exploratorio de Sobrecarga a 80 A:**
   * Los registros 02 y 04 ($80\text{ A}$) corresponden a la duración de pulso de $20\ \mu\text{s}$ provista en la guía preliminar. Se clasifican como **exploratorios y fuera del Área de Operación Segura (SOA)**, ya que someten al transistor a $4.2\times$ su corriente nominal continua (en N-IGBT) y superan el límite pulsado máximo admisible de catálogo ($I_{CM} = 76\text{ A}$ frente a $82.31\text{ A}$ alcanzados), sirviendo únicamente para evaluar la robustez numérica del solver SPICE.
3. **Nota 3 — Exactitud en Modelos Fuji Electric Serie X:**
   * Los modelos Fuji de 7.ª generación Trench-FS presentan una coincidencia excelente con las hojas de datos del fabricante bajo condiciones comparables ($\approx 220\text{ ns}$ de catálogo vs $231\text{ ns}$ en SPICE para 50 A; $\approx 280\text{ ns}$ de catálogo vs $293\text{ ns}$ en SPICE para 75 A), validando la fidelidad del modelado físico de Fuji Electric.
4. **Nota 4 — Trazabilidad del Registro 05 (P-IGBT Control 19A):**
   * Los valores estáticos ($I_{C,\text{pre}} = 19.48\text{ A}$, $V_{CE(\text{on})} = 1.72\text{ V}$, $E_{\text{off}} = 1011.8\ \mu\text{J}$) están debidamente acreditados en el registro oficial `dpt_pigbt_19a.log`.
   * Los parámetros dinámicos ($t_{d(\text{off})}, t_f, I_{C,\text{tail}}, \%E_{\text{tail}}$) se identifican formalmente como `N/V*` (No Verificados) debido a la ausencia del archivo de simulación crudo (`dpt_pigbt_19a.raw`) en disco, evitando aserciones dinámicas que no cuenten con respaldo directo y reproducible en archivos conservados.
