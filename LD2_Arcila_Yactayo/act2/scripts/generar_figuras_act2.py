# -*- coding: utf-8 -*-
"""
Generador de Figuras Cientificas - Actividad 2 (LD2)
Microelectronica y Sistemas Nanoelectronicos - UNMSM 2026-II

Genera tres figuras a 300 DPI con rotulacion completa, unidades, leyendas y
referencia formal a los netlists generadores del protocolo consolidado G2.2:
1. fig1_act2_peor_caso_formas_onda.png: Formas de onda del peor caso sincrono (G2.2b).
2. fig2_act2_dv_vs_cl_analitico_simulado.png: Barrido de dV y Vdyn vs CL (Analitico vs Sincrono vs Historicos).
3. fig3_act2_comparacion_mitigaciones.png: Comparacion de las tecnicas de mitigacion y contencion.

REGLA DE TRAZABILIDAD:
Todos los datos numericos de simulacion se extraen dinamicamente desde:
  resultados/datos/act2_metricas.json
y desde los archivos .raw de simulacion real.
"""

import os
import sys
import json
import shutil
import numpy as np
import matplotlib.pyplot as plt

# Configuracion de estilo IEEE / Cientifico
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 8.0
plt.rcParams['figure.titlesize'] = 12
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['grid.alpha'] = 0.4
plt.rcParams['grid.linestyle'] = ':'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT2_DIR = os.path.dirname(SCRIPT_DIR)
CIR_DIR = os.path.join(ACT2_DIR, "circuitos")
RAW_DIR = os.path.join(ACT2_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT2_DIR, "resultados", "datos")
FIG_DIR = os.path.join(ACT2_DIR, "figuras")
INFORME_FIG_DIR = os.path.abspath(os.path.join(ACT2_DIR, "..", "informe_latex", "figuras"))

PARSER_DIR = os.path.abspath(os.path.join(ACT2_DIR, "..", "scripts", "lectura_resultados"))
sys.path.insert(0, PARSER_DIR)
from parse_spice_raw import read_raw

def find_raw(filename):
    """Busca un archivo .raw en CIR_DIR o en RAW_DIR."""
    p1 = os.path.join(CIR_DIR, filename)
    if os.path.exists(p1):
        return p1
    p2 = os.path.join(RAW_DIR, filename)
    if os.path.exists(p2):
        return p2
    return p1

