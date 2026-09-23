# Notas de Trabajo — Actividad 2: Compartición de carga: predicción, medición y mitigación

## 1. Objetivos de la Actividad
- [ ] Deducción analítica previa de Ca y dVpred.\n- [ ] Simulación de peor caso con parámetros de difusión AS/AD/PS/PD.\n- [ ] Barrido de CL (0.5fF a 4fF) y detección de rango de falla lógica.\n- [ ] Mitigación 1: Precarga de nodos internos n1 y n2 con PMOS.\n- [ ] Mitigación 2: Reordenamiento de apilamiento en la PDN.\n- [ ] Mitigación 3: Incorporación de keeper W=45nm.

## 2. Circuitos y Netlists Asociados
* Ubicación: `act2/circuitos/`
* Registro de simulación: `act2/resultados/logs/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas.
* Opciones de solver: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Comportamiento de convergencia del solver:
  - En los netlists sin keeper y con precarga/reordenamiento, la iteración directa de Newton converge inmediatamente (`Direct Newton iteration succeeded`).
  - En los netlists con keeper realimentado (`nand3_cs_contencion_con_keeper.log` y `nand3_cs_mitigacion_keeper.log`), la iteración directa de Newton falla inicialmente en el punto de operación DC (`Direct Newton failed`), pero el algoritmo de respaldo de LTspice recupera la convergencia exitosamente mediante `Gmin stepping` (`Gmin stepping succeeded in finding the operating point`).
  - En todos los casos, el análisis transitorio converge completamente sin errores fatales y todas las mediciones `.meas` son plenamente válidas y estables.

## 4. Registro de Resultados Clave
*(Se completará durante la ejecución de simulaciones en la Fase 2)*
