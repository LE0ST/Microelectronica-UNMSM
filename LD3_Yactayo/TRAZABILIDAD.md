# Experimental Traceability Matrix: LD3 (IGBT Transistors in LTspice)

**Universidad Nacional Mayor de San Marcos** — Faculty of Electrical and Electronic Engineering (FIEE)<br>
**Course:** Microelectronics and Nanoelectronic Systems (2026-II)<br>
**Author:** Leonardo Sait Yactayo Tolentino (Code: `23190214`) — *Individual Work*<br>
**Tools:** LTspice 24 | Python 3.14<br>
**Official Guide:** `Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf` *(local teaching document, excluded from the public repository for licensing)*<br>
**Presentation Date:** October 21, 2026

---

## 1. Summary Matrix of Official Requirements and Experiments

| Exp. ID | Official Guide Requirement | Device / Model | Schematic `.asc` | Netlist `.cir` | Status | Verification |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **EXP-01** | N-IGBT DPT Bench (Low-Side, $0\to 15\text{ V}$), $V_{GE}, V_{CE}, I_C$ waveforms | NIGBT (`XIRGBC20S`, 600 V, 19 A) | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDATED** | Fig. 1 generated (300 DPI) |
| **EXP-02** | P-IGBT DPT Bench (High-Side, $0\to -15\text{ V}$), $V_{GE}, V_{CE}, I_C$ waveforms | PIGBT (`XPIGBT`, 600 V, 40 A) | `esquemas/DPT_PIGBT_nom.asc` | `simulaciones/netlists/dpt_pigbt_nom.cir` | **VALIDATED** | Fig. 2 generated (300 DPI) |
| **EXP-03** | Tail Current extraction during 2nd turn-off pulse | N-IGBT vs. P-IGBT | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDATED** | Fig. 3 generated ($I_{tail}$ detected) |
| **EXP-04** | Turn-off delay $t_{d(\text{off})}$ (90% $V_{GE} \to$ 90% $I_C$) and datasheet comparison | N-IGBT vs. P-IGBT | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDATED** | Fig. 4 generated (90%-to-90% cursors) |
| **EXP-05** | Turn-off energy $E_{\text{off}} = \int V_{CE} I_C dt$ and % due to tail current | N-IGBT vs. P-IGBT | `esquemas/DPT_NIGBT_nom.asc` | `simulaciones/netlists/dpt_nigbt_nom.cir` | **VALIDATED** | Fig. 5 generated ($E_{off}$ and $E_{tail}$) |
| **EXP-06** | Stray-inductance overshoot $V_{CE,\text{peak}}$: with vs. without co-pack diode (50 A) | `FGW50XS65` vs. `FGW50XS65C` | — *(netlist `.cir`)* | `simulaciones/netlists/fuji_f01.cir`, `simulaciones/netlists/fuji_f02.cir` | **VALIDATED** | Fig. 6 generated (50 A overshoot) |
| **EXP-07** | Stray-inductance overshoot $V_{CE,\text{peak}}$: with vs. without co-pack diode (75 A) | `FGW75XS65` vs. `FGW75XS65C` | — *(netlist `.cir`)* | `simulaciones/netlists/fuji_f03.cir`, `simulaciones/netlists/fuji_f04.cir` | **VALIDATED** | Fig. 7 generated (75 A overshoot) |
| **EXP-08** | Silicon area scaling (50 A vs. 75 A): static and dynamic losses | `FGW50XS65` vs. `FGW75XS65` | — *(netlist `.cir`)* | `simulaciones/netlists/fuji_f01.cir`, `simulaciones/netlists/fuji_f05.cir`, `simulaciones/netlists/fuji_f03.cir` | **VALIDATED** | Fig. 8 generated (50 A vs. 75 A area) |
| **EXP-09** | $R_G$ sensitivity: impact of doubling $R_G$ ($10\ \Omega \to 20\ \Omega$) on delay and $E_{\text{off}}$ | `FGW50XS65C` | — *(netlist `.cir`)* | `simulaciones/netlists/fuji_f02.cir`, `simulaciones/netlists/fuji_f06.cir` | **VALIDATED** | Fig. 9 generated ($R_G$ sensitivity) |
| **REQ-TAB**| Consolidated Master Results Table | All evaluated models | — | `tablas/tabla_resultados_ld3.md` | **VALIDATED** | Tables 1 & 2 in landscape PDF |
| **REQ-CON**| Physics-grounded Technical Conclusions ($\ge 1$ physical page) | N vs. P, area, and diode analysis | — | `informe/conclusiones.md` | **VALIDATED** | Comprehensive conclusions |
| **REQ-EXP**| Oral Presentation of Key Findings (21/10/2026) | Individual presentation | — | `informe/exposicion_21oct.md` | **VALIDATED** | Delivered Oct 21, 2026 |

