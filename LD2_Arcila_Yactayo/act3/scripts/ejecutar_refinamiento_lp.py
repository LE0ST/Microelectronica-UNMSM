# -*- coding: utf-8 -*-
"""
ejecutar_refinamiento_lp.py
Ejecuta el refinamiento de contención en 45nm LP @ 85°C (30nm a 45nm)
de manera aislada, robusta y con diagnóstico completo.
"""

import os
import sys
import time
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

SCRIPTS_DIR = os.path.join(LD2_DIR, "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log

def main():
    cir_name = "nand3_contencion_lp_refinamiento_85C.cir"
    cir_path = os.path.join(CIRCUITOS_DIR, cir_name)
    base_name = os.path.splitext(cir_name)[0]
    log_path = os.path.join(CIRCUITOS_DIR, base_name + ".log")
    raw_path = os.path.join(CIRCUITOS_DIR, base_name + ".raw")

    print(f"==================================================================")
    print(f"DIAGNOSTICO PREVIO:")
    print(f"  LTspice ejecutable: {LTSPICE_EXE} (Existe: {os.path.exists(LTSPICE_EXE)})")
    print(f"  Netlist objetivo:   {cir_path} (Existe: {os.path.exists(cir_path)})")
    print(f"  CWD de ejecucion:   {CIRCUITOS_DIR}")
    print(f"==================================================================")

    if not os.path.exists(LTSPICE_EXE):
        print(f"[ERROR] No se encuentra LTspice en {LTSPICE_EXE}")
        sys.exit(1)

    if not os.path.exists(cir_path):
        print(f"[ERROR] No se encuentra el netlist en {cir_path}")
        sys.exit(1)

    # Eliminar logs/raws previos en circuitos para garantizar frescura
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(raw_path):
        os.remove(raw_path)

    cmd = [LTSPICE_EXE, "-b", cir_path]
    print(f"[EJECUTANDO] {' '.join(cmd)} ...")
    t0 = time.time()
    try:
        res = subprocess.run(cmd, cwd=CIRCUITOS_DIR, capture_output=True, text=True, timeout=60)
        elapsed = time.time() - t0
        print(f"[FIN EJECUCION]")
        print(f"  Returncode: {res.returncode}")
        print(f"  Tiempo transcurrido: {elapsed:.2f} s")
        print(f"  Stdout: {res.stdout.strip() if res.stdout else '(vacio)'}")
        print(f"  Stderr: {res.stderr.strip() if res.stderr else '(vacio)'}")
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Tiempo de espera agotado (timeout > 60s)")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Excepcion al ejecutar subprocess: {e}")
        sys.exit(1)

    if res.returncode != 0:
        print(f"[ERROR] LTspice finalizo con error {res.returncode}")
        sys.exit(1)

    if not os.path.exists(log_path):
        print(f"[ERROR] No se genero el archivo LOG en {log_path}")
        sys.exit(1)

    print(f"[OK] Archivo LOG generado: {log_path} ({os.path.getsize(log_path)} bytes)")
    if os.path.exists(raw_path):
        print(f"[OK] Archivo RAW generado: {raw_path} ({os.path.getsize(raw_path)} bytes)")
        shutil.copy2(raw_path, os.path.join(RAW_DIR, base_name + ".raw"))
    shutil.copy2(log_path, os.path.join(LOGS_DIR, base_name + ".log"))

    # Parsear resultados
    print(f"\n[PARSERS] Extrayendo mediciones con parse_spice_log...")
    data = parse_log(log_path)
    
    tphl_sin_lp = 1.05751507681e-10  # Obtenido en ENS-A3-LP-CONT-01
    
    meas_tphl = data["measurements"].get("tphl_dyn")
    if not meas_tphl or not isinstance(meas_tphl, list):
        print(f"[ERROR] Medicion tphl_dyn no es una lista valida en el log: {meas_tphl}")
        sys.exit(1)

    num_pasos = len(meas_tphl)
    print(f"[OK] Pasos detectados en el log: {num_pasos}/16")
    if num_pasos != 16:
        print(f"[WARNING] Se esperaban 16 pasos, se encontraron {num_pasos}")

    w_list = [30 + i for i in range(num_pasos)]
    
    print("\n" + "="*80)
    print("REFINAMIENTO DE CONTENCION EN VELOCIDAD — 45nm LP @ 85°C (VDD = 1.1 V)")
    print(f"Base Sin Keeper LP: tpHL,dyn,sin = {tphl_sin_lp*1e12:.3f} ps")
    print("="*80)
    print(f"{'Wkp (nm)':>8} | {'Weff (nm)':>9} | {'r':>7} | {'tpHL (ps)':>10} | {'Penal (%)':>10} | {'< 10.0%?':>9} | {'Estado':>12}")
    print("-"*80)
    
    resultados_ref_lp = []
    w_max_lp = None
    r_max_lp = None

    for idx, (w, e) in enumerate(zip(w_list, meas_tphl)):
        tp = e["val"] if isinstance(e, dict) else e
        weff = w - 10.0
        r = (w * 1e-9) / 67.5e-9
        if tp is not None:
            pen = 100.0 * (tp - tphl_sin_lp) / tphl_sin_lp
            cumple = pen < 10.0
            estado = "PASS" if cumple else "FAIL_PENALIZACION"
            if cumple:
                w_max_lp = w
                r_max_lp = r
            print(f"{w:8.1f} | {weff:9.1f} | {r:7.3f} | {tp*1e12:10.3f} | {pen:9.2f}% | {'SI' if cumple else 'NO':>9} | {estado:>12}")
        else:
            pen = None
            cumple = False
            estado = "FAIL_SIN_CONMUTACION_POR_CONTENCION"
            print(f"{w:8.1f} | {weff:9.1f} | {r:7.3f} | {'null':>10} | {'null':>10} | {'NO':>9} | {estado:>12}")

        resultados_ref_lp.append({
            "step": idx + 1,
            "Wkp_nm": float(w),
            "Weff_nm": float(weff),
            "r": round(r, 4),
            "tphl_dyn_s": tp,
            "tphl_dyn_ps": round(tp * 1e12, 3) if tp else None,
            "penalizacion_pct": round(pen, 2) if pen is not None else None,
            "cumple_contencion_menor_10pct": cumple,
            "estado": estado
        })

    print("="*80)
    print(f"FRONTERA MAXIMA DERIVADA EN 45nm LP @ 85°C:")
    print(f"  Wkp_max_lp = {w_max_lp} nm")
    print(f"  r_max_lp   = {r_max_lp:.4f}")
    print("="*80)

if __name__ == "__main__":
    main()
