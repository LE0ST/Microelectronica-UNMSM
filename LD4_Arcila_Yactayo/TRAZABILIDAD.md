# Public Traceability Matrix — LD4 (`LD4_Arcila_Yactayo/`)

**Course:** Microelectrónica y Sistemas Nanoelectrónicos (`2026-II`) — UNMSM FIEE<br>
**Instructor:** MsC. Luz Antuanet Adanaqué Infante<br>
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)

---

## 1. Publication Boundary (Tracked Public Files vs. Excluded Local Materials)

* **Publicly Tracked in Git:** LaTeX sources & compiled PDFs ([`informe/main.pdf`](informe/main.pdf), [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf), [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf)), figures ([`figuras/`](figuras/)), curated CSV/JSON results ([`resultados/`](resultados/)), portable verification/plotting scripts ([`scripts/`](scripts/)), and documentation (`README.md`, `TRAZABILIDAD.md`).
* **Excluded Local Course Materials (Not Redistributed):** Official guide `LabDirigidoNro04.pdf`, course archives `AnexosLD4.zip` and `Lab_TestCI_LTspice.rar` (containing `cmos035_cells.lib`, `.cir`, `.inc`, `.log`, `.raw`), original Word drafts, and internal closure/backup folders (`_cierre_ld4/`).

---

## 2. Bijective Traceability Chain (Requirement → Simulation → Measurement → Deliverable)

