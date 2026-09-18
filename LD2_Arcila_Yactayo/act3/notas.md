# Notas de Trabajo — Actividad 3: Fugas y dimensionamiento del keeper (HP vs LP, 27°C vs 85°C)

## 1. Objetivos de la Actividad
- [ ] Retención con reloj detenido en evaluación (Tstop=1us) a 27°C.\n- [ ] Descomposición de componentes de fuga (subumbral, compuerta, GIDL).\n- [ ] Evaluación térmica a 85°C y comparación con modelo analítico.\n- [ ] Caracterización de 45nm LP y 130nm bulk a dos temperaturas.\n- [ ] Evaluación de contención: tpHL vs Wkp y degradación del 10%.\n- [ ] Diseño de keeper condicional para abrir ventana de contención.

## 2. Circuitos y Netlists Asociados
* Ubicación: `act3/circuitos/`
* Registro de simulación: `act3/resultados/logs/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas.
* Opciones de solver: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Ausencia de advertencias de convergencia en el log.

## 4. Registro de Resultados Clave
*(Se completará durante la ejecución de simulaciones en la Fase 2)*
