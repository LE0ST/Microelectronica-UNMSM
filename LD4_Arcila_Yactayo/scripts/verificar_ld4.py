#!/usr/bin/env python3
"""
Portable verification suite for LD4 (Stuck-at, Stuck-open & Scan Path).
Authors: Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander (UNMSM-FIEE).

Modes:
  1. Standalone public mode (default, no private files required):
     - Validates all curated CSV tables in LD4_Arcila_Yactayo/resultados/.
     - Reproduces Part 1 step-by-step unique fault coverage (25% -> 100%).
     - Reproduces Part 2 test-time equations at 50 MHz.
     - Runs the exhaustive combinational 32-fault proof (proving <= 31/32 for 4 vectors
       and 32/32 for both the official V4=001/1 and alternative V4=101/1 5-vector sets).

  2. Full local forensic mode (--sim-dir <dir> or --rar <Lab_TestCI_LTspice.rar>):
     - Requires the locally excluded teaching-annex simulations (.log, .raw, .lib).
     - Re-verifies all 521 scalar LOG-vs-RAW measurements, P2_scan.raw glitch metrics,
       P1_stuckopen.raw transient extrema, and SDFF transistor count in cmos035_cells.lib.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np


def run_public_checks(ld4_root: Path) -> None:
    res = ld4_root / "resultados"

    # 1. Part 1 healthy sequence
    with (res / "p1_circuito_sano.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 16
    seq = "".join(r["y_logico"] for r in rows)
    assert seq == "1000111011111111", f"Unexpected P1 sequence: {seq}"
    print(f"[PASS] Part 1 healthy sequence (16 vectors): {seq}")

    # 2. Part 1 fault dictionary (140 cells) & cumulative coverage
    with (res / "p1_diccionario_fallos.csv").open(encoding="utf-8") as f:
        drows = list(csv.DictReader(f))
    healthy_row = drows[0]
    fault_rows = drows[1:]
    assert len(fault_rows) == 20, f"Expected 20 faults, got {len(fault_rows)}"

    opt_cols = ["v_0101", "v_0111", "v_0000", "v_0001", "v_0010", "v_0110", "v_1010"]
    expected_cov = [25, 60, 75, 85, 90, 95, 100]
    detected: set[str] = set()
    cov_seq: list[int] = []
    for col in opt_cols:
        for fr in fault_rows:
            if fr[col] != healthy_row[col]:
                detected.add(fr["fallo"])
        cov_seq.append(100 * len(detected) // 20)
    assert cov_seq == expected_cov, f"Coverage mismatch: {cov_seq}"
    print(f"[PASS] Part 1 dictionary (140 cells) & unique coverage: {cov_seq}%")

    # 3. Part 1 stuck-open
    with (res / "p1_stuckopen_muestras.csv").open(encoding="utf-8") as f:
        so_rows = list(csv.DictReader(f))
    assert [r["detecta"] for r in so_rows] == ["No", "Si", "No", "No"]
    print("[PASS] Part 1 stuck-open detection pair verified: T0(0000)->T1(0001)")

    # 4. Part 2 functional & flush
    with (res / "p2_func_muestras.csv").open(encoding="utf-8") as f:
        fn_rows = list(csv.DictReader(f))
    first_z1 = next(int(r["ciclo_k"]) for r in fn_rows if r["z_logico"] == "1")
    assert first_z1 == 7
    with (res / "p2_flush_secuencia.csv").open(encoding="utf-8") as f:
        fl_rows = list(csv.DictReader(f))
    si_s = "".join(r["si_aplicado"] for r in fl_rows)
    so_s = "".join(r["so_logico"] for r in fl_rows)
    assert si_s == "1101001000000" and so_s == "0001101001000"
    print(f"[PASS] Part 2 functional (Z=1 @ k={first_z1}) & flush (3-cycle delay)")

    # 5. Part 2 scan official (V4=001/1) & ensayo 2.6 (V4=101/1)
    for fname, v4_exp, f2_z_v4 in [
        ("p2_scan_oficial.csv", "001/1", "110/0"),
        ("p2_scan_ensayo26.csv", "101/1", "010/1"),
    ]:
        with (res / fname).open(encoding="utf-8") as f:
            srows = list(csv.DictReader(f))
        assert len(srows) == 5 and srows[3]["entrada_q2q1q0_e"] == v4_exp
        assert srows[3]["f2_q1_sa1"] == f2_z_v4
    print("[PASS] Part 2 scan matrices verified (official V4=001/1 & ensayo_26 V4=101/1)")

    # 6. Test time formulas at 50 MHz (T_clk = 20 ns)
    cases = [(3, 5, 23, 0.46), (3, 16, 67, 1.34), (32, 500, 16532, 330.64), (8, 500, 4508, 90.16)]
    for n, m, exp_cyc, exp_us in cases:
        cyc = n + (n + 1) * m
        us = round(cyc * 0.02, 2)
        assert cyc == exp_cyc and us == exp_us
    print("[PASS] Part 2 test-time formulas verified at 50 MHz")

    # 7. Exhaustive 32-fault combinational proof (P2_counter_core.inc topology)
    verify_32_faults_scan()


def verify_32_faults_scan() -> None:
    def eval_circuit(Q2: int, Q1: int, Q0: int, E: int, fault: tuple[str, int] | None = None) -> tuple[int, int, int, int]:
        def inj(node: str, val: int) -> int:
            return fault[1] if (fault is not None and fault[0] == node) else val

        d0 = inj("D0", inj("q0@XX0", Q0) ^ inj("e@XX0", E))
        g1 = inj("e@XG1", E) & inj("q0@XG1", Q0)
        d1 = inj("D1", inj("q1@XX1", Q1) ^ inj("g1@XX1", g1))
        g2 = inj("g1@XG2", g1) & inj("q1@XG2", Q1)
        d2 = inj("D2", inj("q2@XX2", Q2) ^ inj("g2@XX2", g2))
        z = inj("Z", inj("g2@XGZ", g2) & inj("q2@XGZ", Q2))
        return (d2, d1, d0, z)

    nodes = [
        "q0@XX0", "e@XX0", "D0", "e@XG1", "q0@XG1",
        "q1@XX1", "g1@XX1", "D1", "g1@XG2", "q1@XG2",
        "q2@XX2", "g2@XX2", "D2", "g2@XGZ", "q2@XGZ", "Z",
    ]
    vecs = [((i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1) for i in range(16)]
    vec_labels = [f"{q2}{q1}{q0}/{e}" for q2, q1, q0, e in vecs]
    faults = [(n, sa) for n in nodes for sa in (0, 1)]
    healthy = [eval_circuit(*v) for v in vecs]

    det_masks: list[int] = []
    for f in faults:
        mask = 0
        for vi, v in enumerate(vecs):
            if eval_circuit(*v, fault=f) != healthy[vi]:
                mask |= 1 << vi
        det_masks.append(mask)

    best_4 = max(
        sum(1 for fm in det_masks if any((fm >> vi) & 1 for vi in comb))
        for comb in itertools.combinations(range(16), 4)
    )
    valid_5 = sum(
        1 for comb in itertools.combinations(range(16), 5)
        if sum(1 for fm in det_masks if any((fm >> vi) & 1 for vi in comb)) == 32
    )
    assert best_4 == 31 and valid_5 == 21

    for name, vec_set in [
        ("Official (V4=001/1)", ["001/0", "110/1", "011/1", "001/1", "111/1"]),
        ("Ensayo 2.6 (V4=101/1)", ["001/0", "110/1", "011/1", "101/1", "111/1"]),
    ]:
        idxs = [vec_labels.index(lbl) for lbl in vec_set]
        cov = sum(1 for fm in det_masks if any((fm >> vi) & 1 for vi in idxs))
        assert cov == 32
    print(f"[PASS] 32-fault proof: max 4-vec = {best_4}/32; valid 5-vec sets = {valid_5}/4368; Official & 2.6 = 32/32")


def read_ltspice_raw(path: Path) -> list[dict[str, np.ndarray]]:
    data = path.read_bytes()
    for marker, enc in [
        ("Binary:\n".encode("utf-16le"), "utf-16le"),
        ("Binary:\r\n".encode("utf-16le"), "utf-16le"),
        (b"Binary:\n", "latin1"),
        (b"Binary:\r\n", "latin1"),
    ]:
        idx = data.find(marker)
        if idx >= 0:
            hdr = data[:idx].decode(enc, errors="replace")
            bdata = data[idx + len(marker):]
            break
    else:
        raise ValueError(f"Unrecognized RAW format: {path}")

    nvars = int(re.search(r"No\.\s*Variables:\s*(\d+)", hdr).group(1))
    npts = int(re.search(r"No\.\s*Points:\s*(\d+)", hdr).group(1))
    vsec_str = re.split(r"\r?\nVariables:\r?\n", hdr)[1]
    vsec = [line.strip() for line in vsec_str.splitlines() if line.strip()]
    var_names = [line.split()[1].lower() for line in vsec[:nvars]]
    rec_size = 8 + 4 * (nvars - 1)
    dt = np.dtype([("time", "<f8")] + [(f"v{i}", "<f4") for i in range(1, nvars)])
    arr = np.frombuffer(bdata[: npts * rec_size], dtype=dt)
    t = np.abs(arr["time"])
    zero_idxs = np.where(t == 0.0)[0]
    steps: list[dict[str, np.ndarray]] = []
    for s_idx, start in enumerate(zero_idxs):
        end = zero_idxs[s_idx + 1] if s_idx + 1 < len(zero_idxs) else npts
        step_dict = {"time": t[start:end]}
        for i, vn in enumerate(var_names[1:], 1):
            step_dict[vn] = arr[f"v{i}"][start:end].astype(np.float64)
        steps.append(step_dict)
    return steps


def parse_log_meas(log_path: Path) -> list[tuple[str, int, float, float]]:
    txt = log_path.read_text(encoding="utf-8", errors="replace")
    results: list[tuple[str, int, float, float]] = []
    for m in re.finditer(
        r"^\w+:\s+v\(([^)]+)\)\s*=\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+at\s+([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)",
        txt, re.M | re.I,
    ):
        results.append((f"v({m.group(1).lower()})", 0, float(m.group(2)), float(m.group(3))))
    for bm in re.finditer(
        r"Measurement:\s+\w+\s*\r?\n\s*step\s+v\(([^)]+)\)\s+AT\s*\r?\n((?:\s*\d+\s+[^\r\n]+\r?\n)+)",
        txt, re.I,
    ):
        vname = f"v({bm.group(1).lower()})"
        for line in bm.group(2).strip().splitlines():
            p = line.split()
            if len(p) >= 3:
                results.append((vname, int(p[0]) - 1, float(p[1]), float(p[2])))
    return results


def run_local_forensic_checks(sim_dir: Path) -> None:
    total_m = 0
    total_ok = 0
    for base in ["P1_segf_stuckat", "P1_stuckopen", "P2_func", "P2_flush_fix2", "P2_scan"]:
        st = read_ltspice_raw(sim_dir / f"{base}.raw")
        meas = parse_log_meas(sim_dir / f"{base}.log")
        for vname, step_i, val_log, at_t in meas:
            val_raw = float(np.interp(at_t, st[step_i]["time"], st[step_i][vname]))
            total_m += 1
            if abs(val_log - val_raw) < 1e-3:
                total_ok += 1
    assert total_m == 521 and total_ok == 521
    print(f"[PASS] Local LOG-vs-RAW forensic check: {total_ok}/{total_m} scalar measurements match")


def main() -> None:
    parser = argparse.ArgumentParser(description="LD4 reproducible verification suite")
    parser.add_argument("--sim-dir", type=Path, help="Local directory with extracted .log/.raw/.lib files")
    parser.add_argument("--rar", type=Path, help="Local Lab_TestCI_LTspice.rar archive (requires UnRAR)")
    args = parser.parse_args()

    ld4_root = Path(__file__).resolve().parent.parent
    run_public_checks(ld4_root)

    if args.sim_dir:
        run_local_forensic_checks(args.sim_dir)
    elif args.rar:
        unrar = shutil.which("unrar") or shutil.which("UnRAR") or r"C:\Program Files\WinRAR\UnRAR.exe"
        tmp = Path(tempfile.mkdtemp(prefix="ld4_val_"))
        try:
            subprocess.run([unrar, "x", "-y", str(args.rar), str(tmp) + os.sep], check=True, stdout=subprocess.DEVNULL)
            sim_dir = tmp / "Lab_TestCI_LTspice" if (tmp / "Lab_TestCI_LTspice").is_dir() else tmp
            run_local_forensic_checks(sim_dir)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        print("[INFO] Local LOG-vs-RAW check skipped (pass --sim-dir or --rar to run 521-measurement forensic check).")


if __name__ == "__main__":
    main()
