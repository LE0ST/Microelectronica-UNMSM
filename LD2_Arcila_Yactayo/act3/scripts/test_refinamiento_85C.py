# -*- coding: utf-8 -*-
"""
test_refinamiento_85C.py
Refina localmente Wkp entre 10.5nm y 15nm a 85°C con resolución <= 1nm
para caracterizar la transición exacta de retención.
"""

import os
import subprocess
import sys
import shutil

ACT3_DIR = r"G:\Proyectos\MicroNano\LD2_Arcila_Yactayo\act3"
CIRCUITOS_DIR = os.path.join(ACT3_DIR, "circuitos")
LTSPICE_EXE = r"G:\LTspice\LTspice.exe"
SCRIPTS_DIR = r"G:\Proyectos\MicroNano\LD2_Arcila_Yactayo\scripts\lectura_resultados"
sys.path.append(SCRIPTS_DIR)
from parse_spice_log import parse_log

cir_content = """* ACTIVIDAD 3 - Refinamiento Wkp a 85C
.include ../../modelos/ptm45hp.lib
.include ../../modelos/ptm45lp.lib
.include ../../modelos/ptm130.lib

.param VDD=1.0
.param Ln=45n Wn=90n Wp=135n
.param Wkp=15n
.param CL=2f Cout=1f
.param Teval_start=0.52n
.param Tret=1.0u
.param Tstop={Teval_start + Tret}
.temp 85
.options gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear

.step param Wkp list 10.5n 11n 12n 13n 14n 15n

Vdd vdd 0 {VDD}
Vclk clk 0 PWL(0 0 0.5n 0 0.52n {VDD} {Tstop} {VDD})
Va a 0 0
Vb b 0 0
Vc c 0 0

.param Ad={Wn*3*90n} Pd={Wn*3+180n}

Mp dyn clk vdd vdd pmos_45hp W={Wp} L={Ln}
M1 n1 a dyn 0 nmos_45hp W={Wn*3} L={Ln} AS={Ad} AD={Ad} PS={Pd} PD={Pd}
M2 n2 b n1 0 nmos_45hp W={Wn*3} L={Ln} AS={Ad} AD={Ad} PS={Pd} PD={Pd}
M3 n3 c n2 0 nmos_45hp W={Wn*3} L={Ln} AS={Ad} AD={Ad} PS={Pd} PD={Pd}
Mf 0 clk n3 0 nmos_45hp W={Wn*3} L={Ln} AS={Ad} AD={Ad} PS={Pd} PD={Pd}
CL dyn 0 {CL}

Mk dyn out vdd vdd pmos_45hp W={Wkp} L={Ln}

Mpi out dyn vdd vdd pmos_45hp W={Wp} L={Ln}
Mni out dyn 0 0 nmos_45hp W={Wn} L={Ln}
Cout out 0 {Cout}

.tran 0 {Tstop} 0 1n

.meas TRAN vdyn_start FIND V(dyn) AT={Teval_start}
.meas TRAN vdyn_end_1us FIND V(dyn) AT={Tstop}
.meas TRAN vdyn_min MIN V(dyn) FROM={Teval_start} TO={Tstop}
.meas TRAN t_cross_0p9vdd WHEN V(dyn)={0.90*VDD} FALL=1
.meas TRAN isupply_avg AVG -I(Vdd) FROM=10n TO={Tstop}
.meas TRAN ileak_pdn_avg AVG Is(M1) FROM=10n TO={Tstop}
.meas TRAN ikp_d_avg AVG Id(Mk) FROM=10n TO={Tstop}
.meas TRAN ikp_inj_avg PARAM {-ikp_d_avg}

.save V(clk) V(dyn) V(out) I(Vdd) I(CL) Id(M1) Is(M1) Id(Mp) Id(Mk) Is(Mk) Ig(Mni) Ig(Mpi)
.end
"""

test_cir = os.path.join(CIRCUITOS_DIR, "nand3_retencion_refinamiento_85C.cir")
with open(test_cir, "w", encoding="utf-8") as f:
    f.write(cir_content)

print(f"Ejecutando refinamiento en: {test_cir}")
cmd = [LTSPICE_EXE, "-b", test_cir]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"LTspice retorno codigo: {res.returncode}")

log_file = os.path.join(CIRCUITOS_DIR, "nand3_retencion_refinamiento_85C.log")
parsed = parse_log(log_file, required_metrics=["vdyn_start", "vdyn_end_1us", "vdyn_min"])
print(f"Valido: {parsed['is_valid']}")
for i, st in enumerate(parsed['steps']):
    w = st.get('wkp') * 1e9
    vend = parsed['measurements']['vdyn_end_1us'][i]['val']
    vmin = parsed['measurements']['vdyn_min'][i]['val']
    tc = parsed['measurements']['t_cross_0p9vdd'][i]['val'] if parsed['measurements'].get('t_cross_0p9vdd') else None
    ikp = parsed['measurements']['ikp_inj_avg'][i]['val'] if parsed['measurements'].get('ikp_inj_avg') else None
    tc_s = f"{tc*1e6:.4f} us" if tc is not None else "Censurado (>1.0us)"
    print(f"Wkp = {w:5.2f} nm | Vdyn(1us) = {vend:.6f} V | Vmin = {vmin:.6f} V | t_cross = {tc_s} | Ikp_inj = {ikp:.3e} A")
