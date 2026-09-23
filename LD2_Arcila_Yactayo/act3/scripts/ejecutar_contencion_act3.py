# -*- coding: utf-8 -*-
"""
ejecutar_contencion_act3.py
Ejecuta y procesa el análisis de contención en velocidad del keeper (Actividad 3)
en tecnología 45nm HP a 85°C (VDD = 1.0 V, CL = 2 fF, Cout = 1 fF).

Ensayos:
- ENS-A3-CONT-01: Base sin keeper (t_pHL,dyn,sin = 31.80 ps)
- ENS-A3-CONT-02: Barrido de keeper (Wkp in [10.5, 15, 30, 45, 60, 90, 135, 180] nm)
- ENS-A3-CONT-REFIN-85: Refinamiento de 1 nm en la frontera crítica [30 nm .. 45 nm]

Genera:
1. Métricas JSON estructuradas en act3/resultados/datos/act3_contencion_metricas.json
2. Figuras científicas a 300 DPI en act3/figuras/:
   - figura_contencion_penalizacion_vs_r.png
   - figura_contencion_transitorio_formas_onda.png
   - figura_ventana_viabilidad_hp_85C.png
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

def procesar_contencion():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)

    # 1. Simular base sin keeper
    log_sin, raw_sin = simular_netlist("nand3_contencion_sin_keeper_85C.cir")
    data_sin = parse_log(log_sin)
    tphl_sin = float(data_sin["measurements"]["tphl_dyn"])
    tplh_sin = float(data_sin["measurements"]["tplh_out"])
    print(f"[BASE] t_pHL,dyn,sin = {tphl_sin*1e12:.3f} ps | t_pLH,out,sin = {tplh_sin*1e12:.3f} ps")

    # 2. Simular barrido con keeper
    log_con, raw_con = simular_netlist("nand3_contencion_con_keeper_85C.cir")
    data_con = parse_log(log_con)
    w_list_coarse = [10.5e-9, 15e-9, 30e-9, 45e-9, 60e-9, 90e-9, 135e-9, 180e-9]
    tphl_coarse = [entry["val"] for entry in data_con["measurements"]["tphl_dyn"]]
    tplh_coarse = [entry["val"] for entry in data_con["measurements"]["tplh_out"]]
    toff_coarse = [entry["val"] for entry in data_con["measurements"]["toff_kp"]]

    # 3. Simular refinamiento
    log_ref, raw_ref = simular_netlist("nand3_contencion_refinamiento_85C.cir")
    data_ref = parse_log(log_ref)
    w_list_ref = [(30 + i) * 1e-9 for i in range(16)]
    tphl_ref = [entry["val"] for entry in data_ref["measurements"]["tphl_dyn"]]
    tplh_ref = [entry["val"] for entry in data_ref["measurements"]["tplh_out"]]
    toff_ref = [entry["val"] for entry in data_ref["measurements"]["toff_kp"]]

    # Estructura de resultados
    resultados_coarse = []
    for idx, (w, tp, tout, toff) in enumerate(zip(w_list_coarse, tphl_coarse, tplh_coarse, toff_coarse)):
        r = w / 67.5e-9
        weff = w - 10e-9
        if tp is not None:
            pen = 100.0 * (tp - tphl_sin) / tphl_sin
            cumple = bool(pen < 10.0)
        else:
            pen = None
            cumple = False
        
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
            "estado": "PASS" if cumple else ("FAIL_PENALIZACION" if tp else "FAIL_SIN_CONMUTACION_POR_CONTENCION")
        })

    resultados_ref = []
    for idx, (w, tp, tout, toff) in enumerate(zip(w_list_ref, tphl_ref, tplh_ref, toff_ref)):
        r = w / 67.5e-9
        weff = w - 10e-9
        pen = 100.0 * (tp - tphl_sin) / tphl_sin
        cumple = bool(pen < 10.0)
        resultados_ref.append({
            "step": idx + 1,
            "Wkp_nm": round(w * 1e9, 2),
            "Weff_nm": round(weff * 1e9, 2),
            "r": round(r, 4),
            "tphl_dyn_s": tp,
            "tphl_dyn_ps": round(tp * 1e12, 3),
            "tplh_out_s": tout,
            "tplh_out_ps": round(tout * 1e12, 3),
            "toff_kp_s": toff,
            "penalizacion_pct": round(pen, 2),
            "cumple_contencion_menor_10pct": cumple,
            "estado": "PASS" if cumple else "FAIL_PENALIZACION"
        })

    # Cargar métricas de retención de A3.2 para cruce de viabilidad
    retencion_path = os.path.join(DATOS_DIR, "act3_retencion_metricas.json")
    with open(retencion_path, "r", encoding="utf-8") as f:
        datos_ret = json.load(f)
    ret_85C = datos_ret["barrido_con_keeper_85C"]["puntos"]
    ret_ref = datos_ret.get("refinamiento_85C", {}).get("puntos", [])
    todos_ret = ret_85C + ret_ref

    # Cruzar retención vs contención
    cruce_viabilidad = []
    for p_c in resultados_coarse:
        w_nm = p_c["Wkp_nm"]
        # Buscar en retención
        p_ret = next((p for p in todos_ret if abs(p["Wkp_nm"] - w_nm) < 0.1), None)
        vdyn_end = None
        if p_ret:
            vdyn_end = p_ret.get("Vdyn_end_1us_V") or p_ret.get("Vdyn_end_V")
        ret_ok = bool(vdyn_end is not None and vdyn_end > 0.90)
        cont_ok = p_c["cumple_contencion_menor_10pct"]
        viable = bool(ret_ok and cont_ok)
        cruce_viabilidad.append({
            "Wkp_nm": w_nm,
            "r": p_c["r"],
            "Vdyn_end_V": vdyn_end,
            "retencion_ok": ret_ok,
            "penalizacion_pct": p_c["penalizacion_pct"],
            "contencion_ok": cont_ok,
            "viable_conjunto": viable
        })

    # Consolidar JSON de contención
    salida_json = {
        "descripcion": "Evaluación de Contención en Velocidad y Ventana de Viabilidad en 45nm HP @ 85°C",
        "condiciones": {
            "proceso": "45nm_HP",
            "VDD_V": 1.0,
            "temperatura_C": 85.0,
            "CL_fF": 2.0,
            "Cout_fF": 1.0,
            "Tclk_ns": 2.0,
            "entradas": "A=B=C=1.0 V (evaluación activa)",
            "W_PDN_eq_nm": 67.5,
            "definicion_r": "r = Wkp / 67.5nm"
        },
        "referencia_sin_keeper": {
            "ensayo_id": "ENS-A3-CONT-01",
            "tphl_dyn_s": tphl_sin,
            "tphl_dyn_ps": round(tphl_sin * 1e12, 3),
            "tplh_out_s": tplh_sin,
            "tplh_out_ps": round(tplh_sin * 1e12, 3)
        },
        "barrido_grueso": resultados_coarse,
        "refinamiento_frontera_1nm": resultados_ref,
        "cruce_viabilidad_conjunta": cruce_viabilidad
    }

    out_json_path = os.path.join(DATOS_DIR, "act3_contencion_metricas.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(salida_json, f, indent=2)
    print(f"\n[DATOS] Metricas guardadas en: {out_json_path}")

    # =========================================================================
    # GENERACIÓN DE FIGURAS
    # =========================================================================
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    colors = {
        'primary': '#003366',
        'accent': '#D9534F',
        'success': '#2E7D32',
        'neutral': '#4A5568',
        'grid': '#E2E8F0',
        'highlight': '#F59E0B'
    }

    # FIGURA 1: Penalización % vs r y Wkp
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Subplot A: Penalizacion vs Wkp (Refinado + Coarse)
    w_valid = [p["Wkp_nm"] for p in resultados_coarse if p["penalizacion_pct"] is not None]
    pen_valid = [p["penalizacion_pct"] for p in resultados_coarse if p["penalizacion_pct"] is not None]
    
    w_ref_pts = [p["Wkp_nm"] for p in resultados_ref]
    pen_ref_pts = [p["penalizacion_pct"] for p in resultados_ref]

    # Derivar frontera máxima directamente de los datos que cumplen < 10.0%
    w_max_viable = max(p["Wkp_nm"] for p in resultados_ref if p["cumple_contencion_menor_10pct"])
    r_max_viable = max(p["r"] for p in resultados_ref if p["cumple_contencion_menor_10pct"])

    ax1.plot(w_valid, pen_valid, 'o--', color=colors['primary'], label='Malla Gruesa (10.5 - 135 nm)', lw=1.5, alpha=0.7)
    ax1.plot(w_ref_pts, pen_ref_pts, 's-', color=colors['accent'], label='Refinamiento 1 nm [30 - 45 nm]', lw=2.0)
    ax1.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax1.axvspan(10.5, w_max_viable, color='green', alpha=0.12, label=f'Zona Viable Medida ($W_{{kp}} \\leq {w_max_viable:.0f}\\,\\mathrm{{nm}}$)')
    ax1.axvspan(w_max_viable, 140.0, color='red', alpha=0.08, label='Zona Inadmisible (≥ 10.0%)')
    ax1.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Penalización de Retardo vs Ancho Geométrico', fontsize=12, fontweight='bold', color=colors['primary'])
    ax1.set_xlim(5, 140)
    ax1.set_ylim(0, 140)
    ax1.legend(fontsize=9, loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Subplot B: Penalizacion vs r
    r_valid = [p["r"] for p in resultados_coarse if p["penalizacion_pct"] is not None]
    r_ref_pts = [p["r"] for p in resultados_ref]

    ax2.plot(r_valid, pen_valid, 'o--', color=colors['primary'], label='Malla Gruesa', lw=1.5, alpha=0.7)
    ax2.plot(r_ref_pts, pen_ref_pts, 's-', color=colors['accent'], label='Refinamiento', lw=2.0)
    ax2.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax2.axvspan(10.5/67.5, r_max_viable, color='green', alpha=0.12, label=f'Zona Viable Medida ($r \\leq {r_max_viable:.3f}$)')
    ax2.axvspan(r_max_viable, 2.05, color='red', alpha=0.08, label='Zona Inadmisible')
    ax2.set_xlabel(r'Razón de Aspecto $r = \frac{(W/L)_{kp}}{(W/L)_{PDN,eq}} \approx \frac{W_{kp}}{67.5\,\mathrm{nm}}$', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Penalización de Retardo vs Razón de Aspecto $r$', fontsize=12, fontweight='bold', color=colors['primary'])
    ax2.set_xlim(0.1, 2.05)
    ax2.set_ylim(0, 140)
    ax2.legend(fontsize=9, loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    fig1_path = os.path.join(FIGURAS_DIR, "figura_contencion_penalizacion_vs_r.png")
    plt.savefig(fig1_path)
    plt.close()
    print(f"[FIGURA] Figura 1 guardada en: {fig1_path}")

    # FIGURA 2: Formas de Onda Transitorias (RAW)
    raw_con_path = os.path.join(RAW_DIR, "nand3_contencion_con_keeper_85C.raw")
    raw_con_data = read_raw(raw_con_path)
    steps_dict = raw_con_data["steps"]

    plt.figure(figsize=(10, 6), dpi=300)
    # Graficar sin keeper
    raw_sin_data = read_raw(os.path.join(RAW_DIR, "nand3_contencion_sin_keeper_85C.raw"))
    t_sin = (raw_sin_data["steps"][0]["time"] - 1.0e-9) * 1e12  # en ps relativo a 1.0 ns (flanco de clk)
    v_dyn_sin = raw_sin_data["steps"][0]["V(dyn)"]
    v_out_sin = raw_sin_data["steps"][0]["V(out)"]
    v_clk_sin = raw_sin_data["steps"][0]["V(clk)"]

    plt.plot(t_sin, v_clk_sin, 'k:', lw=1.5, label='V(clk) (500 MHz)', alpha=0.6)
    plt.plot(t_sin, v_dyn_sin, color='black', lw=2.0, label='V(dyn) Sin Keeper')
    plt.plot(t_sin, v_out_sin, color='gray', lw=1.5, ls='--', label='V(out) Sin Keeper')

    # Graficar steps representativos: 15nm (viable), 38nm (critico), 60nm (excesivo), 180nm (sin conmutacion)
    map_w = {0: '10.5 nm', 1: '15 nm', 2: '30 nm', 3: '45 nm', 4: '60 nm', 5: '90 nm', 6: '135 nm', 7: '180 nm (Sin Conmutación)'}
    col_steps = {1: '#2E7D32', 3: '#F59E0B', 4: '#E65100', 7: '#C62828'}
    for s_idx in [1, 3, 4, 7]:
        if s_idx < len(steps_dict):
            t_s = (steps_dict[s_idx]["time"] - 1.0e-9) * 1e12
            v_dyn_s = steps_dict[s_idx]["V(dyn)"]
            plt.plot(t_s, v_dyn_s, lw=1.8, color=col_steps[s_idx], label=f'V(dyn) Wkp={map_w[s_idx]}')

    plt.axhline(0.5, color='blue', ls='-.', lw=1.0, label='Umbral 50% VDD (0.5 V)')
    plt.xlabel('Tiempo relativo al flanco de evaluación (ps)', fontsize=11, fontweight='bold')
    plt.ylabel('Tensión (V)', fontsize=11, fontweight='bold')
    plt.title('Transitorio de Evaluación de la NAND3 Dinámica con Contención del Keeper (45nm HP @ 85°C)', fontsize=12, fontweight='bold', color=colors['primary'])
    plt.xlim(0, 150)
    plt.ylim(-0.05, 1.05)
    plt.legend(fontsize=9, loc='center right')
    plt.grid(True, linestyle='--', alpha=0.6)

    fig2_path = os.path.join(FIGURAS_DIR, "figura_contencion_transitorio_formas_onda.png")
    plt.savefig(fig2_path)
    plt.close()
    print(f"[FIGURA] Figura 2 guardada en: {fig2_path}")

    # FIGURA 3: Ventana de Viabilidad Conjunta (Retención vs Contención)
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    w_vals = [p["Wkp_nm"] for p in cruce_viabilidad]
    ret_vals = [p["Vdyn_end_V"] for p in cruce_viabilidad]
    pen_vals = [p["penalizacion_pct"] if p["penalizacion_pct"] is not None else 150.0 for p in cruce_viabilidad]

    ax.plot(w_vals, ret_vals, 'o-', color=colors['success'], lw=2.0, label=r'Retención: $V_{dyn}(1\,\mu\mathrm{s})$ (Eje Izq.)')
    ax.axhline(0.90, color=colors['success'], ls='--', lw=1.5, label='Umbral Mín. Retención (0.90 V)')
    ax.set_ylabel(r'Tensión de Retención $V_{dyn}(1\,\mu\mathrm{s})$ (V)', fontsize=11, fontweight='bold', color=colors['success'])
    ax.tick_params(axis='y', labelcolor=colors['success'])
    ax.set_ylim(0.80, 1.05)
    ax.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')

    ax_twin = ax.twinx()
    ax_twin.plot(w_vals, pen_vals, 's-', color=colors['accent'], lw=2.0, label='Contención: Penalización $\\Delta t_{pHL}$ (Eje Der.)')
    ax_twin.axhline(10.0, color=colors['accent'], ls=':', lw=1.5, label='Límite Máx. Contención (+10.0%)')
    ax_twin.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold', color=colors['accent'])
    ax_twin.tick_params(axis='y', labelcolor=colors['accent'])
    ax_twin.set_ylim(0, 140)

    # Marcar la ventana de viabilidad directamente derivada
    ax.axvspan(10.5, w_max_viable, color='#A7F3D0', alpha=0.35, label=f'Ventana Viable: $W_{{kp}} \\in [10.5, {w_max_viable:.0f}]\\,\\mathrm{{nm}}$')
    ax.set_title('Ventana de Viabilidad Conjunta: Retención vs Contención (45nm HP @ 85°C)', fontsize=12, fontweight='bold', color=colors['primary'])
    ax.set_xlim(5, 140)

    # Combinar leyendas
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='center left', fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.5)

    fig3_path = os.path.join(FIGURAS_DIR, "figura_ventana_viabilidad_hp_85C.png")
    plt.savefig(fig3_path)
    plt.close()
    print(f"[FIGURA] Figura 3 guardada en: {fig3_path}")

    print("\n[PROCESO] A3.5 COMPLETADO EXITOSAMENTE.")

if __name__ == "__main__":
    procesar_contencion()
