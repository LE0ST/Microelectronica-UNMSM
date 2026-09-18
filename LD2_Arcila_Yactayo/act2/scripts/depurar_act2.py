import sys
import os
import numpy as np

sys.path.append('LD2_Arcila_Yactayo/scripts/lectura_resultados')
from parse_spice_raw import read_raw

def inspect(name):
    raw_path = f'LD2_Arcila_Yactayo/act2/circuitos/{name}.raw'
    if not os.path.exists(raw_path):
        print(f"File not found: {raw_path}")
        return
    d = read_raw(raw_path)
    s = d['data']
    t = s['time']
    print(f"==================================================")
    print(f"INSPECTING: {name}")
    print(f"Time span: {t[0]*1e9:.2f} ns to {t[-1]*1e9:.2f} ns, total points: {len(t)}")
    print(f"{'t (ns)':>7} | {'clk':>6} | {'c':>6} | {'dyn':>6} | {'n1':>6} | {'n2':>6} | {'n3':>6} | {'out':>6}")
    print("-" * 65)
    t_targets = np.arange(0.0, 6.01, 0.25) * 1e-9
    for tt in t_targets:
        if tt > t[-1]:
            break
        idx = np.argmin(np.abs(t - tt))
        print(f"{t[idx]*1e9:7.2f} | {s['V(clk)'][idx]:6.3f} | {s['V(c)'][idx]:6.3f} | {s['V(dyn)'][idx]:6.3f} | {s['V(n1)'][idx]:6.3f} | {s['V(n2)'][idx]:6.3f} | {s['V(n3)'][idx]:6.3f} | {s['V(out)'][idx]:6.3f}")

if __name__ == '__main__':
    inspect('test_lit')
