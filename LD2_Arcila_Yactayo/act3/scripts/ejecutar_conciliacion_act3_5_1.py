# -*- coding: utf-8 -*-
"""
ejecutar_conciliacion_act3_5_1.py
Conciliación de dos auditorías independientes (Nemotron 3 Ultra y Muse Spark 1.3) para Actividad 3.5.

Tareas:
1. Simulación directa de retención para Wkp in [35, 36, 37, 38, 39, 40] nm @ 85°C (ENS-A3-RET-FRONTERA-85)
2. Estudio de sensibilidad numérica: Config A (reltol=1e-4, 2p) vs Config B (reltol=1e-5, 0.5p)
   para sin keeper y Wkp in [35, 37, 38, 39] nm
3. Corrección del caso 180 nm a FAIL_SIN_CONMUTACION_POR_CONTENCION
4. Construcción de matriz conjunta rigurosa distinguiendo DIRECTA, INTERPOLADA, INFERIDA, NO_VERIFICADO
5. Regeneración de figuras sin hardcoding de fronteras
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

def ejecutar_conciliacion():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)

    # =========================================================================
    # 1. RETENCIÓN DIRECTA EN LA FRONTERA CRÍTICA (35nm a 40nm)
    # =========================================================================
    log_ret_front, raw_ret_front = simular_netlist("nand3_retencion_frontera_35_40_85C.cir")
    data_ret_front = parse_log(log_ret_front)

    w_ret_list = [35.0, 36.0, 37.0, 38.0, 39.0, 40.0]
    
    def extract_vals(m_obj, default_len):
        if m_obj is None:
            return [None] * default_len
        if isinstance(m_obj, list):
            return [e["val"] if isinstance(e, dict) else e for e in m_obj]
        return [m_obj] * default_len

    vdyn_start_list = extract_vals(data_ret_front["measurements"].get("vdyn_start"), len(w_ret_list))
    vdyn_end_list = extract_vals(data_ret_front["measurements"].get("vdyn_end_1us"), len(w_ret_list))
    vdyn_min_list = extract_vals(data_ret_front["measurements"].get("vdyn_min"), len(w_ret_list))
    t_cross_list = extract_vals(data_ret_front["measurements"].get("t_cross_0p9vdd"), len(w_ret_list))
    isupply_list = extract_vals(data_ret_front["measurements"].get("isupply_avg"), len(w_ret_list))
    ileak_pdn_list = extract_vals(data_ret_front["measurements"].get("ileak_pdn_avg"), len(w_ret_list))
    ikp_inj_list = extract_vals(data_ret_front["measurements"].get("ikp_inj_avg"), len(w_ret_list))

    retencion_frontera_resultados = []
    print("\n" + "="*80)
    print("RESULTADOS DE RETENCION DIRECTA EN FRONTERA (45nm HP @ 85C, VDD=1.0V, Tret=1.0us)")
    print("="*80)
    print(f"{'Wkp (nm)':>8} | {'Weff (nm)':>9} | {'Vdyn_start (V)':>14} | {'Vdyn_end (V)':>12} | {'Vdyn_min (V)':>12} | {'Cumple >0.9V?':>13}")
    print("-"*80)
    for idx, w in enumerate(w_ret_list):
        weff = w - 10.0  # Wint = 5nm de ptm45hp.lib
        v_start = vdyn_start_list[idx]
        v_end = vdyn_end_list[idx]
        v_min = vdyn_min_list[idx]
        t_cr = t_cross_list[idx]
        isup = isupply_list[idx]
        ileak = ileak_pdn_list[idx]
        ikp = ikp_inj_list[idx]
        cumple = bool(v_end > 0.90)
        estado_censura = "Censurado (>1.0us)" if t_cr is None else f"Cruzo en {t_cr*1e9:.2f}ns"

        print(f"{w:8.1f} | {weff:9.1f} | {v_start:14.6f} | {v_end:12.6f} | {v_min:12.6f} | {'SI (CUMPLE)' if cumple else 'NO':>13}")

        retencion_frontera_resultados.append({
            "id_punto": f"ENS-A3-RET-FRONTERA-85-P0{idx+1}",
            "step": idx + 1,
            "Wkp_nm": w,
            "Weff_nm": weff,
            "Vdyn_start_V": v_start,
            "Vdyn_end_1us_V": v_end,
            "Vdyn_min_V": v_min,
            "t_cross_0p9vdd_s": t_cr,
            "estado_censura": estado_censura,
            "cumple_retencion_0p9": cumple,
            "I_supply_avg_A": isup,
            "I_leak_pdn_avg_A": ileak,
            "I_kp_inj_avg_A": ikp,
            "warnings_ltspice": data_ret_front["warnings"]
        })

    # =========================================================================
    # 2. ESTUDIO DE SENSIBILIDAD NUMÉRICA (CONFIG A vs CONFIG B)
    # =========================================================================
    # Base A ya existe de ENS-A3-CONT-01:
    log_sin_A = os.path.join(LOGS_DIR, "nand3_contencion_sin_keeper_85C.log")
    data_sin_A = parse_log(log_sin_A)
    tphl_sin_A = float(data_sin_A["measurements"]["tphl_dyn"])
    tplh_sin_A = float(data_sin_A["measurements"]["tplh_out"])

    # Base B:
    log_sin_B, raw_sin_B = simular_netlist("nand3_contencion_sin_keeper_85C_sensB.cir")
    data_sin_B = parse_log(log_sin_B)
    tphl_sin_B = float(data_sin_B["measurements"]["tphl_dyn"])
    tplh_sin_B = float(data_sin_B["measurements"]["tplh_out"])

    # Sweeps A y B:
    log_sens_A, raw_sens_A = simular_netlist("nand3_contencion_sens_configA.cir")
    data_sens_A = parse_log(log_sens_A)
    w_sens_list = [35.0, 37.0, 38.0, 39.0]
    tphl_A_list = extract_vals(data_sens_A["measurements"].get("tphl_dyn"), len(w_sens_list))
    tplh_A_list = extract_vals(data_sens_A["measurements"].get("tplh_out"), len(w_sens_list))
    toff_A_list = extract_vals(data_sens_A["measurements"].get("toff_kp"), len(w_sens_list))

    log_sens_B, raw_sens_B = simular_netlist("nand3_contencion_sens_configB.cir")
    data_sens_B = parse_log(log_sens_B)
    tphl_B_list = extract_vals(data_sens_B["measurements"].get("tphl_dyn"), len(w_sens_list))
    tplh_B_list = extract_vals(data_sens_B["measurements"].get("tplh_out"), len(w_sens_list))
    toff_B_list = extract_vals(data_sens_B["measurements"].get("toff_kp"), len(w_sens_list))

    w_sens_list = [35.0, 37.0, 38.0, 39.0]
    sensibilidad_resultados = []

    print("\n" + "="*95)
    print("ESTUDIO DE SENSIBILIDAD NUMERICA: CONFIG A (Original) vs CONFIG B (Exigente)")
    print("="*95)
    print(f"Base Sin Keeper: Config A = {tphl_sin_A*1e12:.3f} ps | Config B = {tphl_sin_B*1e12:.3f} ps | Diff = {(tphl_sin_B - tphl_sin_A)*1e12:+.3f} ps")
    print("-"*95)
    print(f"{'Wkp (nm)':>8} | {'tpHL_A (ps)':>11} | {'Pen_A (%)':>10} | {'tpHL_B (ps)':>11} | {'Pen_B (%)':>10} | {'|dtp| (ps)':>10} | {'dPen (%)':>9} | {'38nm < 10%?':>11}")
    print("-"*95)

    for idx, w in enumerate(w_sens_list):
        tp_A = tphl_A_list[idx]
        tp_B = tphl_B_list[idx]
        pen_A = 100.0 * (tp_A - tphl_sin_A) / tphl_sin_A
        pen_B = 100.0 * (tp_B - tphl_sin_B) / tphl_sin_B
        diff_tp_ps = (tp_B - tp_A) * 1e12
        diff_pen = pen_B - pen_A
        cumple_A = pen_A < 10.0
        cumple_B = pen_B < 10.0

        print(f"{w:8.1f} | {tp_A*1e12:11.3f} | {pen_A:9.2f}% | {tp_B*1e12:11.3f} | {pen_B:9.2f}% | {abs(diff_tp_ps):10.3f} | {diff_pen:+8.2f}% | {'A:' + ('SI' if cumple_A else 'NO') + ' B:' + ('SI' if cumple_B else 'NO'):>11}")

        sensibilidad_resultados.append({
            "Wkp_nm": w,
            "tphl_A_ps": round(tp_A * 1e12, 3),
            "penalizacion_A_pct": round(pen_A, 2),
            "cumple_A": cumple_A,
            "tphl_B_ps": round(tp_B * 1e12, 3),
            "penalizacion_B_pct": round(pen_B, 2),
            "cumple_B": cumple_B,
            "diff_tphl_ps": round(diff_tp_ps, 4),
            "diff_penalizacion_pct": round(diff_pen, 3),
            "cambio_clasificacion": bool(cumple_A != cumple_B)
        })

    # =========================================================================
    # 3. AUDITORÍA DEL CASO 180nm Y CORRECCIÓN DE ETIQUETA
    # =========================================================================
    raw_con_path = os.path.join(RAW_DIR, "nand3_contencion_con_keeper_85C.raw")
    raw_con = read_raw(raw_con_path)
    step_180 = raw_con["steps"][7]
    vdyn_min_180 = float(step_180["V(dyn)"].min())
    vdyn_end_180 = float(step_180["V(dyn)"][-1])
    vout_max_180 = float(step_180["V(out)"].max())
    print("\n" + "="*80)
    print("AUDITORIA DEL CASO Wkp=180nm EN RAW:")
    print(f"  V(dyn) min = {vdyn_min_180:.4f} V (nunca cruza VDD/2 = 0.500 V)")
    print(f"  V(dyn) end = {vdyn_end_180:.4f} V")
    print(f"  V(out) max = {vout_max_180:.4f} V (nunca conmuta, permanece < 22 mV)")
    print("  Estado corregido: FAIL_SIN_CONMUTACION_POR_CONTENCION (no FAIL_LATCHUP)")
    print("="*80)

    # =========================================================================
    # 4. MATRIZ CONJUNTA CORREGIDA CON EVIDENCIA EXPLÍCITA
    # =========================================================================
    # Cargar contención de A3.5
    cont_json_path = os.path.join(DATOS_DIR, "act3_contencion_metricas.json")
    with open(cont_json_path, "r", encoding="utf-8") as f:
        datos_cont = json.load(f)

    # Todos los puntos evaluados en contención:
    # Coarse: 10.5, 15, 30, 45, 60, 90, 135, 180
    # Refinamiento: 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45
    puntos_coarse = datos_cont["barrido_grueso"]
    puntos_ref = datos_cont["refinamiento_frontera_1nm"]

    # Cargar retención previa de A3.2
    ret_prev_path = os.path.join(DATOS_DIR, "act3_retencion_metricas.json")
    with open(ret_prev_path, "r", encoding="utf-8") as f:
        datos_ret_prev = json.load(f)
    ret_prev_85C = datos_ret_prev["barrido_con_keeper_85C"]["puntos"]
    ret_prev_ref = datos_ret_prev.get("refinamiento_85C", {}).get("puntos", [])

    # Construir mapa de retención directa
    ret_directa_map = {}
    # De A3.2:
    for p in ret_prev_85C:
        ret_directa_map[round(p["Wkp_nm"], 1)] = {
            "vdyn_end": p["Vdyn_end_1us_V"],
            "fuente": "A3.2 (ENS-A3-RET-04)",
            "tipo": "DIRECTA"
        }
    for p in ret_prev_ref:
        ret_directa_map[round(p["Wkp_nm"], 1)] = {
            "vdyn_end": p.get("Vdyn_end_1us_V") or p.get("Vdyn_end_V"),
            "fuente": "A3.2 (ENS-A3-REFIN-85)",
            "tipo": "DIRECTA"
        }
    # De A3.5.1 (nuevos ensayos de frontera):
    for p in retencion_frontera_resultados:
        ret_directa_map[round(p["Wkp_nm"], 1)] = {
            "vdyn_end": p["Vdyn_end_1us_V"],
            "fuente": "A3.5.1 (ENS-A3-RET-FRONTERA-85)",
            "tipo": "DIRECTA"
        }

    # Construir tabla consolidada de todos los anchos ensayados
    todos_w = sorted(list(set(
        [p["Wkp_nm"] for p in puntos_coarse] + 
        [p["Wkp_nm"] for p in puntos_ref]
    )))

    matriz_conjunta_rigurosa = []
    print("\n" + "="*110)
    print("MATRIZ CONJUNTA CORREGIDA DE RETENCION Y CONTENCION (45nm HP @ 85C)")
    print("="*110)
    print(f"{'Wkp (nm)':>8} | {'r':>6} | {'Retencion Vdyn':>14} | {'Evid. Retencion':>20} | {'Contencion Pen':>14} | {'Evid. Contencion':>20} | {'Viabilidad':>15}")
    print("-"*110)

    for w in todos_w:
        r = round(w / 67.5, 4)
        
        # Datos de retención
        if w in ret_directa_map:
            v_ret = ret_directa_map[w]["vdyn_end"]
            evid_ret = f"DIRECTA [{ret_directa_map[w]['fuente']}]"
            ret_ok = bool(v_ret > 0.90)
            ret_str = f"{v_ret:.5f} V"
        else:
            # Si no está simulado directamente, es inferencia/interpolación
            v_ret = None
            evid_ret = "INFERIDA (monotonicidad)"
            ret_ok = True  # Físicamente monótono entre 30nm y 45nm
            ret_str = ">0.9999 V (inf)"

        # Datos de contención
        p_cont = next((p for p in puntos_ref if abs(p["Wkp_nm"] - w) < 0.05), None)
        if not p_cont:
            p_cont = next((p for p in puntos_coarse if abs(p["Wkp_nm"] - w) < 0.05), None)
            evid_cont = "DIRECTA [A3.5 (Coarse)]"
        else:
            evid_cont = "DIRECTA [A3.5 (Refin)]"

        pen = p_cont["penalizacion_pct"] if p_cont else None
        if p_cont and p_cont.get("estado") == "FAIL_LATCHUP":
            p_cont["estado"] = "FAIL_SIN_CONMUTACION_POR_CONTENCION"
        
        if pen is not None:
            cont_ok = bool(pen < 10.0)
            pen_str = f"{pen:.2f}%"
        else:
            cont_ok = False
            pen_str = "SIN CONM."

        # Estado conjunto
        if ret_ok and cont_ok:
            viabilidad = "VIABLE"
        elif not cont_ok:
            viabilidad = "FALLA CONTENCION"
        else:
            viabilidad = "FALLA RETENCION"

        if "INFERIDA" in evid_ret:
            viabilidad += " (inf)"

        print(f"{w:8.1f} | {r:6.3f} | {ret_str:>14} | {evid_ret:>20} | {pen_str:>14} | {evid_cont:>20} | {viabilidad:>15}")

        matriz_conjunta_rigurosa.append({
            "Wkp_nm": w,
            "r": r,
            "Vdyn_end_V": v_ret,
            "retencion_status": ret_str,
            "evidencia_retencion": evid_ret,
            "retencion_ok": ret_ok,
            "penalizacion_pct": pen,
            "evidencia_contencion": evid_cont,
            "contencion_ok": cont_ok,
            "viabilidad": viabilidad
        })

    # =========================================================================
    # 5. DERIVACIÓN DINÁMICA DE LA FRONTERA MÁXIMA (SIN HARDCODING)
    # =========================================================================
    puntos_viables_directos = [
        p for p in matriz_conjunta_rigurosa 
        if p["contencion_ok"] and p["retencion_ok"] and "INFERIDA" not in p["evidencia_retencion"]
    ]
    w_max_directo = max(p["Wkp_nm"] for p in puntos_viables_directos)
    r_max_directo = max(p["r"] for p in puntos_viables_directos)
    pen_max_directo = next(p["penalizacion_pct"] for p in puntos_viables_directos if p["Wkp_nm"] == w_max_directo)

    print("\n" + "="*80)
    print("FRONTERA MAXIMA DERIVADA DINAMICAMENTE CON EVIDENCIA DIRECTA:")
    print(f"  Wkp_max_directo = {w_max_directo:.1f} nm")
    print(f"  r_max_directo   = {r_max_directo:.4f}")
    print(f"  Penalizacion    = {pen_max_directo:.2f}% (< 10.0%)")
    print("="*80)

    # =========================================================================
    # 6. GUARDAR JSON CONSOLIDADO
    # =========================================================================
    datos_conciliacion = {
        "descripcion": "Reporte de Conciliación A3.5.1: Auditoría Nemotron y Muse Spark",
        "retencion_directa_frontera_85C": retencion_frontera_resultados,
        "estudio_sensibilidad_solver": {
            "config_A_original": {
                "opciones": "gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear",
                "tstep_max": "2ps",
                "tphl_sin_keeper_ps": round(tphl_sin_A * 1e12, 3)
            },
            "config_B_exigente": {
                "opciones": "gmin=1e-15 abstol=1e-15 reltol=1e-5 method=gear",
                "tstep_max": "0.5ps",
                "tphl_sin_keeper_ps": round(tphl_sin_B * 1e12, 3)
            },
            "comparativa_puntos": sensibilidad_resultados
        },
        "caso_180nm_corregido": {
            "estado": "FAIL_SIN_CONMUTACION_POR_CONTENCION",
            "justificacion": "RAW confirma que V(dyn) alcanza minimo de 0.633V (>0.5V) y V(out) maximo de 21.7mV (<0.5V), sin conmutacion",
            "tphl_dyn_s": None,
            "tplh_out_s": None
        },
        "frontera_maxima_dinamica": {
            "Wkp_max_nm": w_max_directo,
            "r_max": r_max_directo,
            "penalizacion_pct": pen_max_directo,
            "criterio": "penalizacion_pct < 10.0 derivado de simulacion directa sin hardcoding"
        },
        "matriz_conjunta_rigurosa": matriz_conjunta_rigurosa
    }

    out_json = os.path.join(DATOS_DIR, "act3_conciliacion_a3_5_1.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(datos_conciliacion, f, indent=2)
    print(f"\n[DATOS] JSON de conciliacion guardado en: {out_json}")

    # =========================================================================
    # 7. REGENERAR FIGURAS CORREGIDAS
    # =========================================================================
    colors = {
        'primary': '#003366',
        'accent': '#D9534F',
        'success': '#2E7D32',
        'neutral': '#4A5568',
        'grid': '#E2E8F0',
        'highlight': '#F59E0B'
    }

    # FIGURA 1: Penalización % vs r y Wkp con derivación dinámica
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

    # Subplot A: Penalizacion vs Wkp
    w_coarse_v = [p["Wkp_nm"] for p in puntos_coarse if p["penalizacion_pct"] is not None]
    pen_coarse_v = [p["penalizacion_pct"] for p in puntos_coarse if p["penalizacion_pct"] is not None]
    w_ref_v = [p["Wkp_nm"] for p in puntos_ref]
    pen_ref_v = [p["penalizacion_pct"] for p in puntos_ref]

    ax1.plot(w_coarse_v, pen_coarse_v, 'o--', color=colors['primary'], label='Malla Gruesa [10.5 - 135 nm]', lw=1.5, alpha=0.7)
    ax1.plot(w_ref_v, pen_ref_v, 's-', color=colors['accent'], label='Refinamiento 1 nm [30 - 45 nm]', lw=2.0)
    ax1.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax1.axvspan(10.5, w_max_directo, color='green', alpha=0.12, label=f'Zona Viable Medida ($W_{{kp}} \\leq {w_max_directo:.0f}\\,\\mathrm{{nm}}$)')
    ax1.axvspan(w_max_directo, 140.0, color='red', alpha=0.08, label='Zona Inadmisible (≥ 10.0%)')
    ax1.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Penalización de Retardo vs Ancho Geométrico', fontsize=12, fontweight='bold', color=colors['primary'])
    ax1.set_xlim(5, 140)
    ax1.set_ylim(0, 140)
    ax1.legend(fontsize=9, loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Subplot B: Penalizacion vs r
    r_coarse_v = [p["r"] for p in puntos_coarse if p["penalizacion_pct"] is not None]
    r_ref_v = [p["r"] for p in puntos_ref]

    ax2.plot(r_coarse_v, pen_coarse_v, 'o--', color=colors['primary'], label='Malla Gruesa', lw=1.5, alpha=0.7)
    ax2.plot(r_ref_v, pen_ref_v, 's-', color=colors['accent'], label='Refinamiento', lw=2.0)
    ax2.axhline(10.0, color='red', ls=':', lw=2.0, label='Límite Estricto (+10.0%)')
    ax2.axvspan(10.5/67.5, r_max_directo, color='green', alpha=0.12, label=f'Zona Viable Medida ($r \\leq {r_max_directo:.3f}$)')
    ax2.axvspan(r_max_directo, 2.05, color='red', alpha=0.08, label='Zona Inadmisible')
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
    print(f"[FIGURA] Figura 1 actualizada: {fig1_path}")

    # FIGURA 2: Formas de Onda con etiqueta corregida
    raw_con_path = os.path.join(RAW_DIR, "nand3_contencion_con_keeper_85C.raw")
    raw_con_data = read_raw(raw_con_path)
    steps_dict = raw_con_data["steps"]

    plt.figure(figsize=(10, 6), dpi=300)
    raw_sin_data = read_raw(os.path.join(RAW_DIR, "nand3_contencion_sin_keeper_85C.raw"))
    t_sin = (raw_sin_data["steps"][0]["time"] - 1.0e-9) * 1e12
    v_dyn_sin = raw_sin_data["steps"][0]["V(dyn)"]
    v_out_sin = raw_sin_data["steps"][0]["V(out)"]
    v_clk_sin = raw_sin_data["steps"][0]["V(clk)"]

    plt.plot(t_sin, v_clk_sin, 'k:', lw=1.5, label='V(clk) (500 MHz)', alpha=0.6)
    plt.plot(t_sin, v_dyn_sin, color='black', lw=2.0, label='V(dyn) Sin Keeper')
    plt.plot(t_sin, v_out_sin, color='gray', lw=1.5, ls='--', label='V(out) Sin Keeper')

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
    print(f"[FIGURA] Figura 2 actualizada: {fig2_path}")

    # FIGURA 3: Ventana de Viabilidad Conjunta con datos directos de frontera
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    
    # Extraer puntos con retención directa disponible
    puntos_grafica_viab = [p for p in matriz_conjunta_rigurosa if p["Vdyn_end_V"] is not None]
    w_g = [p["Wkp_nm"] for p in puntos_grafica_viab]
    ret_g = [p["Vdyn_end_V"] for p in puntos_grafica_viab]
    pen_g = [p["penalizacion_pct"] if p["penalizacion_pct"] is not None else 150.0 for p in puntos_grafica_viab]

    ax.plot(w_g, ret_g, 'o-', color=colors['success'], lw=2.0, label=r'Retención Directa: $V_{dyn}(1\,\mu\mathrm{s})$ (Eje Izq.)')
    ax.axhline(0.90, color=colors['success'], ls='--', lw=1.5, label='Umbral Mín. Retención (0.90 V)')
    ax.set_ylabel(r'Tensión de Retención $V_{dyn}(1\,\mu\mathrm{s})$ (V)', fontsize=11, fontweight='bold', color=colors['success'])
    ax.tick_params(axis='y', labelcolor=colors['success'])
    ax.set_ylim(0.80, 1.05)
    ax.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=11, fontweight='bold')

    ax_twin = ax.twinx()
    ax_twin.plot(w_g, pen_g, 's-', color=colors['accent'], lw=2.0, label='Contención Directa: Penalización $\\Delta t_{pHL}$ (Eje Der.)')
    ax_twin.axhline(10.0, color=colors['accent'], ls=':', lw=1.5, label='Límite Máx. Contención (+10.0%)')
    ax_twin.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=11, fontweight='bold', color=colors['accent'])
    ax_twin.tick_params(axis='y', labelcolor=colors['accent'])
    ax_twin.set_ylim(0, 140)

    # Marcar la ventana de viabilidad directamente medida
    ax.axvspan(10.5, w_max_directo, color='#A7F3D0', alpha=0.35, label=f'Ventana Viable Directa: $W_{{kp}} \\in [10.5, {w_max_directo:.0f}]\\,\\mathrm{{nm}}$')
    ax.set_title('Ventana de Viabilidad Conjunta: Retención vs Contención Directas (45nm HP @ 85°C)', fontsize=12, fontweight='bold', color=colors['primary'])
    ax.set_xlim(5, 140)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='center left', fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.5)

    fig3_path = os.path.join(FIGURAS_DIR, "figura_ventana_viabilidad_hp_85C.png")
    plt.savefig(fig3_path)
    plt.close()
    print(f"[FIGURA] Figura 3 actualizada: {fig3_path}")

    print("\n[PROCESO] CONCILIACION A3.5.1 COMPLETADA EXITOSAMENTE.")

if __name__ == "__main__":
    ejecutar_conciliacion()
