# Activity 4 — Monotonicity, Domino Cascade, and Clock Skew

**Course:** Microelectronics and Nanoelectronic Systems (Semester 2026-II)  
**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — Faculty of Electrical and Electronic Engineering (FIEE)  
**Authors:** Leonardo Sait Yactayo Tolentino (`23190214`) & Marco Antonio Arcila Santander (`23190140`)  
**Base Technology:** PTM 45 nm High-Performance (HP), $V_{DD} = 1.0\,\text{V}$, $T = 27^\circ\text{C}$  
**Official Guide:** `Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf` (Section 8, pp. 8–10; local teaching document excluded from public repository)

---

## 1. Provenance Separation (Published Controls vs. External Historical Runs)

To maintain strict traceability in the public repository:
* **Published in this repository (`act4/`):**
  * Netlists: [`circuitos/a4_control1_bloqueo_inversor.cir`](circuitos/a4_control1_bloqueo_inversor.cir), [`circuitos/a4_control2_pulso_x_descendente.cir`](circuitos/a4_control2_pulso_x_descendente.cir), [`circuitos/a4_control3_x_estatico_cero.cir`](circuitos/a4_control3_x_estatico_cero.cir), [`circuitos/a4_control4_difusion_sensibilidad.cir`](circuitos/a4_control4_difusion_sensibilidad.cir).
  * Consolidated metrics & figures: [`resultados/datos/act4_metricas.json`](resultados/datos/act4_metricas.json), [`scripts/generar_figuras_act4.py`](scripts/generar_figuras_act4.py), and `figuras/fig1..fig3*.png`.
* **External historical runs (`laboratorio4/`, outside this repository):**
  * `Tarea 1 Sin Inversor.cir`/`.log`, `Paso 2 y 3 Con Inversor.cir`/`.log`, `Tarea 4 Footed.cir`/`.log`, and `Paso 5 Unfooted.cir`/`.log`. Metrics from these runs are preserved below as historical primary evidence and are **not** attributed to the published `a4_control*` netlists.

---

## 2. Objectives and Requirements Matrix

| Req. ID | LD2 Guide Task | Technical Statement | Published Netlists (`act4/circuitos/`) | External Historical Netlists | Status |
|:---:|:---:|:---|:---|:---|:---:|
| **REQ-19** | §8.1 (Tasks 1–2) | Demonstrate monotonicity violation in direct cascade $dyn1 \to \text{PDN2}$ and premature firing prevention via static domino inverter. | [`a4_control1_bloqueo_inversor.cir`](circuitos/a4_control1_bloqueo_inversor.cir) | `Tarea 1 Sin Inversor.cir`<br>`Paso 2 y 3 Con Inversor.cir` | **COMPLETE** |
| **REQ-20** | §8.1 (Task 3) | Evaluate external input $X$ with falling transition ($1 \to 0$) during active evaluation; characterize evaluation-cycle logic error and interface flip-flop (TGFF) implications. | [`a4_control2_pulso_x_descendente.cir`](circuitos/a4_control2_pulso_x_descendente.cir)<br>[`a4_control3_x_estatico_cero.cir`](circuitos/a4_control3_x_estatico_cero.cir) | — | **COMPLETE** |
| **REQ-21** | §8.2 (Tasks 1–3) | Characterize 3-stage Footed vs. Unfooted domino cascade under $T_{\text{skew}} \in [-50, 200]\,\text{ps}$; quantify $t_{\text{del}}$, peak current $I_{\text{pk}}$, and Rabaey's timing condition. | [`a4_control4_difusion_sensibilidad.cir`](circuitos/a4_control4_difusion_sensibilidad.cir) | `Tarea 4 Footed.cir`<br>`Paso 5 Unfooted.cir` | **COMPLETE** |

---

## 3. Section 8.1: Monotonicity Rule and Domino Structure

