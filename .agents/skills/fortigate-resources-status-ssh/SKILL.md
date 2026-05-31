---
name: fortigate-resources-status-ssh
description: Consulta CPU, memoria y procesos de FortiGate por SSH en FortiOS 7.x con comandos de solo lectura.
---

# FortiGate Resources Status SSH

Evalua consumo de recursos para diagnostico inicial de performance.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.

## Notas operativas 7.4.x

- Todos los comandos `diagnose` de esta skill pueden depender de `cli-diagnose enable` en el perfil si no se usa `super_admin`.
- `diagnose sys top 1 20` puede ser mas util en sesion interactiva; para automatizacion suele ser mas estable `diagnose sys top-summary`.

## Procedimiento

```bash
ssh <usuario>@<host> "get system performance status"
ssh <usuario>@<host> "diagnose hardware sysinfo memory"
ssh <usuario>@<host> "diagnose sys top-summary"
```

## Interpretacion rapida

- Identificar procesos con mayor CPU/RAM.
- Detectar saturacion sostenida o picos periodicos.
- Correlacionar con sesiones concurrentes, trafico y eventos.

## Guardrails

- Solo lectura: no ejecutar comandos que alteren procesos.
