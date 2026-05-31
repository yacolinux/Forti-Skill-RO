---
name: fortigate-vpn-ssl-status-ssh
description: Consulta estado de SSL-VPN y usuarios conectados en FortiGate por SSH con comandos de solo lectura.
---

# FortiGate VPN SSL Status SSH

Inspecciona estado de SSL-VPN y sesiones de usuarios remotos.

## Placeholders

- `<admin2>`: usuario SSH con permisos de lectura.
- `<NJH3889nsdf>`: IP o FQDN del FortiGate.

## Notas operativas 7.4.x

- `get vpn ssl monitor` es una consulta valida en 7.4.x.
- Los comandos `diagnose vpn ssl ...` pueden requerir `cli-diagnose enable` en el perfil si no usas `super_admin`.
- No existe `enable` para cambiar de modo de privilegio dentro de la CLI.

## Procedimiento

```bash
ssh <usuario>@<host> "get vpn ssl monitor"
ssh <usuario>@<host> "diagnose vpn ssl statistics"
ssh <usuario>@<host> "diagnose vpn ssl list"
```

## Interpretacion rapida

- Ver usuarios conectados, duracion de sesion y IPs asignadas.
- Detectar reconexiones frecuentes o desconexiones abruptas.
- Correlacionar con consumo de recursos y logs de auth.

## Guardrails

- Solo lectura: no finalizar sesiones ni modificar portal/policies.
