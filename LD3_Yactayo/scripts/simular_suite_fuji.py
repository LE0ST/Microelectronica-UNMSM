import os
import subprocess
import re
import numpy as np
import sys
import matplotlib.pyplot as plt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# SUITE EXPERIMENTAL FUJI ELECTRIC SERIE X (LD3 - EXP-06 A EXP-09)
# Autor: Leonardo Sait Yactayo Tolentino (23190214)
# Curso: Microelectrónica y Sistemas Nanoelectrónicos - UNMSM (2026-II)
# ==============================================================================

net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')
models_dir = os.path.abspath('Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltspice_config import resolve_ltspice_exe
ltspice_exe = resolve_ltspice_exe()
os.makedirs(net_dir, exist_ok=True)

# Definición de las 6 configuraciones optimizadas
CONFIGS = {
    'F01': {
        'model': 'FGW50XS65',
        'desc': '50A Discreto (Sin Diodo Co-Pack)',
        'ic_target': 50.0,
        'rg': 10.0,
        'tp1': 11.54,
        'lsigma': 25.0,
        'temp': 25.0,
        'uso': 'EXP-06 (Ref), EXP-08 (Ref 50A)'
    },
    'F02': {
        'model': 'FGW50XS65C',
        'desc': '50A Co-Pack (Con Diodo Integrado)',
        'ic_target': 50.0,
        'rg': 10.0,
        'tp1': 11.54,
        'lsigma': 25.0,
        'temp': 25.0,
        'uso': 'EXP-06 (Co-Pack 50A), EXP-09 (Ref RG 10 Ohm)'
    },
    'F03': {
        'model': 'FGW75XS65',
        'desc': '75A Discreto (Nominal 75A)',
        'ic_target': 75.0,
        'rg': 10.0,
        'tp1': 17.84,  # Calibrado analíticamente para 75A pre-apagado
        'lsigma': 25.0,
        'temp': 25.0,
        'uso': 'EXP-07 (Ref 75A), EXP-08 (Escalamiento Nominal 75A)'
    },
    'F04': {
        'model': 'FGW75XS65C',
        'desc': '75A Co-Pack (Con Diodo Integrado)',
        'ic_target': 75.0,
        'rg': 10.0,
        'tp1': 17.84,
        'lsigma': 25.0,
        'temp': 25.0,
        'uso': 'EXP-07 (Co-Pack 75A)'
    },
    'F05': {
        'model': 'FGW75XS65',
        'desc': '75A Discreto a Corriente Igualada (50A)',
        'ic_target': 50.0,
        'rg': 10.0,
        'tp1': 11.54,  # Mismo pulso que F01 para cargar a 50A
        'lsigma': 25.0,
        'temp': 25.0,
        'uso': 'EXP-08 (Escalamiento Área a 50A constante)'
    },
    'F06': {
        'model': 'FGW50XS65C',
        'desc': '50A Co-Pack con RG Duplicada (20 Ohm)',
        'ic_target': 50.0,
        'rg': 20.0,
        'tp1': 11.54,
        'lsigma': 25.0,
        'temp': 25.0,
        'uso': 'EXP-09 (Sensibilidad RG: 10 -> 20 Ohm)'
    }
}

def generate_netlist(case_id, cfg, maxstep=1.0):
    model_name = cfg['model']
    tp1 = cfg['tp1']
    rg = cfg['rg']
    lsigma = cfg['lsigma']
    temp = cfg['temp']
    
    # Ruta relativa al modelo
    lib_path = os.path.relpath(os.path.join(models_dir, f"{model_name}.LIB"), net_dir).replace('\\', '/')
    
    # Parámetros temporales del DPT
    t0 = 10.0
    t1 = t0 + tp1
    t1f = t1 + 0.1
    t2 = t1f + 5.0
    t2r = t2 + 0.1
    t3 = t2r + 1.0
    t3f = t3 + 0.1
    tstop = t3f + 5.0
    tmeas = t3 - 0.05
    twin_a = t3
    twin_b = t3 + 5.10

    cir = f"""* Banco DPT Suite Fuji - Caso {case_id}: {cfg['desc']}
* Autor: Leonardo Sait Yactayo Tolentino
.include "{lib_path}"
.temp {temp:.1f}

* Fuente de bus y carga inductiva
V2 Vbus 0 400V
L1 Vbus VC 100u Rser=1m
D1 VC Vbus DMOD
.model DMOD D(IS=1e-12 RS=0.01 BV=800 IBV=10u CJO=100p VJ=0.7 M=0.5 TT=35n)

* Inductancia parasita de lazo de conmutacion (sin Rpar anadida)
Lpar VC VC_igbt {lsigma}n Rser=10m

* Sensores ideales de corriente (0V)
Vsens_C VC_igbt C_int 0V
Vsens_G VG_ext G_int 0V
Vsens_E E_int VE 0V

* Transistor IGBT bajo prueba
X1 C_int G_int E_int {model_name}
R2 VE 0 0.001

* Excitacion de compuerta (Pulsos DPT: 15V / 0V con RG = {rg:.1f} ohm)
V1 Vpulse 0 PWL(0 0 {t0:.3f}u 0 {t0+0.1:.3f}u 15 {t1:.3f}u 15 {t1f:.3f}u 0 {t2:.3f}u 0 {t2r:.3f}u 15 {t3:.3f}u 15 {t3f:.3f}u 0 {tstop:.3f}u 0)
R1 VG_ext Vpulse {rg:.1f}

* Metodo de integracion Gear
.tran 0 {tstop:.3f}u 0 {maxstep}n
.options method=gear abstol=1e-8 reltol=1e-3

* Mediciones previas al segundo apagado
.meas tran Ic_pre FIND I(Vsens_C) AT {tmeas:.3f}u
.meas tran Ie_pre FIND I(Vsens_E) AT {tmeas:.3f}u
.meas tran Ig_pre FIND I(Vsens_G) AT {tmeas:.3f}u
.meas tran Vce_on FIND (V(C_int)-V(E_int)) AT {tmeas:.3f}u
.meas tran Vge_on FIND (V(G_int)-V(E_int)) AT {tmeas:.3f}u

* Tensiones pico en el segundo apagado
.meas tran Vce_peak MAX (V(C_int)-V(E_int)) FROM {t3:.3f}u TO {tstop:.3f}u
.meas tran Vge_peak MAX (V(G_int)-V(E_int)) FROM {t2r:.3f}u TO {t3f:.3f}u

* Umbrales dinamicos de corriente para retardos (90% y 10% de Ic_pre)
.meas tran Ic_90 PARAM 0.90*Ic_pre
.meas tran Ic_10 PARAM 0.10*Ic_pre

* Retardos de conmutacion con corriente terminal de colector
.meas tran td_off TRIG V(G_int,E_int) VAL=13.5 TD={t3-0.05:.3f}u FALL=1 TARG I(Vsens_C) VAL=Ic_90 TD={t3-0.05:.3f}u FALL=1
.meas tran tf TRIG I(Vsens_C) VAL=Ic_90 TD={t3-0.05:.3f}u FALL=1 TARG I(Vsens_C) VAL=Ic_10 TD={t3-0.05:.3f}u FALL=1

* Energias integradas en ventana relativa [t3, t3+5.10u]
.meas tran Eoff_C INTEG (V(C_int)-V(E_int))*I(Vsens_C) FROM {twin_a:.3f}u TO {twin_b:.3f}u
.meas tran Eoff_G INTEG (V(G_int)-V(E_int))*I(Vsens_G) FROM {twin_a:.3f}u TO {twin_b:.3f}u
.end
"""
    cir_path = os.path.join(net_dir, f"fuji_{case_id.lower()}.cir")
    with open(cir_path, 'w') as f:
        f.write(cir)
    return cir_path, t3, twin_a, twin_b

def parse_ascii_raw(raw_path):
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"RAW no existe: {raw_path}")
    with open(raw_path, 'r', errors='ignore') as f:
        lines = f.readlines()
    num_vars = None
    num_points = None
    var_names = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('No. Variables:'):
            num_vars = int(line.split(':')[1].strip())
        elif line.startswith('No. Points:'):
            num_points = int(line.split(':')[1].strip())
        elif line.startswith('Variables:'):
            i += 1
            for v in range(num_vars):
                parts = lines[i].strip().split()
                var_names.append(parts[1])
                i += 1
            continue
        elif line.startswith('Values:'):
            i += 1
            break
        i += 1
    
    data = np.zeros((num_points, num_vars))
    p = 0
    while i < len(lines) and p < num_points:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        parts = line.split()
        if len(parts) >= 2:
            data[p, 0] = float(parts[1])
        else:
            data[p, 0] = float(parts[0])
        i += 1
        for v in range(1, num_vars):
            data[p, v] = float(lines[i].strip())
            i += 1
        p += 1
        
    result = {name: data[:, idx] for idx, name in enumerate(var_names)}
    t = result['time']
    assert len(t) >= 2 and np.all(np.diff(t) > 0) and np.all(np.isfinite(data)), "Fallo validacion integral RAW"
    return result

