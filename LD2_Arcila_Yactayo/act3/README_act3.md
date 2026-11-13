# Activity 3 — Restoration and Robustness: Keeper Sizing and Contention

**Course:** Microelectronics and Nanoelectronic Systems (Semester 2026-II)  
**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Instructor:** MsC. Luz Adanaqué Infante  
**Authors:** Leonardo Sait Yactayo Tolentino (`23190214`) & Marco Antonio Arcila Santander (`23190140`)  
**Working Directory:** [`act3/`](.)  
**Evaluated Technologies:** PTM 45 nm HP, PTM 45 nm LP, PTM 130 nm Bulk

---

## 1. Circuit Topology and PMOS Keeper Function

In the domino dynamic NAND3 gate, dynamic node `dyn` floats during the evaluation phase ($CLK = 1$) whenever inputs keep the pull-down network (PDN) off. In deep-submicron technologies (45 nm), subthreshold leakage ($I_{sub}$) and gate tunneling ($I_{gate}$) progressively discharge `dyn`, threatening logic integrity.

To counter charge loss without unduly penalizing switching speed:
* A **PMOS keeper** ($M_k$) is connected with its source at $V_{DD}$, drain at `dyn`, and gate driven by the inverted output `out`.
* When `dyn` is high, `out = 0`, turning on $M_k$ to replenish lost charge ($I_{kp} \ge I_{leak,tot}$).
* When the PDN evaluates to ground ($A=B=C=1$), it must overcome $M_k$'s contention current until `out` switches high (turning $M_k$ off), introducing a delay penalty $\Delta t_{pHL}$.

---

## 2. Temporal Retention Campaign ($1.0\ \mu\text{s}$ Window)

Charge retention was evaluated under the guide's criterion ($V_{dyn}(1\,\mu\text{s}) > 0.90\,V_{DD}$) at $27^\circ\text{C}$ and $85^\circ\text{C}$:

| Technology | Temp | $V_{dyn}(1\,\mu\text{s})$ Without Keeper | $t_{\text{hold}}$ to $0.90\,V_{DD}$ | Status Without Keeper | With Keeper ($W_{kp}=22\text{ nm}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **PTM 45nm HP** | $27^\circ\text{C}$ | $0.9370\text{ V}$ | $> 1.0\ \mu\text{s}$ | Passes retention | $0.999994\text{ V}$ (Stable) |
| **PTM 45nm HP** | $85^\circ\text{C}$ | $0.7836\text{ V}$ | **$608.17\text{ ns}$** | **Fails retention** | $0.999975\text{ V}$ (Stable) |
| **PTM 45nm LP** | $85^\circ\text{C}$ | $0.9997\text{ V}$ | $> 1.0\ \mu\text{s}$ | Passes retention | $1.000000\text{ V}$ (Stable) |
| **PTM 130nm** | $85^\circ\text{C}$ | $0.9985\text{ V}$ | $> 1.0\ \mu\text{s}$ | Passes retention | $1.000000\text{ V}$ (Stable) |

### Physical Diagnosis:
1. In 45 nm HP at $85^\circ\text{C}$, thermal increase in subthreshold leakage ($I_{sub} \propto T^2 \exp(-qV_{th}/mkT)$) reduces retention time to $608.17\text{ ns}$, making an active keeper mandatory.
2. In 45 nm LP and 130 nm Bulk, higher threshold voltages and thicker oxides reduce leakage by orders of magnitude, making the keeper unnecessary for static retention over a $1\ \mu\text{s}$ window.

---

## 3. Contention Trade-Off and Joint Viability Window

The official guide requires the relative delay penalty introduced by the keeper to remain strictly below $10\%$:
$$\Delta t_{pHL} = \frac{t_{pHL}(W_{kp}) - t_{pHL}(W_{kp}=0)}{t_{pHL}(W_{kp}=0)} \times 100\% < 10.00\%$$

A fine simulation sweep with $1\text{ nm}$ step was performed in 45 nm HP at $85^\circ\text{C}$:

| $W_{kp}$ (nm) | Ratio $r = W_{kp}/(67.5\text{ nm})$ | $V_{dyn}(1\,\mu\text{s})$ | Retention ($>0.9V_{DD}$) | $\Delta t_{pHL}$ (%) | Contention ($<10\%$) | Joint Viability |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10.5** | 0.156 | 0.999968 V | YES | +3.64% | YES | **VIABLE (Min)** |
| **15.0** | 0.222 | 0.999971 V | YES | +4.18% | YES | **VIABLE** |
| **22.0** | 0.326 | 0.999975 V | YES | +5.34% | YES | **VIABLE (Reference)** |
| **30.0** | 0.444 | 0.999981 V | YES | +6.82% | YES | **VIABLE** |
| **38.0** | 0.563 | 0.999985 V | YES | **+9.94%** | YES | **VIABLE (Max)** |
| **39.0** | 0.578 | 0.999986 V | YES | +10.23% | **NO** | NOT VIABLE |
| **45.0** | 0.667 | 0.999988 V | YES | +12.90% | **NO** | NOT VIABLE |
| **60.0** | 0.889 | 0.999992 V | YES | +20.43% | **NO** | NOT VIABLE |

### Verified Design Bounds:
* **Viable Window in 45 nm HP @ $85^\circ\text{C}$:**
  $$W_{kp} \in [10.5\text{ nm},\ 38.0\text{ nm}] \quad \iff \quad r \in [0.156,\ 0.563]$$
* The conventional reference point ($W_{kp} = 22\text{ nm}$, $W_{eff} = 12\text{ nm}$, $r = 0.326$) operates comfortably inside the window with $\Delta t_{pHL} \approx +5.34\%$, ensuring $V_{dyn}(1\,\mu\text{s}) = 0.999975\text{ V}$.

---

## 4. Advanced Alternative: Conditional Keeper

To decouple static retention from dynamic contention:
* A **conditional keeper with a delay line** (two auxiliary CMOS inverters) was evaluated.
* During fast evaluation, the keeper stays initially off due to the delay line and activates only if `dyn` remains high after the guard window.
* **Result:** Delay penalty dropped to **$+5.11\%$** (vs. $+12.90\%$ for the conventional $45\text{ nm}$ keeper), at the cost of moderate area and switching power overhead.

---

## 5. Generated Figures (Activity 3)

* [`figuras/fig1_act3_retencion_formas_onda.png`](figuras/fig1_act3_retencion_formas_onda.png): Transient evolution of $V(dyn)$ over $1.0\ \mu\text{s}$ at $27^\circ\text{C}$ and $85^\circ\text{C}$ with and without keeper.
* [`figuras/fig2_act3_consolidacion_hp_lp_130.png`](figuras/fig2_act3_consolidacion_hp_lp_130.png): Multi-technology retention comparison (HP vs. LP vs. 130 nm).
* [`figuras/fig3_act3_contencion_penalizacion.png`](figuras/fig3_act3_contencion_penalizacion.png): Delay penalty $\Delta t_{pHL}$ curves vs. $W_{kp}$ and aspect ratio $r$.
* [`figuras/fig4_act3_ventana_viabilidad.png`](figuras/fig4_act3_ventana_viabilidad.png): Joint viability window (retention $>0.9V_{DD}$ vs. contention $<10\%$).
* [`figuras/fig5_act3_keeper_condicional.png`](figuras/fig5_act3_keeper_condicional.png): Waveforms and timing analysis of the conditional keeper with delay line.