---

## 2. Detailed Requirement and Experiment Records

### `[EXP-01]` — N-IGBT Double Pulse Test Bench (Low-Side)
* **Official Guide Requirement:** Section 5.1, Item 1. Configure N-IGBT schematic with emitter grounded through test resistor $R = 0.001\ \Omega$. Load inductor in series with high $V_{DC}$ connected to collector and parallel freewheeling diode. Gate drive in series with $R_G$ in PULSE mode ($0\to 15\text{ V}$).
* **Model Used:** `XIRGBC20S` in `nigbt.lib` (Duncan Electronics / IR, 600 V, 19 A).
* **Model Source:** `modelos/nigbt.lib` *(local third-party dependency excluded from the public repository; see [`modelos/NOTAS_MODELOS.md`](modelos/NOTAS_MODELOS.md))*.
* **Experimental Conditions:**
  * DC bus voltage: $V_{DC} = 400\text{ V}$
  * Load inductor: $L = 100\ \mu\text{H}$ ($R_{ser} = 1\text{ m}\Omega$)
  * Gate resistance: $R_G = 10\ \Omega$ (guide nominal)
  * Emitter sensing resistor: $R_E = 0.001\ \Omega$
  * Freewheeling diode: Fast diode in parallel with inductor ($DMOD$)
  * Calibrated nominal pulse profile: 1st pulse $t_{p1} = 3.65\ \mu\text{s}$, dead time $5.0\ \mu\text{s}$, 2nd pulse $t_{p2} = 1.0\ \mu\text{s}$.
* **Assigned Files:**
  * Nominal Schematic: `LD3_Yactayo/esquemas/DPT_NIGBT_nom.asc`
  * Nominal Netlist: `LD3_Yactayo/simulaciones/netlists/dpt_nigbt_nom.cir`
  * Historical 80 A Schematic: `LD3_Yactayo/esquemas/DPT_NIGBT.asc`
  * Historical 80 A Netlist: `LD3_Yactayo/simulaciones/netlists/dpt_nigbt.cir`
* **Observed Numerical Data (Nominal $19\text{ A}$ Condition):**
  * $I_{C,\text{on}} = 19.00\text{ A}$ (at 2nd turn-off; error $+0.02\%$)
  * $V_{CE,\text{on}} = 1.88\text{ V}$ (static saturation conduction)
  * $V_{CE,\text{peak}} = 400.99\text{ V}$ (clamped by freewheeling diode $D_1$)
  * $V_{GE,\text{peak}} = +18.63\text{ V}$ (Miller-induced gate overshoot)
