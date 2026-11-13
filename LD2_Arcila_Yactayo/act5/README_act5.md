# Activity 5 — Parasitic Effects and Near-Threshold Voltage (NTV) Operation

**Course:** Microelectronics and Nanoelectronic Systems (Semester 2026-II)  
**Institution:** Universidad Nacional Mayor de San Marcos (UNMSM) — Faculty of Electrical and Electronic Engineering (FIEE)  
**Authors:** Leonardo Sait Yactayo Tolentino (`23190214`) & Marco Antonio Arcila Santander (`23190140`)  
**Base Technology:** PTM 45 nm High-Performance (HP) & Low-Power (LP), $T \in \{27^\circ\text{C}, 85^\circ\text{C}\}$, $V_{DD} \in [0.35\,\text{V}, 1.00\,\text{V}]$  
**Official Guide:** `Semana_04/Guia_Oficial_LD2/LabDirigido2.pdf` (Section 9, pp. 10–13; local teaching document excluded from public repository)

---

## 1. Objectives and Requirements Matrix

| Req. ID | LD2 Guide Task | Technical Statement | External Historical Netlists (`laboratorio5/`) | Published Netlists (`act5/circuitos/`) | Status |
|:---:|:---:|:---|:---|:---|:---:|
| **REQ-22** | §9.1 (Task 1) | Characterize clock feedthrough overshoot at `dyn` coupled via precharge PMOS $C_{gd}$; quantify $D_{DB}$ diode clamping and PMOS keeper damping. | `9.1 Tarea 1.cir` | [`act5_feedthrough_keeper.cir`](circuitos/act5_feedthrough_keeper.cir) | **RECONCILED** |
| **REQ-23** | §9.2 (Tasks 1–2) | Evaluate dynamic retention $t_{\text{hold}}$ under subthreshold leakage at $27^\circ\text{C}$ and $85^\circ\text{C}$; determine $f_{\min}$ and $f_{\max}$ to bound $[f_{\min}, f_{\max}]$. | `9.2 Tarea 1 thold.cir` | [`act5_ntv_thold_fmin.cir`](circuitos/act5_ntv_thold_fmin.cir)<br>[`act5_ntv_thold_85c.cir`](circuitos/act5_ntv_thold_85c.cir) | **RECONCILED** |
| **REQ-24** | §9.2 (Task 3) | Near-Threshold Voltage sweep ($V_{DD} \in [0.35, 1.00]\,\text{V}$), $t_{\text{eval}}$ quantification, keeper contention ($W_{kp} \in \{45, 90\}\,\text{nm}$), and $10\times t_{\text{eval}}$ margin check. | `9.2 Tarea 1 teval.cir`<br>`9.2 Tarea 3 teval keeper...` | [`act5_ntv_teval_fmax.cir`](circuitos/act5_ntv_teval_fmax.cir) | **RECONCILED** |
| **REQ-25** | §9.2 (Task 4) | Subthreshold comparison at $V_{DD} = 0.50\,\text{V}$ between 45 nm HP and 45 nm LP ($I_{\text{on}}, I_{\text{off}}, I_{\text{on}}/I_{\text{off}}, t_{\text{eval}}$) and cycle energy scaling $E_{\text{sw}}$. | `9.2 Tarea 4.cir` | [`act5_hp_vs_lp_subumbral.cir`](circuitos/act5_hp_vs_lp_subumbral.cir)<br>[`act5_energia_ntv.cir`](circuitos/act5_energia_ntv.cir) | **RECONCILED** |

---

## 2. Scientific Audit of External Historical Circuits (`laboratorio5/`, Outside Repository)

The historical suite originally developed by Marco Antonio Arcila (`laboratorio5/`, external to this repository) was audited against the published `act5/` control suite:

1. **`9.1 Tarea 1.cir` (Clock Feedthrough):**  
   Historical run measured $+61.30\,\text{mV}$ overshoot ($V_{\max} = 1.06130\,\text{V}$) vs. $+64.31\,\text{mV}$ ($V_{\max} = 1.06431\,\text{V}$) in `act5_feedthrough_keeper.cir` ($3.01\,\text{mV}$ / $4.9\%$ difference across simulation setups). The reported $9.47\,\text{mV}$ "undershoot" ($V_{\min} = 0.99053\,\text{V}$) occurred at the falling clock edge returning to precharge ($t=2.0\,\text{ns}$), not during active evaluation.
