# Activity 1 — Footed Dynamic NAND3: Phases, Asymmetry, and Power Consumption

**Course:** Microelectronics and Nanoelectronic Systems (Semester 2026-II)  
**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Instructor:** MsC. Luz Adanaqué Infante  
**Authors:** Leonardo Sait Yactayo Tolentino (`23190214`) & Marco Antonio Arcila Santander (`23190140`)  
**Working Directory:** [`act1/`](.)  
**Primary Technology:** PTM 45 nm HP ($V_{DD} = 1.0\text{ V}$, $T = 27^\circ\text{C}$)

---

## 1. Circuit Topology and Sizing

### A. Footed Dynamic NAND3 with Domino Inverter (Official Guide, Sec. 5)
* **Pull-Down Network (PDN) and Footer ($M_f$):**
  * 4 series NMOS transistors ($M_1, M_2, M_3, M_f$) sized per the guide at $W = 3 W_n = 3 \times 90\text{ nm} = 270\text{ nm}$, $L = 45\text{ nm}$.
  * The equivalent pull-down resistance emulates the current of a unit reference NMOS ($W_n = 90\text{ nm}$).
* **Precharge Transistor ($M_p$):**
  * PMOS connected to $V_{DD}$ with $W = W_p = 135\text{ nm}$, $L = 45\text{ nm}$ ($\beta = 1.5$ for hole mobility compensation).
* **Output Domino Inverter:**
  * $M_{pi}$: PMOS with $W = W_p = 135\text{ nm}$, $L = 45\text{ nm}$.
  * $M_{ni}$: NMOS with $W = W_n = 90\text{ nm}$, $L = 45\text{ nm}$.
* **Capacitive Load Conditions (Guide Specification):**
  * External load at the dynamic node: $C_L = 2\text{ fF}$ (`.param CL=2f`).
  * Gate capacitance of the domino inverter connected to node `dyn` ($W_p = 135\text{ nm}, W_n = 90\text{ nm}$).
  * Domino output load: $C_{out} = 1\text{ fF}$ (`Cout out 0 1f`).
* **Transistor Count:**
  * Footed dynamic core alone: **5 transistors** (4 NMOS + 1 PMOS).
  * Complete domino stage (including restoring inverter): **7 transistors**.

### B. Equivalent Static CMOS NAND3
* **PUN:** 3 parallel PMOS transistors ($M_{Pa}, M_{Pb}, M_{Pc}$) with $W = W_p = 135\text{ nm}$, $L = 45\text{ nm}$.
* **PDN:** 3 series NMOS transistors ($M_{Na}, M_{Nb}, M_{Nc}$) with $W = 3 W_n = 270\text{ nm}$, $L = 45\text{ nm}$.
* **Output Load:** $C_{out} = 1\text{ fF}$.
* **Total Transistor Count:** 3 (PUN) + 3 (PDN) = **6 transistors**.

---

## 2. Official Comparative Table: Dynamic vs. Static (Task 3)

All numerical metrics were extracted from LTspice 26.0.2 simulations (`circuitos/*.cir`) and stored in `resultados/datos/`:

