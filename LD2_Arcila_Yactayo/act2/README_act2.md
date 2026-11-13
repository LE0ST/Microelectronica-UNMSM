# Activity 2: Charge Sharing in Footed Dynamic NAND3

**Technical and Quantitative Results Documentation**  
**Authors:** Leonardo Sait Yactayo Tolentino (`23190214`) & Marco Antonio Arcila Santander (`23190140`)  
**Course:** Microelectronics and Nanoelectronic Systems — FIEE UNMSM (2026-II)  
**Technology:** PTM 45 nm HP Metal Gate / High-κ / Strained-Si ($V_{DD} = 1.0\text{ V}$, $T = 27\ ^\circ\text{C}$)  
**Date:** September 17, 2026

---

## 1. Introduction and Physical Fundamentals

In the footed dynamic CMOS NAND3 gate with a domino output inverter, the series pull-down network (PDN) contains three internal intermediate nodes: $n_1$ (between $M_1$ and $M_2$), $n_2$ (between $M_2$ and $M_3$), and $n_3$ (between $M_3$ and footer $M_f$).

When a prior evaluation cycle activates all inputs ($A=B=C=1$), all internal nodes discharge completely to $0\text{ V}$. If in the next cycle the gate evaluates a worst-case input pattern where the PDN must remain open to ground while upper transistors conduct ($A=1, B=1, C=0$):
1. Precharge transistor $M_p$ turns off ($CLK = 1$), leaving dynamic node `dyn` **floating** at $V_{DD}$.
2. Transistor $M_3$ remains off ($C=0$), keeping the path to ground through $M_f$ open.
3. Upper transistors $M_1$ ($A=1$) and $M_2$ ($B=1$) turn on, connecting the charged dynamic node to the parasitic diffusion capacitances of $n_1$ and $n_2$.
4. Electrostatic charge stored on $C_{dyn}$ redistributes into $C_{n1}$ and $C_{n2}$, causing a transient voltage drop $\Delta V$ at the dynamic node.

---

## 2. Diffusion Geometry and Capacitance Calculation

Following Sections 6.2 and 6.3 of the Official Guide, diffusion geometries are modeled explicitly with:
* $L_{diff} = 90\text{ nm}$
* $W_{PDN} = 3 \times W_n = 3 \times 90\text{ nm} = 270\text{ nm}$
* Diffusion area: $Ad = W \times L_{diff} = 270\text{ nm} \times 90\text{ nm} = 0.0243\ \mu\text{m}^2 = 2.430 \times 10^{-14}\text{ m}^2$
* Diffusion perimeter: $Pd = W + 2 L_{diff} = 270\text{ nm} + 180\text{ nm} = 450\text{ nm} = 4.500 \times 10^{-7}\text{ m}$

### Parameters Extracted from `ptm45hp.lib` (local dependency):
* $c_j = c_{js} = c_{jd} = 0.0005\text{ F/m}^2 = 0.500\text{ fF}/\mu\text{m}^2$ ($PB=1\text{ V}$, $MJ=0.50$)
* $c_{jsw} = c_{jsws} = c_{jswd} = 5.00 \times 10^{-10}\text{ F/m} = 0.500\text{ fF}/\mu\text{m}$ ($PBSW=1\text{ V}$, $MJSW=0.33$)

### Capacitance Components per Diffusion Contact ($C_{diff,1}$):
* Bottom-plate: $C_{bottom} = c_j \times Ad = 0.01215\text{ fF}$ ($5.1\%$)
* Sidewall: $C_{sidewall} = c_{jsw} \times Pd = 0.22500\text{ fF}$ ($94.9\%$)
* Total per contact: $C_{diff,1} = 0.23715\text{ fF}$

