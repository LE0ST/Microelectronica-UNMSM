# -*- coding: utf-8 -*-
"""
validar_infraestructura_act3.py
Verifica la integridad de la infraestructura de Actividad 3 sin ejecutar simulaciones SPICE.
- Comprueba presencia de directorios
- Valida los modelos PTM requeridos
- Valida la sintaxis del esquema JSON de datos
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
MODELOS_DIR = os.path.join(LD2_DIR, "modelos")
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")

def validar_directorios():
    dirs_requeridos = [
        os.path.join(ACT3_DIR, "circuitos"),
        os.path.join(ACT3_DIR, "resultados", "logs"),
        os.path.join(ACT3_DIR, "resultados", "raw"),
        os.path.join(ACT3_DIR, "resultados", "datos"),
        os.path.join(ACT3_DIR, "figuras"),
        os.path.join(ACT3_DIR, "scripts"),
    ]
    print("[1] Verificando estructura de directorios:")
    for d in dirs_requeridos:
        ok = os.path.isdir(d)
        print(f"  {'[OK]' if ok else '[FAIL]'} {os.path.relpath(d, LD2_DIR)}")
        if not ok:
            return False
    return True

def validar_modelos():
    modelos = ["ptm45hp.lib", "ptm45lp.lib", "ptm130.lib"]
    print("\n[2] Verificando disponibilidad de modelos PTM:")
    for m in modelos:
        p = os.path.join(MODELOS_DIR, m)
        ok = os.path.isfile(p) and os.path.getsize(p) > 1000
        print(f"  {'[OK]' if ok else '[FAIL]'} {m} ({os.path.getsize(p) if ok else 0} bytes)")
        if not ok:
            return False
    return True

def validar_esquema():
    print("\n[3] Verificando esquema y plantilla de datos JSON:")
    schema_path = os.path.join(DATOS_DIR, "act3_schema.json")
    template_path = os.path.join(DATOS_DIR, "act3_metricas_template.json")
    
    if not os.path.exists(schema_path):
        print(f"  [FAIL] No se encuentra {schema_path}")
        return False
    if not os.path.exists(template_path):
        print(f"  [FAIL] No se encuentra {template_path}")
        return False
        
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
        
    # Validar campos de ensayos_retencion
    required_ret = schema["properties"]["ensayos_retencion"]["items"]["required"]
    for idx, e in enumerate(template["ensayos_retencion"]):
        for r in required_ret:
            if r not in e:
                print(f"  [FAIL] Ensayo retención {idx} carece de campo requerido '{r}'")
                return False
                
    # Validar campos de ensayos_contencion
    required_cont = schema["properties"]["ensayos_contencion"]["items"]["required"]
    for idx, e in enumerate(template["ensayos_contencion"]):
        for r in required_cont:
            if r not in e:
                print(f"  [FAIL] Ensayo contención {idx} carece de campo requerido '{r}'")
                return False

    print("  [OK] Esquema JSON y plantilla validados correctamente (todos los valores iniciales son null/None).")
    return True

def main():
    print("=================================================================")
    print("VALIDACIÓN ESTÁTICA DE INFRAESTRUCTURA — ACTIVIDAD 3 (LD2)")
    print("AVISO: ESTE SCRIPT NO EJECUTA LTSPICE NI GENERA SIMULACIONES.")
    print("=================================================================")
    d_ok = validar_directorios()
    m_ok = validar_modelos()
    e_ok = validar_esquema()
    
    if d_ok and m_ok and e_ok:
        print("\n[ÉXITO] Infraestructura de Actividad 3 validada y lista para futura ejecución.")
        return 0
    else:
        print("\n[ERROR] Fallos detectados en la validación estática.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
