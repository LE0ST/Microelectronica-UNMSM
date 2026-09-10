"""
Script: generar_comparativa_nodos.py
Propósito: Comparación transitoria del inversor CMOS en 3 nodos tecnológicos
           (90 nm bulk, 45 nm HP, 22 nm HP) con C_L = 2 fF.
Curso: Microelectrónica y Sistemas Nanoelectrónicos (UNMSM FIEE)
Autores: Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander
"""

import os
import struct
import numpy as np
import matplotlib.pyplot as plt

# Directorios del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM_DIR = os.path.join(BASE_DIR, "simulaciones", "A2_Retardo_Transitorio")
OUT_DIR = os.path.join(BASE_DIR, "informe_latex", "figuras")
os.makedirs(OUT_DIR, exist_ok=True)

def read_ltspice_binary_raw(raw_path):
    """Lee archivos .raw de LTspice (formato binario forward) extrayendo tiempo, V(in) y V(out)."""
    with open(raw_path, 'rb') as f:
        data = f.read()

    # Identificar encabezado (UTF-16LE o ASCII)
    marker = 'Binary:\n'.encode('utf-16le')
    idx = data.find(marker)
    if idx == -1:
        marker = b'Binary:\n'
        idx = data.find(marker)
        header = data[:idx].decode('utf-8', errors='ignore')
        raw_bytes = data[idx + len(marker):]
    else:
        header = data[:idx].decode('utf-16le', errors='ignore')
        raw_bytes = data[idx + len(marker):]

    n_vars = 15
    for line in header.splitlines():
        if 'No. Variables:' in line:
            n_vars = int(line.split(':')[1].strip())

    point_size = 8 + (n_vars - 1) * 4
    n_pts = len(raw_bytes) // point_size

    times, vins, vouts = [], [], []
    for pt in range(n_pts):
        offset = pt * point_size
        t = struct.unpack('<d', raw_bytes[offset:offset+8])[0]
        vin = struct.unpack('<f', raw_bytes[offset+8:offset+12])[0]
        vout = struct.unpack('<f', raw_bytes[offset+12:offset+16])[0]
        times.append(t)
        vins.append(vin)
        vouts.append(vout)

    return np.array(times) * 1e12, np.array(vins), np.array(vouts)

def main():
    # Rutas a los volcados de simulación
    raw_22nm = os.path.join(SIM_DIR, "A2_22nm.raw")
    raw_45nm = os.path.join(SIM_DIR, "A2_45nm.raw")
    raw_90nm = os.path.join(SIM_DIR, "A2_90nm.raw")

    # Extraer datos de simulación
    t_22, _, vout_22 = read_ltspice_binary_raw(raw_22nm)
    t_45, _, vout_45 = read_ltspice_binary_raw(raw_45nm)
    t_90, _, vout_90 = read_ltspice_binary_raw(raw_90nm)

    # Configuración de estilo editorial
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'sans-serif',
        'axes.labelsize': 11,
        'axes.titlesize': 11,
        'xtick.labelsize': 9.5,
        'ytick.labelsize': 9.5,
        'legend.fontsize': 9,
        'figure.autolayout': True,
        'grid.alpha': 0.5,
        'grid.linestyle': '--'
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.2), dpi=300)

    # Código cromático estricto especificado por la rúbrica y observación de Marco
    c_22 = '#D62728'  # Rojo: 22 nm HP
    c_45 = '#1F77B4'  # Azul: 45 nm HP
    c_90 = '#2CA02C'  # Verde: 90 nm bulk

    # -------------------------------------------------------------
    # Panel (a): Dinámica de conmutación global (ciclo de bajada y subida)
    # -------------------------------------------------------------
    ax1.plot(t_22, vout_22, color=c_22, lw=2.0,
             label=r'22 nm HP ($V_{DD} = 0.8$ V, $t_p = 8.65$ ps)')
    ax1.plot(t_45, vout_45, color=c_45, lw=2.0,
             label=r'45 nm HP ($V_{DD} = 1.0$ V, $t_p = 6.41$ ps)')
    ax1.plot(t_90, vout_90, color=c_90, lw=2.0,
             label=r'90 nm bulk ($V_{DD} = 1.2$ V, $t_p = 7.36$ ps)')

    ax1.set_xlim(150, 850)
    ax1.set_ylim(-0.05, 1.35)
    ax1.set_xlabel('Tiempo, $t$ [ps]', fontweight='bold')
    ax1.set_ylabel('Voltaje de Salida, $V_{out}$ [V]', fontweight='bold')
    ax1.set_title('(a) Ciclo completo de conmutación ($C_L = 2$ fF)', fontweight='bold', color='#1E2761')
    ax1.grid(True)
    ax1.legend(loc='upper right', framealpha=0.95, edgecolor='#1E2761', facecolor='#F4F6FB')

    # -------------------------------------------------------------
    # Panel (b): Detalle del flanco de bajada (transición tpHL)
    # -------------------------------------------------------------
    ax2.plot(t_22, vout_22, color=c_22, lw=2.2,
             label=r'22 nm HP ($t_{pHL} = 10.73$ ps)')
    ax2.plot(t_45, vout_45, color=c_45, lw=2.2,
             label=r'45 nm HP ($t_{pHL} = 7.88$ ps)')
    ax2.plot(t_90, vout_90, color=c_90, lw=2.2,
             label=r'90 nm bulk ($t_{pHL} = 7.86$ ps)')

    # Líneas de referencia del 50% de VDD para cada tecnología
    ax2.axhline(0.4, color=c_22, ls=':', lw=1.2, alpha=0.85)
    ax2.axhline(0.5, color=c_45, ls=':', lw=1.2, alpha=0.85)
    ax2.axhline(0.6, color=c_90, ls=':', lw=1.2, alpha=0.85)

    ax2.text(196, 0.42, r'$V_{DD}/2 = 0.4$ V (22 nm)', color=c_22, fontsize=7.5, fontweight='bold')
    ax2.text(196, 0.52, r'$V_{DD}/2 = 0.5$ V (45 nm)', color=c_45, fontsize=7.5, fontweight='bold')
    ax2.text(196, 0.62, r'$V_{DD}/2 = 0.6$ V (90 nm)', color=c_90, fontsize=7.5, fontweight='bold')

    ax2.set_xlim(195, 235)
    ax2.set_ylim(-0.05, 1.35)
    ax2.set_xlabel('Tiempo, $t$ [ps]', fontweight='bold')
    ax2.set_ylabel('Voltaje de Salida, $V_{out}$ [V]', fontweight='bold')
    ax2.set_title('(b) Detalle del flanco de descarga ($t_{pHL}$)', fontweight='bold', color='#1E2761')
    ax2.grid(True)
    ax2.legend(loc='upper right', framealpha=0.95, edgecolor='#1E2761', facecolor='#F4F6FB')

    out_file = os.path.join(OUT_DIR, "fig2_comparativa_nodos.png")
    plt.savefig(out_file, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Figura comparativa generada exitosamente en: {out_file}")

if __name__ == "__main__":
    main()
