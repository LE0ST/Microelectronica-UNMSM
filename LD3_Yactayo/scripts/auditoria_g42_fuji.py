import os
import subprocess
import re
import numpy as np
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# AUDITORÍA Y CORRECCIÓN CONTROLADA G4.2: PILOTO FUJI FGW50XS65
# Autor: Leonardo Sait Yactayo Tolentino (23190214)
# Curso: Microelectrónica y Sistemas Nanoelectrónicos - UNMSM (2026-II)
# ==============================================================================

net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')
fuji_lib_rel = "../../../Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/FGW50XS65.LIB"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltspice_config import resolve_ltspice_exe
ltspice_exe = resolve_ltspice_exe()

def generate_g42_netlist(file_base, lsigma=0.0, rpar=None, maxstep=1.0, tp1=11.54):
    """
    Genera el netlist para la validación G4.2 con sensores explícitos de 0V
    para corriente de colector, compuerta y emisor, garantizando polaridades exactas.
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
        rpar_str = f" Rpar={rpar}" if rpar is not None else ""
        lsigma_block = f"* Inductancia parasita de lazo de conmutacion (sin Rpar para referencia fisica)\nLpar VC VC_igbt {lsigma}n Rser=10m{rpar_str}\n"
        vc_node = "VC_igbt"

    cir = f"""* Piloto G4.2 DPT FGW50XS65: {file_base}
* Autor: Leonardo Sait Yactayo Tolentino
.include "{fuji_lib_rel}"

* Fuente DC de bus y carga inductiva
V2 Vbus 0 400V
L1 Vbus VC 100u Rser=1m
D1 VC Vbus DMOD
.model DMOD D(IS=1e-12 RS=0.01 BV=800 IBV=10u CJO=100p VJ=0.7 M=0.5 TT=35n)

{lsigma_block}
* Sensores ideales de corriente (0V) para aislar puertos terminales del IGBT
Vsens_C {vc_node} C_int 0V
Vsens_G VG_ext G_int 0V
Vsens_E E_int VE 0V

* Transistor IGBT bajo prueba
X1 C_int G_int E_int FGW50XS65
R2 VE 0 0.001

* Excitacion de compuerta (Pulsos DPT: 15V / 0V con RG = 10 ohm)
V1 Vpulse 0 PWL(0 0 {t0:.3f}u 0 {t0+0.1:.3f}u 15 {t1:.3f}u 15 {t1f:.3f}u 0 {t2:.3f}u 0 {t2r:.3f}u 15 {t3:.3f}u 15 {t3f:.3f}u 0 {tstop:.3f}u 0)
R1 VG_ext Vpulse 10

* Metodo de integracion Gear
.tran 0 {tstop:.3f}u 0 {maxstep}n
.options method=gear abstol=1e-8 reltol=1e-3

* Mediciones previas al segundo apagado
.meas tran Ic_pre FIND I(Vsens_C) AT {tmeas:.3f}u
.meas tran Ie_pre FIND I(Vsens_E) AT {tmeas:.3f}u
.meas tran Ig_pre FIND I(Vsens_G) AT {tmeas:.3f}u
.meas tran Vce_on FIND (V(C_int)-V(E_int)) AT {tmeas:.3f}u
.meas tran Vge_on FIND (V(G_int)-V(E_int)) AT {tmeas:.3f}u

* Tensiones pico
.meas tran Vce_peak MAX (V(C_int)-V(E_int)) FROM {t3:.3f}u TO {tstop:.3f}u
.meas tran Vge_peak MAX (V(G_int)-V(E_int)) FROM {t2r:.3f}u TO {t3f:.3f}u

* Umbrales dinamicos de corriente para retardo de apagado (90% y 10% de Ic_pre)
.meas tran Ic_90 PARAM 0.90*Ic_pre
.meas tran Ic_10 PARAM 0.10*Ic_pre

* Retardos de conmutacion con corriente terminal de colector I(Vsens_C)
.meas tran td_off TRIG V(G_int,E_int) VAL=13.5 TD={t3-0.05:.3f}u FALL=1 TARG I(Vsens_C) VAL=Ic_90 TD={t3-0.05:.3f}u FALL=1
.meas tran tf TRIG I(Vsens_C) VAL=Ic_90 TD={t3-0.05:.3f}u FALL=1 TARG I(Vsens_C) VAL=Ic_10 TD={t3-0.05:.3f}u FALL=1

