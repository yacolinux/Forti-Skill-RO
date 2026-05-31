---
name: fortigate-sessions-status-ssh
description: Consulta estado de sesiones en FortiGate por SSH para FortiOS 7.x usando comandos read-only.
---

# FortiGate Sessions Status SSH

Inspecciona volumen de sesiones activas y su salud para troubleshooting de trafico.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<ip-opcional>`: IP de origen o destino para filtro.

## Notas operativas 7.4.x

- Los `diagnose sys session filter ...` son estado dentro de la sesion actual. Si abres un `ssh` nuevo para `list`, el filtro ya no aplica.
- `diagnose` puede requerir `cli-diagnose enable` desde FortiOS 7.4.2+.
- `head` debe ejecutarse localmente sobre la salida del `ssh`, no dentro de la CLI remota.

## Procedimiento

```bash
ssh <usuario>@<host> "diagnose sys session stat"
ssh <usuario>@<host> "diagnose sys session list" | head -n 200

# Filtro por origen en la misma sesion SSH
ssh -tt <usuario>@<host> <<'EOF' | head -n 100
diagnose sys session filter clear
diagnose sys session filter src <ip-opcional>
diagnose sys session list
EOF

# Filtro por destino en la misma sesion SSH
ssh -tt <usuario>@<host> <<'EOF' | head -n 100
diagnose sys session filter clear
diagnose sys session filter dst <ip-opcional>
diagnose sys session list
EOF
```

## Interpretacion rapida

- Revisar total de sesiones, tasas de creacion/expiracion y drops.
- Buscar sesiones atascadas o patrones repetitivos por IP.
- Limpiar filtros entre consultas para evitar falsos negativos.

## Guardrails

- Solo lectura: no usar comandos de clear global de sesiones.
