==============================================================================
UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS
FACULTAD DE INGENIERIA ELECTRONICA Y ELECTRICA
ESCUELA PROFESIONAL DE INGENIERIA ELECTRONICA
Curso: Microelectronica y Sistemas Nanoelectronicos (Semestre 2026-II)
Docente: MsC. Luz Adanaque Infante
==============================================================================
LABORATORIO DIRIGIDO N.o 2: LOGICA CMOS DINAMICA SUBMICROMETRICA
Entregable Oficial del Paquete de Simulacion y Reporte Tecnico
Fecha de Entrega: Viernes 25 de septiembre de 2026
Integrantes:
- Leonardo Sait Yactayo Tolentino (Codigo: 23190214)
- Marco Antonio Arcila Santander   (Codigo: 23190140)
==============================================================================

1. CONTENIDO Y ESTRUCTURA DEL PAQUETE
------------------------------------------------------------------------------
El presente paquete contiene la totalidad de los archivos de simulacion fisica
SPICE, modelos predictivos PTM BSIM4, post-procesamiento en Python, datos
cuantitativos y el informe maestro oficial en formato IEEE:

LD2_Arcila_Yactayo/
├── Informe_LD2_Arcila_Yactayo.pdf     -> Informe academico final (max. 20 paginas)
├── README.txt                         -> Este archivo de instrucciones y guia de ejecucion
├── verificacion_modelos.txt           -> Reporte de inspeccion y parametros BSIM4 (.lib)
├── trazabilidad_figuras.txt           -> Mapeo biunivoco Figura -> Circuito -> Script
│
├── ptm45hp.lib                        -> Modelo PTM 45nm HP (renombrado en raiz segun Sec. 12)
├── ptm45lp.lib                        -> Modelo PTM 45nm LP (renombrado en raiz segun Sec. 12)
├── ptm130.lib                         -> Modelo PTM 130nm Bulk (renombrado en raiz segun Sec. 12)
│
├── modelos/                           -> Biblioteca centralizada de modelos predictivos
│   ├── ptm45hp.lib                    -> Tarjeta BSIM4 High-Performance (Vdd = 1.0 V)
│   ├── ptm45lp.lib                    -> Tarjeta BSIM4 Low-Power (Vdd = 1.1 V)
│   ├── ptm130.lib                     -> Tarjeta BSIM4 130nm Bulk CMOS (Vdd = 1.3 V)
│   ├── ptm45hp_aux.lib                -> Tarjeta auxiliar para ensayo de ablacion GIDL
│   └── README_modelos.md              -> Descripcion tecnica de modelos PTM
│
├── act1/                              -> Actividad 1: Caracterizacion NAND3 y Comparacion Estatica
│   ├── README_act1.md                 -> Memoria tecnica de fases domino y consumo
│   ├── circuitos/                     -> Netlists ejecutables (.cir)
│   ├── resultados/logs/               -> Registros de medicion SPICE (.log)
│   ├── resultados/raw/                -> Formas de onda binarias transitorias (.raw)
│   ├── resultados/datos/              -> Metricas extraidas estructuradas (.json)
│   ├── scripts/                       -> Scripts generadores de figuras y metricas (.py)
│   └── figuras/                       -> Curvas transitorias generadas (.png)
│
├── act2/                              -> Actividad 2: Comparticion de Carga (Charge Sharing)
│   ├── README_act2.md                 -> Memoria tecnica de peor caso sincrono y mitigaciones
│   ├── prediccion_analitica_act2.md   -> Memoria de calculo analitico a priori de Delta V
│   ├── circuitos/                     -> Netlists SPICE con parametros AS/AD/PS/PD (.cir)
│   ├── resultados/logs/               -> Logs de simulacion (.log)
│   ├── resultados/raw/                -> Formas de onda transitorias (.raw)
│   ├── resultados/datos/              -> Metricas de barrido de CL y mitigaciones (.json)
│   ├── scripts/                       -> Scripts de evaluacion analitica y figuras (.py)
│   └── figuras/                       -> Formas de onda y comparativas analiticas (.png)
│
├── act3/                              -> Actividad 3: Fugas, Retencion y Keeper
│   ├── README_act3.md                 -> Memoria tecnica de keeper, retencion y contencion
│   ├── circuitos/                     -> Netlists de retencion, contencion y tri-nodo (.cir)
│   ├── resultados/logs/               -> Logs a 27°C y 85°C (.log)
│   ├── resultados/raw/                -> Formas de onda transitorias en 1.0 us (.raw)
│   ├── resultados/datos/              -> Metricas consolidadas de contencion y retencion (.json)
│   ├── scripts/                       -> Scripts generadores de figuras tri-nodo y viabilidad
│   └── figuras/                       -> Curvas de retencion, contencion y compromiso (.png)
│
├── act4/                              -> Actividad 4: Monotonicidad y Skew de Reloj en Cascada
│   ├── README_act4.md                 -> Memoria tecnica de monotonicidad y skew dominó
│   ├── circuitos/                     -> Netlists de cascada dominó de 2 y 3 etapas (.cir)
│   ├── resultados/logs/               -> Logs de medicion de retardos y corrientes (.log)
│   ├── resultados/raw/                -> Formas de onda de cascada y pulso descendente (.raw)
│   ├── resultados/datos/              -> Metricas de skew y comparativa footed/unfooted (.json)
│   ├── scripts/                       -> Script generador de graficas de cascada (.py)
│   └── figuras/                       -> Formas de onda y curvas de skew (.png)
│
├── act5/                              -> Actividad 5: Regimen NTV, Feedthrough y Escalado
│   ├── README_act5.md                 -> Memoria tecnica de operacion NTV y feedthrough
│   ├── circuitos/                     -> Netlists de evaluacion NTV (0.35 V a 1.0 V) (.cir)
│   ├── resultados/logs/               -> Logs con mediciones de teval, thold, fmax, fmin (.log)
│   ├── resultados/raw/                -> Formas de onda transitorias y energia (.raw)
│   ├── resultados/datos/              -> Metricas de conmutacion y ventana de frecuencia (.json)
│   ├── scripts/                       -> Script generador de ventanas de frecuencia y energia (.py)
│   └── figuras/                       -> Graficas de feedthrough y ventana operable (.png)
│
└── act6/                              -> Actividad 6: Opcional (No desarrollada)
    └── README.txt                     -> Nota indicativa formal