def integrate_window(t, y, t_a, t_b):
    mask = (t > t_a) & (t < t_b)
    t_mid = t[mask]
    y_mid = y[mask]
    y_a = np.interp(t_a, t, y)
    y_b = np.interp(t_b, t, y)
    t_full = np.concatenate(([t_a], t_mid, [t_b]))
    y_full = np.concatenate(([y_a], y_mid, [y_b]))
    e_net = np.trapezoid(y_full, t_full)
    e_pos = np.trapezoid(np.maximum(y_full, 0.0), t_full)
    e_dev = np.trapezoid(abs(np.minimum(y_full, 0.0)), t_full)
    assert abs(e_net - (e_pos - e_dev)) < 1e-12, "Inconsistencia E_net = E_pos - E_dev"
    return e_net, e_pos, e_dev, t_full, y_full

def compute_metrics_python(t, vge, ic, vce, t_off_cmd):
    # Pre-turn-off reference at t_off_cmd - 40ns
    idx_pre = np.argmin(np.abs(t - (t_off_cmd - 40e-9)))
    vge_pre = vge[idx_pre]
    ic_pre = ic[idx_pre]
    
    vge_90 = 0.90 * vge_pre
    ic_90 = 0.90 * ic_pre
    ic_10 = 0.10 * ic_pre
    ic_tail_level = 0.05 * ic_pre  # Umbral operacional del 5%
    
    mask_win = (t >= t_off_cmd) & (t <= t_off_cmd + 2.5e-6)
    t_w = t[mask_win]
    vge_w = vge[mask_win]
    ic_w = ic[mask_win]
    vce_w = vce[mask_win]
    
    # 1. Cruce 90% VGE
    idx_v = np.where(vge_w < vge_90)[0]
    k_v = idx_v[0]
    t_vge90 = t_w[k_v-1] + (vge_90 - vge_w[k_v-1]) * (t_w[k_v] - t_w[k_v-1]) / (vge_w[k_v] - vge_w[k_v-1])
    
    # 2. Cruce 90% IC
    idx_i90 = np.where(ic_w < ic_90)[0]
    k_i90 = idx_i90[0]
    t_ic90 = t_w[k_i90-1] + (ic_90 - ic_w[k_i90-1]) * (t_w[k_i90] - t_w[k_i90-1]) / (ic_w[k_i90] - ic_w[k_i90-1])
    
    # 3. Cruce 10% IC
    idx_i10 = np.where(ic_w < ic_10)[0]
    k_i10 = idx_i10[0]
    t_ic10 = t_w[k_i10-1] + (ic_10 - ic_w[k_i10-1]) * (t_w[k_i10] - t_w[k_i10-1]) / (ic_w[k_i10] - ic_w[k_i10-1])
    
    # 4. Cruce 5% IC (Inicio de fase de cola)
    idx_tail = np.where((t_w >= t_ic10) & (ic_w < ic_tail_level))[0]
    if len(idx_tail) > 0:
        k_tail = idx_tail[0]
        # Índice en t_w completo
        t_tail = t_w[k_tail-1] + (ic_tail_level - ic_w[k_tail-1]) * (t_w[k_tail] - t_w[k_tail-1]) / (ic_w[k_tail] - ic_w[k_tail-1])
    else:
        t_tail = t_ic10
    
    td_off = t_ic90 - t_vge90
    tf = t_ic10 - t_ic90
    
    # Pendiente máxima di/dt en ventana de caída
    dt_w = np.diff(t_w)
    dic_w = np.diff(ic_w)
    didt = dic_w / dt_w
    # Máxima tasa de caída negativa
    didt_max_fall = np.max(np.abs(np.minimum(didt, 0.0)))  # en A/s
    
    return td_off, tf, ic_pre, vge_pre, t_tail, ic_tail_level, didt_max_fall

