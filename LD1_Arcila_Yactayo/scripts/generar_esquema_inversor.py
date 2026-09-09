import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(6.8, 5.2), dpi=300)
ax.set_xlim(-0.6, 5.2)
ax.set_ylim(-0.4, 4.8)
ax.axis('off')

# Title
ax.set_title("Inversor CMOS en condición de conmutación ($V_{in} = V_{out} = V_M$)",
             fontsize=10.5, fontweight='bold', color='#1E2761', pad=12)

# Rail VDD
ax.plot([0.6, 3.8], [4.4, 4.4], color='#1E2761', lw=2)
ax.text(1.88, 4.55, '$V_{DD} = 1.0\\text{ V}$', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1E2761')

# PMOS MP (y=3.4)
yp = 3.4
xp = 1.7

# Canal PMOS (coral)
ax.plot([xp, xp], [yp-0.28, yp+0.28], color='#F96167', lw=2.8)

# Placa de compuerta (azul oscuro)
ax.plot([xp-0.14, xp-0.14], [yp-0.28, yp+0.28], color='#1E2761', lw=1.6)

# Burbuja exterior (a la izquierda de la compuerta segun norma IEEE)
bub_r = 0.055
circle = patches.Circle((xp-0.14-bub_r, yp), bub_r, edgecolor='#1E2761', facecolor='white', lw=1.3, zorder=4)
ax.add_patch(circle)

# Terminal de compuerta exterior llegando a la burbuja
ax.plot([1.15, xp-0.14-2*bub_r], [yp, yp], color='#1E2761', lw=1.5)

# Drenador y Fuente PMOS
ax.plot([xp, xp+0.18, xp+0.18], [yp+0.18, yp+0.18, yp+0.4], color='#1E2761', lw=1.5) # Source (top)
ax.plot([xp, xp+0.18, xp+0.18], [yp-0.18, yp-0.18, yp-0.4], color='#1E2761', lw=1.5) # Drain (bottom)
ax.plot([xp+0.18, xp+0.18], [yp+0.4, 4.4], color='#1E2761', lw=1.5) # Source to VDD

# Bulk PMOS (4 terminales: contacto B a VDD con flecha hacia afuera)
ax.plot([xp, xp+0.35], [yp, yp], color='#F96167', lw=1.3)
ax.annotate('', xy=(xp+0.25, yp), xytext=(xp+0.10, yp),
            arrowprops=dict(arrowstyle="->", color='#F96167', lw=1.4))
ax.plot([xp+0.35, xp+0.35, xp+0.18], [yp, 4.25, 4.25], color='#F96167', lw=1.1, ls=':')
ax.text(xp+0.38, yp+0.05, '$B$ ($V_{SBp}=0$)', fontsize=7, color='#F96167', va='bottom')

# Flecha Corriente IDp (en el tramo de drenador entre y=2.9 y 2.5)
ax.annotate('$I_{Dp}$', xy=(xp+0.18, 2.55), xytext=(xp+0.18, 2.95),
            arrowprops=dict(arrowstyle="->", color='#F96167', lw=1.6),
            fontsize=8.5, fontweight='bold', color='#F96167', ha='right', va='center')

# Cuadro descriptivo PMOS
ax.text(2.6, yp, '$MP$ (45nm HP)\n$W_p = \\beta W_n = 450\\text{ nm}$\n$L = 45\\text{ nm}$ ($\\beta = 2.5$)',
        ha='left', va='center', fontsize=7.5, color='#F96167',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5F5', edgecolor='#F96167', lw=0.7))


# NMOS MN (y=1.2)
yn = 1.2
xn = 1.7

# Canal NMOS (azul)
ax.plot([xn, xn], [yn-0.28, yn+0.28], color='#1f77b4', lw=2.8)

# Placa de compuerta NMOS
ax.plot([xn-0.14, xn-0.14], [yn-0.28, yn+0.28], color='#1E2761', lw=1.6)

# Terminal de compuerta NMOS (sin burbuja)
ax.plot([1.15, xn-0.14], [yn, yn], color='#1E2761', lw=1.5)

# Drenador y Fuente NMOS
ax.plot([xn, xn+0.18, xn+0.18], [yn+0.18, yn+0.18, yn+0.4], color='#1E2761', lw=1.5) # Drain (top)
ax.plot([xn, xn+0.18, xn+0.18], [yn-0.18, yn-0.18, yn-0.4], color='#1E2761', lw=1.5) # Source (bottom)

# Bulk NMOS (4 terminales: contacto B a GND con flecha hacia adentro)
ax.plot([xn, xn+0.35], [yn, yn], color='#1f77b4', lw=1.3)
ax.annotate('', xy=(xn+0.10, yn), xytext=(xn+0.25, yn),
            arrowprops=dict(arrowstyle="->", color='#1f77b4', lw=1.4))
ax.plot([xn+0.35, xn+0.35, xn+0.18], [yn, 0.55, 0.55], color='#1f77b4', lw=1.1, ls=':')
ax.text(xp+0.38, yn-0.05, '$B$ ($V_{SBn}=0$)', fontsize=7, color='#1f77b4', va='top')

# Flecha Corriente IDn (en el tramo de drenador entre y=2.05 y 1.65)
ax.annotate('$I_{Dn}$', xy=(xn+0.18, 1.65), xytext=(xn+0.18, 2.05),
            arrowprops=dict(arrowstyle="->", color='#1f77b4', lw=1.6),
            fontsize=8.5, fontweight='bold', color='#1f77b4', ha='right', va='center')

# Cuadro descriptivo NMOS
ax.text(2.6, yn, '$MN$ (45nm HP)\n$W_n = 4L = 180\\text{ nm}$\n$L = 45\\text{ nm}$',
        ha='left', va='center', fontsize=7.5, color='#1f77b4',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F0F7FF', edgecolor='#1f77b4', lw=0.7))


# Conexión drenadores PMOS y NMOS a salida
ax.plot([xp+0.18, xp+0.18], [yp-0.4, yn+0.4], color='#1E2761', lw=1.5)
ax.scatter([xp+0.18], [2.3], color='#1E2761', s=35, zorder=5)

# Fuente NMOS a Tierra (tres barras estándar)
ax.plot([xn+0.18, xn+0.18], [yn-0.4, 0.35], color='#1E2761', lw=1.5)
ax.plot([xn+0.02, xn+0.34], [0.35, 0.35], color='#1E2761', lw=1.6)
ax.plot([xn+0.07, xn+0.29], [0.28, 0.28], color='#1E2761', lw=1.3)
ax.plot([xn+0.12, xn+0.24], [0.21, 0.21], color='#1E2761', lw=1.0)
ax.text(xn+0.18, 0.05, 'GND', ha='center', va='center', fontsize=8, fontweight='bold', color='#1E2761')

# Entrada Vin (union compuertas)
ax.plot([1.15, 1.15], [yp, yn], color='#1E2761', lw=1.5)
ax.scatter([1.15], [2.3], color='#1E2761', s=30, zorder=5)
ax.plot([0.3, 1.15], [2.3, 2.3], color='#1E2761', lw=1.5)
ax.scatter([0.3], [2.3], color='#1E2761', s=30, zorder=5)
ax.text(0.2, 2.3, '$V_{in}$', ha='right', va='center', fontsize=10, fontweight='bold', color='#1E2761')

# Salida Vout
ax.plot([xp+0.18, 4.4], [2.3, 2.3], color='#1E2761', lw=1.5)
ax.scatter([4.4], [2.3], color='#1E2761', s=30, zorder=5)
ax.text(4.5, 2.3, '$V_{out}$', ha='left', va='center', fontsize=10, fontweight='bold', color='#1E2761')

# Capacitor Cload y Tierra (tres barras estándar)
xc = 3.7
ax.plot([xc, xc], [2.3, 1.8], color='#1E2761', lw=1.2)
ax.plot([xc-0.18, xc+0.18], [1.8, 1.8], color='#1E2761', lw=1.6)
ax.plot([xc-0.18, xc+0.18], [1.7, 1.7], color='#1E2761', lw=1.6)
ax.plot([xc, xc], [1.7, 1.45], color='#1E2761', lw=1.2)
# 3 barras GND de CL
ax.plot([xc-0.15, xc+0.15], [1.45, 1.45], color='#1E2761', lw=1.5)
ax.plot([xc-0.09, xc+0.09], [1.39, 1.39], color='#1E2761', lw=1.3)
ax.plot([xc-0.04, xc+0.04], [1.33, 1.33], color='#1E2761', lw=1.0)
ax.text(xc+0.25, 1.75, '$C_L = 2\\text{ fF}$', ha='left', va='center', fontsize=7.5, fontweight='bold', color='#1E2761')

# Cortocircuito virtual / Condicion de conmutacion VM (lazo punteado)
ax.plot([0.3, 0.3, 4.4, 4.4], [2.3, -0.15, -0.15, 2.3], color='#8E2800', lw=1.3, ls='--')
ax.text(2.35, -0.15, 'Condición de conmutación: $V_{in} = V_{out} = V_M \\;\\Rightarrow\\; I_{Dn} = I_{Dp}$',
        ha='center', va='center', fontsize=8, fontweight='bold', color='#8E2800',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFF8F0', edgecolor='#8E2800', lw=0.8))

plt.tight_layout()
output_dir = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\informe_latex\figuras"
os.makedirs(output_dir, exist_ok=True)
out_path = os.path.join(output_dir, "fig_esquema_inversor.png")
plt.savefig(out_path, bbox_inches='tight')
plt.close()
print(f"Saved: {out_path}")
