---
name: fortigate-ha-status-ssh
description: Consulta estado HA de FortiGate por SSH en FortiOS 7.x con comandos de solo lectura.
---

# FortiGate HA Status SSH

Valida salud y rol del cluster HA (primary/secondary), sincronizacion y miembros.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN de cualquier miembro del cluster.

## Notas operativas 7.4.x

- `get system ha status` suele funcionar con permisos de lectura.
- Los comandos `diagnose sys ha ...` pueden quedar bloqueados en 7.4.2+ si el perfil no tiene `cli-diagnose enable`.
- No existe un paso `enable` previo.

## Procedimiento

```bash
ssh <usuario>@<host> "get system ha status"
ssh <usuario>@<host> "diagnose sys ha status"
ssh <usuario>@<host> "diagnose sys ha checksum cluster"
```

## Interpretacion rapida

- Confirmar nodo primary y miembros en estado `in-sync`.
- Revisar heartbeat links y eventos de failover recientes.
- Si hay mismatch de checksum, revisar drift de configuracion.

## Guardrails

- Solo lectura: no usar `execute ha failover set` ni comandos de cambio.
