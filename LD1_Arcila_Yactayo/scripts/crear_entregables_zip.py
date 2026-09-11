"""
Script para generar los archivos .zip entregables del Laboratorio Dirigido N.° 1 (LD1):
1. LD1_Arcila_Yactayo.zip : Paquete integral con informe PDF, LaTeX, esquemas, netlists, modelos y scripts.
2. simulaciones_LD1_Arcila_Yactayo.zip : Paquete de simulaciones puras (netlists, logs, modelos) segun requerimiento de la guia.
"""

import os
import sys
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = BASE_DIR.parent

README_TEXT = """================================================================================
UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS (UNMSM)
Facultad de Ingeniería Electrónica y Eléctrica (FIEE)
Curso: Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)
Docente: MsC. Luz Adanaqué Infante

ENTREGABLE OFICIAL: LABORATORIO DIRIGIDO N.° 1 (LD1)
TÍTULO: Lógica CMOS Estática: VTC, Retardo Transitorio, Compuertas y Fuga
================================================================================

AUTORES:
- Leonardo Sait Yactayo Tolentino (Código: 23190214)
- Marco Antonio Arcila Santander   (Código: 23190140)

FECHA DE ENTREGA: 11 de setiembre de 2026

--------------------------------------------------------------------------------
1. ESTRUCTURA DEL PAQUETE ENTREGABLE
--------------------------------------------------------------------------------
El presente paquete contiene la totalidad de los archivos de simulación, modelos,
código de post-procesamiento y el informe técnico final en formato PDF (12 páginas)
y código fuente LaTeX:

├── LD1_Arcila_Yactayo.pdf               # Informe maestro final en formato PDF (12 páginas)
├── LEAME_ENTREGA.txt                    # Guía y documentación del entregable
│
├── informe_latex/                       # Código fuente LaTeX y figuras de alta resolución
│   ├── LD1.tex                          # Archivo maestro LaTeX (.tex)
│   ├── LD1_Arcila_Yactayo.pdf          # Copia del informe final en PDF
│   └── figuras/                         # Gráficas científicas a 300 DPI (Fig. 1 a 8)
│       ├── fig1_vtc_familia.png
│       ├── fig1_cursores_ltspice.png
│       ├── fig2_tp_vs_cl.png
│       ├── fig2_comparativa_nodos.png
│       ├── fig3_transitorio_compleja.png
│       ├── fig4_oscilador_anillo.png
│       ├── fig_esquema_inversor.png
│       └── fig_esquema_compleja.png
│
├── simulaciones/                        # Netlists SPICE organizados por actividad
│   ├── A1_Inversor_VTC/                 # Actividad 1: Barrido de beta y márgenes de ruido
│   │   ├── A1_VTC.cir                   # Netlist nominal 45nm HP (beta 1.0 a 3.0)
│   │   ├── A1_VTC.log                   # Registro de simulación (.meas)
│   │   ├── A1_LP_VTC.cir                # Netlist proceso 45nm LP
│   │   ├── A1_LP_VTC.log                # Registro LP
│   │   ├── 45nm_HP.pm                   # Modelo PTM 45nm HP
│   │   ├── 45nm_LP.pm                   # Modelo PTM 45nm LP
│   │   └── capturas_cursores/           # Capturas de cursores LTspice
│   │
│   ├── A2_Retardo_Transitorio/          # Actividad 2: Retardo vs CL y escalamiento
│   │   ├── A2_Transient.cir             # Barrido CL = 1fF a 8fF en 45nm HP (beta = 2.5)
│   │   ├── A2_Transient.log             # Registro con mediciones tpHL, tpLH, tp
│   │   ├── A2_22nm.cir                  # Nodo 22nm HP (VDD = 0.8 V)
│   │   ├── A2_22nm.log                  # Registro 22nm HP
│   │   ├── A2_45nm.cir                  # Nodo 45nm HP (VDD = 1.0 V)
│   │   ├── A2_45nm.log                  # Registro 45nm HP
│   │   ├── A2_90nm.cir                  # Nodo 90nm bulk (VDD = 1.2 V)
│   │   ├── A2_90nm.log                  # Registro 90nm bulk
│   │   ├── 22nm_HP.pm
│   │   ├── 45nm_HP.pm
│   │   └── 90nm_bulk.pm
│   │
│   ├── A3_NAND2_NOR2/                   # Actividad 3: NAND2 vs NOR2 y esfuerzo lógico
│   │   ├── NAND2_ext.cir                # Entrada A (externa) conmutando
│   │   ├── NAND2_ext.log
│   │   ├── NAND2_int.cir                # Entrada B (interna) conmutando
│   │   ├── NAND2_int.log
│   │   ├── NOR2_single.cir              # Entrada única conmutando
│   │   ├── NOR2_single.log
│   │   ├── NOR2_both.cir                # Ambas entradas en paralelo
│   │   ├── NOR2_both.log
│   │   └── 45nm_HP.pm
│   │
│   ├── A4_Compuerta_Compleja/           # Actividad 4: Síntesis AOI21 (6T)
│   │   ├── A4_ComplexGate.cir           # Y = ~((A*B)+C), beta = 2.0
│   │   ├── A4_ComplexGate.log           # Peor caso de retardo transitorio
│   │   └── 45nm_HP.pm
│   │
│   └── A5_Potencia_y_RO/                # Actividad 5: Potencia, fuga y oscilador de anillo
│       ├── A5_Leak_HP.cir               # Corrientes de fuga en reposo 45nm HP
│       ├── A5_Leak_HP.log
│       ├── A5_Leak_LP.cir               # Corrientes de fuga en reposo 45nm LP
│       ├── A5_Leak_LP.log
│       ├── A5_RO_HP.cir                 # Oscilador de anillo 5 etapas 45nm HP
│       ├── A5_RO_HP.log                 # fosc = 21.94 GHz, tpd = 4.56 ps
│       ├── A5_RO_LP.cir                 # Oscilador de anillo 5 etapas 45nm LP
│       ├── A5_RO_LP.log                 # fosc = 6.25 GHz, tpd = 15.99 ps
│       ├── 45nm_HP.pm
│       └── 45nm_LP.pm
│
├── modelos/                             # Tarjetas PTM oficiales (BSIM4) y librerías
│   ├── 130nm_bulk.pm
│   ├── 180nm_bulk.txt
│   ├── 22nm_HP.pm
│   ├── 22nm_LP.pm
│   ├── 32nm_HP.pm
│   ├── 32nm_LP.pm
│   ├── 45nm_HP.pm
│   ├── 45nm_HP_ren.lib                  # Librería renombrada anti-colisión
│   ├── 45nm_LP.pm
│   ├── 45nm_LP_ren.lib                  # Librería renombrada anti-colisión
│   ├── 65nm_bulk.pm
│   └── 90nm_bulk.pm
│
└── scripts/                             # Automatización analítica en Python
    ├── generar_graficas.py              # Generación masiva de curvas
    ├── generar_bloque_cursores.py       # Mosaico de cursores LTspice (Fig. 1)
    ├── generar_comparativa_nodos.py     # Transitorio multitecnología (Fig. 2)
    ├── generar_esquema_inversor.py      # Diagrama circuital inversor
    ├── generar_esquema_compleja.py      # Topología AOI21 y dimensionamiento
    ├── generar_fig2.py                  # Regresión tp vs CL
    ├── generar_fig3.py                  # Verificación funcional compuerta compleja
    └── crear_entregables_zip.py         # Generador de este paquete ZIP

--------------------------------------------------------------------------------
2. INSTRUCCIONES DE REPRODUCCIÓN (LTSPICE EN WINDOWS)
--------------------------------------------------------------------------------
Para reproducir cualquier simulación en modo batch (silencioso):
  & "G:\\LTspice\\LTspice.exe" -b "<ruta_al_archivo>.cir"

Para examinar las directivas de medición automática (.meas):
  Abrir el archivo .log generado tras la simulación (o Ctrl+L en la GUI de LTspice).

--------------------------------------------------------------------------------
3. INSTRUCCIONES DE POST-PROCESAMIENTO (PYTHON 3)
--------------------------------------------------------------------------------
Todos los scripts emplean bibliotecas estándar (matplotlib, numpy):
  python scripts/generar_graficas.py

Las figuras generadas se guardan automáticamente con resolución de 300 DPI
en la subcarpeta 'informe_latex/figuras/'.
================================================================================
"""

