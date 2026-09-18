# -*- coding: utf-8 -*-
"""
Actualiza registro_ensayos.csv con los ensayos formales de Actividad 2 (ENS-A2-01 a ENS-A2-07).
"""

import os

CSV_PATH = os.path.abspath("LD2_Arcila_Yactayo/documentacion/registro_ensayos.csv")

NEW_ROWS = [
    'ENS-A2-01,Actividad 2 - Peor Caso Oficial (Guía Sec. 6.3),act2/circuitos/nand3_cs_peor_caso_oficial.cir,act2/resultados/logs/nand3_cs_peor_caso_oficial.log,45nm_HP,27,1.0,"Wn=90n, Wp=135n, W_pdn=270n, CL=2f, Cout=1f, Tclk=2n, Ad=2.43e-14, Pd=4.5e-7","Vdyn_min=0.9998V, dV=0.158mV, Vdyn_eval_min=-0.0190V, Vout_end=1.83uV, Vn1_end=0.6825V, Vn2_end=0.6529V, Vn3_end=-0.0603V",PASS,2026-09-17,"Corrida oficial requerida por Sec. 6.3; at=1.95*Tclk cae en precarga de ciclo 2 (CLK=0); A y B activos en precarga precargan n1 y n2 a 0.68V/0.65V"',
    'ENS-A2-02,Actividad 2 - Benchmark Físico Charge Sharing,act2/circuitos/nand3_cs_peor_caso_fisico.cir,act2/resultados/logs/nand3_cs_peor_caso_fisico.log,45nm_HP,27,1.0,"Wn=90n, Wp=135n, W_pdn=270n, CL=2f, Cout=1f, Tclk=2n, n1_0=0V, n2_0=0V","Vdyn_min=0.9003V, dV=99.66mV, Vdyn_eval_min=0.8990V, dV_eval=101.03mV, Vout_max=0.149mV, Vn1=0.6799V, Vn2=0.6596V, Vn3=1.37uV",PASS,2026-09-17,"Benchmark físico con aislamiento previo de n1 y n2 en 0V; corte subumbral de M2 limita dV a 101mV evitando falla lógica"',
    'ENS-A2-03,Actividad 2 - Barrido Paramétrico CL,act2/circuitos/nand3_cs_barrido_cl.cir,act2/resultados/logs/nand3_cs_barrido_cl.log,45nm_HP,27,1.0,"CL list 0.5f 1f 2f 4f, W_pdn=270n, Ln=45n","CL=0.5f: dV=175.92mV, Vdyn_min=0.8241V; CL=1f: dV=138.26mV, Vdyn_min=0.8617V; CL=2f: dV=101.03mV, Vdyn_min=0.8990V; CL=4f: dV=67.62mV, Vdyn_min=0.9324V",PASS,2026-09-17,"Barrido paramétrico 4 puntos; Vdyn,min > VIH (0.579V) en todo el rango; Vout_max <= 0.68mV; cero fallos lógicos"',
    'ENS-A2-04,Actividad 2 - Mitigación 1 Precarga Interna,act2/circuitos/nand3_cs_mitigacion_precarga.cir,act2/resultados/logs/nand3_cs_mitigacion_precarga.log,45nm_HP,27,1.0,"2 PMOS extra Wp=135n en n1 y n2 gobernados por CLK, CL=2f","Vdyn_min=1.0290V, dV=-29.04mV, Vdyn_eval_min=1.0120V, dV_eval=-12.05mV, Vout_max=0.267mV, Vn1=1.069V, Vn2=1.062V",PASS,2026-09-17,"Eliminación total del charge sharing (dV<=0); coste: +2 PMOS y +0.34fF gate en CLK (+67%); n3 no se precarga para evitar cortocircuito con footer"',
    'ENS-A2-05,Actividad 2 - Mitigación 2 Reordenamiento PDN,act2/circuitos/nand3_cs_mitigacion_reordenamiento.cir,act2/resultados/logs/nand3_cs_mitigacion_reordenamiento.log,45nm_HP,27,1.0,"Entrada crítica C en tope de la PDN junto a dyn; M1(A) y M2(B) inferiores","Vdyn_min=1.0222V, dV=-22.17mV, Vdyn_eval_min=0.99999V, dV_eval=0.014mV (14uV), Vout_max=0.294mV, Vn1=15.7uV, Vn2=10.5uV",PASS,2026-09-17,"C=0 en tope aísla n1 y n2 de dyn; redistribución suprimida sin coste de área ni capacitancia extra de reloj"',
    'ENS-A2-06,Actividad 2 - Mitigación 3 Keeper Wkp=45n,act2/circuitos/nand3_cs_mitigacion_keeper.cir,act2/resultados/logs/nand3_cs_mitigacion_keeper.log,45nm_HP,27,1.0,"Keeper PMOS Wkp=45n (L=45n) realimentado desde out, CL=2f","Vdyn_min=0.9996V, dV=0.43mV, Vdyn_eval_min=0.9578V, dV_eval=42.18mV, t_restore=80.30ps, Vout_max=0.384mV",PASS,2026-09-17,"Keeper restaura activamente dyn a 0.99*VDD en 80.3ps; reduce caída máxima de 101.0mV a 42.2mV (-58.2%)"',
    'ENS-A2-07,Actividad 2 - Contención del Keeper,act2/circuitos/nand3_cs_contencion_sin_keeper.cir y nand3_cs_contencion_con_keeper.cir,act2/resultados/logs/nand3_cs_contencion_sin_keeper.log y nand3_cs_contencion_con_keeper.log,45nm_HP,27,1.0,"A=B=C=1 (evaluación a 0), Wkp=45n vs sin keeper","tpHL_dyn_sin=23.95ps, tpHL_dyn_con=27.46ps (+14.65%), tpLH_out_sin=37.58ps, tpLH_out_con=43.09ps (+14.69%)",PASS,2026-09-17,"Cuantificación rigurosa del coste de contención: penalización de +3.51ps (+14.7%) en retardo de evaluación"'
]

def main():
    # Leer contenido actual
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar si ya existen los IDs para evitar duplicación
    for row in NEW_ROWS:
        eid = row.split(",")[0]
        if eid in content:
            print(f"Registro {eid} ya presente en CSV.")
        else:
            with open(CSV_PATH, "a", encoding="utf-8") as f:
                f.write(row + "\n")
            print(f"Anadido {eid} a {CSV_PATH}.")

if __name__ == "__main__":
    main()
