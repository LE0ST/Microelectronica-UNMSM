import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

output_dir = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\informe_latex\figuras"
os.makedirs(output_dir, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.0), dpi=300, gridspec_kw={'width_ratios': [1, 1.4]})

# Panel 1: Grafo dual topológico
ax1.set_xlim(-0.2, 3.2)
ax1.set_ylim(-0.2, 5.2)
ax1.axis('off')
ax1.set_title('(a) Grafos de conducción duales', fontsize=10, fontweight='bold', color='#1E2761', pad=8)

ax1.text(1.5, 4.9, '$V_{DD}$', ha='center', va='center', fontsize=10, fontweight='bold', color='#1E2761')
ax1.plot([1.5, 1.5], [4.7, 3.8], color='#F96167', lw=2)
ax1.text(1.3, 4.25, '$C$', ha='right', va='center', fontsize=9, fontweight='bold', color='#F96167')
ax1.scatter([1.5], [3.8], color='#1E2761', s=35, zorder=5)

ax1.plot([1.5, 0.8, 0.8, 1.5], [3.8, 3.8, 2.7, 2.7], color='#F96167', lw=2)
ax1.plot([1.5, 2.2, 2.2, 1.5], [3.8, 3.8, 2.7, 2.7], color='#F96167', lw=2)
ax1.text(0.6, 3.25, '$A$', ha='right', va='center', fontsize=9, fontweight='bold', color='#F96167')
ax1.text(2.4, 3.25, '$B$', ha='left', va='center', fontsize=9, fontweight='bold', color='#F96167')

ax1.scatter([1.5], [2.7], color='#1E2761', s=45, zorder=5)
ax1.plot([1.5, 2.9], [2.7, 2.7], color='#1E2761', lw=1.5, ls='--')
ax1.text(3.0, 2.7, '$Y$', ha='left', va='center', fontsize=11, fontweight='bold', color='#1E2761')

ax1.plot([1.5, 0.8, 0.8, 1.5], [2.7, 2.7, 0.4, 0.4], color='#1f77b4', lw=2)
ax1.text(0.6, 1.55, '$C$', ha='right', va='center', fontsize=9, fontweight='bold', color='#1f77b4')

ax1.plot([1.5, 2.2, 2.2], [2.7, 2.7, 1.55], color='#1f77b4', lw=2)
ax1.scatter([2.2], [1.55], color='#1E2761', s=30, zorder=5)
ax1.plot([2.2, 2.2, 1.5], [1.55, 0.4, 0.4], color='#1f77b4', lw=2)
ax1.text(2.4, 2.15, '$A$', ha='left', va='center', fontsize=9, fontweight='bold', color='#1f77b4')
ax1.text(2.4, 0.95, '$B$', ha='left', va='center', fontsize=9, fontweight='bold', color='#1f77b4')

ax1.scatter([1.5], [0.4], color='#1E2761', s=35, zorder=5)
ax1.text(1.5, 0.15, 'GND', ha='center', va='center', fontsize=10, fontweight='bold', color='#1E2761')

ax1.text(1.5, 4.45, 'PUN: $C$ serie $(A \\parallel B)$', fontsize=8, color='#F96167', ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='#F4F6FB', edgecolor='#F96167', lw=0.8))
ax1.text(1.5, 0.65, 'PDN: $(A \\text{ serie } B) \\parallel C$', fontsize=8, color='#1f77b4', ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='#F4F6FB', edgecolor='#1f77b4', lw=0.8))

# Panel 2: Esquema
ax2.set_xlim(-0.5, 5.0)
ax2.set_ylim(-0.2, 5.2)
ax2.axis('off')
ax2.set_title('(b) Topología CMOS y dimensionamiento de transistores', fontsize=10, fontweight='bold', color='#1E2761', pad=8)

def draw_pmos(ax, x, y, label, w_label):
    ax.plot([x, x], [y-0.25, y+0.25], color='#F96167', lw=2.5)
    ax.plot([x-0.18, x-0.18], [y-0.25, y+0.25], color='#1E2761', lw=1.5)
    circle = patches.Circle((x-0.09, y), 0.06, edgecolor='#1E2761', facecolor='white', lw=1.2)
    ax.add_patch(circle)
    ax.plot([x-0.45, x-0.15], [y, y], color='#1E2761', lw=1.5)
    ax.plot([x, x+0.18, x+0.18], [y+0.18, y+0.18, y+0.4], color='#1E2761', lw=1.5)
    ax.plot([x, x+0.18, x+0.18], [y-0.18, y-0.18, y-0.4], color='#1E2761', lw=1.5)
    ax.text(x-0.5, y, label, ha='right', va='center', fontsize=9, fontweight='bold', color='#1E2761')
    ax.text(x+0.28, y, w_label, ha='left', va='center', fontsize=7.5, color='#F96167')

def draw_nmos(ax, x, y, label, w_label):
    ax.plot([x, x], [y-0.25, y+0.25], color='#1f77b4', lw=2.5)
    ax.plot([x-0.14, x-0.14], [y-0.25, y+0.25], color='#1E2761', lw=1.5)
    ax.plot([x-0.45, x-0.14], [y, y], color='#1E2761', lw=1.5)
    ax.plot([x, x+0.18, x+0.18], [y+0.18, y+0.18, y+0.4], color='#1E2761', lw=1.5)
    ax.plot([x, x+0.18, x+0.18], [y-0.18, y-0.18, y-0.4], color='#1E2761', lw=1.5)
    ax.text(x-0.5, y, label, ha='right', va='center', fontsize=9, fontweight='bold', color='#1E2761')
    ax.text(x+0.28, y, w_label, ha='left', va='center', fontsize=7.5, color='#1f77b4')

