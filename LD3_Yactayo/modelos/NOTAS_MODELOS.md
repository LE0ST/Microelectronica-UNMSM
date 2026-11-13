# SPICE Model Provenance & Licensing Notes (LD3)

This document records the provenance, official sources, copyright notices, and placement instructions for the IGBT SPICE models used in **Laboratory Project No. 3 (LD3)**.

---

## 1. Expected Model Placement for Reproduction

Third-party manufacturer and behavioral SPICE libraries are **not redistributed** in the public repository unless an explicit redistribution license is verified. To reproduce the LD3 schematics (`.asc`) and netlists (`.cir`) without modifying their relative `.include` paths, place the downloaded libraries in:

```text
Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/
├── FGW50XS65.LIB                 # Fuji Electric X-Series 650 V, 50 A (Discrete)
├── FGW50XS65C.LIB                # Fuji Electric X-Series 650 V, 50 A (Co-Pack Diode)
├── FGW75XS65.LIB                 # Fuji Electric X-Series 650 V, 75 A (Discrete)
├── FGW75XS65C.LIB                # Fuji Electric X-Series 650 V, 75 A (Co-Pack Diode)
├── nigbt.lib                     # Duncan Electronics N-IGBT (XIRGBC20S)
└── pigbt.lib                     # Duncan Electronics P-IGBT (XPIGBT)
```

All `.cir` netlists in `LD3_Yactayo/simulaciones/netlists/` and `LD3_Yactayo/validation/cases/` reference this directory via relative `.include` directives:

```spice
.include "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/FGW50XS65C.LIB"
```

---

## 2. Commercial Models — Fuji Electric X-Series (650 V Trench-FS)

* **Evaluated Devices:**
  1. `FGW50XS65`: 650 V, 50 A (@ 100 °C) Trench Field-Stop IGBT, discrete (no antiparallel diode).
  2. `FGW50XS65C`: 650 V, 50 A (@ 100 °C) Trench Field-Stop IGBT with co-packaged fast recovery diode (`DFGW50XS65C_sp`).
  3. `FGW75XS65`: 650 V, 75 A (@ 100 °C) Trench Field-Stop IGBT, discrete.
  4. `FGW75XS65C`: 650 V, 75 A (@ 100 °C) Trench Field-Stop IGBT with co-packaged fast recovery diode (`DFGW75XS65C_sp`).
* **Official Download Source:** [Fuji Electric Co., Ltd. — Technical Discrete P-Spice Models](https://www.fujielectric.com/products/semiconductors_devices/semiconductor/product_series/model_power_discrete_technical_discrete_p-spice.html)
* **Copyright Notice in `.LIB` Headers:**
  ```text
  * (C) Fuji Electric Co., Ltd. All Rights Reserved.
  ```
* **Redistribution Status:** **Excluded from public redistribution.** Users must download the four `.LIB` files directly from Fuji Electric's official portal under Fuji Electric's terms of use and place them in the directory shown in Section 1.

---

## 3. Behavioral / Generic Models — Duncan Electronics (`nigbt.lib`, `pigbt.lib`)

* **Evaluated Subcircuits:**
  * **N-IGBT:** `.SUBCKT XIRGBC20S 71 72 74` (600 V, 19 A, TO-220, MCE 7-13-95).
  * **P-IGBT:** `.SUBCKT XPIGBT 71 72 74` (600 V, 40 A, TO-220, MCE 5-20-95).
* **Official Source:** [Duncan's Amp Pages — SPICE Models](https://www.duncanamps.com/spicemosfet.html)
* **Nature of the Models:** Classical behavioral electro-thermal macromodels combining a lateral MOSFET (`MFIN`), an output bipolar transistor (`QOUT`), junction diodes, and controlled sources for base charge modulation.
* **Licensing & Redistribution Status:** Inspection of `nigbt.lib` and `pigbt.lib` headers shows **no explicit open-source or public redistribution license**. Consequently, no free/open-source license is attributed to these files, and manual download instructions from `duncanamps.com` are provided alongside the placement path in Section 1.
* **Local Schematic Symbols:** `LD3_Yactayo/esquemas/NIGBT.asy` and `PIGBT.asy` are included locally in `esquemas/` so the `.asc` schematics open cleanly once the `.lib` files are placed.
