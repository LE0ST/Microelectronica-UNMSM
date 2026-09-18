# -*- coding: utf-8 -*-
"""
Orquestador de Simulaciones - Actividad 2 (LD2)
Ejecuta los circuitos en LTspice en modo batch, organiza las salidas (.log y .raw),
parsea las métricas con el parser certificado y exporta los datos cuantitativos
a resultados/datos/act2_metricas.json.
"""

import os
import sys
import shutil
import subprocess
import json

# Rutas base
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"
ACT2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIRCUITOS_DIR = os.path.join(ACT2_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT2_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT2_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT2_DIR, "resultados", "datos")

# Importar parser certificado de logs
SCRIPTS_DIR = os.path.join(os.path.dirname(ACT2_DIR), "scripts", "lectura_resultados")
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log

CIRCUITOS = [
    "nand3_cs_peor_caso_oficial.cir",
    "nand3_cs_peor_caso_fisico.cir",
    "nand3_cs_barrido_cl.cir",
    "nand3_cs_mitigacion_precarga.cir",
    "nand3_cs_mitigacion_reordenamiento.cir",
    "nand3_cs_mitigacion_keeper.cir",
    "nand3_cs_contencion_sin_keeper.cir",
    "nand3_cs_contencion_con_keeper.cir"
]

def main():
    if not os.path.exists(LTSPICE_EXE):
        print(f"ERROR: No se encontro el ejecutable de LTspice en: {LTSPICE_EXE}")
        sys.exit(1)

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATOS_DIR, exist_ok=True)

    print("==================================================================")
    print("INICIANDO SIMULACIONES DE PRODUCCION - ACTIVIDAD 2 (LD2)")
    print(f"Ejecutable LTspice: {LTSPICE_EXE}")
    print(f"Directorio de Circuitos: {CIRCUITOS_DIR}")
    print("==================================================================")

    exitos = 0
    metricas_consolidadas = {}

    for cir_file in CIRCUITOS:
        cir_path = os.path.join(CIRCUITOS_DIR, cir_file)
        if not os.path.exists(cir_path):
            print(f"[ERROR] Archivo no encontrado: {cir_path}")
            continue

        base_name = os.path.splitext(cir_file)[0]
        print(f"\n-> Simulando: {cir_file} ...")
        cmd = [LTSPICE_EXE, "-b", cir_path]
        res = subprocess.run(cmd, capture_output=True, text=True)

        if res.returncode != 0:
            print(f"   [FALLO] Codigo de retorno: {res.returncode}")
            print(f"   Stderr: {res.stderr}")
            continue

        src_log = os.path.join(CIRCUITOS_DIR, base_name + ".log")
        src_raw = os.path.join(CIRCUITOS_DIR, base_name + ".raw")
        src_op_raw = os.path.join(CIRCUITOS_DIR, base_name + ".op.raw")
        src_log_raw = os.path.join(CIRCUITOS_DIR, base_name + ".log.raw")

        dst_log = os.path.join(LOGS_DIR, base_name + ".log")
        dst_raw = os.path.join(RAW_DIR, base_name + ".raw")

        if os.path.exists(src_log):
            shutil.copy2(src_log, dst_log)
            print(f"   Log copiado a: {dst_log}")

        if os.path.exists(src_raw):
            shutil.copy2(src_raw, dst_raw)
            print(f"   Raw copiado a: {dst_raw}")

        # Limpiar temporales y duplicados en el directorio de circuitos
        src_db = os.path.join(CIRCUITOS_DIR, base_name + ".db")
        for tmp_f in [src_log, src_raw, src_op_raw, src_log_raw, src_db]:
            if os.path.exists(tmp_f):
                os.remove(tmp_f)

        # Parsear log
        try:
            parsed = parse_log(dst_log, raise_on_error=True)
            metricas_consolidadas[base_name] = {
                "measurements": parsed["measurements"],
                "steps": parsed["steps"],
                "elapsed_time": parsed["elapsed_time"],
                "is_valid": parsed["is_valid"]
            }
            exitos += 1
            print(f"   [OK] Parseo exitoso sin advertencias ni NaN.")
        except Exception as e:
            print(f"   [ERROR AL PARSEAR] {e}")

    # Guardar métricas en JSON
    json_path = os.path.join(DATOS_DIR, "act2_metricas.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metricas_consolidadas, f, indent=4)
    print(f"\n[OK] Metricas cuantitativas guardadas en: {json_path}")

    print("\n==================================================================")
    print(f"RESUMEN: {exitos}/{len(CIRCUITOS)} circuitos simulados y parseados exitosamente.")
    print("==================================================================")

if __name__ == '__main__':
    main()
