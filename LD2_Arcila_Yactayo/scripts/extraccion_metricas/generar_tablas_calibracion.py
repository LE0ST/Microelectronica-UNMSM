# -*- coding: utf-8 -*-
"""
Generador de tablas de calibración para la Fase 2 (LD2)
Lee los resultados estructurados en JSON/CSV generados por los extractores
y produce tablas formateadas en Markdown y LaTeX.
"""

import os
import sys
import json
import csv

def generar_tablas():
    base_dir = r"G:\Proyectos\MicroNano\LD2_Arcila_Yactayo"
    
    # 1. Tabla de caracterización del inversor
    inv_json = os.path.join(base_dir, "auxiliares", "caracterizacion_inversor", "caracterizacion_inversor_resultados.json")
    if os.path.exists(inv_json):
        with open(inv_json, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
            
        print("### Tabla 1: Caracterización del Inversor de Referencia (LD2)")
        print("| Proceso / Temp | $V_{DD}$ (V) | $V_M$ (V) | $V_{IL}$ (V) | $V_{IH}$ (V) | $NM_L$ (V) | $NM_H$ (V) | Ganancia Máx |")
        print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        for r in inv_data:
            tag = r['tag']
            vdd = "1.0" if "45hp" in tag else ("1.1" if "45lp" in tag else "1.3")
            print(f"| {tag:<14} | {vdd:<12} | {r['VM']:<9.4f} | {r['VIL']:<12.4f} | {r['VIH']:<12.4f} | {r['NML']:<10.4f} | {r['NMH']:<10.4f} | {r['gain_max']:<12.2f} |")
        print("\n")

    # 2. Tabla del experimento gmin
    gmin_json = os.path.join(base_dir, "auxiliares", "experimento_gmin", "experimento_gmin_resultados.json")
    if os.path.exists(gmin_json):
        with open(gmin_json, "r", encoding="utf-8") as f:
            gmin_data = json.load(f)
        print("### Tabla 2: Experimento de Sensibilidad Numérica de gmin (45nm LP a 27 °C)")
        print("| Métrica Evaluada | gmin = 1e-12 (Default) | gmin = 1e-15 (LD2) | $\\Delta$ Absoluto | Impacto Relativo |")
        print("| :--- | :---: | :---: | :---: | :---: |")
        r12 = gmin_data['gmin_1e12']
        r15 = gmin_data['gmin_1e15']
        
        dv12 = r12['dv_leak'] * 1e3
        dv15 = r15['dv_leak'] * 1e3
        ddv = abs(dv12 - dv15)
        pct_dv = (ddv / dv15) * 100
        
        i12 = r12['ileak_avg'] * 1e12
        i15 = r15['ileak_avg'] * 1e12
        di = abs(i12 - i15)
        pct_i = (di / i15) * 100
        
        print(f"| Tensión inicial $V(dyn)$ | {r12['vdyn_start']:.6f} V | {r15['vdyn_start']:.6f} V | {abs(r12['vdyn_start']-r15['vdyn_start']):.2e} V | 0.00 % |")
        print(f"| Tensión final ($1\\,\\mu$s) | {r12['vdyn_end']:.6f} V | {r15['vdyn_end']:.6f} V | {abs(r12['vdyn_end']-r15['vdyn_end']):.2e} V | {abs(r12['vdyn_end']-r15['vdyn_end'])/r15['vdyn_end']*100:.2f} % |")
        print(f"| Caída $\\Delta V$ en retención | {dv12:.4f} mV | {dv15:.4f} mV | {ddv:.4f} mV | +{pct_dv:.2f} % |")
        print(f"| Corriente media suministrada por $V_{{DD}}$ en retención | {i12:.4f} pA | {i15:.4f} pA | {di:.4f} pA | **+{pct_i:.2f} %** |")
        print("\n")

if __name__ == '__main__':
    generar_tablas()
