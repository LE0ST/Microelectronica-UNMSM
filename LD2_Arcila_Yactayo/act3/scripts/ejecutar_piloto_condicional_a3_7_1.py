# -*- coding: utf-8 -*-
"""
ejecutar_piloto_condicional_a3_7_1.py
Ejecuta y procesa el piloto controlado del Keeper Condicional (Fase A3.7.1)
en tecnología 45nm HP a 85°C (VDD = 1.0 V, CL = 2 fF, Cout = 1 fF).

Ensayos:
- ENS-A3-COND-PILOT-01: Piloto A - Descarga intencional (A=B=C=1)
- ENS-A3-COND-PILOT-02: Piloto B - Retencion real de 1.0 us (A=B=C=0)
- ENS-A3-COND-PILOT-03: Piloto C - Charge sharing preliminar (A=B=1, C=0)

Genera:
1. Metricas JSON en act3/resultados/datos/act3_piloto_condicional.json
2. Figuras cientificas a 300 DPI en act3/figuras/:
   - fig_a3_7_piloto_a_contencion.png
   - fig_a3_7_piloto_b_retencion.png
   - fig_a3_7_piloto_c_chargesharing.png
"""

import os
import sys
import shutil
import subprocess
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
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

def simular_netlist(cir_name):
    cir_path = os.path.join(CIRCUITOS_DIR, cir_name)
    base_name = os.path.splitext(cir_name)[0]
    print(f"\n[SPICE] Ejecutando: {cir_name} ...")
    res = subprocess.run([LTSPICE_EXE, "-b", cir_path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] LTspice fallo con codigo {res.returncode}")
        print(res.stderr)
        sys.exit(1)
        
    src_log = os.path.join(CIRCUITOS_DIR, base_name + ".log")
    src_raw = os.path.join(CIRCUITOS_DIR, base_name + ".raw")
    dst_log = os.path.join(LOGS_DIR, base_name + ".log")
    dst_raw = os.path.join(RAW_DIR, base_name + ".raw")
    
    if os.path.exists(src_log):
        shutil.copy2(src_log, dst_log)
    if os.path.exists(src_raw):
        shutil.copy2(src_raw, dst_raw)
    return dst_log, dst_raw

def find_crossing(t, y, val, direction='both', t_min=None, t_max=None):
    """Encuentra el instante exacto por interpolacion lineal cuando y cruza val."""
    mask = np.ones_like(t, dtype=bool)
    if t_min is not None:
        mask = mask & (t >= t_min)
    if t_max is not None:
        mask = mask & (t <= t_max)
    t_sub = t[mask]
    y_sub = y[mask]
    if len(t_sub) < 2:
        return None
    diff = y_sub - val
    for i in range(len(diff) - 1):
        if diff[i] == 0:
            return float(t_sub[i])
        if diff[i] * diff[i+1] < 0:
            if direction == 'rise' and diff[i+1] <= diff[i]:
                continue
            if direction == 'fall' and diff[i+1] >= diff[i]:
                continue
            # Interpolacion lineal
            t_cross = t_sub[i] + (0 - diff[i]) * (t_sub[i+1] - t_sub[i]) / (diff[i+1] - diff[i])
            return float(t_cross)
    return None

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)
    
    resultados = {
        "metadata": {
            "fase": "A3.7.1",
            "tecnologia": "45nm HP",
            "temperatura_C": 85,
            "VDD_V": 1.0,
            "CL_fF": 2.0,
            "Cout_fF": 1.0,
            "Wkp_fb_nm": 45.0,
            "Wkp_en_nm": 45.0,
            "topologia_keeper": "Mk_fb (out) en serie con Mk_en (d3) + 3 inversores desde CLK"
        }
    }

    # =========================================================================
    # 1. PILOTO A: DESCARGA INTENCIONAL (A=B=C=1)
    # =========================================================================
    cir_a = "nand3_condicional_hp_contencion_pilot_85C.cir"
    log_a, raw_a = simular_netlist(cir_a)
    data_log_a = parse_log(log_a)
    raw_data_a = read_raw(raw_a)
    
    t_a = raw_data_a['data']['time']
    v_clk_a = raw_data_a['data']['V(clk)']
    v_dyn_a = raw_data_a['data']['V(dyn)']
    v_out_a = raw_data_a['data']['V(out)']
    v_d3_a = raw_data_a['data']['V(d3)']
    v_kmid_a = raw_data_a['data']['V(k_mid)']
    
    # Corrientes:
    # Ikp hacia dyn: -Id(Mk_en) o Is(Mk_fb)
    # En raw, busquemos los nombres exactos de corrientes disponibles
    var_names = list(raw_data_a['data'].keys())
    
    # Identificar variables de corriente
    ikp_var = None
    for cand in ['-Id(Mk_en)', 'Id(Mk_en)', 'Is(Mk_en)', 'Is(Mk_fb)', 'Id(Mk_fb)']:
        if cand in var_names:
            ikp_var = cand
            break
    ipdn_var = None
    for cand in ['Is(M1)', 'Id(M1)', 'Is(Mf)', 'Id(Mf)']:
        if cand in var_names:
            ipdn_var = cand
            break

    # Orientar correctamente: Ikp entrando a dyn, Ipdn saliendo de dyn hacia tierra
    if 'Id(Mk_en)' in var_names:
        i_kp_a = -raw_data_a['data']['Id(Mk_en)']
    elif 'Is(Mk_fb)' in var_names:
        i_kp_a = raw_data_a['data']['Is(Mk_fb)']
    else:
        i_kp_a = np.zeros_like(t_a)

    if 'Is(M1)' in var_names:
        i_pdn_a = raw_data_a['data']['Is(M1)']
    elif 'Id(M1)' in var_names:
        i_pdn_a = -raw_data_a['data']['Id(M1)']
    else:
        i_pdn_a = np.zeros_like(t_a)

    # Mediciones temporales sobre flanco ascendente en t=1.0ns
    t_clk_rise = find_crossing(t_a, v_clk_a, 0.5, 'rise', t_min=0.99e-9, t_max=1.05e-9)
    t_d3_fall = find_crossing(t_a, v_d3_a, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_dyn_50 = find_crossing(t_a, v_dyn_a, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_out_10 = find_crossing(t_a, v_out_a, 0.1, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    t_out_50 = find_crossing(t_a, v_out_a, 0.5, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    t_out_90 = find_crossing(t_a, v_out_a, 0.9, 'rise', t_min=1.00e-9, t_max=1.15e-9)

    tpHL_dyn = (t_dyn_50 - t_clk_rise) if (t_dyn_50 and t_clk_rise) else None
    tpLH_out = (t_out_50 - t_clk_rise) if (t_out_50 and t_clk_rise) else None
    tau_delay_3inv = (t_d3_fall - t_clk_rise) if (t_d3_fall and t_clk_rise) else None

    # Referencias historicas fijadas en A3
    tpHL_sin = 31.7994e-12
    tpLH_sin = 51.1520e-12
    tpHL_conv_45 = 35.9008e-12
    tpLH_conv_45 = 57.9982e-12

    penalizacion_pct = ((tpHL_dyn - tpHL_sin) / tpHL_sin) * 100.0 if tpHL_dyn else None
    penalizacion_conv_pct = ((tpHL_conv_45 - tpHL_sin) / tpHL_sin) * 100.0

    # Analisis de Contencion Residual:
    # Intervalo donde PDN conduce (Ipdn > 1uA) Y Keeper conduce (Ikp > 1uA)
    mask_eval = (t_a >= 1.00e-9) & (t_a <= 1.15e-9)
    t_eval = t_a[mask_eval]
    ikp_eval = i_kp_a[mask_eval]
    ipdn_eval = i_pdn_a[mask_eval]

    umbral_i = 1.0e-6 # 1.0 uA
    mask_overlap = (ikp_eval > umbral_i) & (ipdn_eval > umbral_i)
    
    if np.any(mask_overlap):
        t_overlap_start = float(t_eval[mask_overlap][0])
        t_overlap_end = float(t_eval[mask_overlap][-1])
        duracion_overlap_ps = (t_overlap_end - t_overlap_start) * 1e12
        ikp_peak_overlap_uA = float(np.max(ikp_eval[mask_overlap])) * 1e6
        contencion_residual_detectada = True
    else:
        t_overlap_start = None
        t_overlap_end = None
        duracion_overlap_ps = 0.0
        ikp_peak_overlap_uA = 0.0
        contencion_residual_detectada = False

    piloto_a_res = {
        "ensayo_id": "ENS-A3-COND-PILOT-01",
        "descripcion": "Piloto A - Descarga intencional con entradas en 1 (45nm HP @ 85C)",
        "t_clk_rise_ps": float(t_clk_rise * 1e12) if t_clk_rise else None,
        "t_d3_fall_ps": float(t_d3_fall * 1e12) if t_d3_fall else None,
        "t_dyn_50_ps": float(t_dyn_50 * 1e12) if t_dyn_50 else None,
        "t_out_10_ps": float(t_out_10 * 1e12) if t_out_10 else None,
        "t_out_50_ps": float(t_out_50 * 1e12) if t_out_50 else None,
        "t_out_90_ps": float(t_out_90 * 1e12) if t_out_90 else None,
        "tpHL_dyn_ps": float(tpHL_dyn * 1e12) if tpHL_dyn else None,
        "tpLH_out_ps": float(tpLH_out * 1e12) if tpLH_out else None,
        "tau_delay_3inv_ps": float(tau_delay_3inv * 1e12) if tau_delay_3inv else None,
        "referencias_comparativas": {
            "sin_keeper": {
                "tpHL_dyn_ps": float(tpHL_sin * 1e12),
                "tpLH_out_ps": float(tpLH_sin * 1e12)
            },
            "keeper_convencional_45nm": {
                "tpHL_dyn_ps": float(tpHL_conv_45 * 1e12),
                "tpLH_out_ps": float(tpLH_conv_45 * 1e12),
                "penalizacion_pct": float(penalizacion_conv_pct)
            }
        },
        "penalizacion_pct_vs_sin": float(penalizacion_pct) if penalizacion_pct is not None else None,
        "cumple_criterio_10pct": bool(penalizacion_pct < 10.0) if penalizacion_pct is not None else False,
        "contencion_residual": {
            "detectada": contencion_residual_detectada,
            "t_inicio_ps": float(t_overlap_start * 1e12) if t_overlap_start else None,
            "t_fin_ps": float(t_overlap_end * 1e12) if t_overlap_end else None,
            "duracion_ps": float(duracion_overlap_ps),
            "ikp_pico_uA": float(ikp_peak_overlap_uA)
        }
    }
    resultados["piloto_a"] = piloto_a_res

    # =========================================================================
    # 2. PILOTO B: RETENCIÓN REAL DE 1.0 us (A=B=C=0)
    # =========================================================================
    cir_b = "nand3_condicional_hp_retencion_pilot_85C.cir"
    log_b, raw_b = simular_netlist(cir_b)
    data_log_b = parse_log(log_b)
    raw_data_b = read_raw(raw_b)

    t_b = raw_data_b['data']['time']
    v_dyn_b = raw_data_b['data']['V(dyn)']
    v_out_b = raw_data_b['data']['V(out)']
    v_d3_b = raw_data_b['data']['V(d3)']
    v_kmid_b = raw_data_b['data']['V(k_mid)']

    vdyn_start = float(v_dyn_b[np.argmin(np.abs(t_b - 0.52e-9))])
    vdyn_end = float(v_dyn_b[-1])
    vdyn_min = float(np.min(v_dyn_b[t_b >= 0.52e-9]))
    vout_end = float(v_out_b[-1])
    vd3_end = float(v_d3_b[-1])
    vkmid_end = float(v_kmid_b[-1])

    # Corrientes terminales al final de 1us
    var_names_b = list(raw_data_b['data'].keys())
    if 'Id(Mk_en)' in var_names_b:
        irest_end = float(-raw_data_b['data']['Id(Mk_en)'][-1])
    elif 'Is(Mk_fb)' in var_names_b:
        irest_end = float(raw_data_b['data']['Is(Mk_fb)'][-1])
    else:
        irest_end = None

    if 'Is(M1)' in var_names_b:
        ileak_end = float(raw_data_b['data']['Is(M1)'][-1])
    elif 'Id(M1)' in var_names_b:
        ileak_end = float(-raw_data_b['data']['Id(M1)'][-1])
    else:
        ileak_end = None

    # Corriente de alimentacion media
    meas_log_b = data_log_b.get('measurements', {})
    isupply_avg = meas_log_b.get('isupply_avg', None)
    t_cross_0p9 = meas_log_b.get('t_cross_0p9vdd', None)
    censurado_0p9 = (t_cross_0p9 is None)

    cumple_retencion = bool(vdyn_end >= 0.900)

    piloto_b_res = {
        "ensayo_id": "ENS-A3-COND-PILOT-02",
        "descripcion": "Piloto B - Retencion real de 1.0us continuo (45nm HP @ 85C, A=B=C=0)",
        "t0_inicio_eval_ns": 0.52,
        "t_fin_eval_us": float(t_b[-1] * 1e6),
        "vdyn_start_V": vdyn_start,
        "vdyn_end_1us_V": vdyn_end,
        "vdyn_min_V": vdyn_min,
        "vout_end_V": vout_end,
        "vd3_end_V": vd3_end,
        "vkmid_end_V": vkmid_end,
        "irest_end_nA": float(irest_end * 1e9) if irest_end is not None else None,
        "ileak_pdn_end_nA": float(ileak_end * 1e9) if ileak_end is not None else None,
        "isupply_avg_nA": float(isupply_avg * 1e9) if isupply_avg is not None else None,
        "t_cross_0p9vdd_ns": float(t_cross_0p9 * 1e9) if t_cross_0p9 is not None else None,
        "censurado_0p9": censurado_0p9,
        "d3_habilita_durante_toda_retencion": bool(vd3_end < 0.05),
        "cumple_retencion_1us": cumple_retencion
    }
    resultados["piloto_b"] = piloto_b_res

    # =========================================================================
    # 3. PILOTO C: CHARGE SHARING PRELIMINAR (A=B=1, C=0)
    # =========================================================================
    # Ejecutamos Piloto C si A y B concluyen operacion basica
    cir_c = "nand3_condicional_hp_cs_pilot_85C.cir"
    log_c, raw_c = simular_netlist(cir_c)
    data_log_c = parse_log(log_c)
    raw_data_c = read_raw(raw_c)

    t_c = raw_data_c['data']['time']
    v_dyn_c = raw_data_c['data']['V(dyn)']
    v_out_c = raw_data_c['data']['V(out)']
    v_clk_c = raw_data_c['data']['V(clk)']
    v_d3_c = raw_data_c['data']['V(d3)']

    # Eval 2 en t in [3.0ns, 4.0ns]
    mask_eval2 = (t_c >= 3.00e-9) & (t_c <= 4.00e-9)
    t_eval2 = t_c[mask_eval2]
    vdyn_eval2 = v_dyn_c[mask_eval2]
    vout_eval2 = v_out_c[mask_eval2]

    vdyn_cs_min = float(np.min(vdyn_eval2))
    vout_cs_max = float(np.max(vout_eval2))
    dV_drop = float(1.0 - vdyn_cs_min)
    vdyn_end_cs = float(v_dyn_c[np.argmin(np.abs(t_c - 3.95e-9))])
    vout_end_cs = float(v_out_c[np.argmin(np.abs(t_c - 3.95e-9))])

    t_clk_rise2 = find_crossing(t_c, v_clk_c, 0.5, 'rise', t_min=2.99e-9, t_max=3.05e-9)
    t_d3_fall2 = find_crossing(t_c, v_d3_c, 0.5, 'fall', t_min=3.00e-9, t_max=3.10e-9)
    tau_delay_cs = (t_d3_fall2 - t_clk_rise2) if (t_d3_fall2 and t_clk_rise2) else None

    # Ver si recupera dyn hacia VDD tras la caida
    recupera_dyn = bool(vdyn_end_cs > vdyn_cs_min + 0.5 * dV_drop)

    piloto_c_res = {
        "ensayo_id": "ENS-A3-COND-PILOT-03",
        "descripcion": "Piloto C - Charge sharing preliminar con nodos descargados (45nm HP @ 85C, A=B=1, C=0)",
        "vdyn_min_eval2_V": vdyn_cs_min,
        "vout_max_eval2_V": vout_cs_max,
        "dV_caida_mV": float(dV_drop * 1e3),
        "tau_delay_3inv_ps": float(tau_delay_cs * 1e12) if tau_delay_cs else None,
        "t_d3_act_ps": float((t_d3_fall2 - 3.0e-9) * 1e12) if t_d3_fall2 else None,
        "vdyn_end_eval2_V": vdyn_end_cs,
        "vout_end_eval2_V": vout_end_cs,
        "recuperacion_observada": recupera_dyn
    }
    resultados["piloto_c"] = piloto_c_res

    # =========================================================================
    # 4. GUARDAR RESULTADOS JSON
    # =========================================================================
    json_path = os.path.join(DATOS_DIR, "act3_piloto_condicional.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2)
    print(f"\n[JSON] Metricas guardadas en: {json_path}")

    # =========================================================================
    # 5. GENERAR FIGURAS CIENTÍFICAS (300 DPI)
    # =========================================================================
    print("\n[PLOTS] Generando figuras cientificas...")

    # --- FIGURA A: Piloto A Formas de Onda y Contencion Residual ---
    fig_a, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True, dpi=300)
    
    t_plot_a = (t_a - 1.0e-9) * 1e12 # tiempo en ps relativo al flanco de CLK
    mask_plot_a = (t_plot_a >= -10) & (t_plot_a <= 150)
    
    tp = t_plot_a[mask_plot_a]
    ax1.plot(tp, v_clk_a[mask_plot_a], 'k--', label='CLK', lw=1.5)
    ax1.plot(tp, v_d3_a[mask_plot_a], 'm-', label='d3 (Habilita Mk_en)', lw=1.8)
    ax1.plot(tp, v_dyn_a[mask_plot_a], 'b-', label='dyn', lw=2.0)
    ax1.plot(tp, v_out_a[mask_plot_a], 'r-', label='out (Controla Mk_fb)', lw=2.0)
    ax1.plot(tp, v_kmid_a[mask_plot_a], 'g:', label='k_mid', lw=1.5)
    
    ax1.axhline(0.5, color='gray', linestyle=':', lw=0.8)
    if t_dyn_50:
        ax1.axvline((t_dyn_50 - 1.0e-9)*1e12, color='b', linestyle=':', lw=0.8)
    if t_d3_fall:
        ax1.axvline((t_d3_fall - 1.0e-9)*1e12, color='m', linestyle=':', lw=0.8)
    if t_out_50:
        ax1.axvline((t_out_50 - 1.0e-9)*1e12, color='r', linestyle=':', lw=0.8)

    ax1.set_ylabel('Tension [V]', fontsize=11, fontweight='bold')
    ax1.set_title(r'Piloto A: Descarga Intencional ($A=B=C=1$) — Keeper Condicional (45nm HP @ 85$^\circ$C)', 
                  fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='center right', fontsize=9)
    ax1.set_ylim(-0.05, 1.05)

    # Subplot 2: Corrientes de PDN y Keeper
    ax2.plot(tp, i_pdn_a[mask_plot_a]*1e6, 'b-', label=r'$I_{\mathrm{PDN}}$ (descarga dyn)', lw=1.8)
    ax2.plot(tp, i_kp_a[mask_plot_a]*1e6, 'm-', label=r'$I_{\mathrm{keeper}}$ (hacia dyn)', lw=1.8)
    
    if contencion_residual_detectada:
        t_start_p = (t_overlap_start - 1.0e-9)*1e12
        t_end_p = (t_overlap_end - 1.0e-9)*1e12
        ax2.axvspan(t_start_p, t_end_p, color='orange', alpha=0.25, 
                    label=f'Contencion residual ($\Delta t = {duracion_overlap_ps:.1f}\,$ps)')
        ax2.scatter([(t_start_p+t_end_p)/2], [ikp_peak_overlap_uA], color='darkred', zorder=5,
                    label=f'$I_{{kp,\max}} = {ikp_peak_overlap_uA:.1f}\,\mu$A')

    ax2.set_xlabel('Tiempo relativo al flanco de CLK [ps]', fontsize=11, fontweight='bold')
    ax2.set_ylabel(r'Corriente [$\mu$A]', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=9)
    
    plt.tight_layout()
    fig_a_path = os.path.join(FIGURAS_DIR, "fig_a3_7_piloto_a_contencion.png")
    fig_a.savefig(fig_a_path, dpi=300)
    plt.close(fig_a)
    print(f"  -> Guardada: {fig_a_path}")

    # --- FIGURA B: Piloto B Retención 1.0 us ---
    fig_b, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    t_plot_b_us = t_b * 1e6
    ax.plot(t_plot_b_us, v_dyn_b, 'b-', lw=2.0, label=r'$V(dyn)$')
    ax.plot(t_plot_b_us, v_out_b, 'r--', lw=1.5, label=r'$V(out)$')
    ax.plot(t_plot_b_us, v_d3_b, 'm:', lw=1.5, label=r'$V(d_3)$')
    ax.plot(t_plot_b_us, v_kmid_b, 'g-.', lw=1.2, label=r'$V(k\_mid)$')
    
    ax.axhline(0.900, color='crimson', linestyle='--', lw=1.0, label=r'Criterio $0.90\,V_{DD}$ (0.900 V)')
    ax.set_xlabel(r'Tiempo [$\mu$s]', fontsize=11, fontweight='bold')
    ax.set_ylabel('Tension [V]', fontsize=11, fontweight='bold')
    ax.set_title(r'Piloto B: Retencion Dinamica Continua de $1.0\,\mu$s ($A=B=C=0$, 45nm HP @ 85$^\circ$C)', 
                 fontsize=11, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower left', fontsize=9)
    ax.set_ylim(-0.05, 1.05)
    
    # Inset de inicio
    ax_ins = ax.inset_axes([0.45, 0.25, 0.50, 0.45])
    mask_ins = t_b <= 5e-9
    ax_ins.plot(t_b[mask_ins]*1e9, v_dyn_b[mask_ins], 'b-', lw=1.8)
    ax_ins.plot(t_b[mask_ins]*1e9, v_d3_b[mask_ins], 'm:', lw=1.5)
    ax_ins.plot(t_b[mask_ins]*1e9, v_out_b[mask_ins], 'r--', lw=1.5)
    ax_ins.set_title('Transicion Inicial [0..5 ns]', fontsize=8)
    ax_ins.set_xlabel('Tiempo [ns]', fontsize=8)
    ax_ins.set_ylabel('V [V]', fontsize=8)
    ax_ins.tick_params(labelsize=7)
    ax_ins.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    fig_b_path = os.path.join(FIGURAS_DIR, "fig_a3_7_piloto_b_retencion.png")
    fig_b.savefig(fig_b_path, dpi=300)
    plt.close(fig_b)
    print(f"  -> Guardada: {fig_b_path}")

    # --- FIGURA C: Piloto C Charge Sharing ---
    fig_c, ax_c = plt.subplots(figsize=(8, 4.5), dpi=300)
    t_plot_c_ns = t_c * 1e9
    ax_c.plot(t_plot_c_ns, v_clk_c, 'k--', lw=1.2, label='CLK')
    ax_c.plot(t_plot_c_ns, v_dyn_c, 'b-', lw=2.0, label=r'$V(dyn)$')
    ax_c.plot(t_plot_c_ns, v_out_c, 'r-', lw=1.8, label=r'$V(out)$')
    ax_c.plot(t_plot_c_ns, v_d3_c, 'm:', lw=1.5, label=r'$V(d_3)$')

    ax_c.axvspan(3.0, 4.0, color='yellow', alpha=0.15, label='Evaluacion 2 (Charge Sharing)')
    ax_c.scatter([3.0 + (t_eval2[np.argmin(vdyn_eval2)] - 3.0e-9)*1e9], [vdyn_cs_min], 
                 color='darkblue', zorder=5, label=rf'$V_{{dyn,\min}} = {vdyn_cs_min:.3f}\,$V ($\Delta V = {dV_drop*1e3:.1f}\,$mV)')

    ax_c.set_xlabel('Tiempo [ns]', fontsize=11, fontweight='bold')
    ax_c.set_ylabel('Tension [V]', fontsize=11, fontweight='bold')
    ax_c.set_title(r'Piloto C: Charge Sharing Preliminar ($A=B=1, C=0$, 45nm HP @ 85$^\circ$C)', 
                   fontsize=11, fontweight='bold')
    ax_c.grid(True, linestyle='--', alpha=0.6)
    ax_c.legend(loc='upper right', fontsize=9)
    ax_c.set_ylim(-0.05, 1.05)

    plt.tight_layout()
    fig_c_path = os.path.join(FIGURAS_DIR, "fig_a3_7_piloto_c_chargesharing.png")
    fig_c.savefig(fig_c_path, dpi=300)
    plt.close(fig_c)
    print(f"  -> Guardada: {fig_c_path}")

    print("\n[FIN] Ejecucion de pilotos A3.7.1 completada exitosamente.")

if __name__ == '__main__':
    main()
