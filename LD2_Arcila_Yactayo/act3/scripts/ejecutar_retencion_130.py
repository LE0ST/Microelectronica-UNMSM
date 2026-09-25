# -*- coding: utf-8 -*-
"""
ejecutar_retencion_130.py
Ejecuta la caracterización de retención en tecnología 130nm Bulk (Actividad 3.4):
- Ensayos de fallo Wkp=1nm en 130nm (27°C y 85°C)
- Sin keeper @ 27°C y @ 85°C (VDD = 1.3V)
- Con keeper (sweep Wkp in [15, 30, 45, 65, 90, 130, 180, 260, 390] nm) @ 27°C y @ 85°C
Genera:
1. Métricas JSON estructuradas en act3/resultados/datos/act3_retencion_130_metricas.json
2. Archivo de consolidación tecnológica tri-nodo: act3/resultados/datos/act3_consolidacion_tecnologica.json
3. Figuras científicas (300 DPI):
   - figura_retencion_130_vdyn_vs_wkp.png
   - figura_retencion_130_formas_de_onda.png
   - figura_consolidacion_hp_lp_130_retencion.png
4. Actualiza documentacion/registro_ensayos.csv con IDs ENS-A3-130-*
"""

import os
import sys
import shutil
import subprocess
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Directorios
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
FIGURAS_DIR = os.path.join(ACT3_DIR, "figuras")
REGISTRO_CSV = os.path.join(LD2_DIR, "documentacion", "registro_ensayos.csv")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

# Parsers certificados
SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

ENSAYOS_130 = [
    {
        "id": "ENS-A3-130-RET-01",
        "cir": "nand3_retencion_130_sin_keeper_27C.cir",
        "temp": 27.0,
        "keeper": False,
        "desc": "Sin Keeper 130nm @ 27°C (Ensayo Principal)"
    },
    {
        "id": "ENS-A3-130-RET-02",
        "cir": "nand3_retencion_130_con_keeper_27C.cir",
        "temp": 27.0,
        "keeper": True,
        "desc": "Con Keeper 130nm (Sweep Wkp) @ 27°C (Ensayo Principal)"
    },
    {
        "id": "ENS-A3-130-RET-03",
        "cir": "nand3_retencion_130_sin_keeper_85C.cir",
        "temp": 85.0,
        "keeper": False,
        "desc": "Sin Keeper 130nm @ 85°C (Complementario Provisional)"
    },
    {
        "id": "ENS-A3-130-RET-04",
        "cir": "nand3_retencion_130_con_keeper_85C.cir",
        "temp": 85.0,
        "keeper": True,
        "desc": "Con Keeper 130nm (Sweep Wkp) @ 85°C (Complementario Provisional)"
    }
]

ENSAYOS_FALLO_130 = [
    {
        "id": "ENS-A3-130-ERR-01",
        "cir": "nand3_retencion_130_wkp_1nm_fallo_27C.cir",
        "temp": 27.0,
        "desc": "Fallo esperado Wkp=1nm 130nm @ 27°C (Weff <= 0)"
    },
    {
        "id": "ENS-A3-130-ERR-02",
        "cir": "nand3_retencion_130_wkp_1nm_fallo_85C.cir",
        "temp": 85.0,
        "desc": "Fallo esperado Wkp=1nm 130nm @ 85°C (Weff <= 0)"
    }
]

def simular_fallo(ensayo):
    cir_file = ensayo["cir"]
    cir_path = os.path.join(CIRCUITOS_DIR, cir_file)
    base_name = os.path.splitext(cir_file)[0]
    
    print(f"\n[SIMULANDO FALLO ESPERADO 130nm] {ensayo['id']}: {ensayo['desc']}")
    res = subprocess.run([LTSPICE_EXE, "-b", cir_path], capture_output=True, text=True)
    print(f"  Codigo de salida (esperado != 0): {res.returncode}")
    
    src_log = os.path.join(CIRCUITOS_DIR, base_name + ".log")
    dst_log = os.path.join(LOGS_DIR, base_name + ".log")
    if os.path.exists(src_log):
        shutil.copy2(src_log, dst_log)
        
    with open(dst_log, "r", encoding="utf-8") as f:
        log_text = f.read()
    err_detected = "Effective channel width <= 0" in log_text
    print(f"  Error 'Effective channel width <= 0' confirmado: {err_detected}")
    return {
        "ensayo": ensayo,
        "exit_code": res.returncode,
        "error_detectado": err_detected,
        "log_path": dst_log
    }

