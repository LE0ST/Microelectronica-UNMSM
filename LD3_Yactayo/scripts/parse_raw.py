import numpy as np

def parse_ltspice_ascii_raw(raw_path):
    with open(raw_path, 'r', errors='ignore') as f:
        lines = f.readlines()
    
    # Parse header
    num_vars = 0
    num_points = 0
    var_names = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('No. Variables:'):
            num_vars = int(line.split(':')[1].strip())
        elif line.startswith('No. Points:'):
            num_points = int(line.split(':')[1].strip())
        elif line.startswith('Variables:'):
            i += 1
            for v in range(num_vars):
                parts = lines[i].strip().split()
                # parts[0] is index, parts[1] is name, parts[2] is type
                var_names.append(parts[1])
                i += 1
            continue
        elif line.startswith('Values:'):
            i += 1
            break
        i += 1
    
    # Pre-allocate array
    data = np.zeros((num_points, num_vars))
    p = 0
    while i < len(lines) and p < num_points:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        # First variable (time) might have index prefixed
        parts = line.split()
        if len(parts) == 2:
            data[p, 0] = float(parts[1])
        else:
            data[p, 0] = float(parts[0])
        i += 1
        for v in range(1, num_vars):
            data[p, v] = float(lines[i].strip())
            i += 1
        p += 1
    
    result = {name: data[:, idx] for idx, name in enumerate(var_names)}
    return result

if __name__ == '__main__':
    data = parse_ltspice_ascii_raw('LD3_Yactayo/simulaciones/netlists/dpt_nigbt_nom.raw')
    print('Variables parsed:', list(data.keys()))
    t = data['time']
    ic = data['I(R2)']
    print(f'Time span: {t[0]*1e6:.2f} us to {t[-1]*1e6:.2f} us, total points: {len(t)}')
    print(f'Ic max: {np.max(ic):.4f} A')
