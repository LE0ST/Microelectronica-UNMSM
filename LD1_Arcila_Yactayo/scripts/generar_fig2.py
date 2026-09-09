import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = r"G:\Proyectos\MicroNano\LD1_Arcila_Yactayo\informe_latex\figuras"
os.makedirs(output_dir, exist_ok=True)

cload_fF = np.array([1, 2, 3, 4, 5, 6, 7, 8])
tphl_ps = np.array([5.464, 7.881, 10.256, 12.613, 14.960, 17.300, 19.638, 21.972])
tplh_ps = np.array([3.580, 4.931, 6.272, 7.612, 8.948, 10.282, 11.617, 12.950])
tp_ps = (tphl_ps + tplh_ps) / 2.0

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
plt.title('Retardo de Propagación frente a la Carga $C_L$\n($45$ nm HP, $W_n = 180$ nm, $\\beta = 2.5$)', fontweight='bold')
plt.grid(True)
plt.xlim(0.5, 8.5)
plt.ylim(2.5, 23.5)
plt.legend(loc='upper left')

plt.text(4.5, 7.0, f'Pendiente ($m$): {m:.3f} ps/fF\nIntersección ($t_0$): {b:.3f} ps',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F6FB', edgecolor='#1E2761', alpha=0.9))

out_path = os.path.join(output_dir, "fig2_tp_vs_cl.png")
plt.savefig(out_path, bbox_inches='tight')
plt.close()
print(f"Figura 2 regenerada con exito en: {out_path}")
