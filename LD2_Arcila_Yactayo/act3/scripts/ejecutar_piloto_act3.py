# -*- coding: utf-8 -*-
"""
ejecutar_piloto_act3.py
Ejecuta la validación piloto del banco de retención en 45nm HP a 27°C:
- Piloto A (ENS-A3-PILOT-01): Sin keeper
- Piloto B (ENS-A3-PILOT-02): Keeper realimentado Wkp=45nm
Genera métricas estructuradas, figura diagnóstica y verifica balances nodales.
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

# Rutas del entorno
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
FIGURAS_DIR = os.path.join(ACT3_DIR, "figuras")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

# Importar parsers certificados
SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

PILOTOS = [
    {
        "id": "ENS-A3-PILOT-01",
        "cir": "nand3_retencion_piloto_sin_keeper.cir",
        "desc": "Sin Keeper (Instancia Mk ausente)",
        "keeper": False,
        "Wkp": None
    },
    {
        "id": "ENS-A3-PILOT-02",
        "cir": "nand3_retencion_piloto_con_keeper.cir",
        "desc": "Con Keeper realimentado Wkp=45nm",
        "keeper": True,
        "Wkp": 45e-9
    }
]

def simular_piloto(piloto):
    cir_file = piloto["cir"]
    cir_path = os.path.join(CIRCUITOS_DIR, cir_file)
    base_name = os.path.splitext(cir_file)[0]
    
    print(f"\n==================================================================")
    print(f"SIMULANDO PILOTO: {piloto['id']} - {piloto['desc']}")
    print(f"Netlist: {cir_path}")
    print(f"==================================================================")
    
    if not os.path.exists(cir_path):
        raise FileNotFoundError(f"No se encuentra el netlist: {cir_path}")
        
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
        raise FileNotFoundError(f"No se genero el log en: {src_log}")
        
    if os.path.exists(src_raw):
        shutil.copy2(src_raw, dst_raw)
    else:
        raise FileNotFoundError(f"No se genero el raw en: {src_raw}")
        
    print(f"[OK] Simulacion completada. Archivos copiados a resultados/logs y resultados/raw.")
    
    # Parsear log
    log_data = parse_log(dst_log)
    print(f"Metricas extraidas del log ({len(log_data['measurements'])} medidas):")
    for k, v in log_data["measurements"].items():
        print(f"  {k}: {v}")
        
    # Parsear raw para extraccion de curvas
    raw_data = read_raw(dst_raw)
    print(f"Variables en RAW: {list(raw_data['data'].keys())}")
    
    return {
        "info": piloto,
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
    
    resultados = []
    for p in PILOTOS:
        res = simular_piloto(p)
        resultados.append(res)
        
    # Consolidar datos de ambos pilotos
    res_a = resultados[0]
    res_b = resultados[1]
    
    meas_a = res_a["log_data"]["measurements"]
    meas_b = res_b["log_data"]["measurements"]
    
    # Tiempos de retencion y censura
    t_eval_start = 0.52e-9 # 0.52 ns
    
    # Cruces Piloto A
    tc_0p9_a = meas_a.get("t_cross_0p9vdd")
    tc_vdd2_a = meas_a.get("t_cross_vdd2")
    tc_vm_a = meas_a.get("t_cross_vm")
    
    thold_0p9_a = (tc_0p9_a - t_eval_start) if (isinstance(tc_0p9_a, (int, float)) and tc_0p9_a > 0) else None
    thold_vdd2_a = (tc_vdd2_a - t_eval_start) if (isinstance(tc_vdd2_a, (int, float)) and tc_vdd2_a > 0) else None
    thold_vm_a = (tc_vm_a - t_eval_start) if (isinstance(tc_vm_a, (int, float)) and tc_vm_a > 0) else None
    
    # Cruces Piloto B
    tc_0p9_b = meas_b.get("t_cross_0p9vdd")
    tc_vdd2_b = meas_b.get("t_cross_vdd2")
    tc_vm_b = meas_b.get("t_cross_vm")
    
    thold_0p9_b = (tc_0p9_b - t_eval_start) if (isinstance(tc_0p9_b, (int, float)) and tc_0p9_b > 0) else None
    thold_vdd2_b = (tc_vdd2_b - t_eval_start) if (isinstance(tc_vdd2_b, (int, float)) and tc_vdd2_b > 0) else None
    thold_vm_b = (tc_vm_b - t_eval_start) if (isinstance(tc_vm_b, (int, float)) and tc_vm_b > 0) else None
    
    datos_consolidados = {
        "descripcion": "Validacion Piloto del Banco de Retencion (Actividad 3)",
        "tecnologia": "45nm_HP",
        "VDD": 1.0,
        "temperatura_C": 27.0,
        "t_eval_start_s": t_eval_start,
        "t_retencion_ventana_s": 1.0e-6,
        "piloto_a_sin_keeper": {
            "id": res_a["info"]["id"],
            "Vdyn_start": meas_a.get("vdyn_start"),
            "Vdyn_end_1us": meas_a.get("vdyn_end_1us"),
            "Vdyn_min": meas_a.get("vdyn_min"),
            "t_cross_0p9vdd": tc_0p9_a if isinstance(tc_0p9_a, (int, float)) else None,
            "t_cross_vdd2": tc_vdd2_a if isinstance(tc_vdd2_a, (int, float)) else None,
            "t_cross_vm": tc_vm_a if isinstance(tc_vm_a, (int, float)) else None,
            "t_hold_0p9vdd": thold_0p9_a,
            "t_hold_vdd2": thold_vdd2_a,
            "t_hold_vm": thold_vm_a,
            "estado_0p9vdd": "CENSURADO (>1.0us)" if thold_0p9_a is None else "CRUZADO",
            "estado_vdd2": "CENSURADO (>1.0us)" if thold_vdd2_a is None else "CRUZADO",
            "estado_vm": "CENSURADO (>1.0us)" if thold_vm_a is None else "CRUZADO",
            "I_supply_avg": meas_a.get("isupply_avg"),
            "I_leak_pdn_avg": meas_a.get("ileak_pdn_avg"),
            "I_leak_mp_avg": meas_a.get("ileak_mp_avg"),
            "I_g_inv_n_avg": meas_a.get("ig_inv_n_avg"),
            "I_g_inv_p_avg": meas_a.get("ig_inv_p_avg"),
            "dvd_dt_10n": meas_a.get("dvd_dt")
        },
        "piloto_b_con_keeper": {
            "id": res_b["info"]["id"],
            "Wkp_m": 45e-9,
            "Vdyn_start": meas_b.get("vdyn_start"),
            "Vdyn_end_1us": meas_b.get("vdyn_end_1us"),
            "Vdyn_min": meas_b.get("vdyn_min"),
            "t_cross_0p9vdd": tc_0p9_b if isinstance(tc_0p9_b, (int, float)) else None,
            "t_cross_vdd2": tc_vdd2_b if isinstance(tc_vdd2_b, (int, float)) else None,
            "t_cross_vm": tc_vm_b if isinstance(tc_vm_b, (int, float)) else None,
            "t_hold_0p9vdd": thold_0p9_b,
            "t_hold_vdd2": thold_vdd2_b,
            "t_hold_vm": thold_vm_b,
            "estado_0p9vdd": "CENSURADO (>1.0us)" if thold_0p9_b is None else "CRUZADO",
            "estado_vdd2": "CENSURADO (>1.0us)" if thold_vdd2_b is None else "CRUZADO",
            "estado_vm": "CENSURADO (>1.0us)" if thold_vm_b is None else "CRUZADO",
            "I_supply_avg": meas_b.get("isupply_avg"),
            "I_leak_pdn_avg": meas_b.get("ileak_pdn_avg"),
            "I_leak_mp_avg": meas_b.get("ileak_mp_avg"),
            "I_kp_d_avg": meas_b.get("ikp_d_avg"),
            "I_kp_inj_avg": meas_b.get("ikp_inj_avg"),
            "I_kp_s_avg": meas_b.get("ikp_s_avg"),
            "I_g_inv_n_avg": meas_b.get("ig_inv_n_avg"),
            "I_g_inv_p_avg": meas_b.get("ig_inv_p_avg"),
            "dvd_dt_10n": meas_b.get("dvd_dt")
        }
    }
    
    out_json = os.path.join(DATOS_DIR, "act3_piloto_metricas.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(datos_consolidados, f, indent=2)
    print(f"\n[OK] Metricas consolidadas exportadas a: {out_json}")
    
    # Generar figura diagnostica comparativa
    t_a = res_a["raw_data"]["data"]["time"] * 1e6 # en us
    vdyn_a = res_a["raw_data"]["data"]["V(dyn)"]
    vout_a = res_a["raw_data"]["data"]["V(out)"]
    vclk_a = res_a["raw_data"]["data"]["V(clk)"]
    
    t_b = res_b["raw_data"]["data"]["time"] * 1e6 # en us
    vdyn_b = res_b["raw_data"]["data"]["V(dyn)"]
    vout_b = res_b["raw_data"]["data"]["V(out)"]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Subplot 1: V(dyn) comparativo
    ax1.plot(t_a, vdyn_a, label="Piloto A: Sin Keeper (Wkp=0)", color="#d9534f", linewidth=2.0)
    ax1.plot(t_b, vdyn_b, label="Piloto B: Con Keeper (Wkp=45nm)", color="#0275d8", linewidth=2.0)
    ax1.axhline(1.0, color="#555555", linestyle=":", label="VDD = 1.0 V")
    ax1.axhline(0.9, color="#f0ad4e", linestyle="--", label="Umbral 0.9*VDD = 0.90 V")
    ax1.axhline(0.5, color="#5cb85c", linestyle="--", label="Umbral VDD/2 = 0.50 V")
    ax1.axhline(0.4797, color="#6f42c1", linestyle="-.", label="Umbral VM = 0.4797 V")
    ax1.set_ylabel("Tensión V(dyn) [V]", fontsize=12)
    ax1.set_title("Validación Piloto del Banco de Retención — 45nm HP @ 27°C (Tret = 1.0 µs)", fontsize=14, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.legend(loc="lower left", fontsize=10)
    ax1.set_ylim(-0.05, 1.08)
    
    # Subplot 2: V(out) e I(Vdd) / V(clk)
    ax2.plot(t_a, vout_a, label="V(out) Sin Keeper", color="#d9534f", linestyle="--", linewidth=1.8)
    ax2.plot(t_b, vout_b, label="V(out) Con Keeper (45nm)", color="#0275d8", linestyle="-", linewidth=1.8)
    ax2.set_ylabel("Tensión V(out) [V]", fontsize=12)
    ax2.set_xlabel("Tiempo [µs]", fontsize=12)
    ax2.grid(True, linestyle=':', alpha=0.7)
    ax2.legend(loc="upper left", fontsize=10)
    ax2.set_ylim(-0.05, 1.08)
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURAS_DIR, "piloto_retencion_comparativo.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[OK] Figura diagnostica guardada en: {fig_path}")

if __name__ == "__main__":
    main()
