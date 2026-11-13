# Microelectronics and Nanoelectronic Systems — UNMSM FIEE

**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — Faculty of Electronic and Electrical Engineering (FIEE)  
**Academic Term:** 2026-II  
**Authors:**
* **Leonardo Sait Yactayo Tolentino** (`23190214`) — Co-author of LD1 & LD2; Sole author of LD3
* **Marco Antonio Arcila Santander** (`23190140`) — Co-author of LD1 & LD2

---

## Overview

This repository consolidates the SPICE circuit simulations, Python post-processing pipelines, validation suites, and IEEE-formatted technical reports developed for **Microelectronics and Nanoelectronic Systems**. It spans two complementary domains:

1. **Sub-Micron Digital CMOS Logic (LD1 & LD2):** Static and dynamic/domino characterization using **BSIM4 (Level 54)** Predictive Technology Models (PTM) across 130 nm, 90 nm, 45 nm HP/LP, and 22 nm nodes.
2. **Power Semiconductor Devices — IGBTs (LD3):** Double Pulse Test (DPT) switching characterization of N/P-channel behavioral macromodels and commercial 650 V Trench Field-Stop IGBTs (Fuji Electric X-Series).

> [!NOTE]
> The official technical reports (`.pdf`) are preserved in their original Spanish academic versions without alteration.

---

## Laboratory Projects

| Lab | Title | Authors | Report (Spanish) | Highlights |
| :---: | :--- | :--- | :--- | :--- |
| [**LD1**](LD1_Arcila_Yactayo/) | Static CMOS Logic Characterization | L. Yactayo & M. Arcila | [12-page PDF](LD1_Arcila_Yactayo/informe_latex/LD1_Arcila_Yactayo.pdf) | $\beta_{\text{opt}} = 2.50$ ($V_M = 0.4989\text{ V}$), FO4 scaling (90/45/22 nm), 6T AOI21, 5-stage RO ($21.94\text{ GHz}$ HP vs. $6.25\text{ GHz}$ LP) |
| [**LD2**](LD2_Arcila_Yactayo/) | Sub-Micron Dynamic & Domino CMOS | L. Yactayo & M. Arcila | [20-page PDF](LD2_Arcila_Yactayo/informe_latex/main.pdf) | $-42.4\%$ $C_{in}$ vs. static NAND3, charge sharing ($164.29\text{ mV}$ droop), keeper window ($[10.5, 38.0]\text{ nm}$ @ $85\ ^\circ\text{C}$), NTV ($0.40\text{ V}$, $-85.2\%$ energy) |
| [**LD3**](LD3_Yactayo/) | Comparative IGBT Characterization (DPT) | L. Yactayo *(Individual)* | [15-page PDF](LD3_Yactayo/informe/informe_ld3_yactayo.pdf) | Duncan N/P & Fuji X-Series (50 A / 75 A), isolated `Vsens_C` Tellegen balance ($-33\text{ pJ}$), die-area scaling ($-13.3\%$ $V_{CE(\text{on})}$, $+28.2\%$ $E_{\text{off}}$), $R_G$ trade-off |

---

## Key Findings

* **Static & Dynamic CMOS (LD1–LD2):** Eliminating the pull-up network in dynamic NAND3 reduces input capacitance by $42.4\%$, while aggressive voltage scaling to $0.40\text{ V}$ (NTV) cuts switching energy by $85.2\%$ with a viable $1.12\text{ MHz}$–$420\text{ MHz}$ window at $85\ ^\circ\text{C}$.
* **Power IGBT Switching (LD3):** Doubling gate resistance ($10\ \Omega \to 20\ \Omega$) in `FGW50XS65C` reduces inductive bus overshoot ($L_\sigma = 25\text{ nH}$) by $38.8\%$ ($+42.36\text{ V} \to +25.94\text{ V}$) at the cost of $+70.5\%$ turn-off energy. Commercial Fuji X-Series models match datasheet $t_{d(\text{off})}$ within $+4.7\%$ to $+5.0\%$.

