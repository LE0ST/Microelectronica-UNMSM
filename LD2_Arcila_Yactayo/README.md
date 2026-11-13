# Laboratory Project No. 2: Sub-Micron Dynamic & Domino CMOS Logic

**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Course:** Microelectronics and Nanoelectronic Systems (2026-II)  
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)  
**Official Technical Report (Spanish, 20 pages IEEE):** [`informe_latex/main.pdf`](informe_latex/main.pdf)

---

## Overview

This module presents the physical modeling, SPICE circuit simulation (LTspice with **BSIM4 Level 54** PTM cards), Python post-processing, and technical documentation for **dynamic and domino CMOS logic** across **45 nm High-Performance (HP)**, **45 nm Low-Power (LP)**, and **130 nm Bulk CMOS** nodes. All circuits are implemented as pure `.cir` netlists to specify exact diffusion geometries (`AS`, `AD`, `PS`, `PD`) and strict numerical tolerances (`abstol=1e-14`, `gmin=1e-15`, `cshunt=1e-18`).

---

## Key Findings

| Activity | Metric / Phenomenon | Condition / Configuration | Measured Value (SPICE) | Key Takeaway |
| :--- | :--- | :--- | :--- | :--- |
| **A1** | Input capacitance ($C_{in}$) | Footed dynamic vs. static NAND3 (45 nm HP) | $0.3417\text{ fF}$ vs. $0.5936\text{ fF}$ | **$-42.4\%$** reduction by eliminating PUN |
| **A1** | Output propagation delay | $C_{out} = 1.0\text{ fF}$, 45 nm HP | Dynamic: $35.89\text{ ps}$ ($CLK\uparrow$)<br>Static: $9.61\text{ ps}$ ($A\uparrow$) | Asymmetric clock-to-out vs. data-to-out trigger |
| **A2** | Worst-case charge sharing | Baseline without mitigation ($C_L = 2.0\text{ fF}$) | $\Delta V_{dyn} = 164.29\text{ mV}$ | Safe margin ($V_{dyn,\min} = 0.8357\text{ V}$, $NM_H = +257.2\text{ mV}$) |
| **A2** | Mitigation: internal precharge | Internal PMOS precharge ($W_p = 45\text{ nm}$) | Droop suppressed ($+50.47\text{ mV}$ overshoot) | $+0.127\text{ fF}$ clock load overhead |
| **A2** | Mitigation: C-A-B reordering | Internal node decoupling (Vector B) | $\Delta V_{dyn} = 72.08\text{ mV}$ | Zero area overhead |
| **A2** | Mitigation: PMOS keeper | Conventional keeper ($W_{kp} = 45\text{ nm}$) | $\Delta V_{dyn} = 69.68\text{ mV}$ | Restores to $0.9996\text{ V}$; $+14.65\%$ $t_{pHL,dyn}$ penalty |
| **A3** | Retention without keeper | 45 nm HP @ $85\ ^\circ\text{C}$ ($T_{\text{stop}} = 1.0\ \mu\text{s}$) | $t_{hold} = 608.17\text{ ns}$ ($0.90\,V_{DD}$) | 130 nm Bulk @ $85\ ^\circ\text{C}$: $t_{hold} = 167.53\text{ ns}$ |
| **A3** | Keeper viability window | 45 nm HP @ $85\ ^\circ\text{C}$ ($\Delta t_{pHL} \le 10\%$) | $W_{kp} \in [10.5, 38.0]\text{ nm}$ | Reference $W_{kp}=22\text{ nm}$: $+5.25\%$ penalty; conditional keeper: $+5.11\%$ |
| **A4** | Domino monotonicity & skew | 3-stage footed domino cascade | $t_{skew} \approx 18.5\text{ ps}$ | $1\to 0$ input glitch causes irreversible charge loss; footed blocks short-circuit |
| **A5** | Clock feedthrough & NTV | $V_{DD} = 1.0\text{ V} \to 0.40\text{ V}$ (45 nm HP @ $85\ ^\circ\text{C}$) | $+64.31\text{ mV}$ ($+49.31\text{ mV}$ w/ keeper)<br>$f_{\max} \approx 420\text{ MHz}$, $f_{\min} \approx 1.12\text{ MHz}$ | **$-85.2\%$** switching energy ($0.1076\text{ fJ}$ vs. $0.7259\text{ fJ}$) |

