# Microelectronics and Nanoelectronic Systems — UNMSM FIEE

**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — Faculty of Electronic and Electrical Engineering (FIEE)  
**Academic Term:** 2026-II  
**Authors:**
* **Leonardo Sait Yactayo Tolentino** (`23190214`) — Co-author of LD1, LD2 & LD4; Sole author of LD3
* **Marco Antonio Arcila Santander** (`23190140`) — Co-author of LD1, LD2 & LD4

---

## Overview

This repository consolidates the SPICE circuit simulations, Python post-processing pipelines, validation suites, and technical reports developed for **Microelectronics and Nanoelectronic Systems**. It spans three complementary domains:

1. **Sub-Micron Digital CMOS Logic (LD1 & LD2):** Static and dynamic/domino characterization using **BSIM4 (Level 54)** Predictive Technology Models (PTM) across 130 nm, 90 nm, 45 nm HP/LP, and 22 nm nodes.
2. **Power Semiconductor Devices — IGBTs (LD3):** Double Pulse Test (DPT) switching characterization of N/P-channel behavioral macromodels and commercial 650 V Trench Field-Stop IGBTs (Fuji Electric X-Series).
3. **Integrated Circuit Testing & Design-for-Testability (LD4):** Structural fault testing (`stuck-at`, `stuck-open`), Roth's D-algorithm, and 3-bit **Scan Path (`SDFF`)** characterization using **0.35 µm CMOS Level-1** models ($V_{DD} = 3.3\text{ V}$).

> [!NOTE]
> The official technical reports (`.pdf`) are preserved in their original Spanish academic versions without alteration.

---

## Laboratory Projects

| Lab | Title | Authors | Report (Spanish) | Highlights |
| :---: | :--- | :--- | :--- | :--- |
| [**LD1**](LD1_Arcila_Yactayo/) | Static CMOS Logic Characterization | L. Yactayo & M. Arcila | [12-page PDF](LD1_Arcila_Yactayo/informe_latex/LD1_Arcila_Yactayo.pdf) | $\beta_{\text{opt}} = 2.50$ ($V_M = 0.4989\text{ V}$), FO4 scaling (90/45/22 nm), 6T AOI21, 5-stage RO ($21.94\text{ GHz}$ HP vs. $6.25\text{ GHz}$ LP) |
| [**LD2**](LD2_Arcila_Yactayo/) | Sub-Micron Dynamic & Domino CMOS | L. Yactayo & M. Arcila | [20-page PDF](LD2_Arcila_Yactayo/informe_latex/main.pdf) | $-42.4\%$ $C_{in}$ vs. static NAND3, charge sharing ($164.29\text{ mV}$ droop), keeper window ($[10.5, 38.0]\text{ nm}$ @ $85\ ^\circ\text{C}$), NTV ($0.40\text{ V}$, $-85.2\%$ energy) |
| [**LD3**](LD3_Yactayo/) | Comparative IGBT Characterization (DPT) | L. Yactayo *(Individual)* | [15-page PDF](LD3_Yactayo/informe/informe_ld3_yactayo.pdf) | Duncan N/P & Fuji X-Series (50 A / 75 A), isolated `Vsens_C` Tellegen balance ($-33\text{ pJ}$), die-area scaling ($-13.3\%$ $V_{CE(\text{on})}$, $+28.2\%$ $E_{\text{off}}$), $R_G$ trade-off |
| [**LD4**](LD4_Arcila_Yactayo/) | Integrated Circuit Testing — Stuck-at, Stuck-open & Scan Path | L. Yactayo & M. Arcila | [3-page PDF](LD4_Arcila_Yactayo/informe/main.pdf) | 10-node BCD `f` (`100%` coverage in 7 vectors), `NOR2_SO` pair (`0000->0001`), 3-cycle flush, 23-cycle scan (`0.46 µs`), 521/521 LOG–RAW check, 32-fault proof |

---

## Key Findings

* **Static & Dynamic CMOS (LD1–LD2):** Eliminating the pull-up network in dynamic NAND3 reduces input capacitance by $42.4\%$, while aggressive voltage scaling to $0.40\text{ V}$ (NTV) cuts switching energy by $85.2\%$ with a viable $1.12\text{ MHz}$–$420\text{ MHz}$ window at $85\ ^\circ\text{C}$.
* **Power IGBT Switching (LD3):** Doubling gate resistance ($10\ \Omega \to 20\ \Omega$) in `FGW50XS65C` reduces inductive bus overshoot ($L_\sigma = 25\text{ nH}$) by $38.8\%$ ($+42.36\text{ V} \to +25.94\text{ V}$) at the cost of $+70.5\%$ turn-off energy. Commercial Fuji X-Series models match datasheet $t_{d(\text{off})}$ within $+4.7\%$ to $+5.0\%$.
* **IC Testing & Scan Path (LD4):** Seven optimized vectors cover all 20 unique stuck-at faults (`25% -> 100%`), while stuck-open requires an ordered `0000 -> 0001` pair. A 3-`SDFF` scan chain (`28` MOS/SDFF) reduces 20-bit test latency from `20.9715 ms` to `400 ns`, diagnoses all 4 injected faults in 23 cycles (`0.46 µs`), and proves `32`-fault combinational coverage requires $\ge 5$ vectors.

---

## Technologies

