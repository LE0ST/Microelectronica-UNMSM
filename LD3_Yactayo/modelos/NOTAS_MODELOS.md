# Registro de Modelos SPICE y Notas de Procedencia: LD3

Este documento registra la procedencia, fuentes oficiales, derechos de autor y directrices de uso de los modelos SPICE de transistores IGBT utilizados en el **Laboratorio Dirigido N.° 3**.

---

## 1. Ubicación de las Bibliotecas en el Repositorio

Para preservar la higiene del repositorio y no duplicar archivos ya versionados, las bibliotecas SPICE se mantienen centralizadas en su ubicación de referencia:

```
Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/
├── FGW50XS65.LIB                 # Modelo Fuji Serie X 650V 50A (Sin diodo)
├── FGW50XS65C.LIB                # Modelo Fuji Serie X 650V 50A (Con diodo co-pack)
├── FGW75XS65.LIB                 # Modelo Fuji Serie X 650V 75A (Sin diodo)
├── FGW75XS65C.LIB                # Modelo Fuji Serie X 650V 75A (Con diodo co-pack)
├── nigbt.lib                     # Modelos teóricos N-IGBT (XIRGBC20S, etc.)
└── pigbt.lib                     # Modelo teórico P-IGBT (XPIGBT)
```

En las simulaciones ejecutadas desde `LD3_Yactayo/`, se referencian mediante directivas relativas reproducibles:
```spice
.include "../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/FGW50XS65C.LIB"
```

---

## 2. Modelos Teóricos / Genéricos (Duncan Electronics)

* **Dispositivos:**
  * **N-IGBT:** Subcircuito `.SUBCKT XIRGBC20S 71 72 74` (600 V, 19 A, empaquetado TO-220).
  * **P-IGBT:** Subcircuito `.SUBCKT XPIGBT 71 72 74` (600 V, 40 A, empaquetado TO-220).
* **Fuente Oficial:** [Duncan's Amp Pages — SPICE Models](https://www.duncanamps.com/spicemosfet.html).
* **Naturaleza del Modelo:** Macromodelos electro-térmicos conductuales clásicos (MCE, 1995) basados en la combinación de un MOSFET lateral (`MFIN`), un transistor bipolar de salida (`QOUT`), diodos de unión y fuentes controladas para modelar la modulación de carga en la base.
* **Términos de Uso:** Modelos de libre distribución con fines educativos y de investigación en simulación circuital.

---

## 3. Modelos Comerciales (Fuji Electric — Serie X Trench-FS 650 V)

* **Dispositivos Evaluados:**
  1. `FGW50XS65`: IGBT Trench Field-Stop de 650 V, $I_C = 50\text{ A}$ a $100^\circ\text{C}$, sin diodo antiparalelo integrado.
  2. `FGW50XS65C`: IGBT Trench Field-Stop de 650 V, $I_C = 50\text{ A}$ a $100^\circ\text{C}$, con diodo rápido de marcha libre (*co-packaged diode*) integrado (`DFGW50XS65C_sp`).
  3. `FGW75XS65`: IGBT Trench Field-Stop de 650 V, $I_C = 75\text{ A}$ a $100^\circ\text{C}$, sin diodo antiparalelo integrado.
  4. `FGW75XS65C`: IGBT Trench Field-Stop de 650 V, $I_C = 75\text{ A}$ a $100^\circ\text{C}$, con diodo rápido de marcha libre integrado (`DFGW75XS65C_sp`).
* **Fuente Oficial:** [Fuji Electric Co., Ltd. — Technical Discrete P-Spice Models](https://www.fujielectric.com/products/semiconductors_devices/semiconductor/product_series/model_power_discrete_technical_discrete_p-spice.html).
* **Aviso de Propiedad Intelectual:**
  ```text
  * (C) Fuji Electric Co., Ltd. All Rights Reserved.
  ```
* **Condiciones de Uso:**
  * Los macromodelos son suministrados por el fabricante como soporte técnico para la evaluación de diseño en plataformas SPICE compatibles (PSpice, LTspice).
  * No se reclama autoría alguna sobre los modelos circuitales del fabricante.
  * Queda prohibida la modificación de sus ecuaciones internas para alterar de forma fraudulenta los resultados de simulación.

---

## 4. Esquemas de Referencia Existentes de la Docente

En el directorio de origen se encuentran esquemas preliminares creados en LTspice:
* `NIGBT.asc`: Banco DPT básico para canal N con $V_{DC} = 400\text{ V}$, inductor de carga de $100\ \mu\text{H}$, resistencia sensora $R_E = 1\text{ m}\Omega$ y pulso doble PWL.
* `PIGBT.asc`: Banco de conmutación para canal P con excitación de compuerta negativa.
* `NIGBT21.asc`: Esquemático de caracterización estática múltiple con barrido DC de $V_{CE}$ ($0 \to 4\text{ V}$) y $V_{GE}$ ($0 \to 20\text{ V}$) comparando los 4 modelos de Fuji Electric.
* `Ejercicio2.asc`: Banco transitorio auxiliar.

Estos esquemas sirven como base de verificación y calibración para los ensayos formales de LD3.
