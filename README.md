# FortiGate SSH Skills (FortiOS 7.x)

Coleccion de skills operativos para diagnostico de FortiGate por SSH, con enfoque **read-only**.

## Estructura

- Skills en `.agents/skills/fortigate-<topic>-ssh/SKILL.md`.
- Cada skill contiene frontmatter YAML (`name`, `description`) y secciones operativas.
- No hay runtime, build ni dependencias de aplicacion.

## Alcance

- Comandos orientados a FortiOS 7.x.
- Uso exclusivo de comandos de lectura (`show`, `get`, `diagnose`).
- Prohibidos comandos de cambio (`config`, `set`, `unset`, `delete`, `execute reboot`, etc.).

## Seguridad de contenido

- No incluir credenciales, IPs reales, dominios reales, hostnames reales ni datos de clientes.
- Usar placeholders como `<usuario>`, `<host>`, `<policyid-opcional>`.

## Validacion local

Ejecutar desde la raiz del repo:

```bash
make test
python3 Tests/run_all.py
python3 Tests/test_skills_syntax.py
python3 Tests/test_skills_docs_check.py
```

La validacion revisa:

- Frontmatter requerido (`name` y `description`).
- Presencia de bloques `bash` con comandos.
- Comandos remotos con prefijos permitidos (`show`, `get`, `diagnose`).
- Ausencia de comandos de mutacion y patrones riesgosos.

Validacion opcional contra docs publicas:

```bash
make test-online
python3 Tests/run_all.py --online
python3 Tests/test_skills_docs_check.py --online
```

- `offline` valida que los comandos usados por skills esten dentro de un catalogo permitido para FortiOS 7.x.
- `--online` consulta busqueda publica de Fortinet por cada comando base para agregar evidencia externa.
- Si hay problemas de red, el modo online reporta `warning` y no detiene la validacion offline.

## Auditoria rapida manual

```bash
find .agents/skills -maxdepth 2 -type f | sort
rg -n "^name:|^description:" .agents/skills/*/SKILL.md
rg -n "config |\bset\b|\bunset\b|\bdelete\b|execute reboot" .agents/skills/*/SKILL.md
```