def simulate_case(case_id, cfg):
    cir_path, t3, twin_a, twin_b = generate_netlist(case_id, cfg, maxstep=1.0)
    cmd = [ltspice_exe, '-b', '-ascii', cir_path]
    subprocess.run(cmd, check=True)
    
    log_path = cir_path.replace('.cir', '.log')
    with open(log_path) as f:
        log = f.read()
    
    def extract(pat):
        m = re.search(pat, log, re.I)
        return float(m.group(1)) if m else None

    meas_spice = {
        'Ic_pre': extract(r'ic_pre:\s*I\(Vsens_C\)\s*=\s*([\d\.\+\-e]+)'),
        'Vce_on': extract(r'vce_on:.*=\s*([\d\.\+\-e]+)'),
        'Vce_peak': extract(r'vce_peak:.*=\s*([\d\.\+\-e]+)'),
        'td_off': extract(r'td_off[=:\s]+([\d\.\+\-e]+)'),
        'tf': extract(r'tf[=:\s]+([\d\.\+\-e]+)'),
        'Eoff_C': extract(r'eoff_c:.*=\s*([\d\.\+\-e]+)'),
        'Eoff_G': extract(r'eoff_g:.*=\s*([\d\.\+\-e]+)')
    }
    
    raw_path = cir_path.replace('.cir', '.raw')
    raw = parse_ascii_raw(raw_path)
    
    t = raw['time']
    vce = raw['V(c_int)'] - raw['V(e_int)']
    ic = raw['I(Vsens_C)']
    ig = raw['I(Vsens_G)']
    ie = raw['I(Vsens_E)']
    vge = raw['V(g_int)'] - raw['V(e_int)']
    
    # 1. KCL Check
    kcl_err = np.max(np.abs(ic + ig - ie))
    assert kcl_err < 1e-4, f"Fallo KCL en {case_id}: error = {kcl_err} A"
    
    # 2. Métricas de retardo y di/dt en Python
    t_off_cmd = t3 * 1e-6
    td_off_py, tf_py, ic_pre_py, vge_pre_py, t_tail, ic_tail_lvl, didt_max = compute_metrics_python(t, vge, ic, vce, t_off_cmd)
    
    # 3. Integrales de energía en ventana [twin_a, twin_b]
    p_c = vce * ic
    e_c_net, e_c_pos, e_c_dev, _, _ = integrate_window(t, p_c, twin_a * 1e-6, twin_b * 1e-6)
    
    # Integral de energía de cola [t_tail, twin_b]
    e_tail, _, _, _, _ = integrate_window(t, p_c, t_tail, twin_b * 1e-6)
    pct_e_tail = (e_tail / e_c_net) * 100 if e_c_net > 0 else 0.0
    
    # Discrepancia SPICE vs Python
    err_eoff = (e_c_net - meas_spice['Eoff_C']) / meas_spice['Eoff_C'] * 100
    assert abs(err_eoff) < 0.05, f"Discrepancia Eoff SPICE vs Python > 0.05% ({err_eoff}%)"
    
    # Calibración de corriente: tolerancia +-1% de ic_target
    target = cfg['ic_target']
    err_ic = (ic_pre_py - target) / target * 100
    
    res = {
        'case_id': case_id,
        'model': cfg['model'],
        'desc': cfg['desc'],
        'target_ic': target,
        'Ic_pre': ic_pre_py,
        'err_ic_pct': err_ic,
        'Vce_on': meas_spice['Vce_on'],
        'Vce_peak': meas_spice['Vce_peak'],
        'sobredv_bus': meas_spice['Vce_peak'] - 400.0,
        'td_off_spice': meas_spice['td_off'],
        'td_off_py': td_off_py,
        'tf_spice': meas_spice['tf'],
        'tf_py': tf_py,
        'didt_max': didt_max / 1e6,  # A/us
        'I_tail': ic_tail_lvl,
        't_tail': t_tail,
        'E_c_net': e_c_net,
        'E_c_pos': e_c_pos,
        'E_c_dev': e_c_dev,
        'E_tail': e_tail,
        'pct_E_tail': pct_e_tail,
        'Eoff_spice': meas_spice['Eoff_C'],
        'err_eoff_pct': err_eoff,
        'twin_a': twin_a,
        'twin_b': twin_b,
        't': t,
        'vce': vce,
        'ic': ic,
        'vge': vge
    }
    return res

