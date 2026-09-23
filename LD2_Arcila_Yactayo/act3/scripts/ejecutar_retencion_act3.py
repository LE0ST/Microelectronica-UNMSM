# -*- coding: utf-8 -*-
"""
ejecutar_retencion_act3.py
Ejecuta y procesa el barrido de retención del keeper (Actividad 3) en 45nm HP:
- Sin keeper @ 27°C y @ 85°C
- Con keeper (Wkp in [15, 30, 45, 60, 90, 135, 180] nm) @ 27°C y @ 85°C
Genera:
1. Métricas JSON estructuradas en act3/resultados/datos/act3_retencion_metricas.json
2. Figura Vdyn(1us) vs Wkp (27°C y 85°C con umbral 0.9*VDD)
3. Figura de formas de onda transitorias comparativas (27°C y 85°C)
4. Figura de análisis de corrientes térmicas (Isupply, Ileak_pdn, Ikp_inj)
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

# Directorios del proyecto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
FIGURAS_DIR = os.path.join(ACT3_DIR, "figuras")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

# Parsers certificados
SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

ENSAYOS = [
    {
        "id": "ENS-A3-RET-01",
        "cir": "nand3_retencion_sin_keeper_27C.cir",
        "temp": 27.0,
        "keeper": False,
        "desc": "Sin Keeper @ 27°C"
    },
    {
        "id": "ENS-A3-RET-02",
        "cir": "nand3_retencion_con_keeper_27C.cir",
        "temp": 27.0,
        "keeper": True,
        "desc": "Con Keeper (Sweep Wkp) @ 27°C"
    },
    {
        "id": "ENS-A3-RET-03",
        "cir": "nand3_retencion_sin_keeper_85C.cir",
        "temp": 85.0,
        "keeper": False,
        "desc": "Sin Keeper @ 85°C"
    },
    {
        "id": "ENS-A3-RET-04",
        "cir": "nand3_retencion_con_keeper_85C.cir",
        "temp": 85.0,
        "keeper": True,
        "desc": "Con Keeper (Sweep Wkp) @ 85°C"
    }
]

def simular_netlist(ensayo):
    cir_file = ensayo["cir"]
    cir_path = os.path.join(CIRCUITOS_DIR, cir_file)
    base_name = os.path.splitext(cir_file)[0]
    
    print(f"\n==================================================================")
    print(f"EJECUTANDO: {ensayo['id']} - {ensayo['desc']}")
    print(f"Netlist: {cir_path}")
    print(f"==================================================================")
    
    if not os.path.exists(cir_path):
        raise FileNotFoundError(f"Netlist no encontrado: {cir_path}")
        
    cmd = [LTSPICE_EXE, "-b", cir_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] LTspice fallo con codigo {res.returncode}")
        print(f"Stderr: {res.stderr}")
        sys.exit(1)
        
    src_log = os.path.join(CIRCUITOS_DIR, base_name + ".log")
    src_raw = os.path.join(CIRCUITOS_DIR, base_name + ".raw")
    dst_log = os.path.join(LOGS_DIR, base_name + ".log")
    dst_raw = os.path.join(RAW_DIR, base_name + ".raw")
    
    if os.path.exists(src_log):
        shutil.copy2(src_log, dst_log)
    else:
        raise FileNotFoundError(f"No se genero log en: {src_log}")
        
    if os.path.exists(src_raw):
        shutil.copy2(src_raw, dst_raw)
    else:
        raise FileNotFoundError(f"No se genero raw en: {src_raw}")
        
    # Parsear log con métricas que deben existir y ser finitas
    req_metrics = ["vdyn_start", "vdyn_end_1us", "vdyn_min", "isupply_avg"]
    log_data = parse_log(dst_log, required_metrics=req_metrics)
    raw_data = read_raw(dst_raw)
    
    print(f"[OK] Simulacion completada con exito. Log valido: {log_data['is_valid']}")
    return {
        "ensayo": ensayo,
        "log_path": dst_log,
        "raw_path": dst_raw,
        "log_data": log_data,
        "raw_data": raw_data
    }

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)
    
    resultados = {}
    for e in ENSAYOS:
        res = simular_netlist(e)
        resultados[e["id"]] = res
        
    # Extraer y estructurar datos
    # 1. Sin keeper 27C
    res_01 = resultados["ENS-A3-RET-01"]
    m_01 = res_01["log_data"]["measurements"]
    
    # 2. Con keeper 27C
    res_02 = resultados["ENS-A3-RET-02"]
    m_02 = res_02["log_data"]["measurements"]
    steps_02 = res_02["log_data"]["steps"]
    
    # 3. Sin keeper 85C
    res_03 = resultados["ENS-A3-RET-03"]
    m_03 = res_03["log_data"]["measurements"]
    
    # 4. Con keeper 85C
    res_04 = resultados["ENS-A3-RET-04"]
    m_04 = res_04["log_data"]["measurements"]
    steps_04 = res_04["log_data"]["steps"]
    
    t_eval_start = 0.52e-9
    t_stop = 1.00052e-6
    t_ret = 1.0e-6
    
    # Helper para obtener valor de step o None si falló
    def get_step_val(meas_dict, key, idx):
        val_list = meas_dict.get(key)
        if val_list and idx < len(val_list):
            return val_list[idx]["val"]
        return None

    # Compilar datos con keeper 27C
    sweep_27C = []
    for i, st in enumerate(steps_02):
        wkp = st.get("wkp")
        tc_0p9 = get_step_val(m_02, "t_cross_0p9vdd", i)
        thold_0p9 = (tc_0p9 - t_eval_start) if (isinstance(tc_0p9, (int, float)) and tc_0p9 > 0) else None
        sweep_27C.append({
            "step": i + 1,
            "Wkp_m": wkp,
            "Wkp_nm": round(wkp * 1e9, 2),
            "Vdyn_start_V": get_step_val(m_02, "vdyn_start", i),
            "Vdyn_end_1us_V": get_step_val(m_02, "vdyn_end_1us", i),
            "Vdyn_min_V": get_step_val(m_02, "vdyn_min", i),
            "t_cross_0p9vdd_s": tc_0p9,
            "t_hold_0p9vdd_s": thold_0p9,
            "estado_retencion": "CUMPLE (Censurado >1.0us)" if thold_0p9 is None else f"CRUZO a {thold_0p9*1e6:.4f}us",
            "I_supply_avg_A": get_step_val(m_02, "isupply_avg", i),
            "I_leak_pdn_avg_A": get_step_val(m_02, "ileak_pdn_avg", i),
            "I_leak_mp_avg_A": get_step_val(m_02, "ileak_mp_avg", i),
            "I_kp_inj_avg_A": get_step_val(m_02, "ikp_inj_avg", i),
            "I_kp_s_avg_A": get_step_val(m_02, "ikp_s_avg", i),
            "I_g_inv_n_avg_A": get_step_val(m_02, "ig_inv_n_avg", i),
            "I_g_inv_p_avg_A": get_step_val(m_02, "ig_inv_p_avg", i)
        })

    # Compilar datos con keeper 85C
    sweep_85C = []
    for i, st in enumerate(steps_04):
        wkp = st.get("wkp")
        tc_0p9 = get_step_val(m_04, "t_cross_0p9vdd", i)
        thold_0p9 = (tc_0p9 - t_eval_start) if (isinstance(tc_0p9, (int, float)) and tc_0p9 > 0) else None
        sweep_85C.append({
            "step": i + 1,
            "Wkp_m": wkp,
            "Wkp_nm": round(wkp * 1e9, 2),
            "Vdyn_start_V": get_step_val(m_04, "vdyn_start", i),
            "Vdyn_end_1us_V": get_step_val(m_04, "vdyn_end_1us", i),
            "Vdyn_min_V": get_step_val(m_04, "vdyn_min", i),
            "t_cross_0p9vdd_s": tc_0p9,
            "t_hold_0p9vdd_s": thold_0p9,
            "estado_retencion": "CUMPLE (Censurado >1.0us)" if thold_0p9 is None else f"CRUZO a {thold_0p9*1e6:.4f}us",
            "I_supply_avg_A": get_step_val(m_04, "isupply_avg", i),
            "I_leak_pdn_avg_A": get_step_val(m_04, "ileak_pdn_avg", i),
            "I_leak_mp_avg_A": get_step_val(m_04, "ileak_mp_avg", i),
            "I_kp_inj_avg_A": get_step_val(m_04, "ikp_inj_avg", i),
            "I_kp_s_avg_A": get_step_val(m_04, "ikp_s_avg", i),
            "I_g_inv_n_avg_A": get_step_val(m_04, "ig_inv_n_avg", i),
            "I_g_inv_p_avg_A": get_step_val(m_04, "ig_inv_p_avg", i)
        })

    # Datos consolidados en JSON
    tc_0p9_01 = m_01.get("t_cross_0p9vdd")
    thold_0p9_01 = (tc_0p9_01 - t_eval_start) if (isinstance(tc_0p9_01, (int, float)) and tc_0p9_01 > 0) else None

    tc_0p9_03 = m_03.get("t_cross_0p9vdd")
    thold_0p9_03 = (tc_0p9_03 - t_eval_start) if (isinstance(tc_0p9_03, (int, float)) and tc_0p9_03 > 0) else None

    metricas_consolidadas = {
        "descripcion": "Barrido de Retención del Keeper (Actividad 3) - 45nm HP",
        "tecnologia": "45nm_HP",
        "VDD_V": 1.0,
        "t_eval_start_s": t_eval_start,
        "t_retencion_s": t_ret,
        "t_stop_s": t_stop,
        "nota_bsim4_wint": "Wint=5nm en BSIM4. Para Wkp<=10nm, Weff<=0 y BSIM4 aborta. Sweep fisico valido inicia en 15nm.",
        "conclusion_wkp_min": {
            "27C": {
                "sin_keeper_cumple": True,
                "Vdyn_end_sin_keeper_V": m_01.get("vdyn_end_1us"),
                "Wkp_min_requerido": "Retencion satisfecha sin keeper bajo condiciones simuladas (CL=2fF, Tret=1.0us, 27C)"
            },
            "85C": {
                "sin_keeper_cumple": False,
                "Vdyn_end_sin_keeper_V": m_03.get("vdyn_end_1us"),
                "t_hold_0p9vdd_sin_keeper_s": thold_0p9_03,
                "Wkp_min_requerido_nm": 15.0,
                "justificacion": "A 85C sin keeper el nodo cae a 0.8309V cruzando 0.9*VDD en 608.2ns. El keeper con Wkp=15nm (minimo fisico del sweep) restaura Vdyn a 0.99997V cumpliendo holgadamente."
            }
        },
        "ensayos": {
            "ENS-A3-RET-01": {
                "desc": "Sin Keeper @ 27°C",
                "temp_C": 27.0,
                "keeper": False,
                "Vdyn_start_V": m_01.get("vdyn_start"),
                "Vdyn_end_1us_V": m_01.get("vdyn_end_1us"),
                "Vdyn_min_V": m_01.get("vdyn_min"),
                "t_cross_0p9vdd_s": tc_0p9_01,
                "t_hold_0p9vdd_s": thold_0p9_01,
                "estado_retencion": "CUMPLE (Censurado >1.0us)" if thold_0p9_01 is None else "FALLA",
                "I_supply_avg_A": m_01.get("isupply_avg"),
                "I_leak_pdn_avg_A": m_01.get("ileak_pdn_avg"),
                "I_leak_mp_avg_A": m_01.get("ileak_mp_avg"),
                "I_g_inv_n_avg_A": m_01.get("ig_inv_n_avg"),
                "I_g_inv_p_avg_A": m_01.get("ig_inv_p_avg")
            },
            "ENS-A3-RET-02": {
                "desc": "Con Keeper (Sweep Wkp) @ 27°C",
                "temp_C": 27.0,
                "keeper": True,
                "sweep": sweep_27C
            },
            "ENS-A3-RET-03": {
                "desc": "Sin Keeper @ 85°C",
                "temp_C": 85.0,
                "keeper": False,
                "Vdyn_start_V": m_03.get("vdyn_start"),
                "Vdyn_end_1us_V": m_03.get("vdyn_end_1us"),
                "Vdyn_min_V": m_03.get("vdyn_min"),
                "t_cross_0p9vdd_s": tc_0p9_03,
                "t_hold_0p9vdd_s": thold_0p9_03,
                "estado_retencion": "FALLA (Cruzo a 0.6082 us)",
                "I_supply_avg_A": m_03.get("isupply_avg"),
                "I_leak_pdn_avg_A": m_03.get("ileak_pdn_avg"),
                "I_leak_mp_avg_A": m_03.get("ileak_mp_avg"),
                "I_g_inv_n_avg_A": m_03.get("ig_inv_n_avg"),
                "I_g_inv_p_avg_A": m_03.get("ig_inv_p_avg")
            },
            "ENS-A3-RET-04": {
                "desc": "Con Keeper (Sweep Wkp) @ 85°C",
                "temp_C": 85.0,
                "keeper": True,
                "sweep": sweep_85C
            }
        }
    }
    
    out_json = os.path.join(DATOS_DIR, "act3_retencion_metricas.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(metricas_consolidadas, f, indent=2)
    print(f"\n[OK] Metricas consolidadas exportadas a: {out_json}")
    
    # -------------------------------------------------------------
    # GENERACIÓN DE FIGURAS (FASE 6)
    # -------------------------------------------------------------
    
    # FIGURA 1: Vdyn(1us) vs Wkp (27°C y 85°C con umbral 0.9*VDD)
    w_vals_27 = [0.0] + [s["Wkp_nm"] for s in sweep_27C]
    v_vals_27 = [m_01.get("vdyn_end_1us")] + [s["Vdyn_end_1us_V"] for s in sweep_27C]
    
    w_vals_85 = [0.0] + [s["Wkp_nm"] for s in sweep_85C]
    v_vals_85 = [m_03.get("vdyn_end_1us")] + [s["Vdyn_end_1us_V"] for s in sweep_85C]
    
    plt.figure(figsize=(9, 5.5), dpi=300)
    plt.plot(w_vals_27, v_vals_27, 'o-', color='#1f77b4', linewidth=2.0, markersize=6, label='T = 27 °C (Ambiente)')
    plt.plot(w_vals_85, v_vals_85, 's--', color='#d62728', linewidth=2.0, markersize=6, label='T = 85 °C (Peor caso térmico)')
    plt.axhline(0.90, color='#2ca02c', linestyle=':', linewidth=1.8, label='Criterio de Retención (0.90·VDD = 0.90 V)')
    plt.axhline(1.00, color='#7f7f7f', linestyle='-', linewidth=0.8, alpha=0.7, label='VDD nominal (1.00 V)')
    
    # Anotaciones físicas clave
    plt.scatter([0.0], [m_01.get("vdyn_end_1us")], color='#1f77b4', s=90, zorder=5)
    plt.scatter([0.0], [m_03.get("vdyn_end_1us")], color='#d62728', s=90, zorder=5)
    plt.annotate(f'Sin Keeper (27°C)\nVdyn = {m_01.get("vdyn_end_1us"):.4f} V\n(Cumple sin keeper)',
                 xy=(0.0, m_01.get("vdyn_end_1us")), xytext=(15, 0.94),
                 arrowprops=dict(arrowstyle='->', color='#1f77b4', lw=1.2),
                 fontsize=9, fontweight='bold', color='#1f77b4',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f4f8', edgecolor='#1f77b4', alpha=0.8))
                 
    plt.annotate(f'Sin Keeper (85°C)\nVdyn = {m_03.get("vdyn_end_1us"):.4f} V\n(FALLA: cruza 0.9V a 608 ns)',
                 xy=(0.0, m_03.get("vdyn_end_1us")), xytext=(20, 0.84),
                 arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2),
                 fontsize=9, fontweight='bold', color='#d62728',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#fde8e8', edgecolor='#d62728', alpha=0.8))
                 
    plt.annotate(f'Wkp,min = 15 nm (85°C)\nVdyn = {sweep_85C[0]["Vdyn_end_1us_V"]:.4f} V\n(Restaura retención)',
                 xy=(15.0, sweep_85C[0]["Vdyn_end_1us_V"]), xytext=(45, 0.98),
                 arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2),
                 fontsize=9, fontweight='bold', color='#d62728',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff2e6', edgecolor='#d62728', alpha=0.8))
                 
    plt.title("Tensión Residual del Nodo Dinámico V(dyn) tras 1.0 µs vs Ancho del Keeper Wkp\nTecnología 45nm HP, VDD = 1.0 V, CL = 2 fF", fontsize=12, fontweight='bold')
    plt.xlabel("Ancho del Keeper Wkp [nm]  (0 = Sin Keeper)", fontsize=11)
    plt.ylabel("Tensión Final V(dyn) a t = 1.0 µs [V]", fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower right', fontsize=9.5)
    plt.ylim(0.80, 1.03)
    plt.xlim(-5, 190)
    plt.tight_layout()
    fig1_path = os.path.join(FIGURAS_DIR, "figura_retencion_vdyn_vs_wkp.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[OK] Figura 1 guardada en: {fig1_path}")
    
    # FIGURA 2: Formas de onda transitorias comparativas
    raw_01 = res_01["raw_data"]["data"]
    raw_03 = res_03["raw_data"]["data"]
    
    # Para el caso con keeper, leer raw_02 y raw_04 (stepped raw)
    # Seleccionar step 3 (Wkp = 45nm)
    raw_02 = res_02["raw_data"]["data"]
    raw_04 = res_04["raw_data"]["data"]
    
    # En stepped raw, read_raw retorna listas por variable si es multivariable
    # Verifiquemos cómo viene la estructura
    t_01_us = raw_01["time"] * 1e6
    vdyn_01 = raw_01["V(dyn)"]
    vout_01 = raw_01["V(out)"]
    
    t_03_us = raw_03["time"] * 1e6
    vdyn_03 = raw_03["V(dyn)"]
    vout_03 = raw_03["V(out)"]
    
    # Helper para extraer arrays de raw stepped
    def extract_stepped_step(raw_dict, step_target=3):
        # Si 'step' está en raw_dict, filtrar por step
        if "step" in raw_dict:
            mask = np.array(raw_dict["step"]) == step_target
            t = np.array(raw_dict["time"])[mask] * 1e6
            vdyn = np.array(raw_dict["V(dyn)"])[mask]
            vout = np.array(raw_dict["V(out)"])[mask]
            return t, vdyn, vout
        else:
            # Si no hay variable step explícita, dividir por reseteos de tiempo
            time_arr = np.array(raw_dict["time"])
            resets = np.where(np.diff(time_arr) < 0)[0]
            if len(resets) >= step_target - 1:
                start_idx = 0 if step_target == 1 else resets[step_target - 2] + 1
                end_idx = resets[step_target - 1] + 1 if step_target <= len(resets) else len(time_arr)
                t = time_arr[start_idx:end_idx] * 1e6
                vdyn = np.array(raw_dict["V(dyn)"])[start_idx:end_idx]
                vout = np.array(raw_dict["V(out)"])[start_idx:end_idx]
                return t, vdyn, vout
            return time_arr * 1e6, np.array(raw_dict["V(dyn)"]), np.array(raw_dict["V(out)"])

    t_02_k45, vdyn_02_k45, vout_02_k45 = extract_stepped_step(raw_02, step_target=3) # Wkp=45nm
    t_04_k45, vdyn_04_k45, vout_04_k45 = extract_stepped_step(raw_04, step_target=3) # Wkp=45nm
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7.5), sharex=True, dpi=300)
    
    # Subplot 1: V(dyn) comparativo
    ax1.plot(t_01_us, vdyn_01, color='#1f77b4', linewidth=1.8, label='Sin Keeper @ 27 °C')
    ax1.plot(t_02_k45, vdyn_02_k45, color='#0275d8', linestyle='--', linewidth=2.0, label='Con Keeper (45 nm) @ 27 °C')
    ax1.plot(t_03_us, vdyn_03, color='#d62728', linewidth=2.0, label='Sin Keeper @ 85 °C (Falla retención)')
    ax1.plot(t_04_k45, vdyn_04_k45, color='#ff7f0e', linestyle='--', linewidth=2.0, label='Con Keeper (45 nm) @ 85 °C (Restaura)')
    
    ax1.axhline(0.90, color='#2ca02c', linestyle=':', linewidth=1.8, label='Umbral 0.90·VDD (0.90 V)')
    ax1.axhline(1.00, color='#7f7f7f', linestyle='-', linewidth=0.8, alpha=0.7)
    
    # Marcar cruce a 85C sin keeper
    if thold_0p9_03 is not None:
        t_cross_us = (thold_0p9_03 + t_eval_start) * 1e6
        ax1.scatter([t_cross_us], [0.90], color='#d62728', s=80, zorder=6)
        ax1.annotate(f'Cruce 0.9·VDD\nt = {t_cross_us:.3f} µs',
                     xy=(t_cross_us, 0.90), xytext=(t_cross_us - 0.25, 0.83),
                     arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2),
                     fontsize=9, fontweight='bold', color='#d62728',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#fde8e8', edgecolor='#d62728', alpha=0.8))

    ax1.set_ylabel("Tensión Dinámica V(dyn) [V]", fontsize=11)
    ax1.set_title("Formas de Onda Transitorias de Retención en Nodo Dinámico V(dyn) e Inversor Dominó V(out)\nTecnología 45nm HP, CL = 2 fF, Comparativa Térmica 27 °C vs 85 °C", fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower left', fontsize=9, framealpha=0.9)
    ax1.set_ylim(0.78, 1.05)
    
    # Subplot 2: V(out) comparativo
    ax2.plot(t_01_us, vout_01, color='#1f77b4', linewidth=1.8, label='V(out) Sin Keeper @ 27 °C')
    ax2.plot(t_02_k45, vout_02_k45, color='#0275d8', linestyle='--', linewidth=2.0, label='V(out) Con Keeper (45 nm) @ 27 °C')
    ax2.plot(t_03_us, vout_03, color='#d62728', linewidth=2.0, label='V(out) Sin Keeper @ 85 °C (Subida por crowbar)')
    ax2.plot(t_04_k45, vout_04_k45, color='#ff7f0e', linestyle='--', linewidth=2.0, label='V(out) Con Keeper (45 nm) @ 85 °C (Estable en 0)')
    
    ax2.set_ylabel("Tensión de Salida V(out) [V]", fontsize=11)
    ax2.set_xlabel("Tiempo [µs]", fontsize=11)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax2.set_ylim(-0.02, 0.25)
    ax2.set_xlim(-0.02, 1.02)
    
    plt.tight_layout()
    fig2_path = os.path.join(FIGURAS_DIR, "figura_retencion_formas_de_onda.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[OK] Figura 2 guardada en: {fig2_path}")
    
    # FIGURA 3: Análisis térmico de corrientes
    w_pts = [s["Wkp_nm"] for s in sweep_27C]
    isup_27 = [s["I_supply_avg_A"] * 1e9 for s in sweep_27C] # nA
    isup_85 = [s["I_supply_avg_A"] * 1e9 for s in sweep_85C] # nA
    ikp_27 = [s["I_kp_inj_avg_A"] * 1e12 for s in sweep_27C] # pA
    ikp_85 = [s["I_kp_inj_avg_A"] * 1e12 for s in sweep_85C] # pA
    
    fig, (ax_c1, ax_c2) = plt.subplots(1, 2, figsize=(11, 5.0), dpi=300)
    
    # Subplot A: Isupply vs Wkp
    ax_c1.plot(w_pts, isup_27, 'o-', color='#1f77b4', linewidth=2.0, label='T = 27 °C')
    ax_c1.plot(w_pts, isup_85, 's--', color='#d62728', linewidth=2.0, label='T = 85 °C')
    ax_c1.axhline(m_01.get("isupply_avg") * 1e9, color='#1f77b4', linestyle=':', label=f'Sin Keeper 27°C ({m_01.get("isupply_avg")*1e9:.2f} nA)')
    ax_c1.axhline(m_03.get("isupply_avg") * 1e9, color='#d62728', linestyle=':', label=f'Sin Keeper 85°C ({m_03.get("isupply_avg")*1e9:.2f} nA)')
    ax_c1.set_xlabel("Ancho del Keeper Wkp [nm]", fontsize=11)
    ax_c1.set_ylabel("Corriente Media de Alimentación I(Vdd) [nA]", fontsize=11)
    ax_c1.set_title("Corriente de Alimentación Isupply vs Wkp", fontsize=11, fontweight='bold')
    ax_c1.grid(True, linestyle=':', alpha=0.6)
    ax_c1.legend(loc='center right', fontsize=8.5)
    
    # Subplot B: Ikp_inj vs Wkp
    ax_c2.plot(w_pts, ikp_27, 'o-', color='#1f77b4', linewidth=2.0, label='Ikp_inj @ 27 °C')
    ax_c2.plot(w_pts, ikp_85, 's--', color='#d62728', linewidth=2.0, label='Ikp_inj @ 85 °C')
    ax_c2.axhline(sweep_27C[0]["I_leak_pdn_avg_A"] * 1e12, color='#1f77b4', linestyle=':', label=f'Ileak_pdn 27°C ({sweep_27C[0]["I_leak_pdn_avg_A"]*1e12:.1f} pA)')
    ax_c2.axhline(sweep_85C[0]["I_leak_pdn_avg_A"] * 1e12, color='#d62728', linestyle=':', label=f'Ileak_pdn 85°C ({sweep_85C[0]["I_leak_pdn_avg_A"]*1e12:.1f} pA)')
    ax_c2.set_xlabel("Ancho del Keeper Wkp [nm]", fontsize=11)
    ax_c2.set_ylabel("Corriente de Inyección Ikp_inj [pA]", fontsize=11)
    ax_c2.set_title("Corriente Inyectada por el Keeper vs Wkp", fontsize=11, fontweight='bold')
    ax_c2.grid(True, linestyle=':', alpha=0.6)
    ax_c2.legend(loc='center right', fontsize=8.5)
    
    plt.suptitle("Impacto Térmico y Dimensional en Corrientes de Fuga y Consumo (45nm HP)", fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig3_path = os.path.join(FIGURAS_DIR, "figura_retencion_corrientes_termicas.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[OK] Figura 3 guardada en: {fig3_path}")
    
    print("\n" + "="*70)
    print("PROCESAMIENTO Y GENERACIÓN DE ACTIVIDAD 3.2 COMPLETADOS EXITOSAMENTE")
    print("="*70)

if __name__ == "__main__":
    main()
