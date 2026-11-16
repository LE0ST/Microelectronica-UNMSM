#!/usr/bin/env python3
"""
Portable figure generator for LD4 (Stuck-at discrete samples & 10-node schematic).
Authors: Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander (UNMSM-FIEE).

Usage:
  python LD4_Arcila_Yactayo/scripts/generar_figuras_ld4.py
  python LD4_Arcila_Yactayo/scripts/generar_figuras_ld4.py --log path/to/P1_segf_stuckat.log
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def load_from_csv(ld4_root: Path) -> tuple[list[float], list[float]]:
    res = ld4_root / "resultados"
    with (res / "p1_circuito_sano.csv").open(encoding="utf-8") as f:
        healthy = [float(r["vy_medido_V"]) for r in csv.DictReader(f)]
    with (res / "p1_diccionario_fallos.csv").open(encoding="utf-8") as f:
        drows = list(csv.DictReader(f))
    # 7/s-a-0 differs from healthy on 0101 (idx 5) and 0110 (idx 6)
    f7_row = next(r for r in drows if r["fallo"] == "7/s-a-0")
    faulty = list(healthy)
    # In p1_diccionario_fallos, 0101 and 0110 are 0 for 7/s-a-0
    if f7_row["v_0101"] == "0":
        faulty[5] = 0.0
    if f7_row["v_0110"] == "0":
        faulty[6] = 0.0
    return healthy, faulty


def load_from_log(log_path: Path) -> tuple[list[float], list[float]]:
    raw = log_path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"Measurement:\s+v(\d\d)", raw, flags=re.I)
    meas = {
        int(parts[i]): [float(x) for x in re.findall(r"(?m)^\s*\d+\s+([\d.eE+-]+)\s+[\d.eE+-]+", parts[i + 1])]
        for i in range(1, len(parts), 2)
    }
    return [meas[i][0] for i in range(16)], [meas[i][7] for i in range(16)]


def plot_stuckat_samples(healthy: list[float], faulty: list[float], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 2.7), constrained_layout=True)
    ax.plot(range(16), healthy, marker="o", linestyle="none", markersize=5, label="Sano (NUDO=0, SV=0)")
    ax.plot(range(16), faulty, marker="s", linestyle="none", markersize=8, markerfacecolor="none", markeredgewidth=1.2, label="Fallo (NUDO=7, SV=0)")
    ax.axhline(1.65, linestyle="--", color="gray", linewidth=0.8, label="Umbral 1,65 V")
    for x in (5, 6):
        ax.axvspan(x - 0.35, x + 0.35, color="gold", alpha=0.25)
    ax.set_xticks(range(16), [format(i, "04b") for i in range(16)], rotation=45, fontsize=8)
    ax.set(xlabel="Vector dcba (una muestra estable por vector)", ylabel="V(Y) [V]", ylim=(-0.35, 3.65))
    ax.grid(axis="y", alpha=0.3)
    ax.legend(ncol=3, fontsize=8, loc="center right")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_10node_schematic(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x: float, y: float, w: float, h: float, text: str) -> None:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, lw=1.5))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11)

    def line(points: list[tuple[float, float]]) -> None:
        ax.plot([p[0] for p in points], [p[1] for p in points], color="black", lw=1.2)

    def label(x: float, y: float, n: int) -> None:
        ax.text(x, y, str(n), color="#aa0000", fontsize=10, fontweight="bold", ha="center", va="bottom")

    box(3.2, 4.3, 1.5, 1.1, "NAND2")
    box(3.2, 0.9, 1.5, 1.1, "NOR2")
    box(6.0, 3.4, 1.5, 1.1, "AND2")
    box(9.2, 2.2, 1.5, 1.6, "OR3")
    for name, y in [("d", 6.4), ("c", 5.9), ("b", 5.5), ("a", 5.0)]:
        ax.text(0.3, y, name, fontsize=12, ha="right")
    line([(0.45, 6.4), (8.4, 6.4), (8.4, 3.5), (9.2, 3.5)]); label(8.9, 3.5, 1)
    line([(0.45, 5.9), (5.5, 5.9), (5.5, 4.2), (6.0, 4.2)]); label(5.7, 4.2, 2)
    line([(0.45, 5.5), (2.6, 5.5), (2.6, 5.1), (3.2, 5.1)]); label(2.9, 5.1, 3)
    line([(0.45, 5.0), (2.3, 5.0), (2.3, 4.6), (3.2, 4.6)]); label(2.9, 4.6, 4)
    line([(1.3, 5.5), (1.3, 1.7), (3.2, 1.7)]); label(2.9, 1.7, 5)
    line([(1.9, 5.0), (1.9, 1.2), (3.2, 1.2)]); label(2.9, 1.2, 6)
    ax.plot([1.3, 1.9], [5.5, 5.0], "ko", markersize=4)
    line([(4.7, 4.85), (5.2, 4.85), (5.2, 3.7), (6.0, 3.7)]); label(5.5, 3.7, 7)
    line([(4.7, 1.45), (8.1, 1.45), (8.1, 2.5), (9.2, 2.5)]); label(8.9, 2.5, 8)
    line([(7.5, 3.95), (8.6, 3.95), (8.6, 3.0), (9.2, 3.0)]); label(8.9, 3.0, 9)
    line([(10.7, 3.0), (11.6, 3.0)]); label(11.2, 3.0, 10)
    ax.text(11.7, 3, "Y", fontsize=12)
    ax.text(6, 0.15, "Números: nudos de test; cruce sin punto = sin conexión", ha="center", fontsize=9)
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate LD4 Part 1 figures")
    parser.add_argument("--log", type=Path, help="Optional local P1_segf_stuckat.log file")
    args = parser.parse_args()

    ld4_root = Path(__file__).resolve().parent.parent
    fig_dir = ld4_root / "figuras"
    fig_dir.mkdir(exist_ok=True)

    healthy, faulty = load_from_log(args.log) if args.log else load_from_csv(ld4_root)
    plot_stuckat_samples(healthy, faulty, fig_dir / "stuckat_muestras.png")
    plot_10node_schematic(fig_dir / "esquema_nudos.png")
    print(f"Saved figures in {fig_dir}")


if __name__ == "__main__":
    main()
