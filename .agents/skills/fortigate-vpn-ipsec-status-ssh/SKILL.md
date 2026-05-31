---
name: fortigate-vpn-ipsec-status-ssh
description: Consulta estado de tuneles IPsec en FortiGate por SSH (FortiOS 7.x) con comandos de solo lectura.
---

# FortiGate VPN IPsec Status SSH

Verifica estado de tuneles IPsec, SAs y contadores basicos.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<tunnel-opcional>`: nombre del tunel para filtrar.

## Notas operativas 7.4.x

- `diagnose` puede requerir `cli-diagnose enable` en el perfil administrativo.
- El filtrado con `grep` se hace del lado local.

## Procedimiento

```bash
ssh <usuario>@<host> "get vpn ipsec tunnel summary"
ssh <usuario>@<host> "diagnose vpn tunnel list"
ssh <usuario>@<host> "diagnose vpn ike gateway list"
ssh <usuario>@<host> "diagnose vpn tunnel list" | grep -i "<tunnel-opcional>"
```

## Interpretacion rapida

- Confirmar tuneles `up` y presencia de SAs activas.
- Revisar rekeys, errores IKE y contadores de bytes/paquetes.
- Si un tunel cae, correlacionar con rutas y reachability remota.

## Guardrails

- Solo lectura: no ejecutar comandos para resetear o renegociar tuneles.
