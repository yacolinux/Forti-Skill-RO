#!/usr/bin/env python3
"""Validaciones de sintaxis/base para skills FortiGate read-only."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

REQUIRED_FRONTMATTER_KEYS = ("name", "description")
BLOCKED_PATTERN = re.compile(
    r"\b(config|set|unset|delete|move|append|rename)\b",
    re.IGNORECASE,
)
BLOCKED_EXPLICIT_RE = re.compile(r"\bexecute\s+reboot\b", re.IGNORECASE)
SSH_QUOTED_RE = re.compile(r"ssh\s+[^\n\"]*?@[^\s\n\"]+\s+\"([^\"]+)\"")
ALLOWED_REMOTE_PREFIXES = ("show", "get", "diagnose", "execute")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(md: str) -> dict[str, str]:
    if not md.startswith("---\n"):
        return {}
    parts = md.split("---\n", 2)
    if len(parts) < 3:
        return {}
    raw = parts[1]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip()
    return data


def extract_bash_blocks(md: str) -> list[str]:
    return re.findall(r"```bash\n(.*?)```", md, flags=re.DOTALL)


def extract_heredoc_commands(block: str) -> list[str]:
    cmds: list[str] = []
    for match in re.findall(r"<<'EOF'\n(.*?)\nEOF", block, flags=re.DOTALL):
        for line in match.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cmds.append(line)
    return cmds


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    md = read_text(path)

    frontmatter = parse_frontmatter(md)
    for key in REQUIRED_FRONTMATTER_KEYS:
        if not frontmatter.get(key):
            errors.append(f"{path}: falta frontmatter '{key}'")

    bash_blocks = extract_bash_blocks(md)
    if not bash_blocks:
        errors.append(f"{path}: no tiene bloque ```bash```")
        return errors

    for block in bash_blocks:
        remote_cmds = SSH_QUOTED_RE.findall(block)
        remote_cmds.extend(extract_heredoc_commands(block))

        for remote_cmd in remote_cmds:
            normalized = remote_cmd.strip().lower()
            if BLOCKED_PATTERN.search(normalized) or BLOCKED_EXPLICIT_RE.search(normalized):
                errors.append(f"{path}: comando remoto bloqueado detectado: '{remote_cmd}'")
                continue
            if not normalized.startswith(ALLOWED_REMOTE_PREFIXES):
                errors.append(
                    f"{path}: comando remoto no read-only detectado: '{remote_cmd}'"
                )

    return errors


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print(f"No se encontraron skills en {SKILLS_DIR}")
        return 1

    all_errors: list[str] = []
    for skill in skill_files:
        all_errors.extend(validate_skill(skill))

    if all_errors:
        print("FALLA: validacion de skills")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print(f"OK: {len(skill_files)} skills validados sin hallazgos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
