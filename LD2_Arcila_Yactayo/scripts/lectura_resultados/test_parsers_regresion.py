# -*- coding: utf-8 -*-
"""
Batería Integral de Pruebas de Regresión para Parsers de LTspice (.log y .raw)
Fase 2.1 - LD2 Microelectrónica UNMSM

Verificaciones automáticas:
1. Log Normal (Escalares estándar)
2. Log con Barrido (.step y tablas)
3. Log con Medición FAIL'ed
4. Log con Valor NaN
5. Log con Valor +INF
6. Log con Valor -INF
7. Log con Métrica Requerida Ausente
8. Log con Medición WHEN y timestamp 'AT'
9. RAW Real sin Step (UTF-16 y Delimitador)
10. RAW Real Stepped Transient (Caso A, 3 steps exactos, reinicio a cero)
11. RAW Real Stepped DC Ascendente (Caso B, 3 steps exactos, 0 -> 1V)
12. RAW Real Stepped DC Descendente (Caso C, 3 steps exactos, 1 -> 0V, sin micro-fragmentación)
13. RAW con Puntos Consecutivos Repetidos (Edge-case defensivo: t[i] == t[i-1] no divide el step)
14. RAW Multivariable Doble Precisión
15. RAW Truncado (Detección Estricta de bytes incompletos)
16. RAW Complejo No Soportado (Detección de datos AC/Noise sin falsa compatibilidad)
17. Invariante Estricto de Conservación de Puntos (sum(steps) == No. Points)
"""

import os
import sys
import math
import struct
import tempfile
import numpy as np

# Rutas del entorno
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from parse_spice_log import parse_log, get_metric, SpiceMeasurementError
from parse_spice_raw import read_raw

def run_test(test_name, test_func):
    try:
        test_func()
        print(f"[PASS] {test_name}")
        return True
    except Exception as e:
        print(f"[FAIL] {test_name}: {str(e)}")
        return False

# =====================================================================
# 1. PRUEBAS DE PARSER LOG
# =====================================================================

def test_log_normal():
    log_content = """LTspice 26.0.2 for Windows
Circuit: test_normal.cir
Direct Newton iteration succeeded in finding operating point.
Total elapsed time: 0.123 seconds.

vm: V(in) =0.4796748 at 0.4796748
voh: V(out) =0.999994 at 0
vol: V(out) =1.779e-06 at 1.0
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path, required_metrics=['vm', 'voh', 'vol'], raise_on_error=True)
        assert res['is_valid'] is True
        assert abs(res['measurements']['vm'] - 0.4796748) < 1e-6
        assert abs(res['measurements']['voh'] - 0.999994) < 1e-6
        assert abs(res['measurements']['vol'] - 1.779e-6) < 1e-9
        assert get_metric(res, 'vm', strict=True) == res['measurements']['vm']
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_step():
    log_content = """LTspice 26.0.2 for Windows
Circuit: test_step.cir

.step rval=1000
Direct Newton iteration succeeded.

.step rval=2000
Direct Newton iteration succeeded.

.step rval=5000
Direct Newton iteration succeeded.

Measurement: t_delay
  step	AVG(V(out))	FROM	TO
     1	1.5e-11	0	1e-08
     2	2.5e-11	0	1e-08
     3	5.5e-11	0	1e-08
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path)
        assert res['is_valid'] is True
        assert len(res['steps']) == 3
        assert res['steps'][0]['rval'] == 1000.0
        assert res['steps'][2]['rval'] == 5000.0
        assert 't_delay' in res['measurements']
        assert len(res['measurements']['t_delay']) == 3
        assert abs(res['measurements']['t_delay'][1]['val'] - 2.5e-11) < 1e-13
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_failed_metric():
    log_content = """LTspice 26.0.2 for Windows
Measurement "tphl" FAIL'ed
Measurement "tplh": 2.5e-11 at 1e-9
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path)
        assert res['is_valid'] is False
        assert 'tphl' in res['failed_measurements']
        assert res['measurements']['tphl'] is None

        raised = False
        try:
            parse_log(temp_path, required_metrics=['tphl'], raise_on_error=True)
        except SpiceMeasurementError:
            raised = True
        assert raised, "Debió levantar SpiceMeasurementError al fallar tphl requerido"

        raised_strict = False
        try:
            get_metric(res, 'tphl', strict=True)
        except SpiceMeasurementError:
            raised_strict = True
        assert raised_strict, "get_metric estricto debió levantar SpiceMeasurementError"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_nan():
    log_content = """LTspice 26.0.2 for Windows