2. **`9.2 Tarea 1 teval.cir` (NTV $t_{\text{eval}}$ without keeper):**  
   7-step $V_{DD}$ sweep ($0.35$–$1.00\,\text{V}$) on an isolated dynamic NAND3 (no output inverter): $t_{\text{eval}} = 33.56\,\text{ps}$ ($1.0\,\text{V}$) to $1783.72\,\text{ps}$ ($0.35\,\text{V}$).
3. **`9.2 Tarea 1 thold.cir` ($t_{\text{hold}}$ at $27^\circ\text{C}$ without keeper):**  
   $t_{\text{hold}} = 1.11755\,\mu\text{s}$ ($1.0\,\text{V}$) to $1.97349\,\mu\text{s}$ ($0.35\,\text{V}$), giving $f_{\min,\text{Marco}} = 447.41\,\text{kHz}$ ($1.0\,\text{V}$) and $253.36\,\text{kHz}$ ($0.35\,\text{V}$).
4. **`9.2 Tarea 3 teval keeper 45nm.cir` and `90nm.cir` (NTV Contention):**  
   * $W_{kp} = 45\,\text{nm}$: $t_{\text{eval}} = 36.83\,\text{ps}$ ($1.0\,\text{V}$) to $1902.29\,\text{ps}$ ($0.35\,\text{V}$) ($+9.7\%$ to $+6.6\%$ penalty).
   * $W_{kp} = 90\,\text{nm}$: $t_{\text{eval}} = 44.74\,\text{ps}$ ($1.0\,\text{V}$) to $2102.60\,\text{ps}$ ($0.35\,\text{V}$) ($+33.3\%$ to $+17.9\%$ penalty).
5. **`9.2 Tarea 3 thold keeper 45nm.cir` and `90nm.cir` (Retention with Keeper):**  
   `.meas TRAN t_hold` returned `FAIL'ed` over $T_{\text{stop}} = 15.0\,\mu\text{s}$ because $V(dyn)$ never crossed $V_{DD}/2$: at $15\,\mu\text{s}$, $V(dyn) = 0.999977\,\text{V}$ ($\Delta V = 0.023\,\text{mV}$ at $1.0\,\text{V}$) and $0.349440\,\text{V}$ ($\Delta V = 0.560\,\text{mV}$ at $0.35\,\text{V}$). This establishes a finite observed lower bound $t_{\text{hold}} > 15\,\mu\text{s}$ ($f_{\min} < 33.3\,\text{kHz}$).
6. **`9.2 Tarea 4.cir` (LP vs. HP at $0.50\,\text{V}$):**  
   Historical $t_{\text{eval,LP}} = 8.64761\,\text{ns}$ closely matches `act5_hp_vs_lp_subumbral.cir` ($8.48841\,\text{ns}$, $1.8\%$ difference).

---

## 3. Physical Fundamentals and Analytical Modeling

### A. Clock Feedthrough and Diode Clamping
* **PTM 45 nm HP overlap capacitance:** $C_{gd} = (cgdo + cgdl) \cdot W_p \approx \mathbf{0.0507\,\text{fF}}$ ($W_p = 135\,\text{nm}$).
* **Capacitive divider:**
  $$\Delta V_{\text{feedthrough}} \approx \frac{C_{gd}}{C_{\text{total}}} \Delta V_{clk} \approx \frac{0.0507\,\text{fF}}{0.85 - 1.05\,\text{fF}} \times 1.0\,\text{V} \approx \mathbf{50 - 60\,\text{mV}}$$
  Consistent with the simulated **$+64.31\,\text{mV}$** overshoot ($V_{\max} = 1.0643\,\text{V}$) without keeper.
* **Transient $D_{DB}$ diode clamping:** Exceeding $V_{DD}$ by $64.3\,\text{mV}$ weakly forward-biases the drain-body p-n junction, injecting up to **$2.841\,\mu\text{A}$** transiently into $V_{DD}$ (not general gate-oxide overvoltage protection).
* **PMOS keeper damping ($W_{kp} = 45\,\text{nm}$):** Added capacitance attenuates overshoot to **$+49.31\,\text{mV}$** ($V_{\max} = 1.0493\,\text{V}$, **$-23.3\%$** passive reduction).

### B. Operable Frequency Window $[f_{\min}, f_{\max}]$ and NTV Regime
$$f_{\max} \approx \frac{1}{2(t_{\text{eval}} + t_{pLH,\text{inv}})}, \qquad f_{\min} \approx \frac{1}{2 t_{\text{hold}}}$$

