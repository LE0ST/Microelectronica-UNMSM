# -*- coding: utf-8 -*-
"""
Orquestador de Simulaciones - Actividad 1 (LD2)
Ejecuta los circuitos en LTspice 26.0.2 en modo batch y organiza
las salidas (.log y .raw) en resultados/logs/ y resultados/raw/.
"""

import os
import sys
import shutil
import subprocess

LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

ACT1_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIRCUITOS_DIR = os.path.join(ACT1_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT1_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT1_DIR, "resultados", "raw")

CIRCUITOS = [
    "nand3_dinamica_base.cir",
    "nand3_estatica_base.cir",
    "nand3_estatica_mismo_estimulo.cir",
    "nand3_control_retardo_equivalente.cir",
    "nand3_dinamica_fijas1.cir",
    "nand3_estatica_fijas1.cir",
    "nand3_extraccion_cin.cir",
    "nand3_dinamica_pdn_abierta_tclk2n.cir",
    "nand3_dinamica_pdn_abierta_tclk400n.cir",
]

def main():
    if not os.path.exists(LTSPICE_EXE):
        print(f"ERROR: No se encontro el ejecutable de LTspice en: {LTSPICE_EXE}")
        sys.exit(1)

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)

    print("==================================================================")
    print("INICIANDO SIMULACIONES DE PRODUCCION - ACTIVIDAD 1 (LD2)")
    print(f"Ejecutable LTspice: {LTSPICE_EXE}")
    print(f"Directorio de Circuitos: {CIRCUITOS_DIR}")
    print("==================================================================")

    exitos = 0
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

        # LTspice genera los archivos en el mismo directorio del .cir
        src_log = os.path.join(CIRCUITOS_DIR, base_name + ".log")
        src_raw = os.path.join(CIRCUITOS_DIR, base_name + ".raw")
        src_op_raw = os.path.join(CIRCUITOS_DIR, base_name + ".op.raw")

        dst_log = os.path.join(LOGS_DIR, base_name + ".log")
        dst_raw = os.path.join(RAW_DIR, base_name + ".raw")

        if os.path.exists(src_log):
            shutil.copy2(src_log, dst_log)
            print(f"   Log copiado a: {dst_log}")

        if os.path.exists(src_raw):
            shutil.copy2(src_raw, dst_raw)
            print(f"   Raw copiado a: {dst_raw}")

        # Limpiar archivo temporal op.raw si existe
        if os.path.exists(src_op_raw):
            os.remove(src_op_raw)

        exitos += 1
        print(f"   [OK] {cir_file} completado con exito.")

    print("\n==================================================================")
    print(f"RESUMEN: {exitos}/{len(CIRCUITOS)} circuitos simulados exitosamente.")
    print("==================================================================")

if __name__ == '__main__':
    main()
