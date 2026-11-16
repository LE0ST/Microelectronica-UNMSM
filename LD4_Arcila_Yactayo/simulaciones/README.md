# LD4 SPICE Simulation Setup and Excluded Course Dependencies

**Module:** [`LD4_Arcila_Yactayo/`](../README.md)<br>
**Authors:** **Leonardo Sait Yactayo Tolentino** (`23190214`) & **Marco Antonio Arcila Santander** (`23190140`)

---

## 1. Publication & Licensing Policy

All `.cir` netlists, `.inc` subcircuits/stimuli, `cmos035_cells.lib` (`0.35 µm` CMOS Level-1 library), and `.py` helper scripts distributed in the course teaching package (`Lab_TestCI_LTspice.rar` / `AnexosLD4.zip`, *Microelectrónica — FIEE-UNMSM*) carry **no public redistribution license** and are therefore **excluded** from this public Git repository (along with `.raw`, `.op.raw`, and `.log` binaries/logs per `.gitignore`).

To run LTspice simulations locally:
1. Obtain the official course archive (`Lab_TestCI_LTspice.rar` or `AnexosLD4.zip`) from the course platform.
2. Extract its files into a local path without spaces or accents (e.g., `LD4_Arcila_Yactayo/simulaciones/local/` — ignored by Git for `.cir`, `.inc`, `.lib`, `.log`, `.raw`).
3. Execute any netlist in LTspice batch mode:
   ```powershell
   & "$env:LTSPICE_EXE" -b "path\to\local\P1_segf_stuckat.cir"
   ```

---

## 2. Official Simulation Runs & Solver Options

| Simulation | Purpose | Solver / `.options` | Outcome & Notes |
| :--- | :--- | :--- | :--- |
| `P1_segf_stuckat.cir` | Part I: 22-step sweep (`NUDO=0..10`, `SV=0,1`), 16 vectors | Default LTspice options (`.tran 0.05n 160n 0 0.05n`) | **Converged cleanly** (0 warnings, 352 `.meas`) |
| `P1_stuckopen.cir` | Part I: `NOR2_SO` (`RSO = 1m, 1T`), `T0..T3` | Default LTspice options (`.tran 0.05n 40n 0 0.05n`) | **Converged cleanly** (0 warnings, 16 `.meas`) |
| `P2_func.cir` | Part II: 3-bit counter functional mode (`SE=0`) | Default LTspice options (`.tran 0.05n 200n 0 0.05n`) | **Converged cleanly** (0 warnings, 40 `.meas`) |
| `P2_flush.cir` | Part II: original flush test (`SE=1`) | `method=gear` | **Aborted** after `92.72 s` (`>350` tolerance warnings, 0 `.meas`) — **not used** for HC2 |
| `P2_flush_fix.cir` | Part II: intermediate flush attempt | `cshunt=2f reltol=0.01 trtol=7 vntol=1m abstol=1n` | **Aborted** after `99.20 s` (`411` tolerance warnings, 0 `.meas`) — **not used** for HC2 |
| `P2_flush_fix2.cir` | Part II: final valid flush test (`SE=1`) | `cshunt=20f gshunt=1n reltol=0.01 trtol=7 vntol=1m abstol=1n itl4=500` | **Converged cleanly** in `6.334 s` (0 warnings, 13 `.meas`) — backs **Tabla 2.2** |
| `P2_scan.cir` | Part II: official 5-vector scan (`V4=001/1`, `FAULT=0..4`) | `cshunt=20f gshunt=1n reltol=0.01 trtol=7 vntol=1m abstol=1n itl4=500` | **Converged cleanly** in `68.503 s` (0 warnings, 100 `.meas`) — backs **Tabla 2.3–2.4** |

> [!NOTE]
> The `.options` directives in `P2_flush_fix2.cir` and `P2_scan.cir` are numerical simulator stabilization parameters (not characterized physical circuit elements). While `cshunt=20f` and relaxed tolerances slightly damp sub-nanosecond transients, all logical diagnostic samples are taken `1 ns` before each rising clock edge in steady state.

---

## 3. Alternative Experiment (`ensayo_26`, `V4 = 101/1`)

For Exercise 2.6 (`Tabla 2.6`), an isolated simulation was executed locally with custom stimulus `V1=001/0, V2=110/1, V3=011/1, V4=101/1, V5=111/1` (`FAULT=0..4`), keeping its `.log` and curated output ([`../resultados/p2_scan_ensayo26.csv`](../resultados/p2_scan_ensayo26.csv)) strictly separate from the official `V4=001/1` run ([`../resultados/p2_scan_oficial.csv`](../resultados/p2_scan_oficial.csv)).
