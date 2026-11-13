# LD3 Validation, Resolved Failures, and Known Limitations

This directory documents the numerical verification, diagnostic checks, resolved instrumentation errors, and known technical limitations of **Laboratory Project No. 3 (LD3)** (`LD3_Yactayo/`).

---

## 1. Validation Methodology

Every quantitative metric reported in LD3 was subjected to multi-layer verification:

1. **Terminal Current Decoupling (G4.2-R Protocol):** Ideal 0 V voltage sources (`Vsens_C`, `Vsens_G`, `Vsens_E`) are placed in series with the collector, gate, and emitter terminals of the Fuji Electric IGBT models to isolate pure collector port current $I_C$ from gate displacement currents.
2. **Tellegen / Poynting Energy Balance:** Verified via `scripts/auditoria_g42_fuji.py` (`AS-01` through `AS-07`), checking that net port energy equals the sum of component energies with residual $< 0.5\%$ (observed residual: $-33\text{ pJ}$, $-0.000001\%$).
3. **Timestep & Solver Convergence:** Tested with Gear integration (`method=gear`, `reltol=1e-3`, `abstol=1e-8`) across `maxstep` values of `0.5 ns`, `1.0 ns`, and `5.0 ns`.
4. **Parasitic Loop Damping Isolation:** Evaluated `Lpar = 25 nH` (`Rser = 10 mΩ`) with `Rpar = None`, `200 Ω`, `100 Ω`, and `50 Ω` to ensure no artificial parallel resistor masks inductive overshoot.
5. **Cross-Method Consistency:** SPICE `.meas` directives compared against Python trapezoidal integration and derivative-based tail detection on ASCII `.raw` exports (`< 0.05%` target agreement).

---

## 2. Curated Reproducible Validation Cases (`cases/`)

| Case File | Purpose | Key Observed Metrics (`.log`) | Status |
| :--- | :--- | :--- | :---: |
| `cases/g42_ref_L0_1ns.cir` | Ideal loop baseline ($L_\sigma = 0\text{ nH}$, `maxstep = 1.0 ns`) | $V_{CE,\text{peak}} = 401.33\text{ V}$, $t_{d(\text{off})} = 229.72\text{ ns}$, $E_{C,\text{net}} = 987.37\ \mu\text{J}$ | **PASS** |
| `cases/g42_ref_L25_1ns.cir` | Physical inductive loop baseline ($L_\sigma = 25\text{ nH}$, `Rpar = None`, `1.0 ns`, SPICE default `temp = 27 °C`) | $V_{CE,\text{peak}} = 442.08\text{ V}$, $t_{d(\text{off})} = 234.30\text{ ns}$, $E_{C,\text{net}} = 1089.68\ \mu\text{J}$ | **PASS** |
| `cases/g42_ref_L25_05ns.cir` | Fine-timestep convergence check ($L_\sigma = 25\text{ nH}$, `0.5 ns`, `temp = 27 °C`) | $V_{CE,\text{peak}} = 441.98\text{ V}$, $t_{d(\text{off})} = 234.28\text{ ns}$, $E_{C,\text{net}} = 1089.49\ \mu\text{J}$ ($\Delta V \approx 0.023\%$, $\Delta E \approx 0.017\%$, $\Delta t_d \approx 0.009\%$) | **PASS** |
| `cases/g42_diag_L25_rpar50_1ns.cir` | Diagnostic comparison with artificial damping (`Rpar = 50 Ω`) | $V_{CE,\text{peak}} = 441.14\text{ V}$, $E_{C,\text{net}} = 1088.21\ \mu\text{J}$, $E_{R\text{par}} = 0.758\ \mu\text{J}$ | **PASS** *(Diagnostic)* |
| `cases/val_damp_rpar_None.cir` | Undamped `Lpar` stability check (pre-G4.2) | $V_{CE,\text{peak}} = 442.08\text{ V}$, $E_{\text{off,shunt}} = 1060.41\ \mu\text{J}$ | **PASS** |
| `cases/val_damp_rpar_50.cir` | Damped `Lpar` sensitivity check (`Rpar = 50 Ω`) | $V_{CE,\text{peak}} = 441.14\text{ V}$, $E_{\text{off,shunt}} = 1058.95\ \mu\text{J}$ | **PASS** *(Diagnostic)* |

To run any validation case (after placing the Fuji Electric `.LIB` models as described in [`../modelos/NOTAS_MODELOS.md`](../modelos/NOTAS_MODELOS.md)):

```powershell
& "$env:LTSPICE_EXE" -b -ascii "LD3_Yactayo/validation/cases/g42_ref_L25_1ns.cir"
```

---

## 3. Classification of Tests, Resolved Failures, and Known Limitations

### A. PASS — Verified Experimental & Validation Checks
* **EXP-01 & EXP-02 (Duncan N-IGBT 19 A & P-IGBT 40 A nominal DPT):** Clean switching waveforms, `.meas` extraction, and 300 DPI figures (`fig1`–`fig5`).
* **EXP-06 through EXP-09 (Fuji Electric X-Series `F01`–`F06`):** Full 6-case matrix (`FGW50XS65/C`, `FGW75XS65/C`, $R_G = 10\ \Omega \to 20\ \Omega$) simulated at $V_{bus} = 400\text{ V}$, $L_\sigma = 25\text{ nH}$, $T = 25\ ^\circ\text{C}$, and $R_G = 10\ \Omega$, yielding $t_{d(\text{off})}$ within $+4.7\%$ to $+5.0\%$ of typical datasheet reference values (`231.10 ns` vs. `~220 ns` at 50 A; `293.18 ns` vs. `~280 ns` at 75 A, noting that datasheet test fixtures may differ in $R_G$, $V_{CC}$, and stray inductance).
* **G4.2-R Energy & Convergence Suite:** Tellegen residual $-33\text{ pJ}$ (`-0.000001%`) and sub-$0.025\%$ timestep delta between `0.5 ns` and `1.0 ns` ($\approx 0.023\%$ in $V_{CE,\text{peak}}$, $\approx 0.017\%$ in $E_{C,\text{net}}$, $\approx 0.009\%$ in $t_{d(\text{off})}$).

