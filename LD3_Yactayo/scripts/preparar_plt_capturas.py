import os

plt_n = """[Transient Analysis]
{
   Npanes: 3
   {
      traces: 1 {524290,0,"V(vg)-V(ve)"}
      X: (' ',1,0,3e-005,5e-006)
      Y[0]: (' ',1,-2,20,5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-2,20)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"V(vc)-V(ve)"}
      X: (' ',1,0,3e-005,5e-006)
      Y[0]: (' ',1,-20,450,50)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-20,450)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"I(R2)"}
      X: (' ',1,0,3e-005,5e-006)
      Y[0]: (' ',1,-2,25,5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Amps: (' ',0,0,1,0,-2,25)
      Log: 0 0 0
   }
}
"""

# PLT para zoom de apagado en N-IGBT (19.8us a 20.4us)
plt_n_zoom = """[Transient Analysis]
{
   Npanes: 3
   {
      traces: 1 {524290,0,"V(vg)-V(ve)"}
      X: (' ',1,1.98e-005,2.04e-005,1e-007)
      Y[0]: (' ',1,-2,20,5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-2,20)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"V(vc)-V(ve)"}
      X: (' ',1,1.98e-005,2.04e-005,1e-007)
      Y[0]: (' ',1,-20,450,50)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-20,450)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"I(R2)"}
      X: (' ',1,1.98e-005,2.04e-005,1e-007)
      Y[0]: (' ',1,-2,25,5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Amps: (' ',0,0,1,0,-2,25)
      Log: 0 0 0
   }
}
"""

plt_p = """[Transient Analysis]
{
   Npanes: 3
   {
      traces: 1 {524290,0,"V(vg)-V(ve)"}
      X: (' ',1,0,3.5e-005,5e-006)
      Y[0]: (' ',1,-20,2,5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-20,2)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"V(ve)-V(vc)"}
      X: (' ',1,0,3.5e-005,5e-006)
      Y[0]: (' ',1,-20,450,50)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-20,450)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"-I(R2)"}
      X: (' ',1,0,3.5e-005,5e-006)
      Y[0]: (' ',1,-5,50,10)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Amps: (' ',0,0,1,0,-5,50)
      Log: 0 0 0
   }
}
"""

# PLT para zoom de apagado en P-IGBT (25.0us a 25.8us)
plt_p_zoom = """[Transient Analysis]
{
   Npanes: 3
   {
      traces: 1 {524290,0,"V(vg)-V(ve)"}
      X: (' ',1,2.5e-005,2.58e-005,1e-007)
      Y[0]: (' ',1,-20,2,5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-20,2)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"V(ve)-V(vc)"}
      X: (' ',1,2.5e-005,2.58e-005,1e-007)
      Y[0]: (' ',1,-20,450,50)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,0,-20,450)
      Log: 0 0 0
   }
   {
      traces: 1 {524290,0,"-I(R2)"}
      X: (' ',1,2.5e-005,2.58e-005,1e-007)
      Y[0]: (' ',1,-5,50,10)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Amps: (' ',0,0,1,0,-5,50)
      Log: 0 0 0
   }
}
"""

# Escribir archivos .plt
n_targets = [
    'LD3_Yactayo/esquemas/DPT_NIGBT_nom.plt',
    'LD3_Yactayo/simulaciones/netlists/dpt_nigbt_nom.plt'
]
for p in n_targets:
    with open(p, 'wb') as f:
        f.write(plt_n.encode('utf-16-le'))
    print(f'Archivo escrito: {p}')

p_targets = [
    'LD3_Yactayo/esquemas/DPT_PIGBT_nom.plt',
    'LD3_Yactayo/simulaciones/netlists/dpt_pigbt_nom.plt'
]
for p in p_targets:
    with open(p, 'wb') as f:
        f.write(plt_p.encode('utf-16-le'))
    print(f'Archivo escrito: {p}')

# Guardar versiones de zoom dedicadas por si se requieren cargar directamente
with open('LD3_Yactayo/esquemas/DPT_NIGBT_zoom.plt', 'wb') as f:
    f.write(plt_n_zoom.encode('utf-16-le'))
with open('LD3_Yactayo/esquemas/DPT_PIGBT_zoom.plt', 'wb') as f:
    f.write(plt_p_zoom.encode('utf-16-le'))
print('Archivos de zoom guardados.')