* **Associated Figure:** [`figuras/fig1_dpt_nigbt_transitorios.png`](figuras/fig1_dpt_nigbt_transitorios.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-02]` — P-IGBT Double Pulse Test Bench (High-Side)
* **Official Guide Requirement:** Section 5.1, Item 2. Configure P-IGBT in high-side topology. Gate drive $V_{GE}$ between gate (with $R_G$) and emitter, with levels $0\text{ V}$ (off) to $-15\text{ V}$ (on).
* **Model Used:** `XPIGBT` in `pigbt.lib` (Duncan Electronics, 600 V, 40 A).
* **Model Source:** `modelos/pigbt.lib` *(local third-party dependency excluded from the public repository; see [`modelos/NOTAS_MODELOS.md`](modelos/NOTAS_MODELOS.md))*.
* **Experimental Conditions:**
  * Negative bus voltage: $V_{bus} = -400\text{ V}$ (referenced to grounded emitter)
  * Load inductor: $L = 100\ \mu\text{H}$ ($R_{ser} = 1\text{ m}\Omega$)
  * Gate resistance: $R_G = 10\ \Omega$
  * Freewheeling diode: Anode to $V_{bus}$, cathode to $VC$ (corrected vs. original instructor schematic)
  * Calibrated nominal pulse profile: 1st pulse $t_{p1} = 8.88\ \mu\text{s}$, dead time $5.0\ \mu\text{s}$, 2nd pulse $t_{p2} = 1.0\ \mu\text{s}$.
* **Assigned Files:**
  * Nominal Schematic: `LD3_Yactayo/esquemas/DPT_PIGBT_nom.asc`
  * Nominal Netlist: `LD3_Yactayo/simulaciones/netlists/dpt_pigbt_nom.cir`
  * Historical 80 A Schematic: `LD3_Yactayo/esquemas/DPT_PIGBT.asc`
  * Historical 80 A Netlist: `LD3_Yactayo/simulaciones/netlists/dpt_pigbt.cir`
* **Observed Numerical Data (Nominal $40\text{ A}$ Condition):**
  * $I_{C,\text{on}} = 40.02\text{ A}$ (magnitude at 2nd turn-off; error $+0.03\%$)
  * $V_{CE,\text{on}} = -2.51\text{ V}$ ($V_{EC} = +2.51\text{ V}$ in conduction)
  * $V_{CE,\text{peak}} = -401.22\text{ V}$ ($V_{EC} = +401.22\text{ V}$ peak)
  * $V_{GE,\text{peak}} = -17.47\text{ V}$ (Miller overshoot)
  * *Verified sign convention:* $I(L1)$ flows from Collector to $V_{bus}$, positive ($+80.56\text{ A}$ at 80 A; $+40.02\text{ A}$ at nominal).
* **Associated Figure:** [`figuras/fig2_dpt_pigbt_transitorios.png`](figuras/fig2_dpt_pigbt_transitorios.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-03]` — Tail Current Characterization
* **Official Guide Requirement:** Section 5.1, Item 4.2. Zoom into the second turn-off pulse to determine $I_C$ at the exact onset of the asymptotic tail phase. Physical justification based on semiconductor device physics.
* **Evaluated Models:** `XIRGBC20S` (N-channel, 19 A) vs. `XPIGBT` (P-channel, 40 A).
* **Detection Method:** Analytical inflection detection where $|dI_C/dt|$ drops to 5% of its maximum slope (MOS channel extinction and transition to bipolar recombination in the $N^-$ drift base).
* **Observed Numerical Data:**
  * **N-IGBT ($19\text{ A}$):** $t_{\text{tail}} = 20.258\ \mu\text{s}$, $I_{C,\text{tail}} = 0.94\text{ A}$ ($4.93\%$ of $I_{C,\text{on}}$).
  * **N-IGBT ($80\text{ A}$, exploratory):** $t_{\text{tail}} = 36.340\ \mu\text{s}$, $I_{C,\text{tail}} = 2.65\text{ A}$ ($3.22\%$ of $I_{C,\text{on}}$).
  * **P-IGBT ($40\text{ A}$):** $t_{\text{tail}} = 25.655\ \mu\text{s}$, $I_{C,\text{tail}} = 1.81\text{ A}$ ($4.53\%$ of $I_{C,\text{on}}$).
  * **P-IGBT ($80\text{ A}$, exploratory):** $t_{\text{tail}} = 36.510\ \mu\text{s}$, $I_{C,\text{tail}} = 3.88\text{ A}$ ($4.66\%$ of $I_{C,\text{on}}$).
