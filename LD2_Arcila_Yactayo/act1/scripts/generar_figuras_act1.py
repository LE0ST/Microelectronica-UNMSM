# -*- coding: utf-8 -*-
"""
Generador de Figuras Cientificas - Actividad 1 (LD2)
Microelectronica y Sistemas Nanoelectronicos - UNMSM 2026-II

Genera tres figuras a 300 DPI con rotulacion completa, unidades, leyendas y
referencia formal a los netlists generadores:
1. fig1_act1_fases_formas_onda.png: Fases de la compuerta dinamica y nodo flotante.
2. fig2_act1_dinamica_vs_estatica.png: Comparacion temporal dinamica dominó vs estatica.
3. fig3_act1_retencion_pdn_abierta.png: Retencion con PDN abierta a 2ns vs 400ns.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Configuracion de estilo IEEE / Cientifico
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 12
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['grid.alpha'] = 0.4
plt.rcParams['grid.linestyle'] = ':'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT1_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(ACT1_DIR, "resultados", "raw")
FIG_DIR = os.path.join(ACT1_DIR, "figuras")

PARSER_DIR = os.path.abspath(os.path.join(ACT1_DIR, "..", "scripts", "lectura_resultados"))
sys.path.insert(0, PARSER_DIR)
from parse_spice_raw import read_raw

def generar_figura_1():
    """Figura 1: Formas de onda conjuntas y diagrama de fases (nand3_dinamica_base.raw)"""
    raw_path = os.path.join(RAW_DIR, "nand3_dinamica_base.raw")
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} no existe.")
        return

    res = read_raw(raw_path)
    t = res['data']['time'] * 1e9  # ns
    clk = res['data']['V(clk)']
    va = res['data']['V(a)']
    vdyn = res['data']['V(dyn)']
    vout = res['data']['V(out)']

    # Acotar a los primeros dos ciclos completos (0 a 4 ns)
    mask = t <= 4.0
    t_m = t[mask]
    clk_m = clk[mask]
    va_m = va[mask]
    vdyn_m = vdyn[mask]
    vout_m = vout[mask]

    fig, axes = plt.subplots(4, 1, figsize=(8.5, 7.0), sharex=True, gridspec_kw={'hspace': 0.15})

    # Shading de fases
    # Fase 1: 0 a 1.0 ns (Evaluacion con A=0 -> Nodo Flotante)
    # Fase 2: 1.0 a 2.0 ns (Precarga)
    # Fase 3: 2.0 a 3.0 ns (Evaluacion con A=1 -> Descarga)
    # Fase 4: 3.0 a 4.0 ns (Precarga)
    colors_fases = ['#fff2cc', '#e1d5e7', '#d5e8d4', '#e1d5e7']
    labels_fases = [
        'Fase I: Evaluación (A=0)\n[NODO FLOTANTE]',
        'Fase II: Precarga (CLK=0)\n[Mp ON, Restaura VDD]',
        'Fase III: Evaluación (A=1)\n[PDN Descarga a 0]',
        'Fase IV: Precarga (CLK=0)\n[Restauración a VDD]'
    ]
    fase_bounds = [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)]

    for ax in axes:
        for idx, (b_start, b_end) in enumerate(fase_bounds):
            ax.axvspan(b_start, b_end, color=colors_fases[idx], alpha=0.45, lw=0)
        ax.grid(True)
        ax.set_ylim(-0.1, 1.15)
        ax.set_yticks([0.0, 0.5, 1.0])

    # 1. Reloj CLK
    axes[0].plot(t_m, clk_m, color='#003366', label='V(clk)')
    axes[0].set_ylabel('V(clk) [V]')
    axes[0].legend(loc='upper right')

    # Texto de fases en el panel superior
    for idx, (b_start, b_end) in enumerate(fase_bounds):
        axes[0].text((b_start + b_end)/2, 1.18, labels_fases[idx],
                     ha='center', va='bottom', fontsize=8, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='gray', lw=0.5))

    # 2. Entrada A
    axes[1].plot(t_m, va_m, color='#990000', label='V(a) [Conmuta a 1.1 ns]')
    axes[1].set_ylabel('V(a) [V]')
    axes[1].legend(loc='upper right')

    # 3. Nodo Dinamico V(dyn)
    axes[2].plot(t_m, vdyn_m, color='#cc6600', lw=1.8, label='V(dyn) [Nodo Dinámico]')
    axes[2].axhline(0.5, color='gray', linestyle='--', lw=0.8)
    axes[2].annotate('Flotando en VDD\n(CLK=1, A=0)', xy=(0.5, 1.0), xytext=(0.3, 0.65),
                     arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8), fontsize=8)
    axes[2].annotate(r'Descarga $t_{pHL}=22.2\,$ps', xy=(2.03, 0.5), xytext=(2.15, 0.35),
                     arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8), fontsize=8)
    axes[2].annotate(r'Precarga $t_{pLH}=25.1\,$ps', xy=(3.05, 0.5), xytext=(3.15, 0.65),
                     arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8), fontsize=8)
    axes[2].set_ylabel('V(dyn) [V]')
    axes[2].legend(loc='upper right')

    # 4. Salida Domino V(out)
    axes[3].plot(t_m, vout_m, color='#006633', lw=1.8, label='V(out) [Salida Inversor Dominó]')
    axes[3].axhline(0.5, color='gray', linestyle='--', lw=0.8)
    axes[3].annotate(r'Evaluación $0\to 1$ ($t_{pLH,out}=35.9\,$ps)', xy=(2.04, 0.5), xytext=(2.15, 0.65),
                     arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8), fontsize=8)
    axes[3].set_ylabel('V(out) [V]')
    axes[3].set_xlabel('Tiempo [ns]')
    axes[3].legend(loc='upper right')
    axes[3].set_xlim(0, 4.0)

    fig.suptitle('Comportamiento Temporal y Fases de la NAND3 Dinámica Footed (45nm HP, 500 MHz)\nNetlist: nand3_dinamica_base.cir', y=0.98)
    out_file = os.path.join(FIG_DIR, "fig1_act1_fases_formas_onda.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generada Figura 1: {out_file}")

def generar_figura_2():
    """Figura 2: Comparacion Dinamica Domino vs Estatica Equivalente (Mismo Estimulo)"""
    raw_dyn = os.path.join(RAW_DIR, "nand3_dinamica_base.raw")
    raw_stat = os.path.join(RAW_DIR, "nand3_estatica_mismo_estimulo.raw")

    if not os.path.exists(raw_dyn) or not os.path.exists(raw_stat):
        print("Error: falta un archivo raw para figura 2.")
        return

    r_d = read_raw(raw_dyn)
    r_s = read_raw(raw_stat)

    t_d = r_d['data']['time'] * 1e9
    vout_d = r_d['data']['V(out)']
    vdyn_d = r_d['data']['V(dyn)']
    clk_d = r_d['data']['V(clk)']
    va_d = r_d['data']['V(a)']

    t_s = r_s['data']['time'] * 1e9
    vout_s = r_s['data']['V(out_stat)']
    va_s = r_s['data']['V(a)']

    # Ventana de evaluacion/conmutacion compartida: 0.8 a 3.2 ns
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 6.0), sharex=True)

    # Subplot 1: Dinamica Domino (ENS-A1-01)
    m_d = (t_d >= 0.8) & (t_d <= 3.2)
    ax1.plot(t_d[m_d], clk_d[m_d], label='V(clk) [500 MHz]', color='#003366', linestyle=':', lw=1.2)
    ax1.plot(t_d[m_d], va_d[m_d], label='V(a) [Flanco 0->1 a 1.1 ns]', color='#990000', linestyle='--', lw=1.2)
    ax1.plot(t_d[m_d], vdyn_d[m_d], label='V(dyn) [Nodo Interno]', color='#cc6600', lw=1.6)
    ax1.plot(t_d[m_d], vout_d[m_d], label='V(out) [Salida Dominó]', color='#006633', lw=2.0)
    ax1.axhline(0.5, color='gray', linestyle='--', lw=0.7)
    ax1.axvline(1.1, color='red', linestyle=':', alpha=0.6)
    ax1.axvline(2.0, color='blue', linestyle=':', alpha=0.6)
    ax1.set_ylabel('Tensión [V]')
    ax1.set_title('A. NAND3 Dinámica Footed (Conmutación dominó 0->1 gobernada por CLK y entrada A)', fontsize=10, fontweight='bold')
    ax1.grid(True)
    ax1.legend(loc='center right', fontsize=8.5)
    ax1.set_ylim(-0.05, 1.15)

    # Subplot 2: Estatica Equivalente con el MISMO estimulo (ENS-A1-07)
    m_s = (t_s >= 0.8) & (t_s <= 3.2)
    ax2.plot(t_s[m_s], va_s[m_s], label='V(a) [Mismo Estímulo]', color='#990000', linestyle='--', lw=1.2)
    ax2.plot(t_s[m_s], vout_s[m_s], label='V(out_stat) [Salida NAND3 Estática 1->0]', color='#7030a0', lw=2.0)
    ax2.axhline(0.5, color='gray', linestyle='--', lw=0.7)
    ax2.axvline(1.1, color='red', linestyle=':', alpha=0.6)
    ax2.set_ylabel('Tensión [V]')
    ax2.set_xlabel('Tiempo [ns]')
    ax2.set_title('B. NAND3 CMOS Estática Equivalente (Conmutación 1->0 al llegar entrada A, sin reloj)', fontsize=10, fontweight='bold')
    ax2.grid(True)
    ax2.legend(loc='center right', fontsize=8.5)
    ax2.set_ylim(-0.05, 1.15)
    ax2.set_xlim(0.8, 3.2)

    fig.suptitle('Comparación Temporal Sincronizada: NAND3 Dinámica Dominó vs Estática Equivalente (45nm HP)\nNetlists: nand3_dinamica_base.cir (ENS-A1-01) y nand3_estatica_mismo_estimulo.cir (ENS-A1-07)', y=0.98)
    fig.tight_layout()
    out_file = os.path.join(FIG_DIR, "fig2_act1_dinamica_vs_estatica.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generada Figura 2: {out_file}")

def generar_figura_3():
    """Figura 3: Perdida de Carga y Retencion con PDN Abierta (2ns vs 400ns)"""
    raw_2n = os.path.join(RAW_DIR, "nand3_dinamica_pdn_abierta_tclk2n.raw")
    raw_400n = os.path.join(RAW_DIR, "nand3_dinamica_pdn_abierta_tclk400n.raw")

    if not os.path.exists(raw_2n) or not os.path.exists(raw_400n):
        print("Error: falta un archivo raw para figura 3.")
        return

    r_2n = read_raw(raw_2n)
    r_400n = read_raw(raw_400n)

    t_2n = r_2n['data']['time'] * 1e9  # ns
    vdyn_2n = r_2n['data']['V(dyn)']

    t_400n = r_400n['data']['time'] * 1e9  # ns
    vdyn_400n = r_400n['data']['V(dyn)']
    vout_400n = r_400n['data']['V(out)']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.5))

    # Panel 1: Reloj normal Tclk = 2 ns
    m2 = t_2n <= 6.0
    ax1.plot(t_2n[m2], vdyn_2n[m2], color='#0066cc', lw=1.8, label=r'$V(dyn)$ ($T_{clk}=2\,$ns)')
    ax1.axhline(1.0, color='gray', linestyle=':', lw=0.8)
    ax1.axhline(0.48, color='red', linestyle='--', lw=1.0, label=r'$V_M=0.48\,$V (Umbral)')
    ax1.set_title(r'A. Reloj Normal: $T_{clk}=2\,$ns ($f=500\,$MHz)', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Tiempo [ns]')
    ax1.set_ylabel('Tensión en Nodo Dinámico [V]')
    ax1.set_ylim(0.4, 1.05)
    ax1.grid(True)
    ax1.legend(loc='lower left')
    ax1.annotate(r'$\Delta V_{eval} = 6.4\,$mV' + '\n(Retención Excelente)', xy=(1.0, 0.994), xytext=(1.5, 0.85),
                 arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8), fontsize=8.5)

    # Panel 2: Reloj lento Tclk = 400 ns (Ventana de 200 ns de evaluacion continua)
    ax2.plot(t_400n, vdyn_400n, color='#cc0000', lw=2.0, label=r'$V(dyn)$ ($T_{clk}=400\,$ns)')
    ax2.plot(t_400n, vout_400n, color='#006633', linestyle='--', lw=1.5, label=r'$V(out)$')
    ax2.axhline(0.48, color='red', linestyle='--', lw=1.0, label=r'$V_M=0.48\,$V (Umbral Estático)')
    ax2.set_title(r'B. Reloj Lento: $T_{clk}=400\,$ns (Eval. continua 200 ns)', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Tiempo [ns]')
    ax2.set_ylabel('Tensión [V]')
    ax2.set_ylim(0.0, 1.05)
    ax2.grid(True)
    ax2.legend(loc='center right')
    ax2.annotate(r'Caída por fugas: $\Delta V = 116.3\,$mV' + '\n' + r'$V(dyn)_{final}=0.884\,$V ($> V_M$ a $27^\circ$C)',
                 xy=(199.0, 0.884), xytext=(70.0, 0.65),
                 arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8), fontsize=8.5)

    fig.suptitle('Estudio de Retención con PDN Abierta ($V_c=0$): Impacto de la Frecuencia de Reloj\nNetlists: nand3_dinamica_pdn_abierta_tclk2n.cir y tclk400n.cir', y=0.98)
    fig.tight_layout()
    out_file = os.path.join(FIG_DIR, "fig3_act1_retencion_pdn_abierta.png")
    fig.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generada Figura 3: {out_file}")

def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    print("==================================================================")
    print("GENERANDO FIGURAS CIENTIFICAS DE PRODUCCION - ACTIVIDAD 1 (LD2)")
    print(f"Carpeta destino: {FIG_DIR}")
    print("==================================================================")
    generar_figura_1()
    generar_figura_2()
    generar_figura_3()
    print("==================================================================")

if __name__ == '__main__':
    main()
