# Control Sheet 1 (HC1) — Part I: Combinational Stuck-At & Stuck-Open Testing

**Module:** [`LD4_Arcila_Yactayo/`](../README.md)  
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)  
**Deliverables:** [`HC1_LD4.pdf`](HC1_LD4.pdf) (4 pages, Spanish) | [`main.tex`](main.tex)

---

## Objectives of Part I

1. Map the 10 test nodes of BCD-to-7-segment `f` ($Y = d + c\overline{ba} + \overline{b+a}$) accounting for physical fan-out on inputs `b` (nodes `3`, `5`) and `a` (nodes `4`, `6`).
2. Derive test vectors analytically using Roth's **D-algorithm** (observation + control justification) and verify them against LTspice fault-injection runs.
3. Build a 140-cell fault dictionary (`20` unique stuck-at faults $\times$ `7` vectors) and compute exact unique cumulative fault coverage.
4. Contrast optimized, functional BCD (`0000–1001`), and random vector sets.
5. Demonstrate why a **stuck-open** defect in `NOR2_SO` (`RSO = 1 TΩ`) requires an ordered two-vector sequence (`0000 -> 0001`).

---

## Exercise-to-Table Correspondence (Official Numbering)

| Official Exercise | Table | Topic & Key Verified Results | Curated Data / Figure |
| :--- | :---: | :--- | :--- |
| **Exercise 1.1** — Healthy circuit | **Tabla 1.1** | 16 vectors (`dcba`); sequence `1000111011111111`; cursor delay $t_{pHL} = 38.090\text{ ps} \approx 38.1\text{ ps}$ (`0001`, cursor reading, not `.meas`) | [`../resultados/p1_circuito_sano.csv`](../resultados/p1_circuito_sano.csv), [`../figuras/esquema_nudos.png`](../figuras/esquema_nudos.png) |
| **Exercise 1.2** — D-algorithm | **Tabla 1.2** | 6 analytical cases (`nodes 7, 5, 9`, `s-a-0` & `s-a-1`) verified against `P1_segf_stuckat.log` steps | [`../TRAZABILIDAD.md`](../TRAZABILIDAD.md) |
| **Exercise 1.3** — Fault dictionary | **Tabla 1.3** | 140 responses (`20` faults $\times$ `7` vectors), `100%` match with `P1_segf_stuckat.log` | [`../resultados/p1_diccionario_fallos.csv`](../resultados/p1_diccionario_fallos.csv), [`../figuras/stuckat_muestras.png`](../figuras/stuckat_muestras.png) |
| **Exercise 1.4** — Coverage & sets | **Tabla 1.4**, **Tabla 1.5** | Unique cumulative coverage: `25%, 60%, 75%, 85%, 90%, 95%, 100%` (no double counting of `10/s-a-0`; `1010` detects `1/s-a-0`). BCD: 10 vec (`100%`); Random: 4 vec (`50%`) | [`../resultados/p1_diccionario_fallos.csv`](../resultados/p1_diccionario_fallos.csv) |
| **Exercise 1.5** — Stuck-open | **Tabla 1.6** | `T0(0000)->T1(0001)` detects (`V(o8) = 3.450976 V`, $Y=1$ vs. $0$); `T2(0011)->T3(0001)` misses (`V(o8) = -0.114028 V`, $Y=0$). Transient RAW extrema: $3.451\text{ V}$ (`T1`), $3.811\text{ V}$ (`T2`), $-0.144\text{ V}$ (`T3`). The 7-vector set detects it via consecutive vectors 3 (`0000`) and 4 (`0001`). | [`../resultados/p1_stuckopen_muestras.csv`](../resultados/p1_stuckopen_muestras.csv), [`../figuras/stuckopen.png`](../figuras/stuckopen.png) |

---

## Experimental Provenance

* All `.meas` values in `Tabla 1.1`–`Tabla 1.6` originate from the local course simulations `P1_segf_stuckat.log` (`352` scalar measurements) and `P1_stuckopen.log` (`16` scalar measurements), verified `100%` against their `.raw` waveforms.
* `../figuras/stuckopen.png` is the authors' historical LTspice capture (`V(o8)`: green = healthy, blue = faulty; `V(y)`: blue = healthy, red = faulty); `../figuras/stuckat_muestras.png` plots the 16 discrete `.meas` samples.
