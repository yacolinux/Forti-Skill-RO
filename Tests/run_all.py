#!/usr/bin/env python3
"""Runner simple para ejecutar todas las validaciones de skills."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_step(label: str, command: list[str]) -> int:
    print(f"[RUN] {label}: {' '.join(command)}")
    proc = subprocess.run(command, cwd=ROOT)
    if proc.returncode == 0:
        print(f"[OK]  {label}")
    else:
        print(f"[FAIL] {label} (exit={proc.returncode})")
    print()
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--online",
        action="store_true",
        help="incluye validacion opcional contra docs publicas Fortinet",
    )
    args = parser.parse_args()

    steps: list[tuple[str, list[str]]] = [
        ("Sintaxis skills", [sys.executable, "Tests/test_skills_syntax.py"]),
        ("Catalogo comandos offline", [sys.executable, "Tests/test_skills_docs_check.py"]),
    ]
    if args.online:
        steps.append(
            (
                "Verificacion docs online",
                [sys.executable, "Tests/test_skills_docs_check.py", "--online"],
            )
        )

    failures = 0
    for label, cmd in steps:
        failures += 1 if run_step(label, cmd) != 0 else 0

    if failures:
        print(f"RESULTADO: FALLA ({failures} paso(s) con error)")
        return 1

    print("RESULTADO: OK (todas las validaciones pasaron)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