def generate_figures(results):
    fig_dir = os.path.abspath('LD3_Yactayo/figuras')
    os.makedirs(fig_dir, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # FIGURA 6: EXP-06 - Sobretensión y Diodo Co-Pack a 50 A (F01 vs F02)
    # -------------------------------------------------------------------------
    r1, r2 = results['F01'], results['F02']
    t0_ref = r1['twin_a']
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    # Ventana alrededor del apagado: [-0.1 us, +1.0 us]
    t_start = t0_ref - 0.10
    t_end = t0_ref + 1.00
    
    m1 = (r1['t']*1e6 >= t_start) & (r1['t']*1e6 <= t_end)
    m2 = (r2['t']*1e6 >= t_start) & (r2['t']*1e6 <= t_end)
    
    # Subplot 1: VCE(t)
    ax1.plot((r1['t'][m1]*1e6 - t0_ref)*1e3, r1['vce'][m1], 'b-', lw=1.8, label=f"F01: FGW50XS65 Discreto ($V_{{pk}}={r1['Vce_peak']:.1f}$ V)")
    ax1.plot((r2['t'][m2]*1e6 - t0_ref)*1e3, r2['vce'][m2], 'r--', lw=1.8, label=f"F02: FGW50XS65C Co-Pack ($V_{{pk}}={r2['Vce_peak']:.1f}$ V)")
    ax1.axhline(400, color='gray', linestyle=':', label='Bus DC = 400 V')
    ax1.set_ylabel('$V_{CE}$ [V]')
    ax1.set_title('(a) Tensión Colector-Emisor $V_{CE}(t)$ y Sobretensión Pico ($L_\\sigma = 25$ nH)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # Subplot 2: IC(t)
    ax2.plot((r1['t'][m1]*1e6 - t0_ref)*1e3, r1['ic'][m1], 'b-', lw=1.8, label=f"F01: Discreto ($t_{{d(off)}}={r1['td_off_py']*1e9:.1f}$ ns, $t_f={r1['tf_py']*1e9:.1f}$ ns)")
    ax2.plot((r2['t'][m2]*1e6 - t0_ref)*1e3, r2['ic'][m2], 'r--', lw=1.8, label=f"F02: Co-Pack ($t_{{d(off)}}={r2['td_off_py']*1e9:.1f}$ ns, $t_f={r2['tf_py']*1e9:.1f}$ ns)")
    ax2.set_ylabel('$I_C$ [A]')
    ax2.set_title('(b) Corriente Terminal de Colector $I_C(t)$')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right')
    
    # Subplot 3: Potencia instantánea
    p1 = r1['vce'][m1] * r1['ic'][m1] / 1e3  # kW
    p2 = r2['vce'][m2] * r2['ic'][m2] / 1e3
    ax3.plot((r1['t'][m1]*1e6 - t0_ref)*1e3, p1, 'b-', lw=1.8, label=f"F01: Discreto ($E_{{off}}={r1['E_c_net']*1e6:.1f}$ µJ)")
    ax3.plot((r2['t'][m2]*1e6 - t0_ref)*1e3, p2, 'r--', lw=1.8, label=f"F02: Co-Pack ($E_{{off}}={r2['E_c_net']*1e6:.1f}$ µJ)")
    ax3.set_xlabel('Tiempo relativo al comando de apagado $t - t_{off2}$ [ns]')
    ax3.set_ylabel('$P_C$ [kW]')
    ax3.set_title('(c) Potencia Instantánea de Conmutación $P_C(t) = V_{CE} \\cdot I_C$')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc='upper right')
    
    plt.tight_layout()
    f6_path = os.path.join(fig_dir, 'fig6_sobretension_copack_50a.png')
    plt.savefig(f6_path, dpi=300)
    plt.close()
    print(f"    Guardada: {f6_path}")
    
    # -------------------------------------------------------------------------
    # FIGURA 7: EXP-07 - Sobretensión y Diodo Co-Pack a 75 A (F03 vs F04)
    # -------------------------------------------------------------------------
    r3, r4 = results['F03'], results['F04']
    t0_ref3 = r3['twin_a']
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    t_start3 = t0_ref3 - 0.10
    t_end3 = t0_ref3 + 1.00
    m3 = (r3['t']*1e6 >= t_start3) & (r3['t']*1e6 <= t_end3)
    m4 = (r4['t']*1e6 >= t_start3) & (r4['t']*1e6 <= t_end3)
    
    ax1.plot((r3['t'][m3]*1e6 - t0_ref3)*1e3, r3['vce'][m3], 'b-', lw=1.8, label=f"F03: FGW75XS65 Discreto ($V_{{pk}}={r3['Vce_peak']:.1f}$ V)")
    ax1.plot((r4['t'][m4]*1e6 - t0_ref3)*1e3, r4['vce'][m4], 'r--', lw=1.8, label=f"F04: FGW75XS65C Co-Pack ($V_{{pk}}={r4['Vce_peak']:.1f}$ V)")
    ax1.axhline(400, color='gray', linestyle=':', label='Bus DC = 400 V')
    ax1.set_ylabel('$V_{CE}$ [V]')
    ax1.set_title('(a) Tensión Colector-Emisor $V_{CE}(t)$ en Serie de 75 A ($L_\\sigma = 25$ nH)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper right')
    
    ax2.plot((r3['t'][m3]*1e6 - t0_ref3)*1e3, r3['ic'][m3], 'b-', lw=1.8, label=f"F03: Discreto ($t_{{d(off)}}={r3['td_off_py']*1e9:.1f}$ ns, $t_f={r3['tf_py']*1e9:.1f}$ ns)")
    ax2.plot((r4['t'][m4]*1e6 - t0_ref3)*1e3, r4['ic'][m4], 'r--', lw=1.8, label=f"F04: Co-Pack ($t_{{d(off)}}={r4['td_off_py']*1e9:.1f}$ ns, $t_f={r4['tf_py']*1e9:.1f}$ ns)")
    ax2.set_ylabel('$I_C$ [A]')
    ax2.set_title('(b) Corriente Terminal de Colector $I_C(t)$ a 75 A')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right')
    
    p3 = r3['vce'][m3] * r3['ic'][m3] / 1e3
    p4 = r4['vce'][m4] * r4['ic'][m4] / 1e3
    ax3.plot((r3['t'][m3]*1e6 - t0_ref3)*1e3, p3, 'b-', lw=1.8, label=f"F03: Discreto ($E_{{off}}={r3['E_c_net']*1e6:.1f}$ µJ)")
    ax3.plot((r4['t'][m4]*1e6 - t0_ref3)*1e3, p4, 'r--', lw=1.8, label=f"F04: Co-Pack ($E_{{off}}={r4['E_c_net']*1e6:.1f}$ µJ)")
    ax3.set_xlabel('Tiempo relativo al comando de apagado $t - t_{off2}$ [ns]')
    ax3.set_ylabel('$P_C$ [kW]')
    ax3.set_title('(c) Potencia Instantánea de Conmutación $P_C(t)$')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc='upper right')
    
    plt.tight_layout()
    f7_path = os.path.join(fig_dir, 'fig7_sobretension_copack_75a.png')
    plt.savefig(f7_path, dpi=300)
    plt.close()
    print(f"    Guardada: {f7_path}")
    
    # -------------------------------------------------------------------------
    # FIGURA 8: EXP-08 - Escalamiento de Área de Silicio (F01 vs F05 vs F03)
    # -------------------------------------------------------------------------
    r5 = results['F05']
    t0_ref5 = r5['twin_a']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
    m5 = (r5['t']*1e6 >= t_start) & (r5['t']*1e6 <= t_end)
    
    # Subplot 1: VCE(t)
    ax1.plot((r1['t'][m1]*1e6 - t0_ref)*1e3, r1['vce'][m1], 'b-', lw=1.8, label=f"F01: 50A Chip @ 50A ($V_{{on}}={r1['Vce_on']:.2f}$ V, $V_{{pk}}={r1['Vce_peak']:.1f}$ V)")
    ax1.plot((r5['t'][m5]*1e6 - t0_ref5)*1e3, r5['vce'][m5], 'g--', lw=1.8, label=f"F05: 75A Chip @ 50A ($V_{{on}}={r5['Vce_on']:.2f}$ V, $V_{{pk}}={r5['Vce_peak']:.1f}$ V)")
    ax1.plot((r3['t'][m3]*1e6 - t0_ref3)*1e3, r3['vce'][m3], 'm-.', lw=1.8, label=f"F03: 75A Chip @ 75A ($V_{{on}}={r3['Vce_on']:.2f}$ V, $V_{{pk}}={r3['Vce_peak']:.1f}$ V)")
    ax1.axhline(400, color='gray', linestyle=':')
    ax1.set_ylabel('$V_{CE}$ [V]')
    ax1.set_title('(a) Dinámica de Tensión y Sobretensión Inducida según Área y Corriente')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # Subplot 2: IC(t)
    ax2.plot((r1['t'][m1]*1e6 - t0_ref)*1e3, r1['ic'][m1], 'b-', lw=1.8, label=f"F01: 50A Chip @ 50A ($E_{{off}}={r1['E_c_net']*1e6:.1f}$ µJ)")
    ax2.plot((r5['t'][m5]*1e6 - t0_ref5)*1e3, r5['ic'][m5], 'g--', lw=1.8, label=f"F05: 75A Chip @ 50A ($E_{{off}}={r5['E_c_net']*1e6:.1f}$ µJ)")
    ax2.plot((r3['t'][m3]*1e6 - t0_ref3)*1e3, r3['ic'][m3], 'm-.', lw=1.8, label=f"F03: 75A Chip @ 75A ($E_{{off}}={r3['E_c_net']*1e6:.1f}$ µJ)")
    ax2.set_xlabel('Tiempo relativo al comando de apagado $t - t_{off2}$ [ns]')
    ax2.set_ylabel('$I_C$ [A]')
    ax2.set_title('(b) Formas de Onda de Corriente y Compromiso de Conmutación')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    f8_path = os.path.join(fig_dir, 'fig8_comparativa_area_50vs75.png')
    plt.savefig(f8_path, dpi=300)
    plt.close()
    print(f"    Guardada: {f8_path}")
    
    # -------------------------------------------------------------------------
    # FIGURA 9: EXP-09 - Sensibilidad a la Resistencia de Compuerta RG (F02 vs F06)
    # -------------------------------------------------------------------------
    r6 = results['F06']
    t0_ref6 = r6['twin_a']
    m6 = (r6['t']*1e6 >= t_start) & (r6['t']*1e6 <= t_end)
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    
    # VGE(t)
    ax1.plot((r2['t'][m2]*1e6 - t0_ref)*1e3, r2['vge'][m2], 'r-', lw=1.8, label=f"F02: $R_G = 10\\ \\Omega$ ($t_{{d(off)}}={r2['td_off_py']*1e9:.1f}$ ns)")
    ax1.plot((r6['t'][m6]*1e6 - t0_ref6)*1e3, r6['vge'][m6], 'k--', lw=1.8, label=f"F06: $R_G = 20\\ \\Omega$ ($t_{{d(off)}}={r6['td_off_py']*1e9:.1f}$ ns)")
    ax1.axhline(0, color='gray', linestyle=':')
    ax1.set_ylabel('$V_{GE}$ [V]')
    ax1.set_title('(a) Tensión de Compuerta $V_{GE}(t)$ y Retardo de Descarga')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # VCE(t)
    ax2.plot((r2['t'][m2]*1e6 - t0_ref)*1e3, r2['vce'][m2], 'r-', lw=1.8, label=f"F02: $R_G = 10\\ \\Omega$ ($V_{{pk}}={r2['Vce_peak']:.1f}$ V, $+{r2['sobredv_bus']:.1f}$ V)")
    ax2.plot((r6['t'][m6]*1e6 - t0_ref6)*1e3, r6['vce'][m6], 'k--', lw=1.8, label=f"F06: $R_G = 20\\ \\Omega$ ($V_{{pk}}={r6['Vce_peak']:.1f}$ V, $+{r6['sobredv_bus']:.1f}$ V)")
    ax2.axhline(400, color='gray', linestyle=':')
    ax2.set_ylabel('$V_{CE}$ [V]')
    ax2.set_title('(b) Tensión $V_{CE}(t)$: Mitigación de Sobretensión por Mayor $R_G$')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right')
    
    # IC(t)
    ax3.plot((r2['t'][m2]*1e6 - t0_ref)*1e3, r2['ic'][m2], 'r-', lw=1.8, label=f"F02: $R_G = 10\\ \\Omega$ ($di/dt={r2['didt_max']:.0f}$ A/µs, $E_{{off}}={r2['E_c_net']*1e6:.1f}$ µJ)")
    ax3.plot((r6['t'][m6]*1e6 - t0_ref6)*1e3, r6['ic'][m6], 'k--', lw=1.8, label=f"F06: $R_G = 20\\ \\Omega$ ($di/dt={r6['didt_max']:.0f}$ A/µs, $E_{{off}}={r6['E_c_net']*1e6:.1f}$ µJ)")
    ax3.set_xlabel('Tiempo relativo al comando de apagado $t - t_{off2}$ [ns]')
    ax3.set_ylabel('$I_C$ [A]')
    ax3.set_title('(c) Caída de Corriente $I_C(t)$ y Penalización Energética $E_{off}$')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc='upper right')
    
    plt.tight_layout()
    f9_path = os.path.join(fig_dir, 'fig9_sensibilidad_rg_conmutacion.png')
    plt.savefig(f9_path, dpi=300)
    plt.close()
    print(f"    Guardada: {f9_path}")