| Evaluated Metric | Dynamic NAND3 (Domino) | Equivalent Static NAND3 | Ratio (Dyn / Stat) | Notes / Provenance |
| :--- | :---: | :---: | :---: | :--- |
| **Transistor Count** | **5** (core) / **7** (total) | **6** | **0.833** / **1.167** | Official Guide Sec. 5 |
| **$t_{pHL}$ (Evaluation at node `dyn`)** | **22.17 ps** | **9.61 ps** | **2.307** | Official $t_{pHL,dyn}$ vs $t_{pHL,stat}$ (`ENS-A1-07`) |
| **$t_{pLH}$ (Precharge at node `dyn`)** | **25.13 ps** | **12.40 ps** | **2.027** | Official $t_{pLH,dyn}$ vs $t_{pLH,stat}$ (`ENS-A1-07`) |
| **Logic Output Delay (Asymmetric Triggers)** | **35.89 ps** (output `out` from $CLK\uparrow$) | **9.61 ps** (output `out_stat` from $A\uparrow$) | **3.734** | Both observed at logic output ($C_{out}=1\text{ fF}$); distinct trigger events ($CLK\uparrow$ vs $A\uparrow$, descriptive ratio) |
| **Control without external $C_L$ on `dyn` (`ENS-A1-08`)** | $t_{pHL,dyn}=11.26\text{ ps}$<br>$t_{pd,\text{eval}}=21.27\text{ ps}$ | — | — | Control with $C_L=0$; `dyn` retains diffusions, MOS capacitances, and inverter gate load |
| **Input Capacitance $C_{in}(A)$** | **0.3417 fF** | **0.5936 fF** | **0.5756** (-42.4%) | Integration $Q=\int I\,dt$ (`ENS-A1-HIG-01`; hist. 0.3415 fF in `ENS-A1-04`) |
| **$P_{\text{avg}}$ with $A$ switching ($T_A=8\text{ ns}$)** | **1.2393 $\mu$W** | **0.2692 $\mu$W** | **4.604** | Identical $125\text{ MHz}$ stimulus (`ENS-A1-07`) |
| *$P_{\text{avg}}$ Static with $A$ at 500 MHz (Historical)* | *1.2393 $\mu$W* | *0.8206 $\mu$W* | *1.510* | *Preliminary historical reference (`ENS-A1-02`)* |
| **$P_{\text{avg}}$ @ 500 MHz (Inputs fixed at 1)** | **2.7255 $\mu$W** | **1.7004 nW** | **1602.9** | Power trap: $\alpha=1$ vs $\alpha=0$ (`ENS-A1-03`) |

#### Methodological Clarifications on Delay Comparison:
1. **Asymmetric Trigger Events:**
   * In the **domino NAND3**, the measured delay is:
     $$\text{Evaluation delay from } CLK\uparrow \text{ to } OUT\uparrow = \mathbf{35.89\text{ ps}}$$
     (since input $A$ is already stabilized high during the precharge phase).
   * In the **static NAND3**, the measured delay is:
     $$\text{Propagation delay from } A\uparrow \text{ to } OUT\_STAT\downarrow = \mathbf{9.61\text{ ps}}$$
   * *Clarification:* Although both times are measured at the final logic terminals with a $1\text{ fF}$ load, the physical trigger events differ ($CLK\uparrow$ synchronous vs. $A\uparrow$ asynchronous data). Hence, the $3.734\times$ ratio is descriptive of each topology's temporal response and does not represent a strictly identical data-to-output path comparison.
2. **Delay Control Without External $C_L$ (`ENS-A1-08`):**
   * Setting $C_L = 0\text{ fF}$ on node `dyn` reduces evaluation delay to $t_{pHL,dyn} = 11.26\text{ ps}$ and $t_{pd,\text{eval}} = 21.27\text{ ps}$.
   * *Clarification:* Even without the lumped $2\text{ fF}$ capacitor, `dyn` is not capacitance-free: it retains the drain diffusion capacitances of $M_p$ and $M_1$, intrinsic BSIM4/PTM 45 nm MOS capacitances, and the input gate capacitance of the domino inverter ($M_{pi}$, $M_{ni}$).

---

## 3. Phase Analysis and Waveforms (Task 1)

In the official simulation ([`circuitos/nand3_dinamica_base.cir`](circuitos/nand3_dinamica_base.cir)), the clock switches at $500\text{ MHz}$ ($T_{clk} = 2\text{ ns}$) and input $A$ has an intentional $1.1\text{ ns}$ delay ($0.55 T_{clk}$), revealing the four fundamental operating phases (see Figure 1):

1. **Phase I: Evaluation with Open PDN ($t \in [0.0, 1.0\text{ ns}]$):**
   * Clock $CLK = 1$ ($M_p$ off, footer $M_f$ conducting).
   * Input $A = 0 \implies$ transistor $M_1$ is off, blocking any path to ground.
   * **Dynamic Node State:** `dyn` remains **FLOATING high ($V_{DD} = 1.0\text{ V}$)**.
   * A slight overshoot to $1.022\text{ V}$ appears due to capacitive clock feedthrough through $C_{gd}(M_p)$ on the rising $CLK$ edge.
