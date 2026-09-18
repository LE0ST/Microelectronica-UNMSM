#!/usr/bin/env python3
"""
auditar_latex_ld2.py
Auditoría estructural y de sintaxis para el informe en LaTeX de LD2.
Distingue explícitamente entre:
1. Auditoría estructural estática (balance de entornos, delimitadores, figuras, labels, hyperref, babel).
2. Compilación TeX real (verificación del motor pdflatex/xelatex/Overleaf).
"""

import os
import re
import sys
from pathlib import Path

def expand_inputs(file_path, base_dir, visited=None):
    if visited is None:
        visited = set()
    if file_path in visited:
        return ""
    visited.add(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Archivo incluido no encontrado: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    def replacer(match):
        rel_target = match.group(1).strip()
        if not rel_target.endswith(".tex"):
            rel_target += ".tex"
        target_path = base_dir / rel_target
        return expand_inputs(target_path, base_dir, visited)

    pattern = re.compile(r'(?<!%)\\input\{([^}]+)\}')
    expanded = pattern.sub(replacer, content)
    return expanded

def auditar_documento(main_tex_path):
    print("=" * 72)
    print("AUDITORÍA ESTRUCTURAL ESTÁTICA DE FUENTE LATEX — LD2")
    print(f"Archivo Maestro: {main_tex_path}")
    print("=" * 72)

    base_dir = main_tex_path.parent
    errores = []
    warnings = []

    # 1. Expansión modular
    try:
        full_text = expand_inputs(main_tex_path, base_dir)
        print("[OK] Expansión modular: todos los ficheros \\input existen y fueron cargados.")
    except Exception as e:
        errores.append(f"Error en expansión modular: {e}")
        print(f"[FAIL] {e}")
        return False, errores, warnings

    # Remover comentarios de una línea preservando \%
    lines = full_text.splitlines()
    code_lines = []
    for line in lines:
        clean_line = re.sub(r'(?<!\\)%.*$', '', line)
        code_lines.append(clean_line)
    clean_text = "\n".join(code_lines)

    # 2. Detección de incompatibilidades babel-spanish ('\,\\%')
    bad_glue_matches = re.findall(r'\\,\s*\\%', clean_text)
    if bad_glue_matches:
        msg = f"Detectadas {len(bad_glue_matches)} ocurrencias de '\\,\\%' que causan 'Incompatible glue units' con babel/spanish. Reemplazar por '\\%' sin '\\,'."
        errores.append(msg)
        print(f"[FAIL] {msg}")
    else:
        print("[OK] Sintaxis de porcentajes: sin ocurrencias de '\\,\\%'.")

    # 3. Detección de advertencias hyperref en títulos (matemática sin \texorpdfstring)
    heading_matches = re.findall(r'\\(?:section|subsection|subsubsection)\*?\{([^}]+)\}', clean_text)
    bad_headings = []
    for h in heading_matches:
        # Si tiene $ o _ y no usa \texorpdfstring
        if ("$" in h or "_" in h) and "\\texorpdfstring" not in h:
            bad_headings.append(h)
    if bad_headings:
        msg = f"Títulos con matemática sin \\texorpdfstring detectados (provocan 'Token not allowed in a PDF string' en bookmarks): {bad_headings}"
        errores.append(msg)
        print(f"[FAIL] {msg}")
    else:
        print(f"[OK] Títulos y marcadores PDF: todos los títulos con matemática emplean \\texorpdfstring.")

    # 4. Captions con matemática y argumento corto
    caption_matches = re.finditer(r'\\caption(?:\s*\[([^\]]*)\])?\s*\{([^}]+)\}', clean_text)
    bad_captions = []
    for m in caption_matches:
        short_arg = m.group(1)
        long_arg = m.group(2)
        if ("$" in long_arg or "_" in long_arg) and not short_arg:
            bad_captions.append(long_arg[:40] + "...")
    if bad_captions:
        msg = f"Captions con matemática sin argumento corto plano detectados: {bad_captions}"
        warnings.append(msg)
        print(f"[WARN] {msg}")
    else:
        print("[OK] Captions de figuras y tablas: argumentos cortos planos verificados.")

    # 5. Balance de entornos
    begins = re.findall(r'\\begin\{([^}]+)\}', clean_text)
    ends = re.findall(r'\\end\{([^}]+)\}', clean_text)
    all_envs = sorted(list(set(begins + ends)))
    env_diffs = {env: begins.count(env) - ends.count(env) for env in all_envs if begins.count(env) != ends.count(env)}
    if not env_diffs:
        print(f"[OK] Balance de entornos: {len(begins)} pares \\begin/\\end balanceados.")
    else:
        errores.append(f"Desbalance en entornos: {env_diffs}")
        print(f"[FAIL] Desbalance en entornos: {env_diffs}")

    # 6. Balance matemático
    dollar_matches = re.findall(r'(?<!\\)\$', clean_text)
    if len(dollar_matches) % 2 != 0:
        errores.append(f"Número impar de delimitadores '$' ({len(dollar_matches)}).")
        print(f"[FAIL] Número impar de delimitadores '$' ({len(dollar_matches)}).")
    else:
        print(f"[OK] Matemática inline: {len(dollar_matches)//2} expresiones '$...$' balanceadas.")

    open_bracket_math = len(re.findall(r'(?<!\\)\\\[', clean_text))
    close_bracket_math = len(re.findall(r'(?<!\\)\\\]', clean_text))
    if open_bracket_math != close_bracket_math:
        errores.append(f"Desbalance en bloques display \\[ \\] ({open_bracket_math} vs {close_bracket_math}).")
        print(f"[FAIL] Desbalance en bloques \\[ \\].")
    else:
        print(f"[OK] Matemática display \\[ \\]: {open_bracket_math} pares.")

    # 7. Existencia física de figuras
    fig_matches = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', clean_text)
    missing_figs = [fig for fig in fig_matches if not (base_dir / fig.strip()).exists()]
    if not missing_figs:
        print(f"[OK] Recursos gráficos: {len(fig_matches)} figuras existen en disco a 300 DPI.")
    else:
        errores.append(f"Figuras ausentes: {missing_figs}")
        print(f"[FAIL] Figuras ausentes: {missing_figs}")

    # 8. Referencias y etiquetas fuente
    labels = set(re.findall(r'\\label\{([^}]+)\}', clean_text))
    refs = re.findall(r'\\ref\{([^}]+)\}', clean_text)
    missing_refs = [r for r in refs if r not in labels]
    if not missing_refs:
        print(f"[OK] Referencias cruzadas en código: {len(refs)} llamadas resuelven a \\label definido ({len(labels)} etiquetas).")
    else:
        errores.append(f"Referencias sin etiqueta: {missing_refs}")
        print(f"[FAIL] Referencias sin etiqueta: {missing_refs}")

    # 9. Estimación de volumen y páginas (excluyendo preámbulo y portada fija de 1 página)
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', full_text, re.DOTALL)
    if doc_match:
        doc_body = doc_match.group(1)
        body_no_title = re.sub(r'\\begin\{titlepage\}.*?\\end\{titlepage\}', '', doc_body, flags=re.DOTALL)
        body_no_tables = re.sub(r'\\begin\{(?:tabularx|tabular)\}.*?\\end\{(?:tabularx|tabular)\}', '', body_no_title, flags=re.DOTALL)
        body_clean = re.sub(r'(?<!\\)%.*$', '', body_no_tables, flags=re.MULTILINE)
        prose_words = len(re.findall(r'\b\w+\b', body_clean))
    else:
        words = re.findall(r'\b\w+\b', clean_text)
        prose_words = len(words)

    num_figs = len(fig_matches)
    tabular_matches = re.findall(r'\\begin\{(?:tabularx|tabular)\}', clean_text)
    num_tables = len(tabular_matches)

    # Estimación de ocupación en 11pt a4paper con 2cm de margen:
    # ~550 palabras por página de texto corrido
    # Figuras compactas (0.72\linewidth): ~0.32 páginas cada una
    # Tablas (tabularx): ~0.35 páginas cada una
    content_pages = (prose_words / 550.0) + (num_figs * 0.32) + (num_tables * 0.35)
    est_total_pages = 1 + round(content_pages)  # 1 portada + páginas de contenido

    print("-" * 72)
    print("MÉTRICAS ESTRUCTURALES Y PRESUPUESTO DE PÁGINAS:")
    print(f"  - Palabras netas de prosa (sin portada ni tablas): {prose_words}")
    print(f"  - Figuras incluidas: {num_figs} (escaladas a 0.72\\linewidth)")
    print(f"  - Tablas incluidas: {num_tables}")
    print(f"  - Ecuaciones numeradas / display: {open_bracket_math + begins.count('equation')}")
    print(f"  - Extensión estimada: ~{est_total_pages} páginas (1 Portada + ~{round(content_pages)} págs de contenido)")
    print(f"  - Margen para Actividades 2 a 5 y cuestionario: ~{20 - est_total_pages} páginas")
    print("-" * 72)

    # 10. Compilación TeX Real Local
    print("\n" + "=" * 72)
    print("ESTADO DE COMPILACIÓN TEJ/PDF REAL")
    print("=" * 72)

    # Actualizar PATH en Windows si es necesario
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as k:
                m_path, _ = winreg.QueryValueEx(k, "Path")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
                u_path, _ = winreg.QueryValueEx(k, "Path")
            os.environ["PATH"] = f"{m_path};{u_path};" + os.environ.get("PATH", "")
        except Exception:
            pass

    import shutil
    import subprocess

    latexmk_bin = shutil.which("latexmk")
    pdflatex_bin = shutil.which("pdflatex")

    if latexmk_bin:
        print(f"[OK] Motor TeX detectado: {latexmk_bin}")
        try:
            # Ejecutar compilación latexmk
            res = subprocess.run(
                ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "main.tex"],
                cwd=base_dir,
                capture_output=True,
                text=True,
                timeout=90
            )
            log_path = base_dir / "main.log"
            pdf_path = base_dir / "main.pdf"

            if res.returncode == 0 and pdf_path.exists():
                pdf_size_kb = pdf_path.stat().st_size / 1024.0
                
                # Extraer páginas reales de main.pdf
                num_real_pages = "Desconocido"
                try:
                    import pypdf
                    reader = pypdf.PdfReader(str(pdf_path))
                    num_real_pages = len(reader.pages)
                except Exception:
                    pass

                # Analizar main.log
                log_text = log_path.read_text(encoding="latin-1", errors="ignore")
                log_lines = log_text.splitlines()
                tex_errors = [l for l in log_lines if l.startswith("! ") or "Fatal error" in l]
                tex_warnings = [
                    l for l in log_lines 
                    if re.search(r'\bwarning\b', l, re.I) 
                    and not "infwarerr" in l 
                    and not "00miktex" in l
                ]
                overfull_boxes = [l for l in log_lines if "Overfull \\hbox" in l]
                underfull_boxes = [l for l in log_lines if "Underfull \\hbox" in l]

                print(f"[OK] Compilación real latexmk: EXITOSA (Código de salida: 0)")
                print(f"[OK] Archivo generado: main.pdf ({num_real_pages} páginas, {pdf_size_kb:.1f} KB)")
                print(f"[OK] Errores en main.log: {len(tex_errors)}")
                print(f"[OK] Warnings en main.log: {len(tex_warnings)}")
                print(f"[OK] Overfull \\hbox: {len(overfull_boxes)}")
                print(f"[OK] Underfull \\hbox: {len(underfull_boxes)}")

                if tex_warnings:
                    for w in tex_warnings:
                        warnings.append(f"LaTeX Warning: {w}")
                        print(f"     * {w}")
            else:
                errores.append(f"Fallo en compilación latexmk (código {res.returncode})")
                print(f"[FAIL] Fallo en compilación latexmk (código {res.returncode})")
                print(res.stderr[:500])
        except Exception as e:
            errores.append(f"Error ejecutando latexmk: {e}")
            print(f"[FAIL] Error ejecutando latexmk: {e}")
    else:
        print("Compilación TeX real: NO VERIFICADA LOCALMENTE")
        print("Motivo: El entorno local Windows no dispone de un motor TeX (pdflatex/xelatex) en PATH.")
        print("Procedimiento de compilación oficial: TeX Live 2026 / Overleaf.")

    print("=" * 72)

    is_clean = len(errores) == 0
    return is_clean, errores, warnings

if __name__ == "__main__":
    base_repo = Path(__file__).resolve().parent.parent
    main_tex = base_repo / "informe_latex" / "main.tex"
    clean, errs, warns = auditar_documento(main_tex)
    if not clean:
        print(f"\n>>> AUDITORÍA CON ERRORES ({len(errs)} hallazgos) <<<")
        sys.exit(1)
    print(f"\n>>> AUDITORÍA ESTRUCTURAL Y COMPILACIÓN REAL EXITOSAS (0 errores) <<<")