def print_final_table(results):
    print("\n" + "="*115)
    print("TABLA CONSOLIDADA OFICIAL: SUITE FUJI ELECTRIC SERIE X (F01 A F06 A 25 °C)")
    print("="*115)
    header = f"| {'ID':<4} | {'Modelo':<11} | {'I_tgt':<6} | {'Ic_pre [A]':<10} | {'Vce_on':<8} | {'Vce_pk':<8} | {'td_off':<9} | {'tf [ns]':<8} | {'di/dt [A/us]':<13} | {'Eoff [uJ]':<10} | {'%E_tail':<8} | {'Status':<6} |"
    sep = f"|{'-'*6}|{'-'*13}|{'-'*8}|{'-'*12}|{'-'*10}|{'-'*10}|{'-'*11}|{'-'*10}|{'-'*15}|{'-'*12}|{'-'*10}|{'-'*8}|"
    print(header)
    print(sep)
    for cid in ['F01', 'F02', 'F03', 'F04', 'F05', 'F06']:
        r = results[cid]
        status = "PASS" if abs(r['err_ic_pct']) <= 1.0 else "FAIL"
        row = f"| {r['case_id']:<4} | {r['model']:<11} | {r['target_ic']:<6.0f} | {r['Ic_pre']:<10.3f} | {r['Vce_on']:<8.3f} | {r['Vce_peak']:<8.2f} | {r['td_off_py']*1e9:<9.2f} | {r['tf_py']*1e9:<8.2f} | {r['didt_max']:<13.1f} | {r['E_c_net']*1e6:<10.2f} | {r['pct_E_tail']:<8.2f} | {status:<6} |"
        print(row)
    print(sep)