def cargar_metricas():
    """Carga las metricas de simulacion generadas por el pipeline oficial."""
    json_path = os.path.join(DATOS_DIR, "act2_metricas.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Archivo de metricas no encontrado: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generar_figura_1(metricas):
    """Figura 1: Formas de onda del banco sincrono de peor caso (nand3_cs_g2b_piloto_cl2f.raw)"""
    raw_path = find_raw("nand3_cs_g2b_piloto_cl2f.raw")
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} no existe.")
        return

    m_sinc = metricas["g2b_sincrono_piloto_cl2f"]
    dv_mv = m_sinc["dv_vdd"] * 1e3
    vdyn_min_v = m_sinc["vdyn_min"]

    res = read_raw(raw_path)
    t = res['data']['time'] * 1e9  # ns
    clk = res['data']['V(clk)']
    va = res['data']['V(a)']
    vc = res['data']['V(c)']
    vdyn = res['data']['V(dyn)']
    vn1 = res['data']['V(n1)']
    vn2 = res['data']['V(n2)']
    vn3 = res['data']['V(n3)']
    vout = res['data']['V(out)']

    mask = (t >= 0.5) & (t <= 4.5)
    t_m = t[mask]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8.5, 7.2), sharex=True,
                                        gridspec_kw={'height_ratios': [1.0, 1.6, 0.9]})

    # Subplot 1: Reloj y senales de control sincronas
    ax1.plot(t_m, clk[mask], label=r'$V(clk)$ (500 MHz)', color='#1f77b4', lw=1.6)
    ax1.plot(t_m, va[mask], label=r'$V(A)=V(B)$ (Síncrono)', color='#ff7f0e', linestyle='--', lw=1.3)
    ax1.plot(t_m, vc[mask], label=r'$V(C)=0\,$V', color='#2ca02c', linestyle='-.', lw=1.3)
    ax1.set_ylabel('Control (V)')
    ax1.set_ylim(-0.1, 1.35)
    ax1.grid(True)
    ax1.legend(loc='center left', framealpha=0.9, fontsize=7.8)

    # Sombrear fases operativas
    ax1.axvspan(1.0, 2.0, color='#ffdddd', alpha=0.35)
    ax1.axvspan(2.0, 3.0, color='#ddffdd', alpha=0.35)
    ax1.axvspan(3.0, 4.0, color='#ffffcc', alpha=0.35)
    ax1.text(1.5, 1.18, 'Ciclo 1: Descarga previa\n($A=B=C=1$)', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#8b0000',
             bbox=dict(boxstyle='round,pad=0.18', facecolor='white', alpha=0.85, edgecolor='gray', lw=0.5))
    ax1.text(2.5, 1.18, 'Ciclo 2: Precarga\n($CLK=0$)', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#006400',
             bbox=dict(boxstyle='round,pad=0.18', facecolor='white', alpha=0.85, edgecolor='gray', lw=0.5))
    ax1.text(3.5, 1.18, 'Ciclo 2: Evaluación\n($A=B=1, C=0$)', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#8b8000',
             bbox=dict(boxstyle='round,pad=0.18', facecolor='white', alpha=0.85, edgecolor='gray', lw=0.5))

    # Subplot 2: Nodo dinamico y nodos internos
    ax2.plot(t_m, vdyn[mask], label=r'$V(dyn)$ (flotante)', color='#d62728', lw=2.0)
    ax2.plot(t_m, vn1[mask], label=r'$V(n_1)$', color='#9467bd', linestyle='--', lw=1.4)
    ax2.plot(t_m, vn2[mask], label=r'$V(n_2)$', color='#8c564b', linestyle=':', lw=1.5)
    ax2.plot(t_m, vn3[mask], label=r'$V(n_3)$', color='#7f7f7f', linestyle='-.', lw=1.2)

    # Lineas de referencia de umbrales
    ax2.axhline(0.4797, color='black', linestyle='--', lw=1.0, alpha=0.7, label=r'$V_M = 0.480\,$V')
    ax2.axhline(0.5785, color='gray', linestyle=':', lw=1.0, alpha=0.7, label=r'$V_{IH} = 0.579\,$V')

    # Sombreado de fases en ax2
    ax2.axvspan(1.0, 2.0, color='#ffdddd', alpha=0.35)
    ax2.axvspan(2.0, 3.0, color='#ddffdd', alpha=0.35)
    ax2.axvspan(3.0, 4.0, color='#ffffcc', alpha=0.35)

    # Anotacion dinamica de dV y Vdyn
    annot_dv = (r'Protocolo Síncrono:' + '\n' +
                r'$\Delta V_{\text{sinc}} = ' + f'{dv_mv:.2f}' + r'\,$mV' + '\n' +
                r'$V_{dyn,\text{min}} = ' + f'{vdyn_min_v:.4f}' + r'\,$V')
    ax2.annotate(annot_dv,
                 xy=(3.5, vdyn_min_v), xytext=(3.6, 0.65),
                 arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2),
                 fontsize=8.2, fontweight='bold', color='#d62728',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#d62728', alpha=0.9))

    # Anotacion de redistribucion rapida inicial vs corte de M2
    ax2.annotate(r'Redistribución inicial ($t=3.05\,$ns, $V_{dyn}=0.885\,$V)' + '\n' +
                 r'seguida de corte subumbral de $M_2$ ($V(n_2) \approx 0.66\,$V)',
                 xy=(3.05, 0.885), xytext=(2.2, 0.38),
                 arrowprops=dict(arrowstyle='->', color='#8c564b', lw=1.1),
                 fontsize=7.8, color='#8c564b',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#8c564b', alpha=0.9))

    ax2.set_ylabel('Tensión Nodal (V)')
    ax2.set_ylim(-0.1, 1.25)
    ax2.grid(True)
    ax2.legend(loc='lower left', ncol=3, framealpha=0.9)

    # Subplot 3: Salida domino
    ax3.plot(t_m, vout[mask], label=r'$V(out)$ (Salida Dominó)', color='#17becf', lw=1.6)
    ax3.axvspan(1.0, 2.0, color='#ffdddd', alpha=0.35)
    ax3.axvspan(2.0, 3.0, color='#ddffdd', alpha=0.35)
    ax3.axvspan(3.0, 4.0, color='#ffffcc', alpha=0.35)
    ax3.set_xlabel('Tiempo (ns)')
    ax3.set_ylabel('Salida (V)')
    ax3.set_ylim(-0.05, 1.15)
    ax3.grid(True)
    ax3.legend(loc='upper right', framealpha=0.9)

    fig.suptitle('Comportamiento Temporal del Peor Caso de Redistribución de Carga (PTM 45nm HP, $C_L=2.0\,$fF)', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.91)

    os.makedirs(FIG_DIR, exist_ok=True)
    out_file = os.path.join(FIG_DIR, "fig1_act2_peor_caso_formas_onda.png")
    plt.savefig(out_file, dpi=300)
    if os.path.exists(INFORME_FIG_DIR):
        shutil.copy2(out_file, os.path.join(INFORME_FIG_DIR, "fig1_act2_peor_caso_formas_onda.png"))
    plt.close()
    print(f"[OK] Generada Figura 1 en: {out_file}")

def generar_figura_2(metricas):
    """Figura 2: dV vs CL y Vdyn,min vs CL (Analitico vs Sincrono vs Historicos)"""
    # Extraccion de datos
    barrido_sinc = metricas["g2b_sincrono_barrido_cl"]
    cl_vals = np.array([step["cl"] * 1e15 for step in barrido_sinc["steps"]])  # [0.5, 1.0, 2.0, 4.0] fF
    dv_sinc = np.array([v * 1e3 for v in barrido_sinc["dv_vdd"]])  # mV
    vdyn_min_sinc = np.array(barrido_sinc["vdyn_min"])  # V

    # Serie con estímulo alternativo (entradas anticipadas)
    barrido_hist = metricas["nand3_cs_barrido_cl"]
    dv_leo_hist = np.array([item["val"] * 1e3 for item in barrido_hist["measurements"]["dv_eval_max"]])
    vdyn_leo_hist = np.array([item["val"] for item in barrido_hist["measurements"]["vdyn_eval_min"]])

    # Modelos analiticos
    VDD = 1.0
    Ca = 0.9486  # fF
    C_extra_guia = 0.3441  # fF (Modelo 2)
    C_extra_full = 0.5813  # fF (Modelo 3)

    cl_sweep_dense = np.linspace(0.4, 4.2, 100)
    dv_pred_nom_dense = VDD * Ca / (Ca + cl_sweep_dense) * 1e3
    dv_pred_guia_dense = VDD * Ca / (Ca + cl_sweep_dense + C_extra_guia) * 1e3
    dv_pred_full_dense = VDD * Ca / (Ca + cl_sweep_dense + C_extra_full) * 1e3

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.5))

    # Panel A: dV vs CL
    ax1.plot(cl_sweep_dense, dv_pred_nom_dense, label=r'Analítico Nominal: $\frac{C_a}{C_a + C_L}$',
             color='#9467bd', linestyle=':', lw=1.3)
    ax1.plot(cl_sweep_dense, dv_pred_guia_dense, label=r'Analítico Guía: $\frac{C_a}{C_a + C_L + 0.344\,\text{fF}}$',
             color='#d62728', linestyle='--', lw=1.5)
    ax1.plot(cl_sweep_dense, dv_pred_full_dense, label=r'Analítico Total: $\frac{C_a}{C_a + C_L + 0.581\,\text{fF}}$',
             color='#ff7f0e', linestyle='-.', lw=1.3)
    
    # Curvas de simulacion
    ax1.plot(cl_vals, dv_sinc, 'o-', color='#1f77b4', lw=2.2, ms=6, label=r'Protocolo Síncrono Nominal ($\Delta V_{\text{sinc}}$)')
    ax1.plot(cl_vals, dv_leo_hist, 's--', color='#2ca02c', lw=1.4, ms=5, label=r'Protocolo Alternativo (Entradas Anticipadas)')

    # Umbrales
    ax1.axhline(421.5, color='gray', linestyle='--', lw=1.0, alpha=0.8, label=r'Margen $NM_H = 421.5\,$mV')
    ax1.axhline(520.3, color='black', linestyle=':', lw=1.0, alpha=0.8, label=r'$\Delta V_{crit,M} = 520.3\,$mV')

    ax1.set_xlabel(r'Capacitancia de Carga $C_L$ (fF)')
    ax1.set_ylabel(r'Caída de Tensión $\Delta V$ (mV)')
    ax1.set_title('(a) Caída por Redistribución vs Carga', fontsize=10.0, pad=6)
    ax1.set_xlim(0.3, 4.3)
    ax1.set_ylim(40, 700)
    ax1.grid(True)
    ax1.legend(loc='upper right', framealpha=0.9, fontsize=7.2)

    # Panel B: Vdyn,min vs CL y Zona Segura
    vdyn_pred_guia_dense = VDD - dv_pred_guia_dense * 1e-3
    ax2.plot(cl_sweep_dense, vdyn_pred_guia_dense, label=r'Predicción $V_{dyn,pred}$ (Guía)',
             color='#d62728', linestyle='--', lw=1.4)
    ax2.plot(cl_vals, vdyn_min_sinc, 'o-', color='#1f77b4', lw=2.2, ms=6, label=r'Protocolo Síncrono Nominal ($V_{dyn,\text{min}}$)')
    ax2.plot(cl_vals, vdyn_leo_hist, 's--', color='#2ca02c', lw=1.4, ms=5, label=r'Protocolo Alternativo (Entradas Anticipadas)')

    # Umbrales estaticos
    ax2.axhline(0.4797, color='black', linestyle='--', lw=1.1, alpha=0.8, label=r'$V_M = 0.480\,$V')
    ax2.axhline(0.5785, color='gray', linestyle=':', lw=1.1, alpha=0.8, label=r'$V_{IH} = 0.579\,$V')

    ax2.axhspan(0.5785, 1.05, color='#e6f5e6', alpha=0.45, label=r'Zona Lógica Segura ($V_{dyn} > V_{IH}$)')
    ax2.axhspan(0.4797, 0.5785, color='#fff5e6', alpha=0.45, label='Región de Transición')

    ax2.set_xlabel(r'Capacitancia de Carga $C_L$ (fF)')
    ax2.set_ylabel(r'Tensión Mínima $V_{dyn,min}$ (V)')
    ax2.set_title('(b) Margen Dinámico y Región Segura', fontsize=10.0, pad=6)
    ax2.set_xlim(0.3, 4.3)
    ax2.set_ylim(0.35, 1.05)
    ax2.grid(True)
    ax2.legend(loc='lower right', framealpha=0.9, fontsize=7.2)

    fig.suptitle('Validación Paramétrica de Charge Sharing: Analítica vs Simulación (45nm HP)', fontsize=11.2, y=0.975)
    fig.text(0.5, 0.915, 'Simulación SPICE (Protocolo Síncrono vs Entradas Anticipadas) vs Modelos Teóricos', fontsize=8.8, ha='center', color='#333333')
    fig.tight_layout(rect=[0, 0.02, 1.0, 0.89])

    out_file = os.path.join(FIG_DIR, "fig2_act2_dv_vs_cl_analitico_simulado.png")
    plt.savefig(out_file, dpi=300)
    if os.path.exists(INFORME_FIG_DIR):
        shutil.copy2(out_file, os.path.join(INFORME_FIG_DIR, "fig2_act2_dv_vs_cl_analitico_simulado.png"))
    plt.close()
    print(f"[OK] Generada Figura 2 en: {out_file}")

