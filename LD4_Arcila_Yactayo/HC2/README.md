# Control Sheet 2 (HC2) — Part II: Sequential Logic & Scan Path

**Module:** [`LD4_Arcila_Yactayo/`](../README.md)<br>
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)<br>
**Deliverables:** [`HC2_LD4.pdf`](HC2_LD4.pdf) (3 pages, Spanish) | [`main.tex`](main.tex)

---

## Objectives of Part II

1. Characterize the 3-bit synchronous counter (`SE=0`) and quantify exponential functional test growth ($2^N - 1$ cycles).
2. Verify scan-chain shift integrity via the 13-cycle **flush test** (`SE=1`, 3-cycle latency `SI -> FF0 -> FF1 -> FF2 -> SO`) and diagnose single `s-a-0` / `s-a-1` flip-flop faults.
3. Execute the official 5-vector, 23-cycle **scan test program** (`FAULT=0`), distinguish the `Z` static-0 hazard glitch in `V3` from static diagnostic sampling, and diagnose `FAULT=1..4`.
4. Evaluate test-time scaling at $50\text{ MHz}$ and I/O pad overhead for parallel scan chains.
5. Isolate the alternative custom-vector experiment (**Exercise 2.6**) from the official program (**Exercises 2.3–2.4**).

---

## Official vs. Alternative Vector Sets (Strict Separation)

| Program | Vector Sequence (`Q2Q1Q0/E`) | Key Diagnostic Difference | Curated Data |
| :--- | :--- | :--- | :--- |
| **Official (Ex. 2.3–2.4)** | `V1=001/0, V2=110/1, V3=011/1, V4=001/1, V5=111/1` | All 4 faults (`FAULT=1..4`) detected via `SO` (`0%` via `Z`) | [`../resultados/p2_scan_oficial.csv`](../resultados/p2_scan_oficial.csv) |
| **Alternative (Ex. 2.6)** | `V1=001/0, V2=110/1, V3=011/1, V4=101/1, V5=111/1` | `V4=101/1` makes `FAULT 2` also directly observable at `Z=1` | [`../resultados/p2_scan_ensayo26.csv`](../resultados/p2_scan_ensayo26.csv) |

---

## Exercise-to-Table Correspondence

| Official Exercise | Table | Topic & Key Verified Results | Curated Data / Figure |
| :--- | :---: | :--- | :--- |
| **Exercise 2.1** — Functional mode | **Tabla 2.1** | 10 cycles (`P2_func.log`); first `Z=1` at `k = 7` (`149 ns`); $N=20$ @ $50\text{ MHz}$: $20.9715\text{ ms}$ functional vs. $400\text{ ns}$ scan | [`../resultados/p2_func_muestras.csv`](../resultados/p2_func_muestras.csv) |
| **Exercise 2.2** — Flush test | **Tabla 2.2** | `SI=1101001000000` $\mapsto$ `SO=0001101001000` (3-cycle delay) from `P2_flush_fix2.log` (`P2_flush.log` & `P2_flush_fix.log` aborted). `s-a-0` gives `0` from `k=3`; `s-a-1` gives `0`, `1`, `2`-cycle latency for `FF2`, `FF1`, `FF0` | [`../resultados/p2_flush_secuencia.csv`](../resultados/p2_flush_secuencia.csv) |
| **Exercise 2.3** — Healthy scan | **Tabla 2.3** | 23 cycles ($0.46\ \mu\text{s}$). `Z` glitch in `V3`: $2.1694\text{ V}$ peak at $230.700\text{ ns}$, $0.134\text{ ns}$ above $1.65\text{ V}$, $0.210\text{ ns}$ FWHM; static `z_v3` sampled at $229\text{ ns}$ ($0\text{ V}$) | [`../resultados/p2_scan_oficial.csv`](../resultados/p2_scan_oficial.csv), [`../figuras/scan.png`](../figuras/scan.png) |
| **Exercise 2.4** — Fault diagnosis | **Tabla 2.4** | 25 combinations (`FAULT=0..4`); first detectors `F1->V3`, `F2->V4` (`X01/1`), `F3->V2`, `F4->V1` | [`../resultados/p2_scan_oficial.csv`](../resultados/p2_scan_oficial.csv) |
| **Exercise 2.5** — Test time | **Tabla 2.5** | At $50\text{ MHz}$: `23` cyc (`0.46 µs`), `67` cyc (`1.34 µs`), `16,532` cyc (`330.64 µs`), `4,508` cyc (`90.16 µs`, 4 parallel chains $\implies$ 6 extra pads) | [`../TRAZABILIDAD.md`](../TRAZABILIDAD.md) |
| **Exercise 2.6** — Custom vectors | **Tabla 2.6** | Isolated experiment (`V4=101/1`, 25/25 match) + exhaustive 32-fault combinational proof (4 vectors reach $\le 31/32$; 5 disjoint sets $S_1\dots S_5$ required) | [`../resultados/p2_scan_ensayo26.csv`](../resultados/p2_scan_ensayo26.csv), [`../scripts/verificar_ld4.py`](../scripts/verificar_ld4.py) |
