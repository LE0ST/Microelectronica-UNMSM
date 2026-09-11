"""
Script para generar el bloque de 5 capturas de cursores LTspice (Actividad 1)
Medicion de voltajes criticos V_IL y V_IH en los puntos de pendiente unitaria d(Vout)/d(Vin) = -1
para beta in [1.0, 1.5, 2.0, 2.5, 3.0] en 45nm HP.
Autores: Leonardo Sait Yactayo Tolentino (23190214) & Marco Antonio Arcila Santander (23190140)
"""

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Directorios de entrada y salida
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
input_dir = os.path.join(base_dir, "simulaciones", "A1_Inversor_VTC", "capturas_cursores")
output_dir = os.path.join(base_dir, "informe_latex", "figuras")
os.makedirs(output_dir, exist_ok=True)

# Configuracion de las 5 capturas y sus recortes normalizados a (1012, 650)
capturas = [
    {
        "file": "cursores_beta10.jpg",
        "box": (6, 38, 1018, 688),
        "title": r"(a) $\beta = 1.0$   [$V_{IL} = 346.2\,$mV, $V_{IH} = 554.8\,$mV]"
    },
    {
        "file": "cursores_beta15.jpg",
        "box": (6, 35, 1018, 685),
        "title": r"(b) $\beta = 1.5$   [$V_{IL} = 367.1\,$mV, $V_{IH} = 576.9\,$mV]"
    },
    {
        "file": "cursores_beta20.jpg",
        "box": (6, 35, 1018, 685),
        "title": r"(c) $\beta = 2.0$   [$V_{IL} = 381.4\,$mV, $V_{IH} = 593.6\,$mV]"
    },
    {
        "file": "cursores_beta25.jpg",
        "box": (6, 32, 1018, 682),
        "title": r"(d) $\beta = 2.5$ [Óptimo]   [$V_{IL} = 392.1\,$mV, $V_{IH} = 604.3\,$mV]"
    },
    {
        "file": "cursores_beta30.jpg",
        "box": (6, 37, 1018, 687),
        "title": r"(e) $\beta = 3.0$   [$V_{IL} = 401.1\,$mV, $V_{IH} = 612.6\,$mV]"
    }
]

# Crear figura de alta definicion (300 DPI)
fig = plt.figure(figsize=(15, 6.7), dpi=300)
# Grid de 2 filas y 6 columnas para centrar la segunda fila
gs = gridspec.GridSpec(2, 6, figure=fig, hspace=0.18, wspace=0.08,
                       top=0.94, bottom=0.03, left=0.02, right=0.98)

axes = [
    fig.add_subplot(gs[0, 0:2]),
    fig.add_subplot(gs[0, 2:4]),
    fig.add_subplot(gs[0, 4:6]),
    fig.add_subplot(gs[1, 1:3]),
    fig.add_subplot(gs[1, 3:5])
]

for ax, cap in zip(axes, capturas):
    img_path = os.path.join(input_dir, cap["file"])
    im = Image.open(img_path)
    cropped = im.crop(cap["box"])
    # Borde sutil gris para delimitar el fondo blanco del plot
    bordered = ImageOps.expand(cropped, border=1, fill="#90A4AE")
    
    ax.imshow(bordered)
    ax.set_title(cap["title"], fontsize=10.5, fontweight="bold", pad=4)
    ax.axis("off")

output_path = os.path.join(output_dir, "fig1_cursores_ltspice.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print(f"Figura generada con exito en: {output_path}")
