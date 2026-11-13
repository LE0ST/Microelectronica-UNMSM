# TABLA CONSOLIDADA OFICIAL: SUITE FUJI ELECTRIC SERIE X
## EXPERIMENTOS EXP-06, EXP-07, EXP-08 Y EXP-09 (CONDICIÓN CONTROLADA A 25 °C)

* **Proyecto:** Microelectrónica y Sistemas Nanoelectrónicos — UNMSM (2026-II)
* **Autor:** Leonardo Sait Yactayo Tolentino (`23190214`)
* **Docente:** MsC. Luz Adanaqué Infante
* **Condiciones fijas de simulación:** $V_{\text{bus}} = 400.0\text{ V}$, $L_{\text{carga}} = 100\ \mu\text{H}$ ($R_{\text{ser}} = 1\text{ m}\Omega$), $L_\sigma = 25\text{ nH}$ ($R_{\text{ser}} = 10\text{ m}\Omega$, sin $R_{\text{par}}$ añadida), Diodo superior $D_1$ (`DMOD` con $TT = 35\text{ ns}$), Temperatura explícita `.temp 25` ($25.0\ ^\circ\text{C}$), Método de integración Gear, `abstol = 1e-8`, `reltol = 1e-3`, `maxstep = 1.0 ns`.
* **Sensores de corriente:** Sensores ideales de 0 V (`Vsens_C`, `Vsens_G`, `Vsens_E`) aislando puertos terminales del transistor.
* **Ventana de integración energética:** Iniciada estrictamente en el comando de apagado $t_3 = t_{\text{off2}}$ con duración fija de $5.10\ \mu\text{s}$ ($[t_3, t_3 + 5.10\ \mu\text{s}]$ adaptada a la secuencia DPT de cada caso).

---

### Matriz de Resultados Cuantitativos

| ID Caso | Modelo SPICE | Tipo Encapsulado | $I_{\text{target}}$ [A] | $I_{C,\text{pre}}$ [A] | Error $I_C$ [%] | $V_{CE(\text{on})}$ [V] | $V_{CE,\text{peak}}$ [V] | Sobretensión vs Bus [$+V$] | $t_{d(\text{off})}$ [ns] | $t_f$ [ns] | $di/dt_{\text{max}}$ [A/µs] | $E_{C,\text{net}}$ [µJ] | $E_{\text{tail}}$ [µJ] | $\%E_{\text{tail}}$ [%] | Status $\pm 1\%$ |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **F01** | `FGW50XS65` | Discreto | $50.0$ | $50.013$ | $+0.03\%$ | $1.362$ | $442.36$ | $+42.36$ | $231.10$ | $31.38$ | $1669.5$ | $1066.98$ | $4.68$ | $0.44\%$ | **PASS** |
| **F02** | `FGW50XS65C` | Co-Pack ($R_G=10$) | $50.0$ | $50.012$ | $+0.02\%$ | $1.362$ | $442.36$ | $+42.36$ | $231.09$ | $31.38$ | $1669.6$ | $1066.98$ | $4.68$ | $0.44\%$ | **PASS** |
| **F03** | `FGW75XS65` | Discreto ($75\text{ A}$) | $75.0$ | $75.230$ | $+0.31\%$ | $1.356$ | $445.98$ | $+45.98$ | $293.18$ | $40.48$ | $1818.0$ | $2052.75$ | $7.56$ | $0.37\%$ | **PASS** |
| **F04** | `FGW75XS65C` | Co-Pack ($75\text{ A}$) | $75.0$ | $75.233$ | $+0.31\%$ | $1.356$ | $445.98$ | $+45.98$ | $293.16$ | $40.48$ | $1818.4$ | $2052.74$ | $7.57$ | $0.37\%$ | **PASS** |
| **F05** | `FGW75XS65` | Discreto ($50\text{ A}$) | $50.0$ | $50.362$ | $+0.72\%$ | $1.181$ | $436.37$ | $+36.37$ | $324.75$ | $34.18$ | $1429.8$ | $1367.85$ | $4.39$ | $0.32\%$ | **PASS** |
| **F06** | `FGW50XS65C` | Co-Pack ($R_G=20$) | $50.0$ | $50.123$ | $+0.25\%$ | $1.392$ | $425.94$ | $+25.94$ | $361.60$ | $57.27$ | $1019.4$ | $1818.73$ | $8.74$ | $0.48\%$ | **PASS** |

