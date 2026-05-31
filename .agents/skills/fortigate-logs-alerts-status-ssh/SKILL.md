---
name: fortigate-logs-alerts-status-ssh
description: Consulta eventos y alertas recientes en FortiGate por SSH para FortiOS 7.x con comandos de solo lectura.
---

# FortiGate Logs Alerts Status SSH

Recupera eventos recientes de sistema y seguridad para diagnostico inicial.

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<filtro-opcional>`: texto para filtrar eventos.

## Notas operativas 7.4.x

- Los filtros de logs son estado dentro de la sesion CLI. Si ejecutas cada `execute log filter ...` en un `ssh` distinto, no persisten.
- `execute` suele seguir permitido aunque `diagnose` este bloqueado, pero depende del perfil.
- La falta de soporte/licencia no deshabilita por si sola este acceso; si falla el login SSH, revisar `allowaccess ssh` y restricciones del admin.

## Procedimiento

```bash
# Mantener el mismo SSH para que el filtro persista
ssh -tt <usuario>@<host> <<'EOF'
execute log filter reset
execute log filter category 0
execute log display
EOF

# Filtrado local opcional de la salida
ssh -tt <usuario>@<host> <<'EOF' | grep -i "<filtro-opcional>"
execute log filter reset
execute log filter category 0
execute log display
EOF
```

## Interpretacion rapida

- Revisar errores de sistema, eventos de VPN y denegaciones.
- Usar filtros para acotar por servicio, IP o texto clave.
- Correlacionar timestamp de eventos con incidentes reportados.

## Guardrails

- Solo lectura: no borrar logs ni cambiar destinos de logging.
