import os
import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# PILOTO EXPERIMENTAL: FUJI ELECTRIC FGW50XS65 (50A, 650V Serie X)
# Autor: Leonardo Sait Yactayo Tolentino (23190214)
# Curso: Microelectrónica y Sistemas Nanoelectrónicos - UNMSM (2026-II)
# ==============================================================================

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltspice_config import resolve_ltspice_exe

net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')
fuji_lib_rel = "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/FGW50XS65.LIB"
ltspice_exe = resolve_ltspice_exe()

def generate_pilot_netlist(tp1=11.54, lsigma=25.0, rpar=50.0, maxstep=1.0):
    """
    Genera el netlist SPICE para el banco DPT del FGW50XS65.
    Condiciones nominales: Vbus=400V, Ic=50A, RG=10 ohm, VGE=15V/0V, T=27C.
    Se utiliza .options method=gear para garantizar convergencia incondicional
    frente a la rigidez numérica de las fuentes no lineales LIMIT del macromodelo.
    """
    t0 = 10.0
    t1 = t0 + tp1
    t1f = t1 + 0.1
    t2 = t1f + 5.0
    t2r = t2 + 0.1
    t3 = t2r + 1.0
    t3f = t3 + 0.1
    tstop = t3f + 5.0
    tmeas = t3 - 0.05

    lsigma_block = ""
    vc_node = "VC"
    if lsigma > 0:
        rpar_str = f" Rpar={rpar}" if rpar else ""
        lsigma_block = f"Lpar VC VC_igbt {lsigma}n Rser=10m{rpar_str}\n"
        vc_node = "VC_igbt"

    cir = f"""* Piloto DPT FGW50XS65 (Fuji Electric Serie X 50A 650V)
* Autor: Leonardo Sait Yactayo Tolentino
.include "{fuji_lib_rel}"

* Fuente DC de bus y carga inductiva
V2 Vbus 0 400V
L1 Vbus VC 100u Rser=1m
D1 VC Vbus DMOD
.model DMOD D(IS=1e-12 RS=0.01 BV=800 IBV=10u CJO=100p VJ=0.7 M=0.5 TT=35n)

* Inductancia parasita de lazo de conmutacion
{lsigma_block}
* Interruptor bajo prueba (Low-Side IGBT)
X1 {vc_node} VG VE FGW50XS65
R2 VE 0 0.001

* Excitacion de compuerta (Pulsos DPT: 15V / 0V con RG = 10 ohm)
V1 Vpulse 0 PWL(0 0 {t0:.3f}u 0 {t0+0.1:.3f}u 15 {t1:.3f}u 15 {t1f:.3f}u 0 {t2:.3f}u 0 {t2r:.3f}u 15 {t3:.3f}u 15 {t3f:.3f}u 0 {tstop:.3f}u 0)
R1 VG Vpulse 10

* Metodo de integracion Gear para estabilidad numerica superior
.tran 0 {tstop:.3f}u 0 {maxstep}n
.options method=gear abstol=1e-8 reltol=1e-3

* Mediciones en el segundo pulso de conduccion y apagado
.meas tran Ic_on FIND I(R2) AT {tmeas:.3f}u
.meas tran Vce_on FIND (V({vc_node})-V(VE)) AT {tmeas:.3f}u
.meas tran Vce_peak MAX (V({vc_node})-V(VE)) FROM {t3:.3f}u TO {tstop:.3f}u
.meas tran Vge_peak MAX (V(VG)-V(VE)) FROM {t2r:.3f}u TO {t3f:.3f}u

* Retardos de conmutacion: td(off) [90% VGE a 90% IC] y tf [90% IC a 10% IC]
.meas tran td_off TRIG V(VG,VE) VAL=13.5 TD={t3-0.05:.3f}u FALL=1 TARG I(R2) VAL=45.0 TD={t3-0.05:.3f}u FALL=1
.meas tran tf TRIG I(R2) VAL=45.0 TD={t3-0.05:.3f}u FALL=1 TARG I(R2) VAL=5.0 TD={t3-0.05:.3f}u FALL=1

* Energia de apagado Eoff
.meas tran Eoff INTEG (V({vc_node})-V(VE))*I(R2) FROM {t3:.3f}u TO {tstop:.3f}u
.end
"""
    return cir, t3, tstop

