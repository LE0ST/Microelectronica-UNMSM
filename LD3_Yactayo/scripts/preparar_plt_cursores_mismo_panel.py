import os

plt_n_cur = """[Transient Analysis]
{
   Npanes: 1
   {
      traces: 2 {524290,0,"V(vg)-V(ve)"} {524291,0,"I(R2)"}
      X: (' ',1,1.98e-005,2.025e-005,5e-008)
      Y[0]: (' ',1,-2,18,2)
      Y[1]: ('_',1,-2,22,2)
      Volts: (' ',0,0,1,0,-2,18)
      Amps: ('_',0,0,1,0,-2,22)
      Log: 0 0 0
   }
}
"""

plt_p_cur = """[Transient Analysis]
{
   Npanes: 1
   {
      traces: 2 {524290,0,"V(vg)-V(ve)"} {524291,0,"-I(R2)"}
      X: (' ',1,2.50e-005,2.565e-005,5e-008)
      Y[0]: (' ',1,-18,2,2)
      Y[1]: ('_',1,-5,45,5)
      Volts: (' ',0,0,1,0,-18,2)
      Amps: ('_',0,0,1,0,-5,45)
      Log: 0 0 0
   }
}
"""

targets = [
    ('LD3_Yactayo/esquemas/DPT_NIGBT_cursores.plt', plt_n_cur),
    ('LD3_Yactayo/simulaciones/netlists/dpt_nigbt_cursores.plt', plt_n_cur),
    ('LD3_Yactayo/esquemas/DPT_PIGBT_cursores.plt', plt_p_cur),
    ('LD3_Yactayo/simulaciones/netlists/dpt_pigbt_cursores.plt', plt_p_cur)
]

for p, content in targets:
    with open(p, 'wb') as f:
        f.write(content.encode('utf-16-le'))
    print(f'Generado exitosamente: {p}')
