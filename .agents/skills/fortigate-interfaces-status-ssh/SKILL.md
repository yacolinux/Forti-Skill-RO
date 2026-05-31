---
name: fortigate-interfaces-status-ssh
description: Consulta estado de interfaces de FortiGate por SSH en FortiOS 7.x con comandos read-only.
---

# FortiGate Interfaces Status SSH

Inspecciona estado administrativo y operativo de interfaces fisicas y logicas.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<ifname-opcional>`: interfaz para filtrar.

## Notas operativas 7.4.x

- `diagnose` puede requerir permiso `cli-diagnose` en FortiOS 7.4.2+.
- El `grep` debe aplicarse localmente sobre la salida del `ssh`, no dentro del CLI remoto.

## Procedimiento

```bash
ssh <usuario>@<host> "get system interface"
ssh <usuario>@<host> "diagnose netlink interface list"
ssh <usuario>@<host> "diagnose netlink interface list" | grep -i "<ifname-opcional>"
ssh <usuario>@<host> "get system arp"
```

## Interpretacion rapida

- Validar `status up` en interfaces criticas.
- Confirmar direccionamiento, speed/duplex y errores visibles.
- Correlacionar ARP con reachability de segmentos esperados.

## Guardrails

- Solo lectura: no usar `config system interface` ni `set`.
