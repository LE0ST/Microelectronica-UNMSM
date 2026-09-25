# Notas de Trabajo — Actividad 3: Fugas y dimensionamiento del keeper (HP vs LP, 27°C vs 85°C)

## 1. Objetivos de la Actividad
- [x] Retención con reloj detenido en evaluación ($T_{stop}=1.0\,\mu\text{s}$) a 27°C y 85°C (REQ-14, REQ-15).
- [x] Descomposición y aislamiento de componentes de fuga terminales (subumbral, compuerta, GIDL) (REQ-14, REQ-15).
- [x] Evaluación térmica a 85°C y comparación analítica en 3 niveles (BSIM4, transistor aislado, circuito in situ) (REQ-15).
- [x] Caracterización comparativa de 45nm LP y 130nm bulk a dos temperaturas (REQ-16).
- [x] Evaluación de contención en velocidad: $t_{pHL}$ vs $W_{kp}$ y cota de degradación estricta $< 10.0\%$ (REQ-17).
- [x] Evaluación de alternativas de diseño: Keeper Condicional con línea retardada y descomposición causal (REQ-18).

## 2. Circuitos y Netlists Asociados
* Ubicación de netlists: `act3/circuitos/`
* Registros de simulación (.log): `act3/resultados/logs/`
* Formas de onda crudas (.raw): `act3/resultados/raw/`
* Datos estructurados (.json): `act3/resultados/datos/`
* Figuras científicas (.png): `act3/figuras/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas (ventana de retención estricta: $[10\text{ ns}, 1.00052\,\mu\text{s}]$).
* Opciones de solver verificadas: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Ausencia de advertencias de convergencia en logs; archivos RAW sin truncamiento.
* Cierre de punto literal de la guía: $W_{kp} = 22\text{ nm}$ evaluado y verificado en 27°C y 85°C (`ENS-A3-RET-22NM-27C`, `ENS-A3-RET-22NM-85C`).
* Clasificación estricta de 130nm: falla de criterio $0.90\,V_{DD}$ sin falla lógica ($V_{dyn} > V_M$).

## 4. Registro de Resultados Clave Consolidados (Fase A3.8.7)
1. **Retención Tecnológica Comparativa Sin Keeper ($T_{stop}=1.0\,\mu\text{s}$):**
   * **45nm HP ($V_{DD}=1.0\text{ V}$):**
     * 27°C: $V_{dyn}(t_0=10\text{ ns}) = 1.0235\text{ V}$, $V_{dyn}(t_1=1.0\,\mu\text{s}) = 0.9370\text{ V}$ ($\Delta V = -86.5\text{ mV}$). Cumple holgadamente ($V_{dyn} > 0.90\text{ V}$).
     * 85°C: $V_{dyn}(t_0=10\text{ ns}) = 1.0240\text{ V}$, $V_{dyn}(t_1=1.0\,\mu\text{s}) = 0.8309\text{ V}$ ($\Delta V = -193.1\text{ mV}$). Cruza $0.90\,V_{DD}$ en $t_{\text{cross}} = 608.7\text{ ns}$ (falla criterio estricto, sin falla lógica frente a $V_M \approx 0.50\text{ V}$).
     * Con keeper: $W_{kp} \in [10.5, 180]\,\text{nm}$ y $W_{kp}=22\,\text{nm}$ cumplen retención ($V_{dyn} > 0.9999\,\text{V}$).
     * Límite de modelo: $W_{kp}=1\,\text{nm}$ aborta en BSIM4 por $W_{eff} \le 0$ ($W_{int}=5\,\text{nm}$).
   * **45nm LP ($V_{DD}=1.2\text{ V}$):**
     * 27°C: $V_{dyn}(1.0\,\mu\text{s}) = 1.12748\text{ V}$ (retiene sin keeper, no cruza $0.90\,V_{DD}$).
     * 85°C: $V_{dyn}(1.0\,\mu\text{s}) = 1.12570\text{ V}$ (retiene sin keeper, margen muy superior por canal largo/óxido grueso).
   * **130nm Bulk ($V_{DD}=1.2\text{ V}$):**
     * 27°C: $V_{dyn}(1.0\,\mu\text{s}) = 1.01777\text{ V}$ (cruza $0.90\,V_{DD} = 1.08\text{ V}$ en $t_{\text{cross}} = 318.8\text{ ns}$; falla criterio estricto, pero retiene nivel lógico frente a $V_M \approx 0.60\text{ V}$).
     * 85°C: $V_{dyn}(1.0\,\mu\text{s}) = 0.87697\text{ V}$ (cruza $0.90\,V_{DD}$ en $t_{\text{cross}} = 168.0\text{ ns}$; falla criterio estricto, sin falla lógica frente a $V_M$).
     * *(La extensión provisional de 130nm/85°C requiere keeper mayor por subumbral acumulado)*.
2. **Balance Nodal en $dyn$ (Promedios Integrales $10\text{ ns}\to 1.00052\,\mu\text{s}$):**
   * 27°C: $I_s(M_1)=110.528\,\text{pA}$, $I_d(M_p)=-12.259\,\text{pA}$, $I_g(M_{pi})=76.311\,\text{pA}$, $I_g(M_{ni})=16.441\,\text{pA}$.
   * 85°C: $I_s(M_1)=430.888\,\text{pA}$, $I_d(M_p)=-56.081\,\text{pA}$, $I_g(M_{pi})=49.862\,\text{pA}$, $I_g(M_{ni})=0.612\,\text{pA}$.
   * Partición de descarga (PDN vs Inversor): $54.4\% / 45.6\%$ a 27°C; $89.5\% / 10.5\%$ a 85°C.
   * Capacitancia dinámica aparente inferida: $C_{\text{eff}} \approx 2.18644\,\text{fF}$ (27°C) y $2.18142\,\text{fF}$ (85°C), con $I(C_L) = -174.732\,\text{pA}$ y $-389.913\,\text{pA}$ verificado en RAW.
3. **Contención y Ventana Viable a 85°C:**
   * 45nm HP: $W_{kp} = 38\,\text{nm}$ es el máximo ensayado que cumple velocidad ($\Delta t_{pHL} = +9.94\%$ Config A / $+9.96\%$ Config B); $W_{kp}=39\,\text{nm}$ falla ($+10.35\%$).
   * 45nm LP: $W_{kp} = 36\,\text{nm}$ es el máximo ensayado que cumple velocidad ($\Delta t_{pHL} = +9.99\%$); $W_{kp}=37\,\text{nm}$ falla ($+10.45\%$).
   * Ventana viable HP: $[10.5, 38]\,\text{nm}$ ($r \in [0.156, 0.563]$); puntos $31\dots 34\,\text{nm}$ evaluados directamente en contención e inferidos monótonamente en retención.
4. **Keeper Condicional (Alternativa Complementaria):**
   * Reduce penalización de $+12.90\%$ (convencional 45nm) a $+5.11\%$.
   * La mejora refleja conjuntamente la resistencia de paso de dos PMOS en serie, el desfase de habilitación y cargas adicionales (no una partición causal pura).
   * Sobrecarga de reloj estimada geométricamente en $+55.5\%$ respecto a la carga base.
