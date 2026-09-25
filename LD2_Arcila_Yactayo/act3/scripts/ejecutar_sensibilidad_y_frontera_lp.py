# -*- coding: utf-8 -*-
"""
ejecutar_sensibilidad_y_frontera_lp.py
Ejecuta:
1. ENS-A3-LP-RET-FRONTERA-85: Retención directa en 45nm LP @ 85°C para Wkp in [35, 36, 37] nm.
2. ENS-A3-LP-SENS-B-BASE: Referencia base sin keeper bajo Configuración B (reltol=1e-5, tstep=0.5ps).
3. ENS-A3-LP-SENS-A-SWEEP: Barrido Wkp in [34, 35, 36, 37] nm bajo Configuración A (reltol=1e-4, tstep=2ps).
4. ENS-A3-LP-SENS-B-SWEEP: Barrido Wkp in [34, 35, 36, 37] nm bajo Configuración B (reltol=1e-5, tstep=0.5ps).

Consolida:
- Comparación de sensibilidad numérica LP (Config A vs Config B).
- Retención directa en la frontera LP.
- Actualización canónica de act3_contencion_lp_metricas.json.
"""

import os
import sys
import subprocess
import shutil
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")

SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log
from parse_spice_raw import read_raw

LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

def run_simulation(cir_name, force=False):
    cir_path = os.path.join(CIRCUITOS_DIR, cir_name)
    base_name = os.path.splitext(cir_name)[0]
    log_path = os.path.join(CIRCUITOS_DIR, f"{base_name}.log")
    raw_path = os.path.join(CIRCUITOS_DIR, f"{base_name}.raw")
    dest_log = os.path.join(LOGS_DIR, f"{base_name}.log")
    dest_raw = os.path.join(RAW_DIR, f"{base_name}.raw")

    if not force and os.path.exists(dest_log) and os.path.getsize(dest_log) > 0:
        print(f"[CACHE] {cir_name} ya existe en logs/. Omitiendo corrida.")
        return dest_log, dest_raw

    print(f"[SIMULACION] Ejecutando {cir_name}...")
    cmd = [LTSPICE_EXE, "-b", cir_path]
    result = subprocess.run(cmd, cwd=CIRCUITOS_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] LTspice retorno codigo {result.returncode} para {cir_name}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
    else:
        print(f"[OK] {cir_name} completado.")

    if os.path.exists(log_path):
        shutil.copy2(log_path, dest_log)
    if os.path.exists(raw_path):
        shutil.copy2(raw_path, dest_raw)

    return dest_log, dest_raw

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)

    # 1. Simular retención directa frontera LP
    log_ret, raw_ret = run_simulation("nand3_retencion_lp_frontera_35_37_85C.cir")

    # 2. Simular referencia sin keeper Config B
    log_sens_base_b, raw_sens_base_b = run_simulation("nand3_contencion_lp_sin_keeper_85C_sensB.cir")

    # 3. Simular barrido Config A
    log_sens_a, raw_sens_a = run_simulation("nand3_contencion_lp_sens_configA.cir")

    # 4. Simular barrido Config B
    log_sens_b, raw_sens_b = run_simulation("nand3_contencion_lp_sens_configB.cir")

    # --- PROCESAR RETENCION DIRECTA FRONTERA LP ---
    data_ret = parse_log(log_ret)
    w_ret_list = [35e-9, 36e-9, 37e-9]
    ret_frontera_lp = []
    for idx, w in enumerate(w_ret_list):
        step_idx = idx + 1
        v_start = data_ret["measurements"]["vdyn_start"][idx]["val"]
        v_end = data_ret["measurements"]["vdyn_end_1us"][idx]["val"]
        v_min = data_ret["measurements"]["vdyn_min"][idx]["val"]
        t_cross_meas = data_ret["measurements"].get("t_cross_0p9vdd")
        t_cross = t_cross_meas[idx]["val"] if (t_cross_meas is not None and idx < len(t_cross_meas)) else None
        i_sup = data_ret["measurements"]["isupply_avg"][idx]["val"]
        i_leak_pdn = data_ret["measurements"]["ileak_pdn_avg"][idx]["val"]
        i_kp_inj = data_ret["measurements"]["ikp_inj_avg"][idx]["val"]
        warnings = data_ret.get("warnings", [])

        cumple = bool(v_end is not None and v_end >= 0.990)
        estado_censura = "Censurado (>1.0us)" if t_cross is None else f"Cruzado a {t_cross*1e6:.4f}us"

        ret_frontera_lp.append({
            "id_punto": f"ENS-A3-LP-RET-FRONTERA-85-P{step_idx:02d}",
            "step": step_idx,
            "Wkp_nm": round(w * 1e9, 2),
            "Weff_nm": round((w - 10e-9) * 1e9, 2),
            "Vdyn_start_V": v_start,
            "Vdyn_end_1us_V": v_end,
            "Vdyn_min_V": v_min,
            "t_cross_0p9vdd_s": t_cross,
            "estado_censura": estado_censura,
            "cumple_retencion_0p9": cumple,
            "I_supply_avg_A": i_sup,
            "I_leak_pdn_avg_A": i_leak_pdn,
            "I_kp_inj_avg_A": i_kp_inj,
            "warnings_ltspice": warnings,
            "evidencia": "DIRECTA [ENS-A3-LP-RET-FRONTERA-85]"
        })

    # --- PROCESAR SENSIBILIDAD NUMERICA LP ---
    # Referencia Config A (original de A3.6)
    log_base_a = os.path.join(LOGS_DIR, "nand3_contencion_lp_sin_keeper_85C.log")
    data_base_a = parse_log(log_base_a)
    tphl_base_a = float(data_base_a["measurements"]["tphl_dyn"])
    tplh_base_a = float(data_base_a["measurements"]["tplh_out"])

    # Referencia Config B
    data_base_b = parse_log(log_sens_base_b)
    tphl_base_b = float(data_base_b["measurements"]["tphl_dyn"])
    tplh_base_b = float(data_base_b["measurements"]["tplh_out"])
    trig_base_b = float(data_base_b["measurements"]["t_trig_clk"])
    targ_dyn_base_b = float(data_base_b["measurements"]["t_targ_dyn"])
    targ_out_base_b = float(data_base_b["measurements"]["t_targ_out"])

    # Barrido Config A
    data_sens_a = parse_log(log_sens_a)
    w_sens_list = [34e-9, 35e-9, 36e-9, 37e-9]

    # Barrido Config B
    data_sens_b = parse_log(log_sens_b)

    comparativa_sensibilidad = []
    for idx, w in enumerate(w_sens_list):
        w_nm = round(w * 1e9, 2)
        # Config A
        tp_a = data_sens_a["measurements"]["tphl_dyn"][idx]["val"]
        tplh_a = data_sens_a["measurements"]["tplh_out"][idx]["val"]
        trig_a = data_sens_a["measurements"]["t_trig_clk"][idx]["val"]
        targ_dyn_a = data_sens_a["measurements"]["t_targ_dyn"][idx]["val"]
        targ_out_a = data_sens_a["measurements"]["t_targ_out"][idx]["val"]
        pen_a = 100.0 * (tp_a - tphl_base_a) / tphl_base_a
        cumple_a = bool(pen_a < 10.0)

        # Config B
        tp_b = data_sens_b["measurements"]["tphl_dyn"][idx]["val"]
        tplh_b = data_sens_b["measurements"]["tplh_out"][idx]["val"]
        trig_b = data_sens_b["measurements"]["t_trig_clk"][idx]["val"]
        targ_dyn_b = data_sens_b["measurements"]["t_targ_dyn"][idx]["val"]
        targ_out_b = data_sens_b["measurements"]["t_targ_out"][idx]["val"]
        pen_b = 100.0 * (tp_b - tphl_base_b) / tphl_base_b
        cumple_b = bool(pen_b < 10.0)

        diff_tphl_ps = (tp_b - tp_a) * 1e12
        diff_pen_pct = pen_b - pen_a
        cambio_clasificacion = (cumple_a != cumple_b)

        comparativa_sensibilidad.append({
            "Wkp_nm": w_nm,
            "Weff_nm": round((w - 10e-9) * 1e9, 2),
            "r": round(w / 67.5e-9, 4),
            "config_A": {
                "tphl_dyn_ps": round(tp_a * 1e12, 4),
                "tplh_out_ps": round(tplh_a * 1e12, 4),
                "trig_clk_ns": round(trig_a * 1e9, 6),
                "targ_dyn_ns": round(targ_dyn_a * 1e9, 6),
                "targ_out_ns": round(targ_out_a * 1e9, 6),
                "penalizacion_pct": round(pen_a, 4),
                "cumple_menor_10pct": cumple_a
            },
            "config_B": {
                "tphl_dyn_ps": round(tp_b * 1e12, 4),
                "tplh_out_ps": round(tplh_b * 1e12, 4),
                "trig_clk_ns": round(trig_b * 1e9, 6),
                "targ_dyn_ns": round(targ_dyn_b * 1e9, 6),
                "targ_out_ns": round(targ_out_b * 1e9, 6),
                "penalizacion_pct": round(pen_b, 4),
                "cumple_menor_10pct": cumple_b
            },
            "diff_tphl_ps": round(diff_tphl_ps, 4),
            "diff_penalizacion_pct": round(diff_pen_pct, 4),
            "cambio_clasificacion": cambio_clasificacion
        })

    # Cargar y actualizar act3_contencion_lp_metricas.json
    json_path = os.path.join(DATOS_DIR, "act3_contencion_lp_metricas.json")
    with open(json_path, "r", encoding="utf-8") as f:
        datos_lp = json.load(f)

    # Actualizar cruce de viabilidad conjunta con la retención directa de 35, 36, 37 nm
    # y asegurar separación de categorías
    cruce_actualizado = []
    # 1. Sin keeper (Mk ausente)
    cruce_actualizado.append({
        "categoria": "SIN_KEEPER (Mk ausente)",
        "Wkp_nm": 0.0,
        "r": 0.0,
        "Vdyn_end_V": 1.1256994009,
        "retencion_status": "1.1257 V",
        "evidencia_retencion": "DIRECTA [ENS-A3-LP-RET-03]",
        "retencion_ok": True,
        "penalizacion_pct": 0.0,
        "evidencia_contencion": "DIRECTA [ENS-A3-LP-CONT-01]",
        "contencion_ok": True,
        "viabilidad": "VIABLE (Sin contencion)",
        "nota": "Fuga PDN = 3.40 pA; retiene sin keeper en 1.0 us"
    })

    # 2. Puntos con keeper simulados
    puntos_coarse = [10.5, 15.0, 30.0, 35.0, 36.0, 37.0, 45.0, 60.0, 90.0, 135.0, 180.0]
    for w_nm in puntos_coarse:
        r = round(w_nm / 67.5, 4)
        # Buscar en retención
        p_ret_dir = next((p for p in ret_frontera_lp if abs(p["Wkp_nm"] - w_nm) < 0.1), None)
        if p_ret_dir:
            v_end = p_ret_dir["Vdyn_end_1us_V"]
            ret_ev = p_ret_dir["evidencia"]
            ret_ok = p_ret_dir["cumple_retencion_0p9"]
            ret_st = f"{v_end:.5f} V"
        elif abs(w_nm - 10.5) < 0.1:
            v_end = None
            ret_ev = "NO EVALUADO DIRECTAMENTE"
            ret_ok = False
            ret_st = "No evaluado"
        else:
            # Buscar en barrido grueso LP de A3.3
            ret_lp_path = os.path.join(DATOS_DIR, "act3_retencion_lp_metricas.json")
            with open(ret_lp_path, "r", encoding="utf-8") as f_ret:
                datos_ret_a33 = json.load(f_ret)
            p_coarse_ret = next((p for p in datos_ret_a33["barrido_con_keeper_85C"]["puntos"] if abs(p["Wkp_nm"] - w_nm) < 0.1), None)
            if p_coarse_ret:
                v_end = p_coarse_ret["Vdyn_end_1us_V"]
                ret_ev = "DIRECTA [A3.3 (ENS-A3-LP-RET-04)]"
                ret_ok = bool(v_end >= 0.990)
                ret_st = f"{v_end:.5f} V"
            else:
                v_end = None
                ret_ev = "NO EVALUADO"
                ret_ok = False
                ret_st = "No evaluado"

        # Buscar en contención
        p_cont_ref = next((p for p in datos_lp["refinamiento_frontera_1nm"] if abs(p["Wkp_nm"] - w_nm) < 0.1), None)
        if p_cont_ref:
            pen = p_cont_ref["penalizacion_pct"]
            cont_ok = p_cont_ref["cumple_contencion_menor_10pct"]
            cont_ev = "DIRECTA [A3.6 (Refin)]"
        else:
            p_cont_c = next((p for p in datos_lp["barrido_grueso"] if abs(p["Wkp_nm"] - w_nm) < 0.1), None)
            pen = p_cont_c["penalizacion_pct"] if p_cont_c else None
            cont_ok = p_cont_c["cumple_contencion_menor_10pct"] if p_cont_c else False
            cont_ev = "DIRECTA [A3.6 (Coarse)]" if p_cont_c else "NO EVALUADO"

        if ret_ok and cont_ok:
            viab = "VIABLE"
        elif not cont_ok and pen is not None:
            viab = "FALLA CONTENCION"
        elif pen is None:
            viab = "FALLA SIN CONMUTACION"
        else:
            viab = "INVIABLE"

        cruce_actualizado.append({
            "categoria": "CON_KEEPER (Weff > 0)",
            "Wkp_nm": w_nm,
            "Weff_nm": round(w_nm - 10.0, 2),
            "r": r,
            "Vdyn_end_V": v_end,
            "retencion_status": ret_st,
            "evidencia_retencion": ret_ev,
            "retencion_ok": ret_ok,
            "penalizacion_pct": pen,
            "evidencia_contencion": cont_ev,
            "contencion_ok": cont_ok,
            "viabilidad": viab
        })

    datos_lp["retencion_directa_frontera_85C"] = ret_frontera_lp
    datos_lp["estudio_sensibilidad_solver"] = {
        "config_A_original": {
            "opciones": "gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear",
            "tstep_max": "2ps",
            "tphl_sin_keeper_ps": round(tphl_base_a * 1e12, 4),
            "tplh_sin_keeper_ps": round(tplh_base_a * 1e12, 4)
        },
        "config_B_exigente": {
            "opciones": "gmin=1e-15 abstol=1e-15 reltol=1e-5 method=gear",
            "tstep_max": "0.5ps",
            "tphl_sin_keeper_ps": round(tphl_base_b * 1e12, 4),
            "tplh_sin_keeper_ps": round(tplh_base_b * 1e12, 4),
            "trig_clk_ns": round(trig_base_b * 1e9, 6),
            "targ_dyn_ns": round(targ_dyn_base_b * 1e9, 6),
            "targ_out_ns": round(targ_out_base_b * 1e9, 6)
        },
        "comparativa_puntos": comparativa_sensibilidad
    }
    datos_lp["cruce_viabilidad_conjunta"] = cruce_actualizado

    # Corregir aclaraciones de PDN y delimitaciones
    datos_lp["condiciones"]["W_PDN_eq_nm"] = 67.5
    datos_lp["condiciones"]["descripcion_PDN"] = "4 NMOS en serie (M1, M2, M3, Mf) de W=270nm. W_PDN_eq approx 270nm/4 = 67.5nm (aproximacion resistiva de primer orden)"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(datos_lp, f, indent=2)
    print(f"[CONSOLIDADO] JSON actualizado exitosamente en: {json_path}")

    print("\n" + "="*70)
    print("RESULTADOS DE SENSIBILIDAD NUMERICA LP @ 85C:")
    print("="*70)
    print(f"Base Sin Keeper: Config A = {tphl_base_a*1e12:.3f} ps | Config B = {tphl_base_b*1e12:.3f} ps (diff = {(tphl_base_b-tphl_base_a)*1e12:.4f} ps)")
    for p in comparativa_sensibilidad:
        print(f"Wkp = {p['Wkp_nm']:4.1f} nm | Pen A = {p['config_A']['penalizacion_pct']:6.3f}% ({'PASS' if p['config_A']['cumple_menor_10pct'] else 'FAIL'}) | Pen B = {p['config_B']['penalizacion_pct']:6.3f}% ({'PASS' if p['config_B']['cumple_menor_10pct'] else 'FAIL'}) | dPen = {p['diff_penalizacion_pct']:+6.3f}% | Cambio = {p['cambio_clasificacion']}")

    print("\n" + "="*70)
    print("RESULTADOS DE RETENCION DIRECTA FRONTERA LP @ 85C:")
    print("="*70)
    for p in ret_frontera_lp:
        print(f"{p['id_punto']}: Wkp = {p['Wkp_nm']} nm | Vdyn_end = {p['Vdyn_end_1us_V']:.6f} V | Cumple = {p['cumple_retencion_0p9']} | Censura = {p['estado_censura']}")

if __name__ == "__main__":
    main()