1. **Maximum Frequency ($f_{\max}$, full domino cell in `act5/`):**
   * At $V_{DD} = 1.00\,\text{V}$: $t_{\text{eval}} = 23.21\,\text{ps}$, $t_{pLH,\text{inv}} = 4.52\,\text{ps} \implies t_{\text{pd}} = 27.72\,\text{ps} \implies f_{\max} = \mathbf{18.035\,\text{GHz}}$.
   * At $V_{DD} = 0.35\,\text{V}$: $t_{\text{eval}} = 1739.95\,\text{ps}$, $t_{pLH,\text{inv}} = 1347.25\,\text{ps} \implies t_{\text{pd}} = 3087.20\,\text{ps} \implies f_{\max} = \mathbf{161.96\,\text{MHz}}$.
2. **Minimum Frequency ($f_{\min}$):**
   * At $27^\circ\text{C}$ ($t_{\text{hold}} = 1.096\,\mu\text{s}$ at $1.0\,\text{V}$; $1.930\,\mu\text{s}$ at $0.35\,\text{V}$): $f_{\min} = \mathbf{456.21\,\text{kHz}}$ ($1.0\,\text{V}$), $\mathbf{259.12\,\text{kHz}}$ ($0.35\,\text{V}$).
   * At $85^\circ\text{C}$ ($t_{\text{hold}} = 0.305\,\mu\text{s}$ at $1.0\,\text{V}$; $0.440\,\mu\text{s}$ at $0.35\,\text{V}$): $f_{\min} = \mathbf{1638.94\,\text{kHz}}$ ($\approx 1.64\,\text{MHz}$ at $1.0\,\text{V}$), $\mathbf{1136.28\,\text{kHz}}$ ($\approx 1.14\,\text{MHz}$ at $0.35\,\text{V}$). Thermal retention ratio $27^\circ\text{C}/85^\circ\text{C}$ is $\mathbf{3.59\times}$ ($3.66\times$ with historical data).
   * Additional static retention steps ($0.30\,\text{V}$ and $0.25\,\text{V}$): $t_{\text{hold}} = 1.889\,\mu\text{s}$ ($27^\circ\text{C}$) / $0.424\,\mu\text{s}$ ($85^\circ\text{C}$) at $0.30\,\text{V}$; $1.802\,\mu\text{s}$ ($27^\circ\text{C}$) / $0.398\,\mu\text{s}$ ($85^\circ\text{C}$) at $0.25\,\text{V}$.
3. **Window Margin ($V_{DD} \in [0.35, 1.00]\,\text{V}$):**
   * The operable window stays wide open ($161.96\,\text{MHz} \gg 1.14\,\text{MHz}$ at $0.35\,\text{V}, 85^\circ\text{C}$).
   * Safety ratio $t_{\text{hold}}/t_{\text{eval}}$ ($27^\circ\text{C}$): $\approx \mathbf{47,200} \gg 10$ at $1.00\,\text{V}$ and $\approx \mathbf{1,109} \gg 10$ at $0.35\,\text{V}$. Because $t_{\text{eval}}$ and $f_{\max}$ were not simulated below $0.35\,\text{V}$, the bidirectional window $[f_{\min}, f_{\max}]$ is strictly bounded on $[0.35, 1.00]\,\text{V}$ without extrapolation.

### C. Subthreshold Comparison at $V_{DD} = 0.50\,\text{V}$: 45 nm HP vs. 45 nm LP

| Physical Parameter ($V_{DD} = 0.50\,\text{V}$) | 45 nm HP Node | 45 nm LP Node | Comparative Ratio (LP / HP) |
|:---|:---:|:---:|:---:|
| **Threshold Voltage ($V_{thn}$)** | $0.469\,\text{V}$ | $0.623\,\text{V}$ | $+154\,\text{mV}$ (Deep subthreshold in LP) |
| **ON Current ($I_{\text{on}}$)** | $\mathbf{4.898\,\mu\text{A}}$ | $\mathbf{0.0986\,\mu\text{A}}$ ($98.6\,\text{nA}$) | $\mathbf{0.0201\times}$ ($-98.0\%$) |
| **OFF Current ($I_{\text{off}}$)** | $\mathbf{125.05\,\text{pA}}$ | $\mathbf{0.671\,\text{pA}}$ ($671\,\text{fA}$) | $\mathbf{0.0054\times}$ ($-99.5\%$, **$186.4\times$ lower**) |
| **Selectivity ($I_{\text{on}} / I_{\text{off}}$)** | **$39,168.5$** | **$146,950.1$** | $\mathbf{3.75\times}$ higher in LP |
| **Evaluation Delay ($t_{\text{eval}}$)** | $\mathbf{161.57\,\text{ps}}$ | $\mathbf{8488.41\,\text{ps}}$ ($8.49\,\text{ns}$) | $\mathbf{52.54\times}$ slower in LP |

