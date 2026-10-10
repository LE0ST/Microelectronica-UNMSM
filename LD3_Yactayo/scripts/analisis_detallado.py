import os
import subprocess
import numpy as np

# Import raw parser
from parse_raw import parse_ltspice_ascii_raw

def analyze_device(raw_path, device_type='N', t_off_start=19.85e-6, t_off_end=25.0e-6):
    data = parse_ltspice_ascii_raw(raw_path)
    time = data['time']
    
    # Sign conventions
    if device_type == 'N':
        vge = data['V(vg)'] - data['V(ve)']
        vce = data['V(vc)'] - data['V(ve)']
        ic = data['I(R2)']
    else:
        # P-IGBT: V_GE = V(VG)-V(VE) is negative; V_EC = V(VE)-V(VC) > 0; |I_C| = -I(R2)
        vge = data['V(vg)'] - data['V(ve)']
        vce = data['V(ve)'] - data['V(vc)']  # positive V_EC
        ic = -data['I(R2)']                  # positive magnitude

    # Conduction values right before turn-off (e.g. 50ns before t_off_start)
    idx_before = np.argmin(np.abs(time - (t_off_start - 50e-9)))
    ic_on = ic[idx_before]
    vce_on = vce[idx_before]
    vge_on = vge[idx_before]

    # Select turn-off window
    mask_off = (time >= t_off_start) & (time <= t_off_end)
    t_win = time[mask_off]
    vge_win = vge[mask_off]
    vce_win = vce[mask_off]
    ic_win = ic[mask_off]

    # Vce peak
    vce_peak = np.max(vce_win)
    idx_vce_peak = np.argmax(vce_win)
    t_vce_peak = t_win[idx_vce_peak]

    # 90% VGE threshold
    if device_type == 'N':
        vge_th90 = 0.90 * 15.0  # 13.5V
        idx_vge90 = np.where((t_win >= t_off_start) & (vge_win <= vge_th90))[0][0]
    else:
        vge_th90 = -13.5
        idx_vge90 = np.where((t_win >= t_off_start) & (vge_win >= vge_th90))[0][0]
    t_vge90 = t_win[idx_vge90]

    # 90% IC threshold
    ic_th90 = 0.90 * ic_on
    idx_ic90 = np.where((t_win >= t_vge90) & (ic_win <= ic_th90))[0][0]
    t_ic90 = t_win[idx_ic90]

    td_off = t_ic90 - t_vge90

    # 10% IC threshold
    ic_th10 = 0.10 * ic_on
    idx_ic10 = np.where((t_win >= t_ic90) & (ic_win <= ic_th10))[0][0]
    t_ic10 = t_win[idx_ic10]

    tf = t_ic10 - t_ic90
    t_off = td_off + tf

    # Tail current identification via derivative
    dt = np.diff(t_win)
    dic = np.diff(ic_win)
    dic_dt = dic / dt
    t_mid = 0.5 * (t_win[:-1] + t_win[1:])

    mask_slope = (t_mid >= t_ic90) & (t_mid <= t_off_start + 1.5e-6)
    max_neg_slope = np.min(dic_dt[mask_slope])
    idx_min_slope = np.argmin(dic_dt[mask_slope])
    t_steepest = t_mid[mask_slope][idx_min_slope]
    
    mask_after_steep = mask_slope & (t_mid > t_steepest)
    knee_candidates = np.where(dic_dt[mask_after_steep] >= 0.05 * max_neg_slope)[0]
    if len(knee_candidates) > 0:
        idx_knee = np.where(mask_after_steep)[0][knee_candidates[0]]
        t_tail = t_mid[idx_knee]
        ic_tail = np.interp(t_tail, t_win, ic_win)
    else:
        t_tail = t_ic10
        ic_tail = ic_th10

    # Switching Power & Energy
    p_inst = vce_win * ic_win
    e_off_total = np.trapezoid(p_inst, t_win)

    mask_tail = t_win >= t_tail
    e_tail = np.trapezoid(p_inst[mask_tail], t_win[mask_tail])
    pct_e_tail = (e_tail / e_off_total) * 100.0

    return {
        'device': device_type,
        'ic_on': ic_on,
        'vce_on': vce_on,
        'vge_on': vge_on,
        'vce_peak': vce_peak,
        't_vce_peak': t_vce_peak,
        't_vge90': t_vge90,
        't_ic90': t_ic90,
        'td_off': td_off,
        't_ic10': t_ic10,
        'tf': tf,
        't_off': t_off,
        't_tail': t_tail,
        'ic_tail': ic_tail,
        'e_off_total': e_off_total,
        'e_tail': e_tail,
        'pct_e_tail': pct_e_tail,
        'time_full': time,
        'vge_full': vge,
        'vce_full': vce,
        'ic_full': ic,
        't_win': t_win,
        'vge_win': vge_win,
        'vce_win': vce_win,
        'ic_win': ic_win,
        'p_inst': p_inst
    }

if __name__ == '__main__':
    # 1. Asegurar simulacion con -ascii para los 4 circuitos
    net_dir = 'LD3_Yactayo/simulaciones/netlists'
    for cir in ['dpt_nigbt_nom.cir', 'dpt_pigbt_nom.cir', 'dpt_nigbt.cir', 'dpt_pigbt.cir']:
        p = os.path.join(net_dir, cir)
        print(f"Ejecutando {cir} (-ascii)...")
        subprocess.run(['G:\\LTspice\\LTspice.exe', '-b', '-ascii', p], timeout=60)

    res_n_nom = analyze_device(os.path.join(net_dir, 'dpt_nigbt_nom.raw'), 'N', 19.85e-6, 25.0e-6)
    res_p_nom = analyze_device(os.path.join(net_dir, 'dpt_pigbt_nom.raw'), 'P', 25.08e-6, 30.0e-6)
    res_n_80  = analyze_device(os.path.join(net_dir, 'dpt_nigbt.raw'), 'N', 36.0e-6, 45.0e-6)
    res_p_80  = analyze_device(os.path.join(net_dir, 'dpt_pigbt.raw'), 'P', 36.0e-6, 45.0e-6)

    cases = [
        ('N-IGBT Nominal (19A)', res_n_nom),
        ('N-IGBT Sobrecarga (80A)', res_n_80),
        ('P-IGBT Nominal (40A)', res_p_nom),
        ('P-IGBT Sobrecarga (80A)', res_p_80),
    ]

    print("\n" + "="*95)
    print(f"{'CASO':<26} | {'Ic_on [A]':<9} | {'Vce_on [V]':<10} | {'td_off [ns]':<11} | {'tf [ns]':<9} | {'Eoff [uJ]':<9} | {'E_tail [%]':<9}")
    print("="*95)
    for name, r in cases:
        print(f"{name:<26} | {r['ic_on']:<9.2f} | {r['vce_on']:<10.2f} | {r['td_off']*1e9:<11.1f} | {r['tf']*1e9:<9.1f} | {r['e_off_total']*1e6:<9.1f} | {r['pct_e_tail']:<9.2f}")
    print("="*95)