### A. Direct Cascade Without Inverter (Monotonicity Violation — Historical Run)
* **External Historical Netlist:** `laboratorio4/Tarea 1 Sin Inversor.cir` (outside repository).
* **Stimuli:** $V_a = 1.0\,\text{V}$, $V_b = 1.0\,\text{V}$, $V_x = 1.0\,\text{V}$, $T_{clk} = 2.0\,\text{ns}$ ($500\,\text{MHz}$).
* **Historical LOG Result:**  
  $$\mathbf{V_{dyn2,\text{min}} = 0.64624\,\text{V}} \implies \Delta V = 1.00000 - 0.64624 = \mathbf{353.76\,\text{mV}}$$
* **Physical Diagnosis:**  
  Stage 1 has $A=B=1$, so its final evaluation state is $dyn1 \to 0$. Stage 2 computes $dyn2 = \overline{dyn1 \cdot X} = \overline{0 \cdot 1} = 1$. However, during precharge ($CLK=0$), $dyn1$ charged to $V_{DD} = 1.0\,\text{V}$. At the evaluation edge ($CLK: 0 \to 1$), $dyn1$ takes a finite $t_{pHL1}$ to discharge, creating a transient conduction path in PDN2 that drains $353.76\,\text{mV}$ from $dyn2$. Once $dyn1 < V_{thn}$, PDN2 cuts off, but with $M_{p2}$ off during evaluation, the lost charge **cannot be recovered within that cycle**.
* **Noise Margin Impact:**  
  With $V_M = 0.4797\,\text{V}$ and $V_{IH} = 0.5785\,\text{V}$, the high-level noise margin drops to $NM_H = 0.6462 - 0.5785 = \mathbf{67.7\,\text{mV}}$ (**$84\%$** loss relative to nominal $421.5\,\text{mV}$; the $353.76\,\text{mV}$ droop leaves $dyn2$ at $0.6462\,\text{V}$). While $0.6462\,\text{V} > V_M$ prevents output inversion in an ideal isolated cell, it leaves the gate near functional collapse under supply or thermal noise.

### B. Premature Firing Prevention and Blocking with Static Domino Inverter
Three operating regimes are distinguished:
1. **Premature Activation Prevention:** Inserting the static inverter ($out1 = \overline{dyn1}$) fixes $out1 = 0\,\text{V}$ during precharge ($dyn1=1$), guaranteeing a strictly **monotonic rising ($0 \to 1$)** transition during evaluation and keeping PDN2 off while $dyn1$ discharges.
2. **Legitimate Functional Discharge (External Historical Run with $X=1$):** In `Paso 2 y 3 Con Inversor.cir` ($A=B=X=1$), the domino gate evaluates $out2 = out1 \cdot X = 1$, requiring $dyn2 \to 0\,\text{V}$. Historical LOG: $V_{dyn2,\text{min}} = \mathbf{-0.00584\,\text{V}} \approx 0.00\,\text{V}$ (expected active switching, not a failure).
3. **Correct Blocking with $X=0$ (Published Control 1):**  
   In [`circuitos/a4_control1_bloqueo_inversor.cir`](circuitos/a4_control1_bloqueo_inversor.cir), $A=B=1$ ($out1 \to 1$) and $X=0$ yield $out2 = 1 \cdot 0 = 0$, requiring $dyn2$ to remain high:
   * $V(dyn1)$ at end of evaluation ($t=2.99\,\text{ns}$): $3.65\,\mu\text{V} \approx 0.00\,\text{V}$.
   * $V(out1)$ at $t=2.99\,\text{ns}$: $0.999999\,\text{V} \approx 1.00\,\text{V}$.
   * $V(dyn2)$ at $t=2.99\,\text{ns}$: $1.03894\,\text{V}$ (intact high state, with clock overshoot).
   * $V(out2)$ at $t=2.99\,\text{ns}$: $26.8\,\text{nV} \approx 0.00\,\text{V}$.
   * **Absolute minimum of $V(dyn2)$ in evaluation:** $\mathbf{0.999999\,\text{V}}$ ($\Delta V = 0.77\,\mu\text{V} \approx \mathbf{0.000\,\text{mV}}$).