### D. Energy Scaling Toward NTV ($T_{\text{clk}} = 10.0\,\text{ns}$)

| $V_{DD}$ (V) | Peak Current $I_{\text{pk}}$ ($\mu\text{A}$) | Energy/Cycle $E_{\text{sw}}$ (fJ) | Avg. Power $P_{\text{avg}}$ (nW) | Relative Energy Savings |
|:---:|:---:|:---:|:---:|:---:|
| **$1.00$** | $37.29$ | $\mathbf{0.7259}$ | $72.59$ | $0.0\%$ (Reference) |
| **$0.80$** | $18.74$ | $\mathbf{0.4533}$ | $45.33$ | $-37.6\%$ |
| **$0.60$** | $6.44$ | $\mathbf{0.2876}$ | $28.76$ | $-60.4\%$ |
| **$0.50$** | $2.25$ | $\mathbf{0.2018}$ | $20.18$ | $-72.2\%$ |
| **$0.45$** | $0.99$ | $\mathbf{0.1533}$ | $15.33$ | $-78.9\%$ |
| **$0.40$** | $0.70$ | $\mathbf{0.1076}$ | $10.76$ | $-85.2\%$ |
| **$0.35$** | $0.62$ | $\mathbf{0.0719}$ | $7.19$ | $\mathbf{-90.1\%}$ ($\mathbf{10.1\times}$ reduction) |

---

## 4. Consolidated Master Matrix (NTV Sweep)

| $V_{DD}$ (V) | $t_{\text{eval}}$ Act5 (ps) | $t_{pLH,\text{inv}}$ (ps) | $t_{\text{pd}}$ (ps) | $f_{\max}$ Act5 (GHz) | $t_{\text{eval}}$ Hist. (ps) | $t_{\text{hold}}$ 27°C Act5 ($\mu\text{s}$) | $f_{\min}$ 27°C Act5 (kHz) | $t_{\text{hold}}$ 27°C Hist. ($\mu\text{s}$) | $f_{\min}$ 27°C Hist. (kHz) | $t_{\text{hold}}$ 85°C ($\mu\text{s}$) | $f_{\min}$ 85°C (kHz) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$1.00$** | $23.21$ | $4.52$ | $27.72$ | **$18.035$** | $33.56$ | $1.096$ | **$456.21$** | $1.118$ | **$447.23$** | $0.305$ | **$1638.94$** |
| **$0.80$** | $33.31$ | $9.80$ | $43.11$ | **$11.599$** | $43.65$ | $1.429$ | **$349.93$** | $1.458$ | **$342.94$** | $0.375$ | **$1334.82$** |
| **$0.60$** | $70.48$ | $34.92$ | $105.40$ | **$4.744$** | $81.17$ | $1.754$ | **$285.03$** | $1.792$ | **$279.02$** | $0.432$ | **$1157.19$** |
| **$0.50$** | $162.34$ | $102.19$ | $264.52$ | **$1.890$** | $174.85$ | $1.874$ | **$266.74$** | $1.916$ | **$260.96$** | $0.448$ | **$1117.00$** |
| **$0.45$** | $308.17$ | $212.30$ | $520.47$ | **$0.961$** | $323.39$ | $1.914$ | **$261.17$** | $1.957$ | **$255.49$** | $0.450$ | **$1110.68$** |
| **$0.40$** | $686.10$ | $505.22$ | $1191.33$ | **$0.420$** | $708.53$ | $1.935$ | **$258.37$** | $1.979$ | **$252.65$** | $0.448$ | **$1115.75$** |
| **$0.35$** | $1739.95$ | $1347.25$ | $3087.20$ | **$0.162$** | $1783.72$ | $1.930$ | **$259.12$** | $1.973$ | **$253.42$** | $0.440$ | **$1136.28$** |

### Supplementary Preserved Details

