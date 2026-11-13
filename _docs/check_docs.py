#!/usr/bin/env python3
"""
Reproducible documentation & traceability validator for Microelectronica-UNMSM.

`git ls-files` is the single source of truth: a link target is valid only if it is
tracked by Git (a file that merely exists on disk but is excluded from Git is NOT valid).
Fenced code blocks and inline code spans are ignored, so local dependencies documented
as plain text (e.g. `Semana_07/.../LabDirigidoNro03.pdf`) are never treated as public links.

Usage (from repository root):  python _docs/check_docs.py
Exit code 0 = all checks passed, 1 = at least one error.
"""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
import sys

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_RE = re.compile(r"""<(?:img|a)\b[^>]*?\b(?:src|href)=["']([^"']+)["']""", re.I)
REF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.M)
FENCE = "`" * 3


def get_tracked_files() -> set[str]:
    out = subprocess.check_output(["git", "ls-files"], text=True, encoding="utf-8")
    return {line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()}


def get_tracked_dirs(tracked: set[str]) -> set[str]:
    dirs: set[str] = {"", "."}
    for f in tracked:
        parts = f.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))
    return dirs


def scan_text(md: str, text: str, tracked: set[str], tracked_dirs: set[str]) -> list[str]:
    """Check one Markdown document (links, images, HTML img/a, reference links, file: URIs)."""
    errors: list[str] = []
    md_dir = posixpath.dirname(md)
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(FENCE):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        clean = re.sub(r"`[^`]*`", "", line)  # drop inline code spans
        targets = LINK_RE.findall(clean) + HTML_RE.findall(clean) + REF_RE.findall(clean)
        for raw_t in targets:
            parts = raw_t.strip().strip("<>").split()
            target = parts[0] if parts else ""
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.lower().startswith("file:"):
                errors.append(f"[FILE_URI] {md}:{lineno}: '{target}'")
                continue
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            resolved = posixpath.normpath(posixpath.join(md_dir, path_part)).rstrip("/")
            if resolved not in tracked and resolved not in tracked_dirs:
                errors.append(
                    f"[BROKEN_LINK] {md}:{lineno}: '{target}' -> '{resolved}' not in git ls-files"
                )
    return errors


def check_markdown_links(md_files: list[str], tracked: set[str], tracked_dirs: set[str]) -> list[str]:
    errors: list[str] = []
    for md in md_files:
        with open(md, encoding="utf-8", errors="replace") as fh:
            errors.extend(scan_text(md, fh.read(), tracked, tracked_dirs))
    return errors


def self_test(tracked: set[str], tracked_dirs: set[str]) -> list[str]:
    """Negative/positive tests on in-memory text only; no document is modified."""
    fails: list[str] = []
    cases = [
        ("[x](file:///g:/Proyectos/a.md)", 1, "file:/// URI"),
        ("[x](nonexistent_file.md)", 1, "missing file"),
        ("![fig](figuras/no_existe.png)", 1, "missing image"),
        ("[x](LD3_Yactayo/tablas/tabla_resultados_exp01_exp05.md)", 1,
         "file present on disk but excluded from Git"),
        ('<img src="figuras/no_existe.png">', 1, "missing HTML image"),
        ("[ref]: missing_ref_target.md", 1, "missing reference-style link"),
        ("`Semana_07/Guia/LabDirigidoNro03.pdf` is a documented local dependency", 0,
         "plain-text local path must not be flagged"),
        ("[ok](README.md)", 0, "valid tracked link must not be flagged"),
    ]
    for text, expected, label in cases:
        got = len(scan_text("x.md", text, tracked, tracked_dirs))
        if got != expected:
            fails.append(f"[SELFTEST] {label}: expected {expected} error(s), got {got}")
    return fails


