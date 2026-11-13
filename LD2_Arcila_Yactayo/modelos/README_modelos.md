# PTM Technology Models for LD2 (`modelos/`)

This directory is the local placement target for the **BSIM4 (Level 54)** Predictive Technology Model (PTM) libraries required to run the SPICE netlists in **Laboratory Project No. 2 (LD2)**, following Section 4.1 of the official guide (`LabDirigido2.pdf`).

> [!IMPORTANT]
> **Third-Party Model Exclusion:** The `.lib` model files (`ptm45hp.lib`, `ptm45lp.lib`, `ptm130.lib`, `ptm45hp_aux.lib`) are **not redistributed** in this public repository because ASU/Berkeley NIMO PTM cards do not include an explicit open-source redistribution license. Obtain the original `.pm` parameter cards from the official PTM distribution and generate the renamed `.lib` files locally before running LTspice.

---

## 1. Model Collision Prevention Rule (Guide Section 4.1)

In SPICE, unmodified PTM model cards declare generic model names:

```spice
.model  nmos  nmos  level = 54
.model  pmos  pmos  level = 54
```

If two unmodified files (e.g., 45 nm HP and 45 nm LP) are `.include`d in the same simulation, the second definition silently overrides the first. Therefore, each model card must be renamed into a collision-free `.lib` file.

---

## 2. Local File Placement & Model Name Mapping

Create or populate `LD2_Arcila_Yactayo/modelos/` (and copy `ptm45hp.lib`, `ptm45lp.lib`, `ptm130.lib` into `LD2_Arcila_Yactayo/` if running legacy root-relative scripts) with the following renamed libraries:

| Original PTM Card | Local Target (`LD2_Arcila_Yactayo/modelos/`) | NMOS Model Name | PMOS Model Name | BSIM4 Level |
| :--- | :--- | :--- | :--- | :---: |
| `45nm_HP.pm` | `ptm45hp.lib` | `nmos_45hp` | `pmos_45hp` | 54 |
| `45nm_LP.pm` | `ptm45lp.lib` | `nmos_45lp` | `pmos_45lp` | 54 |
| `130nm_bulk.pm` | `ptm130.lib` | `nmos_130` | `pmos_130` | 54 |

### Transformation Commands (Guide Section 4.1)

```bash
sed -e 's/^\.model  *nmos  *nmos/.model nmos_45hp nmos/' \
    -e 's/^\.model  *pmos  *pmos/.model pmos_45hp pmos/' 45nm_HP.pm > ptm45hp.lib

sed -e 's/^\.model  *nmos  *nmos/.model nmos_45lp nmos/' \
    -e 's/^\.model  *pmos  *pmos/.model pmos_45lp pmos/' 45nm_LP.pm > ptm45lp.lib

sed -e 's/^\.model  *nmos  *nmos/.model nmos_130 nmos/' \
    -e 's/^\.model  *pmos  *pmos/.model pmos_130 pmos/' 130nm_bulk.pm > ptm130.lib
```

### Verification (`grep '^.model'`)

```text
ptm45hp.lib: .model nmos_45hp nmos  level = 54
ptm45hp.lib: .model pmos_45hp pmos  level = 54
ptm45lp.lib: .model nmos_45lp nmos  level = 54
ptm45lp.lib: .model pmos_45lp pmos  level = 54
ptm130.lib:  .model nmos_130  nmos  level = 54
ptm130.lib:  .model pmos_130  pmos  level = 54
```

This yields **6 distinct, independent models** with zero `.model` name collisions.

---

## 3. Verified Reference Parameters (Guide Table 4.2 vs. Local Libraries)

| Parameter | Guide: 45 nm HP | 45 nm HP (`ptm45hp.lib`) | Guide: 45 nm LP | 45 nm LP (`ptm45lp.lib`) | Guide: 130 nm | 130 nm (`ptm130.lib`) | Match |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Nominal $V_{DD}$ | 1.0 V | *(In netlist)* | 1.1 V | *(In netlist)* | 1.3 V | *(In netlist)* | Yes |
| $V_{th0}$ NMOS | 0.469 V | 0.46893 V | 0.623 V | 0.62261 V | 0.378 V | 0.3782 V | Yes |
| $V_{th0}$ PMOS | -0.492 V | -0.49158 V | -0.587 V | -0.58700 V | -0.321 V | -0.3210 V | Yes |
| $t_{oxe}$ NMOS | 1.25 nm | $1.25 \times 10^{-9}\text{ m}$ | 1.80 nm | $1.80 \times 10^{-9}\text{ m}$ | 2.25 nm | $2.25 \times 10^{-9}\text{ m}$ | Yes |
| $\mu_0$ NMOS ($\text{m}^2/\text{V}\cdot\text{s}$) | 0.054 | 0.054 | 0.049 | 0.049 | 0.059 | 0.05928 | Yes |
| $\mu_0$ PMOS ($\text{m}^2/\text{V}\cdot\text{s}$) | 0.020 | 0.020 | 0.021 | 0.021 | 0.0084 | 0.00835 | Yes |
| $v_{sat}$ NMOS (m/s) | $1.7 \times 10^5$ | 170000 | $1.3 \times 10^5$ | 130000 | $1.0 \times 10^5$ | 100370 | Yes |
| `nfactor` NMOS | 2.22 | 2.22 | 1.60 | 1.60 | 1.50 | 1.50 | Yes |

*Note: For historical parameter-inspection logs of the local `.lib` files prior to public release, see [`../verificacion_modelos.txt`](../verificacion_modelos.txt).*
