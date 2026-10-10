import os
import numpy as np
import matplotlib.pyplot as plt

# Script de generacion de figuras cientificas para EXP-01 a EXP-05
# Autor: Leonardo Sait Yactayo Tolentino (LD3 - Microelectronica UNMSM)

from parse_raw import parse_ltspice_ascii_raw
from analisis_detallado import analyze_device

# Crear directorio de figuras si no existe
fig_dir = os.path.abspath('LD3_Yactayo/figuras')
os.makedirs(fig_dir, exist_ok=True)

# Configuracion estetica para publicaciones cientificas
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 12,
    'grid.alpha': 0.4,
    'grid.linestyle': '--',
    'lines.linewidth': 1.5,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

# Cargar y analizar datos
net_dir = os.path.abspath('LD3_Yactayo/simulaciones/netlists')
res_n = analyze_device(os.path.join(net_dir, 'dpt_nigbt_nom.raw'), 'N', 19.85e-6, 25.0e-6)
res_p = analyze_device(os.path.join(net_dir, 'dpt_pigbt_nom.raw'), 'P', 25.08e-6, 30.0e-6)

# ==============================================================================
# FIGURA 1: EXP-01 - Formas de Onda Globales DPT N-IGBT (XIRGBC20S, 19A)
# ==============================================================================
fig, axs = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
t_us = res_n['time_full'] * 1e6

axs[0].plot(t_us, res_n['vge_full'], color='#1f77b4')
axs[0].set_ylabel('$V_{GE}$ [V]')
axs[0].set_title('(a) Doble Pulso en Compuerta ($V_{GE}$)', loc='left')
axs[0].grid(True)
axs[0].set_ylim(-2, 22)

axs[1].plot(t_us, res_n['vce_full'], color='#d62728')
axs[1].set_ylabel('$V_{CE}$ [V]')
axs[1].set_title('(b) Tensión Colector-Emisor ($V_{CE}$)', loc='left')
axs[1].grid(True)
axs[1].set_ylim(-20, 450)

axs[2].plot(t_us, res_n['ic_full'], color='#2ca02c')
axs[2].set_ylabel('$I_C$ [A]')
axs[2].set_xlabel('Tiempo [$\\mu$s]')
axs[2].set_title('(c) Corriente de Colector ($I_C$)', loc='left')
axs[2].grid(True)
axs[2].set_ylim(-2, 32)

plt.suptitle('EXP-01: Formas de Onda Globales DPT — N-IGBT XIRGBC20S ($I_{C,nom} = 19\\text{ A}$)', y=0.99)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig1_dpt_nigbt_transitorios.png'))
plt.close(fig)
print("Figura 1 guardada: fig1_dpt_nigbt_transitorios.png")

# ==============================================================================
# FIGURA 2: EXP-02 - Formas de Onda Globales DPT P-IGBT (XPIGBT, 40A)
# ==============================================================================
fig, axs = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
t_us_p = res_p['time_full'] * 1e6

axs[0].plot(t_us_p, res_p['vge_full'], color='#1f77b4')
axs[0].set_ylabel('$V_{GE}$ [V]')
axs[0].set_title('(a) Doble Pulso en Compuerta ($V_{GE}$: $0\\to -15\\text{ V}$)', loc='left')
axs[0].grid(True)
axs[0].set_ylim(-22, 2)

axs[1].plot(t_us_p, -res_p['vce_full'], color='#d62728') # V_EC positivo o V_CE negativo
axs[1].set_ylabel('$V_{CE}$ [V]')
axs[1].set_title('(b) Tensión Colector-Emisor ($V_{CE}$ respecto a Emisor)', loc='left')
axs[1].grid(True)
axs[1].set_ylim(-450, 20)

axs[2].plot(t_us_p, res_p['ic_full'], color='#2ca02c')
axs[2].set_ylabel('$|I_C|$ [A]')
axs[2].set_xlabel('Tiempo [$\\mu$s]')
axs[2].set_title('(c) Magnitud de Corriente de Colector ($|I_C|$)', loc='left')
axs[2].grid(True)
axs[2].set_ylim(-2, 45)

plt.suptitle('EXP-02: Formas de Onda Globales DPT — P-IGBT XPIGBT ($I_{C,nom} = 40\\text{ A}$)', y=0.99)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig2_dpt_pigbt_transitorios.png'))
plt.close(fig)
print("Figura 2 guardada: fig2_dpt_pigbt_transitorios.png")

# ==============================================================================
# FIGURA 3: EXP-03 - Acercamiento a Conmutación de Apagado y Corriente de Cola
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

