# -*- coding: utf-8 -*-
"""
Generador de Figuras Científicas — Actividad 4 (LD2)
Microelectrónica y Sistemas Nanoelectrónicos — FIEE UNMSM 2026-II

Genera tres figuras académicas a 300 DPI con rotulación estricta, unidades físicas,
leyendas precisas y ausencia total de metadatos administrativos internos:

1. fig1_act4_monotonicidad_cascada.png:
   Análisis de monotonicidad y regímenes de operación en cascada de dos etapas.
   - Régimen A: Cascada directa sin inversor (violación de monotonicidad, caída de 353.8 mV).
   - Régimen B: Cascada con inversor dominó bajo entradas activas (descarga funcional legítima).
   - Régimen C: Cascada con inversor dominó y bloqueo (retención intacta de VDD con X=0).

2. fig2_act4_pulso_x_descendente.png:
   Impacto de entrada externa no monótona (X: 1 -> 0 a 2.50 ns) durante evaluación activa.
   - Comparación homóloga: Referencia X=0 vs Ensayo de pulso descendente.
   - Demostración de que dyn2 se descargó ANTES de la caída de X.
   - Error lógico durante el ciclo de evaluación por imposibilidad de recuperar carga.

3. fig3_act4_footed_vs_unfooted_skew.png:
   Sensibilidad al skew de reloj en cascada dominó de 3 etapas (Footed vs Unfooted).
   - Panel A: Retardo de propagación total t_del vs Tskew.
   - Panel B: Pico de corriente de alimentación Ipk vs Tskew.
   - Datos verificados en los cinco puntos (-50, 0, 50, 100, 200 ps).
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURACIÓN DE ESTILO CIENTÍFICO / IEEE
# ==============================================================================
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
ACT4_DIR = os.path.dirname(SCRIPT_DIR)
PROJ_DIR = os.path.dirname(ACT4_DIR)
RAW_ACT4_DIR = os.path.join(ACT4_DIR, "resultados", "raw")
DATOS_DIR = os.path.join(ACT4_DIR, "resultados", "datos")
FIG_DIR = os.path.join(ACT4_DIR, "figuras")
LATEX_FIG_DIR = os.path.join(PROJ_DIR, "informe_latex", "figuras")
LAB4_RAW_DIR = "G:/Proyectos/Micro/laboratorio4"

PARSER_DIR = os.path.join(PROJ_DIR, "scripts", "lectura_resultados")
sys.path.insert(0, PARSER_DIR)
from parse_spice_raw import read_raw

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(LATEX_FIG_DIR, exist_ok=True)

# Paleta cromática formal
C_CLK = '#555555'       # Gris oscuro para señal de sincronismo
C_DYN1 = '#2b5c8f'      # Azul acero para etapa 1
C_OUT1 = '#137333'      # Verde bosque para salida estática etapa 1
C_DYN2 = '#b80000'      # Rojo carmesí para nodo dinámico etapa 2
C_OUT2 = '#7b1fa2'      # Púrpura para salida estática etapa 2
C_VX = '#d97706'        # Ámbar oscuro para entrada externa X
C_FOOT = '#1f77b4'      # Azul estándar para footed
C_UNFOOT = '#d62728'    # Rojo estándar para unfooted

def cargar_metricas():
    json_path = os.path.join(DATOS_DIR, "act4_metricas.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ==============================================================================
# FIGURA 1: MONOTONICIDAD Y REGÍMENES DE OPERACIÓN EN CASCADA
# ==============================================================================
def generar_figura_1():
    """Genera fig1_act4_monotonicidad_cascada.png con 3 paneles para los regímenes A, B y C."""
    path_a = os.path.join(LAB4_RAW_DIR, "Tarea 1 Sin Inversor.raw")
    path_b = os.path.join(LAB4_RAW_DIR, "Paso 2 y 3 Con Inversor.raw")
    path_c = os.path.join(RAW_ACT4_DIR, "a4_control1_bloqueo_inversor.raw")

    raw_a = read_raw(path_a)
    raw_b = read_raw(path_b)
    raw_c = read_raw(path_c)

    fig, axes = plt.subplots(3, 1, figsize=(8.0, 7.5), sharex=True, gridspec_kw={'hspace': 0.32})

    t_min, t_max = 1.85, 3.15

    # Panel 1: Régimen A — Cascada Directa sin Inversor (A=B=X=1)
    ax = axes[0]
    t = raw_a['data']['time'] * 1e9
    m = (t >= t_min) & (t <= t_max)
    t_m = t[m]

    ax.axvspan(2.0, 3.0, color='#e8f0fe', alpha=0.5, label='Fase de Evaluación ($CLK=1$)')
    ax.plot(t_m, raw_a['data']['V(clk)'][m], label=r'$V(CLK)$', color=C_CLK, linestyle='--', linewidth=1.4)
    ax.plot(t_m, raw_a['data']['V(dyn1)'][m], label=r'$V(dyn1)$ (Etapa 1)', color=C_DYN1, linewidth=1.8)
    ax.plot(t_m, raw_a['data']['V(dyn2)'][m], label=r'$V(dyn2)$ (Etapa 2)', color=C_DYN2, linewidth=2.0)

    ax.annotate(r'$V_{dyn2,\min} = 0.646\,\text{V}$' + '\n' + r'($\Delta V = 353.8\,\text{mV}$)',
                xy=(2.15, 0.654), xytext=(2.32, 0.36),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff2cc', edgecolor='#d6b656', alpha=0.9))

    ax.set_title(r'(a) Cascada Directa Sin Inversor ($A=B=1, X=1$): Activación Prematura y Descarga Espuria',
                 loc='left', fontweight='bold', fontsize=11.5)
    ax.set_ylabel('Tensión (V)')
    ax.set_ylim(-0.08, 1.25)
    ax.grid(True)
    ax.legend(loc='upper right', ncol=4, framealpha=0.92, fontsize=9.5)

    # Panel 2: Régimen B — Cascada con Inversor Dominó (A=B=X=1)
    ax = axes[1]
    t = raw_b['data']['time'] * 1e9
    m = (t >= t_min) & (t <= t_max)
    t_m = t[m]

    ax.axvspan(2.0, 3.0, color='#e8f0fe', alpha=0.5)
    ax.plot(t_m, raw_b['data']['V(clk)'][m], label=r'$V(CLK)$', color=C_CLK, linestyle='--', linewidth=1.4)
    ax.plot(t_m, raw_b['data']['V(dyn1)'][m], label=r'$V(dyn1)$', color=C_DYN1, linewidth=1.6)
    ax.plot(t_m, raw_b['data']['V(out1)'][m], label=r'$V(out1)$ (Inversor Dominó)', color=C_OUT1, linewidth=1.8)
    ax.plot(t_m, raw_b['data']['V(dyn2)'][m], label=r'$V(dyn2)$', color=C_DYN2, linewidth=2.0)

    ax.annotate(r'$out1$ monótona ($0 \to 1$)' + '\n' + r'Descarga activa a $\approx 0\,\text{V}$',
                xy=(2.07, 0.35), xytext=(2.25, 0.42),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#e1d5e7', edgecolor='#9673a6', alpha=0.9))

    ax.set_title(r'(b) Cascada con Inversor Dominó ($A=B=1, X=1$): Conmutación Funcional Activa ($out1 \cdot X = 1$)',
                 loc='left', fontweight='bold', fontsize=11.5)
    ax.set_ylabel('Tensión (V)')
    ax.set_ylim(-0.08, 1.25)
    ax.grid(True)
    ax.legend(loc='upper right', ncol=4, framealpha=0.92, fontsize=9.5)

    # Panel 3: Régimen C — Cascada con Inversor Dominó y Bloqueo (A=B=1, X=0)
    ax = axes[2]
    t = raw_c['data']['time'] * 1e9
    m = (t >= t_min) & (t <= t_max)
    t_m = t[m]

    ax.axvspan(2.0, 3.0, color='#e8f0fe', alpha=0.5)
    ax.plot(t_m, raw_c['data']['V(clk)'][m], label=r'$V(CLK)$', color=C_CLK, linestyle='--', linewidth=1.4)
    ax.plot(t_m, raw_c['data']['V(out1)'][m], label=r'$V(out1)$', color=C_OUT1, linewidth=1.6)
    ax.plot(t_m, raw_c['data']['V(dyn2)'][m], label=r'$V(dyn2)$', color=C_DYN2, linewidth=2.0)
    ax.plot(t_m, raw_c['data']['V(out2)'][m], label=r'$V(out2)$ (Salida Dominó)', color=C_OUT2, linewidth=1.8)

    ax.annotate(r'$V(dyn2) \geq 1.000\,\text{V}$ (Retenido)' + '\n' + r'$V(out2) \approx 0.0\,\text{V}$ ($26.8\,\text{nV}$)',
                xy=(2.50, 1.04), xytext=(2.32, 0.42),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#d5e8d4', edgecolor='#82b366', alpha=0.9))

    ax.set_title(r'(c) Cascada con Inversor y Bloqueo ($A=B=1, X=0$): Retención de $V_{DD}$ y Bloqueo de PDN2',
                 loc='left', fontweight='bold', fontsize=11.5)
    ax.set_xlabel('Tiempo (ns)')
    ax.set_ylabel('Tensión (V)')
    ax.set_ylim(-0.08, 1.25)
    ax.set_xlim(t_min, t_max)
    ax.grid(True)
    ax.legend(loc='upper right', ncol=4, framealpha=0.92, fontsize=9.5)

    out_png = os.path.join(FIG_DIR, "fig1_act4_monotonicidad_cascada.png")
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(LATEX_FIG_DIR, "fig1_act4_monotonicidad_cascada.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generada Figura 1: {out_png}")

# ==============================================================================
# FIGURA 2: IMPACTO DE ENTRADA X NO MONÓTONA (PULSO DESCENDENTE)
# ==============================================================================
def generar_figura_2():
    """Genera fig2_act4_pulso_x_descendente.png comparando X=0 estático vs pulso X descendente."""
    path_ref = os.path.join(RAW_ACT4_DIR, "a4_control3_x_estatico_cero.raw")
    path_pulse = os.path.join(RAW_ACT4_DIR, "a4_control2_pulso_x_descendente.raw")

    raw_ref = read_raw(path_ref)
    raw_pulse = read_raw(path_pulse)

    fig, axes = plt.subplots(2, 1, figsize=(8.0, 5.8), sharex=True, gridspec_kw={'hspace': 0.32})

    t_min, t_max = 1.90, 3.10

    # Panel Superior: Referencia con X=0 Estático
    ax = axes[0]
    t = raw_ref['data']['time'] * 1e9
    m = (t >= t_min) & (t <= t_max)
    t_m = t[m]

    ax.axvspan(2.0, 3.0, color='#e8f0fe', alpha=0.5, label='Fase de Evaluación')
    ax.plot(t_m, raw_ref['data']['V(clk)'][m], label=r'$V(CLK)$', color=C_CLK, linestyle='--', linewidth=1.4)
    ax.plot(t_m, raw_ref['data']['V(x)'][m], label=r'$V(X)=0\,\text{V}$', color=C_VX, linestyle=':', linewidth=1.8)
    ax.plot(t_m, raw_ref['data']['V(out1)'][m], label=r'$V(out1)$', color=C_OUT1, linewidth=1.6)
    ax.plot(t_m, raw_ref['data']['V(dyn2)'][m], label=r'$V(dyn2)$', color=C_DYN2, linewidth=2.0)
    ax.plot(t_m, raw_ref['data']['V(out2)'][m], label=r'$V(out2)$', color=C_OUT2, linewidth=1.8)

    ax.annotate('Operación Correcta:\n' + r'$V(dyn2) = 1.039\,\text{V}$' + '\n' + r'$V(out2) \approx 0.0\,\text{V}$',
                xy=(2.60, 1.04), xytext=(2.40, 0.40),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#d5e8d4', edgecolor='#82b366', alpha=0.9))

    ax.set_title(r'(a) Control de Referencia ($X=0$ Estático): Salida Esperada $out2 = out1 \cdot X = 0$',
                 loc='left', fontweight='bold', fontsize=11.5)
    ax.set_ylabel('Tensión (V)')
    ax.set_ylim(-0.08, 1.32)
    ax.grid(True)
    ax.legend(loc='upper right', ncol=6, fontsize=9.0, framealpha=0.92)

    # Panel Inferior: Pulso Descendente en X (1 -> 0 a 2.50 ns)
    ax = axes[1]
    t = raw_pulse['data']['time'] * 1e9
    m = (t >= t_min) & (t <= t_max)
    t_m = t[m]

    ax.axvspan(2.0, 3.0, color='#e8f0fe', alpha=0.5)
    ax.plot(t_m, raw_pulse['data']['V(clk)'][m], label=r'$V(CLK)$', color=C_CLK, linestyle='--', linewidth=1.4)
    ax.plot(t_m, raw_pulse['data']['V(x)'][m], label=r'$V(X)$ ($1 \to 0$ a $2.5\,\text{ns}$)', color=C_VX, linewidth=1.8)
    ax.plot(t_m, raw_pulse['data']['V(out1)'][m], label=r'$V(out1)$', color=C_OUT1, linewidth=1.6)
    ax.plot(t_m, raw_pulse['data']['V(dyn2)'][m], label=r'$V(dyn2)$', color=C_DYN2, linewidth=2.0)
    ax.plot(t_m, raw_pulse['data']['V(out2)'][m], label=r'$V(out2)$', color=C_OUT2, linewidth=1.8)

    # Línea vertical en el instante de caída de X
    ax.axvline(2.50, color='#b80000', linestyle='-.', linewidth=1.4, alpha=0.85)

    # Anotación 1: Descarga previa
    ax.annotate('Descarga completa previa\n' + r'($dyn2 \to 0\,\text{V}$ antes de $2.5\,\text{ns}$)',
                xy=(2.12, 0.05), xytext=(2.03, 0.40),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff2cc', edgecolor='#d6b656', alpha=0.9))

    # Anotación 2: Error lógico en el ciclo
    ax.annotate('Error lógico durante el ciclo de evaluación:\n' +
                r'Sin recarga ($CLK=1 \rightarrow M_{p2}$ OFF)' + '\n' +
                r'$V(out2) \approx 1.0\,\text{V}$ (esperado: $0.0\,\text{V}$)',
                xy=(2.75, 1.00), xytext=(2.42, 0.38),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#f8cecc', edgecolor='#b85450', alpha=0.9))

    ax.set_title(r'(b) Entrada No Monótona ($X: 1 \to 0$ a $t=2.50\,\text{ns}$): Pérdida Irreversible de Carga en Evaluación',
                 loc='left', fontweight='bold', fontsize=11.5)
    ax.set_xlabel('Tiempo (ns)')
    ax.set_ylabel('Tensión (V)')
    ax.set_ylim(-0.08, 1.32)
    ax.set_xlim(t_min, t_max)
    ax.grid(True)
    ax.legend(loc='upper right', ncol=5, fontsize=9.0, framealpha=0.92)

    out_png = os.path.join(FIG_DIR, "fig2_act4_pulso_x_descendente.png")
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(LATEX_FIG_DIR, "fig2_act4_pulso_x_descendente.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generada Figura 2: {out_png}")

# ==============================================================================
# FIGURA 3: FOOTED VS UNFOOTED CON BARRIDO DE SKEW DE RELOJ
# ==============================================================================
def generar_figura_3():
    """Genera fig3_act4_footed_vs_unfooted_skew.png con dos paneles (Retardo e Ipk vs Tskew)."""
    # Datos oficiales de simulación extraídos de los LOG
    tskew = np.array([-50.0, 0.0, 50.0, 100.0, 200.0])
    
    tdel_foot = np.array([77.20, 77.21, 125.47, 226.68, 426.91])
    tdel_unfoot = np.array([66.46, 66.47, 95.12, 130.81, 171.48])

    ipk_foot = np.array([113.80, 318.85, 110.56, 110.56, 110.56])
    ipk_unfoot = np.array([326.30, 332.91, 110.57, 160.57, 214.63])

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.2), gridspec_kw={'wspace': 0.28})

    # Panel A: Retardo de propagación total vs Tskew
    ax = axes[0]
    ax.plot(tskew, tdel_foot, marker='s', markersize=7, color=C_FOOT,
            linestyle='-', label=r'Footed (3 etapas con $M_f$)', linewidth=2.0)
    ax.plot(tskew, tdel_unfoot, marker='o', markersize=7, color=C_UNFOOT,
            linestyle='--', label=r'Unfooted (etapas 2 y 3 sin $M_f$)', linewidth=2.0)

    ax.annotate(r'$\Delta t = -10.74\,\text{ps}$' + '\n(-13.9% ahorro)',
                xy=(0, 66.47), xytext=(-45, 145),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#d5e8d4', edgecolor='#82b366', alpha=0.9))

    ax.annotate('Footed degrada por espera:\n' + r'$t_{del} = 426.9\,\text{ps}$',
                xy=(200, 426.91), xytext=(65, 360),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#e8f0fe', edgecolor='#b0c4de', alpha=0.9))

    ax.text(0.04, 0.52, 'Sensibilidad a difusión (Control 4, Footed, 0 ps):\n' +
            r'$t_{del}$ pasa de $77.21\,\text{ps}$ a $89.90\,\text{ps}$ ($+16.4\%$)',
            transform=ax.transAxes, fontsize=9.2,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#f5f5f5', edgecolor='#cccccc', alpha=0.85))

    ax.set_title(r'(a) Retardo Total de Propagación ($t_{del}$)', loc='left', fontweight='bold', fontsize=11.5)
    ax.set_xlabel('Skew de Reloj $T_{skew}$ (ps)')
    ax.set_ylabel('Retardo Total $t_{del}$ (ps)')
    ax.set_xticks(tskew)
    ax.set_xlim(-65, 215)
    ax.set_ylim(40, 470)
    ax.grid(True)
    ax.legend(loc='upper left', framealpha=0.9, fontsize=9.5)

    # Panel B: Pico de corriente de alimentación vs Tskew
    ax = axes[1]
    ax.plot(tskew, ipk_foot, marker='s', markersize=7, color=C_FOOT,
            linestyle='-', label='Footed', linewidth=2.0)
    ax.plot(tskew, ipk_unfoot, marker='o', markersize=7, color=C_UNFOOT,
            linestyle='--', label='Unfooted', linewidth=2.0)

    ax.annotate('Precarga paralela síncrona\n' + r'($3 \times \approx 110\,\mu\text{A}$)',
                xy=(0, 332.91), xytext=(15, 335),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff2cc', edgecolor='#d6b656', alpha=0.9))

    ax.annotate(r'$\Delta I_{pk} = +104.07\,\mu\text{A}$' + '\n(+94.1% elevación)',
                xy=(200, 214.63), xytext=(70, 255),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=10.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#f8cecc', edgecolor='#b85450', alpha=0.9))

    ax.annotate('Skew negativo no seguro:\n' + r'$I_{pk} = 326.3\,\mu\text{A}$ (Unfooted)',
                xy=(-50, 326.30), xytext=(-62, 385),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=9.5,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#fce5cd', edgecolor='#e69138', alpha=0.9))

    ax.set_title(r'(b) Pico de Corriente de Alimentación ($I_{pk}$)', loc='left', fontweight='bold', fontsize=11.5)
    ax.set_xlabel('Skew de Reloj $T_{skew}$ (ps)')
    ax.set_ylabel(r'Pico de Corriente de Alimentación $I_{pk}$ ($\mu\text{A}$)')
    ax.set_xticks(tskew)
    ax.set_xlim(-65, 215)
    ax.set_ylim(80, 440)
    ax.grid(True)
    ax.legend(loc='lower left', framealpha=0.9, fontsize=9.5)

    out_png = os.path.join(FIG_DIR, "fig3_act4_footed_vs_unfooted_skew.png")
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(LATEX_FIG_DIR, "fig3_act4_footed_vs_unfooted_skew.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generada Figura 3: {out_png}")

if __name__ == '__main__':
    print("Iniciando generación de figuras científicas para Actividad 4...")
    generar_figura_1()
    generar_figura_2()
    generar_figura_3()
    print("Todas las figuras de Actividad 4 fueron generadas exitosamente en act4/figuras/")
