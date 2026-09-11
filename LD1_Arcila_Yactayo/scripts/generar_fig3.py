import os
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'figure.titlesize': 13,
    'figure.autolayout': True,
    'grid.alpha': 0.5,
    'grid.linestyle': '--'
})

output_dir = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\informe_latex\figuras"
cg_raw = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\simulaciones\A4_Compuerta_Compleja\A4_ComplexGate.raw"

def read_raw_lines(path):
    with open(path, 'rb') as f:
        data = f.read()
    if b'\x00' in data[:100]:
        return data.decode('utf-16le', errors='ignore').splitlines(True)
    return data.decode('utf-8', errors='ignore').splitlines(True)

cg_lines = read_raw_lines(cg_raw)

n_vars = 0
var_map = {}
in_vars = False
val_idx = 0

for idx, line in enumerate(cg_lines):
    if line.startswith('No. Variables:'):
        n_vars = int(line.split(':')[1].strip())
    elif line.startswith('Variables:'):
        in_vars = True
    elif line.startswith('Values:'):
        in_vars = False
        val_idx = idx + 1
        break
    elif in_vars:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[0].isdigit():
            v_idx = int(parts[0])
            v_name = parts[1].lower()
            var_map[v_name] = v_idx

cg_data = cg_lines[val_idx:]
t_list, va_list, vb_list, vc_list, vout_list = [], [], [], [], []

i = 0
while i < len(cg_data):
    parts = cg_data[i].split()
    if len(parts) >= 2:
        t_val = float(parts[1])
        va_val = float(cg_data[i + var_map['v(a)']].split()[0])
        vb_val = float(cg_data[i + var_map['v(b)']].split()[0])
        vc_val = float(cg_data[i + var_map['v(c)']].split()[0])
        vout_val = float(cg_data[i + var_map['v(out)']].split()[0])
        
        t_list.append(t_val * 1e9)
        va_list.append(va_val)
        vb_list.append(vb_val)
        vc_list.append(vc_val)
        vout_list.append(vout_val)
        i += n_vars
    else:
        i += 1

fig, axs = plt.subplots(4, 1, figsize=(10, 6.2), sharex=True, dpi=300)

axs[0].plot(t_list, va_list, color='#1f77b4', linewidth=1.6)
axs[0].set_ylabel('V(A) [V]', fontweight='bold')
axs[0].set_ylim(-0.1, 1.15)
axs[0].grid(True)
axs[0].set_title(r'Verificación Funcional: $Y = \overline{(A \cdot B) + C}$ (Recorrido de 8 Combinaciones)', fontweight='bold', pad=8)

axs[1].plot(t_list, vb_list, color='#ff7f0e', linewidth=1.6)
axs[1].set_ylabel('V(B) [V]', fontweight='bold')
axs[1].set_ylim(-0.1, 1.15)
axs[1].grid(True)

axs[2].plot(t_list, vc_list, color='#2ca02c', linewidth=1.6)
axs[2].set_ylabel('V(C) [V]', fontweight='bold')
axs[2].set_ylim(-0.1, 1.15)
axs[2].grid(True)

axs[3].plot(t_list, vout_list, color='#d62728', linewidth=1.8)
axs[3].set_ylabel('V(out) [V]', fontweight='bold')
axs[3].set_ylim(-0.1, 1.15)
axs[3].set_xlabel('Tiempo, t [ns]', fontweight='bold')
axs[3].grid(True)

estados = ['111', '110', '101', '100', '011', '010', '001', '000']
y_esperados = [0, 0, 0, 1, 0, 1, 0, 1]

for ax in axs:
    for t_div in range(1, 8):
        ax.axvline(t_div, color='#888888', linestyle=':', alpha=0.7, linewidth=1.2)

for idx, (est, y_esp) in enumerate(zip(estados, y_esperados)):
    t_center = idx + 0.5
    axs[3].text(t_center, 0.5, f'ABC = {est}\nY = {y_esp}', ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#1E2761',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#F4F6FB', edgecolor='#1E2761', alpha=0.92, lw=1.0))

plt.xlim(0, 8.0)
out_path = os.path.join(output_dir, 'fig3_transitorio_compleja.png')
plt.savefig(out_path, bbox_inches='tight')
plt.close()
print("Guardado con exito fig3_transitorio_compleja.png")
