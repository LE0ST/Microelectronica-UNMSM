# -*- coding: utf-8 -*-
"""
Generador de Figuras Científicas — Actividad 5 (LD2)
Microelectrónica y Sistemas Nanoelectrónicos — FIEE UNMSM 2026-II

Genera dos figuras compuestas a 300 DPI según el estándar IEEE:
1. fig1_act5_feedthrough_energia.png:
   - Panel (a): Formas de onda de Clock Feedthrough (V(clk), V(dyn) con/sin keeper, diodo D_DB).
   - Panel (b): Escalado de Energía por conmutación y Corriente pico vs VDD en NTV.

2. fig2_act5_ventana_frecuencia_ntv.png:
   - Panel (a): Tiempos teval y thold (27°C y 85°C) vs VDD en escala log, con marca 10x teval.
   - Panel (b): Ventana de frecuencia operable [fmin, fmax] vs VDD (reproducción de Fig. 9 de la guía).
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

# Estilo científico formal
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12.0
plt.rcParams['axes.labelsize'] = 12.5
plt.rcParams['axes.titlesize'] = 12.5
plt.rcParams['xtick.labelsize'] = 11.0
plt.rcParams['ytick.labelsize'] = 11.0
plt.rcParams['legend.fontsize'] = 10.0
plt.rcParams['figure.titlesize'] = 13.5
plt.rcParams['lines.linewidth'] = 1.8
plt.rcParams['grid.alpha'] = 0.35
plt.rcParams['grid.linestyle'] = ':'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT5_DIR = os.path.dirname(SCRIPT_DIR)
PROJ_DIR = os.path.dirname(ACT5_DIR)
DATOS_DIR = os.path.join(ACT5_DIR, "resultados", "datos")
FIG_DIR = os.path.join(ACT5_DIR, "figuras")
LATEX_FIG_DIR = os.path.join(PROJ_DIR, "informe_latex", "figuras")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(LATEX_FIG_DIR, exist_ok=True)

PARSER_DIR = os.path.join(PROJ_DIR, "scripts", "lectura_resultados")
sys.path.insert(0, PARSER_DIR)
from parse_spice_raw import read_raw

def cargar_metricas():
    with open(os.path.join(DATOS_DIR, "act5_metricas.json"), 'r', encoding='utf-8') as f:
        return json.load(f)

# Paleta formal
C_CLK = '#4b5563'      # Gris neutro
C_DYNA = '#1e3a8a'     # Azul marino (sin keeper)
C_DYNB = '#047857'     # Verde esmeralda (con keeper)
C_DIODE = '#b91c1c'    # Carmesí oscuro (diodo D_DB)
C_FMAX = '#1d4ed8'     # Azul brillante (fmax)
C_FMIN27 = '#b45309'   # Ámbar oscuro (fmin 27C)
C_FMIN85 = '#dc2626'   # Rojo intenso (fmin 85C)
C_ENERGY = '#6d28d9'   # Púrpura (energía)

# ==============================================================================
# FIGURA 1: CLOCK FEEDTHROUGH Y ESCALADO DE ENERGÍA NTV
# ==============================================================================
def generar_figura_1():
    metricas = cargar_metricas()
    raw_path = os.path.join(ACT5_DIR, "circuitos", "act5_feedthrough_keeper.raw")
    raw_data = read_raw(raw_path)['data']

    time_ns = raw_data['time'] * 1e9
    v_clk = raw_data['V(clk)']
    v_dyna = raw_data['V(dyna)']
    v_dynb = raw_data['V(dynb)']
    i_diode = -raw_data['Ib(Mpa)'] * 1e6  # uA

    # Ventana de enfoque en el ciclo activo (0.8 ns a 3.2 ns)
    mask = (time_ns >= 0.8) & (time_ns <= 3.2)
    t = time_ns[mask]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.2))

    # Panel A: Formas de onda de Feedthrough
    ax1.plot(t, v_clk[mask], '--', color=C_CLK, label=r'$V(CLK)$', alpha=0.85, lw=1.6)
    ax1.plot(t, v_dyna[mask], color=C_DYNA, label=r'$V(dyn)$ Base (Sin Keeper)', lw=2.0)
    ax1.plot(t, v_dynb[mask], color=C_DYNB, label=r'$V(dyn)$ Con Keeper ($W_{kp}=45\,\mathrm{nm}$)', lw=2.0)

    # Anotaciones de sobreimpulso y subimpulso
    ax1.annotate(r'Sobreimpulso: $+64.3\,\mathrm{mV}$' + '\n' + r'($V_{\max}=1.064\,\mathrm{V}$)',
                 xy=(2.005, 1.064), xytext=(1.25, 1.068),
                 arrowprops=dict(facecolor=C_DYNA, shrink=0.08, width=1.2, headwidth=5),
                 fontsize=10.0, bbox=dict(boxstyle='round,pad=0.25', facecolor='#eff6ff', edgecolor=C_DYNA, alpha=0.9))

    ax1.annotate(r'Amortiguado por $C_{kp}$:' + '\n' + r'$+49.3\,\mathrm{mV}$ ($-23.3\%$)',
                 xy=(2.005, 1.049), xytext=(2.15, 1.018),
                 arrowprops=dict(facecolor=C_DYNB, shrink=0.08, width=1.2, headwidth=5),
                 fontsize=10.0, bbox=dict(boxstyle='round,pad=0.25', facecolor='#ecfdf5', edgecolor=C_DYNB, alpha=0.9))

    ax1.annotate(r'Subimpulso reloj: $11.1\,\mathrm{mV}$' + '\n' + r'($Mp$ entra en conducción)',
                 xy=(1.011, 0.985), xytext=(1.08, 0.938),
                 arrowprops=dict(facecolor='#6b7280', shrink=0.08, width=1.2, headwidth=5),
                 fontsize=10.0, bbox=dict(boxstyle='round,pad=0.25', facecolor='#f3f4f6', edgecolor='#9ca3af', alpha=0.9))

    ax1.axvspan(0.8, 1.0, color='#e0f2fe', alpha=0.25)
    ax1.axvspan(1.0, 2.0, color='#fef3c7', alpha=0.25, label='Precarga ($CLK=0$)')
    ax1.axvspan(2.0, 3.0, color='#e0f2fe', alpha=0.25, label='Evaluación ($CLK=1$)')
    ax1.axvspan(3.0, 3.2, color='#fef3c7', alpha=0.25)

    ax1.set_title('(a) Dinámica de Clock Feedthrough en dyn', fontweight='bold', fontsize=11.5)
    ax1.set_xlabel('Tiempo (ns)')
    ax1.set_ylabel('Tensión (V)')
    ax1.set_ylim(0.92, 1.11)
    ax1.set_xlim(0.8, 3.2)
    ax1.grid(True)
    ax1.legend(loc='lower right', framealpha=0.92, fontsize=9.0)

    # Panel B: Energía y Potencia vs VDD
    vdd_list = metricas['barrido_ntv_hp']['VDD_V']
    energy_fJ = metricas['barrido_ntv_hp']['energia_conmutacion']['E_cycle_fJ']
    ipeak_uA = metricas['barrido_ntv_hp']['energia_conmutacion']['I_peak_uA']

    ax2_twin = ax2.twinx()

    l1 = ax2.plot(vdd_list, energy_fJ, 'o-', color=C_ENERGY, lw=2.0, ms=6, label=r'Energía por ciclo $E_{\mathrm{sw}}$')
    l2 = ax2_twin.plot(vdd_list, ipeak_uA, 's--', color='#ea580c', lw=1.8, ms=6, label=r'Pico de corriente $I_{\mathrm{pk}}$')

    ax2.set_title('(b) Escalado Energético hacia Régimen NTV', fontweight='bold', fontsize=11.5)
    ax2.set_xlabel(r'Tensión de Alimentación $V_{DD}$ (V)')
    ax2.set_ylabel(r'Energía por Ciclo $E_{\mathrm{sw}}$ (fJ)', color=C_ENERGY)
    ax2_twin.set_ylabel(r'Corriente Pico $I_{\mathrm{pk}}$ ($\mu\mathrm{A}$)', color='#ea580c')
    ax2.tick_params(axis='y', labelcolor=C_ENERGY)
    ax2_twin.tick_params(axis='y', labelcolor='#ea580c')
    ax2.grid(True)

    ax2.annotate(r'$\mathbf{10.1\times}$ Ahorro energ.' + '\n' + r'($0.726 \to 0.072\,\mathrm{fJ}$)',
                 xy=(0.35, energy_fJ[-1]), xytext=(0.42, 0.22),
                 arrowprops=dict(facecolor=C_ENERGY, shrink=0.08, width=1.2, headwidth=5),
                 fontsize=10.0, bbox=dict(boxstyle='round,pad=0.25', facecolor='#faf5ff', edgecolor=C_ENERGY, alpha=0.9))

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='center left', framealpha=0.9, fontsize=9.0)

    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "fig1_act5_feedthrough_energia.png")
    plt.savefig(out_file, dpi=300)
    plt.savefig(os.path.join(LATEX_FIG_DIR, "fig1_act5_feedthrough_energia.png"), dpi=300)
    plt.close()
    print(f"Figura 1 generada en: {out_file}")

# ==============================================================================
# FIGURA 2: TIEMPOS TEVAL/THOLD Y VENTANA DE FRECUENCIA NTV
# ==============================================================================
def generar_figura_2():
    metricas = cargar_metricas()
    vdd = np.array(metricas['barrido_ntv_hp']['VDD_V'])
    
    # Tiempos
    teval_base = np.array(metricas['barrido_ntv_hp']['sin_keeper']['teval_ps']) * 1e-12
    teval_kp45 = np.array(metricas['barrido_ntv_hp']['con_keeper_45nm']['teval_ps']) * 1e-12
    teval_kp90 = np.array(metricas['barrido_ntv_hp']['con_keeper_90nm']['teval_ps']) * 1e-12
    thold_27 = np.array(metricas['barrido_ntv_hp']['retencion_27C']['thold_us']) * 1e-6
    thold_85 = np.array(metricas['barrido_ntv_hp']['retencion_85C']['thold_us']) * 1e-6

    # Frecuencias en MHz
    fmax_base_MHz = np.array(metricas['barrido_ntv_hp']['sin_keeper']['fmax_GHz']) * 1e3
    fmax_kp45_MHz = np.array(metricas['barrido_ntv_hp']['con_keeper_45nm']['fmax_GHz']) * 1e3
    fmin_27_MHz = np.array(metricas['barrido_ntv_hp']['retencion_27C']['fmin_kHz']) * 1e-3
    fmin_85_MHz = np.array(metricas['barrido_ntv_hp']['retencion_85C']['fmin_kHz']) * 1e-3

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.2))

    # Panel A: teval y thold vs VDD
    ax1.semilogy(vdd, thold_27 * 1e9, 's-', color='#059669', label=r'$t_{\mathrm{hold}}$ ($27^\circ\mathrm{C}$, sin keeper)', lw=2.0)
    ax1.semilogy(vdd, thold_85 * 1e9, 'd-', color=C_FMIN85, label=r'$t_{\mathrm{hold}}$ ($85^\circ\mathrm{C}$, peor caso térmico)', lw=2.0)
    ax1.semilogy(vdd, teval_base * 1e9, 'o-', color=C_FMAX, label=r'$t_{\mathrm{eval}}$ (Sin keeper)', lw=2.0)
    ax1.semilogy(vdd, teval_kp45 * 1e9, '^--', color='#7c3aed', label=r'$t_{\mathrm{eval}}$ (Keeper $45\,\mathrm{nm}$)', lw=1.6)
    ax1.semilogy(vdd, 10 * teval_base * 1e9, ':', color='#475569', label=r'Criterio $10\times t_{\mathrm{eval}}$', lw=1.6)

    ax1.annotate(r'Margen $10\times$ seguro' + '\n' + r'($t_{\mathrm{hold}} \gg 10 t_{\mathrm{eval}}$)',
                 xy=(0.35, 10 * teval_base[-1] * 1e9), xytext=(0.42, 60),
                 arrowprops=dict(facecolor='#475569', shrink=0.08, width=1.2, headwidth=5),
                 fontsize=10.0, bbox=dict(boxstyle='round,pad=0.25', facecolor='#f8fafc', edgecolor='#64748b', alpha=0.9))

    ax1.set_title(r'(a) Tiempos $t_{\mathrm{eval}}$ y $t_{\mathrm{hold}}$ vs $V_{DD}$', fontweight='bold', fontsize=11.5)
    ax1.set_xlabel(r'Tensión de Alimentación $V_{DD}$ (V)')
    ax1.set_ylabel('Tiempo (ns)')
    ax1.set_ylim(0.015, 3500)
    ax1.grid(True, which='both')
    ax1.legend(loc='center right', framealpha=0.9, fontsize=8.5)

    # Panel B: Ventana de Frecuencia [fmin, fmax]
    ax2.semilogy(vdd, fmax_base_MHz, 'o-', color=C_FMAX, label=r'$f_{\max}$ (Sin keeper)', lw=2.0)
    ax2.semilogy(vdd, fmax_kp45_MHz, '^--', color='#7c3aed', label=r'$f_{\max}$ (Keeper $45\,\mathrm{nm}$)', lw=1.6)
    ax2.semilogy(vdd, fmin_85_MHz, 'd-', color=C_FMIN85, label=r'$f_{\min}$ ($85^\circ\mathrm{C}$, peor caso)', lw=2.0)
    ax2.semilogy(vdd, fmin_27_MHz, 's-', color='#059669', label=r'$f_{\min}$ ($27^\circ\mathrm{C}$)', lw=2.0)

    # Relleno de region operable
    ax2.fill_between(vdd, fmin_85_MHz, fmax_base_MHz, color='#dbeafe', alpha=0.45, label=r'Región Operable ($85^\circ\mathrm{C}$)')

    ax2.set_title(r'(b) Ventana de Frecuencia Operable vs $V_{DD}$', fontweight='bold', fontsize=11.5)
    ax2.set_xlabel(r'Tensión de Alimentación $V_{DD}$ (V)')
    ax2.set_ylabel('Frecuencia (MHz)')
    ax2.set_ylim(0.1, 35000)
    ax2.grid(True, which='both')
    ax2.legend(loc='upper left', framealpha=0.9, fontsize=8.5)

    # Anotacion del ancho de ventana
    ax2.text(0.68, 60, 'Región Operable\nDominó NTV', fontsize=10.5, fontweight='bold', color='#1e3a8a',
             ha='center', va='center', bbox=dict(boxstyle='round,pad=0.25', facecolor='#eff6ff', edgecolor='#93c5fd', alpha=0.9))

    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "fig2_act5_ventana_frecuencia_ntv.png")
    plt.savefig(out_file, dpi=300)
    plt.savefig(os.path.join(LATEX_FIG_DIR, "fig2_act5_ventana_frecuencia_ntv.png"), dpi=300)
    plt.close()
    print(f"Figura 2 generada en: {out_file}")

if __name__ == '__main__':
    generar_figura_1()
    generar_figura_2()