# Rail VDD
ax2.plot([0.8, 3.4], [4.9, 4.9], color='#1E2761', lw=2)
ax2.text(2.1, 5.08, '$V_{DD} = 1.0\\text{ V}$', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E2761')

# PMOS C (arriba)
draw_pmos(ax2, 1.9, 4.4, '$C$', '$W=2W_p=720$n')
ax2.plot([2.08, 2.08], [4.8, 4.9], color='#1E2761', lw=1.5)

# Nodo intermedio pmid
ax2.scatter([2.08], [3.95], color='#1E2761', s=25, zorder=5)
ax2.plot([1.18, 2.98], [3.95, 3.95], color='#1E2761', lw=1.5)

# PMOS A y B en paralelo
draw_pmos(ax2, 1.0, 3.4, '$A$', '$2W_p=720$n')
draw_pmos(ax2, 2.8, 3.4, '$B$', '$2W_p=720$n')
ax2.plot([1.18, 1.18], [3.8, 3.95], color='#1E2761', lw=1.5)
ax2.plot([2.98, 2.98], [3.8, 3.95], color='#1E2761', lw=1.5)

# --- 1. CONEXIÓN INFERIOR PMOS HACIA EL NODO Y ---
# Conectar drenadores de PMOS A y B (desde y=3.0 hasta y=2.85)
ax2.plot([1.18, 1.18], [3.0, 2.85], color='#1E2761', lw=1.5)
ax2.plot([2.98, 2.98], [3.0, 2.85], color='#1E2761', lw=1.5)

# Salida Y (unión de PMOS y NMOS)
ax2.plot([1.18, 2.98], [2.85, 2.85], color='#1E2761', lw=1.5)
ax2.scatter([2.08], [2.85], color='#1E2761', s=35, zorder=5)

# Terminal de salida Y con CL desplazada a la derecha para no solapar
ax2.plot([2.08, 3.9], [2.85, 2.85], color='#1E2761', lw=2)
ax2.scatter([3.9], [2.85], color='#1E2761', s=30, zorder=5)
ax2.text(4.0, 2.85, '$Y = \\overline{(A \\cdot B) + C}$', ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1E2761')

# --- 3. MEJORA DEL SÍMBOLO DE TIERRA EN C_L ---
ax2.plot([3.65, 3.65], [2.85, 2.5], color='#1E2761', lw=1.2)
ax2.plot([3.45, 3.85], [2.5, 2.5], color='#1E2761', lw=1.5)
ax2.plot([3.45, 3.85], [2.4, 2.4], color='#1E2761', lw=1.5)
ax2.plot([3.65, 3.65], [2.4, 2.2], color='#1E2761', lw=1.2)
# Tres barras decrecientes para GND de CL
ax2.plot([3.50, 3.80], [2.2, 2.2], color='#1E2761', lw=1.5)
ax2.plot([3.56, 3.74], [2.14, 2.14], color='#1E2761', lw=1.3)
ax2.plot([3.62, 3.68], [2.08, 2.08], color='#1E2761', lw=1.1)
ax2.text(3.9, 2.45, '$C_L=2\\text{ fF}$', ha='left', va='center', fontsize=7.5, color='#1E2761')

# --- 2. CORRECCIÓN DEL RIEL SUPERIOR DE LA PDN ---
# Conexión vertical hacia la PDN
ax2.plot([2.08, 2.08], [2.85, 2.7], color='#1E2761', lw=1.5)
# El riel debe terminar exactamente en el NMOS A (x=2.68), no en 2.98
ax2.plot([1.18, 2.68], [2.7, 2.7], color='#1E2761', lw=1.5)

# PDN: NMOS C a la izquierda
draw_nmos(ax2, 1.0, 1.8, '$C$', '$W=W_n=180$n')
ax2.plot([1.18, 1.18], [2.7, 2.2], color='#1E2761', lw=1.5)

# PDN: NMOS A y B a la derecha
draw_nmos(ax2, 2.5, 2.1, '$A$', '$2W_n=360$n')
ax2.plot([2.68, 2.68], [2.7, 2.5], color='#1E2761', lw=1.5)

draw_nmos(ax2, 2.5, 1.0, '$B$', '$2W_n=360$n')
ax2.plot([2.68, 2.68], [1.7, 1.4], color='#1E2761', lw=1.5)
ax2.scatter([2.68], [1.55], color='#1E2761', s=20, zorder=5)
ax2.text(2.8, 1.55, '$n_{ab}$', ha='left', va='center', fontsize=7, color='#666')

# Conexión a tierra
ax2.plot([1.18, 1.18, 2.08], [1.4, 0.45, 0.45], color='#1E2761', lw=1.5)
ax2.plot([2.68, 2.68, 2.08], [0.6, 0.45, 0.45], color='#1E2761', lw=1.5)
ax2.scatter([2.08], [0.45], color='#1E2761', s=25, zorder=5)
ax2.plot([2.08, 2.08], [0.45, 0.25], color='#1E2761', lw=1.5)
ax2.plot([1.9, 2.26], [0.25, 0.25], color='#1E2761', lw=1.5)
ax2.plot([1.96, 2.2], [0.18, 0.18], color='#1E2761', lw=1.5)
ax2.plot([2.02, 2.14], [0.11, 0.11], color='#1E2761', lw=1.5)
ax2.text(2.08, -0.05, 'GND', ha='center', va='center', fontsize=8, fontweight='bold', color='#1E2761')

plt.tight_layout()
out_path = os.path.join(output_dir, "fig_esquema_compleja.png")
plt.savefig(out_path, bbox_inches='tight')
plt.close()
print(f"Esquema regenerado exitosamente en: {out_path}")