2. **Phase II: Precharge with $A=1$ ($t \in [1.0, 2.0\text{ ns}]$):**
   * Clock $CLK = 0$ ($M_p$ actively pulling up to $V_{DD}$, footer $M_f$ off).
   * At $t = 1.1\text{ ns}$, input $A$ switches to 1. Although $A=B=C=1$, $M_f$ remains off ($CLK=0$), so no pull-down path forms and `dyn` stays driven to $V_{DD}$ by $M_p$.
3. **Phase III: Evaluation with Full Discharge ($t \in [2.0, 3.0\text{ ns}]$):**
   * Clock $CLK = 1$ (rising edge at $t = 2.0\text{ ns}$).
   * Since $A=B=C=1$, the entire PDN ($M_1, M_2, M_3, M_f$) conducts simultaneously.
   * Dynamic node `dyn` discharges to $0\text{ V}$ with delay $t_{pHL,dyn} = 22.17\text{ ps}$.
   * The domino inverter output `out` transitions monotonically $0 \to 1$ with $t_{pLH,out} = 35.89\text{ ps}$.
4. **Phase IV: Precharge and Restoration ($t \in [3.0, 4.0\text{ ns}]$):**
   * Clock $CLK = 0$ (falling edge at $t = 3.0\text{ ns}$).
   * $M_p$ turns on and recharges `dyn` from $0\text{ V}$ to $V_{DD}$ with precharge delay $t_{pLH,dyn} = 25.13\text{ ps}$.
   * The domino inverter restores `out` back to $0\text{ V}$ with $t_{pHL,out} = 38.06\text{ ps}$.

---

## 4. Timing Asymmetry and Role of $t_{pLH}$ in Domino Logic (Task 2)

* **Why does $t_{pLH}$ of the dynamic node "not count" as logic delay in domino?**  
  In domino logic, data propagation occurs exclusively during the evaluation phase ($CLK=1$), where outputs switch monotonically on rising edges ($0 \to 1$). Precharge ($t_{pLH}$ at `dyn`, corresponding to $t_{pHL}$ at `out`) occurs while $CLK=0$, a global restoration half-cycle outside the combinational data critical path.
* **Constraint imposed on the clock period ($T_{clk}$):**  
  The precharge half-period ($T_{clk}/2$) must be strictly sufficient for $M_p$ to restore `dyn` completely to $V_{DD}$:
  $$\frac{T_{clk}}{2} \ge t_{\text{precharge}} \approx 3 \text{ to } 4 \times \tau_{\text{pre}}$$
  If clock frequency increases such that $T_{clk}/2 < t_{\text{precharge}}$, evaluation begins with incomplete charge ($V(dyn) < V_{DD}$), degrading $NM_H$ and risking spurious firing in cascaded gates.

---

## 5. The Power Trap and Analytical vs. Measured Comparison (Task 4)

### A. Explanation of the Power Trap
With inputs permanently fixed high ($A=1, B=1, C=1$):
* In the **static NAND3**, the output remains fixed at $0\text{ V}$. With zero node transitions, dynamic activity is zero ($\alpha = 0$), leaving only subthreshold and gate leakage ($P_{\text{stat}} = 1.7004\text{ nW}$).
* In the **footed dynamic NAND3**, even with constant data inputs, the clock switches periodically at $500\text{ MHz}$:
  * During precharge ($CLK=0$), $M_p$ charges `dyn` to $V_{DD}$.
  * During evaluation ($CLK=1$), the PDN discharges `dyn` to ground.
  Thus, the dynamic gate switches with a **forced activity factor $\alpha = 1$ every clock cycle**, consuming $2.7255\ \mu\text{W}$ (**$1602.9\times$** higher than static).