### Internal and Dynamic Node Capacitances:
* Node $n_1$ (2 contacts: $M_1$ and $M_2$): $C_{n1} = 2 \times 0.23715 = 0.4743\text{ fF}$
* Node $n_2$ (2 contacts: $M_2$ and $M_3$): $C_{n2} = 2 \times 0.23715 = 0.4743\text{ fF}$
* **Aggregate internal capacitance:** $C_a \equiv C_{n1} + C_{n2} = 0.9486\text{ fF}$
* Fixed parasitic capacitance on `dyn`:
  * PMOS overlap: $C_{gd}(M_p) = cgdo \times W_p = 0.0149\text{ fF}$
  * Domino inverter input: $C_g(\text{inverter}) = 0.3292\text{ fF}$
  * $M_1$ diffusion on `dyn`: $C_{diff,M1} = 0.2372\text{ fF}$
  * Total parasitics on `dyn`: $C_{par,dyn} = 0.5812\text{ fF}$ (or $0.3441\text{ fF}$ excluding $M_1$ diffusion per the guide's abbreviated formula).

---

## 3. Physical Discrepancy: Pure Charge Sharing vs. Pass-Transistor Subthreshold Cutoff

The standard ideal charge-sharing equation assumes ideal switches without threshold drop:
$$\Delta V_{pred} = V_{DD} \cdot \frac{C_a}{C_a + C_{dyn}}$$

However, in SPICE simulation with BSIM4 models, the actual drop is significantly smaller ($\approx 2.5\times$ to $3\times$ lower than the theoretical prediction):

1. **Subthreshold Cutoff of $M_2$:**  
   Transistor $M_2$ acts as a pass transistor with its gate at $V_B = 1.0\text{ V}$. As charge flows into $n_2$, $V(n_2)$ rises. Since the body is at $0\text{ V}$, the source experiences body effect ($V_{SB2} = V_{n2} > 0$). Using first-order estimation with $k_1 = 0.4\text{ V}^{1/2}$ ($k_2 = 0$) and $2\phi_F \approx 0.8\text{ V}$ at $V_{SB2} \approx 0.5\text{ V} - 0.66\text{ V}$, $\Delta V_{th} \approx k_1 (\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F}) \approx 0.4(\sqrt{1.3} - \sqrt{0.8}) \approx 0.10\text{ V}$, placing the effective threshold in an approximate reference range of $V_{th,eff} \approx 0.55\text{ V} - 0.60\text{ V}$ (vs. zero-bias $V_{th0} = 0.469\text{ V}$). Note that this is an approximate analytical reference rather than a direct LTspice operating-point extraction, as BSIM4 also includes DIBL (`eta0`), channel-length modulation, and narrow-width effects.  
   When $V(n_2)$ reaches $\approx 0.66\text{ V}$ in simulation, $V_{GS2} = 1.0 - 0.66 = 0.34\text{ V} \ll V_{th,eff}$, pushing $M_2$ into **subthreshold cutoff**, where channel resistance jumps to tens of megaohms and halts charge flow into $C_{n2}$ within the $1\text{ ns}$ evaluation window.
2. **Nonlinear Junction Capacitance:**  
   As $n_1$ and $n_2$ charge up, reverse bias $V_R$ across the p-n junctions increases, reducing effective diffusion capacitance relative to zero bias ($C_j(V_R) = C_{j0} / (1 + V_R/PB)^M$).

---

## 4. Parametric Load Sweep $C_L$ and Noise Margins

The load sweep $C_L \in [0.5, 1.0, 2.0, 4.0]\text{ fF}$ contrasts analytical models against the **Canonical Synchronous Reference Bench** ([`circuitos/nand3_cs_g2b_piloto_cl2f.cir`](circuitos/nand3_cs_g2b_piloto_cl2f.cir) and [`circuitos/nand3_cs_g2b_barrido_cl.cir`](circuitos/nand3_cs_g2b_barrido_cl.cir)) and historical series (domino inverter thresholds: $V_M = 0.4797\text{ V}$, $V_{IH} = 0.5785\text{ V}$, $NM_H = 0.4215\text{ V}$, $\Delta V_{crit,M} = 0.5203\text{ V}$):

