# Microelectrónica y Sistemas Nanoelectrónicos (UNMSM – FIEE)

Repositorio de prácticas de laboratorio, simulaciones SPICE e informes técnicos para el curso de **Microelectrónica**, Universidad Nacional Mayor de San Marcos (FIEE).

* **Docente:** MsC. Luz Adanaqué Infante
* **Integrantes:**
  * Arcila
  * Yactayo
* **Semestre:** 2026-II

---

## Estructura del Repositorio

```
MicroNano/
│
├── Semana_01/                                  # Introducción e Inversor CMOS básico
│   ├── Teoria/                                 # Diapositivas y material introductorio
│   └── Practica_Inversor_NOT/                  # Esquemáticos y netlist inicial
│
├── Semana_02/                                  # Documentación oficial de la Semana 2
│   ├── Teoria_y_Lecturas/                      # Diapositivas y lecturas (Thick/Thin Films)
│   ├── Guia_Oficial_LD1/                       # Guía en PDF y plantillas vírgenes
│   └── Material_Adicional_Semestre/            # Referencias de laboratorios avanzados
│
└── LD1_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 1 (Oficial)
    ├── informe_latex/                          # Código fuente LaTeX y figuras para el reporte
    │   ├── LD1.tex                             # Plantilla oficial con tablas y 20 preguntas resueltas
    │   └── figuras/                            # Gráficas en alta resolución con ejes rotulados
    ├── simulaciones/                           # Circuitos SPICE organizados por actividad
    │   ├── A1_Inversor_VTC/                    # Caracterización VTC y márgenes de ruido
    │   ├── A2_Retardo_Transitorio/             # Retardo vs carga (CL) y nodos (90nm, 45nm, 22nm)
    │   ├── A3_NAND2_NOR2/                      # Comparación de compuertas y esfuerzo lógico
    │   ├── A4_Compuerta_Compleja/              # Síntesis de Y = ~((A*B)+C)
    │   └── A5_Potencia_y_RO/                   # Fuga HP/LP y oscilador de anillo de 5 etapas
    ├── modelos/                                # Tarjetas PTM y librerías anti-colisión
    ├── scripts/                                # Automatización en Python para graficación
    └── simulaciones_LD1_Arcila_Yactayo.zip     # Paquete listo para entrega en aula virtual
```

---

## Laboratorio Dirigido N.° 1: Lógica CMOS Estática

* **Objetivo:** Caracterización estática y dinámica de celdas lógicas elementales y complejas en tecnología submicrométrica de 45 nm (PTM BSIM4), evaluando márgenes de ruido, retardo, esfuerzo lógico y compromiso velocidad/potencia entre procesos HP y LP.
* **Herramientas:** LTspice 24, Python 3.14 (`matplotlib`, `numpy`), LaTeX (Overleaf / TeXLive).

### Ejecución de Simulaciones

Para ejecutar una simulación en modo batch desde la consola:

```powershell
LTspice.exe -b -ascii .\LD1_Arcila_Yactayo\simulaciones\A1_Inversor_VTC\A1_VTC.cir
```

### Generación Automatizada de Figuras

```powershell
python .\LD1_Arcila_Yactayo\scripts\generar_graficas.py
```

---

## Flujo de Trabajo con Git

Para mantener el repositorio sincronizado entre ambos integrantes:

1. **Antes de empezar a trabajar:**
   ```bash
   git pull origin main
   ```
2. **Al terminar cambios o simulaciones:**
   ```bash
   git add .
   git commit -m "feat(LD1): descripcion clara del cambio"
   git push origin main
   ```