------------------------------------------------------------------------------
2. PROGRAMA UTILIZADO Y REQUISITOS DEL ENTORNO
------------------------------------------------------------------------------
- Simulador SPICE: Analog Devices LTspice (R) para Windows (64-bit).
- Modelos de Transistores: Predictive Technology Model (PTM) BSIM4 Level 54.
- Entorno de Post-Procesamiento: Python 3.10+ con librerias cientificas:
  matplotlib, numpy, scipy.

------------------------------------------------------------------------------
3. INSTRUCCIONES DE EJECUCION DE LOS CIRCUITOS SPICE
------------------------------------------------------------------------------
Todos los circuitos fueron concebidos con rutas relativas estandarizadas:
    .include ../../modelos/ptm45hp.lib
    .include ../../modelos/ptm45lp.lib
    .include ../../modelos/ptm130.lib

A. Modo Grafico (GUI):
   1. Abrir LTspice en Windows.
   2. Seleccionar File -> Open...
   3. Navegar hacia la carpeta actX/circuitos/ y seleccionar el netlist .cir deseado.
   4. Presionar el boton Run (icono del corredor) en la barra de herramientas.
   5. Seleccionar los nodos a graficar (ej. V(clk), V(dyn), V(out)) o consultar
      las mediciones cuantitativas en View -> SPICE Error Log (Ctrl+L).

B. Modo Consola (Batch Silencioso):
   Desde la linea de comandos (PowerShell / CMD), ejecutar:
   & "<Ruta_LTspice>\LTspice.exe" -b act1\circuitos\nand3_dinamica_base.cir
   Esto generara directamente el archivo .log con todas las sentencias .meas y
   el archivo .raw con las formas de onda completas.

------------------------------------------------------------------------------
4. REGENERACION DE FIGURAS DEL INFORME
------------------------------------------------------------------------------
Para regenerar las graficas cientificas presentadas en el documento maestro:
- Actividad 1: python act1/scripts/generar_figuras_act1.py
- Actividad 2: python act2/scripts/generar_figuras_act2.py
- Actividad 3:
    python act3/scripts/generar_figura8_editorial.py
    python act3/scripts/regenerar_figura_consolidacion.py
- Actividad 4: python act4/scripts/generar_figuras_act4.py
- Actividad 5: python act5/scripts/generar_figuras_act5.py

Las figuras generadas se guardan automaticamente en sus respectivas carpetas
actX/figuras/ con una resolucion optima de 300 DPI y ejes plenamente rotulados.

------------------------------------------------------------------------------
5. NOTA SOBRE FORMATO DE ARCHIVOS: NETLISTS .CIR FRENTE A .ASC
------------------------------------------------------------------------------
La Seccion 12 de la guia solicita que cada figura indique el nombre del archivo
.asc generador. Se precisa formalmente que, debido al nivel de profundidad y rigor
fisico requerido para el modelado BSIM4 sub-45nm (donde resulta mandatario incluir
parametros de difusion geometricos AS/AD/PS/PD en cada terminal, tolerancias de
conductancia gmin=1e-15 y abstol=1e-14, asi como complejas sentencias de medicion
en cascada), este proyecto implementa la totalidad de sus diseños mediante
netlists SPICE puros (.cir).

LTspice admite, reconoce y ejecuta de forma nativa los archivos .cir con total
compatibilidad funcional. El documento auxiliar trazabilidad_figuras.txt
establece la correspondencia exacta entre cada figura del informe academico y su
netlist .cir asociado.

------------------------------------------------------------------------------
6. ESTADO DE LA ACTIVIDAD 6 (OPCIONAL)
------------------------------------------------------------------------------
Conforme a la estructura solicitada en la Seccion 12, la carpeta act6/ se
encuentra incluida. La Actividad 6 ("Lógica CMOS Dinámica Multietapa Compleja"),
siendo de caracter opcional (+2 puntos), no fue desarrollada, focalizando el
esfuerzo integro del equipo en la conciliacion matematica rigurosa, medicion
experimental sin keepers ideales y optimizacion editorial de las Actividades 1 a 5.

==============================================================================
Fin del archivo README.txt
==============================================================================