### B. Theoretical Load Power vs. Measured Power
The theoretical dynamic power required to charge and discharge the explicit lumped load ($C_L = 2.0\text{ fF}$) at $\alpha = 1$, $V_{DD} = 1.0\text{ V}$, and $f = 500\text{ MHz}$ is:
$$P_{\text{theor}}(C_L) = \alpha \cdot C_L \cdot V_{DD}^2 \cdot f = 1 \times (2.0\text{ fF}) \times (1.0\text{ V})^2 \times (500\times 10^6\text{ s}^{-1}) = \mathbf{1.0000\ \mu\text{W}}$$

Total average power supplied by $V_{DD}$, measured in LTspice via `.meas TRAN Pavg AVG -I(Vdd)*V(vdd)`, is:
$$P_{\text{measured,total}} = \mathbf{2.7255\ \mu\text{W}}$$

### C. Physical Justification of the Discrepancy
The difference between elementary $C_L$ power ($1.000\ \mu\text{W}$) and total source power ($2.7255\ \mu\text{W}$) arises from:
1. **Dynamic node parasitics ($C_{par,dyn}$):** Drain diffusion capacitances of $M_p$ and $M_1$, plus input gate capacitance of the domino inverter ($M_{pi}, M_{ni}$).
2. **Output domino inverter switching:** Every cycle, `out` switches between $0\text{ V}$ and $V_{DD}$, driving $C_{out} = 1\text{ fF}$ and inverter drain diffusions.
3. **Short-circuit current in the domino inverter:** Finite simultaneous conduction of $M_{pi}$ and $M_{ni}$ during `dyn` transitions.
4. **Internal PDN diffusion charging/discharging:** Intermediate series nodes ($n_1, n_2, n_3$) undergo partial charge redistribution.
5. **Static leakage:** Subthreshold and gate tunneling currents across all devices connected to $V_{DD}$.

*Methodological Note:* Consistent with physical integrity rules, no fabricated arithmetic breakdown is assigned to individual sub-components; each physical mechanism contributes to the measured $2.7255\ \mu\text{W}$ total.

---

## 6. Retention with Open PDN and Leakage Degradation (Task 5)

In this test, $V_c = 0\text{ V}$ (bottom transistor $M_3$ off), permanently opening the PDN path to ground.

### Retention Comparison at $27^\circ\text{C}$:
1. **Nominal Clock ($T_{clk} = 2\text{ ns}$, $f = 500\text{ MHz}$):**
   * During the $1\text{ ns}$ evaluation phase, `dyn` floats high.
   * Minimum voltage reached: $V(dyn)_{\text{min}} = \mathbf{0.9936\text{ V}}$, a drop of only $\Delta V = \mathbf{6.41\text{ mV}}$.
   * Output `out` stays near $0\text{ V}$ ($V_{out,\text{max}} = 0.31\text{ mV}$).
   * **Conclusion:** At $500\text{ MHz}$, the evaluation window is short enough that leakage does not compromise retention.
2. **Slow Clock ($T_{clk} = 400\text{ ns}$, continuous $200\text{ ns}$ evaluation window):**
   * Over $200\text{ ns}$ of floating retention, subthreshold leakage ($I_{off}$) through the PDN and footer drains node charge.
   * Voltage decays monotonically to $V(dyn)_{\text{final}} = \mathbf{0.8837\text{ V}}$, a net loss of $\Delta V = \mathbf{116.28\text{ mV}}$.
   * At $27^\circ\text{C}$, the final voltage ($0.884\text{ V}$) remains above the inverter switching threshold ($V_M = 0.48\text{ V}$), so `out` stays quiescent ($V_{out} \approx 0.04\text{ mV}$).
   * **Experimental Conclusion:** Longer evaluation windows produce measurable cumulative charge loss, demonstrating that a floating dynamic node cannot hold state indefinitely and motivating minimum frequency ($f_{min}$) and keeper sizing studies in Activities 2 and 3.

---

## 7. Input Capacitance Advantage $C_{in}(A)$