* **Note on P-IGBT $19.48\text{ A}$ Control (`dpt_pigbt_19a.cir`):** Static/integral `.meas` metrics (`Ic_pre = 19.48 A`, `Vce_on = 1.72 V`, `Eoff = 1011.8 µJ`) are preserved from `.log`; waveform-derived dynamic metrics ($t_{d(\text{off})}, t_f, I_{C,\text{tail}}, \%E_{\text{tail}}$) remain marked **`N/V*`** in [`tablas/tabla_resultados_ld3.md`](tablas/tabla_resultados_ld3.md) because `dpt_pigbt_19a.raw` is not present on disk.
* **Associated Figure:** [`figuras/fig3_detalle_corriente_cola.png`](figuras/fig3_detalle_corriente_cola.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-04]` — Turn-Off Delay $t_{d(\text{off})}$ and Datasheet Comparison
* **Official Guide Requirement:** Section 5.1, Item 4.3. Measure the interval between 90% $V_{GE}$ and 90% $I_C$. Compare against manufacturer datasheets and justify discrepancies.
* **Evaluated Models:** `XIRGBC20S` (N-channel) vs. `XPIGBT` (P-channel).
* **Rigorous Definition:**
  * N-IGBT: Trigger at $V_{GE} = 13.5\text{ V}$ (falling); target at $I_C = 0.90 \times 19.00\text{ A} = 17.10\text{ A}$.
  * P-IGBT: Trigger at $V_{GE} = -13.5\text{ V}$ (rising toward $0\text{ V}$); target at $|I_C| = 0.90 \times 40.02\text{ A} = 36.02\text{ A}$.
* **Observed Numerical Data:**
  * **N-IGBT Nominal ($19\text{ A}$):** $t_{d(\text{off})} = 150.83\text{ ns}$ (SPICE) / $152.2\text{ ns}$ (Python); $t_f = 185.24\text{ ns}$; $t_{\text{off}} = 336.07\text{ ns}$.
  * **N-IGBT Overload ($80\text{ A}$, exploratory):** $t_{d(\text{off})} = 103.32\text{ ns}$; $t_f = 196.03\text{ ns}$; $t_{\text{off}} = 299.35\text{ ns}$.
  * **P-IGBT Nominal ($40\text{ A}$):** $t_{d(\text{off})} = 194.57\text{ ns}$ (SPICE) / $194.8\text{ ns}$ (Python); $t_f = 268.42\text{ ns}$; $t_{\text{off}} = 463.00\text{ ns}$.
  * **P-IGBT Overload ($80\text{ A}$, exploratory):** $t_{d(\text{off})} = 172.32\text{ ns}$; $t_f = 275.03\text{ ns}$; $t_{\text{off}} = 447.36\text{ ns}$.
* **Comparison vs. IRGBC20S Datasheet (Farnell 68617):**
  * *IR Catalog Values ($V_{CC}=480\text{ V}, I_C=10\text{ A}, R_G=50\ \Omega, T_j=25^\circ\text{C}$):*
    * Typical $V_{CE(\text{on})}$: $1.8\text{ V}$ (at $10\text{ A}$); $2.4\text{ V}$ (at $19\text{ A}$).
    * Typical $t_{d(\text{off})}$: $820\text{ ns}$ (max. $1000\text{ ns}$).
    * Typical $t_f$: $910\text{ ns}$ (max. $1500\text{ ns}$).
    * Typical $E_{\text{off}}$: $3.9\text{ mJ}$ ($3900\ \mu\text{J}$).
  * *Duncan Macromodel Simulation (`XIRGBC20S`, $V_{bus}=400\text{ V}, I_C=19\text{ A}, R_G=10\ \Omega$):*
    * $V_{CE(\text{on})} = 1.88\text{ V}$ (at $19\text{ A}$; underestimates catalog $2.4\text{ V}$).
    * $t_{d(\text{off})} = 150.83\text{ ns}$ (SPICE) / $152.2\text{ ns}$ (Python).
    * $t_f = 185.24\text{ ns}$.
    * $E_{\text{off}} = 0.691\text{ mJ}$ ($691.5\ \mu\text{J}$).
  * *Physical Justification of Discrepancies:*
    * The physical IRGBC20S is a slow *Standard Speed* device ($\le 1\text{ kHz}$) specified at higher gate resistance ($R_G = 50\ \Omega$) and bus voltage ($480\text{ V}$).
    * The Duncan Electronics behavioral macromodel (`nigbt.lib`, 1995) uses a fast BJT transit time $T_F = 16.8\text{ ns}$.
    * The lower test $R_G$ ($10\ \Omega$ vs. $50\ \Omega$) substantially accelerates gate capacitance discharge.
* **Associated Figure:** [`figuras/fig4_medicion_cursores_tdoff.png`](figuras/fig4_medicion_cursores_tdoff.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-05]` — Turn-Off Energy $E_{\text{off}}$ and Tail Fraction
* **Official Guide Requirement:** Section 5.1, Item 4.4. Compute $E_{\text{off}} = \int V_{CE} \cdot I_C dt$ during turn-off and percentage attributable to tail current.
* **Window Criterion:** Integration starts strictly at the gate turn-off command ($t_{\text{off2}}$) to isolate switching losses without accumulating prior static conduction.
* **Observed Numerical Data:**
  * **N-IGBT Nominal ($19\text{ A}$):** $E_{\text{off}} = 691.5\ \mu\text{J}$ ($0.6915\text{ mJ}$); $E_{\text{tail}} = 32.7\ \mu\text{J}$; $\%E_{\text{tail}} = 4.73\%$.
  * **N-IGBT Overload ($80\text{ A}$, exploratory):** $E_{\text{off}} = 3402.5\ \mu\text{J}$ ($3.4025\text{ mJ}$); $E_{\text{tail}} = 76.5\ \mu\text{J}$; $\%E_{\text{tail}} = 2.25\%$.
  * **P-IGBT Nominal ($40\text{ A}$):** $E_{\text{off}} = 2115.3\ \mu\text{J}$ ($2.1153\text{ mJ}$); $E_{\text{tail}} = 91.6\ \mu\text{J}$; $\%E_{\text{tail}} = 4.33\%$.
  * **P-IGBT Overload ($80\text{ A}$, exploratory):** $E_{\text{off}} = 4698.9\ \mu\text{J}$ ($4.6989\text{ mJ}$); $E_{\text{tail}} = 140.5\ \mu\text{J}$; $\%E_{\text{tail}} = 2.99\%$.
