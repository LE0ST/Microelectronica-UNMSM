# -*- coding: utf-8 -*-
"""
Generador de Figuras Cientificas - Actividad 2 (LD2)
Microelectronica y Sistemas Nanoelectronicos - UNMSM 2026-II

Genera tres figuras a 300 DPI con rotulacion completa, unidades, leyendas y
referencia formal a los netlists generadores:
1. fig1_act2_peor_caso_formas_onda.png: Formas de onda del peor caso de charge sharing.
2. fig2_act2_dv_vs_cl_analitico_simulado.png: Barrido de dV y Vdyn vs CL (Analitico vs Simulado).
3. fig3_act2_comparacion_mitigaciones.png: Comparacion de las 3 mitigaciones y contencion.

REGLA DE TRAZABILIDAD:
Todos los datos numericos de simulacion se extraen dinamicamente desde:
  resultados/datos/act2_metricas.json
y desde los archivos .raw de simulacion real. No se admiten copias hardcodeadas de resultados.
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

# Configuracion de estilo IEEE / Cientifico
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 8.5
plt.rcParams['figure.titlesize'] = 12
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['grid.alpha'] = 0.4
plt.rcParams['grid.linestyle'] = ':'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT2_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(ACT2_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT2_DIR, "resultados", "datos")
FIG_DIR = os.path.join(ACT2_DIR, "figuras")

PARSER_DIR = os.path.abspath(os.path.join(ACT2_DIR, "..", "scripts", "lectura_resultados"))
sys.path.insert(0, PARSER_DIR)
from parse_spice_raw import read_raw

def cargar_metricas():
    """Carga las metricas de simulacion generadas por el pipeline oficial."""
    json_path = os.path.join(DATOS_DIR, "act2_metricas.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Archivo de metricas no encontrado: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generar_figura_1(metricas):
    """Figura 1: Formas de onda completas del peor caso de charge sharing (nand3_cs_peor_caso_fisico.raw)"""
    raw_path = os.path.join(RAW_DIR, "nand3_cs_peor_caso_fisico.raw")
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} no existe.")
        return

    # Metricas dinamicas del ensayo fisico (ENS-A2-02)
    m_fisico = metricas["nand3_cs_peor_caso_fisico"]["measurements"]
    dv_eval_mv = m_fisico["dv_eval_max"] * 1e3
    vdyn_eval_v = m_fisico["vdyn_eval_min"]

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

    # Subplot 1: Reloj y senales de control
    ax1.plot(t_m, clk[mask], label=r'$V(clk)$ (500 MHz)', color='#1f77b4', lw=1.6)
    ax1.plot(t_m, va[mask], label=r'$V(A)$', color='#ff7f0e', linestyle='--', lw=1.3)
    ax1.plot(t_m, vc[mask], label=r'$V(C)$', color='#2ca02c', linestyle='-.', lw=1.3)
    ax1.set_ylabel('Control (V)')
    ax1.set_ylim(-0.1, 1.25)
    ax1.grid(True)
    ax1.legend(loc='upper right', ncol=3, framealpha=0.9)

    # Sombrear fases operativas
    ax1.axvspan(1.0, 2.0, color='#ffdddd', alpha=0.35)
    ax1.axvspan(2.0, 3.0, color='#ddffdd', alpha=0.35)
    ax1.axvspan(3.0, 4.0, color='#ffffcc', alpha=0.35)
    ax1.text(1.5, 1.08, 'Ciclo 1: Eval (A=B=C=1)', ha='center', fontsize=8.5, fontweight='bold', color='#8b0000')
    ax1.text(2.5, 1.08, 'Ciclo 2: Precarga (CLK=0)', ha='center', fontsize=8.5, fontweight='bold', color='#006400')
    ax1.text(3.5, 1.08, 'Ciclo 2: Eval (A=B=1, C=0)', ha='center', fontsize=8.5, fontweight='bold', color='#8b8000')

    # Subplot 2: Nodo dinamico y nodos internos
    ax2.plot(t_m, vdyn[mask], label=r'$V(dyn)$ (flotante)', color='#d62728', lw=2.0)
    ax2.plot(t_m, vn1[mask], label=r'$V(n_1)$', color='#9467bd', linestyle='--', lw=1.4)
    ax2.plot(t_m, vn2[mask], label=r'$V(n_2)$', color='#8c564b', linestyle=':', lw=1.5)
    ax2.plot(t_m, vn3[mask], label=r'$V(n_3)$', color='#7f7f7f', linestyle='-.', lw=1.2)

    # Lineas de referencia de umbrales (Constantes de calibracion ENS-CAL-02)
    ax2.axhline(0.4797, color='black', linestyle='--', lw=1.0, alpha=0.7, label=r'$V_M = 0.480\,$V')
    ax2.axhline(0.5785, color='gray', linestyle=':', lw=1.0, alpha=0.7, label=r'$V_{IH} = 0.579\,$V')

    # Sombreado de fases en ax2
    ax2.axvspan(1.0, 2.0, color='#ffdddd', alpha=0.35)
    ax2.axvspan(2.0, 3.0, color='#ddffdd', alpha=0.35)
    ax2.axvspan(3.0, 4.0, color='#ffffcc', alpha=0.35)

    # Anotacion dinamica de dV y Vdyn
    annot_dv = (r'$\Delta V \approx ' + f'{dv_eval_mv:.0f}' + r'\,$mV' + '\n' +
                r'($V_{dyn} = ' + f'{vdyn_eval_v:.3f}' + r'\,$V)')
    ax2.annotate(annot_dv,
                 xy=(3.4, vdyn_eval_v), xytext=(3.6, 0.72),
                 arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2),
                 fontsize=8.5, fontweight='bold', color='#d62728',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#d62728', alpha=0.9))

    # Anotacion de corte de M2
    ax2.annotate(r'Corte subumbral de $M_2$' + '\n' + r'($V_{GS2} \leq V_{th2}$)',
                 xy=(3.3, 0.66), xytext=(2.6, 0.38),
                 arrowprops=dict(arrowstyle='->', color='#8c564b', lw=1.1),
                 fontsize=8.0, color='#8c564b',
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

    fig.suptitle('Comportamiento Temporal de Charge Sharing en NAND3 Dinámica Footed (45nm HP)\nNetlist: nand3_cs_peor_caso_fisico.cir (ENS-A2-02)', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.91)

    os.makedirs(FIG_DIR, exist_ok=True)
    out_file = os.path.join(FIG_DIR, "fig1_act2_peor_caso_formas_onda.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generada Figura 1 en: {out_file}")

def generar_figura_2(metricas):
    """Figura 2: dV vs CL y Vdyn,min vs CL (Analitico vs Simulado)"""
    # Extraccion dinamica desde act2_metricas.json (ENS-A2-03)
    barrido = metricas["nand3_cs_barrido_cl"]
    cl_vals = np.array([step["cl"] * 1e15 for step in barrido["steps"]])  # [0.5, 1.0, 2.0, 4.0] fF
    dv_sim = np.array([item["val"] * 1e3 for item in barrido["measurements"]["dv_eval_max"]])  # mV
    vdyn_min_sim = np.array([item["val"] for item in barrido["measurements"]["vdyn_eval_min"]])  # V

    # Parametros analiticos deducidos en prediccion_analitica_act2.md
    VDD = 1.0
    Ca = 0.9486  # fF (Cn1 + Cn2 = 2 * 0.4743 fF)
    C_extra_guia = 0.3441  # fF (Cgd_Mp + Cg_inv segun Sec. 6.2)
    C_extra_full = 0.5812  # fF (Cgd_Mp + Cg_inv + Cdiff_M1)

    # Curvas analiticas densas
    cl_sweep_dense = np.linspace(0.4, 4.2, 100)
    dv_pred_nom_dense = VDD * Ca / (Ca + cl_sweep_dense) * 1e3
    dv_pred_guia_dense = VDD * Ca / (Ca + cl_sweep_dense + C_extra_guia) * 1e3
    dv_pred_full_dense = VDD * Ca / (Ca + cl_sweep_dense + C_extra_full) * 1e3

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 4.2))

    # Panel A: dV vs CL
    ax1.plot(cl_sweep_dense, dv_pred_nom_dense, label=r'Analítico Nominal: $\frac{C_a}{C_a + C_L}$',
             color='#9467bd', linestyle=':', lw=1.4)
    ax1.plot(cl_sweep_dense, dv_pred_guia_dense, label=r'Analítico Guía: $\frac{C_a}{C_a + C_{L,tot}}$',
             color='#d62728', linestyle='--', lw=1.6)
    ax1.plot(cl_sweep_dense, dv_pred_full_dense, label=r'Analítico Carga Total Completa',
             color='#ff7f0e', linestyle='-.', lw=1.4)
    ax1.plot(cl_vals, dv_sim, 'o-', color='#1f77b4', lw=2.0, ms=6, label=r'Simulación SPICE ($\Delta V_{eval}$)')

    # Umbrales de calibracion del inversor dominó (ENS-CAL-02)
    ax1.axhline(421.5, color='gray', linestyle='--', lw=1.0, alpha=0.8, label=r'Margen $NM_H = 421.5\,$mV')
    ax1.axhline(520.3, color='black', linestyle=':', lw=1.0, alpha=0.8, label=r'$\Delta V_{crit,M} = 520.3\,$mV')

    ax1.set_xlabel(r'Capacitancia de Carga $C_L$ (fF)')
    ax1.set_ylabel(r'Caída de Tensión $\Delta V$ (mV)')
    ax1.set_title('(a) Caída por Redistribución vs Carga', fontsize=10.5)
    ax1.set_xlim(0.3, 4.3)
    ax1.set_ylim(40, 700)
    ax1.grid(True)
    ax1.legend(loc='upper right', framealpha=0.9, fontsize=7.8)

    # Panel B: Vdyn,min vs CL y Zona Segura
    vdyn_pred_guia_dense = VDD - dv_pred_guia_dense * 1e-3
    ax2.plot(cl_sweep_dense, vdyn_pred_guia_dense, label=r'Predicción $V_{dyn,pred}$ (Guía)',
             color='#d62728', linestyle='--', lw=1.5)
    ax2.plot(cl_vals, vdyn_min_sim, 's-', color='#2ca02c', lw=2.0, ms=6, label=r'Simulado $V_{dyn,min}$')

    # Umbrales estaticos
    ax2.axhline(0.4797, color='black', linestyle='--', lw=1.1, alpha=0.8, label=r'$V_M = 0.480\,$V')
    ax2.axhline(0.5785, color='gray', linestyle=':', lw=1.1, alpha=0.8, label=r'$V_{IH} = 0.579\,$V')

    # Sombrear zona de inmunidad logica
    ax2.axhspan(0.5785, 1.05, color='#e6f5e6', alpha=0.5, label=r'Zona Lógica Segura ($V_{dyn} > V_{IH}$)')
    ax2.axhspan(0.4797, 0.5785, color='#fff5e6', alpha=0.5, label='Región de Transición')

    ax2.set_xlabel(r'Capacitancia de Carga $C_L$ (fF)')
    ax2.set_ylabel(r'Tensión Mínima $V_{dyn,min}$ (V)')
    ax2.set_title('(b) Margen Dinámico y Región Segura', fontsize=10.5)
    ax2.set_xlim(0.3, 4.3)
    ax2.set_ylim(0.35, 1.05)
    ax2.grid(True)
    ax2.legend(loc='lower right', framealpha=0.9, fontsize=7.8)

    fig.suptitle('Validación Paramétrica de Charge Sharing: Analítica vs Simulación (45nm HP)\nNetlist: nand3_cs_barrido_cl.cir (ENS-A2-03)', y=0.99)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)

    out_file = os.path.join(FIG_DIR, "fig2_act2_dv_vs_cl_analitico_simulado.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generada Figura 2 en: {out_file}")

def generar_figura_3(metricas):
    """Figura 3: Comparacion de las 3 Mitigaciones y Evaluacion de Contencion"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.2))

    # Cargar datos RAW transitorios
    raw_base = read_raw(os.path.join(RAW_DIR, "nand3_cs_peor_caso_fisico.raw"))['data']
    raw_mit1 = read_raw(os.path.join(RAW_DIR, "nand3_cs_mitigacion_precarga.raw"))['data']
    raw_mit2 = read_raw(os.path.join(RAW_DIR, "nand3_cs_mitigacion_reordenamiento.raw"))['data']
    raw_mit3 = read_raw(os.path.join(RAW_DIR, "nand3_cs_mitigacion_keeper.raw"))['data']

    t_base = raw_base['time'] * 1e9
    mask_eval = (t_base >= 2.95) & (t_base <= 3.8)

    t_mit1 = raw_mit1['time'] * 1e9
    mask_mit1 = (t_mit1 >= 2.95) & (t_mit1 <= 3.8)

    t_mit2 = raw_mit2['time'] * 1e9
    mask_mit2 = (t_mit2 >= 2.95) & (t_mit2 <= 3.8)

    t_mit3 = raw_mit3['time'] * 1e9
    mask_mit3 = (t_mit3 >= 2.95) & (t_mit3 <= 3.8)

    # Metricas dinamicas para etiquetas de Panel A
    dv_base_mv = metricas["nand3_cs_peor_caso_fisico"]["measurements"]["dv_eval_max"] * 1e3
    dv_reord_uv = metricas["nand3_cs_mitigacion_reordenamiento"]["measurements"]["dv_eval_max"] * 1e6
    t_restore_ps = metricas["nand3_cs_mitigacion_keeper"]["measurements"]["t_restore"] * 1e12

    label_base = r'Base (Sin Mitigación, $\Delta V = ' + f'{dv_base_mv:.0f}' + r'\,$mV)'
    label_mit1 = r'Mitigación 1: Precarga $n_1, n_2$ ($\Delta V \leq 0$)'
    label_mit2 = r'Mitigación 2: Reordenamiento $C$ tope (' + f'{dv_reord_uv:.0f}' + r'$\,\mu$V)'
    label_mit3 = r'Mitigación 3: Keeper $W_{kp}=45\,$nm ($t_{rec}=' + f'{t_restore_ps:.0f}' + r'\,$ps)'

    # Panel A: Formas de onda de V(dyn) en evaluacion (mitigaciones)
    ax1.plot(t_base[mask_eval], raw_base['V(dyn)'][mask_eval], label=label_base, color='#d62728', lw=1.8)
    ax1.plot(t_mit1[mask_mit1], raw_mit1['V(dyn)'][mask_mit1], label=label_mit1, color='#2ca02c', linestyle='--', lw=1.7)
    ax1.plot(t_mit2[mask_mit2], raw_mit2['V(dyn)'][mask_mit2], label=label_mit2, color='#1f77b4', linestyle='-.', lw=1.7)
    ax1.plot(t_mit3[mask_mit3], raw_mit3['V(dyn)'][mask_mit3], label=label_mit3, color='#ff7f0e', linestyle='-', lw=1.9)

    ax1.set_xlim(2.95, 3.6)
    ax1.set_ylim(0.85, 1.05)
    ax1.set_xlabel('Tiempo (ns)')
    ax1.set_ylabel(r'Tensión $V(dyn)$ (V)')
    ax1.set_title(r'(a) Respuesta de $V(dyn)$ en Evaluación ($A=B=1, C=0$)', fontsize=10.0)
    ax1.grid(True)
    ax1.legend(loc='lower right', framealpha=0.9, fontsize=7.5)

    # Panel B: Evaluacion de contencion en transicion 1 -> 0 (A=B=C=1)
    raw_cont_sin = read_raw(os.path.join(RAW_DIR, "nand3_cs_contencion_sin_keeper.raw"))['data']
    raw_cont_con = read_raw(os.path.join(RAW_DIR, "nand3_cs_contencion_con_keeper.raw"))['data']

    t_cont_sin = raw_cont_sin['time'] * 1e9
    mask_cont_sin = (t_cont_sin >= 0.98) & (t_cont_sin <= 1.25)

    t_cont_con = raw_cont_con['time'] * 1e9
    mask_cont_con = (t_cont_con >= 0.98) & (t_cont_con <= 1.25)

    # Metricas dinamicas de contencion (ENS-A2-07a / ENS-A2-07b)
    m_cont_sin = metricas["nand3_cs_contencion_sin_keeper"]["measurements"]
    m_cont_con = metricas["nand3_cs_contencion_con_keeper"]["measurements"]
    tphl_sin_ps = m_cont_sin["tphl_dyn"] * 1e12
    tphl_con_ps = m_cont_con["tphl_dyn"] * 1e12
    tplh_sin_ps = m_cont_sin["tplh_out"] * 1e12
    tplh_con_ps = m_cont_con["tplh_out"] * 1e12
    delta_tphl_ps = tphl_con_ps - tphl_sin_ps
    delta_tphl_pct = (delta_tphl_ps / tphl_sin_ps) * 100

    label_vdyn_sin = r'Sin Keeper ($t_{pHL} = ' + f'{tphl_sin_ps:.2f}' + r'\,$ps)'
    label_vdyn_con = r'Con Keeper $W_{kp}=45\,$nm ($t_{pHL} = ' + f'{tphl_con_ps:.2f}' + r'\,$ps)'
    label_vout_sin = r'$V(out)$ Sin Keeper ($t_{pLH} = ' + f'{tplh_sin_ps:.2f}' + r'\,$ps)'
    label_vout_con = r'$V(out)$ Con Keeper ($t_{pLH} = ' + f'{tplh_con_ps:.2f}' + r'\,$ps)'

    ax2.plot(t_cont_sin[mask_cont_sin], raw_cont_sin['V(dyn)'][mask_cont_sin], label=label_vdyn_sin, color='#1f77b4', lw=1.8)
    ax2.plot(t_cont_con[mask_cont_con], raw_cont_con['V(dyn)'][mask_cont_con], label=label_vdyn_con, color='#d62728', linestyle='--', lw=1.8)
    
    # Salidas
    ax2.plot(t_cont_sin[mask_cont_sin], raw_cont_sin['V(out)'][mask_cont_sin], label=label_vout_sin, color='#1f77b4', linestyle=':', lw=1.3)
    ax2.plot(t_cont_con[mask_cont_con], raw_cont_con['V(out)'][mask_cont_con], label=label_vout_con, color='#d62728', linestyle=':', lw=1.3)

    ax2.axhline(0.5, color='gray', linestyle='--', lw=0.9, alpha=0.7)
    annot_pen = (r'Penalización de contención:' + '\n' +
                 r'$\Delta t_{pHL} = +' + f'{delta_tphl_ps:.2f}' + r'\,$ps (+' + f'{delta_tphl_pct:.1f}' + r'%)')
    ax2.annotate(annot_pen,
                 xy=(1.05, 0.5), xytext=(1.08, 0.70),
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.0),
                 fontsize=8.0, color='black',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray', alpha=0.9))

    ax2.set_xlim(0.98, 1.22)
    ax2.set_ylim(-0.05, 1.1)
    ax2.set_xlabel('Tiempo (ns)')
    ax2.set_ylabel('Tensión Nodal (V)')
    ax2.set_title(r'(b) Compromiso de Contención ($A=B=C=1$)', fontsize=10.0)
    ax2.grid(True)
    ax2.legend(loc='center right', framealpha=0.9, fontsize=7.5)

    fig.suptitle('Efectividad de Mitigaciones y Compromiso de Contención (45nm HP)\nNetlists: ENS-A2-02, ENS-A2-04, ENS-A2-05, ENS-A2-06, ENS-A2-07a/b', y=0.99)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)

    out_file = os.path.join(FIG_DIR, "fig3_act2_comparacion_mitigaciones.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[OK] Generada Figura 3 en: {out_file}")

if __name__ == '__main__':
    metricas = cargar_metricas()
    generar_figura_1(metricas)
    generar_figura_2(metricas)
    generar_figura_3(metricas)
