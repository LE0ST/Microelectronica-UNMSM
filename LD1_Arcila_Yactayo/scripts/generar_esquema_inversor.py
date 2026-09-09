import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

output_dir = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\informe_latex\figuras"
os.makedirs(output_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(4.2, 3.8), dpi=300)
ax.set_xlim(-0.2, 4.0)
ax.set_ylim(-0.2, 4.4)
ax.axis('off')

# Rail VDD
ax.plot([0.8, 2.6], [4.1, 4.1], color='#1E2761', lw=2)
ax.text(1.7, 4.22, '$V_{DD} = 1.0\\text{ V}$', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E2761')

# PMOS
x, y = 1.7, 3.2
ax.plot([x, x], [y-0.25, y+0.25], color='#F96167', lw=2.5)
ax.plot([x-0.18, x-0.18], [y-0.25, y+0.25], color='#1E2761', lw=1.5)
circle = patches.Circle((x-0.09, y), 0.06, edgecolor='#1E2761', facecolor='white', lw=1.2)
ax.add_patch(circle)
ax.plot([x-0.45, x-0.15], [y, y], color='#1E2761', lw=1.5)
ax.plot([x, x+0.18, x+0.18], [y+0.18, y+0.18, y+0.4], color='#1E2761', lw=1.5)
ax.plot([x, x+0.18, x+0.18], [y-0.18, y-0.18, y-0.4], color='#1E2761', lw=1.5)
ax.text(x+0.3, y, '$MP$\n$W_p = \\beta W_n$', ha='left', va='center', fontsize=7.5, color='#F96167')

# Conexión VDD a PMOS
ax.plot([1.88, 1.88], [3.6, 4.1], color='#1E2761', lw=1.5)

# NMOS
y_n = 1.2
ax.plot([x, x], [y_n-0.25, y_n+0.25], color='#1f77b4', lw=2.5)
ax.plot([x-0.14, x-0.14], [y_n-0.25, y_n+0.25], color='#1E2761', lw=1.5)
ax.plot([x-0.45, x-0.14], [y_n, y_n], color='#1E2761', lw=1.5)
ax.plot([x, x+0.18, x+0.18], [y_n+0.18, y_n+0.18, y_n+0.4], color='#1E2761', lw=1.5)
ax.plot([x, x+0.18, x+0.18], [y_n-0.18, y_n-0.18, y_n-0.4], color='#1E2761', lw=1.5)
ax.text(x+0.3, y_n, '$MN$\n$W_n = 4L$', ha='left', va='center', fontsize=7.5, color='#1f77b4')

# Unión drenadores PMOS y NMOS a salida
ax.plot([1.88, 1.88], [2.8, 1.6], color='#1E2761', lw=1.5)
ax.scatter([1.88], [2.2], color='#1E2761', s=30, zorder=5)

# Entrada Vin (unión de compuertas)
ax.plot([1.25, 1.25], [3.2, 1.2], color='#1E2761', lw=1.5)
ax.scatter([1.25], [2.2], color='#1E2761', s=25, zorder=5)
ax.plot([0.5, 1.25], [2.2, 2.2], color='#1E2761', lw=1.5)
ax.scatter([0.5], [2.2], color='#1E2761', s=25, zorder=5)
ax.text(0.4, 2.2, '$V_{in}$', ha='right', va='center', fontsize=9.5, fontweight='bold', color='#1E2761')

# Salida Vout y Cload
ax.plot([1.88, 3.2], [2.2, 2.2], color='#1E2761', lw=1.5)
ax.scatter([3.2], [2.2], color='#1E2761', s=25, zorder=5)
ax.text(3.3, 2.2, '$V_{out}$', ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1E2761')

ax.plot([2.6, 2.6], [2.2, 1.8], color='#1E2761', lw=1.2)
ax.plot([2.4, 2.8], [1.8, 1.8], color='#1E2761', lw=1.5)
ax.plot([2.4, 2.8], [1.7, 1.7], color='#1E2761', lw=1.5)
ax.plot([2.6, 2.6], [1.7, 1.5], color='#1E2761', lw=1.2)
ax.plot([2.45, 2.75], [1.5, 1.5], color='#1E2761', lw=1.5)
ax.text(2.9, 1.75, '$C_L$', ha='left', va='center', fontsize=7.5, color='#1E2761')

# Conexión NMOS a tierra
ax.plot([1.88, 1.88], [0.8, 0.45], color='#1E2761', lw=1.5)
ax.scatter([1.88], [0.45], color='#1E2761', s=25, zorder=5)
ax.plot([1.88, 1.88], [0.45, 0.25], color='#1E2761', lw=1.5)
ax.plot([1.7, 2.06], [0.25, 0.25], color='#1E2761', lw=1.5)
ax.plot([1.76, 2.0], [0.18, 0.18], color='#1E2761', lw=1.5)
ax.plot([1.82, 1.94], [0.11, 0.11], color='#1E2761', lw=1.5)
ax.text(1.88, -0.05, 'GND', ha='center', va='center', fontsize=8, fontweight='bold', color='#1E2761')

plt.tight_layout()
out_path = os.path.join(output_dir, "fig_esquema_inversor.png")
plt.savefig(out_path, bbox_inches='tight')
plt.close()
print(f"Esquema inversor guardado en: {out_path}")
