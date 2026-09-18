# Notas de Trabajo — Actividad 5: Clock feedthrough, frecuencia mínima y régimen NTV

## 1. Objetivos de la Actividad
- [ ] Medición de sobreimpulso y subimpulso de feedthrough con CL=0.5fF y tr=5ps.\n- [ ] Análisis de recorte por diodo drenador-sustrato D-B.\n- [ ] Barrido VDD de 1.0V a 0.35V en 45nm HP; medición de teval y thold.\n- [ ] Cálculo de fmax y fmin; graficación de la ventana de frecuencia e identificación de VDD,min.\n- [ ] Impacto del keeper y del proceso 45nm LP en NTV.\n- [ ] Redacción de la conclusión obligatoria de viabilidad en NTV (máximo 10 líneas).

## 2. Circuitos y Netlists Asociados
* Ubicación: `act5/circuitos/`
* Registro de simulación: `act5/resultados/logs/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas.
* Opciones de solver: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Ausencia de advertencias de convergencia en el log.

## 4. Registro de Resultados Clave
*(Se completará durante la ejecución de simulaciones en la Fase 2)*
