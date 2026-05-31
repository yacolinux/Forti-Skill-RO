---
name: fortigate-firewall-policy-hit-status-ssh
description: Consulta estado de politicas y hits de firewall en FortiGate por SSH (FortiOS 7.x) sin cambios de configuracion.
---

# FortiGate Firewall Policy Hit Status SSH

Permite revisar politicas activas y validacion basica de coincidencia de trafico.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<policyid-opcional>`: policy ID para filtro puntual.
- `<src-ip>`, `<src-port>`, `<dst-ip>`, `<dst-port>`, `<proto>`: flujo a validar con lookup.
- `<srcintf>`: interfaz de ingreso del flujo.
- `<pol-type>`: tipo de policy, normalmente `policy`.

## Notas operativas 7.4.x

- `diagnose` puede estar bloqueado por perfil a partir de FortiOS 7.4.2 aunque `show` y `get` funcionen. Si falla solo `diagnose`, revisar `cli-diagnose`.
- No usar `grep`, `head`, `nl` o `;` dentro del comando remoto de FortiGate. Si necesitas filtrar, filtra localmente despues del `ssh`.
- No existe `enable` para elevar privilegios dentro de la CLI.

## Procedimiento

```bash
ssh <usuario>@<host> "show firewall policy"
ssh <usuario>@<host> "diagnose firewall iprope list"
ssh <usuario>@<host> "diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <proto> <srcintf> <pol-type>"
ssh <usuario>@<host> "show firewall policy" | grep -n "edit <policyid-opcional>"
```

## Interpretacion rapida

- Corroborar existencia y orden de policy esperada.
- Usar lookup para validar match teorico de flujo especifico.
- Si no hay match, revisar objetos, interfaces y orden de reglas.

## Guardrails

- Solo lectura: no usar `config firewall policy`, `set` o `move`.