v_nan: V(out)=NaN at 0.5
v_ok: 1.05 at 1.0
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path)
        assert res['is_valid'] is False
        assert 'v_nan' in res['invalid_measurements']
        assert math.isnan(res['measurements']['v_nan'])
        
        raised = False
        try:
            get_metric(res, 'v_nan', strict=True)
        except SpiceMeasurementError:
            raised = True
        assert raised, "get_metric estricto debió levantar SpiceMeasurementError para NaN"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_pos_inf():
    log_content = """LTspice 26.0.2 for Windows
gain_inf: +INF at 0.5
gain_win: 1.#INF at 0.6
v_ok: 1.0
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path)
        assert res['is_valid'] is False
        assert 'gain_inf' in res['invalid_measurements']
        assert 'gain_win' in res['invalid_measurements']
        assert math.isinf(res['measurements']['gain_inf']) and res['measurements']['gain_inf'] > 0
        assert math.isinf(res['measurements']['gain_win']) and res['measurements']['gain_win'] > 0
        
        raised = False
        try:
            get_metric(res, 'gain_inf', strict=True)
        except SpiceMeasurementError:
            raised = True
        assert raised, "get_metric estricto debió levantar SpiceMeasurementError para +INF"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_neg_inf():
    log_content = """LTspice 26.0.2 for Windows
drift_neg: -INF at 0.1
v_ok: 1.0
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path)
        assert res['is_valid'] is False
        assert 'drift_neg' in res['invalid_measurements']
        assert math.isinf(res['measurements']['drift_neg']) and res['measurements']['drift_neg'] < 0
        
        raised = False
        try:
            get_metric(res, 'drift_neg', strict=True)
        except SpiceMeasurementError:
            raised = True
        assert raised, "get_metric estricto debió levantar SpiceMeasurementError para -INF"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_missing_metric():
    log_content = """LTspice 26.0.2 for Windows
vm: 0.48
voh: 1.0
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path, required_metrics=['vm', 'voh', 'vol'])
        assert res['is_valid'] is False
        assert 'vol' in res['missing_metrics']
        
        raised = False
        try:
            parse_log(temp_path, required_metrics=['vol'], raise_on_error=True)
        except SpiceMeasurementError:
            raised = True
        assert raised, "Debió levantar SpiceMeasurementError por métrica requerida ausente"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_log_meas_when():
    # Verifica que mediciones tipo WHEN extraigan el timestamp/valor tras 'AT' y no el umbral de la condición
    log_content = """LTspice 26.0.2 for Windows
Circuit: test_when.cir
Total elapsed time: 0.458 seconds.