> **Methodological Clarification:** Control 1 demonstrates proper blocking with $X=0$; it must not be presented as a "quantitative $100\%$ reduction of the $353\,\text{mV}$ drop by direct comparison", because the uninverted circuit ran with $X=1$ and opposite inputs, whereas Control 1 runs with $X=0$.

### C. Logic Error from Non-Monotonic External Input $X$ (Published Controls 2 & 3)
* **Published Netlists:**  
  - Control 2: [`circuitos/a4_control2_pulso_x_descendente.cir`](circuitos/a4_control2_pulso_x_descendente.cir) ($X: 1 \to 0$ mid-evaluation at $t = 2.50\,\text{ns}$).
  - Control 3: [`circuitos/a4_control3_x_estatico_cero.cir`](circuitos/a4_control3_x_estatico_cero.cir) (static $X = 0$ reference).

| Variable / Parameter | Control 3 (Static $X=0$) | Control 2 ($X: 1 \to 0$ at $t=2.50\,\text{ns}$) | Physical Behavior Demonstrated |
|:---|:---:|:---:|:---|
| $V(clk)$ at $t=2.50\,\text{ns}$ | $1.000\,\text{V}$ | $1.000\,\text{V}$ | Active evaluation phase ($CLK=1$) |
| $V(x)$ before $2.50\,\text{ns}$ | $0.000\,\text{V}$ | $1.000\,\text{V}$ | In Control 2, $X=1$ enabled PDN2 initially |
| $V(x)$ final ($t=2.99\,\text{ns}$) | $0.000\,\text{V}$ | $0.000\,\text{V}$ | Both end with input vector $(out1=1, X=0)$ |
| $V(dyn2)$ before ($t=2.49\,\text{ns}$) | $\mathbf{1.0410\,\text{V}}$ | $\mathbf{3.66\,\mu\text{V}}$ | Discharge in Control 2 occurred BEFORE $X$ fell |
| $V(dyn2)$ final ($t=2.99\,\text{ns}$) | $\mathbf{1.0389\,\text{V}}$ | $\mathbf{-0.0265\,\text{V}}$ | Inability to recharge in evaluation ($M_{p2}$ off) |
| $V(out2)$ final ($t=2.99\,\text{ns}$) | $\mathbf{26.8\,\text{nV} \approx 0.0\,\text{V}}$ | $\mathbf{0.999997\,\text{V} \approx 1.0\,\text{V}}$ | **Evaluation-cycle logic error** |
| Expected $dyn2, out2$ | $dyn2=1,\; out2=0$ | $dyn2=1,\; out2=0$ | For $out1=1, X=0$: $out2 = 1 \cdot 0 = 0$ |
| Observed $dyn2, out2$ | $dyn2=1,\; out2=0$ (PASS) | $dyn2 \approx 0,\; out2 \approx 1$ (**ERROR**) | Erroneous complementary output during cycle |

* **Causal sequence:** Between $t=2.00\,\text{ns}$ and $t=2.50\,\text{ns}$ ($CLK=1$, $out1=1$, $X=1$) PDN2 conducts and drains $dyn2$ to ground in under $60\,\text{ps}$; at $t=2.50\,\text{ns}$, $X$ falls to $0\,\text{V}$, but $M_{p2}$ is off during evaluation, so no path to $V_{DD}$ restores $dyn2$ and $out2$ stays near $1.0\,\text{V}$ against the required $out2 = 1 \cdot 0 = 0$.
* **Terminology:** This is an evaluation-cycle logic error of the second stage, not a memory "bit flip" and not a permanent failure; the next precharge half-cycle ($CLK=0$) restores $dyn2$ to $V_{DD}$.
* **Implications for Interface Flip-Flops:** External inputs to domino logic must come from glitch-free storage elements (e.g., transmission-gate flip-flops, TGFF) whose outputs remain strictly monotonic rising or stable throughout evaluation. This is an evaluation-cycle logic error (not a permanent latch/memory bit flip), as precharge ($CLK=0$) restores $dyn2$ on the next half-cycle.

