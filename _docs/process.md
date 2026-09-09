# Proceso Operativo y Protocolo de Laboratorio (`_docs/process.md`)

Este documento establece el protocolo estándar de trabajo para la ejecución de simulaciones SPICE, extracción de parámetros, generación de figuras de alta resolución, redacción de informes en LaTeX y control de calidad académico en el repositorio **Microelectronica-UNMSM**.

---

## 1. Ciclo de Vida de una Actividad de Laboratorio

Todo laboratorio o diseño analógico/digital en este repositorio sigue un flujo secuencial riguroso de 5 fases:

```
[ 1. Pre-Lab Teórico ] ──> [ 2. Netlist SPICE ] ──> [ 3. Simulación & .meas ]
                                                               │
[ 5. Auditoría & Entrega ] <── [ 4. Figuras & LaTeX ] <────────┘
```

### Fase 1: Análisis Teórico y Pre-Lab
1. Consultar la guía oficial en `Semana_XX/Guia_Oficial_*/`.
2. Deducir algebraicamente los puntos estáticos ($V_M$, márgenes de ruido $NM_L/NM_H$) y dinámicos ($t_p$, capacitancias equivalentes).
3. Identificar el régimen físico dominante:
   - Canales largos ($\ge 180\text{ nm}$): Modelo cuadrático de saturación ($I_D \propto (V_{GS}-V_T)^2$).
   - Nodos submicrométricos ($\le 65\text{ nm}$): Saturación de velocidad por alto campo eléctrico ($I_D \propto (V_{GS}-V_T) v_{sat}$).

### Fase 2: Configuración de Netlists SPICE
1. Crear un subdirectorio temático en `LDX_*/simulaciones/A*_.../`.
2. Incluir los modelos predictivos PTM (`.include 45nm_HP.pm`, etc.) ubicados en `modelos/` o en la carpeta local.
3. Declarar explícitamente parámetros tecnológicos:
   - Longitud mínima: `.param Lmin = 45n`
   - Ancho unitario de referencia: `.param Wn = 4*Lmin` (180 nm en 45 nm)
   - Razón de aspecto PMOS/NMOS: `.param beta = ...`
4. Configurar estímulos limpios (`PULSE`, `.dc`, `.tran`) con tiempos de subida y bajada no nulos ($t_r, t_f \ge 5\text{ ps}$ para prevenir singularidades numéricas).

### Fase 3: Simulación por Lote y Extracción Automática
1. Ejecutar en modo *batch* (`LTspice.exe -b -ascii ...`).
2. Utilizar directivas `.meas` para todas las métricas cuantitativas clave:
   - Umbral estático: `.meas dc VM FIND V(in) WHEN V(out)=V(in)`
   - Retardos: `.meas tran tpHL TRIG ... TARG ...`
   - Corriente media y fuga: `.meas tran Iavg AVG I(V1)` / `.meas dc Ileak_lo FIND I(V1) AT 0`
3. Inspeccionar el archivo `.log` resultante. **Nunca copiar datos a mano sin cotejar contra el registro generado.**

### Fase 4: Post-procesamiento y Redacción del Informe
1. Generar gráficas vectoriales o PNG a 300 DPI con scripts de Python (`matplotlib`) alojados en `scripts/`:
   - Ejes claramente rotulados con unidades físicas en KaTeX/LaTeX.
   - Puntos críticos señalados con anotaciones (`plt.annotate`).
   - Paleta de color institucional (Azul `#1E2761`, Rojo/Coral `#F96167`).
2. Insertar resultados en la plantilla oficial LaTeX (`LDX.tex`):
   - Formato IEEE de doble columna.
   - Límite estricto de páginas (ej. 12 páginas para LD1).
   - Cada tabla debe citarse en el texto (`Tabla~\ref{tab:...}`).
   - Cada pregunta de la rúbrica debe contar con respuesta técnica exhaustiva fundamentada en física de semiconductores.

### Fase 5: Verificación y Entrega
1. Correr script de balanceo de entornos LaTeX.
2. Confirmar que no queden discrepancias entre el texto explicativo, las tablas, los esquemas circuitales y los anexos de código.
3. Generar el archivo comprimido `.zip` requerido por el aula virtual.
4. Hacer `commit` convencional y `push` a la rama `main`.

---

## 2. Protocolo de Manejo de Modelos Tecnológicos PTM

1. **Inmutabilidad:** Las tarjetas PTM originales (`45nm_HP.pm`, `45nm_LP.pm`, `90nm_bulk.pm`, `22nm_HP.pm`) descargadas de Nanoscale Integration and Modeling (NIMO) son de solo lectura. No se deben editar los coeficientes del modelo BSIM4 directamente.
2. **Prevención de colisiones:** Si una simulación involucra simultáneamente transistores de alto rendimiento (HP) y bajo consumo (LP) en el mismo archivo SPICE, usar las librerías renombradas (`45nm_HP_ren.lib` y `45nm_LP_ren.lib`), las cuales asignan nombres únicos de subcircuito (`nmos_hp`, `pmos_hp`, `nmos_lp`, `pmos_lp`).
3. **Escalamiento de tensiones:**
   - 90 nm: $V_{DD} = 1.2\text{ V}$
   - 45 nm HP: $V_{DD} = 1.0\text{ V}$
   - 45 nm LP: $V_{DD} = 1.1\text{ V}$
   - 22 nm HP: $V_{DD} = 0.8\text{ V}$

---

## 3. Lista de Chequeo para Pull Requests y Commits (QA Checklist)

Antes de realizar un commit a `main`, validar los siguientes 6 puntos:

- [ ] **Simulaciones verificadas:** Todos los valores numéricos citados en el texto provienen de un archivo `.log` real.
- [ ] **Consistencia de $\beta$:** La calibración de $\beta$ del inversor se propaga fielmente a las celdas estándar derivadas.
- [ ] **Límite de páginas:** El informe en LaTeX no supera el tope máximo de la guía (12 páginas).
- [ ] **Integridad gráfica:** Todas las figuras referenciadas (`\includegraphics`) existen en `figuras/` y renderizan sin oclusiones de texto.
- [ ] **Limpieza del árbol Git:** Ningún archivo binario o temporal de LTspice (`.raw`, `.op.raw`, `.db`) ha sido añadido al repositorio.
- [ ] **Mensaje de commit estructurado:** Sigue el estándar Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`).
