import subprocess
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltspice_config import resolve_ltspice_exe

net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')

def check_n(tp1):
    t0 = 10.0
    t1 = t0 + tp1
    t1f = t1 + 0.1
    t2 = t1f + 5.0
    t2r = t2 + 0.1
    t3 = t2r + 1.0
    t3f = t3 + 0.1
    tstop = t3f + 5.0
    tmeas = t3 - 0.05
    net = (
        '* Test NIGBT\n'
        '.include "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/nigbt.lib"\n'
        'XZ1 VC VG VE XIRGBC20S\n'
        f'V1 Vpulse 0 PWL(0 0 {t0:.3f}u 0 {t0+0.1:.3f}u 15 {t1:.3f}u 15 {t1f:.3f}u 0 {t2:.3f}u 0 {t2r:.3f}u 15 {t3:.3f}u 15 {t3f:.3f}u 0 {tstop:.3f}u 0)\n'
        'R1 VG Vpulse 10\n'
        'R2 VE 0 0.001\n'
        'V2 Vbus 0 400V\n'
        'L1 Vbus VC 100u Rser=1m\n'
        'D1 VC Vbus DMOD\n'
        '.model DMOD D(IS=1e-12 RS=0.01 BV=800 IBV=10u CJO=100p VJ=0.7 M=0.5 TT=35n)\n'
        f'.tran 0 {tstop:.3f}u 0 25n uic\n'
        '.options abstol=1e-9 reltol=1e-4\n'
        f'.meas tran Ic_before_off FIND I(R2) AT {tmeas:.3f}u\n'
        '.end\n'
    )
    cir = os.path.join(net_dir, 'check_n.cir')
    with open(cir, 'w') as f:
        f.write(net)
    subprocess.run([resolve_ltspice_exe(), '-b', cir], timeout=15)
    with open(cir.replace('.cir', '.log'), 'r') as f:
        log = f.read()
    m = re.search(r'ic_before_off:\s*I\(R2\)\s*=\s*([\d\.\+\-e]+)', log, re.I)
    val = float(m.group(1)) if m else 0.0
    print(f'NIGBT tp1={tp1:.3f}us -> Ic={val:.4f} A (error vs 19A: {val-19.0:+.4f} A)')
    return val, t0, t1, t2, t3

def check_p(tp1):
    t0 = 10.0
    t1 = t0 + tp1
    t1f = t1 + 0.1
    t2 = t1f + 5.0
    t2r = t2 + 0.1
    t3 = t2r + 1.0
    t3f = t3 + 0.1
    tstop = t3f + 5.0
    tmeas = t3 - 0.05
    net = (
        '* Test PIGBT\n'
        '.include "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/pigbt.lib"\n'
        'XZ1 VC VG VE XPIGBT\n'
        f'V1 Vpulse 0 PWL(0 0 {t0:.3f}u 0 {t0+0.1:.3f}u -15 {t1:.3f}u -15 {t1f:.3f}u 0 {t2:.3f}u 0 {t2r:.3f}u -15 {t3:.3f}u -15 {t3f:.3f}u 0 {tstop:.3f}u 0)\n'
        'R1 VG Vpulse 10\n'
        'R2 VE 0 0.001\n'
        'V2 0 Vbus 400V\n'
        'L1 VC Vbus 100u Rser=1m\n'
        'D1 Vbus VC DMOD\n'
        '.model DMOD D(IS=1e-12 RS=0.01 BV=800 IBV=10u CJO=100p VJ=0.7 M=0.5 TT=35n)\n'
        f'.tran 0 {tstop:.3f}u 0 25n uic\n'
        '.options abstol=1e-9 reltol=1e-4\n'
        f'.meas tran Ic_before_off FIND -I(R2) AT {tmeas:.3f}u\n'
        '.end\n'
    )
    cir = os.path.join(net_dir, 'check_p.cir')
    with open(cir, 'w') as f:
        f.write(net)
    subprocess.run([resolve_ltspice_exe(), '-b', cir], timeout=15)
    with open(cir.replace('.cir', '.log'), 'r') as f:
        log = f.read()
    m = re.search(r'ic_before_off:\s*-I\(R2\)\s*=\s*([\d\.\+\-e]+)', log, re.I)
    val = float(m.group(1)) if m else 0.0
    print(f'PIGBT tp1={tp1:.3f}us -> Ic={val:.4f} A (error vs 40A: {val-40.0:+.4f} A)')
    return val, t0, t1, t2, t3

if __name__ == '__main__':
    print("--- NIGBT CALIBRATION ---")
    for t in [3.64, 3.65, 3.66, 3.67, 3.68]:
        check_n(t)

    print("\n--- PIGBT CALIBRATION ---")
    for t in [8.86, 8.88, 8.90, 8.92]:
        check_p(t)