# Subplot 1: NIGBT
t_rel_n = (res_n['t_win'] - 19.85e-6) * 1e9 # ns desde comando de apagado
ax1.plot(t_rel_n, res_n['ic_win'], color='#2ca02c', label='$I_C(t)$')
ax1.axvline((res_n['t_tail'] - 19.85e-6)*1e9, color='orange', linestyle='--', label=f'Inicio Cola: $t_{{tail}}$\n$I_{{tail}} = {res_n["ic_tail"]:.2f}\\text{{ A}}$')
ax1.scatter([(res_n['t_tail'] - 19.85e-6)*1e9], [res_n['ic_tail']], color='red', zorder=5)
ax1.set_title('N-IGBT (19 A) — Transitorio de Apagado')
ax1.set_xlabel('Tiempo relativo $\\Delta t$ [ns]')
ax1.set_ylabel('Corriente de Colector $I_C$ [A]')
ax1.set_xlim(0, 1000)
ax1.set_ylim(-0.5, 21)
ax1.grid(True)
ax1.legend(loc='upper right')

# Subplot 2: PIGBT
t_rel_p = (res_p['t_win'] - 25.08e-6) * 1e9 # ns desde comando de apagado
ax2.plot(t_rel_p, res_p['ic_win'], color='#2ca02c', label='$|I_C(t)|$')
ax2.axvline((res_p['t_tail'] - 25.08e-6)*1e9, color='orange', linestyle='--', label=f'Inicio Cola: $t_{{tail}}$\n$I_{{tail}} = {res_p["ic_tail"]:.2f}\\text{{ A}}$')
ax2.scatter([(res_p['t_tail'] - 25.08e-6)*1e9], [res_p['ic_tail']], color='red', zorder=5)
ax2.set_title('P-IGBT (40 A) — Transitorio de Apagado')
ax2.set_xlabel('Tiempo relativo $\\Delta t$ [ns]')
ax2.set_ylabel('Magnitud de Corriente $|I_C|$ [A]')
ax2.set_xlim(0, 1000)
ax2.set_ylim(-0.5, 43)
ax2.grid(True)
ax2.legend(loc='upper right')

plt.suptitle('EXP-03: Detección y Caracterización de la Corriente de Cola ($I_{C,tail}$)', y=0.99)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig3_detalle_corriente_cola.png'))
plt.close(fig)
print("Figura 3 guardada: fig3_detalle_corriente_cola.png")

# ==============================================================================
# FIGURA 4: EXP-04 - Medicion de Retardo de Apagado td(off) (90% VGE a 90% IC)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 5.5), sharex=True)

# Graficar N-IGBT con cursores
t_ns_n = (res_n['t_win'] - 19.85e-6) * 1e9
ax1_twin = ax1.twinx()

p1 = ax1.plot(t_ns_n, res_n['vge_win'], color='#1f77b4', label='$V_{GE}(t)$')
p2 = ax1_twin.plot(t_ns_n, res_n['ic_win'], color='#2ca02c', label='$I_C(t)$')

# Cursores
t_vge90_rel = (res_n['t_vge90'] - 19.85e-6) * 1e9
t_ic90_rel  = (res_n['t_ic90'] - 19.85e-6) * 1e9
t_ic10_rel  = (res_n['t_ic10'] - 19.85e-6) * 1e9

ax1.axvline(t_vge90_rel, color='#1f77b4', linestyle=':')
ax1.axvline(t_ic90_rel, color='#2ca02c', linestyle=':')
ax1.axvline(t_ic10_rel, color='gray', linestyle=':')

# Anotacion td(off)
ax1.annotate('', xy=(t_vge90_rel, 10), xytext=(t_ic90_rel, 10),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
ax1.text(0.5*(t_vge90_rel + t_ic90_rel), 11, f'$t_{{d(off)}} = {res_n["td_off"]*1e9:.1f}\\text{{ ns}}$',
         ha='center', fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.6))

# Anotacion tf
ax1.annotate('', xy=(t_ic90_rel, 5), xytext=(t_ic10_rel, 5),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=1.2))
ax1.text(0.5*(t_ic90_rel + t_ic10_rel), 6, f'$t_f = {res_n["tf"]*1e9:.1f}\\text{{ ns}}$',
         ha='center', fontsize=9, color='purple')

ax1.set_ylabel('$V_{GE}$ [V]', color='#1f77b4')
ax1_twin.set_ylabel('$I_C$ [A]', color='#2ca02c')
ax1.set_title('(a) N-IGBT (19 A): Intervalo 90% $V_{GE}$ (13.5 V) a 90% $I_C$ (17.1 A)', loc='left')
ax1.set_xlim(0, 500)
ax1.grid(True)

# Graficar P-IGBT
t_ns_p = (res_p['t_win'] - 25.08e-6) * 1e9
ax2_twin = ax2.twinx()

