# AGENTS.md

## Repo Structure

- Skills live under **`.agents/skills/<fortigate-<topic>-ssh>/SKILL.md`** — not at repo root.
- Root-level `REPORTE.md` and `REPORTE-ANON.md` are sample diagnostic outputs (not skills).
- There is **no build system, no CI, no package manifests, no runtime code**.

## Skill Format

Each skill is exactly one `SKILL.md` with:

- YAML frontmatter: `name`, `description`.
- Sections: Placeholders, Procedure (bash SSH command blocks), Interpretation, Guardrails.
- Directory name pattern: `fortigate-<topic>-ssh`.
- Frontmatter `name` should match the directory intent.

## Validation Commands

Since there is no test runner, verify manually:

```bash
# Verify layout and frontmatter
find .agents/skills -maxdepth 2 -type f | sort
rg -n "^name:|^description:" .agents/skills/*/SKILL.md

# Detect non-read-only or risky commands
rg -n "config |\bset\b|\bunset\b|\bdelete\b|execute reboot" .agents/skills/*/SKILL.md
```

## Hard Constraints

- **Strictly read-only.** All commands must be `show`, `get`, or `diagnose` only.
- Never include `config`, `set`, `unset`, `delete`, `execute reboot`, or any mutation command.
- Do not include credentials, hostnames, or customer IPs in examples.
- Target FortiOS 7.x via SSH.

## Language & Placeholders

- Skill content is in **Spanish**.
- Use placeholders like `<usuario>`, `<host>`, `<policyid-opcional>`.

## Known Operational Quirk

Some runtime `diagnose` and `get` commands may fail even with a `super_admin` profile on certain builds/contexts (see `REPORTE.md`). Skills should still document the standard 7.x command; note profile restrictions in "Notas operativas" when relevant.
