import os
import subprocess
import numpy as np

# Script de QA Científico G3.1 para LD3
# Autor: Leonardo Sait Yactayo Tolentino

from parse_raw import parse_ltspice_ascii_raw

def analyze_sensitivity(raw_path, device_type='N', t_off_start=19.85e-6, t_off_end=25.0e-6):
    data = parse_ltspice_ascii_raw(raw_path)
    time = data['time']
    
    if device_type == 'N':
        vge = data['V(vg)'] - data['V(ve)']
        vce = data['V(vc)'] - data['V(ve)']
        ic = data['I(R2)']
    else:
        vge = data['V(vg)'] - data['V(ve)']
        vce = data['V(ve)'] - data['V(vc)']
        ic = -data['I(R2)']

    idx_before = np.argmin(np.abs(time - (t_off_start - 50e-9)))
    ic_on = ic[idx_before]
    vce_on = vce[idx_before]

    mask_off = (time >= t_off_start) & (time <= t_off_end)
    t_win = time[mask_off]
    vge_win = vge[mask_off]
    vce_win = vce[mask_off]
    ic_win = ic[mask_off]

    if device_type == 'N':
        idx_vge90 = np.where((t_win >= t_off_start) & (vge_win <= 13.5))[0][0]
    else:
        idx_vge90 = np.where((t_win >= t_off_start) & (vge_win >= -13.5))[0][0]
    t_vge90 = t_win[idx_vge90]

    idx_ic90 = np.where((t_win >= t_vge90) & (ic_win <= 0.90 * ic_on))[0][0]
    t_ic90 = t_win[idx_ic90]
    td_off = t_ic90 - t_vge90

    idx_ic10 = np.where((t_win >= t_ic90) & (ic_win <= 0.10 * ic_on))[0][0]
    t_ic10 = t_win[idx_ic10]
    tf = t_ic10 - t_ic90

    # Potencia instantánea
    p_inst = vce_win * ic_win

    # Ventanas alternativas de Eoff:
    # 1. Ventana A (completa desde flanco de pulso t_off_start hasta t_off_end)
    e_off_A = np.trapezoid(p_inst, t_win)

    # 2. Ventana B (desde 90% VGE hasta final)
    mask_B = t_win >= t_vge90
    e_off_B = np.trapezoid(p_inst[mask_B], t_win[mask_B])

    # 3. Ventana C (estándar IEC: desde Vce = 10% Vbus = 40V hasta Ic = 2% Ic_on)
    idx_vce10 = np.where((t_win >= t_off_start) & (vce_win >= 40.0))[0]
    idx_ic02 = np.where((t_win >= t_ic10) & (ic_win <= 0.02 * ic_on))[0]
    if len(idx_vce10) > 0 and len(idx_ic02) > 0:
        t_start_C = t_win[idx_vce10[0]]
        t_end_C = t_win[idx_ic02[0]]
        mask_C = (t_win >= t_start_C) & (t_win <= t_end_C)
        e_off_C = np.trapezoid(p_inst[mask_C], t_win[mask_C])
    else:
        e_off_C = e_off_B

    # Analisis de sensibilidad de cola (3%, 5%, 10% de max pendiente)
    dt = np.diff(t_win)
    dic = np.diff(ic_win)
    dic_dt = dic / dt
    t_mid = 0.5 * (t_win[:-1] + t_win[1:])

    mask_slope = (t_mid >= t_ic90) & (t_mid <= t_off_start + 1.5e-6)
    max_neg_slope = np.min(dic_dt[mask_slope])
    idx_min_slope = np.argmin(dic_dt[mask_slope])
    t_steepest = t_mid[mask_slope][idx_min_slope]
    mask_after_steep = mask_slope & (t_mid > t_steepest)

    sensitivity = {}
    for pct in [3, 5, 10]:
        th = (pct / 100.0) * max_neg_slope
        candidates = np.where(dic_dt[mask_after_steep] >= th)[0]
        if len(candidates) > 0:
            idx_k = np.where(mask_after_steep)[0][candidates[0]]
            t_k = t_mid[idx_k]
            ic_k = np.interp(t_k, t_win, ic_win)
        else:
            t_k = t_ic10
            ic_k = 0.10 * ic_on
        
        mask_tail_k = t_win >= t_k
        e_tail_k = np.trapezoid(p_inst[mask_tail_k], t_win[mask_tail_k])
        pct_k = (e_tail_k / e_off_A) * 100.0

        sensitivity[pct] = {
            't_tail': t_k,
            'ic_tail': ic_k,
            'pct_ic_on': (ic_k / ic_on) * 100.0,
            'e_tail': e_tail_k,
            'pct_e_tail': pct_k
        }

    return {
        'ic_on': ic_on,
        'vce_on': vce_on,
        'td_off': td_off,
        'tf': tf,
        't_off': td_off + tf,
        'e_off_A': e_off_A,
        'e_off_B': e_off_B,
        'e_off_C': e_off_C,
        'sensitivity': sensitivity,
        't_win': t_win,
        'vge_win': vge_win,
        'vce_win': vce_win,
        'ic_win': ic_win,
        'p_inst': p_inst
    }

