#!/usr/bin/env python3
"""Chequeo opcional de comandos vs docs publicas de Fortinet.

Modo por defecto (offline):
- Extrae comandos remotos desde skills.
- Verifica que cada comando base este en un catalogo permitido por version.

Modo online (opcional):
- Ademas consulta busqueda publica de docs Fortinet por comando base.
- Si una consulta falla por red, marca warning y continua.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

SSH_QUOTED_RE = re.compile(r"ssh\s+[^\n\"]*?@[^\s\n\"]+\s+\"([^\"]+)\"")

# Catalogo base esperado para skills FortiOS 7.x de este repo.
ALLOWED_BASE_COMMANDS_7X = {
    "diagnose firewall iprope list",
    "diagnose firewall iprope lookup",
    "diagnose hardware sysinfo memory",
    "diagnose netlink interface list",
    "diagnose sys ha checksum cluster",
    "diagnose sys ha status",
    "diagnose sys session filter clear",
    "diagnose sys session filter dst",
    "diagnose sys session filter dport",
    "diagnose sys session filter proto",
    "diagnose sys session filter src",
    "diagnose sys session filter sport",
    "diagnose sys session list",
    "diagnose sys session stat",
    "diagnose sys top-summary",
    "diagnose vpn ike gateway list",
    "diagnose vpn ssl list",
    "diagnose vpn ssl statistics",
    "diagnose vpn tunnel list",
    "execute log display",
    "execute log filter category",
    "execute log filter reset",
    "get router info routing-table all",
    "get router info routing-table database",
    "get router info routing-table details",
    "get system arp",
    "get system ha status",
    "get system interface",
    "get system performance status",
    "get system status",
    "get vpn ipsec tunnel summary",
    "get vpn ssl monitor",
    "show",
    "show firewall addrgrp",
    "show firewall address",
    "show firewall policy",
    "show firewall policy6",
    "show firewall service custom",
    "show firewall service group",
    "show full-configuration",
}


def extract_bash_blocks(md: str) -> list[str]:
    return re.findall(r"```bash\n(.*?)```", md, flags=re.DOTALL)


def extract_heredoc_commands(block: str) -> list[str]:
    cmds: list[str] = []
    for chunk in re.findall(r"<<'EOF'\n(.*?)\nEOF", block, flags=re.DOTALL):
        for line in chunk.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cmds.append(line)
    return cmds


def normalize_remote_command(cmd: str) -> str:
    s = cmd.strip().lower()
    s = s.split("|", 1)[0].strip()

    tokens = []
    for tok in s.split():
        if tok.startswith("<") and tok.endswith(">"):
            break
        if tok.isdigit():
            break
        tokens.append(tok)

    return " ".join(tokens)


def collect_base_commands() -> set[str]:
    base_cmds: set[str] = set()
    for skill in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        md = skill.read_text(encoding="utf-8")
        for block in extract_bash_blocks(md):
            for quoted in SSH_QUOTED_RE.findall(block):
                norm = normalize_remote_command(quoted)
                if norm:
                    base_cmds.add(norm)
            for heredoc_cmd in extract_heredoc_commands(block):
                norm = normalize_remote_command(heredoc_cmd)
                if norm:
                    base_cmds.add(norm)
    return base_cmds


def check_docs_search(query: str, timeout: float = 12.0) -> tuple[bool, str]:
    encoded = urllib.parse.urlencode({"q": query})
    url = f"https://docs.fortinet.com/search?{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": "skills-validator/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="ignore").lower()
    except Exception as exc:  # noqa: BLE001
        return False, f"warning: no se pudo consultar '{query}' ({exc})"

    if "no results" in html or "no result" in html:
        return False, f"sin resultados en docs para '{query}'"
    return True, "ok"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--online",
        action="store_true",
        help="ademas consulta docs publicas de Fortinet por comando",
    )
    args = parser.parse_args()

    repo_cmds = collect_base_commands()

    unknown = sorted(cmd for cmd in repo_cmds if cmd not in ALLOWED_BASE_COMMANDS_7X)
    if unknown:
        print("FALLA: comandos fuera del catalogo permitido 7.x")
        for cmd in unknown:
            print(f"- {cmd}")
        return 1

    print(f"OK offline: {len(repo_cmds)} comandos base dentro del catalogo 7.x")

    if not args.online:
        print("Info: para validacion contra docs publicas usar --online")
        return 0

    failures = []
    warnings = []
    for cmd in sorted(repo_cmds):
        ok, msg = check_docs_search(cmd)
        if ok:
            continue
        if msg.startswith("warning:"):
            warnings.append(msg)
        else:
            failures.append(msg)

    if warnings:
        print(f"WARN: {len(warnings)} consultas no verificadas por red")
        for w in warnings:
            print(f"- {w}")

    if failures:
        print("FALLA online: comandos sin evidencia en docs publicas")
        for f in failures:
            print(f"- {f}")
        return 1

    print("OK online: comandos con resultados en docs publicas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