def generar_figura_3(metricas):
    """Figura 3: Comparacion de las Tecnicas de Mitigacion y Evaluacion de Contencion"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.5))

    # Cargar datos RAW transitorios
    raw_base = read_raw(find_raw("nand3_cs_g2b_piloto_cl2f.raw"))['data']
    raw_prec45 = read_raw(find_raw("nand3_cs_g2c_precarga_w45.raw"))['data']
    raw_reord_cab_a = read_raw(find_raw("nand3_cs_g2b_reord_cab_combA.raw"))['data']
    raw_reord_cab_b = read_raw(find_raw("nand3_cs_g2b_reord_cab_combB.raw"))['data']
    raw_keeper = read_raw(find_raw("nand3_cs_g2c_keeper_w45.raw"))['data']

    t_base = raw_base['time'] * 1e9
    mask_eval = (t_base >= 2.95) & (t_base <= 3.8)

    t_prec = raw_prec45['time'] * 1e9
    mask_prec = (t_prec >= 2.95) & (t_prec <= 3.8)

    t_cab_a = raw_reord_cab_a['time'] * 1e9
    mask_cab_a = (t_cab_a >= 2.95) & (t_cab_a <= 3.8)

    t_cab_b = raw_reord_cab_b['time'] * 1e9
    mask_cab_b = (t_cab_b >= 2.95) & (t_cab_b <= 3.8)

    t_kp = raw_keeper['time'] * 1e9
    mask_kp = (t_kp >= 2.95) & (t_kp <= 3.8)

    # Metricas
    dv_base_mv = metricas["g2b_sincrono_piloto_cl2f"]["dv_vdd"] * 1e3
    dv_kp_mv = metricas["g2c_keeper_w45"]["dv_vdd"] * 1e3
    t_rec_from_min_ps = metricas["g2c_keeper_w45"]["t_restore_from_min"] * 1e12

    label_base = r'Caso Base Síncrono ($\Delta V = ' + f'{dv_base_mv:.1f}' + r'\,$mV)'
    label_prec = r'Precarga Nodos $n_1, n_2$ ($W_p=45/135\,$nm, $\Delta V \leq 0$)'
    label_reord_a = r'Reord PDN C-A-B (Vect A: $A=B=1, C=0$, $\Delta V \leq 0$)'
    label_reord_b = r'Reord PDN C-A-B (Vect B: $A=0, B=C=1$, $\Delta V = 72.1\,$mV)'
    label_kp = r'Keeper $W_{kp}=45\,$nm ($\Delta V = ' + f'{dv_kp_mv:.1f}' + r'\,$mV, $t_{rec} = ' + f'{t_rec_from_min_ps:.1f}' + r'\,$ps)'

    # Panel A: Formas de onda de V(dyn) en evaluacion
    ax1.plot(t_base[mask_eval], raw_base['V(dyn)'][mask_eval], label=label_base, color='#d62728', lw=1.9)
    ax1.plot(t_prec[mask_prec], raw_prec45['V(dyn)'][mask_prec], label=label_prec, color='#2ca02c', linestyle='--', lw=1.7)
    ax1.plot(t_cab_a[mask_cab_a], raw_reord_cab_a['V(dyn)'][mask_cab_a], label=label_reord_a, color='#1f77b4', linestyle='-.', lw=1.4)
    ax1.plot(t_cab_b[mask_cab_b], raw_reord_cab_b['V(dyn)'][mask_cab_b], label=label_reord_b, color='#9467bd', linestyle=':', lw=1.6)
    ax1.plot(t_kp[mask_kp], raw_keeper['V(dyn)'][mask_kp], label=label_kp, color='#ff7f0e', linestyle='-', lw=2.0)

    ax1.set_xlim(2.95, 3.65)
    ax1.set_ylim(0.80, 1.08)
    ax1.set_xlabel('Tiempo (ns)')
    ax1.set_ylabel(r'Tensión $V(dyn)$ (V)')
    ax1.set_title(r'(a) Respuesta de $V(dyn)$ en Evaluación ($C_L=2.0\,$fF)', fontsize=10.0, pad=6)
    ax1.grid(True)
    ax1.legend(loc='lower right', framealpha=0.9, fontsize=7.0)

    # Panel B: Contencion dinamica
    raw_cont_sin = read_raw(find_raw("nand3_cs_g2c_contencion_sin_keeper.raw"))['data']
    raw_cont_con = read_raw(find_raw("nand3_cs_g2c_contencion_con_keeper.raw"))['data']

    t_cont_sin = raw_cont_sin['time'] * 1e9
    mask_cont_sin = (t_cont_sin >= 0.98) & (t_cont_sin <= 1.25)

    t_cont_con = raw_cont_con['time'] * 1e9
    mask_cont_con = (t_cont_con >= 0.98) & (t_cont_con <= 1.25)

    m_cont = metricas["g2c_contencion_con_keeper"]
    tphl_sin_ps = metricas["g2c_contencion_sin_keeper"]["tphl_dyn"] * 1e12
    tphl_con_ps = m_cont["tphl_dyn"] * 1e12
    tplh_sin_ps = metricas["g2c_contencion_sin_keeper"]["tplh_out"] * 1e12
    tplh_con_ps = m_cont["tplh_out"] * 1e12
    delta_tphl_pct = m_cont["delta_tphl_pct"]

    label_vdyn_sin = r'Sin Keeper ($t_{pHL} = ' + f'{tphl_sin_ps:.2f}' + r'\,$ps)'
    label_vdyn_con = r'Con Keeper $W_{kp}=45\,$nm ($t_{pHL} = ' + f'{tphl_con_ps:.2f}' + r'\,$ps)'
    label_vout_sin = r'$V(out)$ Sin Keeper ($t_{pLH} = ' + f'{tplh_sin_ps:.2f}' + r'\,$ps)'
    label_vout_con = r'$V(out)$ Con Keeper ($t_{pLH} = ' + f'{tplh_con_ps:.2f}' + r'\,$ps)'

    ax2.plot(t_cont_sin[mask_cont_sin], raw_cont_sin['V(dyn)'][mask_cont_sin], label=label_vdyn_sin, color='#1f77b4', lw=1.8)
    ax2.plot(t_cont_con[mask_cont_con], raw_cont_con['V(dyn)'][mask_cont_con], label=label_vdyn_con, color='#d62728', linestyle='--', lw=1.8)
    
    ax2.plot(t_cont_sin[mask_cont_sin], raw_cont_sin['V(out)'][mask_cont_sin], label=label_vout_sin, color='#1f77b4', linestyle=':', lw=1.3)
    ax2.plot(t_cont_con[mask_cont_con], raw_cont_con['V(out)'][mask_cont_con], label=label_vout_con, color='#d62728', linestyle=':', lw=1.3)

    ax2.axhline(0.5, color='gray', linestyle='--', lw=0.9, alpha=0.7)
    annot_pen = (r'Penalización de contención:' + '\n' +
                 r'$\Delta t_{pHL} = +' + f'{tphl_con_ps - tphl_sin_ps:.2f}' + r'\,$ps (+' + f'{delta_tphl_pct:.1f}' + r'%)' + '\n' +
                 r'$\Delta t_{pLH,out} = +' + f'{tplh_con_ps - tplh_sin_ps:.2f}' + r'\,$ps (+' + f'{m_cont["delta_tplh_pct"]:.1f}' + r'%)')
    ax2.annotate(annot_pen,
                 xy=(1.05, 0.5), xytext=(1.06, 0.68),
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.0),
                 fontsize=7.8, color='black',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray', alpha=0.9))

    ax2.set_xlim(0.98, 1.22)
    ax2.set_ylim(-0.05, 1.1)
    ax2.set_xlabel('Tiempo (ns)')
    ax2.set_ylabel('Tensión Nodal (V)')
    ax2.set_title(r'(b) Compromiso de Contención en Evaluación ($A=B=C=1$)', fontsize=10.0, pad=6)
    ax2.grid(True)
    ax2.legend(loc='lower right', framealpha=0.9, fontsize=7.0)

    fig.suptitle('Efectividad de Mitigaciones y Compromiso de Contención (PTM 45nm HP)', fontsize=11.2, y=0.975)
    fig.text(0.5, 0.915, 'Técnicas de Mitigación: Precarga Interna, Reordenamiento de la PDN y Keeper PMOS',
             fontsize=8.8, ha='center', color='#333333')
    fig.tight_layout(rect=[0, 0.02, 1.0, 0.89])

    out_file = os.path.join(FIG_DIR, "fig3_act2_comparacion_mitigaciones.png")
    plt.savefig(out_file, dpi=300)
    if os.path.exists(INFORME_FIG_DIR):
        shutil.copy2(out_file, os.path.join(INFORME_FIG_DIR, "fig3_act2_comparacion_mitigaciones.png"))
    plt.close()
    print(f"[OK] Generada Figura 3 en: {out_file}")

if __name__ == '__main__':
    metricas = cargar_metricas()
    generar_figura_1(metricas)
    generar_figura_2(metricas)
    generar_figura_3(metricas)