---

## 4. Section 8.2: 3-Stage Domino Cascade (Footed vs. Unfooted — Historical Skew Sweep)

### A. Skew Matrix ($T_{\text{skew}} \in [-50, 200]\,\text{ps}$)
Data extracted from external historical logs (`laboratorio4/Tarea 4 Footed.log` and `laboratorio4/Paso 5 Unfooted.log`, outside this repository; summarized in [`resultados/datos/act4_metricas.json`](resultados/datos/act4_metricas.json)):

| $T_{\text{skew}}$ (ps) | Footed Delay ($t_{\text{del}}$) | Unfooted Delay ($t_{\text{del}}$) | Delay Savings ($\Delta t$) | $I_{\text{pk}}$ Footed ($\mu\text{A}$) | $I_{\text{pk}}$ Unfooted ($\mu\text{A}$) | $\Delta I_{\text{pk}}$ Unfooted | Dominant Dynamic Behavior |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **$-50$** | $77.20\,\text{ps}$ | $66.46\,\text{ps}$ | $-10.74\,\text{ps}$ ($-13.9\%$) | $113.80$ | $326.30$ | $+212.50\,\mu\text{A}$ | Early precharge in downstream stages overlaps high inputs. |
| **$0$** | $77.21\,\text{ps}$ | $66.47\,\text{ps}$ | $-10.74\,\text{ps}$ ($-13.9\%$) | $318.85$ | $332.91$ | $+14.06\,\mu\text{A}$ | Synchronous switching: all 3 stages precharge in parallel. |
| **$+50$** | $125.47\,\text{ps}$ | $95.12\,\text{ps}$ | $-30.35\,\text{ps}$ ($-24.2\%$) | $110.56$ | $110.57$ | $+0.01\,\mu\text{A}$ | Temporal decoupling of precharge peaks; equal peak currents. |
| **$+100$** | $226.68\,\text{ps}$ | $130.81\,\text{ps}$ | $-95.87\,\text{ps}$ ($-42.3\%$) | $110.56$ | $160.57$ | $+50.01\,\mu\text{A}$ | Onset of supply current spike in unfooted stage. |
| **$+200$** | $426.91\,\text{ps}$ | $171.48\,\text{ps}$ | $-255.43\,\text{ps}$ ($-59.8\%$) | $110.56$ | $214.63$ | $+104.07\,\mu\text{A}$ | Significant supply peak rise in unfooted ($+94.1\%$ over footed). |

### B. Physical Analysis of $I_{\text{pk}}$ and Rabaey's Timing Condition
* $I_{\text{pk}}$ was measured via `.meas TRAN Ipk MAX -I(Vdd) FROM={Tbase} TO={Tbase+Tclk*2}` over $t \in [0.5, 4.5]\,\text{ns}$, representing total instantaneous supply peak current (capacitive charging, leakage, and overlap conduction).
* $\Delta I_{\text{pk}}(+200\,\text{ps}) = 214.63\,\mu\text{A} - 110.56\,\mu\text{A} = \mathbf{104.07\,\mu\text{A}}$ is a **difference of supply-current peaks** between topologies, not an isolated short-circuit current; $I_{\text{sc,footed}}=0$ is not claimed because internal branches are not isolated. At $T_{\text{skew}}=-50\,\text{ps}$ unfooted peaks at $326.30\,\mu\text{A}$ vs. $113.80\,\mu\text{A}$ footed; at $+100$ and $+200\,\text{ps}$ unfooted reaches $160.57$ and $214.63\,\mu\text{A}$. $I_{\text{pk}}$ is an instantaneous peak and does not represent average energy without integrating $\int -I(V_{DD})\,V_{DD}\,dt$.
* Rabaey's condition: footer omission is admissible if the precharge propagation delay of the previous stage extinguishes PDN conduction before excessive overlap dissipation occurs.
* Because the historical netlists measured only end-to-end $t_{\text{del}}$ and global $I_{\text{pk}}$ without per-stage delays ($t_{p,\text{inv}}, t_{pHL,\text{dyn}}$), **$T_{\text{skew,max}} = 50\,\text{ps}$ is not claimed as an exact experimental boundary**; rather, the data show low $I_{\text{pk}}$ at $+50\,\text{ps}$ ($110.57\,\mu\text{A}$) and rising overlap conduction at $+100\,\text{ps}$, $+200\,\text{ps}$, and $-50\,\text{ps}$ ($326.30\,\mu\text{A}$).

