#!/usr/bin/env python3
"""
Portable verification suite for LD4 (Stuck-at, Stuck-open & Scan Path).
Authors: Leonardo Sait Yactayo Tolentino & Marco Antonio Arcila Santander (UNMSM-FIEE).

Modes:
  1. Standalone public mode (default, no excluded private/course files required):
     - Validates Part I healthy sequence (16 vectors) against Boolean equation.
     - Recomputes and validates all 140 cells (20 faults x 7 vectors) of
       resultados/p1_diccionario_fallos.csv from the 10-node gate netlist.
     - Reproduces Part I step-by-step unique fault coverage (25% -> 100%).
     - Validates Part I stuck-open detection pair T0(0000)->T1(0001).
     - Validates Part II functional (k=7) and flush (3-cycle delay) sequences.
     - Recomputes and validates all 25 responses (5 vectors x 5 FAULT=0..4 runs)
       for both official (V4=001/1) and alternative (V4=101/1) scan matrices.
     - Reproduces Part II test-time equations at 50 MHz.
     - Runs the exhaustive combinational 32-fault proof (<= 31/32 for 4 vectors;
       32/32 for both 5-vector sets).

  2. Full local forensic mode (--sim-dir <dir> or --rar <Lab_TestCI_LTspice.rar>):
     - Requires locally excluded course simulation files (.log, .raw, cmos035_cells.lib).
     - Re-verifies exact per-file and total (521) scalar LOG-vs-RAW measurements and reports max|LOG-RAW|.
     - Reproduces P2_scan.raw Z glitch metrics (peak, width > 1.65 V, FWHM).
     - Reproduces P1_stuckopen.raw transient extrema (T1, T2, T3) and .meas samples.
     - Mandatorily verifies individual subcircuit MOS counts (INV=2, TG=2, NOR2=4, AND2=6,
       XOR2=12, SDFF=28) and core total (138 MOS, separate from 8 output buffer MOS) in cmos035_cells.lib.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np


def eval_p1_gate_netlist(d: int, c: int, b: int, a: int, fault: tuple[int, int] | None = None) -> int:
    """Evaluate 10-node BCD segment-f gate netlist with optional single stuck-at fault."""
    def inj(node: int, val: int) -> int:
        return fault[1] if (fault is not None and fault[0] == node) else val

    n1 = inj(1, d)
    n2 = inj(2, c)
    n3 = inj(3, b)
    n4 = inj(4, a)
    n5 = inj(5, b)
    n6 = inj(6, a)
    n7 = inj(7, 1 - (n3 & n4))       # NAND2(b, a)
    n8 = inj(8, 1 - (n5 | n6))       # NOR2(b, a)
    n9 = inj(9, n2 & n7)             # AND2(c, nand)
    n10 = inj(10, n1 | n8 | n9)      # OR3(d, nor, and)
    return n10


def eval_p2_scan_core(q2: int, q1: int, q0: int, e: int, fault_id: int) -> str:
    """Evaluate 3-bit scan-path combinational core for FAULT=0..4."""
    e_x0 = 1 if fault_id == 4 else e
    d0 = q0 ^ e_x0
    g1 = e & q0
    g1_x1 = 0 if fault_id == 1 else g1
    d1 = q1 ^ g1_x1
    q1_g2 = 1 if fault_id == 2 else q1
    g2 = g1 & q1_g2
    d2x = q2 ^ g2
    d2 = 0 if fault_id == 3 else d2x
    z = g2 & q2
    return f"{d2}{d1}{d0}/{z}"


def run_public_checks(ld4_root: Path) -> None:
    res = ld4_root / "resultados"

    # 1. Part I healthy sequence (16 vectors vs Boolean model)
    with (res / "p1_circuito_sano.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 16
    for i, r in enumerate(rows):
        d, c, b, a = (i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1
        assert int(r["y_logico"]) == eval_p1_gate_netlist(d, c, b, a)
    seq = "".join(r["y_logico"] for r in rows)
    assert seq == "1000111011111111"
    print(f"[PASS] Part I healthy sequence (16/16 vectors match Boolean model): {seq}")

    # 2. Part I fault dictionary: recompute & check all 140 cells (20 faults x 7 vectors)
    with (res / "p1_diccionario_fallos.csv").open(encoding="utf-8") as f:
        drows = list(csv.DictReader(f))
    assert len(drows) == 21  # healthy + 20 faults
    opt_cols = ["v_0101", "v_0111", "v_0000", "v_0001", "v_0010", "v_0110", "v_1010"]
    opt_bits = [(int(c[2]), int(c[3]), int(c[4]), int(c[5])) for c in opt_cols]

    healthy_row = drows[0]
    for col, bits in zip(opt_cols, opt_bits):
        assert int(healthy_row[col]) == eval_p1_gate_netlist(*bits)

    fault_rows = drows[1:]
    cells_checked = 0
    for fr in fault_rows:
        m = re.match(r"^(\d+)/s-a-([01])$", fr["fallo"])
        assert m, f"Unexpected fault label: {fr['fallo']}"
        fault = (int(m.group(1)), int(m.group(2)))
        for col, bits in zip(opt_cols, opt_bits):
            expected_y = eval_p1_gate_netlist(*bits, fault=fault)
            assert int(fr[col]) == expected_y, f"Mismatch at {fr['fallo']} {col}"
            cells_checked += 1
    assert cells_checked == 140

    expected_cov = [25, 60, 75, 85, 90, 95, 100]
    detected: set[str] = set()
    cov_seq: list[int] = []
    for col in opt_cols:
        for fr in fault_rows:
            if fr[col] != healthy_row[col]:
                detected.add(fr["fallo"])
        cov_seq.append(100 * len(detected) // 20)
    assert cov_seq == expected_cov
    print(f"[PASS] Part I dictionary ({cells_checked}/140 cells) & unique coverage: {cov_seq}%")

    # 3. Part I stuck-open
    with (res / "p1_stuckopen_muestras.csv").open(encoding="utf-8") as f:
        so_rows = list(csv.DictReader(f))
    assert [r["detecta"] for r in so_rows] == ["No", "Si", "No", "No"]
    print("[PASS] Part I stuck-open detection pair verified: T0(0000)->T1(0001)")

    # 4. Part II functional & flush
    with (res / "p2_func_muestras.csv").open(encoding="utf-8") as f:
        fn_rows = list(csv.DictReader(f))
    first_z1 = next(int(r["ciclo_k"]) for r in fn_rows if r["z_logico"] == "1")
    assert first_z1 == 7
    with (res / "p2_flush_secuencia.csv").open(encoding="utf-8") as f:
        fl_rows = list(csv.DictReader(f))
    si_s = "".join(r["si_aplicado"] for r in fl_rows)
    so_s = "".join(r["so_logico"] for r in fl_rows)
    assert si_s == "1101001000000" and so_s == "0001101001000"
    print(f"[PASS] Part II functional (Z=1 @ k={first_z1}) & flush (3-cycle delay)")

    # 5. Part II scan matrices: recompute & verify all 25 combinations for official & ensayo_26
    fault_cols = ["f0_sano", "f1_g1_sa0", "f2_q1_sa1", "f3_d2_sa0", "f4_e_sa1"]
    for label, fname, v4_exp in [
        ("official", "p2_scan_oficial.csv", "001/1"),
        ("ensayo_26", "p2_scan_ensayo26.csv", "101/1"),
    ]:
        with (res / fname).open(encoding="utf-8") as f:
            srows = list(csv.DictReader(f))
        assert len(srows) == 5 and srows[3]["entrada_q2q1q0_e"] == v4_exp
        combos = 0
        first_det: dict[int, str] = {}
        for r in srows:
            vin = r["entrada_q2q1q0_e"]
            q2, q1, q0, e = int(vin[0]), int(vin[1]), int(vin[2]), int(vin[4])
            healthy_resp = eval_p2_scan_core(q2, q1, q0, e, 0)
            for fid, col in enumerate(fault_cols):
                expected_resp = eval_p2_scan_core(q2, q1, q0, e, fid)
                assert r[col] == expected_resp, f"Mismatch {label} {r['vector']} {col}"
                if fid > 0 and fid not in first_det and expected_resp != healthy_resp:
                    first_det[fid] = r["vector"]
                combos += 1
        assert combos == 25
        assert first_det == {1: "V3", 2: "V4", 3: "V2", 4: "V1"}
    print("[PASS] Part II scan matrices (25/25 official V4=001/1 & 25/25 ensayo_26 V4=101/1; F1->V3, F2->V4, F3->V2, F4->V1)")

    # 6. Test time formulas at 50 MHz (T_clk = 20 ns)
    cases = [(3, 5, 23, 0.46), (3, 16, 67, 1.34), (32, 500, 16532, 330.64), (8, 500, 4508, 90.16)]
    for n, m, exp_cyc, exp_us in cases:
        cyc = n + (n + 1) * m
        us = round(cyc * 0.02, 2)
        assert cyc == exp_cyc and us == exp_us
    print("[PASS] Part II test-time formulas verified at 50 MHz")

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

    for vec_set in [
        ["001/0", "110/1", "011/1", "001/1", "111/1"],
        ["001/0", "110/1", "011/1", "101/1", "111/1"],
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


def crossing_width(t_arr: np.ndarray, v_arr: np.ndarray, thresh: float) -> float:
    above = v_arr >= thresh
    idxs = np.where(np.diff(above.astype(int)) != 0)[0]
    if len(idxs) < 2:
        raise ValueError(f"Fewer than 2 crossings at threshold {thresh}")
    i1, i2 = int(idxs[0]), int(idxs[-1])
    t1 = t_arr[i1] + (thresh - v_arr[i1]) * (t_arr[i1 + 1] - t_arr[i1]) / (v_arr[i1 + 1] - v_arr[i1])
    t2 = t_arr[i2] + (thresh - v_arr[i2]) * (t_arr[i2 + 1] - t_arr[i2]) / (v_arr[i2 + 1] - v_arr[i2])
    return float(t2 - t1)


EXPECTED_LOG_MEAS_COUNTS: dict[str, int] = {
    "P1_segf_stuckat": 352,
    "P1_stuckopen": 16,
    "P2_func": 40,
    "P2_flush_fix2": 13,
    "P2_scan": 100,
}
EXPECTED_TOTAL_LOG_MEAS = 521
MAX_LOG_RAW_ERR_V = 1e-11

EXPECTED_SUBCKT_MOS_COUNTS: dict[str, int] = {
    "INV": 2,
    "TG": 2,
    "NOR2": 4,
    "AND2": 6,
    "XOR2": 12,
    "SDFF": 28,
}
EXPECTED_CORE_MOS = 138
EXPECTED_OUTPUT_BUFFER_MOS = 8


def count_lib_transistors(lib_path: Path) -> dict[str, int]:
    if not lib_path.is_file():
        raise FileNotFoundError(f"Missing CMOS library file: {lib_path}")
    txt = lib_path.read_text(encoding="utf-8", errors="replace")
    subckts: dict[str, list[str]] = {}
    cur = None
    for line in txt.splitlines():
        s = line.strip()
        if not s or s.startswith("*"):
            continue
        if s.lower().startswith(".subckt "):
            cur = s.split()[1].upper()
            subckts[cur] = []
        elif s.lower().startswith(".ends"):
            cur = None
        elif cur is not None:
            subckts[cur].append(s)

    def count_mos(name: str, visiting: set[str] | None = None) -> int:
        if name not in subckts:
            raise ValueError(f"Missing required subcircuit '{name}' in {lib_path}")
        stack = set() if visiting is None else set(visiting)
        if name in stack:
            raise ValueError(f"Cyclic subcircuit reference '{name}' in {lib_path}")
        stack.add(name)
        total = 0
        for line in subckts[name]:
            tok = line.split()
            if tok[0].upper().startswith("M"):
                total += 1
            elif tok[0].upper().startswith("X"):
                total += count_mos(tok[-1].upper(), stack)
        return total

    return {k: count_mos(k) for k in EXPECTED_SUBCKT_MOS_COUNTS}


def run_local_forensic_checks(sim_dir: Path, ld4_root: Path) -> None:
    if not sim_dir.is_dir():
        raise FileNotFoundError(f"Simulation directory not found: {sim_dir}")

    ref = json.loads((ld4_root / "resultados" / "resumen_verificacion_forense.json").read_text(encoding="utf-8"))
    ref_log = ref["log_raw_scalar_verification"]
    if (
        ref_log.get("breakdown") != EXPECTED_LOG_MEAS_COUNTS
        or ref_log.get("total_checked") != EXPECTED_TOTAL_LOG_MEAS
        or ref_log.get("total_matched") != EXPECTED_TOTAL_LOG_MEAS
        or sum(EXPECTED_LOG_MEAS_COUNTS.values()) != EXPECTED_TOTAL_LOG_MEAS
    ):
        raise ValueError(
            "Inconsistent LOG-RAW breakdown between script constants and "
            f"resumen_verificacion_forense.json: {ref_log}"
        )

    # 1. Exact LOG-vs-RAW max absolute error across all 521 scalar measurements
    total_m = 0
    global_max_err = 0.0
    for base, expected_count in EXPECTED_LOG_MEAS_COUNTS.items():
        raw_path = sim_dir / f"{base}.raw"
        log_path = sim_dir / f"{base}.log"
        if not raw_path.is_file():
            raise FileNotFoundError(f"Missing required RAW file: {raw_path}")
        if not log_path.is_file():
            raise FileNotFoundError(f"Missing required LOG file: {log_path}")

        st = read_ltspice_raw(raw_path)
        if not st:
            raise ValueError(f"No simulation steps found in RAW file: {raw_path}")
        meas = parse_log_meas(log_path)
        if len(meas) != expected_count:
            raise ValueError(
                f"Measurement count mismatch in {log_path.name}: "
                f"expected {expected_count}, got {len(meas)}"
            )

        file_max = 0.0
        for vname, step_i, val_log, at_t in meas:
            if step_i < 0 or step_i >= len(st):
                raise ValueError(
                    f"Missing simulation step {step_i} in {raw_path.name} "
                    f"(available steps: {len(st)}) for {vname}"
                )
            step_data = st[step_i]
            if vname not in step_data:
                raise ValueError(f"Missing signal '{vname}' in {raw_path.name} step {step_i}")
            t_arr = step_data["time"]
            v_arr = step_data[vname]
            if len(t_arr) == 0 or len(v_arr) == 0:
                raise ValueError(f"Empty waveform for '{vname}' in {raw_path.name} step {step_i}")
            if not (np.isfinite(val_log) and np.isfinite(at_t)):
                raise ValueError(
                    f"Non-finite LOG measurement for '{vname}' in {log_path.name} step {step_i}"
                )
            if at_t < float(t_arr[0]) or at_t > float(t_arr[-1]):
                raise ValueError(
                    f"Measurement time {at_t} outside RAW time range "
                    f"[{float(t_arr[0])}, {float(t_arr[-1])}] in {raw_path.name} step {step_i} ({vname})"
                )
            val_raw = float(np.interp(at_t, t_arr, v_arr))
            if not np.isfinite(val_raw):
                raise ValueError(
                    f"Non-finite interpolated RAW value for '{vname}' in {raw_path.name} "
                    f"step {step_i} at t={at_t}"
                )
            err = abs(val_log - val_raw)
            file_max = max(file_max, err)
            global_max_err = max(global_max_err, err)
            total_m += 1
        print(
            f"[PASS] Local LOG-vs-RAW {base}: {len(meas)}/{expected_count} meas, "
            f"max|LOG-RAW| = {file_max:.3e} V"
        )

    if total_m != EXPECTED_TOTAL_LOG_MEAS:
        raise ValueError(
            f"Total LOG-vs-RAW measurements mismatch: expected {EXPECTED_TOTAL_LOG_MEAS}, got {total_m}"
        )
    if not np.isfinite(global_max_err) or global_max_err >= MAX_LOG_RAW_ERR_V:
        raise ValueError(
            f"Global max|LOG-RAW| exceeds limit {MAX_LOG_RAW_ERR_V:.1e} V: {global_max_err:.3e} V"
        )
    print(
        f"[PASS] Local LOG-vs-RAW total: {total_m}/{EXPECTED_TOTAL_LOG_MEAS}, "
        f"global max|LOG-RAW| = {global_max_err:.3e} V"
    )

    # 2. P2_scan.raw Z glitch metrics
    st_scan = read_ltspice_raw(sim_dir / "P2_scan.raw")
    t_ns = st_scan[0]["time"] * 1e9
    vz = st_scan[0]["v(z)"]
    m = (t_ns >= 229.5) & (t_ns <= 232.0)
    tw, vw = t_ns[m], vz[m]
    imax = int(np.argmax(vw))
    v_peak, t_peak = float(vw[imax]), float(tw[imax])
    w_165 = crossing_width(tw, vw, 1.65)
    w_fwhm = crossing_width(tw, vw, v_peak / 2.0)
    g_ref = ref["p2_scan_glitch_V3_raw_FAULT0"]
    assert abs(v_peak - g_ref["peak_V"]) < 1e-5
    assert abs(t_peak - g_ref["peak_ns"]) < 1e-4
    assert abs(w_165 - g_ref["width_above_1p65V_ns"]) < 1e-5
    assert abs(w_fwhm - g_ref["fwhm_ns"]) < 1e-5
    print(f"[PASS] Local Z glitch (P2_scan.raw V3): peak={v_peak:.6f} V @ {t_peak:.3f} ns, >1.65V={w_165:.6f} ns, FWHM={w_fwhm:.6f} ns")

    # 3. P1_stuckopen.raw transient extrema
    st_so = read_ltspice_raw(sim_dir / "P1_stuckopen.raw")
    t_so = st_so[1]["time"] * 1e9
    vo8 = st_so[1]["v(o8)"]
    so_ref = ref["p1_stuckopen_raw_extrema_RSO_1T"]
    t1_max = float(np.max(vo8[(t_so >= 10) & (t_so <= 20)]))
    t2_max = float(np.max(vo8[(t_so >= 20) & (t_so <= 30)]))
    t3_min = float(np.min(vo8[(t_so >= 30) & (t_so <= 40)]))
    assert abs(t1_max - so_ref["T1_max_V"]) < 1e-5
    assert abs(t2_max - so_ref["T2_max_V"]) < 1e-5
    assert abs(t3_min - so_ref["T3_min_V"]) < 1e-5
    print(f"[PASS] Local stuck-open extrema (P1_stuckopen.raw RSO=1T): T1_max={t1_max:.6f} V, T2_max={t2_max:.6f} V, T3_min={t3_min:.6f} V")

    # 4. Mandatory CMOS 0.35 um library transistor count in cmos035_cells.lib
    lib_path = sim_dir / "cmos035_cells.lib"
    if not lib_path.is_file():
        raise FileNotFoundError(f"Missing required CMOS library in forensic mode: {lib_path}")

    counts = count_lib_transistors(lib_path)
    ref_lib = ref["sdff_transistors_cmos035_cells"]
    for subckt, expected_cnt in EXPECTED_SUBCKT_MOS_COUNTS.items():
        if ref_lib.get(subckt) != expected_cnt:
            raise ValueError(
                f"Inconsistent expected count for '{subckt}' in resumen_verificacion_forense.json: "
                f"expected {expected_cnt}, got {ref_lib.get(subckt)}"
            )
        if counts[subckt] != expected_cnt:
            raise ValueError(
                f"MOS count mismatch for subcircuit '{subckt}' in {lib_path.name}: "
                f"expected {expected_cnt}, got {counts[subckt]}"
            )

    core = 3 * counts["XOR2"] + 3 * counts["AND2"] + 3 * counts["SDFF"]
    if ref_lib.get("core_total") != EXPECTED_CORE_MOS or ref_lib.get("output_buffers") != EXPECTED_OUTPUT_BUFFER_MOS:
        raise ValueError(
            "Inconsistent core_total/output_buffers in resumen_verificacion_forense.json: "
            f"{ref_lib}"
        )
    if core != EXPECTED_CORE_MOS:
        raise ValueError(
            f"Core MOS total mismatch (3*XOR2 + 3*AND2 + 3*SDFF): expected {EXPECTED_CORE_MOS}, got {core}"
        )

    subckt_summary = ", ".join(f"{k}={counts[k]}" for k in EXPECTED_SUBCKT_MOS_COUNTS)
    print(
        f"[PASS] Local library check ({lib_path.name}): {subckt_summary} MOS; "
        f"core={core} MOS (output_buffers={EXPECTED_OUTPUT_BUFFER_MOS} MOS separate)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="LD4 reproducible verification suite")
    parser.add_argument("--sim-dir", type=Path, help="Local directory with excluded .log/.raw/.lib files")
    parser.add_argument("--rar", type=Path, help="Local Lab_TestCI_LTspice.rar archive (requires UnRAR)")
    args = parser.parse_args()

    ld4_root = Path(__file__).resolve().parent.parent
    run_public_checks(ld4_root)

    if args.sim_dir:
        run_local_forensic_checks(args.sim_dir, ld4_root)
    elif args.rar:
        unrar = shutil.which("unrar") or shutil.which("UnRAR") or r"C:\Program Files\WinRAR\UnRAR.exe"
        tmp = Path(tempfile.mkdtemp(prefix="ld4_val_"))
        try:
            subprocess.run([unrar, "x", "-y", str(args.rar), str(tmp) + os.sep], check=True, stdout=subprocess.DEVNULL)
            sim_dir = tmp / "Lab_TestCI_LTspice" if (tmp / "Lab_TestCI_LTspice").is_dir() else tmp
            run_local_forensic_checks(sim_dir, ld4_root)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        print("[INFO] Local forensic checks skipped (pass --sim-dir or --rar for LOG-vs-RAW, RAW extrema, and cmos035_cells.lib checks).")


if __name__ == "__main__":
    main()
