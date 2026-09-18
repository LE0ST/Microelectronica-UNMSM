# Notas de Trabajo — Actividad 1: NAND3 dinámica footed: fases, asimetría y consumo

## 1. Objetivos de la Actividad
- [ ] Captura de formas de onda conjuntas V(clk), V(a), V(dyn), V(out) anotando fases.\n- [ ] Medición de tpHL (evaluación) y tpLH (precarga) justificando asimetría.\n- [ ] Diseño de NAND3 estática equivalente y comparación de métricas (Tabla 1).\n- [ ] Cálculo analítico de potencia dinámica vs simulación con entradas fijas en 1.\n- [ ] Apertura de PDN y comparación de retención a 2ns vs 400ns.

## 2. Circuitos y Netlists Asociados
* Ubicación: `act1/circuitos/`
* Registro de simulación: `act1/resultados/logs/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas.
* Opciones de solver: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Ausencia de advertencias de convergencia en el log.

## 4. Registro de Resultados Clave
*(Se completará durante la ejecución de simulaciones en la Fase 2)*
