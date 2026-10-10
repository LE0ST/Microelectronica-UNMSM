# Bitácora de Desarrollo del Proyecto (`_docs/bitacora.md`)

Este documento constituye el registro cronológico oficial de hitos, decisiones de ingeniería, cambios arquitectónicos, validaciones experimentales y seguimiento de pendientes en el repositorio **Microelectronica-UNMSM**.

---

## Estructura Estándar para Nuevas Entradas

Para registrar una nueva actividad, añadir una sección al inicio de la lista cronológica con la siguiente plantilla:

```markdown
### [YYYY-MM-DD] — Actividad: [Título Breve de la Actividad]
* **Módulo / Entregable:** [LD1 / LD2 / LD3 / Documentación / Infraestructura]
* **Autor(es):** [Leonardo Yactayo / Marco Arcila]
* **Estado:** [EN PROGRESO / COMPLETADO / EN REVISIÓN / BLOQUEADO]
* **Rama / Commit:** [Rama de trabajo | SHA si existe commit real]
* **Archivos Modificados / Creados:**
  * `ruta/archivo1.ext` — Descripción concisa del cambio
* **Decisiones Técnicas / Justificación:**
  * [Decisión 1 y respaldo físico o metodológico]
* **Resultados Obtenidos:**
  * [Métricas cuantitativas verificadas sin redondeos especulativos]
* **Pendientes / Próximos Pasos:**
  * [ ] [Tarea inmediata a desarrollar]
```

---

## Registro Cronológico de Entradas

### [2026-10-10] — Actividad: Auditoría G0 y Normalización Documental G1
* **Módulo / Entregable:** Infraestructura Global / Preparación LD3
* **Autor(es):** Leonardo Sait Yactayo Tolentino
* **Estado:** COMPLETADO (Fases G0 y G1)
* **Rama / Commit:** `feat/ld3-igbt` | *(Sin commit en fase G1 — a la espera de aprobación para commit)*
* **Archivos Modificados / Creados:**
  * `.gitignore` — Refinamiento de exclusiones de evaluaciones locales (`Semana_06/*LC1*.zip`) para evitar ocultar archivos académicos futuros de `Semana_06`.
  * `_docs/plan.md` — Corrección integral: LD2 marcado como completado (100%), LD3 redefinido como transistores IGBT individual (exposición 21/10/2026).
  * `_docs/process.md` — Separación explícita entre reglas globales innegociables y requisitos específicos de LD1, LD2 y LD3.
  * `README.md` — Actualización de autorías (Leonardo y Marco en LD1/LD2; Leonardo individual en LD3), mapa de carpetas, corrección de enlace a `LD1_Arcila_Yactayo.pdf` y presentación de LD3.
  * `AGENTS.md` — Context Engineering actualizado, eliminación de comando inseguro `git add .`, desvinculación de reglas de $\beta$ y 12 páginas para LD3, y corrección de enlaces rotos.
  * `CLAUDE.md` — Actualización de instrucciones y comandos para Claude Code y asistentes IA.
  * `_docs/bitacora.md` — Creación de la bitácora global e inicialización de la primera entrada.
  * `LD3_Yactayo/README.md` — Creación de la portada técnica y metodología de LD3.
  * `LD3_Yactayo/TRAZABILIDAD.md` — Creación de la matriz de trazabilidad con 11 requisitos docentes en estado PENDIENTE.
  * `LD3_Yactayo/modelos/NOTAS_MODELOS.md` — Documentación de procedencia, fuentes oficiales y términos de uso de modelos IGBT existentes.
* **Decisiones Técnicas / Justificación:**
  * **Autoría y Modalidad:** Se formalizó la autoría individual de Leonardo Yactayo en LD3 según lo respaldado por la guía oficial («El laboratorio puede ser en parejas o individual»), preservando la coautoría histórica con Marco Arcila en LD1 y LD2.
  * **Fuente de Verdad de LD3:** Se estableció que `Semana_07/Guia_Oficial_LD3/LabDirigidoNro03.pdf` prevalece sobre borradores y planes antiguos del repositorio (los cuales erróneamente listaban amplificadores CMOS analógicos).
  * **Aprovechamiento de Modelos Existentes:** Se constató que las librerías `nigbt.lib`, `pigbt.lib` y los 4 modelos de Fuji Electric Serie X (`FGW50XS65`, `FGW50XS65C`, `FGW75XS65`, `FGW75XS65C`) ya residen y están rastreados en `Semana_02/Material_Adicional_Semestre/05_Laboratorio_IGBT/Circuitos_y_Modelos/`. Se decidió no duplicarlos físicamente en el repositorio, documentando su procedencia en `NOTAS_MODELOS.md`.
  * **Desacoplamiento de Reglas de LD1:** Se desvincularon las directivas de $\beta=2.50$, límite de 12 páginas y modelos BSIM4 nanométricos para LD3, dado que un banco de IGBTs de potencia se rige por su propia física y requerimientos de guía.
* **Resultados Obtenidos:**
  * Repositorio completamente auditado y normalizado sin pérdida de consistencia.
  * Rama de trabajo `feat/ld3-igbt` activa y desacoplada de `main`.
  * Enlaces rotos eliminados y coherencia documental al 100%.
* **Pendientes / Próximos Pasos:**
  * [ ] Presentar reporte de cierre G1 y aguardar aprobación del usuario antes de cualquier commit o simulación.
  * [ ] Fase G2: Configuración circuital de esquemas DPT en `LD3_Yactayo/esquemas/` y ejecución de simulaciones transitorias SPICE de calibración (NIGBT vs PIGBT).
