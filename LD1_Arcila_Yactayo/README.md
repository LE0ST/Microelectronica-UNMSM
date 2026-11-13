# Laboratory Project No. 1: Static CMOS Logic Characterization (45 nm PTM BSIM4)

**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — FIEE  
**Course:** Microelectronics and Nanoelectronic Systems (2026-II)  
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)  
**Official Technical Report (Spanish, 12 pages IEEE):** [`informe_latex/LD1_Arcila_Yactayo.pdf`](informe_latex/LD1_Arcila_Yactayo.pdf)

---

## Overview

This module investigates the static and transient electrical behavior of fundamental and complex static CMOS logic gates using **BSIM4 (Level 54)** Predictive Technology Models (PTM) in **LTspice**, automated with **Python** for 300 DPI waveform and regression plotting.

---

## Activities & Key Findings

1. **Activity 1 — CMOS Inverter VTC & Beta Calibration (`A1_Inversor_VTC/`):**
   * Swept PMOS-to-NMOS width ratio $\beta = W_p / W_n \in [1.0, 3.0]$ in 45 nm HP ($V_{DD} = 1.0\text{ V}$) and 45 nm LP ($V_{DD} = 1.1\text{ V}$).
   * Calibrated optimal symmetric switching threshold at **$\beta_{\text{opt}} = 2.50$**, achieving **$V_M = 0.4989\text{ V}$** and balanced noise margins ($NM_H$, $NM_L$).
2. **Activity 2 — Transient Delay vs. Load Capacitance & Node Scaling (`A2_Retardo_Transitorio/`):**
   * Measured $t_{pHL}$, $t_{pLH}$, and $t_p$ across $C_L \in [1\text{ fF}, 8\text{ fF}]$ at $\beta = 2.50$ in 45 nm HP.
   * Compared FO4-style transient scaling across **90 nm Bulk** ($1.2\text{ V}$), **45 nm HP** ($1.0\text{ V}$), and **22 nm HP** ($0.8\text{ V}$).
3. **Activity 3 — NAND2 vs. NOR2 & Input-Order Logical Effort (`A3_NAND2_NOR2/`):**
   * Evaluated asymmetrical switching delays for outer vs. inner series inputs in NAND2 and single vs. parallel inputs in NOR2.
4. **Activity 4 — Complex Gate Synthesis: 6T AOI21 (`A4_Compuerta_Compleja/`):**
   * Synthesized and simulated $Y = \overline{(A \cdot B) + C}$ with $\beta = 2.0$, measuring worst-case pull-down/pull-up propagation delays using time-windowed `.meas` directives.
5. **Activity 5 — Static Leakage & 5-Stage Ring Oscillator (`A5_Potencia_y_RO/`):**
   * Contrasted **45 nm HP** vs. **45 nm LP** quiescent leakage currents and 5-stage ring oscillator performance:
     * **45 nm HP:** $f_{\text{osc}} = 21.94\text{ GHz}$, $t_{pd} = 4.56\text{ ps/stage}$.
     * **45 nm LP:** $f_{\text{osc}} = 6.25\text{ GHz}$, $t_{pd} = 15.99\text{ ps/stage}$.

---

## Technologies

* **SPICE Simulator:** LTspice (BSIM4 Level 54, `.meas` batch extraction)
* **Device Models:** Predictive Technology Model (PTM) 22 nm, 32 nm, 45 nm HP/LP, 65 nm, 90 nm, 130 nm, 180 nm
* **Post-Processing:** Python 3 (`numpy`, `matplotlib`)
* **Documentation:** LaTeX (`IEEEtran`, 12-page limit)

---

## Directory Structure

```text
LD1_Arcila_Yactayo/
├── README.md                    # This file
├── LEAME_ENTREGA.txt            # Original Spanish delivery manifest
├── informe_latex/
│   ├── LD1.tex                  # Master IEEE LaTeX source
│   ├── LD1_Arcila_Yactayo.pdf   # Final compiled 12-page report (Spanish)
│   └── figuras/                 # 300 DPI figures (Fig. 1 to Fig. 8)
├── simulaciones/
│   ├── A1_Inversor_VTC/         # VTC sweeps & LTspice cursor captures
│   ├── A2_Retardo_Transitorio/  # Delay vs CL & 22nm/45nm/90nm scaling
│   ├── A3_NAND2_NOR2/           # NAND2/NOR2 input switching cases
│   ├── A4_Compuerta_Compleja/   # 6T AOI21 netlist & logs
│   └── A5_Potencia_y_RO/        # Quiescent leakage & 5-stage ring oscillators
├── modelos/                     # PTM model cards (.pm / .lib)
└── scripts/                     # Python plotting & packaging scripts
```

---

## Reproduction Instructions

1. **Obtain & Place PTM Models (Third-Party Dependency):**
   * Predictive Technology Model (PTM) BSIM4 parameter files (ASU/Berkeley NIMO Group) are **not redistributed** in this public repository due to the absence of an explicit redistribution license.
   * Download the PTM parameter files (`22nm_HP.pm`, `45nm_HP.pm`, `45nm_LP.pm`, `90nm_bulk.pm`, `130nm_bulk.pm`, etc.) from the official PTM distribution and place them in:
     * `LD1_Arcila_Yactayo/modelos/`
     * And inside the corresponding activity folders (`LD1_Arcila_Yactayo/simulaciones/A1_Inversor_VTC/` through `A5_Potencia_y_RO/`) as referenced by each `.cir` `.include` directive.
2. **Run any SPICE netlist in batch mode (LTspice):**
   ```powershell
   & "$env:LTSPICE_EXE" -b "LD1_Arcila_Yactayo/simulaciones/A1_Inversor_VTC/A1_VTC.cir"
   ```
   Inspect `.meas` outputs in the generated `.log` file.
2. **Regenerate figures (Python 3):**
   ```powershell
   pip install numpy matplotlib
   python LD1_Arcila_Yactayo/scripts/generar_graficas.py
   ```

---

## Validation & Limitations

* All `.cir` netlists include local PTM `.pm` model cards in their respective activity folders for standalone execution.
* PTM models are predictive academic/research parameter sets (ASU NIMO Group) intended for comparative technology-node analysis rather than foundry sign-off.

---

## References

* Zhao, W., & Cao, Y. (2006). *New Generation of Predictive Technology Model for Sub-45 nm Early Design Exploration*. IEEE Transactions on Electron Devices.
* Rabaey, J. M., Chandrakasan, A., & Nikolic, B. *Digital Integrated Circuits: A Design Perspective*.
