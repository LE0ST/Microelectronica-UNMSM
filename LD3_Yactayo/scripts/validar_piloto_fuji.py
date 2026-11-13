import os
import subprocess
import re
import numpy as np
import time
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from parse_raw import parse_ltspice_ascii_raw
# Autor: Leonardo Sait Yactayo Tolentino

net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')
fuji_lib_rel = "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/FGW50XS65.LIB"
from ltspice_config import resolve_ltspice_exe
ltspice_exe = resolve_ltspice_exe()

def generate_netlist(tp1=11.54, lsigma=25.0, rpar=50.0, maxstep=1.0, file_base="pilot_test"):
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
        rpar_str = f" Rpar={rpar}" if rpar is not None else ""
        lsigma_block = f"Lpar VC VC_igbt {lsigma}n Rser=10m{rpar_str}\n"
        vc_node = "VC_igbt"

    cir = f"""* G4.1 Validacion Piloto FGW50XS65
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

* Excitacion de compuerta (15V / 0V con RG = 10 ohm)
V1 Vpulse 0 PWL(0 0 {t0:.3f}u 0 {t0+0.1:.3f}u 15 {t1:.3f}u 15 {t1f:.3f}u 0 {t2:.3f}u 0 {t2r:.3f}u 15 {t3:.3f}u 15 {t3f:.3f}u 0 {tstop:.3f}u 0)
R1 VG Vpulse 10

* Metodo de integracion Gear
.tran 0 {tstop:.3f}u 0 {maxstep}n
.options method=gear abstol=1e-8 reltol=1e-3

* Mediciones cuantitativas (.meas)
.meas tran Ic_on FIND I(R2) AT {tmeas:.3f}u
.meas tran Vce_on FIND (V({vc_node})-V(VE)) AT {tmeas:.3f}u
.meas tran Vce_peak MAX (V({vc_node})-V(VE)) FROM {t3:.3f}u TO {tstop:.3f}u
.meas tran Vge_peak MAX (V(VG)-V(VE)) FROM {t2r:.3f}u TO {t3f:.3f}u
.meas tran td_off TRIG V(VG,VE) VAL=13.5 TD={t3-0.05:.3f}u FALL=1 TARG I(R2) VAL=45.0 TD={t3-0.05:.3f}u FALL=1
.meas tran tf TRIG I(R2) VAL=45.0 TD={t3-0.05:.3f}u FALL=1 TARG I(R2) VAL=5.0 TD={t3-0.05:.3f}u FALL=1
.meas tran Eoff INTEG (V({vc_node})-V(VE))*I(R2) FROM {t3:.3f}u TO {tstop:.3f}u
.end
"""
    cir_path = os.path.join(net_dir, f"{file_base}.cir")
    with open(cir_path, 'w') as f:
        f.write(cir)
    return cir_path, t3, tstop

def run_sim(cir_path, timeout=60):
    t_start = time.time()
    try:
        res = subprocess.run([ltspice_exe, '-b', '-ascii', cir_path], timeout=timeout)
        dt = time.time() - t_start
        status = "OK" if res.returncode == 0 else f"ERROR({res.returncode})"
    except subprocess.TimeoutExpired:
        dt = time.time() - t_start
        status = f"TIMEOUT(>{timeout}s)"
        # Kill orphan process if any
        subprocess.run(["powershell", "-Command", "Get-Process LTspice -ErrorAction SilentlyContinue | Stop-Process -Force"])
    
    log_path = cir_path.replace('.cir', '.log')
    metrics = {'status': status, 'cpu_time': dt}
    if os.path.exists(log_path):
        with open(log_path) as f:
            log = f.read()
        def extract(pat):
            m = re.search(pat, log, re.I)
            return float(m.group(1)) if m else None
        metrics['ic_on'] = extract(r'ic_on:\s*I\(R2\)\s*=\s*([\d\.\+\-e]+)')
        metrics['vce_on'] = extract(r'vce_on:.*=\s*([\d\.\+\-e]+)')
        metrics['vce_peak'] = extract(r'vce_peak:.*=\s*([\d\.\+\-e]+)')
        metrics['td_off'] = extract(r'td_off[=:\s]+([\d\.\+\-e]+)')
        metrics['tf'] = extract(r'tf[=:\s]+([\d\.\+\-e]+)')
        metrics['eoff'] = extract(r'eoff:.*=\s*([\d\.\+\-e]+)')
    return metrics