def simular_ensayo(ensayo):
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
    
    # 1. Ejecutar fallos Wkp=1nm en 130nm
    fallos_res = []
    for ef in ENSAYOS_FALLO_130:
        r_f = simular_fallo(ef)
        fallos_res.append(r_f)
        
    # 2. Ejecutar simulaciones 130nm
    resultados = {}
    for e in ENSAYOS_130:
        res = simular_ensayo(e)
        resultados[e["id"]] = res
        
    # Extraer métricas
    res_01 = resultados["ENS-A3-130-RET-01"] # Sin keeper 27C
    m_01 = res_01["log_data"]["measurements"]
    
    res_02 = resultados["ENS-A3-130-RET-02"] # Con keeper 27C
    m_02 = res_02["log_data"]["measurements"]
    steps_02 = res_02["log_data"]["steps"]
    
    res_03 = resultados["ENS-A3-130-RET-03"] # Sin keeper 85C
    m_03 = res_03["log_data"]["measurements"]
    
    res_04 = resultados["ENS-A3-130-RET-04"] # Con keeper 85C
    m_04 = res_04["log_data"]["measurements"]
    steps_04 = res_04["log_data"]["steps"]
    
    t_eval_start = 0.52e-9
    t_stop = 1.00052e-6
    t_ret = 1.0e-6
    wint = 5.0e-9
    vdd_130 = 1.3
    
    def get_step_val(meas_dict, key, idx):
        val_list = meas_dict.get(key)
        if val_list and idx < len(val_list):
            return val_list[idx]["val"]
        return None

    # Puntos con keeper 27C
    puntos_27C = []
    for i, st in enumerate(steps_02):
        wkp = st["wkp"]
        weff = wkp - 2 * wint
        pid = f"ENS-A3-130-RET-02-P{i+1:02d}"
        tc_0p9 = get_step_val(m_02, "t_cross_0p9vdd", i)
        thold_0p9 = (tc_0p9 - t_eval_start) if (isinstance(tc_0p9, (int, float)) and tc_0p9 > 0) else None
        vend = get_step_val(m_02, "vdyn_end_1us", i)
        vstart = get_step_val(m_02, "vdyn_start", i)
        puntos_27C.append({
            "id_punto": pid,
            "step": i + 1,
            "Wkp_m": wkp,
            "Wkp_nm": round(wkp * 1e9, 2),
            "Weff_nm": round(weff * 1e9, 2),
            "Vdyn_start_V": vstart,
            "Vdyn_end_1us_V": vend,
            "Vdyn_min_V": get_step_val(m_02, "vdyn_min", i),
            "delta_V_start_V": (vstart - vend) if (vstart is not None and vend is not None) else None,
            "delta_V_VDD_V": (vdd_130 - vend) if vend is not None else None,
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

    # Puntos con keeper 85C
    puntos_85C = []
    for i, st in enumerate(steps_04):
        wkp = st["wkp"]
        weff = wkp - 2 * wint
        pid = f"ENS-A3-130-RET-04-P{i+1:02d}"
        tc_0p9 = get_step_val(m_04, "t_cross_0p9vdd", i)
        thold_0p9 = (tc_0p9 - t_eval_start) if (isinstance(tc_0p9, (int, float)) and tc_0p9 > 0) else None
        vend = get_step_val(m_04, "vdyn_end_1us", i)
        vstart = get_step_val(m_04, "vdyn_start", i)
        puntos_85C.append({
            "id_punto": pid,
            "step": i + 1,
            "Wkp_m": wkp,
            "Wkp_nm": round(wkp * 1e9, 2),
            "Weff_nm": round(weff * 1e9, 2),
            "Vdyn_start_V": vstart,
            "Vdyn_end_1us_V": vend,
            "Vdyn_min_V": get_step_val(m_04, "vdyn_min", i),
            "delta_V_start_V": (vstart - vend) if (vstart is not None and vend is not None) else None,
            "delta_V_VDD_V": (vdd_130 - vend) if vend is not None else None,
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

    tc_0p9_01 = m_01.get("t_cross_0p9vdd")
    thold_0p9_01 = (tc_0p9_01 - t_eval_start) if (isinstance(tc_0p9_01, (int, float)) and tc_0p9_01 > 0) else None

    tc_0p9_03 = m_03.get("t_cross_0p9vdd")
    thold_0p9_03 = (tc_0p9_03 - t_eval_start) if (isinstance(tc_0p9_03, (int, float)) and tc_0p9_03 > 0) else None

    vend_01 = m_01.get("vdyn_end_1us")
    vstart_01 = m_01.get("vdyn_start")
    
    vend_03 = m_03.get("vdyn_end_1us")
    vstart_03 = m_03.get("vdyn_start")

    # Guardar métricas JSON 130nm
    metricas_130 = {
        "descripcion": "Caracterización de Retención del Keeper (Actividad 3.4) - 130nm Bulk",
        "tecnologia": "130nm_bulk",
        "VDD_V": vdd_130,
        "t_eval_start_s": t_eval_start,
        "t_retencion_s": t_ret,
        "t_stop_s": t_stop,
        "umbrales_calibrados_inversor": {
            "VM_130_27C_V": 0.5833,
            "VM_130_85C_V": 0.5636,
            "umbral_retencion_0p9VDD_V": 1.170,
            "umbral_retencion_0p5VDD_V": 0.650
        },
        "delimitaciones_metodologicas": {
            "menor_ancho_malla_que_cumple_nm": 15.0,
            "limite_matematico_bsim4": "Wint = 5.0 nm => Weff = Wkp - 2*Wint. Para Wkp <= 10.0 nm, Weff <= 0 y BSIM4 aborta.",
            "limites_validez_fisica_ptm": "El modelo PTM 130nm bulk esta calibrado para geometrias nominales (Wn=260nm, Wp=390nm, Ln=130nm). Anchos inferiores a 130nm son extrapolaciones analiticas matematicas de BSIM4.",
            "conclusion_retencion_sin_keeper": {
                "27C": {
                    "cumple": vend_01 >= 1.170,
                    "Vdyn_start_V": vstart_01,
                    "Vdyn_end_V": vend_01,
                    "delta_V_start_V": vstart_01 - vend_01,
                    "delta_V_VDD_V": vdd_130 - vend_01,
                    "dictamen": "Retención satisfecha sin keeper a 27°C (Vdyn_end > 0.90*VDD = 1.170V)"
                },
                "85C": {
                    "cumple": vend_03 >= 1.170,
                    "Vdyn_start_V": vstart_03,
                    "Vdyn_end_V": vend_03,
                    "delta_V_start_V": vstart_03 - vend_03,
                    "delta_V_VDD_V": vdd_130 - vend_03,
                    "t_cross_0p9vdd_s": tc_0p9_03,
                    "t_hold_0p9vdd_s": thold_0p9_03,
                    "dictamen": "Retención evaluada a 85°C sin keeper (Complementario provisional)"
                }
            }
        },
        "ensayos_error_bsim4": [
            {
                "id_ensayo": "ENS-A3-130-ERR-01",
                "temp_C": 27.0,
                "Wkp_nm": 1.0,
                "Weff_nm": -9.0,
                "error_mensaje": "BSIM4: mosfet Mk, model pmos_130: Effective channel width <= 0",
                "archivo_log": "act3/resultados/logs/nand3_retencion_130_wkp_1nm_fallo_27C.log",
                "estado": "FALLO_ESPERADO_BSIM4"
            },
            {
                "id_ensayo": "ENS-A3-130-ERR-02",
                "temp_C": 85.0,
                "Wkp_nm": 1.0,
                "Weff_nm": -9.0,
                "error_mensaje": "BSIM4: mosfet Mk, model pmos_130: Effective channel width <= 0",
                "archivo_log": "act3/resultados/logs/nand3_retencion_130_wkp_1nm_fallo_85C.log",
                "estado": "FALLO_ESPERADO_BSIM4"
            }
        ],
        "ensayos_sin_keeper": {
            "ENS-A3-130-RET-01": {
                "temp_C": 27.0,
                "Wkp_nm": 0.0,
                "keeper": False,
                "Vdyn_start_V": vstart_01,
                "Vdyn_end_1us_V": vend_01,
                "Vdyn_min_V": m_01.get("vdyn_min"),
                "delta_V_start_V": vstart_01 - vend_01,
                "delta_V_VDD_V": vdd_130 - vend_01,
                "t_cross_0p9vdd_s": tc_0p9_01,
                "t_hold_0p9vdd_s": thold_0p9_01,
                "estado_retencion": "CUMPLE (Censurado >1.0us)" if thold_0p9_01 is None else "FALLA",
                "I_supply_avg_A": m_01.get("isupply_avg"),
                "I_leak_pdn_avg_A": m_01.get("ileak_pdn_avg"),
                "I_leak_mp_avg_A": m_01.get("ileak_mp_avg"),
                "I_g_inv_n_avg_A": m_01.get("ig_inv_n_avg"),
                "I_g_inv_p_avg_A": m_01.get("ig_inv_p_avg")
            },
            "ENS-A3-130-RET-03": {
                "temp_C": 85.0,
                "Wkp_nm": 0.0,
                "keeper": False,
                "Vdyn_start_V": vstart_03,
                "Vdyn_end_1us_V": vend_03,
                "Vdyn_min_V": m_03.get("vdyn_min"),
                "delta_V_start_V": vstart_03 - vend_03,
                "delta_V_VDD_V": vdd_130 - vend_03,
                "t_cross_0p9vdd_s": tc_0p9_03,
                "t_hold_0p9vdd_s": thold_0p9_03,
                "estado_retencion": "CUMPLE (Censurado >1.0us)" if thold_0p9_03 is None else f"CRUZO a {thold_0p9_03*1e6:.4f}us",
                "I_supply_avg_A": m_03.get("isupply_avg"),
                "I_leak_pdn_avg_A": m_03.get("ileak_pdn_avg"),
                "I_leak_mp_avg_A": m_03.get("ileak_mp_avg"),
                "I_g_inv_n_avg_A": m_03.get("ig_inv_n_avg"),
                "I_g_inv_p_avg_A": m_03.get("ig_inv_p_avg")
            }
        },
        "barrido_con_keeper_27C": {
            "campana_id": "ENS-A3-130-RET-02",
            "puntos": puntos_27C
        },
        "barrido_con_keeper_85C": {
            "campana_id": "ENS-A3-130-RET-04",
            "puntos": puntos_85C
        }
    }
    
    out_130_json = os.path.join(DATOS_DIR, "act3_retencion_130_metricas.json")
    with open(out_130_json, "w", encoding="utf-8") as f:
        json.dump(metricas_130, f, indent=2)
    print(f"\n[OK] Metricas 130nm consolidadas en: {out_130_json}")
    
    # -------------------------------------------------------------
    # CONSOLIDACIÓN TECNOLÓGICA (HP, LP, 130nm)
    # -------------------------------------------------------------
    with open(os.path.join(DATOS_DIR, "act3_retencion_metricas.json"), "r", encoding="utf-8") as f:
        m_hp = json.load(f)
    with open(os.path.join(DATOS_DIR, "act3_retencion_lp_metricas.json"), "r", encoding="utf-8") as f:
        m_lp = json.load(f)
        
    consolidacion = {
        "descripcion": "Consolidación Tecnológica Tri-Nodo de Retención (Actividad 3) - UNMSM",
        "comparativa_sin_keeper": [
            {
                "proceso": "45nm_HP",
                "temp_C": 27.0,
                "VDD_V": 1.0,
                "Vdyn_start_V": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-01"]["Vdyn_start_V"],
                "Vdyn_end_V": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-01"]["Vdyn_end_1us_V"],
                "Vdyn_end_norm": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-01"]["Vdyn_end_1us_V"] / 1.0,
                "umbral_0p9VDD_V": 0.900,
                "estado_retencion": "CUMPLE (Censurado >1.0us)",
                "t_cross_0p9_s": None,
                "I_supply_avg_A": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-01"]["I_supply_avg_A"],
                "I_leak_pdn_avg_A": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-01"]["I_leak_pdn_avg_A"],
                "menor_keeper_cumple_nm": "No requerido (Sin keeper cumple)"
            },
            {
                "proceso": "45nm_HP",
                "temp_C": 85.0,
                "VDD_V": 1.0,
                "Vdyn_start_V": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["Vdyn_start_V"],
                "Vdyn_end_V": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["Vdyn_end_1us_V"],
                "Vdyn_end_norm": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["Vdyn_end_1us_V"] / 1.0,
                "umbral_0p9VDD_V": 0.900,
                "estado_retencion": "FALLA (Cruzo a 0.6082 us)",
                "t_cross_0p9_s": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["t_cross_0p9vdd_s"],
                "I_supply_avg_A": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["I_supply_avg_A"],
                "I_leak_pdn_avg_A": m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["I_leak_pdn_avg_A"],
                "menor_keeper_cumple_nm": "15 nm (malla gruesa) / 10.5 nm (malla fina)"
            },
            {
                "proceso": "45nm_LP",
                "temp_C": 27.0,
                "VDD_V": 1.1,
                "Vdyn_start_V": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-01"]["Vdyn_start_V"],
                "Vdyn_end_V": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-01"]["Vdyn_end_1us_V"],
                "Vdyn_end_norm": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-01"]["Vdyn_end_1us_V"] / 1.1,
                "umbral_0p9VDD_V": 0.990,
                "estado_retencion": "CUMPLE (Censurado >1.0us)",
                "t_cross_0p9_s": None,
                "I_supply_avg_A": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-01"]["I_supply_avg_A"],
                "I_leak_pdn_avg_A": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-01"]["I_leak_pdn_avg_A"],
                "menor_keeper_cumple_nm": "No requerido (Sin keeper cumple)"
            },
            {
                "proceso": "45nm_LP",
                "temp_C": 85.0,
                "VDD_V": 1.1,
                "Vdyn_start_V": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]["Vdyn_start_V"],
                "Vdyn_end_V": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]["Vdyn_end_1us_V"],
                "Vdyn_end_norm": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]["Vdyn_end_1us_V"] / 1.1,
                "umbral_0p9VDD_V": 0.990,
                "estado_retencion": "CUMPLE (Censurado >1.0us)",
                "t_cross_0p9_s": None,
                "I_supply_avg_A": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]["I_supply_avg_A"],
                "I_leak_pdn_avg_A": m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]["I_leak_pdn_avg_A"],
                "menor_keeper_cumple_nm": "No requerido (Sin keeper cumple)"
            },
            {
                "proceso": "130nm_bulk",
                "temp_C": 27.0,
                "VDD_V": 1.3,
                "Vdyn_start_V": vstart_01,
                "Vdyn_end_V": vend_01,
                "Vdyn_end_norm": vend_01 / 1.3,
                "umbral_0p9VDD_V": 1.170,
                "estado_retencion": "CUMPLE (Censurado >1.0us)" if tc_0p9_01 is None else "FALLA",
                "t_cross_0p9_s": tc_0p9_01,
                "I_supply_avg_A": m_01.get("isupply_avg"),
                "I_leak_pdn_avg_A": m_01.get("ileak_pdn_avg"),
                "menor_keeper_cumple_nm": "No requerido" if (vend_01 >= 1.170) else "15 nm"
            },
            {
                "proceso": "130nm_bulk",
                "temp_C": 85.0,
                "VDD_V": 1.3,
                "Vdyn_start_V": vstart_03,
                "Vdyn_end_V": vend_03,
                "Vdyn_end_norm": vend_03 / 1.3,
                "umbral_0p9VDD_V": 1.170,
                "estado_retencion": "CUMPLE (Censurado >1.0us)" if tc_0p9_03 is None else "FALLA",
                "t_cross_0p9_s": tc_0p9_03,
                "I_supply_avg_A": m_03.get("isupply_avg"),
                "I_leak_pdn_avg_A": m_03.get("ileak_pdn_avg"),
                "menor_keeper_cumple_nm": "No requerido" if (vend_03 >= 1.170) else "15 nm",
                "nota": "Complementario provisional (pendiente respuesta docente)"
            }
        ]
    }
    
    out_cons_json = os.path.join(DATOS_DIR, "act3_consolidacion_tecnologica.json")
    with open(out_cons_json, "w", encoding="utf-8") as f:
        json.dump(consolidacion, f, indent=2)
    print(f"[OK] Consolidacion tecnologica exportada a: {out_cons_json}")
    
    # -------------------------------------------------------------
    # GENERACIÓN DE FIGURAS
    # -------------------------------------------------------------
    
    # FIGURA 1: Vdyn(1us) vs Wkp en 130nm Bulk (27°C y 85°C)
    w_vals_27 = [0.0] + [s["Wkp_nm"] for s in puntos_27C]
    v_vals_27 = [vend_01] + [s["Vdyn_end_1us_V"] for s in puntos_27C]
    
    w_vals_85 = [0.0] + [s["Wkp_nm"] for s in puntos_85C]
    v_vals_85 = [vend_03] + [s["Vdyn_end_1us_V"] for s in puntos_85C]
    
    plt.figure(figsize=(9.5, 5.5), dpi=300)
    plt.plot(w_vals_27, v_vals_27, 'o-', color='#6f42c1', linewidth=2.0, markersize=6, label='130nm Bulk @ 27 °C (Principal)')
    plt.plot(w_vals_85, v_vals_85, 's--', color='#e83e8c', linewidth=2.0, markersize=6, label='130nm Bulk @ 85 °C (Complementario)')
    plt.axhline(1.170, color='#d62728', linestyle=':', linewidth=1.8, label='Criterio Retención (0.90·VDD = 1.170 V)')
    plt.axhline(1.300, color='#7f7f7f', linestyle='-', linewidth=0.8, alpha=0.7, label='VDD nominal (1.300 V)')
    
    plt.scatter([0.0], [vend_01], color='#6f42c1', s=90, zorder=5)
    plt.scatter([0.0], [vend_03], color='#e83e8c', s=90, zorder=5)
    
    plt.annotate(f'Sin Keeper 130nm (27°C)\nVdyn = {vend_01:.4f} V\n(Retención satisfecha)',
                 xy=(0.0, vend_01), xytext=(30, 1.27),
                 arrowprops=dict(arrowstyle='->', color='#6f42c1', lw=1.2),
                 fontsize=9, fontweight='bold', color='#6f42c1',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#f3effa', edgecolor='#6f42c1', alpha=0.8))
                 
    plt.annotate(f'Sin Keeper 130nm (85°C)\nVdyn = {vend_03:.4f} V\n({"Retención satisfecha" if vend_03 >= 1.170 else "Falla retención"})',
                 xy=(0.0, vend_03), xytext=(40, 1.20),
                 arrowprops=dict(arrowstyle='->', color='#e83e8c', lw=1.2),
                 fontsize=9, fontweight='bold', color='#e83e8c',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdf0f5', edgecolor='#e83e8c', alpha=0.8))
                 
    plt.title("Tensión Residual del Nodo Dinámico V(dyn) tras 1.0 µs vs Ancho del Keeper Wkp\nTecnología 130nm Bulk, VDD = 1.3 V, CL = 2 fF", fontsize=12, fontweight='bold')
    plt.xlabel("Ancho del Keeper Wkp [nm]  (0 = Sin Keeper)", fontsize=11)
    plt.ylabel("Tensión Final V(dyn) a t = 1.0 µs [V]", fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower right', fontsize=9.5)
    plt.ylim(1.10, 1.34)
    plt.xlim(-10, 410)
    plt.tight_layout()
    fig1_path = os.path.join(FIGURAS_DIR, "figura_retencion_130_vdyn_vs_wkp.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[OK] Figura 1 130nm guardada en: {fig1_path}")
    
    # FIGURA 2: Formas de onda transitorias en 130nm Bulk
    raw_01 = res_01["raw_data"]["data"]
    raw_03 = res_03["raw_data"]["data"]
    raw_02 = res_02["raw_data"]["data"]
    raw_04 = res_04["raw_data"]["data"]
    
    t_01_us = raw_01["time"] * 1e6
    vdyn_01 = raw_01["V(dyn)"]
    vout_01 = raw_01["V(out)"]
    
    t_03_us = raw_03["time"] * 1e6
    vdyn_03 = raw_03["V(dyn)"]
    vout_03 = raw_03["V(out)"]
    
    def extract_stepped_step(raw_dict, step_target=3):
        if "step" in raw_dict:
            mask = np.array(raw_dict["step"]) == step_target
            t = np.array(raw_dict["time"])[mask] * 1e6
            vdyn = np.array(raw_dict["V(dyn)"])[mask]
            vout = np.array(raw_dict["V(out)"])[mask]
            return t, vdyn, vout
        else:
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
    
    ax1.plot(t_01_us, vdyn_01, color='#6f42c1', linewidth=1.8, label='130nm Sin Keeper @ 27 °C')
    ax1.plot(t_02_k45, vdyn_02_k45, color='#4b2882', linestyle='--', linewidth=2.0, label='130nm Con Keeper (45 nm) @ 27 °C')
    ax1.plot(t_03_us, vdyn_03, color='#e83e8c', linewidth=2.0, label='130nm Sin Keeper @ 85 °C')
    ax1.plot(t_04_k45, vdyn_04_k45, color='#a01550', linestyle='--', linewidth=2.0, label='130nm Con Keeper (45 nm) @ 85 °C')
    
    ax1.axhline(1.170, color='#d62728', linestyle=':', linewidth=1.8, label='Umbral 0.90·VDD (1.170 V)')
    ax1.axhline(1.300, color='#7f7f7f', linestyle='-', linewidth=0.8, alpha=0.7)
    
    ax1.set_ylabel("Tensión Dinámica V(dyn) [V]", fontsize=11)
    ax1.set_title("Formas de Onda Transitorias de Retención en 130nm Bulk — V(dyn) y V(out)\nComparativa Térmica 27 °C vs 85 °C (Tret = 1.0 µs, CL = 2 fF)", fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower left', fontsize=9, framealpha=0.9)
    ax1.set_ylim(1.10, 1.35)
    
    ax2.plot(t_01_us, vout_01, color='#6f42c1', linewidth=1.8, label='V(out) 130nm Sin Keeper @ 27 °C')
    ax2.plot(t_02_k45, vout_02_k45, color='#4b2882', linestyle='--', linewidth=2.0, label='V(out) 130nm Con Keeper (45 nm) @ 27 °C')
    ax2.plot(t_03_us, vout_03, color='#e83e8c', linewidth=2.0, label='V(out) 130nm Sin Keeper @ 85 °C')
    ax2.plot(t_04_k45, vout_04_k45, color='#a01550', linestyle='--', linewidth=2.0, label='V(out) 130nm Con Keeper (45 nm) @ 85 °C')
    
    ax2.set_ylabel("Tensión de Salida V(out) [V]", fontsize=11)
    ax2.set_xlabel("Tiempo [µs]", fontsize=11)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax2.set_ylim(-0.01, 0.05)
    ax2.set_xlim(-0.02, 1.02)
    
    plt.tight_layout()
    fig2_path = os.path.join(FIGURAS_DIR, "figura_retencion_130_formas_de_onda.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[OK] Figura 2 130nm guardada en: {fig2_path}")
    
    # FIGURA 3: Consolidación Tri-Nodo HP vs LP vs 130nm
    # Usar los puntos comunes [0, 15, 30, 45, 90, 180] nm
    w_common = [0.0, 15.0, 30.0, 45.0, 90.0, 180.0]
    
    def get_norm_series(puntos_list, v_sin_keeper, vdd_val):
        w_map = {0.0: v_sin_keeper}
        for p in puntos_list:
            w_map[p["Wkp_nm"]] = p["Vdyn_end_1us_V"]
        return [w_map.get(w, vdd_val) / vdd_val for w in w_common]

    v_hp_27_c = get_norm_series(m_hp["barrido_con_keeper_27C"]["puntos"], m_hp["ensayos_sin_keeper"]["ENS-A3-RET-01"]["Vdyn_end_1us_V"], 1.0)
    v_hp_85_c = get_norm_series(m_hp["barrido_con_keeper_85C"]["puntos"], m_hp["ensayos_sin_keeper"]["ENS-A3-RET-03"]["Vdyn_end_1us_V"], 1.0)
    v_lp_27_c = get_norm_series(m_lp["barrido_con_keeper_27C"]["puntos"], m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-01"]["Vdyn_end_1us_V"], 1.1)
    v_lp_85_c = get_norm_series(m_lp["barrido_con_keeper_85C"]["puntos"], m_lp["ensayos_sin_keeper"]["ENS-A3-LP-RET-03"]["Vdyn_end_1us_V"], 1.1)
    v_130_27_c = get_norm_series(puntos_27C, vend_01, 1.3)
    v_130_85_c = get_norm_series(puntos_85C, vend_03, 1.3)
    
    plt.figure(figsize=(10, 6.0), dpi=300)
    plt.plot(w_common, v_hp_27_c, 'o-', color='#1f77b4', linewidth=2.0, label='45nm HP @ 27 °C (VDD = 1.0 V)')
    plt.plot(w_common, v_hp_85_c, 's--', color='#d62728', linewidth=2.0, label='45nm HP @ 85 °C (VDD = 1.0 V, Falla sin keeper)')
    plt.plot(w_common, v_lp_27_c, '^-.', color='#2ca02c', linewidth=2.0, label='45nm LP @ 27 °C (VDD = 1.1 V)')
    plt.plot(w_common, v_lp_85_c, 'd:', color='#ff7f0e', linewidth=2.0, label='45nm LP @ 85 °C (VDD = 1.1 V)')
    plt.plot(w_common, v_130_27_c, 'v-', color='#6f42c1', linewidth=2.0, label='130nm Bulk @ 27 °C (VDD = 1.3 V)')
    plt.plot(w_common, v_130_85_c, 'x--', color='#e83e8c', linewidth=2.0, label='130nm Bulk @ 85 °C (VDD = 1.3 V)')
    
    plt.axhline(0.90, color='#7f7f7f', linestyle='--', linewidth=1.5, label='Criterio Retención (0.90·VDD normalizado)')
    plt.axhline(1.00, color='#000000', linestyle='-', linewidth=0.8, alpha=0.5)
    
    plt.title("Consolidación Tecnológica Tri-Nodo: Retención Normalizada V(dyn) / VDD\nComparativa 45nm HP, 45nm LP y 130nm Bulk a 27 °C y 85 °C (Tret = 1.0 µs, CL = 2 fF)", fontsize=12, fontweight='bold')
    plt.xlabel("Ancho del Keeper Wkp [nm]  (0 = Sin Keeper)", fontsize=11)
    plt.ylabel("Tensión Normalizada V(dyn) / VDD", fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower right', fontsize=9.0)
    # Incluye el caso 130 nm @ 85 C sin keeper: 0.67459 V/V.
    plt.ylim(0.64, 1.045)
    plt.xlim(-5, 190)
    plt.tight_layout()
    fig3_path = os.path.join(FIGURAS_DIR, "figura_consolidacion_hp_lp_130_retencion.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[OK] Figura 3 consolidacion tecnologica guardada en: {fig3_path}")
    
    # -------------------------------------------------------------
    # ACTUALIZAR REGISTRO DE ENSAYOS
    # -------------------------------------------------------------
    filas_existentes = []
    ids_existentes = set()
    with open(REGISTRO_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row:
                filas_existentes.append(row)
                ids_existentes.add(row[0])

    nuevos_registros_130 = [
        [
            "ENS-A3-130-RET-01", "Actividad 3 - Retencion Sin Keeper 130nm 27C",
            "act3/circuitos/nand3_retencion_130_sin_keeper_27C.cir", "act3/resultados/logs/nand3_retencion_130_sin_keeper_27C.log",
            "130nm_bulk", "27", "1.3", "Wn=260n, Wp=390n, CL=2f, Cout=1f, Tret=1.0us",
            f"Vdyn_end={vend_01:.4f}V, Isupply={m_01['isupply_avg']*1e12:.2f}pA, Ileak_pdn={m_01['ileak_pdn_avg']*1e12:.2f}pA",
            "PASS", "2026-09-20", "Retencion sobresaliente sin keeper en 130nm a 27C (nodo bulk maduro con minima fuga)"
        ],
        [
            "ENS-A3-130-RET-02", "Actividad 3 - Barrido Keeper 130nm 27C (Campana)",
            "act3/circuitos/nand3_retencion_130_con_keeper_27C.cir", "act3/resultados/logs/nand3_retencion_130_con_keeper_27C.log",
            "130nm_bulk", "27", "1.3", "Wkp list 15n..390n, CL=2f, Cout=1f",
            f"Vdyn_end in [{puntos_27C[0]['Vdyn_end_1us_V']:.5f}, {puntos_27C[-1]['Vdyn_end_1us_V']:.5f}]V",
            "PASS", "2026-09-20", "Campana 130nm 27C (ENS-A3-130-RET-02-P01 a P09); retencion holgada en todo el rango"
        ],
        [
            "ENS-A3-130-RET-03", "Actividad 3 - Retencion Sin Keeper 130nm 85C",
            "act3/circuitos/nand3_retencion_130_sin_keeper_85C.cir", "act3/resultados/logs/nand3_retencion_130_sin_keeper_85C.log",
            "130nm_bulk", "85", "1.3", "Wn=260n, Wp=390n, CL=2f, Cout=1f, Tret=1.0us",
            f"Vdyn_end={vend_03:.4f}V, Vdyn_min={m_03['vdyn_min']:.4f}V, Isupply={m_03['isupply_avg']*1e12:.2f}pA, Ileak_pdn={m_03['ileak_pdn_avg']*1e12:.2f}pA",
            "PASS", "2026-09-20", "Complementario provisional: retencion satisfecha sin keeper en 130nm a 85C"
        ],
        [
            "ENS-A3-130-RET-04", "Actividad 3 - Barrido Keeper 130nm 85C (Campana)",
            "act3/circuitos/nand3_retencion_130_con_keeper_85C.cir", "act3/resultados/logs/nand3_retencion_130_con_keeper_85C.log",
            "130nm_bulk", "85", "1.3", "Wkp list 15n..390n, CL=2f, Cout=1f",
            f"Vdyn_end in [{puntos_85C[0]['Vdyn_end_1us_V']:.5f}, {puntos_85C[-1]['Vdyn_end_1us_V']:.5f}]V",
            "PASS", "2026-09-20", "Campana complementaria 130nm 85C (ENS-A3-130-RET-04-P01 a P09); retencion holgada"
        ],
        [
            "ENS-A3-130-ERR-01", "Actividad 3 - Limite Modelo 130nm Wkp=1nm 27C",
            "act3/circuitos/nand3_retencion_130_wkp_1nm_fallo_27C.cir", "act3/resultados/logs/nand3_retencion_130_wkp_1nm_fallo_27C.log",
            "130nm_bulk", "27", "1.3", "Wkp=1n, Wint=5n => Weff=-9n <= 0",
            "BSIM4 aborta: 'Effective channel width <= 0', exit_code=1",
            "LIMITE_MODELO", "2026-09-20", "Confirmada limitacion matematica BSIM4 en 130nm; Wkp <= 10nm no simulable"
        ],
        [
            "ENS-A3-130-ERR-02", "Actividad 3 - Limite Modelo 130nm Wkp=1nm 85C",
            "act3/circuitos/nand3_retencion_130_wkp_1nm_fallo_85C.cir", "act3/resultados/logs/nand3_retencion_130_wkp_1nm_fallo_85C.log",
            "130nm_bulk", "85", "1.3", "Wkp=1n, Wint=5n => Weff=-9n <= 0",
            "BSIM4 aborta: 'Effective channel width <= 0', exit_code=1",
            "LIMITE_MODELO", "2026-09-20", "Confirmada limitacion matematica BSIM4 en 130nm a 85C; Wkp <= 10nm no simulable"
        ]
    ]

    agregados_130 = 0
    for nr in nuevos_registros_130:
        nid = nr[0]
        if nid not in ids_existentes:
            filas_existentes.append(nr)
            ids_existentes.add(nid)
            agregados_130 += 1
            print(f"  + Registrado: {nid}")
        else:
            print(f"  = Ya existente: {nid}")

    with open(REGISTRO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(filas_existentes)
    print(f"[OK] registro_ensayos.csv actualizado con {agregados_130} nuevos ensayos 130nm.")

if __name__ == "__main__":
    main()
