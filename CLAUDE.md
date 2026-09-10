# CLAUDE.md: Microelectronica-UNMSM

This file defines the project instructions and environment configuration for Claude Code and related AI assistants working on **Microelectronica-UNMSM**.

> **Note for AI Assistants:** The complete Context Engineering specification and operational rules are documented in [`AGENTS.md`](./AGENTS.md) and [`_docs/process.md`](./_docs/process.md). Always consult them before making architectural or methodological modifications.

---

## Key Project Commands

* **Run LTspice simulation (Windows batch mode):**
  ```powershell
  & "G:\LTspice\LTspice.exe" -b "<path_to_cir_file>"
  ```
* **Inspect simulation results (.meas directives):**
  ```powershell
  Get-Content "<path_to_log_file>" | Select-String -Pattern "vm|tphl|tplh|tp|fosc|tpd|iavg|ileak"
  ```
* **Regenerate report figures (Python 3.14):**
  ```powershell
  python LD1_Arcila_Yactayo\scripts\generar_esquema_inversor.py
  python LD1_Arcila_Yactayo\scripts\generar_esquema_compleja.py
  python LD1_Arcila_Yactayo\scripts\generar_comparativa_nodos.py
  python LD1_Arcila_Yactayo\scripts\generar_fig3.py
  ```
* **Verify LaTeX environment balance:**
  ```powershell
  python -c "with open('LD1_Arcila_Yactayo/informe_latex/LD1.tex', 'r', encoding='utf-8') as f: text = f.read(); import re; b = re.findall(r'\\begin\{([^}]+)\}', text); e = re.findall(r'\\end\{([^}]+)\}', text); print('Balanced' if b.count('table') == e.count('table') and len(b) == len(e) else 'Mismatch')"
  ```

---

## Core Operational Rules

1. **Zero Data Fabrication:** Never synthesize or estimate simulation timings or currents. All figures and values in tables must come from executed LTspice netlists.
2. **Strict $\beta$ Calibration:**
   - Act. 1 DC sweep yields optimal $\beta = 2.50$ ($V_M = 0.4989\text{ V} \approx V_{DD}/2$).
   - Act. 2, 3, 5: Reference inverter uses $\beta = 2.50$ ($W_n = 180\text{ nm}, W_p = 450\text{ nm}$).
   - Act. 4: Complex gate AOI uses integer sizing $\beta = 2.0$ ($W_p = 720\text{ nm}$) as specified in official course netlists; always document this distinction.
3. **12-Page Hard Ceiling:** The compiled report in `LD1.tex` must not exceed 12 pages under any circumstance (official evaluation rubric penalty).
4. **Physical Explanations:** Answer all questions utilizing physical semiconductor mechanisms (velocity saturation, short-channel effects, body effect $V_{SB}$, DIBL, gate leakage).
5. **Clean Repository Hygiene:** Never commit `.raw`, `.op.raw`, `.db`, or `.tmp` files.
