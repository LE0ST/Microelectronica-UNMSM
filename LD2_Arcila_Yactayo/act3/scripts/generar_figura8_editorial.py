# -*- coding: utf-8 -*-
"""
generar_figura8_editorial.py
Genera las dos figuras de la Figura 8 (Actividad 3) con acabado editorial balanceado:
- fig3_act3_contencion_penalizacion.png: 2 subpaneles verticales (vs Wkp y vs r)
- fig4_act3_ventana_viabilidad.png: panel con doble eje Y de altura útil equivalente
Ambas se guardan tanto en act3/figuras/ como en informe_latex/figuras/.
Utiliza exclusivamente los datos de simulacion reales de act3_contencion_metricas.json.
"""

import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT3_DIR = os.path.dirname(SCRIPT_DIR)
LD2_DIR = os.path.dirname(ACT3_DIR)
DATOS_DIR = os.path.join(ACT3_DIR, "resultados", "datos")
FIG_ACT3_DIR = os.path.join(ACT3_DIR, "figuras")
FIG_LATEX_DIR = os.path.join(LD2_DIR, "informe_latex", "figuras")

def generar():
    json_path = os.path.join(DATOS_DIR, "act3_contencion_metricas.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    barrido_coarse = data["barrido_grueso"]
    barrido_ref = data["refinamiento_frontera_1nm"]
    cruce_viabilidad = data["cruce_viabilidad_conjunta"]

    colors = {
        'primary': '#1E3A8A',    # Azul oscuro
        'secondary': '#0284C7',  # Azul cielo
        'accent': '#D9534F',     # Rojo suave
        'success': '#15803D',    # Verde bosque
        'neutral': '#374151',    # Gris oscuro
        'grid': '#E5E7EB',       # Gris tenue
        'highlight': '#D97706'   # Ámbar
    }

    w_max_viable = max(p["Wkp_nm"] for p in barrido_ref if p["cumple_contencion_menor_10pct"])
    r_max_viable = max(p["r"] for p in barrido_ref if p["cumple_contencion_menor_10pct"])

    w_valid = [p["Wkp_nm"] for p in barrido_coarse if p["penalizacion_pct"] is not None]
    pen_valid = [p["penalizacion_pct"] for p in barrido_coarse if p["penalizacion_pct"] is not None]

    w_ref_pts = [p["Wkp_nm"] for p in barrido_ref]
    pen_ref_pts = [p["penalizacion_pct"] for p in barrido_ref]

    r_valid = [p["r"] for p in barrido_coarse if p["penalizacion_pct"] is not None]
    r_ref_pts = [p["r"] for p in barrido_ref]

    # =========================================================================
    # 1. FIGURA IZQUIERDA: 2 PANELES VERTICALES (vs Wkp y vs r)
    # =========================================================================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.8, 6.2), dpi=300)

    # Subpanel A1: Penalización vs Wkp
    ax1.plot(w_valid, pen_valid, 'o--', color=colors['primary'], label='Malla Gruesa [10.5 - 135 nm]', lw=2.0, ms=6, alpha=0.85)
    ax1.plot(w_ref_pts, pen_ref_pts, 's-', color=colors['accent'], label='Refinamiento 1 nm [30 - 45 nm]', lw=2.2, ms=5)
    ax1.axhline(10.0, color='red', ls=':', lw=2.2, label='Límite Estricto (+10.0%)')
    ax1.axvspan(10.5, w_max_viable, color='green', alpha=0.12, label=f'Zona Viable ($W_{{kp}} \\leq {w_max_viable:.0f}\\,\\mathrm{{nm}}$)')
    ax1.axvspan(w_max_viable, 140.0, color='red', alpha=0.08)
    ax1.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Penalización $\\Delta t_{pHL}$ (%)', fontsize=13, fontweight='bold')
    ax1.set_title('(a1) Penalización vs Ancho Geométrico $W_{kp}$', fontsize=13.5, fontweight='bold', color=colors['primary'], pad=4)
    ax1.set_xlim(5, 140)
    ax1.set_ylim(0, 140)
    ax1.legend(fontsize=10.5, loc='upper left', framealpha=0.92)
    ax1.grid(True, linestyle='--', alpha=0.55)
    ax1.tick_params(labelsize=11.5)

    # Subpanel A2: Penalización vs r
    ax2.plot(r_valid, pen_valid, 'o--', color=colors['primary'], label='Malla Gruesa', lw=2.0, ms=6, alpha=0.85)
    ax2.plot(r_ref_pts, pen_ref_pts, 's-', color=colors['accent'], label='Refinamiento', lw=2.2, ms=5)
    ax2.axhline(10.0, color='red', ls=':', lw=2.2, label='Límite (+10.0%)')
    ax2.axvspan(10.5/67.5, r_max_viable, color='green', alpha=0.12, label=f'Zona Viable ($r \\leq {r_max_viable:.3f}$)')
    ax2.axvspan(r_max_viable, 2.05, color='red', alpha=0.08)
    ax2.set_xlabel(r'Razón de Aspecto $r = W_{kp}/(67.5\,\mathrm{nm})$', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Penalización $\\Delta t_{pHL}$ (%)', fontsize=13, fontweight='bold')
    ax2.set_title('(a2) Penalización vs Razón de Aspecto $r$', fontsize=13.5, fontweight='bold', color=colors['primary'], pad=4)
    ax2.set_xlim(0.1, 2.05)
    ax2.set_ylim(0, 140)
    ax2.legend(fontsize=10.5, loc='upper left', framealpha=0.92)
    ax2.grid(True, linestyle='--', alpha=0.55)
    ax2.tick_params(labelsize=11.5)

    plt.tight_layout(pad=0.6)
    out1_act3 = os.path.join(FIG_ACT3_DIR, "figura_contencion_penalizacion_vs_r.png")
    out1_latex = os.path.join(FIG_LATEX_DIR, "fig3_act3_contencion_penalizacion.png")
    fig.savefig(out1_act3, bbox_inches='tight')
    fig.savefig(out1_latex, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Generado: {out1_latex}")

    # =========================================================================
    # 2. FIGURA DERECHA: VENTANA DE VIABILIDAD CONJUNTA (Doble Eje Y)
    # =========================================================================
    fig2, ax = plt.subplots(figsize=(6.2, 6.2), dpi=300)
    w_vals = [p["Wkp_nm"] for p in cruce_viabilidad]
    ret_vals = [p["Vdyn_end_V"] for p in cruce_viabilidad]
    pen_vals = [p["penalizacion_pct"] if p["penalizacion_pct"] is not None else 150.0 for p in cruce_viabilidad]

    ax.plot(w_vals, ret_vals, 'o-', color=colors['success'], lw=2.2, ms=6, label=r'Retención $V_{dyn}(1\,\mu\mathrm{s})$ (Eje Izq.)')
    ax.axhline(0.90, color=colors['success'], ls='--', lw=1.8, label='Umbral Mín. Retención (0.90 V)')
    ax.set_ylabel(r'Tensión de Retención $V_{dyn}(1\,\mu\mathrm{s})$ (V)', fontsize=13, fontweight='bold', color=colors['success'])
    ax.tick_params(axis='y', labelcolor=colors['success'], labelsize=11.5)
    ax.set_ylim(0.80, 1.05)
    ax.set_xlabel(r'Ancho del Keeper $W_{kp}$ (nm)', fontsize=13, fontweight='bold')
    ax.tick_params(axis='x', labelsize=11.5)

    ax_twin = ax.twinx()
    ax_twin.plot(w_vals, pen_vals, 's-', color=colors['accent'], lw=2.2, ms=6, label=r'Contención $\Delta t_{pHL}$ (Eje Der.)')
    ax_twin.axhline(10.0, color=colors['accent'], ls=':', lw=1.8, label='Límite Máx. Contención (+10.0%)')
    ax_twin.set_ylabel('Penalización de Retardo $\\Delta t_{pHL}$ (%)', fontsize=13, fontweight='bold', color=colors['accent'])
    ax_twin.tick_params(axis='y', labelcolor=colors['accent'], labelsize=11.5)
    ax_twin.set_ylim(0, 140)

    # Ventana viable sombreada
    ax.axvspan(10.5, w_max_viable, color='#A7F3D0', alpha=0.40, label=f'Ventana Viable: $W_{{kp}} \\in [10.5, {w_max_viable:.0f}]\\,\\mathrm{{nm}}$')
    ax.set_title('(b) Ventana de Viabilidad Conjunta\nRetención vs Contención (45nm HP @ 85°C)', fontsize=13.5, fontweight='bold', color=colors['primary'], pad=6)
    ax.set_xlim(5, 140)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='center left', bbox_to_anchor=(0.04, 0.50), fontsize=10.5, framealpha=0.92)
    ax.grid(True, linestyle='--', alpha=0.55)

    plt.tight_layout(pad=0.6)
    out2_act3 = os.path.join(FIG_ACT3_DIR, "figura_ventana_viabilidad_hp_85C.png")
    out2_latex = os.path.join(FIG_LATEX_DIR, "fig4_act3_ventana_viabilidad.png")
    fig2.savefig(out2_act3, bbox_inches='tight')
    fig2.savefig(out2_latex, bbox_inches='tight')
    plt.close(fig2)
    print(f"[OK] Generado: {out2_latex}")

if __name__ == "__main__":
    generar()
