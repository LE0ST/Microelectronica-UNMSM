# LD4 Validation Scope and Reproducibility Guide

**Module:** [`LD4_Arcila_Yactayo/`](../README.md)<br>
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)

---

## 1. Public vs. Local Validation Scope

Because the course SPICE library (`cmos035_cells.lib`), netlists (`.cir`, `.inc`), and raw simulation logs/waveforms (`.log`, `.raw`) are excluded from public redistribution, validation is split into two transparent layers in [`../scripts/verificar_ld4.py`](../scripts/verificar_ld4.py):

* **Python Dependencies:**
  * **Public validation:** Python standard library only (no third-party packages required; verified with `python -S`).
  * **Local LOG–RAW forensic validation:** `numpy` (lazily imported in forensic mode) and local excluded simulation files.
  * **Figure regeneration (`../scripts/generar_figuras_ld4.py`):** `matplotlib`.

### A. Standalone Public Checks (No Private Files Required)
Run directly from a clean Git clone:
```powershell
python LD4_Arcila_Yactayo/scripts/verificar_ld4.py
```
Verifies:
1. **Logical & Coverage Verification:** Recomputes Part I 16-vector healthy sequence (`1000111011111111`), all `140/140` cells of the fault dictionary from the 10-node gate netlist, unique cumulative coverage (`25% -> 100%` without double-counting `10/s-a-0`), and `T0(0000)->T1(0001)` stuck-open pair against [`../resultados/`](../resultados/).
2. **Sequential & Scan Matrices:** Recomputes and validates all `25/25` official (`V4=001/1`) and `25/25` alternative `ensayo_26` (`V4=101/1`) responses (including first detectors `F1->V3, F2->V4, F3->V2, F4->V1`), plus Part II functional (`Z=1` at `k=7`) and flush (`3`-cycle latency) tables.
3. **Numerical Test-Time Equations:** Exact $N = n + (n+1)m$ and $T = N \cdot T_{CLK}$ checks at $50\text{ MHz}$ (`0.46`, `1.34`, `330.64`, `90.16 µs`).
4. **Exhaustive 32-Fault Combinational Proof:** Evaluates all `16` test nodes (`32` stuck-at faults) of the 3-bit scan-path combinational core (`3 XOR2 + 3 AND2`), confirming across all $\binom{16}{4}=1820$ 4-vector subsets that maximum coverage is `31/32` (due to 5 disjoint necessary sets $S_1\dots S_5$), while both 5-vector sets achieve `32/32`.

### B. Full Local Forensic Checks (Requires Excluded Local Simulations)
Run when the local course archive `Lab_TestCI_LTspice.rar` (or extracted `.log`/`.raw`/`.lib` folder) is available:
```powershell
python LD4_Arcila_Yactayo/scripts/verificar_ld4.py --rar path\to\Lab_TestCI_LTspice.rar
# or
python LD4_Arcila_Yactayo/scripts/verificar_ld4.py --sim-dir path\to\extracted\Lab_TestCI_LTspice
```
Verifies:
* **521/521 Scalar LOG-vs-RAW Measurements:** Interpolates every `.meas` timestamp directly from the binary `.raw` files (`P1_segf_stuckat`: `352`, `P1_stuckopen`: `16`, `P2_func`: `40`, `P2_flush_fix2`: `13`, `P2_scan`: `100`) and reports exact `max|LOG-RAW|` per file and globally ($\le 4.863 \times 10^{-12}\text{ V}$).
* **`Z` Glitch & Stuck-Open Extrema:** Reproduces `P2_scan.raw` `V3` glitch metrics (`2.169395 V` peak, `0.133661 ns > 1.65 V`, `0.210248 ns` FWHM) and `P1_stuckopen.raw` (`RSO=1T`) extrema (`3.450989 V`, `3.811100 V`, `-0.143817 V`).
* **SDFF Transistor Count:** Parses `cmos035_cells.lib` to verify `28` MOS per `SDFF` (`138` core MOS).

---

## 2. Transient & Integrity Summary ([`../resultados/resumen_verificacion_forense.json`](../resultados/resumen_verificacion_forense.json))

* **Stuck-Open Transient Extrema (`P1_stuckopen.raw`, `RSO=1T`):** `T1` peak `3.450989 V` @ `10.1199 ns` (`.meas` @ `18 ns` = `3.450976 V`); `T2` initial peak `3.811100 V` @ `20.0446 ns` (`.meas` @ `28 ns` = `0.0 V`); `T3` min `-0.143817 V` @ `30.1000 ns` (`.meas` @ `38 ns` = `-0.114028 V`).
* **Scan `Z` Glitch in `V3` (`P2_scan.raw`, `FAULT=0`):** peak `2.169395 V` @ `230.700000 ns`; width above `1.65 V` = `0.133661 ns`; FWHM (at `1.084698 V`) = `0.210248 ns`; static diagnostic sampling at `229 ns` (`0 V`).
* **SDFF Transistor Count (`cmos035_cells.lib`):** `28` MOS per `SDFF` (`4 INV + 6 TG + 2 NOR2`), totaling `138` core transistors (`+ 8` output buffer MOS).

---

## 3. Limitations of Public Reproduction

* From a clean public clone alone, LTspice `.raw`/`.log` waveforms and `cmos035_cells.lib` cannot be re-simulated until the user supplies the excluded teaching-annex files locally as documented in [`../simulaciones/README.md`](../simulaciones/README.md).
* In LTspice, only `4` behavioral fault injectors (`FAULT=1..4`) are implemented in `P2_counter_core.inc`; the `32`-fault result is a combinational proof on the exact gate topology, not 32 separate SPICE runs.
