---
name: fortigate-firewall-policy-review-ssh
description: Inspecciona y revisa politicas de firewall en FortiGate por SSH (FortiOS 7.x) con enfoque de auditoria read-only.
---

# FortiGate Firewall Policy Review SSH

Revisa politicas IPv4/IPv6, objetos referenciados y orden de reglas para auditoria operativa.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<policyid-opcional>`: policy ID para busqueda puntual.
- `<src-ip>`, `<src-port>`, `<dst-ip>`, `<dst-port>`, `<proto>`: flujo para validacion de match.
- `<srcintf>`: interfaz de ingreso del flujo.
- `<pol-type>`: tipo de policy, normalmente `policy`.

## Notas operativas 7.4.x

- `diagnose` puede requerir `cli-diagnose enable` en el perfil administrativo desde FortiOS 7.4.2+.
- El filtrado con `grep` o la numeracion con `nl` se hace del lado local, no dentro de la CLI remota.
- No existe `enable` para escalar privilegios como en Cisco.

## Procedimiento

```bash
# Dump de politicas IPv4 e IPv6
ssh <usuario>@<host> "show firewall policy"
ssh <usuario>@<host> "show firewall policy6"

# Reglas con numeracion para revisar orden
ssh <usuario>@<host> "show firewall policy" | nl -ba

# Buscar policy puntual
ssh <usuario>@<host> "show firewall policy" | grep -n "edit <policyid-opcional>"

# Revisar objetos usados por las policies
ssh <usuario>@<host> "show firewall address"
ssh <usuario>@<host> "show firewall addrgrp"
ssh <usuario>@<host> "show firewall service custom"
ssh <usuario>@<host> "show firewall service group"

# Validacion teorica de match de flujo
ssh <usuario>@<host> "diagnose firewall iprope list"
ssh <usuario>@<host> "diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <proto> <srcintf> <pol-type>"
```

## Checklist de revision

- Reglas criticas al inicio y reglas de denegacion explicitas al final.
- Politicas sin `srcaddr`, `dstaddr` o `service` excesivamente amplios.
- NAT habilitado solo donde corresponde.
- Objetos inexistentes, obsoletos o redundantes.
- Consistencia entre comentarios, naming y accion real de la policy.

## Guardrails

- Solo lectura: usar `show` y `diagnose`.
- No ejecutar `config firewall policy`, `set`, `unset`, `move` ni `delete`.