def check_private_references(md_files: list[str]) -> list[str]:
    """Warn about Windows drive paths in prose (historical bitacora is exempt)."""
    warnings: list[str] = []
    pat = re.compile(r"(?<![A-Za-z])([A-Za-z]:\\[^\s`'\")]+|[A-Za-z]:/[^\s`'\")]+)")
    for md in md_files:
        if md == "_docs/bitacora.md":
            continue
        with open(md, encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh.read().splitlines(), 1):
                for m in pat.finditer(line):
                    warnings.append(f"[LOCAL_PATH] {md}:{lineno}: '{m.group(1)}'")
    return warnings


def check_traceability_and_authorship(tracked: set[str]) -> list[str]:
    errors: list[str] = []
    if "LD3_Yactayo/tablas/tabla_resultados_exp01_exp05.md" in tracked:
        errors.append("[TRACKING] preliminary LD3 table is still tracked in Git")

    with open("LD3_Yactayo/TRAZABILIDAD.md", encoding="utf-8") as fh:
        traz = fh.read()
    cite = re.compile(
        r"`((?:esquemas|simulaciones/netlists|validation/cases|scripts|figuras|tablas|informe|presentacion)"
        r"/[^`]+\.(?:asc|cir|py|png|md|pdf))`"
    )
    for m in cite.finditer(traz):
        rel = f"LD3_Yactayo/{m.group(1)}"
        if rel not in tracked:
            errors.append(f"[LD3_TRACE] TRAZABILIDAD.md cites '{rel}' which is not in git ls-files")

    for p in ["LD1_Arcila_Yactayo/README.md", "LD2_Arcila_Yactayo/README.md"]:
        txt = open(p, encoding="utf-8").read()
        if "Leonardo" not in txt or "Marco" not in txt:
            errors.append(f"[AUTHORSHIP] {p} missing shared authorship (Leonardo & Marco)")
    for n in range(1, 6):
        p = f"LD2_Arcila_Yactayo/act{n}/README_act{n}.md"
        txt = open(p, encoding="utf-8").read()
        if "Leonardo Sait Yactayo Tolentino" not in txt or "Marco Antonio Arcila Santander" not in txt:
            errors.append(f"[AUTHORSHIP] {p} missing shared authorship")
    for p in ["LD3_Yactayo/README.md", "LD3_Yactayo/TRAZABILIDAD.md"]:
        txt = open(p, encoding="utf-8").read()
        if "Leonardo Sait Yactayo Tolentino" not in txt:
            errors.append(f"[AUTHORSHIP] {p} missing individual author")
        if "Marco Antonio" in txt or "Marco Arcila" in txt:
            errors.append(f"[AUTHORSHIP] {p} mentions Marco in an individual LD3 document")

    act6 = open("LD2_Arcila_Yactayo/act6/README.txt", encoding="utf-8").read().lower()
    if "opcional" not in act6 or "no desarrollada" not in act6:
        errors.append("[LD2_ACT6] act6/README.txt must state optional / not developed")
    ld2 = open("LD2_Arcila_Yactayo/README.md", encoding="utf-8").read()
    if "act6/README.txt" not in ld2:
        errors.append("[LD2_ACT6] LD2 README does not link act6/README.txt")
    return errors


def main() -> int:
    tracked = get_tracked_files()
    tracked_dirs = get_tracked_dirs(tracked)
    md_files = sorted(f for f in tracked if f.endswith(".md"))
    print(f"Tracked files in Git: {len(tracked)}")
    print(f"Tracked Markdown files checked: {len(md_files)}")

    link_errors = check_markdown_links(md_files, tracked, tracked_dirs)
    local_warnings = check_private_references(md_files)
    other_errors = check_traceability_and_authorship(tracked) + self_test(tracked, tracked_dirs)

    for title, items in (("LINK ERRORS", link_errors), ("LOCAL PATH WARNINGS", local_warnings),
                         ("TRACEABILITY / AUTHORSHIP / SELF-TEST ERRORS", other_errors)):
        if items:
            print(f"\n--- {title} ---")
            for it in items:
                print(" ", it)

    total = len(link_errors) + len(other_errors)
    print(f"\nSummary: {total} error(s), {len(local_warnings)} local-path warning(s).")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
