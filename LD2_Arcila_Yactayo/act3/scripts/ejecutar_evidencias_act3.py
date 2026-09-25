# -*- coding: utf-8 -*-
"""
ejecutar_evidencias_act3.py
Ejecuta los ensayos de fallo Wkp=1nm en 27C y 85C,
organiza los logs y raw del refinamiento en act3/resultados/logs y act3/resultados/raw.
"""

import os
import subprocess
import shutil

ACT3_DIR = r"G:\Proyectos\MicroNano\LD2_Arcila_Yactayo\act3"
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LOGS_DIR = os.path.join(ACT3_DIR, "resultados", "logs")
RAW_DIR = os.path.join(ACT3_DIR, "resultados", "raw")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"

# 1. Ejecutar fallos Wkp=1nm
fallos = [
    ("nand3_retencion_wkp_1nm_fallo_27C.cir", "nand3_retencion_wkp_1nm_fallo_27C.log"),
    ("nand3_retencion_wkp_1nm_fallo_85C.cir", "nand3_retencion_wkp_1nm_fallo_85C.log")
]

for cir_f, log_f in fallos:
    cir_path = os.path.join(CIRCUITOS_DIR, cir_f)
    print(f"Ejecutando fallo esperado en: {cir_path}")
    res = subprocess.run([LTSPICE_EXE, "-b", cir_path], capture_output=True, text=True)
    print(f"  Codigo de salida (esperado != 0): {res.returncode}")
    src_log = os.path.join(CIRCUITOS_DIR, log_f)
    dst_log = os.path.join(LOGS_DIR, log_f)
    if os.path.exists(src_log):
        shutil.copy2(src_log, dst_log)
        print(f"  Log copiado a: {dst_log}")

# 2. Copiar refinamiento a resultados/logs y resultados/raw
ref_base = "nand3_retencion_refinamiento_85C"
src_ref_log = os.path.join(CIRCUITOS_DIR, ref_base + ".log")
dst_ref_log = os.path.join(LOGS_DIR, ref_base + ".log")
src_ref_raw = os.path.join(CIRCUITOS_DIR, ref_base + ".raw")
dst_ref_raw = os.path.join(RAW_DIR, ref_base + ".raw")

if os.path.exists(src_ref_log):
    shutil.copy2(src_ref_log, dst_ref_log)
    print(f"Refinamiento log copiado a: {dst_ref_log}")

if os.path.exists(src_ref_raw):
    shutil.copy2(src_ref_raw, dst_ref_raw)
    print(f"Refinamiento raw copiado a: {dst_ref_raw}")

print("\nOrganización completada.")