def run_simulation(cir_content, file_base):
    cir_path = os.path.join(net_dir, f"{file_base}.cir")
    with open(cir_path, 'w') as f:
        f.write(cir_content)
    
    # Run LTspice in batch mode with ASCII raw generation
    cmd = [ltspice_exe, '-b', '-ascii', cir_path]
    subprocess.run(cmd, check=True)
    
    log_path = os.path.join(net_dir, f"{file_base}.log")
    with open(log_path) as f:
        log = f.read()
    
    def extract(pat):
        m = re.search(pat, log, re.I)
        return float(m.group(1)) if m else 0.0
    
    metrics = {
        'ic_on': extract(r'ic_on:\s*I\(R2\)\s*=\s*([\d\.\+\-e]+)'),
        'vce_on': extract(r'vce_on:.*=\s*([\d\.\+\-e]+)'),
        'vce_peak': extract(r'vce_peak:.*=\s*([\d\.\+\-e]+)'),
        'vge_peak': extract(r'vge_peak:.*=\s*([\d\.\+\-e]+)'),
        'td_off': extract(r'td_off[=:\s]+([\d\.\+\-e]+)'),
        'tf': extract(r'tf[=:\s]+([\d\.\+\-e]+)'),
        'eoff': extract(r'eoff:.*=\s*([\d\.\+\-e]+)')
    }
    return metrics

if __name__ == '__main__':
    print("="*80)
    print("EJECUTANDO PILOTO FGW50XS65 (FUJI ELECTRIC 50A 650V)")
    print("="*80)

    # 1. Caso Base: Lsigma = 0 nH
    print("\n1. Simulando Caso Base (Lsigma = 0 nH)...")
    cir_l0, _, _ = generate_pilot_netlist(tp1=11.54, lsigma=0.0, maxstep=1.0)
    m_l0 = run_simulation(cir_l0, "piloto_fgw50xs65_L0")
    print(f"   Ic_on:    {m_l0['ic_on']:.3f} A")
    print(f"   Vce_on:   {m_l0['vce_on']:.3f} V")
    print(f"   Vce_peak: {m_l0['vce_peak']:.2f} V")
    print(f"   td(off):  {m_l0['td_off']*1e9:.2f} ns")
    print(f"   tf:       {m_l0['tf']*1e9:.2f} ns")
    print(f"   Eoff:     {m_l0['eoff']*1e6:.2f} uJ")

    # 2. Caso Nominal con Inductancia Parasita: Lsigma = 25 nH (Rpar = 50 ohm)
    print("\n2. Simulando con Inductancia Parásita (Lsigma = 25 nH, Rpar = 50 ohm)...")
    cir_l25, _, _ = generate_pilot_netlist(tp1=11.54, lsigma=25.0, rpar=50.0, maxstep=1.0)
    m_l25 = run_simulation(cir_l25, "piloto_fgw50xs65_L25")
    print(f"   Ic_on:    {m_l25['ic_on']:.3f} A")
    print(f"   Vce_on:   {m_l25['vce_on']:.3f} V")
    print(f"   Vce_peak: {m_l25['vce_peak']:.2f} V  (Sobretensión: +{m_l25['vce_peak'] - m_l0['vce_peak']:.2f} V)")
    print(f"   td(off):  {m_l25['td_off']*1e9:.2f} ns")
    print(f"   tf:       {m_l25['tf']*1e9:.2f} ns")
    print(f"   Eoff:     {m_l25['eoff']*1e6:.2f} uJ  (Incremento pérdidas: +{(m_l25['eoff']/m_l0['eoff']-1)*100:.2f}%)")

    # 3. Barrido de Convergencia Temporal
    print("\n3. Barrido de Convergencia Temporal en Lsigma = 0 nH (maxstep = 5ns, 1ns, 0.5ns)...")
    conv_steps = [5.0, 1.0, 0.5]
    conv_data = {}
    for step in conv_steps:
        cir_step, _, _ = generate_pilot_netlist(tp1=11.54, lsigma=0.0, maxstep=step)
        conv_data[step] = run_simulation(cir_step, f"piloto_fgw50xs65_conv_{step}ns")

    print("\n" + "="*80)
    print(f"{'maxstep':<10} | {'Ic_on [A]':<11} | {'Vce_pk [V]':<12} | {'td_off [ns]':<12} | {'tf [ns]':<10} | {'Eoff [uJ]':<10}")
    print("="*80)
    for step, d in conv_data.items():
        print(f"{step:<8} ns | {d['ic_on']:<11.3f} | {d['vce_peak']:<12.2f} | {d['td_off']*1e9:<12.2f} | {d['tf']*1e9:<10.2f} | {d['eoff']*1e6:<10.2f}")
    print("="*80)
