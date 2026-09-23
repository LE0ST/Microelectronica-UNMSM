"""Rehacer exclusivamente la figura de consolidación A3 desde métricas existentes.

No ejecuta LTspice ni modifica logs, RAW, métricas o registro de ensayos.
"""

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


LD2 = Path(__file__).resolve().parents[2]
DATOS = LD2 / "act3" / "resultados" / "datos"
FIGURAS = LD2 / "act3" / "figuras"
FIGURA_INFORME = LD2 / "informe_latex" / "figuras" / "fig2_act3_consolidacion_hp_lp_130.png"
ANCHOS = [0.0, 15.0, 30.0, 45.0, 90.0, 180.0]


def cargar(nombre):
    return json.loads((DATOS / nombre).read_text(encoding="utf-8"))


def serie(metricas, id_sin_keeper, temp, vdd):
    datos = metricas[f"barrido_con_keeper_{temp}C"]["puntos"]
    valores = {float(p["Wkp_nm"]): p["Vdyn_end_1us_V"] for p in datos}
    valores[0.0] = metricas["ensayos_sin_keeper"][id_sin_keeper]["Vdyn_end_1us_V"]
    faltantes = [w for w in ANCHOS if w not in valores]
    if faltantes:
        raise ValueError(f"Anchos sin evidencia simulada: {faltantes}")
    return [valores[w] / vdd for w in ANCHOS]


def main():
    hp = cargar("act3_retencion_metricas.json")
    lp = cargar("act3_retencion_lp_metricas.json")
    bulk = cargar("act3_retencion_130_metricas.json")
    curvas = [
        ("45nm HP @ 27 °C (VDD = 1.0 V)", "o-", "#1f77b4", serie(hp, "ENS-A3-RET-01", 27, 1.0)),
        ("45nm HP @ 85 °C (VDD = 1.0 V)", "s--", "#d62728", serie(hp, "ENS-A3-RET-03", 85, 1.0)),
        ("45nm LP @ 27 °C (VDD = 1.1 V)", "^-.", "#2ca02c", serie(lp, "ENS-A3-LP-RET-01", 27, 1.1)),
        ("45nm LP @ 85 °C (VDD = 1.1 V)", "d:", "#ff7f0e", serie(lp, "ENS-A3-LP-RET-03", 85, 1.1)),
        ("130nm Bulk @ 27 °C (VDD = 1.3 V)", "v-", "#6f42c1", serie(bulk, "ENS-A3-130-RET-01", 27, 1.3)),
        ("130nm Bulk @ 85 °C (VDD = 1.3 V)", "x--", "#e83e8c", serie(bulk, "ENS-A3-130-RET-03", 85, 1.3)),
    ]
    plt.figure(figsize=(10, 6), dpi=300)
    for nombre, estilo, color, valores in curvas:
        plt.plot(ANCHOS, valores, estilo, color=color, linewidth=2, label=nombre)
    plt.axhline(0.90, color="#7f7f7f", linestyle="--", linewidth=1.5, label="Criterio de retención: 0.90 VDD")
    plt.axhline(1.00, color="#000000", linestyle="-", linewidth=0.8, alpha=0.5)
    plt.title("Consolidación tecnológica: retención normalizada V(dyn) / VDD\n45 nm HP, 45 nm LP y 130 nm Bulk; 27 °C y 85 °C (1 µs, CL = 2 fF)", fontsize=12, fontweight="bold")
    plt.xlabel("Ancho del keeper Wkp [nm] (0 = sin keeper)", fontsize=11)
    plt.ylabel("Tensión normalizada V(dyn) / VDD", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower right", fontsize=9)
    # 130 nm sin keeper: 0.78290 (27 C) y 0.67459 (85 C): NO recortar.
    plt.ylim(0.64, 1.045)
    plt.xlim(-5, 190)
    plt.tight_layout()
    FIGURAS.mkdir(parents=True, exist_ok=True)
    destino = FIGURAS / "figura_consolidacion_hp_lp_130_retencion.png"
    plt.savefig(destino, dpi=300)
    plt.close()
    shutil.copy2(destino, FIGURA_INFORME)
    print(f"OK: {destino}")
    print(f"OK: {FIGURA_INFORME}")
    print("Puntos sin keeper 130 nm:", curvas[4][3][0], curvas[5][3][0])


if __name__ == "__main__":
    main()
