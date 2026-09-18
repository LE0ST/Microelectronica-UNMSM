================================================================================
UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS (UNMSM)
Facultad de Ingeniería Electrónica y Eléctrica (FIEE)
Curso: Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)
Docente: MsC. Luz Adanaqué Infante

ENTREGABLE OFICIAL: LABORATORIO DIRIGIDO N.° 2 (LD2)
TÍTULO: Lógica CMOS Dinámica: Dominó, Compartición de Carga, Keepers y Operación NTV
================================================================================

AUTORES:
- Leonardo Sait Yactayo Tolentino (Código: 23190214)
- Marco Antonio Arcila Santander   (Código: 23190140)

FECHA DE ENTREGA: Viernes 25 de septiembre de 2026

--------------------------------------------------------------------------------
1. ESTRUCTURA DEL PAQUETE REPRODUCIBLE
--------------------------------------------------------------------------------
Este repositorio contiene la totalidad de los netlists de simulación, modelos
PTM renombrados, scripts de extracción de datos, figuras de alta resolución
y el código fuente del informe técnico final:

LD2_Arcila_Yactayo/
├── README.txt                     # Este archivo informativo
│
├── modelos/                       # Modelos predictivos BSIM4 (PTM)
│   ├── originales/                # Tarjetas PTM originales intactas
│   ├── ptm45hp.lib                # 45nm HP con nmos_45hp y pmos_45hp
│   ├── ptm45lp.lib                # 45nm LP con nmos_45lp y pmos_45lp
│   ├── ptm130.lib                 # 130nm bulk con nmos_130 y pmos_130
│   └── README_modelos.md          # Bitácora de renombrado y verificación
│
├── documentacion/                 # Documentos de soporte y control de calidad
│   ├── requisitos.md              # Matriz de requisitos vinculados a la guía
│   ├── criterios_medicion.md      # Convenciones numéricas y opciones de solver
│   ├── predicciones_analiticas.md # Deducciones matemáticas obligatorias (Pre-Lab)
│   ├── ambiguedades.md            # Auditoría de discrepancias y resolución técnica
│   └── registro_ensayos.csv       # Registro trazable de corridas de simulación
│
├── auxiliares/                    # Circuitos de calibración y caracterización
│   └── caracterizacion_inversor/  # Extracción de VM y parámetros del inversor
│
├── act1/                          # Actividad 1: NAND3 dinámica footed y asimetría
├── act2/                          # Actividad 2: Compartición de carga y mitigaciones
├── act3/                          # Actividad 3: Fugas, temperatura y keeper
├── act4/                          # Actividad 4: Monotonicidad y skew de reloj
├── act5/                          # Actividad 5: Clock feedthrough y régimen NTV
├── act6/                          # Actividad 6 (Opcional): NP-domino (zipper)
│
├── scripts/                       # Automatización analítica en Python
│   ├── lectura_resultados/        # Parsers robustos de registros .log de LTspice
│   ├── extraccion_metricas/       # Procesamiento de métricas y tablas LaTeX
│   └── figuras/                   # Generadores matplotlib a 300 DPI
│
├── informe_latex/                 # Código fuente LaTeX del informe maestro
│   ├── LD2.tex                    # Documento maestro (máximo 20 páginas)
│   ├── figuras/                   # Figuras vectoriales / PNG rotuladas
│   └── tablas/                    # Tablas numéricas generadas automáticamente
│
└── entregables/                   # Archivos comprimidos finales (.zip)

--------------------------------------------------------------------------------
2. INSTRUCCIONES DE REPRODUCCIÓN (LTSPICE EN WINDOWS)
--------------------------------------------------------------------------------
Para reproducir cualquier simulación en modo batch (silencioso):
  & "G:\LTspice\LTspice.exe" -b "actN\circuitos\<archivo>.cir"

Para examinar las mediciones cuantitativas automáticas (.meas):
  Inspeccionar el archivo .log correspondiente en "actN\resultados\logs\".

--------------------------------------------------------------------------------
3. INSTRUCCIONES DE POST-PROCESAMIENTO (PYTHON 3)
--------------------------------------------------------------------------------
Todos los scripts emplean bibliotecas estándar (matplotlib, numpy):
  python scripts/extraccion_metricas/<script>.py
  python scripts/figuras/<script_figura>.py

Todas las figuras y tablas se generan de manera trazable y automatizada,
sin manipulación manual de datos.
================================================================================