if __name__ == '__main__':
    net_dir = 'LD3_Yactayo/simulaciones/netlists'
    
    # Evaluar N nominal (19A), N sobrecarga (80A), P nominal (40A), P sobrecarga (80A)
    res_n_nom = analyze_sensitivity(os.path.join(net_dir, 'dpt_nigbt_nom.raw'), 'N', 19.85e-6, 25.0e-6)
    res_n_80  = analyze_sensitivity(os.path.join(net_dir, 'dpt_nigbt.raw'), 'N', 36.0e-6, 45.0e-6)
    res_p_nom = analyze_sensitivity(os.path.join(net_dir, 'dpt_pigbt_nom.raw'), 'P', 25.08e-6, 30.0e-6)
    res_p_80  = analyze_sensitivity(os.path.join(net_dir, 'dpt_pigbt.raw'), 'P', 36.0e-6, 45.0e-6)

    print("=========================================================================================")
    print("             SENSIBILIDAD DE LA CORRIENTE Y ENERGIA DE COLA (G3.1)                       ")
    print("=========================================================================================")
    for name, r in [('N-IGBT Nominal (19A)', res_n_nom), 
                    ('P-IGBT Nominal (40A)', res_p_nom),
                    ('N-IGBT Sobrecarga (80A)', res_n_80),
                    ('P-IGBT Sobrecarga (80A)', res_p_80)]:
        print(f"\n--- {name} (Ic_on = {r['ic_on']:.2f} A, Eoff total = {r['e_off_A']*1e6:.1f} uJ) ---")
        print(f"{'Umbral Pendiente':<18} | {'t_tail [us]':<12} | {'I_tail [A]':<11} | {'% de Ic_on':<11} | {'E_tail [uJ]':<12} | {'% E_tail/Eoff':<12}")
        print("-" * 88)
        for pct in [3, 5, 10]:
            s = r['sensitivity'][pct]
            print(f"{pct}% de max |di/dt| | {s['t_tail']*1e6:<12.4f} | {s['ic_tail']:<11.3f} | {s['pct_ic_on']:<11.2f}% | {s['e_tail']*1e6:<12.1f} | {s['pct_e_tail']:<12.2f}%")

    print("\n" + "="*88)
    print("             COMPARACION DE VENTANAS DE INTEGRACION DE Eoff (G3.1)                      ")
    print("="*88)
    print(f"{'Caso':<25} | {'Ventana A (Pulso)':<18} | {'Ventana B (90% VGE)':<20} | {'Ventana C (IEC 10%-2%)':<22}")
    print("-" * 88)
    for name, r in [('N-IGBT Nominal (19A)', res_n_nom), 
                    ('P-IGBT Nominal (40A)', res_p_nom),
                    ('N-IGBT Sobrecarga (80A)', res_n_80),
                    ('P-IGBT Sobrecarga (80A)', res_p_80)]:
        print(f"{name:<25} | {r['e_off_A']*1e6:<15.1f} uJ | {r['e_off_B']*1e6:<17.1f} uJ | {r['e_off_C']*1e6:<19.1f} uJ")