### B. RESOLVED FAILURE — Errors Identified and Fixed During Development
1. **Emitter Shunt Current Contamination in G4.1 (`validar_piloto_fuji.py`):**
   * *Failure:* Early Fuji pilot runs integrated $V_{CE} \cdot I(R_2)$ across the emitter shunt resistor, mixing gate discharge current $I_G$ into collector turn-off energy (`1058.95 µJ` vs true `1089.68 µJ`).
   * *Resolution:* Replaced shunt sensing with ideal 0 V terminal sensors (`Vsens_C`, `Vsens_G`, `Vsens_E`) in G4.2-R and `fuji_f01.cir`–`fuji_f06.cir`.
2. **Artificial Parallel Damping (`Rpar = 50 Ω`) on Parasitic Loop Inductance:**
   * *Failure:* Preliminary pilot netlists included `Rpar=50` on `Lpar`, which artificially dissipated `0.758 µJ` and damped peak overshoot from `442.08 V` to `441.14 V`.
   * *Resolution:* Removed `Rpar` (`Rpar=None`) in all final `fuji_f01.cir`–`fuji_f06.cir` netlists while retaining Gear convergence.
3. **P-IGBT Freewheeling Diode Polarity & Current Sign (`DPT_PIGBT.asc`):**
   * *Failure:* Preliminary base schematic required freewheeling diode orientation adjustment for negative-bus high-side operation ($V_{bus} = -400\text{ V}$).
   * *Resolution:* Corrected diode polarity (anode to $V_{bus}$, cathode to $V_C$) and aligned current sign conventions in `DPT_PIGBT_nom.asc` and `dpt_pigbt_nom.cir`.

### C. KNOWN LIMITATION — Retained Transparently Without Fabrication
1. **Missing RAW File for P-IGBT 19.48 A Control (`dpt_pigbt_19a.cir` / `.log`) — `N/V*`:**
   * Static and `.meas` integral metrics (`Ic_pre = 19.48 A`, `Vce_on = 1.72 V`, `Eoff = 1011.8 µJ`) are preserved in `dpt_pigbt_19a.log`.
   * Dynamic waveform-derived metrics ($t_{d(\text{off})}$, $t_f$, $I_{C,\text{tail}}$, $\%E_{\text{tail}}$) are explicitly marked **`N/V*`** (Not Verified) in [`../tablas/tabla_resultados_ld3.md`](../tablas/tabla_resultados_ld3.md) and the final PDF report because `dpt_pigbt_19a.raw` is not present on disk.
2. **Exploratory 80 A Overcurrent Runs (`dpt_nigbt.cir`, `dpt_pigbt.cir`):**
   * Using the preliminary `20 µs` pulse drives `82.31 A` (N-IGBT) and `83.22 A` (P-IGBT), exceeding the `IRGBC20S` Safe Operating Area (`IC = 19 A`, `ICM = 76 A`). These are classified strictly as **exploratory / out-of-SOA** numerical stress runs, not nominal operating conditions.
3. **Co-Pack Diode Reverse-Bias Invariance in Single-Switch Low-Side DPT (`EXP-06`, `EXP-07`):**
   * In a low-side DPT, the device's own antiparallel co-pack diode remains reverse-biased ($V_C > V_E$), so its `0.45 nF` capacitance yields negligible turn-off difference (`< 0.01%`) in `Vce_peak` and `Eoff`. Its physical impact appears when acting as the freewheeling diode in half-bridge topologies.
4. **Duncan Behavioral Macromodel vs. IRGBC20S Datasheet:**
   * `XIRGBC20S` (`T_F = 16.8 ns`, tested at $R_G = 10\ \Omega$, $400\text{ V}$) switches significantly faster ($t_{d(\text{off})} = 150.83\text{ ns}$) than the physical Standard Speed IRGBC20S datasheet ($820\text{ ns}$ at $R_G = 50\ \Omega$, $480\text{ V}$).
5. **Cross-Family Instrumentation & Temperature Differences:**
   * Duncan (`EXP-01`–`05`) used emitter shunt `R2`, $L_\sigma = 0\text{ nH}$, $27\ ^\circ\text{C}$, and derivative-based tail detection ($|dI_C/dt| \le 5\% |dI/dt|_{\max}$). Fuji (`EXP-06`–`09`) used `Vsens_C`, $L_\sigma = 25\text{ nH}$, explicit `.temp 25.0` ($25\ ^\circ\text{C}$), and $0.05 \cdot I_{C,\text{pre}}$ tail threshold.
   * **Note on `fuji_f01.cir` ($1066.98\ \mu\text{J}$) vs. `g42_ref_L25_1ns.cir` ($1089.68\ \mu\text{J}$):** Both simulate `FGW50XS65` at $50\text{ A}$, $400\text{ V}$, $L_\sigma = 25\text{ nH}$; however, `g42_ref_L25_1ns.cir` (methodological G4.2-R pilot) ran at SPICE default `temp = 27 °C`, whereas `fuji_f01.cir` (final `EXP-06` suite) enforces `.temp 25.0` ($25\ ^\circ\text{C}$). Quantitative comparisons should be made within each family and temperature condition.
