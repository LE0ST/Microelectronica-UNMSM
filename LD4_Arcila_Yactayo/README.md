# Laboratory Project No. 4: Integrated Circuit Testing — Stuck-At, Stuck-Open, and Scan Path

**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — Faculty of Electronic and Electrical Engineering (FIEE)<br>
**Course:** Microelectronics and Nanoelectronic Systems (`2026-II`)<br>
**Instructor:** MsC. Luz Antuanet Adanaqué Infante<br>
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)<br>
**Public Deliverables (Spanish):**
* **Technical Report (3 pages):** [`informe/main.pdf`](informe/main.pdf) | [`informe/main.tex`](informe/main.tex)
* **Control Sheet 1 (Part I — Combinational):** [`HC1/HC1_LD4.pdf`](HC1/HC1_LD4.pdf) | [`HC1/main.tex`](HC1/main.tex) | [`HC1/README.md`](HC1/README.md)
* **Control Sheet 2 (Part II — Sequential / Scan):** [`HC2/HC2_LD4.pdf`](HC2/HC2_LD4.pdf) | [`HC2/main.tex`](HC2/main.tex) | [`HC2/README.md`](HC2/README.md)

---

## Overview

This module investigates structural **Design-for-Testability (DFT)** and fault-testing methodologies in `0.35 µm` CMOS integrated circuits ($V_{DD} = 3.3\text{ V}$, Level-1 MOSFET models, logical threshold $V_{th} = 1.65\text{ V}$). It spans two complementary parts:
1. **Combinational Fault Testing (Part I):** Single stuck-at fault modeling, Roth's **D-algorithm**, fault-dictionary generation, cumulative coverage optimization, and **stuck-open** dynamic memory behavior.
2. **Sequential Testing & Scan Path (Part II):** Conversion of a 3-bit synchronous counter into a **Scan-D Flip-Flop (`SDFF`)** shift chain (`SI -> FF0 -> FF1 -> FF2 -> SO`), flush integrity verification, 23-cycle scan test program, fault diagnosis, test-time scaling, and an independent alternative-vector experiment (`ensayo_26`).

---

## Part I — Combinational Circuit Testing

Evaluated on segment `f` of a BCD-to-7-segment decoder: $Y = d + c\overline{ba} + \overline{b+a}$ (using `NAND2`, `NOR2`, `AND2`, and `OR3`). Because primary inputs `b` and `a` each fan out to two gates, the circuit contains **10 test nodes** and **20 unique single stuck-at faults**:
* **Healthy Circuit (`NUDO=0`):** Verified all 16 input vectors (`dcba = 0000..1111`), matching the expected sequence `1000111011111111`. Interactive waveform cursors measured $t_{pHL} = 38.090\text{ ps} \approx 38.1\text{ ps}$ on transition `0001`.
* **D-Algorithm:** Derived control justification and lateral-input observation conditions for nodes `7`, `5`, and `9` (`s-a-0` and `s-a-1`), matching LTspice fault-injection runs.
* **Fault Dictionary & Coverage:** Verified all 140 responses (20 faults $\times$ 7 vectors) in [`resultados/p1_diccionario_fallos.csv`](resultados/p1_diccionario_fallos.csv). Removing the duplicate count of `10/s-a-0` yields exact unique cumulative coverage: `25% -> 60% -> 75% -> 85% -> 90% -> 95% -> 100%`, with the 7th vector (`1010`) strictly required to detect `1/s-a-0`.
* **Stuck-Open (`NOR2_SO`):** Opening the NMOS pull-down of input `a` (`RSO = 1 TΩ`) turns the gate into a dynamic latch requiring an ordered two-vector sequence `T0(0000) -> T1(0001)` for detection, while `T2(0011) -> T3(0001)` misses the defect.

---

## Part II — Sequential Circuit Testing

Evaluated on a 3-bit synchronous counter with enable `E` (`3 XOR2 + 3 AND2 + 3 SDFF`, $T_{CLK} = 20\text{ ns}$ at $50\text{ MHz}$):
* **Functional Mode (`SE=0`):** Verified 10 clock cycles (`k = 0..9`); primary output $Z = E \cdot Q_2 Q_1 Q_0$ asserts at cycle `k = 7` (`149 ns`). Generalized to $2^N - 1$ cycles ($20.9715\text{ ms}$ functional vs. $400\text{ ns}$ scan preload for $N = 20$).
* **Flush Test (`SE=1`):** Confirmed 3-cycle chain latency (`SI = 1101001000000`, `SO = 0001101001000`) using the converged run `P2_flush_fix2.log` (documenting convergence aborts in `P2_flush.log` and `P2_flush_fix.log`). Analyzed `s-a-0` (undetectable location, `0` from `k = 3`) vs. `s-a-1` (`FF2`: 0-cycle, `FF1`: 1-cycle, `FF0`: 2-cycle latency).
* **Official Scan Program (`FAULT = 0..4`):** Strictly used official stimulus `V1=001/0, V2=110/1, V3=011/1, V4=001/1, V5=111/1` (`23` cycles = $0.46\ \mu\text{s}$). Characterized the static-0 hazard glitch on `Z` during `V3` ($2.1694\text{ V}$ peak at $230.700\text{ ns}$, $0.134\text{ ns}$ above $1.65\text{ V}$, $0.210\text{ ns}$ FWHM) and confirmed it does not affect diagnostic sampling at $229\text{ ns}$.
* **Diagnosis & Test-Time Scaling:** Verified all 25 vector-fault combinations with first detectors `F1->V3`, `F2->V4` (via D-algorithm mask `X01/1`), `F3->V2`, `F4->V1` (100% observed via `SO`). Evaluated 32-bit scaling at $50\text{ MHz}$: 1 chain (`16,532` cycles, $330.64\ \mu\text{s}$, 3 pads) vs. 4 parallel 8-bit chains (`4,508` cycles, $90.16\ \mu\text{s}$, 9 pads $\implies$ 6 extra pads).
* **Alternative Experiment (`ensayo_26`, `V4 = 101/1`):** Documented separately in [`resultados/p2_scan_ensayo26.csv`](resultados/p2_scan_ensayo26.csv) and [`HC2/README.md`](HC2/README.md), together with the formal 32-fault combinational proof showing 4 vectors cover at most `31/32` faults.