| Requirement | Local Circuit & Dependencies *(Excluded)* | Local LOG / RAW Source *(Excluded)* | Public Curated Data & Verification | Public Deliverable / Figure |
| :--- | :--- | :--- | :--- | :--- |
| **1.1 Healthy Circuit** (`16` vectors, `10` nodes, $t_{pHL}$) | `P1_segf_stuckat.cir`, `cmos035_cells.lib` | `P1_segf_stuckat.log` Step 1 (`NUDO=0, SV=0`), `.meas` `v00`–`v15`; cursor measurement on `0001` | [`resultados/p1_circuito_sano.csv`](resultados/p1_circuito_sano.csv) (`1000111011111111`); $t_{pHL}=38.090\text{ ps} \approx 38.1\text{ ps}$ (cursors, not `.meas`) | [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf) Tabla 1.1; [`figuras/esquema_nudos.png`](figuras/esquema_nudos.png); [`informe/main.pdf`](informe/main.pdf) Sec. 2.1 |
| **1.2 D-Algorithm** (`6` cases on nodes `7, 5, 9`) | `P1_segf_stuckat.cir`, `cmos035_cells.lib` | `P1_segf_stuckat.log` Steps `11, 12, 15, 16, 19, 20` | Derived analytically & verified against SPICE steps | [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf) Tabla 1.2; [`informe/main.pdf`](informe/main.pdf) Sec. 2.2 |
| **1.3 Fault Dictionary** (`20` faults $\times$ `7` vectors = `140` cells) | `P1_segf_stuckat.cir`, `cmos035_cells.lib` | `P1_segf_stuckat.log` & `.raw` (Steps `1–22`, `352/352` match) | [`resultados/p1_diccionario_fallos.csv`](resultados/p1_diccionario_fallos.csv), [`scripts/verificar_ld4.py`](scripts/verificar_ld4.py) | [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf) Tabla 1.3; [`figuras/stuckat_muestras.png`](figuras/stuckat_muestras.png) |
| **1.4 Cumulative Coverage** & **Set Comparison** | `P1_segf_stuckat.cir`, `cmos035_cells.lib` | `P1_segf_stuckat.log` (`16` vectors) | Unique progression `25%, 60%, 75%, 85%, 90%, 95%, 100%` (no double count of `10/s-a-0`; `1010` detects `1/s-a-0`); BCD `100%`, Random `50%` | [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf) Tablas 1.4–1.5; [`informe/main.pdf`](informe/main.pdf) Sec. 2.2 |
| **1.5 Stuck-Open** (`NOR2_SO`, `RSO = 1 mΩ / 1 TΩ`) | `P1_stuckopen.cir`, `cmos035_cells.lib` | `P1_stuckopen.log` & `.raw` (`16/16` `.meas` match) | [`resultados/p1_stuckopen_muestras.csv`](resultados/p1_stuckopen_muestras.csv); `.meas` (`3.30 V, 3.450976 V, 0.00 V, -0.114028 V`) vs. RAW extrema (`3.451 V` `T1`, `3.811 V` `T2`, `-0.144 V` `T3`) | [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf) Tabla 1.6; [`figuras/stuckopen.png`](figuras/stuckopen.png); [`informe/main.pdf`](informe/main.pdf) Sec. 2.3 |
| **2.1 Functional Mode** (`10` cycles, `N=20` @ `50 MHz`) | `P2_func.cir`, `P2_counter_core.inc`, `P2_stim_func.inc` | `P2_func.log` & `.raw` (`40/40` `.meas` match) | [`resultados/p2_func_muestras.csv`](resultados/p2_func_muestras.csv) ($Z=1$ at `k=7`, `149 ns`; $2^{20}-1 \implies 20.9715\text{ ms}$) | [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) Tabla 2.1; [`informe/main.pdf`](informe/main.pdf) Sec. 3.1 |
| **2.2 Flush Test** (`13` cycles, `SE=1`) | `P2_flush_fix2.cir`, `P2_counter_core.inc`, `P2_stim_flush.inc` | `P2_flush_fix2.log` & `.raw` (`13/13` match; `P2_flush.log` & `P2_flush_fix.log` aborted) | [`resultados/p2_flush_secuencia.csv`](resultados/p2_flush_secuencia.csv) (`3`-cycle latency; individual `s-a-0` and `s-a-1` latencies for `FF2, FF1, FF0`) | [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) Tabla 2.2; [`informe/main.pdf`](informe/main.pdf) Sec. 3.1 |
| **2.3 Healthy Scan** (`V4=001/1`, `23` cycles, `Z` glitch) | `P2_scan.cir`, `P2_counter_core.inc`, `P2_stim_scan.inc` | `P2_scan.log` & `.raw` Step 1 (`FAULT=0`) | [`resultados/p2_scan_oficial.csv`](resultados/p2_scan_oficial.csv), [`resultados/resumen_verificacion_forense.json`](resultados/resumen_verificacion_forense.json) (glitch `2.1694 V` @ `230.700 ns`, `0.134 ns > 1.65 V`, `0.210 ns` FWHM; static sample `229 ns`) | [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) Tabla 2.3; [`figuras/scan.png`](figuras/scan.png); [`informe/main.pdf`](informe/main.pdf) Sec. 3.2 |
| **2.4 Fault Diagnosis** (`FAULT=0..4`, `25` entries) | `P2_scan.cir`, `P2_counter_core.inc`, `P2_stim_scan.inc` | `P2_scan.log` & `.raw` (`100/100` `.meas` match) | [`resultados/p2_scan_oficial.csv`](resultados/p2_scan_oficial.csv) (`F1->V3, F2->V4, F3->V2, F4->V1`; D-algorithm `X01/1` for `F2`) | [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) Tabla 2.4; [`informe/main.pdf`](informe/main.pdf) Sec. 3.2 |
| **2.5 Test Time & Pads** (`50 MHz`) | Analytical equations $N=n+(n+1)m$ | Dimensional evaluation | Verified in [`scripts/verificar_ld4.py`](scripts/verificar_ld4.py) (`0.46`, `1.34`, `330.64`, `90.16 µs`; `6` extra pads) | [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) Tabla 2.5; [`informe/main.pdf`](informe/main.pdf) Sec. 3.2 |
| **2.6 Custom Vectors** (`V4=101/1`) & **32-Fault Proof** | Isolated `ensayo_26` SPICE run (`FAULT=0..4`); combinational topology `P2_counter_core.inc` | Local `ensayo_26` `.log` (`25/25` match); Python exhaustive proof | [`resultados/p2_scan_ensayo26.csv`](resultados/p2_scan_ensayo26.csv), [`scripts/verificar_ld4.py`](scripts/verificar_ld4.py) (4 SPICE injectors vs. 32 combinational faults proof: 4 vec $\le 31/32$) | [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) Tabla 2.6; [`informe/main.pdf`](informe/main.pdf) Sec. 3.2 |
| **Questions 1–10** (incl. P9 `SDFF=28` MOS) | `cmos035_cells.lib`, `P2_counter_core.inc` | Verified in `cmos035_cells.lib` | [`resultados/resumen_verificacion_forense.json`](resultados/resumen_verificacion_forense.json) (`4 INV + 6 TG + 2 NOR2 = 28 MOS/SDFF`, `138` core MOS) | [`informe/main.pdf`](informe/main.pdf) Sec. 4 |

---

## 3. Figure Provenance

| Figure | Public File | Origin & Identification |
| :--- | :--- | :--- |
| HC1 Fig. 1 | [`figuras/esquema_nudos.png`](figuras/esquema_nudos.png) | Vector schematic of the 10 test nodes generated by [`scripts/generar_figuras_ld4.py`](scripts/generar_figuras_ld4.py) |
| Report Fig. 1 | [`figuras/stuckat_muestras.png`](figuras/stuckat_muestras.png) | Python scatter plot of the 16 discrete `.meas` samples (`NUDO=0` vs. `NUDO=7, SV=0`), generated by [`scripts/generar_figuras_ld4.py`](scripts/generar_figuras_ld4.py) (explicitly labeled as discrete samples, not a continuous LTspice oscillogram) |
| Report Fig. 2 | [`figuras/stuckopen.png`](figuras/stuckopen.png) | Historical LTspice capture from the authors' Part I draft (`V(o8)`: green = healthy, blue = faulty; `V(y)`: blue = healthy, red = faulty) |
| Report Fig. 3 | [`figuras/scan.png`](figuras/scan.png) | Historical LTspice capture from the authors' Part II draft (`P2_scan.cir`, `FAULT=0`, 23 cycles at `50 MHz`) |
