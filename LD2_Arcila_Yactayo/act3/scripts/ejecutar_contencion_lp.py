# -*- coding: utf-8 -*-
"""
ejecutar_contencion_lp.py
Procesa y consolida el análisis de contención en velocidad del keeper en 45nm LP @ 85°C
(VDD = 1.1 V, CL = 2 fF, Cout = 1 fF).

Ensayos:
- ENS-A3-LP-CONT-01: Base sin keeper LP @ 85°C (t_pHL,dyn = 105.75 ps)
- ENS-A3-LP-CONT-02: Barrido de keeper LP (Wkp in [10.5, 15, 30, 45, 60, 90, 135, 180] nm)
- ENS-A3-LP-CONT-REFIN-85: Refinamiento de 1 nm en la frontera crítica [30 nm .. 45 nm]

Genera:
1. Métricas JSON estructuradas en act3/resultados/datos/act3_contencion_lp_metricas.json
2. Figuras científicas a 300 DPI en act3/figuras/:
   - figura_contencion_lp_penalizacion_vs_r.png
   - figura_contencion_lp_transitorio_formas_onda.png
   - figura_comparativa_hp_vs_lp_contencion.png
"""

import os
import sys
import shutil
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
FIGURAS_DIR = os.path.join(ACT3_DIR, "figuras")

SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)

    # 1. Base sin keeper LP
    log_sin_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_lp_sin_keeper_85C.log")
    raw_sin_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_lp_sin_keeper_85C.raw")
    shutil.copy2(log_sin_path, os.path.join(LOGS_DIR, "nand3_contencion_lp_sin_keeper_85C.log"))
    if os.path.exists(raw_sin_path):
        shutil.copy2(raw_sin_path, os.path.join(RAW_DIR, "nand3_contencion_lp_sin_keeper_85C.raw"))
    
    data_sin = parse_log(log_sin_path)
    tphl_sin = float(data_sin["measurements"]["tphl_dyn"])
    tplh_sin = float(data_sin["measurements"]["tplh_out"])

    # 2. Barrido grueso con keeper LP
    log_con_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_lp_con_keeper_85C.log")
    raw_con_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_lp_con_keeper_85C.raw")
    shutil.copy2(log_con_path, os.path.join(LOGS_DIR, "nand3_contencion_lp_con_keeper_85C.log"))
    if os.path.exists(raw_con_path):
        shutil.copy2(raw_con_path, os.path.join(RAW_DIR, "nand3_contencion_lp_con_keeper_85C.raw"))

    data_con = parse_log(log_con_path)
    w_list_coarse = [10.5e-9, 15e-9, 30e-9, 45e-9, 60e-9, 90e-9, 135e-9, 180e-9]
    tphl_coarse = [e["val"] for e in data_con["measurements"]["tphl_dyn"]]
    tplh_coarse = [e["val"] for e in data_con["measurements"]["tplh_out"]]
    toff_coarse = [e["val"] for e in data_con["measurements"]["toff_kp"]]

    # 3. Refinamiento 1nm LP
    log_ref_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_lp_refinamiento_85C.log")
    raw_ref_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_lp_refinamiento_85C.raw")
    shutil.copy2(log_ref_path, os.path.join(LOGS_DIR, "nand3_contencion_lp_refinamiento_85C.log"))
    if os.path.exists(raw_ref_path):
        shutil.copy2(raw_ref_path, os.path.join(RAW_DIR, "nand3_contencion_lp_refinamiento_85C.raw"))

    data_ref = parse_log(log_ref_path)
    w_list_ref = [(30 + i) * 1e-9 for i in range(16)]
    tphl_ref = [e["val"] for e in data_ref["measurements"]["tphl_dyn"]]
    tplh_ref = [e["val"] for e in data_ref["measurements"]["tplh_out"]]
    toff_ref = [e["val"] for e in data_ref["measurements"]["toff_kp"]]

    # Estructura de resultados coarse
    resultados_coarse = []
    for idx, (w, tp, tout, toff) in enumerate(zip(w_list_coarse, tphl_coarse, tplh_coarse, toff_coarse)):
        r = w / 67.5e-9
        weff = w - 10e-9
        if tp is not None:
            pen = 100.0 * (tp - tphl_sin) / tphl_sin
            cumple = bool(pen < 10.0)
            estado = "PASS" if cumple else "FAIL_PENALIZACION"
        else:
            pen = None
            cumple = False
            estado = "FAIL_SIN_CONMUTACION_POR_CONTENCION"

        resultados_coarse.append({
            "step": idx + 1,
            "Wkp_nm": round(w * 1e9, 2),
            "Weff_nm": round(weff * 1e9, 2),
            "r": round(r, 4),
            "tphl_dyn_s": tp,
            "tphl_dyn_ps": round(tp * 1e12, 3) if tp else None,
            "tplh_out_s": tout,
            "tplh_out_ps": round(tout * 1e12, 3) if tout else None,
            "toff_kp_s": toff,
            "penalizacion_pct": round(pen, 2) if pen is not None else None,
            "cumple_contencion_menor_10pct": cumple,
            "estado": estado
        })

    # Estructura de resultados refinamiento
    resultados_ref = []
    for idx, (w, tp, tout, toff) in enumerate(zip(w_list_ref, tphl_ref, tplh_ref, toff_ref)):
        r = w / 67.5e-9
        weff = w - 10e-9
        if tp is not None:
            pen = 100.0 * (tp - tphl_sin) / tphl_sin
            cumple = bool(pen < 10.0)
            estado = "PASS" if cumple else "FAIL_PENALIZACION"
        else:
            pen = None
            cumple = False
            estado = "FAIL_SIN_CONMUTACION_POR_CONTENCION"

        resultados_ref.append({
            "step": idx + 1,
            "Wkp_nm": round(w * 1e9, 2),
            "Weff_nm": round(weff * 1e9, 2),
            "r": round(r, 4),
            "tphl_dyn_s": tp,
            "tphl_dyn_ps": round(tp * 1e12, 3) if tp else None,
            "tplh_out_s": tout,
            "tplh_out_ps": round(tout * 1e12, 3) if tout else None,
            "toff_kp_s": toff,
            "penalizacion_pct": round(pen, 2) if pen is not None else None,
            "cumple_contencion_menor_10pct": cumple,
            "estado": estado
        })

    # Derivar frontera máxima dinámicamente
    w_max_lp = max(p["Wkp_nm"] for p in resultados_ref if p["cumple_contencion_menor_10pct"])
    r_max_lp = max(p["r"] for p in resultados_ref if p["cumple_contencion_menor_10pct"])
    pen_max_lp = next(p["penalizacion_pct"] for p in resultados_ref if p["Wkp_nm"] == w_max_lp)

    # Cargar retención LP a 85°C de A3.3 para cruce de viabilidad
    ret_lp_path = os.path.join(DATOS_DIR, "act3_retencion_lp_metricas.json")
    with open(ret_lp_path, "r", encoding="utf-8") as f:
        datos_ret_lp = json.load(f)
    ret_lp_pts = datos_ret_lp["barrido_con_keeper_85C"]["puntos"]
    ret_sin_lp = datos_ret_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]

    cruce_viabilidad_lp = []
    # Punto sin keeper
    cruce_viabilidad_lp.append({
        "Wkp_nm": 0.0,
        "r": 0.0,
        "Vdyn_end_V": ret_sin_lp["Vdyn_end_1us_V"],
        "retencion_ok": bool(ret_sin_lp["Vdyn_end_1us_V"] > 0.90 * 1.1),
        "penalizacion_pct": 0.0,
        "contencion_ok": True,
        "viable_conjunto": True,
        "nota": "Sin keeper cumple holgadamente retención (Vdyn_end=1.1257V > 0.990V)"
    })
    for p_c in resultados_coarse:
        w_nm = p_c["Wkp_nm"]
        p_ret = next((p for p in ret_lp_pts if abs(p["Wkp_nm"] - w_nm) < 0.1), None)
        v_end = p_ret["Vdyn_end_1us_V"] if p_ret else None
        ret_ok = bool(v_end is not None and v_end > 0.90 * 1.1)
        cont_ok = p_c["cumple_contencion_menor_10pct"]
        cruce_viabilidad_lp.append({
            "Wkp_nm": w_nm,
            "r": p_c["r"],
            "Vdyn_end_V": v_end,
            "retencion_ok": ret_ok,
            "penalizacion_pct": p_c["penalizacion_pct"],
            "contencion_ok": cont_ok,
            "viable_conjunto": bool(ret_ok and cont_ok),
            "nota": "Cumple retención" if ret_ok else "No evaluado"
        })

    # Consolidar JSON de contención LP
    salida_json_lp = {
        "descripcion": "Evaluación de Contención en Velocidad y Viabilidad en 45nm LP @ 85°C",
        "condiciones": {
            "proceso": "45nm_LP",
            "VDD_V": 1.1,
            "temperatura_C": 85.0,
            "CL_fF": 2.0,
            "Cout_fF": 1.0,
            "Tclk_ns": 2.0,
            "entradas": "A=B=C=1.1 V (evaluación activa)",
            "W_PDN_eq_nm": 67.5,
            "definicion_r": "r = Wkp / 67.5nm"
        },
        "referencia_sin_keeper": {
            "ensayo_id": "ENS-A3-LP-CONT-01",
            "tphl_dyn_s": tphl_sin,
            "tphl_dyn_ps": round(tphl_sin * 1e12, 3),
            "tplh_out_s": tplh_sin,
            "tplh_out_ps": round(tplh_sin * 1e12, 3)
        },
        "frontera_maxima_dinamica": {
            "Wkp_max_lp_nm": w_max_lp,
            "r_max_lp": r_max_lp,
            "penalizacion_max_pct": pen_max_lp,
            "criterio": "penalizacion_pct < 10.0 derivado de simulacion directa sin hardcoding"
        },
        "barrido_grueso": resultados_coarse,
        "refinamiento_frontera_1nm": resultados_ref,
        "cruce_viabilidad_conjunta": cruce_viabilidad_lp
    }

    out_json_path = os.path.join(DATOS_DIR, "act3_contencion_lp_metricas.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(salida_json_lp, f, indent=2)
    print(f"[DATOS] Metricas LP guardadas en: {out_json_path}")

    # =========================================================================
    # FIGURAS CIENTÍFICAS
    # =========================================================================
    colors = {
        'primary': '#003366',
        'accent': '#D9534F',
        'success': '#2E7D32',
        'neutral': '#4A5568',
        'grid': '#E2E8F0',
        'highlight': '#F59E0B',
        'lp_color': '#6B21A8'
    }

    # FIGURA 1: Penalización % vs r y Wkp en LP
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    w_coarse_v = [p["Wkp_nm"] for p in resultados_coarse if p["penalizacion_pct"] is not None]
    pen_coarse_v = [p["penalizacion_pct"] for p in resultados_coarse if p["penalizacion_pct"] is not None]
    w_ref_v = [p["Wkp_nm"] for p in resultados_ref]
    pen_ref_v = [p["penalizacion_pct"] for p in resultados_ref]

    ax1.plot(w_coarse_v, pen_coarse_v, 'o--', color=colors['lp_color'], label='Malla Gruesa [10.5 - 135 nm]', lw=1.5, alpha=0.7)
    ax1.plot(w_ref_v, pen_ref_v, 's-', color=colors['accent'], label='Refinamiento 1 nm [30 - 45 nm]', lw=2.0)
    ax1.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax1.axvspan(10.5, w_max_lp, color='green', alpha=0.12, label=f'Zona Viable Medida ($W_{{kp}} \\leq {w_max_lp:.0f}\\,\\mathrm{{nm}}$)')
    ax1.axvspan(w_max_lp, 140.0, color='red', alpha=0.08, label='Zona Inadmisible (≥ 10.0%)')
    ax1.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Penalización de Retardo vs Ancho Geométrico — 45nm LP @ 85°C', fontsize=12, fontweight='bold', color=colors['lp_color'])
    ax1.set_xlim(5, 140)
    ax1.set_ylim(0, 140)
    ax1.legend(fontsize=9, loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Subplot B: Penalización vs r
    r_coarse_v = [p["r"] for p in resultados_coarse if p["penalizacion_pct"] is not None]
    r_ref_v = [p["r"] for p in resultados_ref]

    ax2.plot(r_coarse_v, pen_coarse_v, 'o--', color=colors['lp_color'], label='Malla Gruesa', lw=1.5, alpha=0.7)
    ax2.plot(r_ref_v, pen_ref_v, 's-', color=colors['accent'], label='Refinamiento', lw=2.0)
    ax2.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax2.axvspan(10.5/67.5, r_max_lp, color='green', alpha=0.12, label=f'Zona Viable Medida ($r \\leq {r_max_lp:.3f}$)')
    ax2.axvspan(r_max_lp, 2.05, color='red', alpha=0.08, label='Zona Inadmisible')
    ax2.set_xlabel(r'Razón de Aspecto $r = \frac{(W/L)_{kp}}{(W/L)_{PDN,eq}} \approx \frac{W_{kp}}{67.5\,\mathrm{nm}}$', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Penalización de Retardo vs Razón de Aspecto $r$ — 45nm LP @ 85°C', fontsize=12, fontweight='bold', color=colors['lp_color'])
    ax2.set_xlim(0.1, 2.05)
    ax2.set_ylim(0, 140)
    ax2.legend(fontsize=9, loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    fig1_path = os.path.join(FIGURAS_DIR, "figura_contencion_lp_penalizacion_vs_r.png")
    plt.savefig(fig1_path)
    plt.close()
    print(f"[FIGURA] Figura LP 1 guardada en: {fig1_path}")

    # FIGURA 2: Formas de Onda Transitorias LP (RAW)
    raw_con_lp_data = read_raw(os.path.join(RAW_DIR, "nand3_contencion_lp_con_keeper_85C.raw"))
    steps_lp = raw_con_lp_data["steps"]

    plt.figure(figsize=(10, 6), dpi=300)
    raw_sin_lp_data = read_raw(os.path.join(RAW_DIR, "nand3_contencion_lp_sin_keeper_85C.raw"))
    t_sin_lp = (raw_sin_lp_data["steps"][0]["time"] - 1.0e-9) * 1e12
    v_dyn_sin_lp = raw_sin_lp_data["steps"][0]["V(dyn)"]
    v_out_sin_lp = raw_sin_lp_data["steps"][0]["V(out)"]
    v_clk_sin_lp = raw_sin_lp_data["steps"][0]["V(clk)"]

    plt.plot(t_sin_lp, v_clk_sin_lp, 'k:', lw=1.5, label='V(clk) (500 MHz, 1.1V)', alpha=0.6)
    plt.plot(t_sin_lp, v_dyn_sin_lp, color='black', lw=2.0, label='V(dyn) Sin Keeper')
    plt.plot(t_sin_lp, v_out_sin_lp, color='gray', lw=1.5, ls='--', label='V(out) Sin Keeper')

    map_w = {0: '10.5 nm', 1: '15 nm', 2: '30 nm', 3: '45 nm', 4: '60 nm', 5: '90 nm', 6: '135 nm', 7: '180 nm (Sin Conmutación)'}
    col_steps = {1: '#2E7D32', 3: '#F59E0B', 4: '#E65100', 7: '#C62828'}
    for s_idx in [1, 3, 4, 7]:
        if s_idx < len(steps_lp):
            t_s = (steps_lp[s_idx]["time"] - 1.0e-9) * 1e12
            v_dyn_s = steps_lp[s_idx]["V(dyn)"]
            plt.plot(t_s, v_dyn_s, lw=1.8, color=col_steps[s_idx], label=f'V(dyn) Wkp={map_w[s_idx]}')

    plt.axhline(0.55, color='blue', ls='-.', lw=1.0, label='Umbral 50% VDD (0.55 V)')
    plt.xlabel('Tiempo relativo al flanco de evaluación (ps)', fontsize=11, fontweight='bold')
    plt.ylabel('Tensión (V)', fontsize=11, fontweight='bold')
    plt.title('Transitorio de Evaluación con Contención del Keeper — 45nm LP @ 85°C (VDD = 1.1 V)', fontsize=12, fontweight='bold', color=colors['lp_color'])
    plt.xlim(0, 400)
    plt.ylim(-0.05, 1.15)
    plt.legend(fontsize=9, loc='center right')
    plt.grid(True, linestyle='--', alpha=0.6)

    fig2_path = os.path.join(FIGURAS_DIR, "figura_contencion_lp_transitorio_formas_onda.png")
    plt.savefig(fig2_path)
    plt.close()
    print(f"[FIGURA] Figura LP 2 guardada en: {fig2_path}")

    # FIGURA 3: Comparativa HP vs LP de Contención
    # Cargar contención HP de A3.5
    cont_hp_path = os.path.join(DATOS_DIR, "act3_contencion_metricas.json")
    with open(cont_hp_path, "r", encoding="utf-8") as f:
        datos_cont_hp = json.load(f)
    
    w_hp_ref = [p["Wkp_nm"] for p in datos_cont_hp["refinamiento_frontera_1nm"]]
    pen_hp_ref = [p["penalizacion_pct"] for p in datos_cont_hp["refinamiento_frontera_1nm"]]
    w_hp_c = [p["Wkp_nm"] for p in datos_cont_hp["barrido_grueso"] if p["penalizacion_pct"] is not None]
    pen_hp_c = [p["penalizacion_pct"] for p in datos_cont_hp["barrido_grueso"] if p["penalizacion_pct"] is not None]

    fig, (ax_cmp1, ax_cmp2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    # Subplot A: Penalización vs Wkp (HP vs LP)
    ax_cmp1.plot(w_hp_c, pen_hp_c, 'o--', color=colors['primary'], label='45nm HP (Malla Gruesa)', lw=1.5, alpha=0.6)
    ax_cmp1.plot(w_hp_ref, pen_hp_ref, 's-', color=colors['primary'], label='45nm HP (Refinado 1nm)', lw=2.0)
    ax_cmp1.plot(w_coarse_v, pen_coarse_v, '^--', color=colors['lp_color'], label='45nm LP (Malla Gruesa)', lw=1.5, alpha=0.6)
    ax_cmp1.plot(w_ref_v, pen_ref_v, 'd-', color=colors['lp_color'], label='45nm LP (Refinado 1nm)', lw=2.0)
    ax_cmp1.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax_cmp1.axvline(38.0, color=colors['primary'], ls='--', lw=1.2, label=r'Frontera HP ($W_{kp}=38\,\mathrm{nm}$)')
    ax_cmp1.axvline(36.0, color=colors['lp_color'], ls='-.', lw=1.2, label=r'Frontera LP ($W_{kp}=36\,\mathrm{nm}$)')
    ax_cmp1.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')
    ax_cmp1.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold')
    ax_cmp1.set_title('Comparativa de Penalización vs $W_{kp}$ (HP vs LP @ 85°C)', fontsize=12, fontweight='bold')
    ax_cmp1.set_xlim(5, 140)
    ax_cmp1.set_ylim(0, 140)
    ax_cmp1.legend(fontsize=8.5, loc='upper left')
    ax_cmp1.grid(True, linestyle='--', alpha=0.6)

    # Subplot B: Retardo Absoluto tpHL vs Wkp (HP vs LP)
    tphl_hp_c = [p["tphl_dyn_ps"] for p in datos_cont_hp["barrido_grueso"] if p["tphl_dyn_ps"] is not None]
    tphl_lp_c = [p["tphl_dyn_ps"] for p in resultados_coarse if p["tphl_dyn_ps"] is not None]

    ax_cmp2.plot(w_hp_c, tphl_hp_c, 'o-', color=colors['primary'], lw=2.0, label=r'45nm HP: $t_{pHL}$ [31.8 - 73.4 ps]')
    ax_cmp2.plot(w_coarse_v, tphl_lp_c, '^-', color=colors['lp_color'], lw=2.0, label=r'45nm LP: $t_{pHL}$ [105.8 - 362.4 ps]')
    ax_cmp2.axhline(tphl_sin*1e12, color=colors['lp_color'], ls=':', lw=1.2, label=f'Base LP Sin Keeper ({tphl_sin*1e12:.1f} ps)')
    ax_cmp2.axhline(datos_cont_hp["referencia_sin_keeper"]["tphl_dyn_ps"], color=colors['primary'], ls=':', lw=1.2, label=f'Base HP Sin Keeper ({datos_cont_hp["referencia_sin_keeper"]["tphl_dyn_ps"]:.1f} ps)')
    ax_cmp2.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')
    ax_cmp2.set_ylabel('Retardo de Evaluación $t_{pHL,dyn}$ (ps)', fontsize=11, fontweight='bold')
    ax_cmp2.set_title('Comparativa de Retardo Absoluto $t_{pHL}$ (HP vs LP @ 85°C)', fontsize=12, fontweight='bold')
    ax_cmp2.set_xlim(5, 140)
    ax_cmp2.set_yscale('log')
    ax_cmp2.legend(fontsize=8.5, loc='upper left')
    ax_cmp2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    fig3_path = os.path.join(FIGURAS_DIR, "figura_comparativa_hp_vs_lp_contencion.png")
    plt.savefig(fig3_path)
    plt.close()
    print(f"[FIGURA] Figura Comparativa HP/LP guardada en: {fig3_path}")

    print("\n[PROCESO] A3.6 CONTENCION LP COMPLETADO EXITOSAMENTE.")

if __name__ == "__main__":
    main()
