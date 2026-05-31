# Repository Guidelines

## Project Structure & Module Organization
This repository contains FortiGate operational skills. Each skill lives in its own top-level directory and currently contains one file: `SKILL.md`.

Example structure:
- `fortigate-system-status-ssh/SKILL.md`
- `fortigate-firewall-policy-review-ssh/SKILL.md`

Each `SKILL.md` should include YAML frontmatter (`name`, `description`) and concise operational sections (placeholders, procedure, interpretation, guardrails). There are no source-code modules, package manifests, or runtime assets in this repo.

## Build, Test, and Development Commands
There is no build pipeline for this repository. Use lightweight validation commands:
- `find . -maxdepth 2 -type f | sort` — verify expected file layout.
- `rg -n "^name:|^description:" */SKILL.md` — check required frontmatter fields.
- `rg -n "config |\bset\b|\bunset\b|\bdelete\b|execute reboot" */SKILL.md` — detect non-read-only commands or risky patterns.
- `sed -n '1,80p' <skill-dir>/SKILL.md` — quick header/content review.

## Coding Style & Naming Conventions
- Use Markdown with clear `#`/`##` headings and short paragraphs.
- Keep content ASCII where possible.
- Skill directory naming pattern: `fortigate-<topic>-ssh`.
- Frontmatter naming should match the directory intent, e.g. `name: fortigate-routing-status-ssh`.
- Prefer explicit command placeholders like `<usuario>`, `<host>`, `<policyid-opcional>`.

## Testing Guidelines
Validation is documentation-focused:
- Ensure every skill has valid frontmatter and a runnable command block.
- Ensure procedures remain read-only (`show`, `get`, `diagnose` where applicable).
- Spot-check command examples for FortiOS 7.x compatibility before merging.
- For new skills, test at least one primary command in a lab device when available.

## Commit & Pull Request Guidelines
No Git history is available in this directory, so no existing convention can be inferred. Use this standard:
- Commit format: `docs(skill): add fortigate-<topic>-ssh`.
- Keep commits scoped to one skill or one logical doc update.
- PRs should include: objective, affected skill directories, and a brief validation summary (commands run + results).

## Security & Configuration Tips
- Do not include credentials, hostnames, or customer IPs in examples.
- Keep all skills strictly read-only unless a future repository policy explicitly allows change operations.