p3 = ax2.plot(t_ns_p, res_p['vge_win'], color='#1f77b4', label='$V_{GE}(t)$')
p4 = ax2_twin.plot(t_ns_p, res_p['ic_win'], color='#2ca02c', label='$|I_C(t)|$')

t_vge90_p_rel = (res_p['t_vge90'] - 25.08e-6) * 1e9
t_ic90_p_rel  = (res_p['t_ic90'] - 25.08e-6) * 1e9
t_ic10_p_rel  = (res_p['t_ic10'] - 25.08e-6) * 1e9

ax2.axvline(t_vge90_p_rel, color='#1f77b4', linestyle=':')
ax2.axvline(t_ic90_p_rel, color='#2ca02c', linestyle=':')
ax2.axvline(t_ic10_p_rel, color='gray', linestyle=':')

ax2.annotate('', xy=(t_vge90_p_rel, -8), xytext=(t_ic90_p_rel, -8),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
ax2.text(0.5*(t_vge90_p_rel + t_ic90_p_rel), -7, f'$t_{{d(off)}} = {res_p["td_off"]*1e9:.1f}\\text{{ ns}}$',
         ha='center', fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.6))

ax2.annotate('', xy=(t_ic90_p_rel, -12), xytext=(t_ic10_p_rel, -12),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=1.2))
ax2.text(0.5*(t_ic90_p_rel + t_ic10_p_rel), -11, f'$t_f = {res_p["tf"]*1e9:.1f}\\text{{ ns}}$',
         ha='center', fontsize=9, color='purple')

ax2.set_ylabel('$V_{GE}$ [V]', color='#1f77b4')
ax2_twin.set_ylabel('$|I_C|$ [A]', color='#2ca02c')
ax2.set_xlabel('Tiempo relativo desde flanco de apagado $\\Delta t$ [ns]')
ax2.set_title('(b) P-IGBT (40 A): Intervalo 90% $V_{GE}$ (-13.5 V) a 90% $|I_C|$ (36.0 A)', loc='left')
ax2.set_xlim(0, 500)
ax2.grid(True)

plt.suptitle('EXP-04: Medición Normalizada del Retardo de Apagado $t_{d(off)}$ (90% a 90%)', y=0.99)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig4_medicion_cursores_tdoff.png'))
plt.close(fig)
print("Figura 4 guardada: fig4_medicion_cursores_tdoff.png")

# ==============================================================================
# FIGURA 5: EXP-05 - Potencia Instantanea y Energia de Apagado Eoff
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 5.5), sharex=True)

# Curva de potencia instantanea
ax1.plot(t_ns_n, res_n['p_inst'] * 1e-3, color='#d62728', label='N-IGBT (19 A)')
ax1.plot(t_ns_p, res_p['p_inst'] * 1e-3, color='#9467bd', label='P-IGBT (40 A)')
ax1.set_ylabel('Potencia $p(t)$ [kW]')
ax1.set_title('(a) Potencia Instantánea Disipada durante el Apagado ($p(t) = v_{CE} \\cdot i_C$)', loc='left')
ax1.grid(True)
ax1.legend(loc='upper right')

# Curva de energia acumulada
e_cum_n = np.cumsum(res_n['p_inst'] * np.gradient(res_n['t_win'])) * 1e6 # uJ
e_cum_p = np.cumsum(res_p['p_inst'] * np.gradient(res_p['t_win'])) * 1e6 # uJ

ax2.plot(t_ns_n, e_cum_n, color='#d62728', label=f'N-IGBT: $E_{{off}} = {res_n["e_off_total"]*1e6:.1f}\\ \\mu\\text{{J}}$ (Cola: {res_n["pct_e_tail"]:.1f}%)')
ax2.plot(t_ns_p, e_cum_p, color='#9467bd', label=f'P-IGBT: $E_{{off}} = {res_p["e_off_total"]*1e6:.1f}\\ \\mu\\text{{J}}$ (Cola: {res_p["pct_e_tail"]:.1f}%)')

ax2.set_xlabel('Tiempo relativo desde flanco de apagado $\\Delta t$ [ns]')
ax2.set_ylabel('Energía Acumulada [$\\mu$J]')
ax2.set_title('(b) Integración Temporal de Pérdidas de Conmutación ($E_{off} = \\int p(t) dt$)', loc='left')
ax2.set_xlim(0, 1000)
ax2.grid(True)
ax2.legend(loc='lower right')

plt.suptitle('EXP-05: Dinámica de Pérdidas de Apagado y Partición de Energía de Cola', y=0.99)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig5_potencia_energia_apagado.png'))
plt.close(fig)
print("Figura 5 guardada: fig5_potencia_energia_apagado.png")

print("\nTodas las figuras cientificas generadas exitosamente a 300 DPI.")
