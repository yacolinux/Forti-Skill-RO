---
name: fortigate-system-status-ssh
description: Consulta estado general de FortiGate por SSH en FortiOS 7.x usando solo comandos de lectura.
---

# FortiGate System Status SSH

Consulta estado base del equipo: version, uptime, hora y estado global.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.

## Notas operativas 7.4.x

- `get` suele seguir habilitado aunque `diagnose` este restringido por perfil.
- Si `get system status` funciona pero `diagnose ...` no, el problema normalmente es permisos `cli-diagnose`, no licencia ni falta de `enable`.

## Procedimiento

```bash
ssh <usuario>@<host> "get system status"
ssh <usuario>@<host> "get system performance status"
ssh <usuario>@<host> "diagnose hardware sysinfo memory"
ssh <usuario>@<host> "diagnose sys top-summary"
```

## Interpretacion rapida

- Verificar version/build de FortiOS, serial, hostname y uptime.
- Confirmar CPU/memoria en rangos esperados para la ventana operativa.
- Si hay picos de CPU o memoria, correlacionar con sesiones y logs.

## Guardrails

- Solo lectura: usar `get` y `diagnose`.
- No ejecutar comandos de configuracion ni reinicio.