EXCLUDE_EXTS = {'.raw', '.op.raw', '.db', '.tmp', '.bak', '.pyc'}
EXCLUDE_DIRS = {'__pycache__', '.git', '.vscode', '.idea', 'borradores_iniciales'}

def should_include_file(p: Path) -> bool:
    if p.name.startswith('.'):
        return False
    # Check extensions
    ext = p.suffix.lower()
    if ext in EXCLUDE_EXTS:
        return False
    if p.name.endswith('.log.raw'):
        return False
    # Check parts
    for part in p.parts:
        if part in EXCLUDE_DIRS:
            return False
    return True

def build_full_zip():
    zip_path = BASE_DIR / "LD1_Arcila_Yactayo.zip"
    print(f"Construyendo paquete maestro: {zip_path.name}...")
    
    # Escribir LEAME_ENTREGA.txt
    readme_path = BASE_DIR / "LEAME_ENTREGA.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(README_TEXT.strip() + "\n")
    print("  -> Creado LEAME_ENTREGA.txt")

    included_files = []
    
    # 1. Archivos directos en LD1_Arcila_Yactayo/
    for direct_file in ["LD1_Arcila_Yactayo.pdf", "LEAME_ENTREGA.txt"]:
        fp = BASE_DIR / direct_file
        if fp.exists():
            included_files.append((fp, f"LD1_Arcila_Yactayo/{direct_file}"))

    # 2. informe_latex/
    latex_dir = BASE_DIR / "informe_latex"
    if latex_dir.exists():
        for root, dirs, files in os.walk(latex_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                if should_include_file(fp):
                    rel = fp.relative_to(BASE_DIR)
                    included_files.append((fp, f"LD1_Arcila_Yactayo/{rel.as_posix()}"))

    # 3. simulaciones/
    sim_dir = BASE_DIR / "simulaciones"
    if sim_dir.exists():
        for root, dirs, files in os.walk(sim_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                if should_include_file(fp):
                    rel = fp.relative_to(BASE_DIR)
                    included_files.append((fp, f"LD1_Arcila_Yactayo/{rel.as_posix()}"))

    # 4. modelos/
    mod_dir = BASE_DIR / "modelos"
    if mod_dir.exists():
        for root, dirs, files in os.walk(mod_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                if should_include_file(fp):
                    rel = fp.relative_to(BASE_DIR)
                    included_files.append((fp, f"LD1_Arcila_Yactayo/{rel.as_posix()}"))

    # 5. scripts/
    scr_dir = BASE_DIR / "scripts"
    if scr_dir.exists():
        for root, dirs, files in os.walk(scr_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                if should_include_file(fp):
                    rel = fp.relative_to(BASE_DIR)
                    included_files.append((fp, f"LD1_Arcila_Yactayo/{rel.as_posix()}"))

    # Escribir zip con compresión DEFLATED nivel 9
    total_uncompressed = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for fp, arcname in included_files:
            z.write(fp, arcname)
            total_uncompressed += fp.stat().st_size

    zip_size = zip_path.stat().st_size
    ratio = (1 - zip_size / total_uncompressed) * 100 if total_uncompressed else 0
    print(f"  OK: {len(included_files)} archivos incluidos.")
    print(f"  Tamano descomprimido: {total_uncompressed / 1024 / 1024:.2f} MB")
    print(f"  Tamano comprimido (.zip): {zip_size / 1024 / 1024:.2f} MB (Ahorro: {ratio:.1f}%)\n")


def build_simulations_zip():
    zip_path = BASE_DIR / "simulaciones_LD1_Arcila_Yactayo.zip"
    print(f"Construyendo paquete de simulaciones: {zip_path.name}...")

    included_files = []
    
    # 1. simulaciones/
    sim_dir = BASE_DIR / "simulaciones"
    if sim_dir.exists():
        for root, dirs, files in os.walk(sim_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                if should_include_file(fp):
                    rel = fp.relative_to(BASE_DIR)
                    included_files.append((fp, rel.as_posix()))

    # 2. modelos/
    mod_dir = BASE_DIR / "modelos"
    if mod_dir.exists():
        for root, dirs, files in os.walk(mod_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                fp = Path(root) / f
                if should_include_file(fp):
                    rel = fp.relative_to(BASE_DIR)
                    included_files.append((fp, rel.as_posix()))

    total_uncompressed = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for fp, arcname in included_files:
            z.write(fp, arcname)
            total_uncompressed += fp.stat().st_size

    zip_size = zip_path.stat().st_size
    ratio = (1 - zip_size / total_uncompressed) * 100 if total_uncompressed else 0
    print(f"  OK: {len(included_files)} archivos incluidos.")
    print(f"  Tamano descomprimido: {total_uncompressed / 1024 / 1024:.2f} MB")
    print(f"  Tamano comprimido (.zip): {zip_size / 1024 / 1024:.2f} MB (Ahorro: {ratio:.1f}%)\n")


if __name__ == "__main__":
    build_full_zip()
    build_simulations_zip()
    print("Todos los paquetes entregables han sido creados satisfactoriamente.")
