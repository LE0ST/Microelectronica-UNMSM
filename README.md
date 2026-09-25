# Microelectrónica y Sistemas Nanoelectrónicos (UNMSM – FIEE)

Repositorio de prácticas de laboratorio, simulaciones físicas SPICE e informes técnicos para el curso de **Microelectrónica y Sistemas Nanoelectrónicos**, Universidad Nacional Mayor de San Marcos (Facultad de Ingeniería Electrónica y Eléctrica).

* **Docente:** MsC. Luz Adanaqué Infante
* **Integrantes:**
  * **Leonardo Sait Yactayo Tolentino** (Código: 23190214)
  * **Marco Antonio Arcila Santander** (Código: 23190140)
* **Semestre:** 2026-II
* **Horario:** Lunes 18:00 – 20:00

---

## Estructura General del Repositorio

```
MicroNano/
│
├── AGENTS.md                                   # Context Engineering y reglas operativas para agentes IA
├── CLAUDE.md                                   # Guía de interoperabilidad para Claude Code
│
├── _docs/                                      # Documentación viva del proyecto
│   ├── process.md                              # Protocolo de simulación, post-procesamiento y QA
│   └── plan.md                                 # Hoja de ruta del curso y seguimiento de entregables
│
├── Semana_01/                                  # Introducción e Inversor CMOS básico
│   ├── Teoria/                                 # Diapositivas y material introductorio
│   └── Practica_Inversor_NOT/                  # Esquemáticos y netlist inicial
│
├── Semana_02/                                  # Guía oficial y fundamentos de LD1
│   ├── Teoria_y_Lecturas/                      # Diapositivas y lecturas (Thick/Thin Films)
│   ├── Guia_Oficial_LD1/                       # Guía docente oficial en PDF
│   └── Material_Adicional_Semestre/            # Rúbricas y referencias de laboratorio
│
├── Semana_03/                                  # Modelamiento CMOS y Lógica Estática
│   ├── Teoria_y_Lecturas/                      # Diapositivas y lecturas complementarias
│   └── Ejercicios/                             # Guía de ejercicios CMOS y resolución analítica
│
├── Semana_04/                                  # Lógica CMOS Dinámica y Dominó
│   ├── Teoria_y_Lecturas/                      # Diapositivas de lógica dinámica y charge sharing
│   └── Guia_Oficial_LD2/                       # Guía oficial del Laboratorio Dirigido N.° 2
│
├── LD1_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 1 (Lógica CMOS Estática)
│   ├── informe_latex/                          # Código fuente LaTeX y documento maestro (12 páginas)
│   ├── simulaciones/                           # Netlists SPICE (A1 a A5: VTC, retardo, NAND/NOR, compleja, RO)
│   ├── modelos/                                # Tarjetas tecnológicas PTM BSIM4 (45nm, 90nm, 22nm)
│   ├── scripts/                                # Scripts de automatización en Python
│   └── README.md                               # Documentación específica de LD1
│
└── LD2_Arcila_Yactayo/                         # LABORATORIO DIRIGIDO N.° 2 (Lógica CMOS Dinámica)
    ├── informe_latex/                          # Código fuente LaTeX y documento maestro (20 páginas)
    │   └── main.pdf                            # PDF compilado final oficial
    ├── act1/                                   # Actividad 1: Caracterización NAND3 Dinámica vs Estática
    ├── act2/                                   # Actividad 2: Compartición de Carga (Charge Sharing)
    ├── act3/                                   # Actividad 3: Fugas, Retención y Keeper (45nm HP/LP, 130nm)
    ├── act4/                                   # Actividad 4: Monotonicidad y Skew de Reloj en Cascada
    ├── act5/                                   # Actividad 5: Régimen NTV, Feedthrough y Escalado Energético
    ├── act6/                                   # Actividad 6: Lógica Multietapa (Opcional, no desarrollada)
    ├── modelos/                                # Biblioteca centralizada PTM (45nm HP/LP, 130nm Bulk)
    ├── trazabilidad_figuras.txt                # Matriz biunívoca: Figuras -> Netlists -> Scripts
    ├── verificacion_modelos.txt                # Verificación física de parámetros BSIM4 Level 54
    └── README.md                               # Portada técnica detallada de LD2
```

---

## Laboratorios Desarrollados

