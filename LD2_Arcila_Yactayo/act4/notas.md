# Notas de Trabajo — Actividad 4: Regla de monotonicidad, cascada dominó y skew de reloj

## 1. Objetivos de la Actividad
- [ ] Demostración de falla lógica en cascada directa dyn1 -> etapa 2.\n- [ ] Inserción de inversor estático dominó y corrección funcional.\n- [ ] Estímulo no monótono en entrada X y análisis de interfaz con flip-flops (TGFF).\n- [ ] Cascada de 3 etapas footed vs unfooted bajo barrido de skew (-50ps a 200ps).\n- [ ] Medición de corriente pico de cortocircuito en precarga y retardo.\n- [ ] Determinación de la condición de temporización para omitir footer.

## 2. Circuitos y Netlists Asociados
* Ubicación: `act4/circuitos/`
* Registro de simulación: `act4/resultados/logs/`

## 3. Verificación de Criterios y Trazabilidad
* Conteo de flancos y ventanas temporales revisadas.
* Opciones de solver: `gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear`.
* Ausencia de advertencias de convergencia en el log.

## 4. Registro de Resultados Clave
*(Se completará durante la ejecución de simulaciones en la Fase 2)*