vdyn_min: V(dyn) =0.99957269696 at 3.9e-09
dv: {VDD}-Vdyn_min=0.000427303040482
t_rec: V(dyn)=0.99  AT 3.08030399678e-09
t_restore: t_rec-3.0n=8.03039967756e-11
v_cross: V(in)=V(out) AT 0.47967
"""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.log') as f:
        f.write(log_content)
        temp_path = f.name

    try:
        res = parse_log(temp_path, required_metrics=['t_rec', 't_restore', 'vdyn_min', 'v_cross'], raise_on_error=True)
        assert res['is_valid'] is True
        # t_rec debe extraer el timestamp tras 'AT' (3.0803e-9), no la tensión de la condición (0.99)
        assert abs(res['measurements']['t_rec'] - 3.08030399678e-09) < 1e-15
        assert abs(res['measurements']['t_restore'] - 8.03039967756e-11) < 1e-15
        # vdyn_min (FIND) debe extraer la tensión tras '=', no el tiempo tras 'at'
        assert abs(res['measurements']['vdyn_min'] - 0.99957269696) < 1e-10
        # v_cross debe extraer el valor tras 'AT'
        assert abs(res['measurements']['v_cross'] - 0.47967) < 1e-6
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

# =====================================================================
# 2. PRUEBAS DE PARSER RAW (ARCHIVOS REALES DE LTSPICE Y SINTÉTICOS)
# =====================================================================

def test_raw_unstepped_real():
    real_path = os.path.abspath(os.path.join(current_dir, "..", "..", "auxiliares", "caracterizacion_inversor", "inv_vtc_45hp_27C.raw"))
    if not os.path.exists(real_path):
        raise FileNotFoundError(f"Archivo real de prueba no encontrado: {real_path}")
    res = read_raw(real_path)
    assert res['is_stepped'] is False
    assert res['n_steps'] == 1
    assert res['metadata']['n_points'] == 2001
    assert len(res['data']['Vin']) == 2001

def test_raw_stepped_transient_real():
    # Caso A: Generado por LTspice 26.0.2 (.param Rval list 1k 2k 4k, .tran 0 10n)
    real_path = os.path.abspath(os.path.join(current_dir, "..", "..", "auxiliares", "pruebas_parsers", "caso_a_tran_step.raw"))
    if not os.path.exists(real_path):
        raise FileNotFoundError(f"Archivo real Caso A no encontrado: {real_path}")
    res = read_raw(real_path)
    assert res['is_stepped'] is True
    assert res['n_steps'] == 3, f"Se esperaban 3 steps, pero se detectaron {res['n_steps']}"
    assert len(res['steps']) == 3
    assert res['step_boundaries'] == [(0, 1045), (1045, 2090), (2090, 3135)]
    # Verificar reinicio de tiempo a 0.0 en cada paso
    for s in res['steps']:
        assert abs(s['time'][0] - 0.0) < 1e-15
        assert s['time'][-1] > 9.9e-9
    total_pts = sum(len(s['time']) for s in res['steps'])
    assert total_pts == res['metadata']['n_points'] == 3135

def test_raw_stepped_dc_ascending_real():
    # Caso B: Generado por LTspice 26.0.2 (.step param Rval list 1k 2k 4k, .dc V1 0 1 0.1)
    real_path = os.path.abspath(os.path.join(current_dir, "..", "..", "auxiliares", "pruebas_parsers", "caso_b_dc_asc_step.raw"))
    if not os.path.exists(real_path):
        raise FileNotFoundError(f"Archivo real Caso B no encontrado: {real_path}")
    res = read_raw(real_path)
    assert res['is_stepped'] is True
    assert res['n_steps'] == 3, f"Se esperaban 3 steps, pero se detectaron {res['n_steps']}"
    assert res['step_boundaries'] == [(0, 11), (11, 22), (22, 33)]
    for s in res['steps']:
        assert abs(s['V1'][0] - 0.0) < 1e-6
        assert abs(s['V1'][-1] - 1.0) < 1e-6
        assert len(s['V1']) == 11
    total_pts = sum(len(s['V1']) for s in res['steps'])
    assert total_pts == res['metadata']['n_points'] == 33

def test_raw_stepped_dc_descending_real():
    # Caso C: Generado por LTspice 26.0.2 (.step param Rval list 1k 2k 4k, .dc V1 1 0 -0.1)
    real_path = os.path.abspath(os.path.join(current_dir, "..", "..", "auxiliares", "pruebas_parsers", "caso_c_dc_desc_step.raw"))
    if not os.path.exists(real_path):
        raise FileNotFoundError(f"Archivo real Caso C no encontrado: {real_path}")
    res = read_raw(real_path)
    assert res['is_stepped'] is True
    assert res['n_steps'] == 3, f"Se esperaban 3 steps, pero se detectaron {res['n_steps']}"
    assert res['step_boundaries'] == [(0, 11), (11, 22), (22, 33)]
    for s in res['steps']:
        # Cada step debe barrer de 1.0 a 0.0 descendente
        assert abs(s['V1'][0] - 1.0) < 1e-6
        assert abs(s['V1'][-1] - 0.0) < 1e-6
        assert len(s['V1']) == 11
    total_pts = sum(len(s['V1']) for s in res['steps'])
    assert total_pts == res['metadata']['n_points'] == 33

def test_raw_repeated_points_no_split():
    # Edge-case defensivo: dentro de un mismo step, la variable contiene puntos repetidos t[i] == t[i-1]
    # El parser NO debe partir el step por esa igualdad.
    header = (
        "Title: Synthetic Repeated Points\n"
        "Date: Wed Sep 16 2026\n"
        "Plotname: Transient Analysis\n"
        "Flags: real forward stepped\n"
        "No. Variables: 2\n"
        "No. Points: 10\n"
        "Variables:\n"
        "\t0\ttime\ttime\n"
        "\t1\tV(out)\tvoltage\n"
    )
    h_bytes = header.encode('utf-16-le') + b'B\x00i\x00n\x00a\x00r\x00y\x00:\x00\n\x00'
    
    body = bytearray()
    # Step 1 (5 puntos): t = 0.0, 1.0, 1.0 (repetido), 2.0, 3.0
    for t, v in [(0.0, 10.0), (1.0, 11.0), (1.0, 11.5), (2.0, 12.0), (3.0, 13.0)]:
        body.extend(struct.pack('<d', t))
        body.extend(struct.pack('<f', v))
    # Step 2 (5 puntos): t = 0.0 (reinicio), 1.0, 1.0 (repetido), 2.0, 3.0
    for t, v in [(0.0, 20.0), (1.0, 21.0), (1.0, 21.5), (2.0, 22.0), (3.0, 23.0)]:
        body.extend(struct.pack('<d', t))
        body.extend(struct.pack('<f', v))

    with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.raw') as f:
        f.write(h_bytes + body)
        temp_path = f.name

    try:
        res = read_raw(temp_path)
        assert res['is_stepped'] is True
        assert res['n_steps'] == 2, f"Puntos repetidos causaron fragmentación falsa: n_steps={res['n_steps']}"
        assert res['step_boundaries'] == [(0, 5), (5, 10)]
        assert len(res['steps']) == 2
        assert len(res['steps'][0]['time']) == 5
        assert len(res['steps'][1]['time']) == 5
        # Comprobar que los puntos repetidos existen dentro del step
        assert res['steps'][0]['time'][1] == res['steps'][0]['time'][2] == 1.0
        assert res['steps'][1]['time'][1] == res['steps'][1]['time'][2] == 1.0
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_raw_multivariable_double():
    header = (
        "Title: Multi-Var Double Precision\n"
        "Date: Wed Sep 16 2026\n"
        "Plotname: Transient Analysis\n"
        "Flags: real forward double\n"
        "No. Variables: 4\n"
        "No. Points: 3\n"
        "Variables:\n"
        "\t0\ttime\ttime\n"
        "\t1\tV(1)\tvoltage\n"
        "\t2\tV(2)\tvoltage\n"
        "\t3\tI(Vdd)\tdevice_current\n"
    )
    h_bytes = header.encode('latin1') + b'Binary:\n'
    body = bytearray()
    for p in range(3):
        for v in range(4):
            body.extend(struct.pack('<d', float(p * 10 + v)))

    with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.raw') as f:
        f.write(h_bytes + body)
        temp_path = f.name

    try:
        res = read_raw(temp_path)
        assert res['metadata']['n_vars'] == 4
        assert res['metadata']['n_points'] == 3
        assert abs(res['data']['I(Vdd)'][2] - 23.0) < 1e-9
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_raw_truncated_strict():
    header = (
        "Title: Truncated Test\n"
        "Flags: real forward\n"
        "No. Variables: 2\n"
        "No. Points: 10\n"
        "Variables:\n"
        "\t0\ttime\ttime\n"
        "\t1\tV(1)\tvoltage\n"
    )
    h_bytes = header.encode('latin1') + b'Binary:\n'
    # Solo 2 puntos escritos (24 bytes) en lugar de 10 puntos (120 bytes)
    body = struct.pack('<dfdf', 0.0, 1.0, 1.0, 2.0)

    with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.raw') as f:
        f.write(h_bytes + body)
        temp_path = f.name

    try:
        raised = False
        try:
            read_raw(temp_path)
        except ValueError as e:
            if "truncado" in str(e).lower():
                raised = True
        assert raised, "read_raw debió levantar ValueError indicando truncamiento"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def test_raw_complex_unsupported():
    # Si Flags contiene 'complex forward' (AC sweep), el parser debe rechazarlo explícitamente
    header = (
        "Title: AC Sweep Complex Test\n"
        "Flags: complex forward\n"
        "No. Variables: 2\n"
        "No. Points: 2\n"
        "Variables:\n"
        "\t0\tfrequency\tfrequency\n"
        "\t1\tV(out)\tvoltage\n"
    )
    h_bytes = header.encode('latin1') + b'Binary:\n'
    body = bytearray(64) # Dummy data

    with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.raw') as f:
        f.write(h_bytes + body)
        temp_path = f.name

    try:
        raised = False
        try:
            read_raw(temp_path)
        except NotImplementedError as e:
            if "complejos" in str(e).lower():
                raised = True
        assert raised, "read_raw debió levantar NotImplementedError ante formato complejo"
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def main():
    print("=================================================================")
    print("EJECUTANDO BATERÍA INTEGRAL DE PRUEBAS DE REGRESIÓN (FASE 2.1)")
    print("=================================================================")
    tests = [
        ("1. Log Normal (Escalares estándar)", test_log_normal),
        ("2. Log con Barrido (.step y tablas)", test_log_step),
        ("3. Log con Medición FAIL'ed", test_log_failed_metric),
        ("4. Log con Valor NaN", test_log_nan),
        ("5. Log con Valor +INF y 1.#INF", test_log_pos_inf),
        ("6. Log con Valor -INF", test_log_neg_inf),
        ("7. Log con Métrica Requerida Ausente", test_log_missing_metric),
        ("8. Log con Medición WHEN y timestamp 'AT'", test_log_meas_when),
        ("9. RAW Real sin Step (UTF-16 y Delimitador)", test_raw_unstepped_real),
        ("10. RAW Real Stepped Transient (Caso A: 3 steps, t_reset=0)", test_raw_stepped_transient_real),
        ("11. RAW Real Stepped DC Ascendente (Caso B: 3 steps, 0 -> 1V)", test_raw_stepped_dc_ascending_real),
        ("12. RAW Real Stepped DC Descendente (Caso C: 3 steps, 1 -> 0V)", test_raw_stepped_dc_descending_real),
        ("13. RAW Puntos Repetidos en Mismo Step (No división espuria)", test_raw_repeated_points_no_split),
        ("14. RAW Multivariable Doble Precisión", test_raw_multivariable_double),
        ("15. RAW Truncado (Detección Estricta de bytes)", test_raw_truncated_strict),
        ("16. RAW Complejo No Soportado (Rechazo explícito AC/Noise)", test_raw_complex_unsupported),
    ]
    
    passed_count = 0
    for name, func in tests:
        if run_test(name, func):
            passed_count += 1
            
    print("=================================================================")
    print(f"RESUMEN: {passed_count}/{len(tests)} pruebas pasadas con éxito.")
    print("=================================================================")
    
    if passed_count != len(tests):
        sys.exit(1)

if __name__ == '__main__':
    main()
