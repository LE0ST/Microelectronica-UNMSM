# -*- coding: utf-8 -*-
"""
analizar_terminales.py
Auditoria profunda de terminales y corrientes del nodo dyn para Actividad 3.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "lectura_resultados"))
from parse_spice_log import parse_log

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CIRCUITOS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "circuitos")

log_a = os.path.join(CIRCUITOS_DIR, "aux_diagnostico_sin_keeper.log")
log_b = os.path.join(CIRCUITOS_DIR, "aux_diagnostico_con_keeper.log")

res_a = parse_log(log_a)['measurements']
res_b = parse_log(log_b)['measurements']

print("==================================================================")
print("AUDITORIA DE TERMINALES: PILOTO A (SIN KEEPER)")
print("==================================================================")
for t in ['10n', '100n', '500n', '900n']:
    vdyn = res_a.get(f"vdyn_{t}")
    is_m1 = res_a.get(f"is_m1_{t}")
    id_m1 = res_a.get(f"id_m1_{t}")
    ig_m1 = res_a.get(f"ig_m1_{t}")
    ib_m1 = res_a.get(f"ib_m1_{t}")
    id_mp = res_a.get(f"id_mp_{t}")
    is_mp = res_a.get(f"is_mp_{t}")
    ig_mni = res_a.get(f"ig_mni_{t}")
    ig_mpi = res_a.get(f"ig_mpi_{t}")
    i_cl = res_a.get(f"i_cl_{t}")
    i_vdd = res_a.get(f"i_vdd_{t}")
    
    # Convencion: Corriente POSITIVA = corriente que SALE del nodo dyn
    # Terminales conectados a dyn:
    # 1. M1: terminal Source -> corriente que sale de dyn entra a Source de M1: I_saliente_M1 = Is(M1)
    # 2. Mp: terminal Drain -> corriente que sale de dyn entra a Drain de Mp: I_saliente_Mp = Id(Mp)
    # 3. Mni: terminal Gate -> corriente que sale de dyn entra a Gate de Mni: I_saliente_Mni = Ig(Mni)
    # 4. Mpi: terminal Gate -> corriente que sale de dyn entra a Gate de Mpi: I_saliente_Mpi = Ig(Mpi)
    # 5. CL: corriente que sale de dyn entra a CL: I_saliente_CL = I(CL)
    i_saliente_m1 = is_m1
    i_saliente_mp = id_mp
    i_saliente_inv = ig_mni + ig_mpi
    i_saliente_cl = i_cl
    i_residual = i_saliente_m1 + i_saliente_mp + i_saliente_inv + i_saliente_cl
    
    print(f"\n--- Instante t = {t} ---")
    print(f"  Tension V(dyn):        {vdyn:.6f} V")
    print(f"  M1 (Source a dyn):     Is(M1) = {is_m1*1e12:+.3f} pA (Id = {id_m1*1e12:+.3f} pA, Ig = {ig_m1*1e12:+.3f} pA, Ib = {ib_m1*1e12:+.3f} pA)")
    print(f"  Mp (Drain a dyn):      Id(Mp) = {id_mp*1e12:+.3f} pA" + (f" (Is = {is_mp*1e12:+.3f} pA)" if is_mp is not None else ""))
    print(f"  Inversor (Gate a dyn): Ig(Mni) = {ig_mni*1e12:+.3f} pA, Ig(Mpi) = {ig_mpi*1e12:+.3f} pA -> Total Inv = {i_saliente_inv*1e12:+.3f} pA")
    print(f"  Capacitor CL (a dyn):  I(CL)  = {i_cl*1e12:+.3f} pA")
    print(f"  I_dispositivos:        {(i_saliente_m1 + i_saliente_mp + i_saliente_inv)*1e12:+.3f} pA")
    print(f"  I_residual (KCL):      {i_residual*1e12:+.3f} pA")
    print(f"  I(Vdd):                {i_vdd*1e12:+.3f} pA (I_supply = {-i_vdd*1e12:+.3f} pA)")

print("\n==================================================================")
print("AUDITORIA DE TERMINALES: PILOTO B (CON KEEPER 45nm)")
print("==================================================================")
for t in ['10n', '100n', '500n', '900n']:
    vdyn = res_b.get(f"vdyn_{t}")
    is_m1 = res_b.get(f"is_m1_{t}")
    id_m1 = res_b.get(f"id_m1_{t}")
    ig_m1 = res_b.get(f"ig_m1_{t}")
    ib_m1 = res_b.get(f"ib_m1_{t}")
    id_mp = res_b.get(f"id_mp_{t}")
    id_mk = res_b.get(f"id_mk_{t}")
    is_mk = res_b.get(f"is_mk_{t}")
    ig_mk = res_b.get(f"ig_mk_{t}")
    ib_mk = res_b.get(f"ib_mk_{t}")
    ig_mni = res_b.get(f"ig_mni_{t}")
    ig_mpi = res_b.get(f"ig_mpi_{t}")
    i_cl = res_b.get(f"i_cl_{t}")
    i_vdd = res_b.get(f"i_vdd_{t}")
    
    # Terminales conectados a dyn:
    # 1. M1: terminal Source -> I_saliente_M1 = Is(M1)
    # 2. Mp: terminal Drain -> I_saliente_Mp = Id(Mp)
    # 3. Mk: terminal Drain -> I_saliente_Mk = Id(Mk) (si entra a dyn, Id(Mk) es negativa)
    #    I_kp_inyectada = -Id(Mk)
    # 4. Inversor: Ig(Mni) + Ig(Mpi)
    # 5. CL: I(CL)
    i_saliente_m1 = is_m1
    i_saliente_mp = id_mp
    i_saliente_mk = id_mk
    i_saliente_inv = ig_mni + ig_mpi
    i_saliente_cl = i_cl
    i_residual = i_saliente_m1 + i_saliente_mp + i_saliente_mk + i_saliente_inv + i_saliente_cl
    
    print(f"\n--- Instante t = {t} ---")
    print(f"  Tension V(dyn):        {vdyn:.6f} V")
    print(f"  M1 (Source a dyn):     Is(M1) = {is_m1*1e12:+.3f} pA (Id = {id_m1*1e12:+.3f} pA, Ig = {ig_m1*1e12:+.3f} pA, Ib = {ib_m1*1e12:+.3f} pA)")
    print(f"  Mp (Drain a dyn):      Id(Mp) = {id_mp*1e12:+.3f} pA")
    print(f"  Mk (Drain a dyn):      Id(Mk) = {id_mk*1e12:+.3f} pA -> I_kp_inyectada = {-id_mk*1e12:+.3f} pA")
    print(f"                         Is(Mk) = {is_mk*1e12:+.3f} pA, Ig(Mk) = {ig_mk*1e12:+.3f} pA, Ib(Mk) = {ib_mk*1e12:+.3f} pA")
    print(f"                         Check Mk: Is + Id + Ig + Ib = {(is_mk + id_mk + ig_mk + ib_mk)*1e12:+.3f} pA")
    print(f"  Inversor (Gate a dyn): Ig(Mni) = {ig_mni*1e12:+.3f} pA, Ig(Mpi) = {ig_mpi*1e12:+.3f} pA -> Total Inv = {i_saliente_inv*1e12:+.3f} pA")
    print(f"  Capacitor CL (a dyn):  I(CL)  = {i_cl*1e12:+.3f} pA")
    print(f"  I_dispositivos:        {(i_saliente_m1 + i_saliente_mp + i_saliente_mk + i_saliente_inv)*1e12:+.3f} pA")
    print(f"  I_residual (KCL):      {i_residual*1e12:+.3f} pA")
    print(f"  I(Vdd):                {i_vdd*1e12:+.3f} pA (I_supply = {-i_vdd*1e12:+.3f} pA)")
