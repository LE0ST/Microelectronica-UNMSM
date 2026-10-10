import os
import subprocess
import numpy as np
from parse_raw import parse_ltspice_ascii_raw
from qa_cientifico_g31 import analyze_sensitivity

# Controlled comparison: P-IGBT at 19.0A (matching N-IGBT at 19.0A)
net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')

# Create dpt_pigbt_19a.cir
net_p_19a = """* DPT P-IGBT Test Bench (Controlled 19A) - LD3
* Autor: Leonardo Sait Yactayo Tolentino
.include "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/pigbt.lib"

XZ1 VC VG VE XPIGBT
V1 Vpulse 0 PWL(0 0 10.0u 0 10.1u -15 13.65u -15 13.75u 0 18.75u 0 18.85u -15 19.85u -15 19.95u 0 30.0u 0)
R1 VG Vpulse 10
R2 VE 0 0.001
V2 0 Vbus 400V
L1 VC Vbus 100u Rser=1m
D1 Vbus VC DMOD
.model DMOD D(IS=1e-12 RS=0.01 BV=800 IBV=10u CJO=100p VJ=0.7 M=0.5 TT=35n)

.tran 0 30u 0 5n uic
.options abstol=1e-9 reltol=1e-4

.meas tran Ic_on FIND -I(R2) AT 19.80u
.meas tran Vce_on FIND (V(VE)-V(VC)) AT 19.80u
.meas tran td_off TRIG V(VG,VE) VAL=-13.5 TD=19.8u RISE=1 TARG I(R2) VAL=-17.1 TD=19.8u RISE=1
.meas tran tf TRIG I(R2) VAL=-17.1 TD=19.8u RISE=1 TARG I(R2) VAL=-1.9 TD=19.8u RISE=1
.meas tran Eoff INTEG (V(VE)-V(VC))*(-I(R2)) FROM 19.85u TO 25.0u

.end
"""

p_cir = os.path.join(net_dir, 'dpt_pigbt_19a.cir')
with open(p_cir, 'w') as f:
    f.write(net_p_19a)

subprocess.run(['G:\\LTspice\\LTspice.exe', '-b', '-ascii', p_cir], timeout=60)

res_p_19a = analyze_sensitivity(p_cir.replace('.cir', '.raw'), 'P', 19.85e-6, 25.0e-6)
res_n_nom = analyze_sensitivity(os.path.join(net_dir, 'dpt_nigbt_nom.raw'), 'N', 19.85e-6, 25.0e-6)

print("=========================================================================================")
print("     ENSAYO CONTROLADO A IGUAL CORRIENTE (19 A): N-IGBT vs P-IGBT (LD3 G3.1)             ")
print("=========================================================================================")
print(f"{'Métrica':<35} | {'N-IGBT (XIRGBC20S)':<20} | {'P-IGBT (XPIGBT)':<20} | {'Diferencia P vs N':<18}")
print("-" * 100)
print(f"{'Corriente conducida Ic_on [A]':<35} | {res_n_nom['ic_on']:<20.2f} | {res_p_19a['ic_on']:<20.2f} | {res_p_19a['ic_on'] - res_n_nom['ic_on']:+.2f} A")
print(f"{'Tensión de conducción |Vce_on| [V]':<35} | {res_n_nom['vce_on']:<20.2f} | {res_p_19a['vce_on']:<20.2f} | {res_p_19a['vce_on'] - res_n_nom['vce_on']:+.2f} V")
print(f"{'Retardo de apagado td_off [ns]':<35} | {res_n_nom['td_off']*1e9:<20.1f} | {res_p_19a['td_off']*1e9:<20.1f} | {res_p_19a['td_off']*1e9 - res_n_nom['td_off']*1e9:+.1f} ns ({(res_p_19a['td_off']/res_n_nom['td_off']-1)*100:+.1f}%)")
print(f"{'Tiempo de caída tf [ns]':<35} | {res_n_nom['tf']*1e9:<20.1f} | {res_p_19a['tf']*1e9:<20.1f} | {res_p_19a['tf']*1e9 - res_n_nom['tf']*1e9:+.1f} ns ({(res_p_19a['tf']/res_n_nom['tf']-1)*100:+.1f}%)")
print(f"{'Tiempo total toff [ns]':<35} | {res_n_nom['t_off']*1e9:<20.1f} | {res_p_19a['t_off']*1e9:<20.1f} | {res_p_19a['t_off']*1e9 - res_n_nom['t_off']*1e9:+.1f} ns")
print(f"{'Energía Eoff total [uJ]':<35} | {res_n_nom['e_off_A']*1e6:<20.1f} | {res_p_19a['e_off_A']*1e6:<20.1f} | {res_p_19a['e_off_A']*1e6 - res_n_nom['e_off_A']*1e6:+.1f} uJ ({(res_p_19a['e_off_A']/res_n_nom['e_off_A']-1)*100:+.1f}%)")
print(f"{'Energía de cola (5%) [uJ]':<35} | {res_n_nom['sensitivity'][5]['e_tail']*1e6:<20.1f} | {res_p_19a['sensitivity'][5]['e_tail']*1e6:<20.1f} | {res_p_19a['sensitivity'][5]['e_tail']*1e6 - res_n_nom['sensitivity'][5]['e_tail']*1e6:+.1f} uJ")
print(f"{'Fracción de cola (5%) [%]':<35} | {res_n_nom['sensitivity'][5]['pct_e_tail']:<20.2f} | {res_p_19a['sensitivity'][5]['pct_e_tail']:<20.2f} | {res_p_19a['sensitivity'][5]['pct_e_tail'] - res_n_nom['sensitivity'][5]['pct_e_tail']:+.2f} %")