---

## Technologies

* **SPICE Simulator:** LTspice (BSIM4 Level 54, pure `.cir` netlists with renamed collision-free `.lib` models)
* **Device Models:** PTM 45 nm HP (`ptm45hp.lib`), 45 nm LP (`ptm45lp.lib`), 130 nm Bulk (`ptm130.lib`)
* **Post-Processing:** Python 3.10+ (`numpy`, `matplotlib`)
* **Documentation:** LaTeX (`IEEEtran`, 20-page final report)

---

## Repository Structure

```text
LD2_Arcila_Yactayo/
├── README.md                    # This file
├── README.txt                   # Original Spanish delivery runbook
├── trazabilidad_figuras.txt     # Bijective Figure -> Netlist -> Script matrix
├── verificacion_modelos.txt     # BSIM4 Level 54 parameter verification
├── modelos/                     # Collision-free renamed PTM libraries (.lib)
├── act1/ ... act5/              # Activities 1–5 (circuitos/, scripts/, resultados/, figuras/)
├── act6/                        # Optional Activity 6 placeholder (not developed)
└── informe_latex/               # Master IEEE LaTeX source & main.pdf (20 pages)
```

---

## Reproduction Instructions

1. **Obtain & Place PTM Models (Third-Party Dependency):**
   * Predictive Technology Model (PTM) BSIM4 parameter files (ASU/Berkeley NIMO Group) are **not redistributed** in this public repository due to the absence of an explicit redistribution license.
   * Obtain the original `45nm_HP.pm`, `45nm_LP.pm`, and `130nm_bulk.pm` cards and generate/place the collision-free renamed libraries (`ptm45hp.lib`, `ptm45lp.lib`, `ptm130.lib`, `ptm45hp_aux.lib`) in `LD2_Arcila_Yactayo/modelos/` following [`modelos/README_modelos.md`](modelos/README_modelos.md).
2. **Run SPICE simulations (LTspice):** All netlists use relative paths (`../../modelos/*.lib`):
   ```powershell
   & "$env:LTSPICE_EXE" -b "LD2_Arcila_Yactayo/act1/circuitos/nand3_dinamica_base.cir"
   & "$env:LTSPICE_EXE" -b "LD2_Arcila_Yactayo/act2/circuitos/nand3_cs_g2b_piloto_cl2f.cir"
   ```
2. **Regenerate 300 DPI figures (Python 3.10+):**
   ```powershell
   python LD2_Arcila_Yactayo/act1/scripts/generar_figuras_act1.py
   python LD2_Arcila_Yactayo/act2/scripts/generar_figuras_act2.py
   python LD2_Arcila_Yactayo/act3/scripts/generar_figura8_editorial.py
   python LD2_Arcila_Yactayo/act4/scripts/generar_figuras_act4.py
   python LD2_Arcila_Yactayo/act5/scripts/generar_figuras_act5.py
   ```

---

## Validation & Limitations

* **Model Collision Prevention:** PTM cards are renamed (`nmos_45hp`, `nmos_45lp`, `nmos_130`) per `modelos/README_modelos.md` to allow multi-technology comparisons in a single netlist without silent `.model` overrides.
* **45 nm LP Retention:** At $T_{\text{stop}} = 1.0\ \mu\text{s}$ and $85\ ^\circ\text{C}$, 45 nm LP retention exceeds the simulation window ($>1.0\ \mu\text{s}$, right-censored).
* **Optional Activity 6:** Complex multi-stage domino logic (`act6/`) was optional and intentionally omitted to focus on physical verification and non-ideal keeper analysis in Activities 1–5.

---

## References

* Zhao, W., & Cao, Y. (2006). *New Generation of Predictive Technology Model for Sub-45 nm Early Design Exploration*. IEEE TED.
* Weste, N. H. E., & Harris, D. *CMOS VLSI Design: A Circuits and Systems Perspective*.