* **Historical subthreshold/NTV values:** historical $t_{\text{eval,LP}} = 8.64761\,\text{ns}$ ($8647.61\,\text{ps}$) vs. `act5_hp_vs_lp_subumbral.log`: $t_{\text{eval,LP}} = 8.48841\,\text{ns}$, $t_{\text{eval,HP}} = 0.16157\,\text{ns}$ (ratio $52.54\times$); historical run omitted $I_{\text{on}}$ and $I_{\text{off}}$ required by the guide.
* **$f_{\max}$ arithmetic at $1.00\,\text{V}$:** $f_{\max} = 1/(2 \times 27.7235 \times 10^{-12}\,\text{s}) = 18.035\,\text{GHz}$ ($18035\,\text{MHz}$); at $0.35\,\text{V}$ the operable band is $[1.14\,\text{MHz}, 161.96\,\text{MHz}]$ at $85^\circ\text{C}$, i.e., $f_{\max}$ is $142\times$ larger than $f_{\min}$; at $1.00\,\text{V}$ the band is $[1.64\,\text{MHz}, 18035\,\text{MHz}]$.
* **Thermal retention ratio:** $1.096/0.305 \approx 3.59\times$ ($3.66\times$ with historical data), raising $f_{\min}$ by $\sim 3.6\times$; it is not claimed that $I_{\text{off}}$ quadrupled exactly, only that the effective discharge time shrank by the measured factor.
* **Additional static-retention steps** ($0.30\,\text{V}$ and $0.25\,\text{V}$; 9 steps executed): $f_{\min} = 264.68\,\text{kHz}$ ($27^\circ\text{C}$) and $1.179\,\text{MHz}$ ($85^\circ\text{C}$) at $0.30\,\text{V}$; $277.42\,\text{kHz}$ and $1.257\,\text{MHz}$ at $0.25\,\text{V}$. No $t_{\text{eval}}$ or $f_{\max}$ data exist at these voltages, so no exact crossing point (e.g., at $0.20\,\text{V}$) is extrapolated.
* **$t_{\text{hold}}/t_{\text{eval}}$ margin arithmetic:** $1.096\,\mu\text{s}/23.21\,\text{ps} = 1.096\,\mu\text{s}/0.00002321\,\mu\text{s} \approx 47{,}200$ (historical: $1.118\,\mu\text{s}/33.56\,\text{ps} = 1.118/0.00003356 \approx 33{,}300$) at $1.00\,\text{V}$; $1.930\,\mu\text{s}/1739.95\,\text{ps} = 1.930/0.001740 \approx 1{,}109$ (historical: $1.973\,\mu\text{s}/1783.72\,\text{ps} = 1.973/0.001784 \approx 1{,}106$) at $0.35\,\text{V}$.
* **Verified formulas:** $f_{\max} = 1/(2 t_{\text{pd}})$ and $f_{\min} = 1/(2 t_{\text{hold}})$ hold exactly for all rows of the matrix above (Act5, historical, and $85^\circ\text{C}$).
* **Historical overshoot/damping:** the keeper reduces overshoot from $64.3\,\text{mV}$ to $49.3\,\text{mV}$ ($-23.3\%$).
* **Energy scaling:** $E_{\text{sw}}$ falls from $0.726\,\text{fJ}$ ($1.00\,\text{V}$) to $0.072\,\text{fJ}$ ($0.35\,\text{V}$), a $10.1\times$ reduction.
* **Historical keeper retention:** the unmodified historical runs with $W_{kp}=45$ and $90\,\text{nm}$ used $T_{\text{stop}}=15.0\,\mu\text{s}$ (bound $f_{\min} < 1/(2\times 15\,\mu\text{s}) \approx 33.3\,\text{kHz}$).

---

## 5. Generated Scientific Figures (300 DPI)

Generated by [`scripts/generar_figuras_act5.py`](scripts/generar_figuras_act5.py):
1. [`figuras/fig1_act5_feedthrough_energia.png`](figuras/fig1_act5_feedthrough_energia.png): Clock feedthrough dynamics with/without PMOS keeper and NTV cycle energy / peak current scaling.
2. [`figuras/fig2_act5_ventana_frecuencia_ntv.png`](figuras/fig2_act5_ventana_frecuencia_ntv.png): Semilog $t_{\text{eval}}$ / $t_{\text{hold}}$ curves and operable frequency window $[f_{\min}, f_{\max}]$ vs. $V_{DD}$.

---

## 6. Published File Inventory (`act5/`)

* **Netlists (`circuitos/`):** `act5_feedthrough_keeper.cir`, `act5_ntv_teval_fmax.cir`, `act5_ntv_thold_fmin.cir`, `act5_ntv_thold_85c.cir`, `act5_hp_vs_lp_subumbral.cir`, `act5_energia_ntv.cir`.
* **Data & Scripts:** [`resultados/datos/act5_metricas.json`](resultados/datos/act5_metricas.json), [`scripts/generar_figuras_act5.py`](scripts/generar_figuras_act5.py).
* **Figures:** [`figuras/fig1_act5_feedthrough_energia.png`](figuras/fig1_act5_feedthrough_energia.png), [`figuras/fig2_act5_ventana_frecuencia_ntv.png`](figuras/fig2_act5_ventana_frecuencia_ntv.png).