* **Structural Difference:**
  * In the static gate, input $A$ drives one PDN NMOS ($W = 270\text{ nm}$) and one PUN PMOS ($W = 135\text{ nm}$), totaling $405\text{ nm}$ of gate width.
  * In the footed dynamic gate, the PUN is replaced by the clock-driven precharge PMOS; input $A$ drives only the PDN NMOS ($W = 270\text{ nm}$).
* **Canonical Corrected Result (`ENS-A1-HIG-01`):**
  * Measured in [`circuitos/nand3_extraccion_cin_corregido.cir`](circuitos/nand3_extraccion_cin_corregido.cir) ($M_{ni}$ at $W=90\text{ nm}$ consistent with the base topology) via current integration over a $50\text{ ps}$ ramp ($Q_{in} = \int_{90\text{ ps}}^{170\text{ ps}} -I(V_a)\,dt$):
    $$C_{in,\text{dyn}} = \mathbf{0.3417\text{ fF}} \quad \text{vs.} \quad C_{in,\text{stat}} = \mathbf{0.5936\text{ fF}} \implies \text{Ratio } \mathbf{0.5756} \quad (-\mathbf{42.4\%})$$
  * *Preliminary historical reference (`ENS-A1-04`):* With $M_{ni} = 270\text{ nm}$, yielded $C_{in,\text{dyn}} = 0.3415\text{ fF}$ ($-42.5\%$), confirming input load at $A$ is dominated by $M_1$.
* **Geometric Estimate vs. SPICE Measurement:**
  * Using parameters from `../modelos/ptm45hp.lib` (local dependency, excluded from Git; $t_{oxe,n} = 1.25\text{ nm}$, $t_{oxe,p} = 1.30\text{ nm}$, $\epsilon_{ox} = 3.9 \cdot \epsilon_0$):
    $$C_{ox,n} = \frac{3.9 \times 8.854 \times 10^{-12}\text{ F/m}}{1.25 \times 10^{-9}\text{ m}} \approx 27.63\text{ fF}/\mu\text{m}^2, \qquad C_{ox,p} = \frac{3.9 \times 8.854 \times 10^{-12}\text{ F/m}}{1.30 \times 10^{-9}\text{ m}} \approx 26.56\text{ fF}/\mu\text{m}^2$$
    $$C_{in,\text{dyn,geom}} \approx C_{ox,n} W_n L = (27.63\text{ fF}/\mu\text{m}^2)(0.270\,\mu\text{m} \times 0.045\,\mu\text{m}) \approx \mathbf{0.336\text{ fF}}$$
    $$C_{in,\text{stat,geom}} \approx 0.3356\text{ fF} + (26.56\text{ fF}/\mu\text{m}^2)(0.135\,\mu\text{m} \times 0.045\,\mu\text{m}) = 0.3356\text{ fF} + 0.1614\text{ fF} \approx \mathbf{0.497\text{ fF}}$$
  * Differences with SPICE arise because large-signal integration includes strong-inversion channel formation, gate-source/drain overlap capacitances ($C_{ov}$), and fringing capacitances omitted in the 1D geometric estimate.

---

## 8. Generated Figures (300 DPI)

Located in `act1/figuras/`:
1. [`figuras/fig1_act1_fases_formas_onda.png`](figuras/fig1_act1_fases_formas_onda.png): Waveforms $V(clk), V(a), V(dyn), V(out)$ with shaded bands labeling the four operating phases.
2. [`figuras/fig2_act1_dinamica_vs_estatica.png`](figuras/fig2_act1_dinamica_vs_estatica.png): Synchronized temporal comparison under the **same input stimulus** $V(a)$ ($T_A=8\text{ ns}$).
3. [`figuras/fig3_act1_retencion_pdn_abierta.png`](figuras/fig3_act1_retencion_pdn_abierta.png): Charge loss on the floating dynamic node at $T_{clk}=2\text{ ns}$ ($\Delta V = 6.4\text{ mV}$) vs. $T_{clk}=400\text{ ns}$ ($\Delta V = 116.3\text{ mV}$).
