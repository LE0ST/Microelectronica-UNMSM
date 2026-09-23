# -*- coding: utf-8 -*-
"""
ejecutar_descomposicion_causal_a3_7_2.py
Fase A3.7.2: Descomposición causal de la mejora del keeper condicional en 45nm HP @ 85°C.

Compara cuatro arquitecturas:
A) Sin keeper (ENS-A3-CONT-01)
B) Keeper convencional de 45nm (ENS-A3-CONT-02, Step 4)
C) Dos PMOS en serie de 45nm con habilitacion sin retardo intencional (ENS-A3-COND-CTRL-01)
D) Dos PMOS en serie de 45nm con 3 inversores de CLK (ENS-A3-COND-PILOT-01)

Genera:
1. Metricas JSON en act3/resultados/datos/act3_descomposicion_causal.json
2. Figura cientifica a 300 DPI en act3/figuras/fig_a3_7_2_descomposicion_causal.png
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
            t_cross = t_sub[i] + (0 - diff[i]) * (t_sub[i+1] - t_sub[i]) / (diff[i+1] - diff[i])
            return float(t_cross)
    return None

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)
    
    print("==================================================================")
    print("FASE A3.7.2: DESCOMPOSICION CAUSAL DEL KEEPER CONDICIONAL (45nm HP @ 85C)")
    print("==================================================================")

    # 1. Simular Control Auxiliar C (Dos PMOS en serie sin retardo intencional)
    cir_c = "nand3_condicional_hp_control_sin_retardo_85C.cir"
    log_c_path, raw_c_path = simular_netlist(cir_c)
    data_log_c = parse_log(log_c_path)
    raw_data_c = read_raw(raw_c_path)

    # 2. Cargar datos de las otras 3 configuraciones
    # A) Sin keeper
    raw_a_path = os.path.join(RAW_DIR, "nand3_contencion_sin_keeper_85C.raw")
    if not os.path.exists(raw_a_path):
        raw_a_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_sin_keeper_85C.raw")
    raw_data_a = read_raw(raw_a_path)
    log_a_path = os.path.join(LOGS_DIR, "nand3_contencion_sin_keeper_85C.log")
    if not os.path.exists(log_a_path):
        log_a_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_sin_keeper_85C.log")
    data_log_a = parse_log(log_a_path)

    # B) Keeper convencional de 45nm (Step 4 de nand3_contencion_con_keeper_85C)
    raw_b_path = os.path.join(RAW_DIR, "nand3_contencion_con_keeper_85C.raw")
    if not os.path.exists(raw_b_path):
        raw_b_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_con_keeper_85C.raw")
    raw_data_b = read_raw(raw_b_path)
    log_b_path = os.path.join(LOGS_DIR, "nand3_contencion_con_keeper_85C.log")
    if not os.path.exists(log_b_path):
        log_b_path = os.path.join(CIRCUITOS_DIR, "nand3_contencion_con_keeper_85C.log")
    data_log_b = parse_log(log_b_path)

    # D) Keeper condicional con 3 inversores (Piloto A)
    raw_d_path = os.path.join(RAW_DIR, "nand3_condicional_hp_contencion_pilot_85C.raw")
    if not os.path.exists(raw_d_path):
        raw_d_path = os.path.join(CIRCUITOS_DIR, "nand3_condicional_hp_contencion_pilot_85C.raw")
    raw_data_d = read_raw(raw_d_path)
    log_d_path = os.path.join(LOGS_DIR, "nand3_condicional_hp_contencion_pilot_85C.log")
    if not os.path.exists(log_d_path):
        log_d_path = os.path.join(CIRCUITOS_DIR, "nand3_condicional_hp_contencion_pilot_85C.log")
    data_log_d = parse_log(log_d_path)

    # Extraer arrays para cada configuracion
    # Config A: Sin Keeper
    t_a = raw_data_a['data']['time']
    v_dyn_a = raw_data_a['data']['V(dyn)']
    v_out_a = raw_data_a['data']['V(out)']
    v_clk_a = raw_data_a['data']['V(clk)']
    i_pdn_a = raw_data_a['data']['Is(M1)'] if 'Is(M1)' in raw_data_a['data'] else -raw_data_a['data']['Id(M1)']
    i_kp_a = np.zeros_like(t_a)

    t_clk_rise_a = find_crossing(t_a, v_clk_a, 0.5, 'rise', t_min=0.99e-9, t_max=1.05e-9)
    t_dyn_50_a = find_crossing(t_a, v_dyn_a, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_out_50_a = find_crossing(t_a, v_out_a, 0.5, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    tpHL_a = t_dyn_50_a - t_clk_rise_a
    tpLH_a = t_out_50_a - t_clk_rise_a

    # Config B: Keeper convencional de 45nm (step 4, index 3 en steps)
    # Wkp list 10.5n 15n 30n 45n 60n 90n 135n 180n -> index 3 es 45n
    step_b = raw_data_b['steps'][3]
    t_b = step_b['time']
    v_dyn_b = step_b['V(dyn)']
    v_out_b = step_b['V(out)']
    v_clk_b = step_b['V(clk)']
    i_pdn_b = step_b['Is(M1)'] if 'Is(M1)' in step_b else -step_b['Id(M1)']
    i_kp_b = -step_b['Id(Mk)'] if 'Id(Mk)' in step_b else step_b['Is(Mk)']

    t_clk_rise_b = find_crossing(t_b, v_clk_b, 0.5, 'rise', t_min=0.99e-9, t_max=1.05e-9)
    t_dyn_50_b = find_crossing(t_b, v_dyn_b, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_out_50_b = find_crossing(t_b, v_out_b, 0.5, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    t_out_90_b = find_crossing(t_b, v_out_b, 0.9, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    tpHL_b = t_dyn_50_b - t_clk_rise_b
    tpLH_b = t_out_50_b - t_clk_rise_b

    # Config C: Dos PMOS serie sin retardo intencional
    t_c = raw_data_c['data']['time']
    v_dyn_c = raw_data_c['data']['V(dyn)']
    v_out_c = raw_data_c['data']['V(out)']
    v_clk_c = raw_data_c['data']['V(clk)']
    v_en_c = raw_data_c['data']['V(en_sync)']
    v_kmid_c = raw_data_c['data']['V(k_mid)']
    i_pdn_c = raw_data_c['data']['Is(M1)'] if 'Is(M1)' in raw_data_c['data'] else -raw_data_c['data']['Id(M1)']
    i_kp_c = -raw_data_c['data']['Id(Mk_en)'] if 'Id(Mk_en)' in raw_data_c['data'] else raw_data_c['Is(Mk_fb)']

    t_clk_rise_c = find_crossing(t_c, v_clk_c, 0.5, 'rise', t_min=0.99e-9, t_max=1.05e-9)
    t_en_fall_c = find_crossing(t_c, v_en_c, 0.5, 'fall', t_min=0.99e-9, t_max=1.05e-9)
    t_dyn_50_c = find_crossing(t_c, v_dyn_c, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_out_50_c = find_crossing(t_c, v_out_c, 0.5, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    t_out_90_c = find_crossing(t_c, v_out_c, 0.9, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    tpHL_c = t_dyn_50_c - t_clk_rise_c
    tpLH_c = t_out_50_c - t_clk_rise_c
    tau_delay_c = t_en_fall_c - t_clk_rise_c

    # Config D: Dos PMOS serie con 3 inversores de CLK
    t_d = raw_data_d['data']['time']
    v_dyn_d = raw_data_d['data']['V(dyn)']
    v_out_d = raw_data_d['data']['V(out)']
    v_clk_d = raw_data_d['data']['V(clk)']
    v_d3_d = raw_data_d['data']['V(d3)']
    v_kmid_d = raw_data_d['data']['V(k_mid)']
    i_pdn_d = raw_data_d['data']['Is(M1)'] if 'Is(M1)' in raw_data_d['data'] else -raw_data_d['data']['Id(M1)']
    i_kp_d = -raw_data_d['data']['Id(Mk_en)'] if 'Id(Mk_en)' in raw_data_d['data'] else raw_data_d['Is(Mk_fb)']

    t_clk_rise_d = find_crossing(t_d, v_clk_d, 0.5, 'rise', t_min=0.99e-9, t_max=1.05e-9)
    t_d3_fall_d = find_crossing(t_d, v_d3_d, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_dyn_50_d = find_crossing(t_d, v_dyn_d, 0.5, 'fall', t_min=1.00e-9, t_max=1.10e-9)
    t_out_50_d = find_crossing(t_d, v_out_d, 0.5, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    t_out_90_d = find_crossing(t_d, v_out_d, 0.9, 'rise', t_min=1.00e-9, t_max=1.15e-9)
    tpHL_d = t_dyn_50_d - t_clk_rise_d
    tpLH_d = t_out_50_d - t_clk_rise_d
    tau_delay_d = t_d3_fall_d - t_clk_rise_d

    # Analisis de corrientes para cada caso en la ventana de evaluacion [1.0ns .. 1.15ns]
    def analizar_corrientes(t_arr, ikp_arr, ipdn_arr, t_dyn50):
        mask = (t_arr >= 1.00e-9) & (t_arr <= 1.15e-9)
        t_sub = t_arr[mask]
        ikp_sub = ikp_arr[mask]
        ipdn_sub = ipdn_arr[mask]
        
        ikp_max = float(np.max(ikp_sub))
        ipdn_max = float(np.max(ipdn_sub))
        
        # Valor en t_dyn50
        idx_dyn50 = np.argmin(np.abs(t_arr - t_dyn50))
        ikp_at_dyn50 = float(ikp_arr[idx_dyn50])
        ipdn_at_dyn50 = float(ipdn_arr[idx_dyn50])
        
        # Intervalo overlap: Ikp > 1uA e Ipdn > 1uA
        mask_ov = (ikp_sub > 1.0e-6) & (ipdn_sub > 1.0e-6)
        if np.any(mask_ov):
            t_ov_start = float(t_sub[mask_ov][0])
            t_ov_end = float(t_sub[mask_ov][-1])
            dur_ov_ps = (t_ov_end - t_ov_start) * 1e12
        else:
            t_ov_start = None
            t_ov_end = None
            dur_ov_ps = 0.0
            
        return {
            "ikp_max_uA": ikp_max * 1e6,
            "ipdn_max_uA": ipdn_max * 1e6,
            "ikp_at_dyn50_uA": ikp_at_dyn50 * 1e6,
            "ipdn_at_dyn50_uA": ipdn_at_dyn50 * 1e6,
            "t_overlap_start_ps": (t_ov_start - 1.0e-9)*1e12 if t_ov_start else None,
            "t_overlap_end_ps": (t_ov_end - 1.0e-9)*1e12 if t_ov_end else None,
            "duracion_overlap_ps": dur_ov_ps
        }

    corr_a = analizar_corrientes(t_a, i_kp_a, i_pdn_a, t_dyn_50_a)
    corr_b = analizar_corrientes(t_b, i_kp_b, i_pdn_b, t_dyn_50_b)
    corr_c = analizar_corrientes(t_c, i_kp_c, i_pdn_c, t_dyn_50_c)
    corr_d = analizar_corrientes(t_d, i_kp_d, i_pdn_d, t_dyn_50_d)

    # Penalizaciones porcentuales
    pen_a = 0.0
    pen_b = ((tpHL_b - tpHL_a) / tpHL_a) * 100.0
    pen_c = ((tpHL_c - tpHL_a) / tpHL_a) * 100.0
    pen_d = ((tpHL_d - tpHL_a) / tpHL_a) * 100.0

    # Descomposicion Causal:
    # 1. Efecto Estructural / Resistencia Serie (B -> C):
    delta_tpHL_serie_ps = (tpHL_c - tpHL_b) * 1e12
    delta_pen_serie_pct = pen_c - pen_b
    delta_ikp_max_serie_uA = corr_c['ikp_max_uA'] - corr_b['ikp_max_uA']
    
    # 2. Efecto Temporal / Cadena de Retardo (C -> D):
    delta_tpHL_retardo_ps = (tpHL_d - tpHL_c) * 1e12
    delta_pen_retardo_pct = pen_d - pen_c
    delta_ikp_max_retardo_uA = corr_d['ikp_max_uA'] - corr_c['ikp_max_uA']

    # Total B -> D:
    delta_tpHL_total_ps = (tpHL_d - tpHL_b) * 1e12
    delta_pen_total_pct = pen_d - pen_b

    # Estructura del JSON
    metricas = {
        "metadata": {
            "fase": "A3.7.2",
            "tecnologia": "45nm HP",
            "temperatura_C": 85,
            "VDD_V": 1.0,
            "CL_fF": 2.0,
            "Cout_fF": 1.0,
            "objetivo": "Descomposicion causal de la reduccion de penalizacion de contencion"
        },
        "arquitecturas": {
            "A_sin_keeper": {
                "nombre": "Sin keeper (Referencia base)",
                "ensayo_id": "ENS-A3-CONT-01",
                "tpHL_dyn_ps": float(tpHL_a * 1e12),
                "tpLH_out_ps": float(tpLH_a * 1e12),
                "penalizacion_pct": float(pen_a),
                "cumple_criterio_10pct": True,
                "t_hab_Mk_en_ps": None,
                "t_desc_Mk_fb_ps": None,
                "corrientes": corr_a
            },
            "B_keeper_convencional_45nm": {
                "nombre": "Keeper convencional de 45nm",
                "ensayo_id": "ENS-A3-CONT-02-P04",
                "tpHL_dyn_ps": float(tpHL_b * 1e12),
                "tpLH_out_ps": float(tpLH_b * 1e12),
                "penalizacion_pct": float(pen_b),
                "cumple_criterio_10pct": False,
                "t_hab_Mk_en_ps": 0.0, # Siempre habilitado
                "t_desc_Mk_fb_ps": float((t_out_50_b - 1.0e-9)*1e12),
                "corrientes": corr_b
            },
            "C_dos_pmos_serie_sin_retardo": {
                "nombre": "Dos PMOS en serie (45nm) con habilitacion sin retardo (tau=0ps)",
                "ensayo_id": "ENS-A3-COND-CTRL-01",
                "tpHL_dyn_ps": float(tpHL_c * 1e12),
                "tpLH_out_ps": float(tpLH_c * 1e12),
                "penalizacion_pct": float(pen_c),
                "cumple_criterio_10pct": bool(pen_c < 10.0),
                "t_hab_Mk_en_ps": float((t_en_fall_c - 1.0e-9)*1e12),
                "tau_delay_ps": float(tau_delay_c * 1e12),
                "t_desc_Mk_fb_ps": float((t_out_50_c - 1.0e-9)*1e12),
                "corrientes": corr_c
            },
            "D_dos_pmos_serie_con_3inv": {
                "nombre": "Dos PMOS en serie (45nm) con 3 inversores de CLK",
                "ensayo_id": "ENS-A3-COND-PILOT-01",
                "tpHL_dyn_ps": float(tpHL_d * 1e12),
                "tpLH_out_ps": float(tpLH_d * 1e12),
                "penalizacion_pct": float(pen_d),
                "cumple_criterio_10pct": bool(pen_d < 10.0),
                "t_hab_Mk_en_ps": float((t_d3_fall_d - 1.0e-9)*1e12),
                "tau_delay_ps": float(tau_delay_d * 1e12),
                "t_desc_Mk_fb_ps": float((t_out_50_d - 1.0e-9)*1e12),
                "corrientes": corr_d
            }
        },
        "descomposicion_causal": {
            "efecto_resistencia_serie_B_vs_C": {
                "descripcion": "Efecto estructural al pasar de 1 PMOS a 2 PMOS en serie sin retardo intencional",
                "delta_tpHL_dyn_ps": float(delta_tpHL_serie_ps),
                "delta_penalizacion_puntos_pct": float(delta_pen_serie_pct),
                "reduccion_ikp_pico_uA": float(-delta_ikp_max_serie_uA),
                "reduccion_ikp_at_dyn50_uA": float(corr_b['ikp_at_dyn50_uA'] - corr_c['ikp_at_dyn50_uA']),
                "duracion_contencion_ps": {
                    "B_convencional": float(corr_b['duracion_overlap_ps']),
                    "C_serie_sin_retardo": float(corr_c['duracion_overlap_ps'])
                }
            },
            "efecto_retardo_cadena_C_vs_D": {
                "descripcion": "Efecto temporal anadido por la cadena de 3 inversores de retardo (tau_delay = 16.15ps)",
                "delta_tpHL_dyn_ps": float(delta_tpHL_retardo_ps),
                "delta_penalizacion_puntos_pct": float(delta_pen_retardo_pct),
                "desfase_inicio_contencion_ps": float(corr_d['t_overlap_start_ps'] - corr_c['t_overlap_start_ps']),
                "variacion_duracion_contencion_ps": float(corr_d['duracion_overlap_ps'] - corr_c['duracion_overlap_ps']),
                "variacion_ikp_at_dyn50_uA": float(corr_d['ikp_at_dyn50_uA'] - corr_c['ikp_at_dyn50_uA'])
            },
            "balance_global_B_vs_D": {
                "descripcion": "Mejora global del keeper condicional frente al convencional de 45nm",
                "delta_tpHL_dyn_ps": float(delta_tpHL_total_ps),
                "delta_penalizacion_puntos_pct": float(delta_pen_total_pct),
                "contribucion_resistencia_serie_pct": float((delta_pen_serie_pct / delta_pen_total_pct) * 100.0) if delta_pen_total_pct != 0 else 0,
                "contribucion_retardo_cadena_pct": float((delta_pen_retardo_pct / delta_pen_total_pct) * 100.0) if delta_pen_total_pct != 0 else 0
            }
        }
    }

    json_path = os.path.join(DATOS_DIR, "act3_descomposicion_causal.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metricas, f, indent=2)
    print(f"\n[JSON] Metricas guardadas en: {json_path}")

    # =========================================================================
    # GENERAR FIGURA CIENTÍFICA A 300 DPI
    # =========================================================================
    print("\n[PLOTS] Generando figura de descomposicion causal...")
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 10), dpi=300)

    # Mascara temporal [0.99ns .. 1.12ns]
    t_plot_ps = lambda t_arr: (t_arr - 1.0e-9) * 1e12

    # Subplot 1: Tensiones V(dyn) y V(out)
    m_a = (t_a >= 0.99e-9) & (t_a <= 1.12e-9)
    m_b = (t_b >= 0.99e-9) & (t_b <= 1.12e-9)
    m_c = (t_c >= 0.99e-9) & (t_c <= 1.12e-9)
    m_d = (t_d >= 0.99e-9) & (t_d <= 1.12e-9)

    ax1.plot(t_plot_ps(t_a[m_a]), v_dyn_a[m_a], 'k--', lw=1.5, label='A: Sin keeper (Base)')
    ax1.plot(t_plot_ps(t_b[m_b]), v_dyn_b[m_b], 'r-', lw=1.8, label='B: Convencional 45nm (+12.90%)')
    ax1.plot(t_plot_ps(t_c[m_c]), v_dyn_c[m_c], 'orange', lw=1.8, label=f'C: Serie sin retardo (+{pen_c:.2f}%)')
    ax1.plot(t_plot_ps(t_d[m_d]), v_dyn_d[m_d], 'b-', lw=2.0, label='D: Condicional 3-inv (+5.11%)')

    ax1.axhline(0.5, color='gray', linestyle=':', lw=0.8)
    ax1.set_ylabel('Tension V(dyn) [V]', fontsize=10, fontweight='bold')
    ax1.set_title(r'Descomposicion Causal: Descarga Intencional ($A=B=C=1$) en 45nm HP @ 85$^\circ$C', 
                  fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=8.5)
    ax1.set_ylim(-0.05, 1.05)

    # Subplot 2: Corrientes de Keeper Ikp(t)
    ax2.plot(t_plot_ps(t_b[m_b]), i_kp_b[m_b]*1e6, 'r-', lw=1.8, label='B: Keeper Convencional (1 PMOS 45nm)')
    ax2.plot(t_plot_ps(t_c[m_c]), i_kp_c[m_c]*1e6, 'orange', lw=1.8, label='C: 2 PMOS Serie sin retardo')
    ax2.plot(t_plot_ps(t_d[m_d]), i_kp_d[m_d]*1e6, 'b-', lw=2.0, label='D: 2 PMOS Serie + 3 inv (Condicional)')

    ax2.axhline(1.0, color='gray', linestyle=':', lw=0.8, label=r'Umbral contencion (1.0 $\mu$A)')
    ax2.set_ylabel(r'Corriente Keeper $I_{kp}$ [$\mu$A]', fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8.5)

    # Subplot 3: Descomposicion en Barras (Penalizacion vs Corriente Pico)
    arqs = ['A: Sin Kp', 'B: Conv 45nm', 'C: Serie (tau=0)', 'D: Cond (tau=16ps)']
    pens = [pen_a, pen_b, pen_c, pen_d]
    ikp_peaks = [corr_a['ikp_max_uA'], corr_b['ikp_max_uA'], corr_c['ikp_max_uA'], corr_d['ikp_max_uA']]

    x = np.arange(len(arqs))
    width = 0.35

    ax3_twin = ax3.twinx()
    b1 = ax3.bar(x - width/2, pens, width, label='Penalizacion tpHL [%]', color=['gray', 'red', 'orange', 'blue'], alpha=0.75)
    b2 = ax3_twin.bar(x + width/2, ikp_peaks, width, label=r'Corriente Pico $I_{kp,\max}$ [$\mu$A]', color=['darkgray', 'darkred', 'darkorange', 'darkblue'], alpha=0.75)

    ax3.axhline(10.0, color='crimson', linestyle='--', lw=1.0, label='Limite de viabilidad (10.0%)')
    ax3.set_ylabel('Penalizacion de Retardo [%]', fontsize=10, fontweight='bold')
    ax3_twin.set_ylabel(r'Pico de Contencion [$\mu$A]', fontsize=10, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(arqs, fontsize=9.5, fontweight='bold')
    ax3.grid(True, linestyle='--', alpha=0.5, axis='y')

    # Combinar leyendas de ax3 y ax3_twin
    lines_1, labels_1 = ax3.get_legend_handles_labels()
    lines_2, labels_2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', fontsize=8.5)

    ax3.set_xlabel('Configuracion Arquitectonica', fontsize=10, fontweight='bold')

    plt.tight_layout()
    fig_path = os.path.join(FIGURAS_DIR, "fig_a3_7_2_descomposicion_causal.png")
    fig.savefig(fig_path, dpi=300)
    plt.close(fig)
    print(f"  -> Guardada: {fig_path}")

    print("\n==================================================================")
    print(f"RESUMEN CUANTITATIVO DE DESCOMPOSICION CAUSAL:")
    print(f"  A (Sin Keeper):       tpHL = {tpHL_a*1e12:.2f} ps | Pen = {pen_a:.2f}%")
    print(f"  B (Convencional):     tpHL = {tpHL_b*1e12:.2f} ps | Pen = {pen_b:.2f}% | Ikp_max = {corr_b['ikp_max_uA']:.2f} uA")
    print(f"  C (Serie sin retardo): tpHL = {tpHL_c*1e12:.2f} ps | Pen = {pen_c:.2f}% | Ikp_max = {corr_c['ikp_max_uA']:.2f} uA")
    print(f"  D (Condicional 3inv): tpHL = {tpHL_d*1e12:.2f} ps | Pen = {pen_d:.2f}% | Ikp_max = {corr_d['ikp_max_uA']:.2f} uA")
    print("------------------------------------------------------------------")
    print(f"  Efecto Resistencia Serie (B -> C):  dPen = {delta_pen_serie_pct:+.2f} pp ({metricas['descomposicion_causal']['balance_global_B_vs_D']['contribucion_resistencia_serie_pct']:.1f}% de la reduccion total)")
    print(f"  Efecto Retardo Temporal (C -> D):   dPen = {delta_pen_retardo_pct:+.2f} pp ({metricas['descomposicion_causal']['balance_global_B_vs_D']['contribucion_retardo_cadena_pct']:.1f}% de la reduccion total)")
    print(f"  Reduccion Total (B -> D):           dPen = {delta_pen_total_pct:+.2f} pp (de +{pen_b:.2f}% a +{pen_d:.2f}%)")
    print("==================================================================")

if __name__ == '__main__':
    main()