---

## Technologies

* **SPICE Simulation:** LTspice 24+ (`.cir` batch execution, `.asc` schematics, `.meas` extraction, ASCII `.raw`)
* **Post-Processing:** Python 3.10+ (`numpy`, `matplotlib`)
* **Typesetting:** LaTeX (`IEEEtran`)

---

## Repository Structure

```text
MicroNano/
├── README.md                    # Main repository documentation (this file)
├── .gitignore                   # Excludes .raw, .db, .log, ZIPs, previews, caches; keeps .plt
├── LD1_Arcila_Yactayo/          # Lab 1: Static CMOS (Yactayo & Arcila)
├── LD2_Arcila_Yactayo/          # Lab 2: Dynamic & Domino CMOS (Yactayo & Arcila)
├── LD3_Yactayo/                 # Lab 3: IGBT DPT Characterization (Yactayo, Individual)
│   ├── validation/              # Curated validation cases, resolved failures & limitations
│   ├── esquemas/                # LTspice .asc, .plt & .asy symbols
│   ├── simulaciones/netlists/   # Final .cir netlists
│   ├── scripts/                 # Portable Python analysis scripts (ltspice_config.py)
│   ├── modelos/                 # Third-party model provenance & download instructions
│   ├── figuras/                 # 300 DPI figures & LTspice cursor captures
│   ├── tablas/                  # Master consolidated result tables
│   ├── informe/                 # 15-page PDF report & LaTeX source
│   └── presentacion/            # Defense presentation (PDF & PPTX)
├── _docs/                       # Course roadmap, process protocol & development log
└── AGENTS.md / CLAUDE.md        # AI assistant context guidelines
```

---

## Reproduction Instructions

1. **Install Python dependencies:**
   ```powershell
   pip install -r LD3_Yactayo/requirements.txt
   ```
2. **Set LTspice path (for LD3 automation scripts):**
   ```powershell
   $env:LTSPICE_EXE = "C:\Program Files\ADI\LTspice\LTspice.exe"
   ```
3. **Download third-party IGBT models (for LD3):** See [`LD3_Yactayo/modelos/NOTAS_MODELOS.md`](LD3_Yactayo/modelos/NOTAS_MODELOS.md) for official Fuji Electric and Duncan Amps download links and placement paths.
4. **Run simulations:** See the individual READMEs in [`LD1_Arcila_Yactayo/`](LD1_Arcila_Yactayo/README.md), [`LD2_Arcila_Yactayo/`](LD2_Arcila_Yactayo/README.md), and [`LD3_Yactayo/`](LD3_Yactayo/README.md).

---

## Validation and Limitations

* **LD3 Validation Suite:** [`LD3_Yactayo/validation/README.md`](LD3_Yactayo/validation/README.md) documents `PASS` checks (Tellegen energy balance, timestep convergence), `RESOLVED FAILURE` fixes (emitter shunt contamination, artificial `Rpar` damping, P-IGBT diode polarity), and `KNOWN LIMITATION` items (`N/V*` for P-IGBT 19.48 A due to missing `.raw`, exploratory out-of-SOA 80 A runs, and co-pack reverse-bias invariance in low-side DPT).
* **Third-Party Models:** Fuji Electric `.LIB` files (`All Rights Reserved`) and Duncan `.lib` files (no explicit redistribution license) are documented for manual download rather than claimed as open-source.

---

## References

* Zhao, W., & Cao, Y. (2006). *New Generation of Predictive Technology Model for Sub-45 nm Early Design Exploration*. IEEE TED.
* Fuji Electric Co., Ltd. *Technical Discrete P-Spice Models (X-Series 650 V Trench-FS)*.
* Duncan's Amp Pages. *IGBT Behavioral SPICE Macromodels (`nigbt.lib`, `pigbt.lib`)*.
