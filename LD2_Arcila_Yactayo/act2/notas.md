# Notas de Trabajo — Actividad 2: Compartición de carga: predicción, medición y mitigación

## 1. Objetivos de la Actividad
- [ ] Deducción analítica previa de Ca y dVpred.\n- [ ] Simulación de peor caso con parámetros de difusión AS/AD/PS/PD.\n- [ ] Barrido de CL (0.5fF a 4fF) y detección de rango de falla lógica.\n- [ ] Mitigación 1: Precarga de nodos internos n1 y n2 con PMOS.\n- [ ] Mitigación 2: Reordenamiento de apilamiento en la PDN.\n- [ ] Mitigación 3: Incorporación de keeper W=45nm.

## 2. Circuitos y Netlists Asociados
* Ubicación: `act2/circuitos/`
* Registro de simulación: `act2/resultados/logs/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas.
* Opciones de solver: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Ausencia de advertencias de convergencia en el log.

## 4. Registro de Resultados Clave
*(Se completará durante la ejecución de simulaciones en la Fase 2)*
