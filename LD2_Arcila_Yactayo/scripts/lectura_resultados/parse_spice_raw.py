# -*- coding: utf-8 -*-
"""
Parser de archivos .raw de LTspice para análisis Transient y DC (datos reales).

Alcance verificado y delimitado:
- Soportado: Transient (real forward) y DC (real forward/linear), con y sin barridos (.step).
- Modos de datos: Binary y Values (ASCII).
- Codificación de cabecera: UTF-16-LE (LTspice 17.1+/26.0+) y ASCII/latin1.
- Segmentación robusta de .step dependiente de la dirección del barrido (ascendente/descendente).
- Puntos repetidos tratados como parte del mismo paso (sin fragmentación espuria).
- Control estricto de conservación de puntos (sum(steps) == No. Points).
- Detección de archivos truncados o dañados con excepción explícita.

FUERA DE ALCANCE / NO SOPORTADO:
- Barridos en frecuencia AC (complex forward, 16 bytes por punto).
- Análisis de ruido (Noise) y funciones de transferencia complejas.
"""

import os
import sys
import struct
import numpy as np

def read_raw(file_path):
    """
    Lee un archivo .raw de LTspice y devuelve un diccionario estructurado:
    {
        'metadata': meta,
        'data': { 'name': np.ndarray (todos los puntos contiguos) },
        'is_stepped': bool,
        'n_steps': int,
        'step_boundaries': [(start_idx, end_idx), ...],
        'steps': [ { 'name': np.ndarray (por cada step) }, ... ]
    }
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo RAW no encontrado: {file_path}")

    with open(file_path, 'rb') as f:
        content = f.read()

    if len(content) == 0:
        raise ValueError(f"Archivo RAW vacío: {file_path}")

    # 1. Detectar si el encabezado es UTF-16-LE o ASCII
    is_utf16 = False
    if len(content) > 2 and content[1] == 0:
        is_utf16 = True

    header_text = ""
    data_start = 0
    data_mode = 'binary'

    if is_utf16:
        # Buscar el separador de fin de encabezado (soporta \n y \r\n en UTF-16-LE)
        markers_bin = [b'B\x00i\x00n\x00a\x00r\x00y\x00:\x00\r\x00\n\x00', b'B\x00i\x00n\x00a\x00r\x00y\x00:\x00\n\x00']
        markers_val = [b'V\x00a\x00l\x00u\x00e\x00s\x00:\x00\r\x00\n\x00', b'V\x00a\x00l\x00u\x00e\x00s\x00:\x00\n\x00']
        
        found = False
        for mb in markers_bin:
            idx = content.find(mb)
            if idx != -1:
                header_text = content[:idx].decode('utf-16-le', errors='ignore')
                data_mode = 'binary'
                data_start = idx + len(mb)
                found = True
                break
                
        if not found:
            for mv in markers_val:
                idx = content.find(mv)
                if idx != -1:
                    header_text = content[:idx].decode('utf-16-le', errors='ignore')
                    data_mode = 'ascii'
                    data_start = idx + len(mv)
                    found = True
                    break
                    
        if not found:
            raise ValueError("No se encontró el delimitador de datos (Binary: o Values:) en encabezado UTF-16.")
    else:
        markers_bin = [b'Binary:\r\n', b'Binary:\n']
        markers_val = [b'Values:\r\n', b'Values:\n']
        
        found = False
        for mb in markers_bin:
            idx = content.find(mb)
            if idx != -1:
                header_text = content[:idx].decode('latin1', errors='ignore')
                data_mode = 'binary'
                data_start = idx + len(mb)
                found = True
                break
                
        if not found:
            for mv in markers_val:
                idx = content.find(mv)
                if idx != -1:
                    header_text = content[:idx].decode('latin1', errors='ignore')
                    data_mode = 'ascii'
                    data_start = idx + len(mv)
                    found = True
                    break
                    
        if not found:
            raise ValueError("No se encontró el delimitador de datos (Binary: o Values:) en encabezado ASCII.")

    # 2. Parsear metadatos del encabezado
    lines = header_text.splitlines()
    meta = {
        'title': '',
        'date': '',
        'plotname': '',
        'flags': '',
        'n_vars': 0,
        'n_points': 0,
        'variables': []
    }

    in_vars = False
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        if line_s.startswith('Title:'):
            meta['title'] = line_s[6:].strip()
        elif line_s.startswith('Date:'):
            meta['date'] = line_s[5:].strip()
        elif line_s.startswith('Plotname:'):
            meta['plotname'] = line_s[9:].strip()
        elif line_s.startswith('Flags:'):
            meta['flags'] = line_s[6:].strip()
        elif line_s.startswith('No. Variables:'):
            meta['n_vars'] = int(line_s[14:].strip())
        elif line_s.startswith('No. Points:'):
            meta['n_points'] = int(line_s[11:].strip())
        elif line_s.startswith('Variables:'):
            in_vars = True
        elif in_vars:
            parts = line_s.split()
            if len(parts) >= 3:
                v_idx = int(parts[0])
                v_name = parts[1]
                v_type = parts[2]
                meta['variables'].append((v_idx, v_name, v_type))
            elif line_s.startswith('Binary:') or line_s.startswith('Values:'):
                in_vars = False

    # Verificar compatibilidad: no soportar datos complejos (AC/Noise)
    flags_lower = meta['flags'].lower()
    if 'complex' in flags_lower:
        raise NotImplementedError(
            "El formato RAW contiene datos complejos ('complex forward', AC/Noise), "
            "los cuales no están soportados por este parser de análisis real (Transient/DC)."
        )

    n_vars = meta['n_vars']
    n_points = meta['n_points']

    # 3. Leer datos
    data_dict = {}
    step_names = [v[1] for v in meta['variables']]
    for v_name in step_names:
        data_dict[v_name] = np.zeros(n_points)

    if data_mode == 'binary':
        is_double = 'double' in flags_lower
        point_bytes = 8 + (n_vars - 1) * (8 if is_double else 4)

        expected_bytes = point_bytes * n_points
        available_bytes = len(content) - data_start
        if available_bytes < expected_bytes:
            raise ValueError(
                f"Archivo RAW truncado: se esperaban {expected_bytes} bytes para {n_points} puntos, "
                f"pero solo hay {available_bytes} bytes disponibles en el archivo."
            )

        raw_body = content[data_start:data_start + expected_bytes]

        offset = 0
        fmt_rest = f"{n_vars - 1}d" if is_double else f"{n_vars - 1}f"

        for p in range(n_points):
            v0 = struct.unpack_from('<d', raw_body, offset)[0]
            data_dict[step_names[0]][p] = v0
            offset += 8

            if n_vars > 1:
                vals = struct.unpack_from('<' + fmt_rest, raw_body, offset)
                for i, val in enumerate(vals):
                    data_dict[step_names[i + 1]][p] = val
                offset += (n_vars - 1) * (8 if is_double else 4)

    elif data_mode == 'ascii':
        lines_data = content[data_start:].decode('latin1', errors='ignore').splitlines()
        p = 0
        v_idx = 0
        for l in lines_data:
            l_s = l.strip()
            if not l_s:
                continue
            parts = l_s.split()
            if len(parts) == 2 and parts[0].isdigit():
                p = int(parts[0])
                if p >= n_points:
                    break
                val = float(parts[1])
                data_dict[step_names[0]][p] = val
                v_idx = 1
            elif len(parts) == 1 and v_idx < n_vars:
                if p < n_points:
                    val = float(parts[0])
                    data_dict[step_names[v_idx]][p] = val
                    v_idx += 1

    # 4. Segmentación robusta de barridos (.step)
    is_stepped = 'stepped' in flags_lower
    step_boundaries = []
    steps_data = []

    if n_points > 0 and len(step_names) > 0:
        v0 = data_dict[step_names[0]]

        if is_stepped and n_points > 1:
            # 4.1 Determinar dirección dominante del barrido inicial
            direction = 0  # +1: ascendente, -1: descendente
            for k in range(1, n_points):
                if v0[k] > v0[0]:
                    direction = 1
                    break
                elif v0[k] < v0[0]:
                    direction = -1
                    break

            resets = [0]
            if direction == 1:
                # Barrido predominantemente ascendente (ej. .tran o .dc ascendente 0 -> VDD):
                # Una nueva corrida (.step) comienza ÚNICAMENTE cuando la variable se reinicia hacia atrás
                # (v0[i] < v0[i-1]). Puntos consecutivos iguales (v0[i] == v0[i-1]) pertenecen al mismo step.
                for i in range(1, n_points):
                    if v0[i] < v0[i - 1]:
                        resets.append(i)
            elif direction == -1:
                # Barrido predominantemente descendente (ej. .dc descendente VDD -> 0):
                # Una nueva corrida (.step) comienza ÚNICAMENTE cuando la variable salta hacia arriba
                # al reiniciar hacia el valor inicial superior (v0[i] > v0[i-1]).
                for i in range(1, n_points):
                    if v0[i] > v0[i - 1]:
                        resets.append(i)
            else:
                # Variable plana: caso ambiguo. No inventar fronteras.
                resets = [0]

            resets.append(n_points)

            n_steps = len(resets) - 1
            for s in range(n_steps):
                s_start = resets[s]
                s_end = resets[s + 1]
                step_boundaries.append((s_start, s_end))
                s_dict = { v_name: data_dict[v_name][s_start:s_end] for v_name in step_names }
                steps_data.append(s_dict)
        else:
            n_steps = 1
            step_boundaries = [(0, n_points)]
            steps_data = [data_dict]
    else:
        n_steps = 1 if n_points > 0 else 0
        step_boundaries = [(0, n_points)]
        steps_data = [data_dict]

    # Invariante estricto de conservación de puntos
    if steps_data and step_names:
        total_step_points = sum(len(step[step_names[0]]) for step in steps_data)
        if total_step_points != n_points:
            raise ValueError(
                f"Fallo de integridad en segmentación: la suma de puntos de los steps ({total_step_points}) "
                f"no coincide con No. Points del archivo RAW ({n_points})."
            )

    return {
        'metadata': meta,
        'data': data_dict,
        'is_stepped': is_stepped,
        'n_steps': n_steps,
        'step_boundaries': step_boundaries,
        'steps': steps_data
    }

if __name__ == '__main__':
    if len(sys.argv) > 1:
        res = read_raw(sys.argv[1])
        print(f"Archivo: {sys.argv[1]}")
        print(f"Título: {res['metadata']['title']}")
        print(f"Variables ({res['metadata']['n_vars']}): {[v[1] for v in res['metadata']['variables']]}")
        print(f"Puntos totales: {res['metadata']['n_points']}")
        print(f"Es barrido (.step): {res['is_stepped']}")
        if res['is_stepped']:
            print(f"Cantidad de pasos detectados: {res['n_steps']}")
            print(f"Límites de pasos: {res['step_boundaries']}")
    else:
        print("Uso: python parse_spice_raw.py <archivo.raw>")