---

### Mapeo Biunívoco de Reutilización de Casos

| Requisito Docente | Descripción del Ensayo | Casos Comparados | Variable Independiente | Variables Constantes | Conclusión Física Principal |
|:---|:---|:---:|:---:|:---:|:---|
| **EXP-06** | Sobretensión y diodo co-pack en serie 50 A | **F01 vs F02** | Presencia de diodo co-pack antiparalelo | $I_C = 50\text{ A}$, $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$ | En switch low-side, el diodo co-pack está en polarización inversa; no conduce en directa y su capacitancia ($0.45\text{ nF}$) tiene impacto despreciable en $V_{CE,\text{peak}}$ y $E_{\text{off}}$. |
| **EXP-07** | Sobretensión y diodo co-pack en serie 75 A | **F03 vs F04** | Presencia de diodo co-pack antiparalelo | $I_C = 75\text{ A}$, $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$ | Se comprueba la misma independencia en 75 A: el diodo co-pack no altera las pérdidas de corte del propio transistor. |
| **EXP-08 (A)** | Comparación a corriente igualada (50 A vs 75 A) | **F01 vs F05** | Tamaño de chip (50 A vs 75 A) | $I_C = 50\text{ A}$, $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$ | Mayor área reduce $V_{CE(\text{on})}$ en $-181\text{ mV}$ ($-13.3\%$), pero mayores capacitancias ($C_{ies}, C_{res}$) aumentan $E_{\text{off}}$ en $+28.2\%$ y reducen $di/dt$ ($V_{CE,\text{peak}}$ baja $6.0\text{ V}$). |
| **EXP-08 (B)** | Escalamiento de área a corriente nominal | **F01 vs F03** | Régimen nominal de chip ($50\text{ A}$ vs $75\text{ A}$) | $100\%$ de carga de diseño, $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$ | Caída en conducción similar ($1.362\text{ V}$ vs $1.356\text{ V}$); $E_{\text{off}}$ casi se duplica ($+92.4\%$) y mayor $di/dt$ eleva $V_{CE,\text{peak}}$ a $445.98\text{ V}$. |
| **EXP-09** | Sensibilidad a la resistencia de compuerta $R_G$ | **F02 vs F06** | Resistencia de compuerta ($10\ \Omega \to 20\ \Omega$) | $I_C = 50\text{ A}$, Chip 50A Co-Pack, $L_\sigma = 25\text{ nH}$ | Trade-off clásico: Duplicar $R_G$ reduce la sobretensión inducida de $+42.36\text{ V}$ a $+25.94\text{ V}$ ($-38.8\%$), a costa de elevar $E_{\text{off}}$ en $+70.5\%$ ($1067\ \mu\text{J} \to 1819\ \mu\text{J}$). |

---

### Evidencias Gráficas Asociadas (300 DPI)
* **EXP-06:** [`figuras/fig6_sobretension_copack_50a.png`](../figuras/fig6_sobretension_copack_50a.png)
* **EXP-07:** [`figuras/fig7_sobretension_copack_75a.png`](../figuras/fig7_sobretension_copack_75a.png)
* **EXP-08:** [`figuras/fig8_comparativa_area_50vs75.png`](../figuras/fig8_comparativa_area_50vs75.png)
* **EXP-09:** [`figuras/fig9_sensibilidad_rg_conmutacion.png`](../figuras/fig9_sensibilidad_rg_conmutacion.png)