* **SPICE Simulation:** LTspice 24+ (`.cir` batch execution, `.asc` schematics, `.meas` extraction, `.raw` validation; `0.35 µm` CMOS Level-1 in LD4, PTM BSIM4 in LD1–LD2, IGBT macromodels in LD3)
* **Post-Processing & Verification:** Python 3.10+ (`numpy`, `matplotlib`)
* **Typesetting:** LaTeX (`IEEEtran` / `article`)

---

## Repository Structure

```text
MicroNano/
├── README.md                    # Main repository documentation (this file)
├── .gitignore                   # Excludes .raw, .db, .log, ZIPs, previews, caches; keeps .plt
├── LD1_Arcila_Yactayo/          # Lab 1: Static CMOS (Yactayo & Arcila)
├── LD2_Arcila_Yactayo/          # Lab 2: Dynamic & Domino CMOS (Yactayo & Arcila)
├── LD3_Yactayo/                 # Lab 3: IGBT DPT Characterization (Yactayo, Individual)
├── LD4_Arcila_Yactayo/          # Lab 4: IC Testing & Scan Path (Yactayo & Arcila)
│   ├── README.md                # LD4 technical documentation
│   ├── TRAZABILIDAD.md          # Public bijective traceability matrix
│   ├── informe/                 # 3-page technical report (main.tex, main.pdf)
│   ├── HC1/                     # Control Sheet 1 (README.md, main.tex, HC1_LD4.pdf)
│   ├── HC2/                     # Control Sheet 2 (README.md, main.tex, HC2_LD4.pdf)
│   ├── figuras/                 # Schematic, discrete-sample plot, and LTspice captures
│   ├── resultados/              # Curated CSV tables & JSON verification summary
│   ├── simulaciones/README.md   # Simulation setup & excluded dependency guide
│   ├── scripts/                 # Portable verification & plotting scripts
│   └── validacion/README.md     # Public vs. local validation guide
├── _docs/                       # Course roadmap, process protocol & development log
└── AGENTS.md / CLAUDE.md        # AI assistant context guidelines
```

---

## Reproduction Instructions

1. **Install Python dependencies:**
   ```powershell
   pip install -r LD3_Yactayo/requirements.txt
   ```
2. **Set LTspice path (for local SPICE batch scripts):**
   ```powershell
   $env:LTSPICE_EXE = "C:\Program Files\ADI\LTspice\LTspice.exe"
   ```
3. **Download third-party / course dependencies (excluded from public Git):**
   * **LD1 & LD2:** PTM BSIM4 model cards per [`LD2_Arcila_Yactayo/modelos/README_modelos.md`](LD2_Arcila_Yactayo/modelos/README_modelos.md).
   * **LD3:** Fuji Electric and Duncan Amps IGBT models per [`LD3_Yactayo/modelos/NOTAS_MODELOS.md`](LD3_Yactayo/modelos/NOTAS_MODELOS.md).
   * **LD4:** Course `0.35 µm` CMOS library (`cmos035_cells.lib`) and netlists per [`LD4_Arcila_Yactayo/simulaciones/README.md`](LD4_Arcila_Yactayo/simulaciones/README.md).
4. **Run standalone LD4 public validation (no private files required):**
   ```powershell
   python LD4_Arcila_Yactayo/scripts/verificar_ld4.py
   ```
5. **Run individual lab workflows:** See [`LD1_Arcila_Yactayo/README.md`](LD1_Arcila_Yactayo/README.md), [`LD2_Arcila_Yactayo/README.md`](LD2_Arcila_Yactayo/README.md), [`LD3_Yactayo/README.md`](LD3_Yactayo/README.md), and [`LD4_Arcila_Yactayo/README.md`](LD4_Arcila_Yactayo/README.md).

---

## Validation and Limitations

* **LD3 Validation Suite:** [`LD3_Yactayo/validation/README.md`](LD3_Yactayo/validation/README.md) documents `PASS` checks (Tellegen energy balance, timestep convergence), `RESOLVED FAILURE` fixes, and `KNOWN LIMITATION` items (`N/V*` for P-IGBT 19.48 A, exploratory 80 A runs, co-pack reverse-bias invariance).
* **LD4 Validation Suite:** [`LD4_Arcila_Yactayo/validacion/README.md`](LD4_Arcila_Yactayo/validacion/README.md) documents standalone CSV/combinational checks (`32`-fault proof) alongside local `521/521` LOG–RAW verification, `P2_flush_fix2.log` solver stabilization options, and historical figure provenance.
* **Excluded Materials:** Third-party SPICE models (PTM, Duncan, Fuji) and course teaching annexes (`LabDirigidoNro04.pdf`, `cmos035_cells.lib`, `.cir`/`.inc`) are documented for local placement without public redistribution.

---

## References

* Zhao, W., & Cao, Y. (2006). *New Generation of Predictive Technology Model for Sub-45 nm Early Design Exploration*. IEEE TED.
* Fuji Electric Co., Ltd. *Technical Discrete P-Spice Models (X-Series 650 V Trench-FS)*.
* Duncan's Amp Pages. *IGBT Behavioral SPICE Macromodels (`nigbt.lib`, `pigbt.lib`)*.
* Bushnell, M. L., & Agrawal, V. D. (2000). *Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits*. Kluwer/Springer.