| $C_L$ (fF) | $\Delta V_{pred}$ (Guide) | $\Delta V_{pred}$ (Total) | $\Delta V_{\text{sync}}$ (Sync Ref.) | $V_{dyn,min}$ (Sync) | $\Delta V_{\text{Leo}}$ (Hist.) | $\Delta V_{\text{Marco}}$ (Hist.) | Logic Margin ($V_{IH}=0.579\,\text{V}$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.5** | 529.15 mV | 467.34 mV | **364.85 mV** | **0.6351 V** | 175.92 mV | --- | Safe ($V_{dyn} > V_{IH} + 56\,\text{mV}$) |
| **1.0** | 413.75 mV | 374.97 mV | **265.93 mV** | **0.7341 V** | 138.26 mV | --- | Safe ($V_{dyn} > V_{IH} + 155\,\text{mV}$) |
| **2.0** | 288.09 mV | 268.74 mV | **164.29 mV** | **0.8357 V** | 101.03 mV | 176.57 mV | Safe ($V_{dyn} > V_{IH} + 257\,\text{mV}$) |
| **4.0** | 179.23 mV | 171.54 mV | **92.60 mV** | **0.9074 V** | 67.62 mV | --- | Safe ($V_{dyn} > V_{IH} + 328\,\text{mV}$) |

### Physical Diagnosis and Historical Traceability:
* **Full logic immunity:** No spurious switching occurs at the domino output across the synchronous bench ($V_{out,max} \le 15.6\text{ mV} \ll V_{IL} = 0.3675\text{ V}$).
* **Subthreshold protection:** Under the ideal formula without threshold cutoff, at $C_L = 0.5\text{ fF}$ the predicted drop ($\Delta V_{pred} = 529.2\text{ mV}$) would push $V(dyn)$ to $0.4708\text{ V} < V_M$, causing a false logic failure. Intrinsic subthreshold cutoff of $M_2$ preserves circuit integrity.
* **Traceability:** The preliminary historical result ($101.03\text{ mV}$ nominal at $C_L=2\text{ fF}$) originates from [`circuitos/nand3_cs_peor_caso_fisico.cir`](circuitos/nand3_cs_peor_caso_fisico.cir) and [`circuitos/nand3_cs_barrido_cl.cir`](circuitos/nand3_cs_barrido_cl.cir) (`dv_eval_max: 0.101034 V`), where inputs $A$ and $B$ switched early ($[2.98, 3.00]\text{ ns}$, overlapping $20\text{ ps}$ with active precharge $CLK=0$). Removing this precharge-assisted overlap in the canonical synchronous bench ($[3.00, 3.02]\text{ ns}$) accounts for the $+63.26\text{ mV}$ increase to $164.29\text{ mV}$. The residual $12.28\text{ mV}$ difference vs. the alternative historical run ($176.5718\text{ mV}$ at $t=2.90\text{ ns}$, $C_L=2\text{ fF}$) coexists with documented differences in prior node bias on $n_2$ ($-160.8\text{ mV}$ vs. $-126.8\text{ mV}$) and measurement instants ($t=2.90\text{ ns}$, i.e., $900\text{ ps}$ into evaluation, vs. the synchronous-window minimum), with both confirming the subthreshold-limited regime.

---

## 5. Quantitative Evaluation of Mitigation Techniques

Mitigations were characterized under the nominal synchronous bench ($C_L = 2.0\text{ fF}$, $T_{clk} = 2\text{ ns}$, PTM 45 nm HP). Active-area baselines: dynamic core $W_{\text{dyn,base}} = 1215\text{ nm}$ ($A=0.0547\,\mu\text{m}^2$), full cell $W_{\text{cell,base}} = 1440\text{ nm}$ ($A=0.0648\,\mu\text{m}^2$).

| Configuration | Description | $\Delta V_{eval}$ / Peak | $V_{dyn,min}$ | $V_{out,max}$ | Recovery Time ($t_{rec}$) | Extra Active Area | Clock Load Overhead |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Synchronous Base (No Mitigation)** | Sync Ref. | **164.29 mV** | 0.8357 V | 0.134 mV | No recovery in eval. | Base (5 dyn / 7 cell) | Base ($C_g \approx 0.50\,\text{fF}$) |
| **Mitigation 1a: Precharge $W=45\,$nm** | Internal Precharge | **$-50.47\,$mV** (overshoot) | 1.0505 V | 0.267 mV | Immediate | +2 PMOS (+7.4% dyn) | $+0.1274\,$fF ($63.7\,$nW) |
| **Mitigation 1b: Precharge $W=135\,$nm**| Internal Precharge | **$-50.47\,$mV** (overshoot) | 1.0505 V | 0.267 mV | Immediate | +2 PMOS (+22.2% dyn) | $+0.3821\,$fF ($191.1\,$nW) |
| **Mitigation 2: Reordering C-B-A** | Input Reordering | Vec A: $\le 0\,$ / Vec B: **164.3 mV** | 0.8357 V | 0.134 mV | Vector-dependent | **0 transistors** (0 nm) | **0 fF** (identical to base) |
| **Mitigation 2: Reordering C-A-B** | Input Reordering | Vec A: $\le 0\,$ / Vec B: **72.1 mV** | 0.9279 V | 0.134 mV | Vector-dependent | **0 transistors** (0 nm) | **0 fF** (identical to base) |
| **Mitigation 3: Keeper $W_{kp} = 45\,$nm** | PMOS Keeper | **69.68 mV** (initial droop) | 0.9303 V | 0.356 mV | **92.92 ps** (from min) | +1 PMOS (+3.7% dyn) | 0 fF on $CLK$ |

### Detailed Physical Analysis:
1. **Internal Precharge ($W_p = 45\text{ nm}$ vs. $135\text{ nm}$):**
   * Both widths eliminate static droop ($V_{dyn,min} = 1.0505\text{ V}$) within the $1\text{ ns}$ precharge window ($1\text{ ns} \gg 5\tau$).
   * Minimum width ($45\text{ nm}$) cuts clock gate capacitive overhead by $66.7\%$ ($0.1274\text{ fF}$ vs. $0.3821\text{ fF}$) and associated dynamic power ($63.69\text{ nW}$ vs. $191.07\text{ nW}$ at $500\text{ MHz}$).
   * Both introduce $+50.47\text{ mV}$ clock-feedthrough overshoot. Node $n_3$ is not precharged because footer turn-on in evaluation would dump $C_{n3} V_{DD}^2 f$ directly to ground without logic benefit.
2. **PDN Input Reordering:**
   * Under Vector A ($A=B=1, C=0$), placing $C=0$ at the top transistor (adjacent to `dyn`) isolates internal nodes and eliminates droop.
   * Under Vector B ($A=0, B=C=1$), topology C-B-A still exposes two discharged internal nodes to `dyn` ($164.29\text{ mV}$ droop), whereas C-A-B limits droop to $72.08\text{ mV}$ by placing $A=0$ in the middle (preliminary early-switching runs yielded $100.37\text{ mV}$ and $31.26\text{ mV}$). Thus, reordering is **not universal** and introduces layout routing trade-offs.
3. **PMOS Keeper ($W_{kp} = 45\text{ nm}$) and Dynamic Contention Trade-off:**
   * Adds a single PMOS ($\Delta W = +45\text{ nm}$, $+3.70\%$ dynamic active area), limiting initial droop to $69.68\text{ mV}$ ($V_{dyn,min} = 0.9303\text{ V}$ at $t=3.0271\text{ ns}$), restoring `dyn` to $99\%$ of $V_{DD}$ in $92.92\text{ ps}$ after the minimum ($110.02\text{ ps}$ from the $0.50\text{ V}$ clock crossing; $120.02\text{ ps}$ from clock ramp start), and reaching $0.9996\text{ V}$ ($99.96\%$) by phase end.
   * **Contention penalty (50% delay points):**
     * $t_{pHL,dyn}$: increases from $23.95\text{ ps}$ to $27.46\text{ ps}$ ($\Delta t = +3.51\text{ ps}$, **$+14.65\%$**).
     * $t_{pLH,out}$: increases from $37.58\text{ ps}$ to $43.09\text{ ps}$ ($\Delta t = +5.52\text{ ps}$, **$+14.69\%$**).

---

## 6. Generated Figures (300 DPI)

* [`figuras/fig1_act2_peor_caso_formas_onda.png`](figuras/fig1_act2_peor_caso_formas_onda.png): Synchronized worst-case waveforms (control, internal nodes, dynamic node, and output).
* [`figuras/fig2_act2_dv_vs_cl_analitico_simulado.png`](figuras/fig2_act2_dv_vs_cl_analitico_simulado.png): Parametric $\Delta V \text{ vs } C_L$ and $V_{dyn,min} \text{ vs } C_L$ curves showing analytical/simulated divergence and safe logic region.
* [`figuras/fig3_act2_comparacion_mitigaciones.png`](figuras/fig3_act2_comparacion_mitigaciones.png): Transient comparison of the three mitigations and speed contention trade-off.
