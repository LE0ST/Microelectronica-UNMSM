"""
Script para generar las 4 figuras requeridas en la Guía de Laboratorio 1
(Lógica CMOS Estática - UNMSM FIEE)
Autores: Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 13,
    'figure.autolayout': True,
    'grid.alpha': 0.5,
    'grid.linestyle': '--'
})

output_dir = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\informe_latex\figuras"
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------------------
# FIGURA 1: Familia de curvas VTC (Actividad 1)
# -------------------------------------------------------------
print("Generando Figura 1: Familia VTC...")
vtc_raw = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\simulaciones\A1_Inversor_VTC\A1_VTC.raw"

with open(vtc_raw, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

val_idx = 0
for idx, line in enumerate(lines):
    if line.startswith("Values:"):
        val_idx = idx + 1
        break

data_lines = lines[val_idx:]
n_vars = 14
n_pts = 501
steps_beta = [1.0, 1.5, 2.0, 2.5, 3.0]

vin_all = []
vout_all = []
cur_vin, cur_vout = [], []

i = 0
while i < len(data_lines):
    parts = data_lines[i].split()
    if len(parts) >= 2:
        vin_val = float(parts[1])
        parts_out = data_lines[i+2].split()
        vout_val = float(parts_out[0])
        cur_vin.append(vin_val)
        cur_vout.append(vout_val)
        i += n_vars
        if len(cur_vin) == n_pts:
            vin_all.append(np.array(cur_vin))
            vout_all.append(np.array(cur_vout))
            cur_vin, cur_vout = [], []
    else:
        i += 1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for b_idx, b in enumerate(steps_beta):
    v_in = vin_all[b_idx]
    v_out = vout_all[b_idx]
    ax1.plot(v_in, v_out, label=f'$\\beta = {b:.1f}$', color=colors[b_idx], linewidth=1.8)
    
    # Derivada
    d_vout = np.gradient(v_out, v_in)
    ax2.plot(v_in, d_vout, label=f'$\\beta = {b:.1f}$', color=colors[b_idx], linewidth=1.8)

# Recta Vin = Vout
ax1.plot([0, 1], [0, 1], 'k--', alpha=0.6, linewidth=1, label='$V_{out} = V_{in}$')
ax1.set_xlabel('Voltaje de Entrada, $V_{in}$ [V]')
ax1.set_ylabel('Voltaje de Salida, $V_{out}$ [V]')
ax1.set_title('(a) Familia de Curvas VTC')
ax1.set_xlim(0, 1.0)
ax1.set_ylim(-0.02, 1.02)
ax1.grid(True)
ax1.legend(loc='upper right')

# Línea pendiente = -1
ax2.axhline(-1.0, color='black', linestyle=':', linewidth=1.2, label='Pendiente = -1 ($V_{IL}, V_{IH}$)')
ax2.set_xlabel('Voltaje de Entrada, $V_{in}$ [V]')
ax2.set_ylabel('Ganancia $d(V_{out})/d(V_{in})$ [V/V]')
ax2.set_title('(b) Derivada y Pendiente Crítica')
ax2.set_xlim(0.2, 0.8)
ax2.set_ylim(-7.0, 0.5)
ax2.grid(True)
ax2.legend(loc='lower left')

fig.suptitle('Caracterización de la VTC - Inversor CMOS 45 nm HP ($V_{DD} = 1.0$ V)', fontweight='bold')
plt.savefig(os.path.join(output_dir, "fig1_vtc_familia.png"))
plt.close()

# -------------------------------------------------------------
# FIGURA 2: Retardo vs Cload (Actividad 2)
# -------------------------------------------------------------
print("Generando Figura 2: Retardo vs Cload...")
cload_fF = np.array([1, 2, 3, 4, 5, 6, 7, 8])
tphl_ps = np.array([5.464, 7.881, 10.256, 12.613, 14.960, 17.300, 19.638, 21.972])
tplh_ps = np.array([3.580, 4.931, 6.272, 7.612, 8.948, 10.282, 11.617, 12.950])
tp_ps = (tphl_ps + tplh_ps) / 2.0

# Ajuste lineal
m, b = np.polyfit(cload_fF, tp_ps, 1)
cl_dense = np.linspace(0.5, 8.5, 100)
tp_dense = m * cl_dense + b

plt.figure(figsize=(7, 4.8), dpi=300)
plt.plot(cl_dense, tp_dense, 'r--', label=f'Ajuste: $t_p = {m:.3f}\\,C_L + {b:.3f}$ ps', linewidth=1.6)
plt.scatter(cload_fF, tp_ps, color='#1E2761', s=50, zorder=5, label='Mediciones $t_p = (t_{pHL}+t_{pLH})/2$')
plt.plot(cload_fF, tphl_ps, 's--', color='#F96167', alpha=0.7, markersize=5, label='$t_{pHL}$ (descarga)')
plt.plot(cload_fF, tplh_ps, '^--', color='#2ca02c', alpha=0.7, markersize=5, label='$t_{pLH}$ (carga)')

plt.xlabel('Capacitancia de Carga, $C_L$ [fF]')
plt.ylabel('Retardo de Propagación, $t_p$ [ps]')
plt.title('Retardo de Propagación frente a la Carga $C_L$\n($45$ nm HP, $W_n = 180$ nm, $\\beta = 2$)', fontweight='bold')
plt.grid(True)
plt.xlim(0.5, 8.5)
plt.ylim(2.5, 23.5)
plt.legend(loc='upper left')

plt.text(4.5, 7.0, f'Pendiente ($m$): {m:.3f} ps/fF\nIntersección ($t_0$): {b:.3f} ps',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F6FB', edgecolor='#1E2761', alpha=0.9))

plt.savefig(os.path.join(output_dir, "fig2_tp_vs_cl.png"))
plt.close()

# -------------------------------------------------------------
# FIGURA 3: Transitorio Compuerta Compleja (Actividad 4)
# -------------------------------------------------------------
print("Generando Figura 3: Verificación Compuerta Compleja...")
cg_raw = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\simulaciones\A4_Compuerta_Compleja\A4_ComplexGate.raw"

with open(cg_raw, 'r', encoding='utf-8', errors='ignore') as f:
    cg_lines = f.readlines()

val_idx = 0
for idx, line in enumerate(cg_lines):
    if line.startswith("Values:"):
        val_idx = idx + 1
        break

cg_data = cg_lines[val_idx:]
t_list, va_list, vb_list, vc_list, vout_list = [], [], [], [], []

i = 0
while i < len(cg_data):
    parts = cg_data[i].split()
    if len(parts) >= 2:
        t_val = float(parts[1])
        va_val = float(cg_data[i+1].split()[0])
        vb_val = float(cg_data[i+2].split()[0])
        vc_val = float(cg_data[i+3].split()[0])
        vout_val = float(cg_data[i+4].split()[0])
        
        t_list.append(t_val * 1e9) # ns
        va_list.append(va_val)
        vb_list.append(vb_val)
        vc_list.append(vc_val)
        vout_list.append(vout_val)
        i += 7
    else:
        i += 1

fig, axs = plt.subplots(4, 1, figsize=(10, 6.5), sharex=True, dpi=300)

axs[0].plot(t_list, va_list, color='#1f77b4', linewidth=1.5)
axs[0].set_ylabel('$V(A)$ [V]')
axs[0].set_ylim(-0.1, 1.15)
axs[0].grid(True)
axs[0].set_title('Verificación Funcional: $Y = \\overline{(A \\cdot B) + C}$ (Recorrido de 8 Combinaciones)', fontweight='bold')

axs[1].plot(t_list, vb_list, color='#ff7f0e', linewidth=1.5)
axs[1].set_ylabel('$V(B)$ [V]')
axs[1].set_ylim(-0.1, 1.15)
axs[1].grid(True)

axs[2].plot(t_list, vc_list, color='#2ca02c', linewidth=1.5)
axs[2].set_ylabel('$V(C)$ [V]')
axs[2].set_ylim(-0.1, 1.15)
axs[2].grid(True)

axs[3].plot(t_list, vout_list, color='#d62728', linewidth=1.8)
axs[3].set_ylabel('$V(out)$ [V]')
axs[3].set_ylim(-0.1, 1.15)
axs[3].set_xlabel('Tiempo, $t$ [ns]')
axs[3].grid(True)

# Anotaciones de estados
estados = ["000", "001", "010", "011", "100", "101", "110", "111"]
y_esperados = [1, 0, 1, 0, 1, 0, 0, 0]
for idx, (est, y_esp) in enumerate(zip(estados, y_esperados)):
    t_center = idx + 0.5
    axs[3].text(t_center, 0.5, f'{est}\n$Y={y_esp}$', ha='center', va='center',
                fontsize=8, bbox=dict(boxstyle='square,pad=0.2', facecolor='white', alpha=0.8))

plt.xlim(0, 8.0)
plt.savefig(os.path.join(output_dir, "fig3_transitorio_compleja.png"))
plt.close()

# -------------------------------------------------------------
# FIGURA 4: Oscilador de Anillo (Actividad 5)
# -------------------------------------------------------------
print("Generando Figura 4: Oscilador de Anillo...")
ro_raw = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\simulaciones\A5_Potencia_y_RO\A5_RO_HP.raw"

with open(ro_raw, 'r', encoding='utf-8', errors='ignore') as f:
    ro_lines = f.readlines()

val_idx = 0
for idx, line in enumerate(ro_lines):
    if line.startswith("Values:"):
        val_idx = idx + 1
        break

ro_data = ro_lines[val_idx:]
t_ro, vn1, vn2, vn3 = [], [], [], []

i = 0
while i < len(ro_data):
    parts = ro_data[i].split()
    if len(parts) >= 2:
        t_val = float(parts[1])
        vn1_val = float(ro_data[i+1].split()[0])
        vn2_val = float(ro_data[i+2].split()[0])
        vn3_val = float(ro_data[i+3].split()[0])
        
        t_ro.append(t_val * 1e12) # ps
        vn1.append(vn1_val)
        vn2.append(vn2_val)
        vn3.append(vn3_val)
        i += 9
    else:
        i += 1

t_ro = np.array(t_ro)
vn1 = np.array(vn1)
vn2 = np.array(vn2)
vn3 = np.array(vn3)

# Filtrar ventana estacionaria entre 5000 ps y 5250 ps
mask = (t_ro >= 5000) & (t_ro <= 5250)

plt.figure(figsize=(9, 4.5), dpi=300)
plt.plot(t_ro[mask], vn1[mask], label='Etapa 1: $V(n_1)$', color='#1E2761', linewidth=1.8)
plt.plot(t_ro[mask], vn2[mask], label='Etapa 2: $V(n_2)$', color='#F96167', linewidth=1.5, linestyle='--')
plt.plot(t_ro[mask], vn3[mask], label='Etapa 3: $V(n_3)$', color='#2ca02c', linewidth=1.5, linestyle=':')

plt.axhline(0.5, color='gray', linestyle='-.', alpha=0.6, label='$V_{DD}/2 = 0.5$ V')
plt.xlabel('Tiempo, $t$ [ps]')
plt.ylabel('Voltaje de los Nodos [V]')
plt.title('Oscilación Estacionaria en Oscilador de Anillo de 5 Etapas ($45$ nm HP)', fontweight='bold')
plt.grid(True)
plt.xlim(5000, 5250)
plt.ylim(-0.05, 1.05)
plt.legend(loc='upper right')

plt.text(5015, 0.15,
         'Período $T_{osc} = 45.58$ ps\nFrecuencia $f_{osc} = 21.94$ GHz\nRetardo por etapa $t_{pd} = 4.56$ ps',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F6FB', edgecolor='#1E2761', alpha=0.9))

plt.savefig(os.path.join(output_dir, "fig4_oscilador_anillo.png"))
plt.close()

print("Todas las figuras han sido generadas exitosamente en:", output_dir)