if __name__ == '__main__':
    print("="*95)
    print("EJECUTANDO SUITE COMPLETA CONTROLADA DE F01 A F06 A 25 °C")
    print("="*95)
    
    results = {}
    for cid in ['F01', 'F02', 'F03', 'F04', 'F05', 'F06']:
        print(f"\n>>> Simulando {cid}: {CONFIGS[cid]['desc']}...")
        r = simulate_case(cid, CONFIGS[cid])
        results[cid] = r
        status_ic = "PASS" if abs(r['err_ic_pct']) <= 1.0 else "FAIL"
        print(f"    Ic_pre:      {r['Ic_pre']:.3f} A (Target: {r['target_ic']:.1f} A | Error: {r['err_ic_pct']:+.2f}%) [{status_ic}]")
        print(f"    Vce_on:      {r['Vce_on']:.3f} V")
        print(f"    Vce_peak:    {r['Vce_peak']:.2f} V (Sobretensión vs bus: +{r['sobredv_bus']:.2f} V)")
        print(f"    td_off:      SPICE={r['td_off_spice']*1e9:.2f} ns | Python={r['td_off_py']*1e9:.2f} ns")
        print(f"    tf:          SPICE={r['tf_spice']*1e9:.2f} ns | Python={r['tf_py']*1e9:.2f} ns")
        print(f"    di/dt_max:   {r['didt_max']:.1f} A/us")
        print(f"    E_c_net:     SPICE={r['Eoff_spice']*1e6:.2f} uJ | Python={r['E_c_net']*1e6:.2f} uJ (Diff: {r['err_eoff_pct']:+.5f}%)")
        print(f"    E_tail:      {r['E_tail']*1e6:.2f} uJ ({r['pct_E_tail']:.2f}% de Eoff)")
    
    print("\n" + "="*95)
    print("GENERANDO FIGURAS CIENTÍFICAS A 300 DPI")
    print("="*95)
    generate_figures(results)
    
    print_final_table(results)