if __name__ == '__main__':
    print("="*85)
    print("1. ESTUDIO DE SENSIBILIDAD AL AMORTIGUAMIENTO (Lpar = 25 nH)")
    print("="*85)
    rpar_cases = [None, 200.0, 100.0, 50.0]
    damping_results = {}
    for rp in rpar_cases:
        rp_label = "None" if rp is None else f"{int(rp)}"
        print(f"Simulando Rpar = {rp_label} ohm ...")
        cpath, _, _ = generate_netlist(tp1=11.54, lsigma=25.0, rpar=rp, maxstep=1.0, file_base=f"val_damp_rpar_{rp_label}")
        res = run_sim(cpath, timeout=60)
        damping_results[rp_label] = res
        print(f"   Status: {res['status']} | Tiempo: {res['cpu_time']:.2f} s")
        if res.get('vce_peak') is not None:
            print(f"   Ic_on={res.get('ic_on', 0):.3f} A | Vce_pk={res.get('vce_peak', 0):.2f} V | td_off={res.get('td_off', 0)*1e9:.2f} ns | Eoff={res.get('eoff', 0)*1e6:.2f} uJ")

    print("\n" + "="*85)
    print("2. ESTUDIO DE CONVERGENCIA TEMPORAL DEL CASO CRÍTICO (Lpar = 25 nH, Rpar = 50 ohm)")
    print("="*85)
    conv_steps = [5.0, 1.0, 0.5]
    conv_results = {}
    for st in conv_steps:
        print(f"Simulando maxstep = {st} ns ...")
        cpath, _, _ = generate_netlist(tp1=11.54, lsigma=25.0, rpar=50.0, maxstep=st, file_base=f"val_conv_step_{st}ns")
        res = run_sim(cpath, timeout=90)
        conv_results[st] = res
        print(f"   Status: {res['status']} | Tiempo: {res['cpu_time']:.2f} s")
        if res.get('vce_peak') is not None:
            print(f"   Ic_on={res.get('ic_on', 0):.3f} A | Vce_pk={res.get('vce_peak', 0):.2f} V | td_off={res.get('td_off', 0)*1e9:.2f} ns | Eoff={res.get('eoff', 0)*1e6:.2f} uJ")

    print("\n" + "="*85)
    print("3. VALIDACIÓN DE ENERGÍA Y DESGLOSE DE COMPONENTES (LTspice vs Python)")
    print("="*85)
    from parse_raw import parse_ltspice_ascii_raw

    # Validar caso L25 Rpar50 step 1.0ns
    raw_path = os.path.join(net_dir, "val_conv_step_1.0ns.raw")
    if os.path.exists(raw_path):
        data = parse_ltspice_ascii_raw(raw_path)
        t = data['time']
        vce = data['V(vc_igbt)'] - data['V(ve)']
        ic = data['I(R2)']
        v_lpar = data['V(vc)'] - data['V(vc_igbt)']

        t_start = 27.74e-6
        t_end = 32.84e-6
        mask = (t >= t_start) & (t <= t_end)
        t_w = t[mask]
        vce_w = vce[mask]
        ic_w = ic[mask]
        vlpar_w = v_lpar[mask]

        # Energia IGBT en Python
        p_igbt = vce_w * ic_w
        p_igbt_pos = np.copy(p_igbt)
        p_igbt_pos[p_igbt_pos < 0] = 0
        e_igbt_py = np.trapezoid(p_igbt_pos, t_w)
        e_igbt_spice = conv_results[1.0]['eoff']

        # Energia disipada en Rpar = 50 ohm
        p_rpar = (vlpar_w ** 2) / 50.0
        e_rpar_py = np.trapezoid(p_rpar, t_w)

        # Energia almacenada inicial y final en Lpar = 25 nH
        idx_start = np.argmin(np.abs(t - t_start))
        idx_end = np.argmin(np.abs(t - t_end))
        i_lpar_start = ic[idx_start]
        i_lpar_end = ic[idx_end]
        e_lpar_init = 0.5 * 25e-9 * (i_lpar_start ** 2)
        e_lpar_final = 0.5 * 25e-9 * (i_lpar_end ** 2)
        delta_e_lpar = e_lpar_init - e_lpar_final

        print(f"Ventana de integracion: [{t_start*1e6:.3f} us, {t_end*1e6:.3f} us]")
        print(f"Eoff IGBT (LTspice .meas): {e_igbt_spice*1e6:.2f} uJ")
        print(f"Eoff IGBT (Python trapz):  {e_igbt_py*1e6:.2f} uJ")
        diff_pct = (e_igbt_py - e_igbt_spice) / e_igbt_spice * 100
        print(f"Discrepancia Python vs SPICE: {diff_pct:+.3f} %")
        print(f"Energia disipada en Rpar (50 ohm): {e_rpar_py*1e6:.3f} uJ ({e_rpar_py/e_igbt_spice*100:.3f}% de Eoff)")
        print(f"Energia inductiva liberada por Lpar: {delta_e_lpar*1e6:.3f} uJ")