---

## 5. Diffusion Parameter Sensitivity (Published Control 4)

Common settings: $W_n=90\,\text{nm}$, $W_p=135\,\text{nm}$, $W_{\text{PDN}}=180\,\text{nm}$, $L_n=45\,\text{nm}$; $V_{DD}=1.0\,\text{V}$, $T_{clk}=2.0\,\text{ns}$, $t_r=t_f=20\,\text{ps}$, $T_{\text{skew}}=0$; solver `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`; delay = TRIG $V(clk1)=0.5$ RISE=2 to TARG $V(out3)=0.5$ RISE=2; $I_{\text{pk}}$ window `FROM 5e-10 TO 4.5e-09`. Line-by-line audit comparing external historical `Tarea 4 Footed.cir` (no explicit diffusion parameters) vs. published [`circuitos/a4_control4_difusion_sensibilidad.cir`](circuitos/a4_control4_difusion_sensibilidad.cir) (explicit $AS, AD, PS, PD$ with $L_{\text{diff}}=90\,\text{nm}$, identical topology, $W/L$, $C_1=C_2=C_3=2.0\,\text{fF}$, $27^\circ\text{C}$, Gear solver):
* End-to-end delay without explicit diffusion (historical): $t_{\text{del}} = \mathbf{77.21\,\text{ps}}$ ($I_{\text{pk}} = 318.85\,\mu\text{A}$).
* End-to-end delay with explicit diffusion (Control 4): $t_{\text{del}} = \mathbf{89.90\,\text{ps}}$ ($\Delta t = \mathbf{+12.69\,\text{ps}}$, **$+16.43\%$**; $I_{\text{pk}} = 312.66\,\mu\text{A}$ vs. $318.85\,\mu\text{A}$ without explicit diffusion, an increase of $\approx +1.98\%$ from $312.66\,\mu\text{A}$ to $318.85\,\mu\text{A}$, $< 2\%$ variation). The $16.4\%$ increase quantifies the global junction-parasitic impact; an exact $4.23\,\text{ps}$-per-stage increase is **not** claimed (no per-node measurements), and the result is not extrapolated to unfooted skew tolerance.

---

## 6. Published File Inventory (`act4/`)

* **Netlists:** `circuitos/a4_control1_bloqueo_inversor.cir`, `a4_control2_pulso_x_descendente.cir`, `a4_control3_x_estatico_cero.cir`, `a4_control4_difusion_sensibilidad.cir`.
* **Data & Scripts:** [`resultados/datos/act4_metricas.json`](resultados/datos/act4_metricas.json), [`scripts/generar_figuras_act4.py`](scripts/generar_figuras_act4.py).
* **Figures (300 DPI):** [`figuras/fig1_act4_monotonicidad_cascada.png`](figuras/fig1_act4_monotonicidad_cascada.png), [`figuras/fig2_act4_pulso_x_descendente.png`](figuras/fig2_act4_pulso_x_descendente.png), [`figuras/fig3_act4_footed_vs_unfooted_skew.png`](figuras/fig3_act4_footed_vs_unfooted_skew.png).
