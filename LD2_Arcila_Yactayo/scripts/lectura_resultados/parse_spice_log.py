# -*- coding: utf-8 -*-
"""
Parser universal y dinámico de archivos .log de LTspice.
Extrae de manera estructurada y segura:
- Mediciones escalares directas (.meas)
- Tablas de mediciones con barridos (.step)
- Parámetros de cada paso de barrido
- Detección explícita de mediciones fallidas (FAIL'ed)
- Detección explícita de valores no finitos (NaN, +INF, -INF, 1.#QNAN, 1.#INF)
- Validación estricta de métricas requeridas (sin fallos silenciosos)
- Advertencias numéricas y de convergencia
"""

import os
import sys
import re
import math
import json

class SpiceMeasurementError(Exception):
    """Excepción levantada cuando una medición SPICE requerida falla, falta o resulta no finita (NaN/Inf)."""
    pass

def parse_log(log_path, required_metrics=None, raise_on_error=False):
    """
    Parsea un archivo .log de LTspice y retorna un diccionario estructurado:
    {
        'measurements': { name: float_or_str_or_list },
        'steps': [ { param_name: val, ... }, ... ],
        'failed_measurements': [ name, ... ],
        'invalid_measurements': { name: reason },
        'missing_metrics': [ name, ... ],
        'warnings': [ str, ... ],
        'operating_point': {},
        'elapsed_time': float or None,
        'is_valid': bool,
        'error_message': str or None
    }
    
    Parámetros:
    - log_path: Ruta absoluta o relativa al archivo .log.
    - required_metrics: Lista opcional de nombres de métricas requeridas (case-insensitive).
    - raise_on_error: Si True, levanta SpiceMeasurementError en caso de fallo, ausencia o NaN/Inf.
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Archivo .log no encontrado: {log_path}")

    # Intentar decodificar en varios formatos comunes
    raw_bytes = open(log_path, 'rb').read()
    text = ""
    for enc in ['utf-8', 'utf-16-le', 'latin1', 'cp1252']:
        try:
            text = raw_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue

    lines = text.splitlines()

    result = {
        'measurements': {},
        'steps': [],
        'failed_measurements': [],
        'invalid_measurements': {},
        'missing_metrics': [],
        'warnings': [],
        'operating_point': {},
        'elapsed_time': None,
        'is_valid': True,
        'error_message': None
    }

    # 1. Parsear .step lines
    step_param_re = re.compile(r'^\.step\s+([a-zA-Z0-9_]+)=([^\s]+)', re.IGNORECASE)
    for line in lines:
        m = step_param_re.match(line.strip())
        if m:
            pname = m.group(1).lower()
            try:
                pval = float(m.group(2))
            except ValueError:
                pval = m.group(2)
            result['steps'].append({pname: pval})

    # 2. Detectar advertencias y tiempo transcurrido
    for line in lines:
        l_s = line.strip()
        if 'warning' in l_s.lower():
            result['warnings'].append(l_s)
        elif 'time step too small' in l_s.lower():
            result['warnings'].append(l_s)
        elif 'singular matrix' in l_s.lower():
            result['warnings'].append(l_s)
        elif l_s.startswith('Total elapsed time:'):
            m_time = re.search(r'Total elapsed time:\s*([\d\.]+)\s*seconds', l_s)
            if m_time:
                result['elapsed_time'] = float(m_time.group(1))

    # 3. Parsear mediciones explícitamente fallidas (FAIL'ed)
    fail_re = re.compile(r'Measurement\s+["\']?([^"\']+)["\']?\s+FAIL', re.IGNORECASE)
    for line in lines:
        m = fail_re.search(line)
        if m:
            m_name = m.group(1).lower()
            if m_name not in result['failed_measurements']:
                result['failed_measurements'].append(m_name)
            result['invalid_measurements'][m_name] = "FAIL'ed"
            result['measurements'][m_name] = None

    # 4. Parsear mediciones tabulares y escalares
    in_table = False
    current_table_name = None
    table_headers = []

    # Regex para mediciones WHEN de LTspice: formato '<name>: <condition>  AT <result>'
    # En LTspice, las mediciones '.meas ... WHEN ...' generan 'AT' en mayúsculas separando la condición del valor temporal o de barrido resultante.
    meas_when_re = re.compile(
        r'^([a-zA-Z0-9_\.]+):\s*.*?\s+AT\s+([+-]?(?:1\.#[a-zA-Z]+|nan|inf|[\d\.]+(?:[eE][+-]?\d+)?))\s*$'
    )

    # Regex robusta para mediciones escalares: soporta 'name: val', 'name: expr = val' y 'name=val' (TRIG/TARG)
    # Priorizar variantes de Windows/SPICE (1.#INF, NaN) antes de dígitos
    meas_scalar_re = re.compile(
        r'^([a-zA-Z0-9_\.]+)(?::\s*|\s*=\s*|\s*=)(?:.*=)?\s*([+-]?(?:1\.#[a-zA-Z]+|nan|inf|[\d\.]+(?:[eE][+-]?\d+)?))',
        re.IGNORECASE
    )
    HEADER_IGNORE = {'tnom', 'temp', 'gmin', 'abstol', 'reltol', 'chgtol', 'vntol', 'solver', 'method'}

    for idx, line in enumerate(lines):
        l_s = line.strip()
        if not l_s:
            in_table = False
            continue

        if l_s.startswith('Measurement:'):
            m_name = l_s[12:].strip().lower()
            current_table_name = m_name
            in_table = True
            table_headers = []
            result['measurements'][current_table_name] = []
            continue

        if in_table:
            parts = l_s.split()
            if not table_headers:
                table_headers = [p.lower() for p in parts]
            else:
                if parts[0].isdigit():
                    try:
                        step_num = int(parts[0])
                        val_str = parts[1].lower()
                        
                        if 'fail' in val_str:
                            val = None
                            result['invalid_measurements'][f"{current_table_name}[step {step_num}]"] = "FAIL'ed"
                        elif 'nan' in val_str or 'ind' in val_str:
                            val = float('nan')
                            result['invalid_measurements'][f"{current_table_name}[step {step_num}]"] = "NaN"
                        elif '+inf' in val_str or val_str == 'inf':
                            val = float('inf')
                            result['invalid_measurements'][f"{current_table_name}[step {step_num}]"] = "+INF"
                        elif '-inf' in val_str:
                            val = float('-inf')
                            result['invalid_measurements'][f"{current_table_name}[step {step_num}]"] = "-INF"
                        else:
                            val = float(parts[1])
                            
                        result['measurements'][current_table_name].append({
                            'step': step_num,
                            'val': val
                        })
                    except (ValueError, IndexError):
                        pass
        else:
            if (l_s.startswith('.') or l_s.startswith('Direct Newton') or 
                l_s.startswith('Circuit:') or l_s.startswith('Start Time:') or 
                l_s.startswith('Total elapsed') or l_s.startswith('Files loaded:') or
                l_s.lower().startswith('options:') or l_s.lower().startswith('gmin =') or
                l_s.lower().startswith('abstol =') or l_s.lower().startswith('reltol =') or
                l_s.lower().startswith('method =') or l_s.lower().startswith('solver =')):
                continue

            # Intentar primero formato WHEN (prioridad para timestamps tras ' AT ')
            m_when = meas_when_re.match(l_s)
            if m_when:
                m_name = m_when.group(1).lower()
                if m_name in HEADER_IGNORE:
                    continue
                val_raw = m_when.group(2).lower()
            else:
                m = meas_scalar_re.match(l_s)
                if not m:
                    continue
                m_name = m.group(1).lower()
                if m_name in HEADER_IGNORE:
                    continue
                val_raw = m.group(2).lower()

            if m_name in result['failed_measurements']:
                continue

            if 'nan' in val_raw or 'ind' in val_raw:
                result['measurements'][m_name] = float('nan')
                result['invalid_measurements'][m_name] = "NaN"
            elif '+inf' in val_raw or val_raw == 'inf' or '+1.#inf' in val_raw or '1.#inf' in val_raw:
                result['measurements'][m_name] = float('inf')
                result['invalid_measurements'][m_name] = "+INF"
            elif '-inf' in val_raw or '-1.#inf' in val_raw:
                result['measurements'][m_name] = float('-inf')
                result['invalid_measurements'][m_name] = "-INF"
            else:
                try:
                    m_val = float(val_raw)
                    result['measurements'][m_name] = m_val
                except ValueError:
                    result['invalid_measurements'][m_name] = f"Formato no numérico: '{val_raw}'"
                    result['measurements'][m_name] = None

    # 5. Validación de métricas requeridas o integridad general
    errors = []
    if required_metrics is not None:
        for req in required_metrics:
            req_l = req.lower()
            if req_l not in result['measurements']:
                result['missing_metrics'].append(req_l)
                errors.append(f"Métrica requerida ausente: '{req}'")
            elif req_l in result['failed_measurements']:
                errors.append(f"Métrica requerida falló (FAIL'ed): '{req}'")
            elif req_l in result['invalid_measurements']:
                reason = result['invalid_measurements'][req_l]
                errors.append(f"Métrica requerida no finita ({reason}): '{req}'")
            else:
                val = result['measurements'][req_l]
                if val is None:
                    errors.append(f"Métrica requerida es None: '{req}'")
                elif isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
                    errors.append(f"Métrica requerida es no finita ({val}): '{req}'")
    else:
        if result['failed_measurements']:
            errors.append(f"Mediciones fallidas: {result['failed_measurements']}")
        if result['invalid_measurements']:
            errors.append(f"Mediciones no finitas o anómalas: {result['invalid_measurements']}")

    if errors:
        result['is_valid'] = False
        result['error_message'] = "; ".join(errors)
        if raise_on_error:
            raise SpiceMeasurementError(result['error_message'])
    else:
        result['is_valid'] = True
        result['error_message'] = None

    return result

def get_metric(parsed_result, metric_name, strict=True):
    """
    Obtiene el valor numérico de una métrica de forma segura.
    Si strict=True, levanta SpiceMeasurementError si la métrica no existe, falló, o es NaN/Inf.
    """
    m_name = metric_name.lower()
    measurements = parsed_result.get('measurements', {})
    
    if m_name not in measurements:
        if strict:
            raise SpiceMeasurementError(f"Métrica '{metric_name}' no existe en los resultados de simulación.")
        return None
        
    val = measurements[m_name]
    
    if val is None:
        if strict:
            reason = parsed_result.get('invalid_measurements', {}).get(m_name, "Valor es None o FAIL'ed")
            raise SpiceMeasurementError(f"Métrica '{metric_name}' inválida: {reason}")
        return None
        
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        if strict:
            reason = parsed_result.get('invalid_measurements', {}).get(m_name, f"Valor no finito: {val}")
            raise SpiceMeasurementError(f"Métrica '{metric_name}' no es un número finito: {reason}")
        return val

    return val

if __name__ == '__main__':
    if len(sys.argv) > 1:
        res = parse_log(sys.argv[1])
        print(f"Archivo: {sys.argv[1]}")
        print(f"Estado de validez: {'VÁLIDO' if res['is_valid'] else 'INVÁLIDO'}")
        if not res['is_valid']:
            print(f"Errores: {res['error_message']}")
        print("Mediciones encontradas:")
        for k, v in res['measurements'].items():
            print(f"  {k} = {v}")
        if res['failed_measurements']:
            print(f"Mediciones FAIL: {res['failed_measurements']}")
        if res['invalid_measurements']:
            print(f"Mediciones anómalas: {res['invalid_measurements']}")
        if res['warnings']:
            print(f"Advertencias ({len(res['warnings'])}): {res['warnings'][:3]}")
    else:
        print("Uso: python parse_spice_log.py <archivo.log>")