### [Laboratorio Dirigido N.° 1: Lógica CMOS Estática](LD1_Arcila_Yactayo/)
* **Enfoque:** Caracterización estática y dinámica de celdas lógicas elementales y complejas en tecnología submicrométrica de 45 nm (PTM BSIM4), evaluando márgenes de ruido ($NM_H$, $NM_L$), retardo de propagación, esfuerzo lógico y compromiso velocidad/potencia entre procesos HP y LP.
* **Informe Maestro:** `LD1_Arcila_Yactayo/informe_latex/LD1.pdf` (12 páginas).
* **Ejecución SPICE (Modo Batch):**
  ```powershell
  & "LTspice.exe" -b .\LD1_Arcila_Yactayo\simulaciones\A1_Inversor_VTC\A1_VTC.cir
  ```
* **Generación de Figuras:**
  ```powershell
  python .\LD1_Arcila_Yactayo\scripts\generar_graficas.py
  ```

---

### [Laboratorio Dirigido N.° 2: Lógica CMOS Dinámica Submicrométrica](LD2_Arcila_Yactayo/)
* **Enfoque:** Análisis circuital, físico y cuantitativo de lógica CMOS dinámica y dominó en tecnologías nanométricas PTM BSIM4 (45 nm HP, 45 nm LP y 130 nm Bulk). Se investiga la reducción de capacitancia de entrada ($-42.4\%$), peor caso sincrónico de compartición de carga ($\Delta V_{dyn} = 164.29\text{ mV}$ con $C_L = 2.0\text{ fF}$) y sus técnicas de mitigación, compromiso de contención y ventana de viabilidad del *keeper* ($W_{kp} \in [10.5, 38.0]\text{ nm}$), regla de monotonicidad dominó ante entradas no monótonas, robustez frente al desfase de reloj (*skew*), amortiguación de *feedthrough* de reloj, y caracterización de la ventana de frecuencia operable y energía en régimen Near-Threshold Voltage ($V_{DD} \in [0.35, 1.00]\text{ V}$).
* **Informe Maestro Oficial:** [LD2_Arcila_Yactayo/informe_latex/main.pdf](LD2_Arcila_Yactayo/informe_latex/main.pdf) (20 páginas físicas exactas).
* **Ejecución SPICE (Modo Batch):**
  ```powershell
  & "LTspice.exe" -b .\LD2_Arcila_Yactayo\act1\circuitos\nand3_dinamica_base.cir
  & "LTspice.exe" -b .\LD2_Arcila_Yactayo\act2\circuitos\nand3_cs_g2b_piloto_cl2f.cir
  ```
* **Generación de Figuras Científicas (Python 3.10+):**
  ```powershell
  python .\LD2_Arcila_Yactayo\act1\scripts\generar_figuras_act1.py
  python .\LD2_Arcila_Yactayo\act2\scripts\generar_figuras_act2.py
  python .\LD2_Arcila_Yactayo\act3\scripts\generar_figura8_editorial.py
  python .\LD2_Arcila_Yactayo\act4\scripts\generar_figuras_act4.py
  python .\LD2_Arcila_Yactayo\act5\scripts\generar_figuras_act5.py
  ```

---

## Flujo de Trabajo y Control de Versiones (Git)

Para garantizar la integridad y trazabilidad del repositorio colaborativo:

1. **Sincronización inicial:**
   ```bash
   git fetch origin
   git status
   ```
2. **Preparación y verificación de cambios puntuales (evitar `git add .` indiscriminado):**
   ```bash
   # Inspeccionar archivos modificados
   git status --short

   # Agregar selectivamente únicamente los archivos académicos aprobados
   git add <ruta/al/archivo>

   # Verificar el área de preparación (staging)
   git diff --cached --stat
   ```
3. **Confirmación con mensajes convencionales estructurados:**
   ```bash
   git commit -m "feat(alcance): descripcion clara y tecnica en tiempo presente"
   ```
4. **Publicación en la rama correspondiente:**
   ```bash
   git push origin <nombre-de-rama>
   ```

> **Aviso de higiene del repositorio:** No realizar commit de archivos binarios pesados de simulación transitoria (`.raw`), archivos de volcado temporal (`.tmp`), ni paquetes comprimidos redundantes de entrega local (`.zip`).