---

## Key Results

* **521/521 Scalar Measurements Verified:** All 521 `.meas` values across `P1_segf_stuckat`, `P1_stuckopen`, `P2_func`, `P2_flush_fix2`, and `P2_scan` match their `.raw` waveforms within $\le 4.863 \times 10^{-12}\text{ V}$.
* **Part I Coverage:** `100%` (20/20 faults) in 7 optimized vectors (`25% -> 100%`) and 10 BCD vectors, vs. `50%` (10/20) for the 4-vector random set.
* **Part II Scan Coverage:** `4/4` injected SPICE faults (`FAULT=1..4`) detected in 23 cycles ($0.46\ \mu\text{s}$); exhaustive combinational analysis over the 16 test nodes (`32` faults) proves 4 vectors reach at most `31/32`, whereas both 5-vector sets achieve `32/32`.
* **Transistor Count (`SDFF`):** Verified in `cmos035_cells.lib` as **28 transistors/SDFF** (`4 INV + 6 TG + 2 NOR2`), yielding `138` core transistors (`+ 8` output buffer MOS).

---

## Directory Structure

```text
LD4_Arcila_Yactayo/
├── README.md                    # This file
├── TRAZABILIDAD.md              # Public bijective traceability matrix
├── informe/                     # 3-page Spanish technical report (main.tex, main.pdf)
├── HC1/                         # Control Sheet 1 (README.md, main.tex, HC1_LD4.pdf)
├── HC2/                         # Control Sheet 2 (README.md, main.tex, HC2_LD4.pdf)
├── figuras/                     # Schematic, discrete-sample plot, and LTspice captures
├── resultados/                  # Curated CSV tables & JSON verification summary
├── simulaciones/README.md       # Simulation setup, solver options & local dependency guide
├── scripts/                     # Portable Python verification & figure scripts
└── validacion/README.md         # Public vs. local validation scope and instructions
```

---

## Verification and Traceability

* **Logical Threshold:** $V_{th} = 1.65\text{ V}$ ($V_{DD}/2$).
* **LOG vs. RAW & Solver Options:** See [`TRAZABILIDAD.md`](TRAZABILIDAD.md) and [`simulaciones/README.md`](simulaciones/README.md) for the exact `.options` used in `P2_flush_fix2` and `P2_scan` (`cshunt=20f gshunt=1n reltol=0.01 trtol=7 vntol=1m abstol=1n itl4=500`).
* **Public Validation:** [`validacion/README.md`](validacion/README.md) details standalone checks vs. local `.raw`/`.log` forensic checks.

---

## Reproduction Instructions

1. **Run standalone public validation (no private files required):**
   ```powershell
   python LD4_Arcila_Yactayo/scripts/verificar_ld4.py
   ```
2. **Regenerate Part I figures from curated CSV data:**
   ```powershell
   python LD4_Arcila_Yactayo/scripts/generar_figuras_ld4.py
   ```
3. **Run full local forensic check (if you hold the course `Lab_TestCI_LTspice.rar` locally):**
   ```powershell
   python LD4_Arcila_Yactayo/scripts/verificar_ld4.py --rar path\to\Lab_TestCI_LTspice.rar
   ```

---

## Known Limitations

* **Excluded Course Teaching Files:** The official guide (`LabDirigidoNro04.pdf`), cell library (`cmos035_cells.lib`), netlists (`.cir`, `.inc`), and raw archives (`AnexosLD4.zip`, `Lab_TestCI_LTspice.rar`) are course teaching materials without a public redistribution license and are excluded from this repository.
* **Historical Captures vs. Python Plot:** `figuras/stuckopen.png` and `figuras/scan.png` are historical LTspice captures from the authors' original drafts; `figuras/stuckat_muestras.png` plots the 16 discrete `.meas` samples from `P1_segf_stuckat.log` (labeled explicitly as discrete samples, not a continuous oscillogram).
* **SPICE Fault Injectors vs. 32-Fault Proof:** The SPICE netlist implements 4 behavioral fault injectors (`FAULT=1..4`); full 32-fault combinational coverage is demonstrated exhaustively in Python (`scripts/verificar_ld4.py`).

---

## References

* MsC. L. A. Adanaqué Infante, *Guía de Laboratorio: Test de Circuitos Integrados (Stuck-at y Scan Path)*, LD4, FIEE-UNMSM, 2026-II.
* Bushnell, M. L., & Agrawal, V. D. (2000). *Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits*. Kluwer/Springer.
* Pollán Santamaría, T. (2007). *Tecnología Electrónica*, Cap. 25: «Test de circuitos integrados». Universidad de Zaragoza.
