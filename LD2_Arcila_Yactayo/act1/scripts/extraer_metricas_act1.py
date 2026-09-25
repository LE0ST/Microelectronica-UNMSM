# -*- coding: utf-8 -*-
"""
Extraccion y Estructuracion de Metricas - Actividad 1 (LD2)
Utiliza parse_spice_log.py para extraer mediciones de los logs de simulacion
y consolida los resultados cuantitativos en un archivo JSON.
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACT1_DIR = os.path.dirname(SCRIPT_DIR)
LOGS_DIR = os.path.join(ACT1_DIR, "resultados", "logs")
DATOS_DIR = os.path.join(ACT1_DIR, "resultados", "datos")

# Importar parser robusto de LD2
PARSER_DIR = os.path.abspath(os.path.join(ACT1_DIR, "..", "scripts", "lectura_resultados"))
sys.path.insert(0, PARSER_DIR)
from parse_spice_log import parse_log, get_metric

def main():
    os.makedirs(DATOS_DIR, exist_ok=True)
    json_path = os.path.join(DATOS_DIR, "act1_metricas.json")

    print("==================================================================")
    print("EXTRACCION DE METRICAS DE PRODUCCION - ACTIVIDAD 1 (LD2)")
    print(f"Carpeta de logs: {LOGS_DIR}")
    print("==================================================================")

    metricas_totales = {}

    # 1. NAND3 Dinamica Base
    log_din_base = os.path.join(LOGS_DIR, "nand3_dinamica_base.log")
    res_din_base = parse_log(log_din_base, required_metrics=['tphl_dyn', 'tplh_dyn', 'tplh_out', 'tphl_out', 'pavg'])
    metricas_totales['dinamica_base'] = {
        'tphl_dyn_s': get_metric(res_din_base, 'tphl_dyn'),
        'tplh_dyn_s': get_metric(res_din_base, 'tplh_dyn'),
        'tplh_out_s': get_metric(res_din_base, 'tplh_out'),
        'tphl_out_s': get_metric(res_din_base, 'tphl_out'),
        'tpd_eval_dyn_s': get_metric(res_din_base, 'tpd_eval_dyn'),
        'tpd_eval_out_s': get_metric(res_din_base, 'tpd_eval_out'),
        'pavg_w': get_metric(res_din_base, 'pavg'),
    }

    # 2. NAND3 Estatica Base (Historica: A conmutando a 500 MHz, T_A = 2ns)
    log_stat_base = os.path.join(LOGS_DIR, "nand3_estatica_base.log")
    res_stat_base = parse_log(log_stat_base, required_metrics=['tphl_stat', 'tplh_stat', 'pavg_stat_sw'])
    metricas_totales['estatica_base_historica'] = {
        'tphl_stat_s': get_metric(res_stat_base, 'tphl_stat'),
        'tplh_stat_s': get_metric(res_stat_base, 'tplh_stat'),
        'pavg_stat_sw_w': get_metric(res_stat_base, 'pavg_stat_sw'),
    }

    # 2b. NAND3 Estatica Mismo Estimulo (ENS-A1-07: A conmutando a 125 MHz, T_A = 8ns, identico a dinamica)
    log_stat_mismo = os.path.join(LOGS_DIR, "nand3_estatica_mismo_estimulo.log")
    res_stat_mismo = parse_log(log_stat_mismo, required_metrics=['tphl_stat', 'tplh_stat', 'pavg_stat_sw'])
    metricas_totales['estatica_mismo_estimulo'] = {
        'tphl_stat_s': get_metric(res_stat_mismo, 'tphl_stat'),
        'tplh_stat_s': get_metric(res_stat_mismo, 'tplh_stat'),
        'pavg_stat_sw_w': get_metric(res_stat_mismo, 'pavg_stat_sw'),
        'ratio_potencia_conmutando': metricas_totales['dinamica_base']['pavg_w'] / get_metric(res_stat_mismo, 'pavg_stat_sw'),
    }

    # 2c. Control de Ingenieria: Retardo Equivalente Dominó (ENS-A1-08: CL=0 en dyn)
    log_ctrl_ret = os.path.join(LOGS_DIR, "nand3_control_retardo_equivalente.log")
    res_ctrl_ret = parse_log(log_ctrl_ret, required_metrics=['tphl_dyn', 'tplh_dyn', 'tplh_out', 'tphl_out', 'pavg'])
    metricas_totales['control_retardo_equivalente_cl0'] = {
        'tphl_dyn_s': get_metric(res_ctrl_ret, 'tphl_dyn'),
        'tplh_dyn_s': get_metric(res_ctrl_ret, 'tplh_dyn'),
        'tplh_out_s': get_metric(res_ctrl_ret, 'tplh_out'),
        'tphl_out_s': get_metric(res_ctrl_ret, 'tphl_out'),
        'pavg_w': get_metric(res_ctrl_ret, 'pavg'),
    }

    # 3. Entradas Fijas en 1 (Dinamica vs Estatica)
    log_din_f1 = os.path.join(LOGS_DIR, "nand3_dinamica_fijas1.log")
    res_din_f1 = parse_log(log_din_f1, required_metrics=['pavg_dyn_fixed1'])
    log_stat_f1 = os.path.join(LOGS_DIR, "nand3_estatica_fijas1.log")
    res_stat_f1 = parse_log(log_stat_f1, required_metrics=['pavg_stat_fixed1'])

    metricas_totales['entradas_fijas_1'] = {
        'pavg_dyn_fixed1_w': get_metric(res_din_f1, 'pavg_dyn_fixed1'),
        'pavg_stat_fixed1_w': get_metric(res_stat_f1, 'pavg_stat_fixed1'),
        'ratio_potencia_fijas1': get_metric(res_din_f1, 'pavg_dyn_fixed1') / get_metric(res_stat_f1, 'pavg_stat_fixed1'),
    }

    # 4. Capacitancia de Entrada Cin(A)
    # 4a. Referencia Canonica Corregida (ENS-A1-HIG-01: Mni W=90nm)
    log_cin_corr = os.path.join(LOGS_DIR, "nand3_extraccion_cin_corregido.log")
    res_cin_corr = parse_log(log_cin_corr, required_metrics=['qin_dyn', 'qin_stat', 'cin_dyn', 'cin_stat', 'ratio_cin'])

    # 4b. Historico Banco Original (ENS-A1-04: Mni W=270nm)
    log_cin_hist = os.path.join(LOGS_DIR, "nand3_extraccion_cin.log")
    res_cin_hist = parse_log(log_cin_hist, required_metrics=['qin_dyn', 'qin_stat', 'cin_dyn', 'cin_stat', 'ratio_cin'])

    metricas_totales['capacitancia_entrada'] = {
        'qin_dyn_c': get_metric(res_cin_corr, 'qin_dyn'),
        'qin_stat_c': get_metric(res_cin_corr, 'qin_stat'),
        'cin_dyn_f': get_metric(res_cin_corr, 'cin_dyn'),
        'cin_stat_f': get_metric(res_cin_corr, 'cin_stat'),
        'ratio_cin': get_metric(res_cin_corr, 'ratio_cin'),
        'ensayo_referencia': "ENS-A1-HIG-01 (nand3_extraccion_cin_corregido.cir, Mni W=90nm)",
        'historico_banco_original': {
            'qin_dyn_c': get_metric(res_cin_hist, 'qin_dyn'),
            'qin_stat_c': get_metric(res_cin_hist, 'qin_stat'),
            'cin_dyn_f': get_metric(res_cin_hist, 'cin_dyn'),
            'cin_stat_f': get_metric(res_cin_hist, 'cin_stat'),
            'ratio_cin': get_metric(res_cin_hist, 'ratio_cin'),
            'ensayo': "ENS-A1-04 (nand3_extraccion_cin.cir, Mni W=270nm)"
        }
    }

    # 5. Retencion con PDN Abierta (Tclk = 2 ns vs 400 ns)
    log_ret_2n = os.path.join(LOGS_DIR, "nand3_dinamica_pdn_abierta_tclk2n.log")
    res_ret_2n = parse_log(log_ret_2n, required_metrics=['vdyn_min', 'vdyn_drop', 'vout_max'])
    log_ret_400n = os.path.join(LOGS_DIR, "nand3_dinamica_pdn_abierta_tclk400n.log")
    res_ret_400n = parse_log(log_ret_400n, required_metrics=['vdyn_final', 'vdyn_min', 'vdyn_drop', 'vout_final', 'vout_max'])

    metricas_totales['retencion_pdn_abierta'] = {
        'tclk_2n': {
            'vdyn_min_v': get_metric(res_ret_2n, 'vdyn_min'),
            'vdyn_drop_v': get_metric(res_ret_2n, 'vdyn_drop'),
            'vout_max_v': get_metric(res_ret_2n, 'vout_max'),
        },
        'tclk_400n': {
            'vdyn_final_v': get_metric(res_ret_400n, 'vdyn_final'),
            'vdyn_min_v': get_metric(res_ret_400n, 'vdyn_min'),
            'vdyn_drop_v': get_metric(res_ret_400n, 'vdyn_drop'),
            'vout_final_v': get_metric(res_ret_400n, 'vout_final'),
            'vout_max_v': get_metric(res_ret_400n, 'vout_max'),
        }
    }

    # Guardar en archivo JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metricas_totales, f, indent=2)

    print(f"\n[OK] Metricas consolidadas exitosamente en: {json_path}")
    print("\n--- RESUMEN DE METRICAS PRINCIPALES ---")
    print(f"tpHL Dinamico (evaluacion dyn) : {metricas_totales['dinamica_base']['tphl_dyn_s']*1e12:.2f} ps")
    print(f"tpLH Dinamico (precarga dyn)   : {metricas_totales['dinamica_base']['tplh_dyn_s']*1e12:.2f} ps")
    print(f"tpLH Salida (evaluacion out)   : {metricas_totales['dinamica_base']['tplh_out_s']*1e12:.2f} ps")
    print(f"tpHL Salida (precarga out)     : {metricas_totales['dinamica_base']['tphl_out_s']*1e12:.2f} ps")
    print(f"tpHL Estatico (Mismo Estimulo) : {metricas_totales['estatica_mismo_estimulo']['tphl_stat_s']*1e12:.2f} ps")
    print(f"tpLH Estatico (Mismo Estimulo) : {metricas_totales['estatica_mismo_estimulo']['tplh_stat_s']*1e12:.2f} ps")
    print(f"tpHL Estatico (Historico 500M) : {metricas_totales['estatica_base_historica']['tphl_stat_s']*1e12:.2f} ps")
    print(f"tpLH Estatico (Historico 500M) : {metricas_totales['estatica_base_historica']['tplh_stat_s']*1e12:.2f} ps")
    print(f"Cin(A) Dinamica (Canonica)     : {metricas_totales['capacitancia_entrada']['cin_dyn_f']*1e15:.4f} fF")
    print(f"Cin(A) Estatica                : {metricas_totales['capacitancia_entrada']['cin_stat_f']*1e15:.4f} fF")
    print(f"Cociente Cin(A) (Dyn/Stat)     : {metricas_totales['capacitancia_entrada']['ratio_cin']:.4f}")
    print(f"Cin(A) Dinamica (Historico)    : {metricas_totales['capacitancia_entrada']['historico_banco_original']['cin_dyn_f']*1e15:.4f} fF")
    print(f"Cociente Historico (Dyn/Stat)  : {metricas_totales['capacitancia_entrada']['historico_banco_original']['ratio_cin']:.4f}")
    print(f"Pavg Dinamica (A conmutando)   : {metricas_totales['dinamica_base']['pavg_w']*1e6:.4f} uW")
    print(f"Pavg Estatica (Mismo Estimulo) : {metricas_totales['estatica_mismo_estimulo']['pavg_stat_sw_w']*1e6:.4f} uW")
    print(f"Pavg Estatica (Historico 500M) : {metricas_totales['estatica_base_historica']['pavg_stat_sw_w']*1e6:.4f} uW")
    print(f"Ratio Pavg (Mismo Estimulo)    : {metricas_totales['estatica_mismo_estimulo']['ratio_potencia_conmutando']:.3f}x")
    print(f"Pavg Dinamica (Fijas en 1)     : {metricas_totales['entradas_fijas_1']['pavg_dyn_fixed1_w']*1e6:.4f} uW")
    print(f"Pavg Estatica (Fijas en 1)     : {metricas_totales['entradas_fijas_1']['pavg_stat_fixed1_w']*1e9:.4f} nW")
    print(f"Factor Consumo Fijas en 1      : {metricas_totales['entradas_fijas_1']['ratio_potencia_fijas1']:.1f}x")
    print(f"Caida Vdyn (Tclk=2ns, 1ns eval): {metricas_totales['retencion_pdn_abierta']['tclk_2n']['vdyn_drop_v']*1e3:.2f} mV")
    print(f"Caida Vdyn (Tclk=400n, 200n ev): {metricas_totales['retencion_pdn_abierta']['tclk_400n']['vdyn_drop_v']*1e3:.2f} mV")
    print(f"Control CL=0: tpHL_dyn={metricas_totales['control_retardo_equivalente_cl0']['tphl_dyn_s']*1e12:.2f} ps, tpLH_out={metricas_totales['control_retardo_equivalente_cl0']['tplh_out_s']*1e12:.2f} ps")

if __name__ == '__main__':
    main()