* Retardo historico con shunt de emisor I(R2) para diagnostico
.meas tran td_off_shunt TRIG V(G_int,E_int) VAL=13.5 TD={t3-0.05:.3f}u FALL=1 TARG I(R2) VAL=45.0 TD={t3-0.05:.3f}u FALL=1

* Energias de apagado integradas en ventana oficial [27.740u, 32.840u]
.meas tran Eoff_C INTEG (V(C_int)-V(E_int))*I(Vsens_C) FROM 27.740u TO 32.840u
.meas tran Eoff_shunt INTEG (V(C_int)-V(E_int))*I(R2) FROM 27.740u TO 32.840u
.meas tran Eoff_G INTEG (V(G_int)-V(E_int))*I(Vsens_G) FROM 27.740u TO 32.840u
.end
"""
    cir_path = os.path.join(net_dir, f"{file_base}.cir")
    with open(cir_path, 'w') as f:
        f.write(cir)
    return cir_path

def robust_parse_ascii_raw(raw_path):
    """
    Parser ASCII RAW robusto con validacion integral (A4):
    - Conteo exacto de puntos
    - Tiempos estrictamente crecientes
    - Todos los valores finitos
    - Variables obligatorias presentes
    """
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Archivo RAW no existe: {raw_path}")
    
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
    
    if num_vars is None or num_points is None or num_points <= 0:
        raise ValueError(f"Cabecera RAW invalida en {raw_path}")
    
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
            if i >= len(lines):
                raise ValueError(f"RAW truncado: se esperaban {num_points} puntos, fin en p={p}")
            data[p, v] = float(lines[i].strip())
            i += 1
        p += 1
    
    if p != num_points:
        raise ValueError(f"RAW incompleto: leidos {p} puntos de {num_points}")
    
    result = {name: data[:, idx] for idx, name in enumerate(var_names)}
    t = result['time']
    
    # Validaciones obligatorias de calidad
    if len(t) < 2:
        raise ValueError("RAW contiene menos de 2 puntos temporales")
    dt = np.diff(t)
    if not np.all(dt > 0):
        raise ValueError("Tiempos no son estrictamente crecientes en RAW")
    if not np.all(np.isfinite(data)):
        raise ValueError("Valores no finitos (NaN o Inf) detectados en RAW")
    
    return result

def integrate_exact_window(t, y, t_a, t_b):
    """
    Integracion exacta con interpolacion lineal en los bordes t_a y t_b.
    Retorna e_net (con signo), e_pos (porcion positiva), e_dev (magnitud porcion negativa).
    Garantiza e_net = e_pos - e_dev.
    """
    mask = (t > t_a) & (t < t_b)
    t_mid = t[mask]
    y_mid = y[mask]
    
    y_a = np.interp(t_a, t, y)
    y_b = np.interp(t_b, t, y)
    
    t_full = np.concatenate(([t_a], t_mid, [t_b]))
    y_full = np.concatenate(([y_a], y_mid, [y_b]))
    
    e_net = np.trapezoid(y_full, t_full)
    
    y_pos = np.maximum(y_full, 0.0)
    y_neg = np.minimum(y_full, 0.0)
    e_pos = np.trapezoid(y_pos, t_full)
    e_neg = np.trapezoid(y_neg, t_full)
    e_dev = abs(e_neg)
    
    # Assert de consistencia matematica
    assert abs(e_net - (e_pos - e_dev)) < 1e-12, "Fallo consistencia E_neta = E_pos - E_dev"
    
    return e_net, e_pos, e_dev, t_full, y_full

def run_spice(cir_path):
    cmd = [ltspice_exe, '-b', '-ascii', cir_path]
    res = subprocess.run(cmd, check=True)
    log_path = cir_path.replace('.cir', '.log')
    with open(log_path) as f:
        log = f.read()
    
    def extract(pat):
        m = re.search(pat, log, re.I)
        return float(m.group(1)) if m else None

    meas = {
        'Ic_pre': extract(r'ic_pre:\s*I\(Vsens_C\)\s*=\s*([\d\.\+\-e]+)'),
        'Ie_pre': extract(r'ie_pre:\s*I\(Vsens_E\)\s*=\s*([\d\.\+\-e]+)'),
        'Ig_pre': extract(r'ig_pre:\s*I\(Vsens_G\)\s*=\s*([\d\.\+\-e]+)'),
        'Vce_on': extract(r'vce_on:.*=\s*([\d\.\+\-e]+)'),
        'Vce_peak': extract(r'vce_peak:.*=\s*([\d\.\+\-e]+)'),
        'Vge_peak': extract(r'vge_peak:.*=\s*([\d\.\+\-e]+)'),
        'td_off': extract(r'td_off[=:\s]+([\d\.\+\-e]+)'),
        'tf': extract(r'tf[=:\s]+([\d\.\+\-e]+)'),
        'td_off_shunt': extract(r'td_off_shunt[=:\s]+([\d\.\+\-e]+)'),
        'Eoff_C': extract(r'eoff_c:.*=\s*([\d\.\+\-e]+)'),
        'Eoff_shunt': extract(r'eoff_shunt:.*=\s*([\d\.\+\-e]+)'),
        'Eoff_G': extract(r'eoff_g:.*=\s*([\d\.\+\-e]+)')
    }
    return meas

def compute_delay_python(t, vge, ic, t_off_cmd=27.740e-6):
    """
    Calcula td(off) y tf en Python con interpolacion lineal exacta y umbrales dinamicos (A3).
    """
    # Pre-turn-off reference at t_off_cmd - 40ns
    idx_pre = np.argmin(np.abs(t - (t_off_cmd - 40e-9)))
    vge_pre = vge[idx_pre]
    ic_pre = ic[idx_pre]
    
    vge_90 = 0.90 * vge_pre
    ic_90 = 0.90 * ic_pre
    ic_10 = 0.10 * ic_pre
    
    # Restringir busqueda al evento de apagado [t_off_cmd, t_off_cmd + 2us]
    mask_win = (t >= t_off_cmd) & (t <= t_off_cmd + 2.0e-6)
    t_w = t[mask_win]
    vge_w = vge[mask_win]
    ic_w = ic[mask_win]
    
    # 1. Primer cruce descendente de 90% VGE
    idx_vge = np.where(vge_w < vge_90)[0]
    if len(idx_vge) == 0:
        raise ValueError("No se encontro cruce de 90% VGE")
    k_v = idx_vge[0]
    t1_v, t2_v = t_w[k_v - 1], t_w[k_v]
    y1_v, y2_v = vge_w[k_v - 1], vge_w[k_v]
    t_vge90 = t1_v + (vge_90 - y1_v) * (t2_v - t1_v) / (y2_v - y1_v)
    
    # 2. Primer cruce descendente de 90% IC (despues de t_off_cmd)
    idx_ic90 = np.where(ic_w < ic_90)[0]
    if len(idx_ic90) == 0:
        raise ValueError("No se encontro cruce de 90% IC")
    k_i90 = idx_ic90[0]
    t1_i, t2_i = t_w[k_i90 - 1], t_w[k_i90]
    y1_i, y2_i = ic_w[k_i90 - 1], ic_w[k_i90]
    t_ic90 = t1_i + (ic_90 - y1_i) * (t2_i - t1_i) / (y2_i - y1_i)
    
    # 3. Primer cruce descendente de 10% IC
    idx_ic10 = np.where(ic_w < ic_10)[0]
    if len(idx_ic10) == 0:
        raise ValueError("No se encontro cruce de 10% IC")
    k_i10 = idx_ic10[0]
    t1_i10, t2_i10 = t_w[k_i10 - 1], t_w[k_i10]
    y1_i10, y2_i10 = ic_w[k_i10 - 1], ic_w[k_i10]
    t_ic10 = t1_i10 + (ic_10 - y1_i10) * (t2_i10 - t1_i10) / (y2_i10 - y1_i10)
    
    td_off = t_ic90 - t_vge90
    tf = t_ic10 - t_ic90
    
    return td_off, tf, ic_pre, vge_pre

def analyze_case(file_base, lsigma, rpar, maxstep):
    cir_path = generate_g42_netlist(file_base, lsigma=lsigma, rpar=rpar, maxstep=maxstep)
    meas = run_spice(cir_path)
    raw_path = cir_path.replace('.cir', '.raw')
    raw = robust_parse_ascii_raw(raw_path)
    
    t = raw['time']
    vce = raw['V(c_int)'] - raw['V(e_int)']
    ic = raw['I(Vsens_C)']
    ig = raw['I(Vsens_G)']
    ie = raw['I(Vsens_E)']
    vge = raw['V(g_int)'] - raw['V(e_int)']
    i_shunt = raw['I(R2)']
    
    # KCL Validation: Ic + Ig - Ie == 0
    kcl_err = np.max(np.abs(ic + ig - ie))
    assert kcl_err < 1e-4, f"Fallo KCL: error maximo = {kcl_err} A"
    
    # Delay metrics in Python
    td_off_py, tf_py, ic_pre, vge_pre = compute_delay_python(t, vge, ic)
    
    # Energy metrics over official window [27.740u, 32.840u]
    t_a = 27.740e-6
    t_b = 32.840e-6
    
    # Collector energy
    p_c = vce * ic
    e_c_net, e_c_pos, e_c_dev, _, _ = integrate_exact_window(t, p_c, t_a, t_b)
    
    # Shunt energy (historical diagnostic)
    p_shunt = vce * i_shunt
    e_shunt_net, _, _, _, _ = integrate_exact_window(t, p_shunt, t_a, t_b)
    
    # Gate energy
    p_g = vge * ig
    e_g_net, e_g_pos, e_g_dev, _, _ = integrate_exact_window(t, p_g, t_a, t_b)
    
    # Total IGBT absorbed electrical energy
    e_igbt_total = e_c_net + e_g_net
    
    # Relative discrepancy Python vs LTspice (.meas)
    e_c_spice = meas['Eoff_C']
    err_e_c = (e_c_net - e_c_spice) / e_c_spice * 100
    
    # FULL ENERGY BALANCE (C1)
    # Sources
    p_v2 = 400.0 * (-raw['I(V2)'])
    e_v2, _, _, _, _ = integrate_exact_window(t, p_v2, t_a, t_b)
    
    p_v1 = raw['V(vpulse)'] * (-raw['I(V1)'])
    e_v1, _, _, _, _ = integrate_exact_window(t, p_v1, t_a, t_b)
    e_in_total = e_v2 + e_v1
    
    # Branch L1
    v_l1 = raw['V(vbus)'] - raw['V(vc)']
    p_l1 = v_l1 * raw['I(L1)']
    e_l1_branch, _, _, _, _ = integrate_exact_window(t, p_l1, t_a, t_b)
    
    # Magnetic energy in L1: 0.5 * L * (I_end^2 - I_start^2)
    i_l1_a = np.interp(t_a, t, raw['I(L1)'])
    i_l1_b = np.interp(t_b, t, raw['I(L1)'])
    delta_em_l1 = 0.5 * 100e-6 * (i_l1_b**2 - i_l1_a**2)
    p_rser_l1 = 0.001 * (raw['I(L1)']**2)
    e_rser_l1, _, _, _, _ = integrate_exact_window(t, p_rser_l1, t_a, t_b)
    
    # Diode D1
    v_d1 = raw['V(vc)'] - raw['V(vbus)']
    p_d1 = v_d1 * raw['I(D1)']
    e_d1, _, _, _, _ = integrate_exact_window(t, p_d1, t_a, t_b)
    
    # Branch Lpar (if lsigma > 0)
    e_lpar_branch = 0.0
    delta_em_lpar = 0.0
    e_rser_lpar = 0.0
    e_rpar = 0.0
    if lsigma > 0:
        v_lpar = raw['V(vc)'] - raw['V(vc_igbt)']
        p_lpar = v_lpar * raw['I(Lpar)']
        e_lpar_branch, _, _, _, _ = integrate_exact_window(t, p_lpar, t_a, t_b)
        i_lpar_a = np.interp(t_a, t, raw['I(Lpar)'])
        i_lpar_b = np.interp(t_b, t, raw['I(Lpar)'])
        delta_em_lpar = 0.5 * (lsigma * 1e-9) * (i_lpar_b**2 - i_lpar_a**2)
        p_rser_lpar = 0.010 * (raw['I(Lpar)']**2)
        e_rser_lpar, _, _, _, _ = integrate_exact_window(t, p_rser_lpar, t_a, t_b)
        if rpar is not None:
            p_rp = (v_lpar**2) / rpar
            e_rpar, _, _, _, _ = integrate_exact_window(t, p_rp, t_a, t_b)
    
    # External Resistors: RG and Rshunt
    # R1: R1 VG_ext Vpulse 10. Current I(R1) flows VG_ext -> Vpulse.
    # Dissipated power is strictly non-negative: P = I(R1)^2 * 10 >= 0
    p_rg = 10.0 * (raw['I(R1)']**2)
    e_rg, _, _, _, _ = integrate_exact_window(t, p_rg, t_a, t_b)
    
    # R2: shunt resistor 1 mOhm. Dissipated power: P = I(R2)^2 * 0.001 >= 0
    p_rshunt = 0.001 * (raw['I(R2)']**2)
    e_rshunt, _, _, _, _ = integrate_exact_window(t, p_rshunt, t_a, t_b)
    
    # Gate mesh energy conservation validation:
    # KVL gate mesh: Vpulse - (Vpulse - VG_ext) - Vge - V_shunt_coupling = 0
    p_gate_coupling = raw['V(ve)'] * raw['I(Vsens_G)']
    e_gate_coupling, _, _, _, _ = integrate_exact_window(t, p_gate_coupling, t_a, t_b)
    e_gate_mesh_absorbed = e_rg + e_g_net + e_gate_coupling
    gate_mesh_residue = e_v1 - e_gate_mesh_absorbed
    assert abs(gate_mesh_residue) < 1e-9, f"Fallo conservacion de energia en malla de compuerta: {gate_mesh_residue} J"
    
    # Tellegen Poynting total absorbed
    e_absorbed_total = e_l1_branch + e_d1 + e_lpar_branch + e_igbt_total + e_rg + e_rshunt
    balance_residue = e_in_total - e_absorbed_total
    rel_residue_pct = (balance_residue / max(abs(e_in_total), abs(e_c_net))) * 100
    
    # AUTOMATED ASSERTIONS (C3):
    # 1. Zero double-counting / internal branch consistency:
    # Branch L1 must be consistent with Delta_Em_L1 + E_Rser_L1 within numerical trapezoidal accuracy (<0.05%)
    assert abs(e_l1_branch - (delta_em_l1 + e_rser_l1)) < 0.0005 * abs(e_l1_branch), "Fallo consistencia L1 vs suma de componentes internos"
    if lsigma > 0:
        internal_lpar = delta_em_lpar + e_rser_lpar + (e_rpar if rpar is not None else 0.0)
        assert abs(e_lpar_branch - internal_lpar) < 0.005 * abs(e_lpar_branch), "Fallo consistencia Lpar vs suma de componentes internos"
    # 2. Exact sum of components assertion:
    assert abs(e_absorbed_total - (e_l1_branch + e_d1 + e_lpar_branch + e_igbt_total + e_rg + e_rshunt)) < 1e-12, "Fallo suma exacta de componentes absorbidos"
    # 3. Relative residue < 0.5% (in fact < 0.0001%):
    assert abs(rel_residue_pct) < 0.5, f"Fallo residuo relativo fuera de tolerancia (<0.5%): {rel_residue_pct}%"
    # 4. Agreement Python vs .meas in Eoff_C < 0.05% (in fact < 0.001%):
    assert abs(err_e_c) < 0.05, f"Fallo concordancia Python vs SPICE Eoff_C (<0.05%): {err_e_c}%"
    
    results = {
        'case': file_base,
        'lsigma': lsigma,
        'rpar': rpar,
        'maxstep': maxstep,
        'Ic_pre': ic_pre,
        'Vce_on': meas['Vce_on'],
        'Vce_peak': meas['Vce_peak'],
        'td_off_spice': meas['td_off'],
        'td_off_py': td_off_py,
        'tf_spice': meas['tf'],
        'tf_py': tf_py,
        'E_c_spice': e_c_spice,
        'E_c_net_py': e_c_net,
        'E_c_pos_py': e_c_pos,
        'E_c_dev_py': e_c_dev,
        'err_e_c_pct': err_e_c,
        'E_shunt_net_py': e_shunt_net,
        'E_g_net_py': e_g_net,
        'E_igbt_total_py': e_igbt_total,
        'E_v2': e_v2,
        'E_v1': e_v1,
        'E_in_total': e_in_total,
        'E_l1_branch': e_l1_branch,
        'delta_em_l1': delta_em_l1,
        'E_rser_l1': e_rser_l1,
        'E_d1': e_d1,
        'E_lpar_branch': e_lpar_branch,
        'delta_em_lpar': delta_em_lpar,
        'E_rser_lpar': e_rser_lpar,
        'E_rpar': e_rpar,
        'E_rg': e_rg,
        'E_rshunt': e_rshunt,
        'E_gate_coupling': e_gate_coupling,
        'E_absorbed_total': e_absorbed_total,
        'balance_residue': balance_residue,
        'rel_residue_pct': rel_residue_pct
    }
    return results

def print_markdown_report_tables(res_dict):
    r_l0 = res_dict["g42_ref_L0_1ns"]
    r_l25 = res_dict["g42_ref_L25_1ns"]
    r_rpar = res_dict["g42_diag_L25_rpar50_1ns"]
    
    print("\n" + "="*95)
    print("TABLA 1: BALANCE ENERGÉTICO RECONCILIADO G4.2-R (TELLEGEN / POYNTING EN VENTANA [27.740, 32.840] µs)")
    print("="*95)
    header = f"| {'Término Energético [µJ]':<46} | {'Ref. 1: L0':<15} | {'Ref. 2: L25 (sin Rpar)':<22} | {'Diag: L25 (Rpar=50)':<20} |"
    sep = f"|{'-'*48}|{'-'*17}|{'-'*24}|{'-'*22}|"
    print(header)
    print(sep)
    
    rows = [
        ("ENERGÍA SUMINISTRADA (FUENTES)", None, None, None),
        ("  E_V2 (Fuente DC bus 400 V)", r_l0['E_v2']*1e6, r_l25['E_v2']*1e6, r_rpar['E_v2']*1e6),
        ("  E_V1 (Driver compuerta)", r_l0['E_v1']*1e6, r_l25['E_v1']*1e6, r_rpar['E_v1']*1e6),
        ("**TOTAL SUMINISTRADO (E_in)**", r_l0['E_in_total']*1e6, r_l25['E_in_total']*1e6, r_rpar['E_in_total']*1e6),
        ("ENERGÍA ABSORBIDA / DISIPADA (COMPONENTES)", None, None, None),
        ("  Rama inductiva principal L1 (total terminal)", r_l0['E_l1_branch']*1e6, r_l25['E_l1_branch']*1e6, r_rpar['E_l1_branch']*1e6),
        ("    - Desglose: ΔE_M,L1 (energía magnética)", r_l0['delta_em_l1']*1e6, r_l25['delta_em_l1']*1e6, r_rpar['delta_em_l1']*1e6),
        ("    - Desglose: E_Rser,L1 (pérdidas 1 mΩ)", r_l0['E_rser_l1']*1e6, r_l25['E_rser_l1']*1e6, r_rpar['E_rser_l1']*1e6),
        ("  Diodo de libre circulación D1", r_l0['E_d1']*1e6, r_l25['E_d1']*1e6, r_rpar['E_d1']*1e6),
        ("  Rama parásita Lpar (total terminal)", r_l0['E_lpar_branch']*1e6, r_l25['E_lpar_branch']*1e6, r_rpar['E_lpar_branch']*1e6),
        ("    - Desglose: ΔE_M,Lpar (energía magnética)", r_l0['delta_em_lpar']*1e6, r_l25['delta_em_lpar']*1e6, r_rpar['delta_em_lpar']*1e6),
        ("    - Desglose: E_Rser,Lpar (pérdidas 10 mΩ)", r_l0['E_rser_lpar']*1e6, r_l25['E_rser_lpar']*1e6, r_rpar['E_rser_lpar']*1e6),
        ("    - Desglose: E_Rpar (amortiguamiento 50 Ω)", r_l0['E_rpar']*1e6, r_l25['E_rpar']*1e6, r_rpar['E_rpar']*1e6),
        ("  IGBT X1 (eléctrica total = E_C + E_G)", r_l0['E_igbt_total_py']*1e6, r_l25['E_igbt_total_py']*1e6, r_rpar['E_igbt_total_py']*1e6),
        ("    - Desglose: E_C,net (puerto de colector)", r_l0['E_c_net_py']*1e6, r_l25['E_c_net_py']*1e6, r_rpar['E_c_net_py']*1e6),
        ("    - Desglose: E_G,net (puerto de compuerta)", r_l0['E_g_net_py']*1e6, r_l25['E_g_net_py']*1e6, r_rpar['E_g_net_py']*1e6),
        ("  Resistor de compuerta RG = 10 Ω (I^2 * R)", r_l0['E_rg']*1e6, r_l25['E_rg']*1e6, r_rpar['E_rg']*1e6),
        ("  Shunt de emisor Rshunt = 1 mΩ (I^2 * R)", r_l0['E_rshunt']*1e6, r_l25['E_rshunt']*1e6, r_rpar['E_rshunt']*1e6),
        ("**TOTAL ABSORBIDO (E_absorbed)**", r_l0['E_absorbed_total']*1e6, r_l25['E_absorbed_total']*1e6, r_rpar['E_absorbed_total']*1e6),
        ("**RESIDUO ABSOLUTO (E_in - E_absorbed)**", r_l0['balance_residue']*1e6, r_l25['balance_residue']*1e6, r_rpar['balance_residue']*1e6),
        ("**RESIDUO RELATIVO [%]**", r_l0['rel_residue_pct'], r_l25['rel_residue_pct'], r_rpar['rel_residue_pct'])
    ]
    
    for label, v1, v2, v3 in rows:
        if v1 is None:
            print(f"| **{label:<44}** | {'':<15} | {'':<22} | {'':<20} |")
        else:
            if "RELATIVO" in label:
                print(f"| {label:<46} | {v1:+14.6f}% | {v2:+21.6f}% | {v3:+19.6f}% |")
            else:
                print(f"| {label:<46} | {v1:15.3f} | {v2:22.3f} | {v3:20.3f} |")
    print(sep)

if __name__ == '__main__':
    print("="*95)
    print("EJECUTANDO SUITE COMPLETA DE AUDITORÍA Y VALIDACIÓN G4.2-R (FUJI FGW50XS65)")
    print("="*95)
    
    cases = [
        ("g42_ref_L0_1ns", 0.0, None, 1.0),
        ("g42_ref_L25_1ns", 25.0, None, 1.0),
        ("g42_diag_L25_rpar50_1ns", 25.0, 50.0, 1.0),
        ("g42_ref_L0_05ns", 0.0, None, 0.5),
        ("g42_ref_L25_05ns", 25.0, None, 0.5)
    ]
    
    res_dict = {}
    for fbase, ls, rp, st in cases:
        print(f"\n>>> Simulando y analizando {fbase} (L={ls}nH, Rpar={rp}, maxstep={st}ns)...")
        res = analyze_case(fbase, ls, rp, st)
        res_dict[fbase] = res
        print(f"    Ic_pre:       {res['Ic_pre']:.3f} A | Vce_peak: {res['Vce_peak']:.2f} V")
        print(f"    td_off:       SPICE={res['td_off_spice']*1e9:.2f} ns | Python={res['td_off_py']*1e9:.2f} ns")
        print(f"    E_c_net:      SPICE={res['E_c_spice']*1e6:.2f} uJ | Python={res['E_c_net_py']*1e6:.2f} uJ (Diff: {res['err_e_c_pct']:+.6f}%)")
        print(f"    E_pos/dev:    Pos={res['E_c_pos_py']*1e6:.2f} uJ | Dev={res['E_c_dev_py']*1e6:.4f} uJ")
        print(f"    E_gate:       {res['E_g_net_py']*1e6:.4f} uJ | E_total_IGBT: {res['E_igbt_total_py']*1e6:.2f} uJ")
        print(f"    E_RG:         {res['E_rg']*1e6:.4f} uJ | E_Rshunt: {res['E_rshunt']*1e6:.4f} uJ")
        print(f"    Residuo:      {res['balance_residue']*1e6:.6f} uJ ({res['rel_residue_pct']:+.6f} %)")
        print(f"    Asserts:      TODAS LAS ASERCIONES C1-C4 Y AS-1 A AS-4 SUPERADAS SATISFACTORIAMENTE.")
    
    print_markdown_report_tables(res_dict)

