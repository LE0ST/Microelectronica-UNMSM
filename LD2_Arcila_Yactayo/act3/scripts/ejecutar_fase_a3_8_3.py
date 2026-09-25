# -*- coding: utf-8 -*-
"""
ejecutar_fase_a3_8_3.py
Script de ejecucion controlada para la Fase A3.8.3:
1. Retencion puntual Wkp=22nm @ 27°C y @ 85°C (ENS-A3-RET-22NM-27C / 85C)
2. Caracterizacion DC de NMOS de PDN @ 27°C y @ 85°C (ENS-A3-DC-01A-27C / 85C)
3. Caracterizacion DC de Fugas de Compuerta @ 27°C y @ 85°C (ENS-A3-DC-01C-27C / 85C)
4. Investigacion de GIDL por ablacion controlada @ 27°C y @ 85°C (ENS-A3-DC-01B-27C / 85C)
"""

import os
import sys
import shutil
import subprocess
import json

# Rutas del proyecto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

# Parsers
sys.path.append(os.path.join(LD2_DIR, "scripts", "lectura_resultados"))
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

def run_simulation(cir_name):
    cir_path = os.path.join(CIRCUITOS_DIR, cir_name)
    base_name = os.path.splitext(cir_name)[0]
    
    if not os.path.exists(cir_path):
        raise FileNotFoundError(f"Netlist no encontrado: {cir_path}")
        
    print(f"\n[EJECUTANDO] {cir_name} ...")
    cmd = [LTSPICE_EXE, "-b", cir_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"LTspice fallo en {cir_name} con codigo {res.returncode}: {res.stderr}")
        
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
        
    # Limpiar archivos en circuitos/
    for ext in [".log", ".raw", ".db", ".op.raw"]:
        f = os.path.join(CIRCUITOS_DIR, base_name + ext)
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass
                
    log_data = parse_log(dst_log)
    print(f"  -> Exito. Log valido: {log_data['is_valid']}, Warnings: {len(log_data.get('warnings', []))}")
    return dst_log, dst_raw, log_data

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)
    
    print("==================================================================")
    print("FASE A3.8.3: EJECUCION CONTROLADA DE ENSAYOS PENDIENTES")
    print("==================================================================")
    
    # -------------------------------------------------------------------------
    # ETAPA 1: Retencion Wkp=22nm (27C y 85C)
    # -------------------------------------------------------------------------
    ret_22nm_results = {}
    for temp, cir in [(27, "nand3_retencion_wkp_22nm_27C.cir"), (85, "nand3_retencion_wkp_22nm_85C.cir")]:
        log_path, raw_path, log_data = run_simulation(cir)
        meas = log_data["measurements"]
        
        vdyn_start = meas.get("vdyn_start")
        vdyn_end = meas.get("vdyn_end_1us")
        vdyn_min = meas.get("vdyn_min")
        t_cross = meas.get("t_cross_0p9vdd")
        isupply = meas.get("isupply_avg")
        ileak_pdn = meas.get("ileak_pdn_avg")
        ikp_inj = meas.get("ikp_inj_avg")
        
        # t_hold: si t_cross es None, esta censurado (> 1.0 us)
        t_hold = None if t_cross is None else (t_cross - 0.52e-9)
        estado_ret = "PASS" if (vdyn_end is not None and vdyn_end > 0.90) else "FALLA_CRITERIO"
        
        ret_22nm_results[f"T_{temp}C"] = {
            "ensayo_id": f"ENS-A3-RET-22NM-{temp}C",
            "netlist": cir,
            "temp_C": temp,
            "Wkp_nm": 22.0,
            "Weff_nm": 12.0,
            "vdyn_start_V": vdyn_start,
            "vdyn_end_1us_V": vdyn_end,
            "vdyn_min_V": vdyn_min,
            "t_cross_0p9vdd_s": t_cross,
            "t_hold_s": t_hold,
            "t_hold_str": "> 1.0 us (Censurado)" if t_hold is None else f"{t_hold*1e9:.2f} ns",
            "isupply_avg_A": isupply,
            "ileak_pdn_avg_A": ileak_pdn,
            "ikp_inj_avg_A": ikp_inj,
            "estado_retencion": estado_ret
        }
        print(f"  [22nm @ {temp}C] Vdyn(1us)={vdyn_end:.6f}V, Estado: {estado_ret}, Isupply={isupply*1e9:.3f}nA, Ileak_pdn={ileak_pdn*1e12:.2f}pA, Ikp_inj={ikp_inj*1e12:.2f}pA")

    # Guardar JSON de retencion 22nm
    path_ret_22 = os.path.join(DATOS_DIR, "act3_retencion_22nm.json")
    with open(path_ret_22, "w", encoding="utf-8") as f:
        json.dump(ret_22nm_results, f, indent=2)
    print(f"[OK] Guardado {path_ret_22}")

    # -------------------------------------------------------------------------
    # ETAPA 2: NMOS DC (27C y 85C)
    # -------------------------------------------------------------------------
    nmos_dc_results = {}
    for temp, cir in [(27, "dc_fugas_nmos_pdn_45hp_27C.cir"), (85, "dc_fugas_nmos_pdn_45hp_85C.cir")]:
        log_path, raw_path, log_data = run_simulation(cir)
        meas = log_data["measurements"]
        
        # parse_log para stepped measurements devuelve lista de valores
        # Pasos corresponden a Vsb = [0.0, 0.3, 0.6]
        vsb_steps = [0.0, 0.3, 0.6]
        step_data = []
        for i, vsb in enumerate(vsb_steps):
            def get_val(key):
                v = meas.get(key.lower())
                if v is None:
                    return None
                if isinstance(v, list):
                    if i < len(v):
                        item = v[i]
                        if isinstance(item, dict):
                            return item.get("val")
                        return item
                    return None
                if isinstance(v, dict):
                    return v.get("val")
                return v
                
            step_data.append({
                "step_index": i + 1,
                "Vsb_V": vsb,
                "Vgs_eff_V": get_val("vgs_eff"),
                "Vds_eff_V": get_val("vds_eff"),
                "Vsb_eff_V": get_val("vsb_eff"),
                "Vd_abs_V": get_val("vd_abs"),
                "Vg_abs_V": get_val("vg_abs"),
                "Vs_abs_V": get_val("vs_abs"),
                "Vb_abs_V": 0.0,
                "Ids_vds0p05_A": get_val("Ids_vds0p05"),
                "Ids_vds0p5_A": get_val("Ids_vds0p5"),
                "Ids_vds1p0_A": get_val("Ids_vds1p0"),
                "Ig_terminal_A": get_val("Ig_terminal"),
                "Ib_terminal_A": get_val("Ib_terminal"),
                "Is_terminal_A": get_val("Is_terminal")
            })
        nmos_dc_results[f"T_{temp}C"] = {
            "ensayo_id": f"ENS-A3-DC-01A-{temp}C",
            "netlist": cir,
            "temp_C": temp,
            "W_nm": 270.0,
            "L_nm": 45.0,
            "steps": step_data
        }
        for sd in step_data:
            print(f"  [NMOS DC @ {temp}C, Vsb={sd['Vsb_V']}V] Ids(1V)={sd['Ids_vds1p0_A']*1e12:.2f}pA, Ids(50mV)={sd['Ids_vds0p05_A']*1e12:.2f}pA, Ig={sd['Ig_terminal_A']*1e15:.2f}fA, Ib={sd['Ib_terminal_A']*1e15:.2f}fA")

    # -------------------------------------------------------------------------
    # ETAPA 3: Fuga de Compuerta (27C y 85C)
    # -------------------------------------------------------------------------
    gate_leak_results = {}
    for temp, cir in [(27, "dc_fugas_compuerta_45hp_27C.cir"), (85, "dc_fugas_compuerta_45hp_85C.cir")]:
        log_path, raw_path, log_data = run_simulation(cir)
        meas = log_data["measurements"]
        gate_leak_results[f"T_{temp}C"] = {
            "ensayo_id": f"ENS-A3-DC-01C-{temp}C",
            "netlist": cir,
            "temp_C": temp,
            "polarizacion_referencia": "dyn=1.0V, out=0.0V, clk=1.0V, vdd=1.0V",
            "dispositivos": {
                "M1_NMOS_PDN": {
                    "W_nm": 270.0,
                    "L_nm": 45.0,
                    "polarizacion": "Vd=1.0, Vg=0.0, Vs=0.0, Vb=0.0 (VGD=-1V, VGS=0V)",
                    "Ig_A": meas.get("ig_nmos_m1"),
                    "Id_A": meas.get("id_nmos_m1")
                },
                "Mp_PMOS_Precarga": {
                    "W_nm": 135.0,
                    "L_nm": 45.0,
                    "polarizacion": "Vd=1.0, Vg=1.0, Vs=1.0, Vb=1.0 (VGD=0V, VGS=0V)",
                    "Ig_A": meas.get("ig_pmos_mp"),
                    "Id_A": meas.get("id_pmos_mp")
                },
                "Mk_PMOS_Keeper": {
                    "W_nm": 45.0,
                    "L_nm": 45.0,
                    "polarizacion": "Vd=1.0, Vg=0.0, Vs=1.0, Vb=1.0 (VGD=1V, VGS=-1V)",
                    "Ig_A": meas.get("ig_pmos_mk"),
                    "Id_A": meas.get("id_pmos_mk")
                },
                "Mni_NMOS_Inversor": {
                    "W_nm": 90.0,
                    "L_nm": 45.0,
                    "polarizacion": "Vd=0.0, Vg=1.0, Vs=0.0, Vb=0.0 (VGD=1V, VGS=1V)",
                    "Ig_A": meas.get("ig_inv_n"),
                    "Id_A": meas.get("id_inv_n")
                },
                "Mpi_PMOS_Inversor": {
                    "W_nm": 135.0,
                    "L_nm": 45.0,
                    "polarizacion": "Vd=0.0, Vg=1.0, Vs=1.0, Vb=1.0 (VGD=1V, VGS=0V)",
                    "Ig_A": meas.get("ig_inv_p"),
                    "Id_A": meas.get("id_inv_p")
                }
            }
        }
        for k, v in gate_leak_results[f"T_{temp}C"]["dispositivos"].items():
            print(f"  [Gate Leak @ {temp}C - {k}] Ig = {v['Ig_A']*1e15:.3f} fA ({v['Ig_A']*1e12:.4f} pA)")

    # -------------------------------------------------------------------------
    # ETAPA 4: GIDL Controlado (27C y 85C)
    # -------------------------------------------------------------------------
    gidl_results = {}
    for temp, cir in [(27, "dc_investigacion_gidl_45hp_27C.cir"), (85, "dc_investigacion_gidl_45hp_85C.cir")]:
        log_path, raw_path, log_data = run_simulation(cir)
        meas = log_data["measurements"]
        id_canon = meas.get("id_canon")
        id_nogidl = meas.get("id_nogidl")
        delta_id = meas.get("delta_id_gidl")
        ib_canon = meas.get("ib_canon")
        ib_nogidl = meas.get("ib_nogidl")
        delta_ib = meas.get("delta_ib_gidl")
        
        gidl_results[f"T_{temp}C"] = {
            "ensayo_id": f"ENS-A3-DC-01B-{temp}C",
            "netlist": cir,
            "temp_C": temp,
            "W_nm": 270.0,
            "L_nm": 45.0,
            "Vds_eval_V": 1.0,
            "Vgs_eval_V": 0.0,
            "Id_canon_A": id_canon,
            "Id_nogidl_A": id_nogidl,
            "Delta_Id_gidl_A": delta_id,
            "Ib_canon_A": ib_canon,
            "Ib_nogidl_A": ib_nogidl,
            "Delta_Ib_gidl_A": delta_ib,
            "relacion_delta_vs_total": (delta_id / id_canon) if id_canon else 0.0
        }
        print(f"  [GIDL @ {temp}C] Id_canon={id_canon*1e12:.3f}pA, Id_nogidl={id_nogidl*1e12:.3f}pA, Delta_Id={delta_id:.3e}A, Delta_Ib={delta_ib:.3e}A")

    # -------------------------------------------------------------------------
    # ETAPA 5: Consolidacion de Caracterizacion DC
    # -------------------------------------------------------------------------
    dc_consolidado = {
        "descripcion": "Caracterizacion experimental DC de fugas y mecanismos en 45nm HP (Fase A3.8.3)",
        "NMOS_PDN": nmos_dc_results,
        "Fugas_Compuerta": gate_leak_results,
        "Investigacion_GIDL": gidl_results,
        "Contraste_Termico": {
            "explicacion": "Factores termicos I(85C)/I(27C) estrictamente comparados en los mismos puntos de polarizacion",
            "comparaciones": []
        }
    }
    
    # Calcular factores térmicos NMOS
    for i, vsb in enumerate([0.0, 0.3, 0.6]):
        s27 = nmos_dc_results["T_27C"]["steps"][i]
        s85 = nmos_dc_results["T_85C"]["steps"][i]
        factor_vds1p0 = s85["Ids_vds1p0_A"] / s27["Ids_vds1p0_A"]
        factor_vds0p05 = s85["Ids_vds0p05_A"] / s27["Ids_vds0p05_A"]
        dc_consolidado["Contraste_Termico"]["comparaciones"].append({
            "Vsb_V": vsb,
            "Ids_27C_vds1p0_pA": s27["Ids_vds1p0_A"] * 1e12,
            "Ids_85C_vds1p0_pA": s85["Ids_vds1p0_A"] * 1e12,
            "Factor_vds1p0": factor_vds1p0,
            "Ids_27C_vds0p05_pA": s27["Ids_vds0p05_A"] * 1e12,
            "Ids_85C_vds0p05_pA": s85["Ids_vds0p05_A"] * 1e12,
            "Factor_vds0p05": factor_vds0p05
        })
        print(f"  [Contraste Termico NMOS Vsb={vsb}V] Factor @ Vds=1.0V: {factor_vds1p0:.3f}x, Factor @ Vds=0.05V: {factor_vds0p05:.3f}x")

    path_dc_json = os.path.join(DATOS_DIR, "act3_fugas_caracterizacion_dc.json")
    with open(path_dc_json, "w", encoding="utf-8") as f:
        json.dump(dc_consolidado, f, indent=2)
    print(f"\n[OK] Dataset DC consolidado guardado en: {path_dc_json}")
    print("\n[PROCESO] EJECUCION CONTROLADA A3.8.3 COMPLETADA CON EXITO.")

if __name__ == "__main__":
    main()