* **Associated Figure:** [`figuras/fig5_potencia_energia_apagado.png`](figuras/fig5_potencia_energia_apagado.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[PILOTO-FUJI-50A]` — Methodological and Energy Validation (G4.2-R)
* **Methodological Requirement:** Experimental baseline for Fuji Electric X-Series models. Decouple collector port current $I_C$, eliminate emitter-shunt gate-current distortion, and close the Tellegen/Poynting energy balance.
* **Evaluated Model:** `FGW50XS65` (Fuji Electric X-Series, discrete without co-packaged diode).
* **DPT Bench Conditions:** $V_{bus} = 400\text{ V}$, $I_C \approx 50\text{ A}$ ($t_{p1} = 11.54\ \mu\text{s}$), $R_G = 10\ \Omega$, $V_{GE} = 15\text{ V} / 0\text{ V}$, $\text{temp} = 27\ ^\circ\text{C}$ (effective SPICE default), $\text{maxstep} = 1.0\text{ ns}$ (Gear).
* **Curated Reproducible Netlists (`validation/cases/`):**
  * [`validation/cases/g42_ref_L0_1ns.cir`](validation/cases/g42_ref_L0_1ns.cir) — Ideal reference $L_\sigma = 0\text{ nH}$.
  * [`validation/cases/g42_ref_L25_1ns.cir`](validation/cases/g42_ref_L25_1ns.cir) — Physical inductive reference $L_\sigma = 25\text{ nH}$ (no $R_{\text{par}}$).
  * [`validation/cases/g42_diag_L25_rpar50_1ns.cir`](validation/cases/g42_diag_L25_rpar50_1ns.cir) — Diagnostic variant ($R_{\text{par}} = 50\ \Omega$).
  * [`validation/cases/g42_ref_L25_05ns.cir`](validation/cases/g42_ref_L25_05ns.cir) — Timestep convergence check at $0.5\text{ ns}$ *(note: `g42_ref_L0_05ns.cir` and `.log`/`.raw` outputs are local historical evidence excluded from the public tree by `.gitignore`)*.
* **Automated Validation Script:** [`scripts/auditoria_g42_fuji.py`](scripts/auditoria_g42_fuji.py).
* **Validated Quantitative Metrics (Window $[27.740\ \mu\text{s}, 32.840\ \mu\text{s}]$):**
  * **Ref. 1 ($L_0$):** $V_{CE,\text{on}} = 1.365\text{ V}$, $V_{CE,\text{peak}} = 401.33\text{ V}$, $t_f = 35.19\text{ ns}$, $E_{C,\text{net}} = 987.37\ \mu\text{J}$, Tellegen residual: $-34\text{ pJ}$ ($-0.000001\%$).
    * *$t_{d(\text{off})}$ (SPICE `.meas`, $I_{C,\text{pre}} = 50.006\text{ A}$ at $27.690\ \mu\text{s}$, $V_{GE} = 13.5\text{ V}$):* **$229.72\text{ ns}$**.
    * *$t_{d(\text{off})}$ (Python `compute_delay_python`, $I_{C,\text{pre}} = 50.044\text{ A}$ at $27.700\ \mu\text{s}$, $0.90 \cdot V_{GE,\text{pre}} = 13.44\text{ V}$):* **$228.67\text{ ns}$**.
  * **Ref. 2 ($L_{25}$, no $R_{\text{par}}$):** $V_{CE,\text{on}} = 1.364\text{ V}$, $V_{CE,\text{peak}} = 442.08\text{ V}$ ($+42.08\text{ V}$ overshoot above bus), $t_f = 31.44\text{ ns}$, $E_{C,\text{net}} = 1089.68\ \mu\text{J}$, Tellegen residual: $-33\text{ pJ}$ ($-0.000001\%$).
    * *$t_{d(\text{off})}$ (SPICE `.meas`, $I_{C,\text{pre}} = 49.970\text{ A}$ at $27.690\ \mu\text{s}$, $V_{GE} = 13.5\text{ V}$):* **$234.30\text{ ns}$**.
    * *$t_{d(\text{off})}$ (Python `compute_delay_python`, $I_{C,\text{pre}} = 50.009\text{ A}$ at $27.700\ \mu\text{s}$, $0.90 \cdot V_{GE,\text{pre}} = 13.44\text{ V}$):* **$233.24\text{ ns}$**.
  * **Diagnostic Variant ($L_{25}, R_{\text{par}}=50\ \Omega$):** $V_{CE,\text{peak}} = 441.14\text{ V}$, $t_{d(\text{off})} = 232.98\text{ ns}$ *(Python criterion, as in the L0/L25 Python values above)* / $234.04\text{ ns}$ *(SPICE `.meas`, from local `g42_diag_L25_rpar50_1ns.log`)*, $E_{C,\text{net}} = 1088.21\ \mu\text{J}$, $E_{Rpar} = 0.758\ \mu\text{J}$ ($0.070\%$ of $E_C$).
* **Assertions Passed:** `AS-01` through `AS-07` at 100% (zero double counting, exact component sum, residual $< 0.5\%$, Python vs. SPICE agreement $< 0.05\%$).
* **Prior Runs Status:** G4.1 exploratory runs classified as **HISTORICAL** (superseded by G4.2-R after fixing collector port sensing and $R_G$ polarity).
* **Status:** **VALIDATED WITH LIMITATIONS (G4.2-R Baseline)**

---

### `[EXP-06]` — Overshoot $V_{CE,\text{peak}}$ and Co-Pack Diode (50 A Module)
* **Official Guide Requirement:** Section 5.1, Item 4.5. Stray-inductance overshoot comparing models with and without integrated freewheeling diode.
* **Evaluated Models:** `FGW50XS65` (`F01`, discrete) vs. `FGW50XS65C` (`F02`, co-pack with diode `DFGW50XS65C_sp`).
* **Conditions:** $V_{bus} = 400\text{ V}$, $I_C = 50.0\text{ A}$, $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$, $T = 25\ ^\circ\text{C}$.
* **Observed Numerical Data:**
  * **F01 (Discrete):** $V_{CE(\text{on})} = 1.362\text{ V}$, $V_{CE,\text{peak}} = 442.36\text{ V}$ ($+42.36\text{ V}$ vs. bus), $t_{d(\text{off})} = 231.10\text{ ns}$, $t_f = 31.38\text{ ns}$, $di/dt_{\text{max}} = 1669.5\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 1066.98\ \mu\text{J}$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
  * **F02 (Co-Pack):** $V_{CE(\text{on})} = 1.362\text{ V}$, $V_{CE,\text{peak}} = 442.36\text{ V}$ ($+42.36\text{ V}$ vs. bus), $t_{d(\text{off})} = 231.09\text{ ns}$, $t_f = 31.38\text{ ns}$, $di/dt_{\text{max}} = 1669.6\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 1066.98\ \mu\text{J}$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
* **Physical Finding:** In a low-side switch, the co-pack diode remains reverse-biased ($V_C > V_E$) with zero forward current; its parasitic capacitance ($0.45\text{ nF}$) causes no measurable change in inductive overshoot or turn-off losses.
* **Associated Figure:** [`figuras/fig6_sobretension_copack_50a.png`](figuras/fig6_sobretension_copack_50a.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-07]` — Overshoot $V_{CE,\text{peak}}$ and Co-Pack Diode (75 A Module)
* **Official Guide Requirement:** Section 5.1, Item 4.5. Stray-inductance overshoot for the 75 A series.
* **Evaluated Models:** `FGW75XS65` (`F03`, discrete) vs. `FGW75XS65C` (`F04`, co-pack with diode `DFGW75XS65C_sp`).
* **Conditions:** $V_{bus} = 400\text{ V}$, $I_C = 75.0\text{ A}$ ($t_{p1} = 17.84\ \mu\text{s}$), $R_G = 10\ \Omega$, $L_\sigma = 25\text{ nH}$, $T = 25\ ^\circ\text{C}$.
* **Observed Numerical Data:**
  * **F03 (Discrete):** $I_{C,\text{pre}} = 75.230\text{ A}$, $V_{CE(\text{on})} = 1.356\text{ V}$, $V_{CE,\text{peak}} = 445.98\text{ V}$ ($+45.98\text{ V}$ vs. bus), $t_{d(\text{off})} = 293.18\text{ ns}$, $t_f = 40.48\text{ ns}$, $di/dt_{\text{max}} = 1818.0\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 2052.75\ \mu\text{J}$, $E_{\text{tail}} = 7.56\ \mu\text{J}$ ($0.37\%$).
  * **F04 (Co-Pack):** $I_{C,\text{pre}} = 75.233\text{ A}$, $V_{CE(\text{on})} = 1.356\text{ V}$, $V_{CE,\text{peak}} = 445.98\text{ V}$ ($+45.98\text{ V}$ vs. bus), $t_{d(\text{off})} = 293.16\text{ ns}$, $t_f = 40.48\text{ ns}$, $di/dt_{\text{max}} = 1818.4\text{ A}/\mu\text{s}$, $E_{C,\text{net}} = 2052.74\ \mu\text{J}$, $E_{\text{tail}} = 7.57\ \mu\text{J}$ ($0.37\%$).
* **Physical Finding:** Identical behavior confirmed in the 75 A series: the antiparallel diode does not affect turn-off losses of the active switch itself.
* **Associated Figure:** [`figuras/fig7_sobretension_copack_75a.png`](figuras/fig7_sobretension_copack_75a.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-08]` — Silicon Area Scaling (50 A vs. 75 A)
* **Official Guide Requirement:** Section 6 (Conclusions). Justify physically how larger silicon area impacts conduction and switching losses.
* **Evaluated Models:** `FGW50XS65` (`F01`) vs. `FGW75XS65` at 50 A (`F05`) and at nominal 75 A (`F03`).
* **Observed Numerical Data:**
  * **At matched current (constant $50\text{ A}$, `F01` vs. `F05`):**
    * Larger area reduces $V_{CE(\text{on})}$ from $1.362\text{ V}$ to **$1.181\text{ V}$** ($-181\text{ mV}$, $-13.3\%$ conduction loss).
    * Larger capacitance ($C_{ies} = 9.5\text{ nF}$ vs. $6.77\text{ nF}$) increases $t_{d(\text{off})}$ from $231.10\text{ ns}$ to **$324.75\text{ ns}$** ($+40.5\%$) and $E_{C,\text{net}}$ from $1066.98\ \mu\text{J}$ to **$1367.85\ \mu\text{J}$** ($+28.2\%$).
    * Lower $di/dt_{\text{max}}$ ($1429.8$ vs. $1669.5\text{ A}/\mu\text{s}$) reduces peak overshoot from $442.36\text{ V}$ to **$436.37\text{ V}$** ($+36.37\text{ V}$ above bus).
  * **At nominal current ($50\text{ A}$ vs. $75\text{ A}$, `F01` vs. `F03`):**
    * Similar conduction drop ($1.362\text{ V}$ vs. $1.356\text{ V}$).
    * $E_{\text{off}}$ nearly doubles from $1066.98\ \mu\text{J}$ to **$2052.75\ \mu\text{J}$** ($+92.4\%$) due to switching $50\%$ more current with a longer BJT transit time ($TF = 3.0\text{ ns}$ vs. $0.1\text{ ns}$).
* **Associated Figure:** [`figuras/fig8_comparativa_area_50vs75.png`](figuras/fig8_comparativa_area_50vs75.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[EXP-09]` — Gate Resistance $R_G$ Sensitivity
* **Official Guide Requirement:** Section 5.1, Item 4.6. Relationship between $R_G$ and $t_{d(\text{off})}$; impact of doubling $R_G$ ($10\ \Omega \to 20\ \Omega$) on switching losses and speed.
* **Evaluated Model:** `FGW50XS65C` ($50\text{ A}$, $400\text{ V}$): `F02` ($R_G = 10\ \Omega$) vs. `F06` ($R_G = 20\ \Omega$).
* **Observed Numerical Data:**
  * **$R_G = 10\ \Omega$ (`F02`):** $t_{d(\text{off})} = 231.09\text{ ns}$, $t_f = 31.38\text{ ns}$, $di/dt_{\text{max}} = 1669.6\text{ A}/\mu\text{s}$, $V_{CE,\text{peak}} = 442.36\text{ V}$ ($+42.36\text{ V}$ overshoot), $E_{C,\text{net}} = 1066.98\ \mu\text{J}$.
  * **$R_G = 20\ \Omega$ (`F06`):** $t_{d(\text{off})} = 361.60\text{ ns}$ ($+56.5\%$), $t_f = 57.27\text{ ns}$ ($+82.5\%$), $di/dt_{\text{max}} = 1019.4\text{ A}/\mu\text{s}$ ($-38.9\%$), $V_{CE,\text{peak}} = 425.94\text{ V}$ ($+25.94\text{ V}$ overshoot, $-38.8\%$ reduction), $E_{C,\text{net}} = 1818.73\ \mu\text{J}$ ($+70.5\%$).
* **Key Physical Trade-Off:** Doubling $R_G$ strongly mitigates inductive overshoot stress ($-16.4\text{ V}$ absolute peak, $-38.8\%$ bus overshoot), at the cost of a severe $+70.5\%$ penalty in turn-off energy dissipation.
* **Associated Figure:** [`figuras/fig9_sensibilidad_rg_conmutacion.png`](figuras/fig9_sensibilidad_rg_conmutacion.png) (300 DPI)
* **Status:** **VALIDATED**

---

### `[REQ-TAB]` — Consolidated Master Results Table
* **Official Guide Requirement:** Section 1 ("The main deliverable of this laboratory consists of the complete results table and comparative plots.").
* **Table Contents:** 11 unique conditions without duplicates (2 N-IGBT, 3 P-IGBT, and 6 Fuji Electric X-Series).
* **Target File:** [`tablas/tabla_resultados_ld3.md`](tablas/tabla_resultados_ld3.md).
* **Status:** **VALIDATED**

---

### `[REQ-CON]` — Physics-Grounded Technical Conclusions
* **Official Guide Requirement:** Section 6. Technical analysis of **at least one page** discussing fundamental N vs. P channel differences, co-packaged diode impact, and silicon area scaling (50 A vs. 75 A).
* **Physics Covered:**
  1. Electron vs. hole mobility asymmetry ($\mu_n \approx 3.1 \mu_p$) and its effect on capacitances, delay ($+40.7\%$), and losses ($+46.3\%$).
  2. Conductivity modulation in the $N^-$ drift base and floating-base recombination dynamics (origin of tail current).
  3. Permanent reverse bias of the co-pack diode in a low-side DPT switch vs. its freewheeling role in half-bridge inverters.
  4. Silicon area scaling: $-13.3\%$ $V_{CE(\text{on})}$ reduction at the expense of $+28.2\%$ higher $E_{\text{off}}$ from larger parasitic capacitances.
  5. $R_G$ trade-off: $-38.8\%$ inductive overshoot mitigation vs. $+70.5\%$ turn-off energy penalty.
* **Associated Files:** [`informe/conclusiones.md`](informe/conclusiones.md) and Section 7 of [`informe/informe_ld3_yactayo.md`](informe/informe_ld3_yactayo.md).
* **Status:** **VALIDATED**

---

### `[REQ-EXP]` — Oral Presentation of Key Findings
* **Official Guide Requirement:** Section 1 ("On October 21, a brief oral presentation of the main laboratory findings will be held for grading.").
* **Scheduled Date:** **October 21, 2026**.
* **Modality:** Individual (Leonardo Sait Yactayo Tolentino).
* **Prepared Support Deliverables:** Slide-by-slide technical script and defense Q&A bank in [`informe/exposicion_21oct.md`](informe/exposicion_21oct.md), and final slides in [`presentacion/LD3_IGBT_Yactayo.pdf`](presentacion/LD3_IGBT_Yactayo.pdf).
* **Status:** **VALIDATED / DELIVERED (Oral presentation Oct 21, 2026)**
