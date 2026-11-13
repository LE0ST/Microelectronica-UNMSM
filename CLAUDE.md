# CLAUDE.md: Microelectronica-UNMSM

This file defines the project instructions and environment configuration for Claude Code and related AI assistants working on **Microelectronica-UNMSM**.

> **Note for AI Assistants:** The complete Context Engineering specification and operational rules are documented in [`AGENTS.md`](./AGENTS.md), [`_docs/process.md`](./_docs/process.md) and [`_docs/bitacora.md`](./_docs/bitacora.md). Always consult them before making architectural or methodological modifications.

---

## Authorship & Project Context
* **Course:** Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II) — UNMSM (FIEE).
* **Instructor:** MsC. Luz Adanaqué Infante.
* **Authors:**
  * **Leonardo Sait Yactayo Tolentino** (23190214): Co-author LD1 & LD2; Sole author for LD3 (*Individual*).
  * **Marco Antonio Arcila Santander** (23190140): Co-author LD1 & LD2.

---

## Key Project Commands

* **Run LTspice simulation (Windows batch mode):**
  ```powershell
  & "G:\LTspice\LTspice.exe" -b "<path_to_cir_file>"
  ```
* **Inspect simulation results (.meas directives):**
  ```powershell
  Get-Content "<path_to_log_file>" | Select-String -Pattern "vm|tphl|tplh|tp|fosc|tpd|iavg|ileak|td_off|eoff|itail|vce_max"
  ```
* **Run Python processing and figure generation (Python 3.14):**
  ```powershell
  python <path_to_script.py>
  ```
* **Git Safe Workflow:**
  ```powershell
  git status
  git add <specific_file>
  git commit -m "type(scope): description"
  ```

---

## Core Operational Rules

### Global Rules (Universal)
1. **Zero Data Fabrication:** Never synthesize or estimate simulation timings, currents, or voltages. All values in tables and text must originate from executed LTspice netlists (`.meas`) or documented analytical formulas.
2. **Experimental Traceability:** Maintain 1:1 biunivocal mapping between schematic/netlist, simulation output, python script, and generated figure.
3. **Model Immutability:** Never modify vendor/foundry SPICE cards (PTM BSIM4 or discrete IGBT models).
4. **Physical Grounding:** All explanations must be rooted in semiconductor device physics.
5. **Clean Repository Hygiene:** Never commit `.raw`, `.op.raw`, `.db`, or `.tmp` simulation files.
6. **Feature Branching:** Active development takes place on dedicated branches (e.g. `feat/ld3-igbt`) before merging to `main`.

### Lab-Specific Requirements
* **LD1 (CMOS Static):** $\beta_{\text{opt}} = 2.50$, AOI $\beta = 2.0$, strict 12-page ceiling in IEEE format.
* **LD2 (CMOS Dynamic):** 5 activities developed (domino, charge sharing, keeper sizing, NTV), 20 pages in IEEE format.
* **LD3 (IGBT Characterization):** Individual work by Leonardo Yactayo. Governed by official guide [`Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf`](./Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf). Focus on Double Pulse Test (DPT), tail current, $t_{d(\text{off})}$, $E_{\text{off}}$, $V_{CE,\text{peak}}$, and $R_G$ influence using Fuji Electric and Duncan Electronics models. Deliverables: full comparative table, clear waveforms, conclusions ($\ge 1$ page), and presentation on October 21, 2026.
