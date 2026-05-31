---
name: fortigate-routing-status-ssh
description: Consulta estado de routing en FortiGate por SSH para FortiOS 7.x usando solo lectura.
---

# FortiGate Routing Status SSH

Verifica rutas activas, default route y estado de protocolos dinamicos si aplica.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<prefijo-opcional>`: red o IP para lookup.

## Notas operativas 7.4.x

- El filtrado con `grep` se hace localmente, no dentro del CLI del FortiGate.

## Procedimiento

```bash
ssh <usuario>@<host> "get router info routing-table all"
ssh <usuario>@<host> "get router info routing-table details"
ssh <usuario>@<host> "get router info routing-table database"
ssh <usuario>@<host> "get router info routing-table all" | grep -F "<prefijo-opcional>"
```

## Interpretacion rapida

- Confirmar presencia de ruta por defecto y next-hop valido.
- Revisar origen de rutas (static, connected, dynamic).
- Si falta ruta critica, validar anuncios o dependencias upstream.

## Guardrails

- Solo lectura: no usar comandos de cambio de rutas.
