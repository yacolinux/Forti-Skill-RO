---
name: fortigate-config-audit-vs-defaults-ssh
description: Revisa configuracion completa de FortiGate por SSH y determina features usadas y diferencias respecto de defaults en FortiOS 7.x.
---

# FortiGate Config Audit vs Defaults SSH

Obtiene configuracion completa y efectiva para detectar:
1) que caracteristicas estan en uso
2) que configuraciones difieren de defaults

## Placeholders

- `<usuario>`: usuario SSH con permisos de lectura.
- `<host>`: IP o FQDN del FortiGate.
- `<prefix-local>`: prefijo local para archivos de evidencia (ejemplo: `fgt01`).

## Notas operativas 7.4.x

- FortiOS no usa un modo `enable` al estilo Cisco. Si el login entra a CLI, ya quedas en el nivel permitido por el perfil administrativo.
- En FortiOS 7.4.2 o superior, los comandos `diagnose` pueden estar bloqueados por perfil aunque el usuario sea admin funcional. `get` y `show` suelen seguir habilitados; `diagnose` requiere `cli-diagnose enable` en el `accprofile`, salvo `super_admin`.
- La falta de soporte/licencia de FortiCare no deshabilita por si sola la CLI/SSH. Si no hay acceso, revisar `allowaccess ssh` en la interfaz, `trustedhosts`, perfil administrativo y restricciones de acceso.

## Procedimiento

```bash
# 1) Capturar config no-default (effective custom)
ssh <usuario>@<host> "show" > <prefix-local>.show.conf

# 2) Capturar config completa con defaults
ssh <usuario>@<host> "show full-configuration" > <prefix-local>.full.conf

# 3) Capturar estado base y version
ssh <usuario>@<host> "get system status" > <prefix-local>.status.txt
```

## Deteccion de features usadas

```bash
# Secciones presentes en la config custom (features activamente configuradas)
rg '^config ' <prefix-local>.show.conf

# Busquedas rapidas por feature comun
rg -n 'config firewall policy|config firewall vip|config vpn ipsec|config vpn ssl|config router static|config router bgp|config system interface|config user' <prefix-local>.show.conf
```

## Deteccion de diferencias vs defaults

```bash
# Lineas custom efectivas (lo que difiere de defaults normalmente aparece en show)
wc -l <prefix-local>.show.conf

# Diff contextual entre full/default-aware y custom
# (orientativo: la fuente de verdad para cambios efectivos es <prefix-local>.show.conf)
diff -u <prefix-local>.full.conf <prefix-local>.show.conf | sed -n '1,200p'
```

## Criterio de interpretacion

- `show` representa cambios efectivos respecto al baseline/default del equipo.
- Secciones presentes en `show` equivalen a features usadas o ajustadas.
- `show full-configuration` sirve para contraste y auditoria completa del estado.
- Para auditoria multi-equipo, repetir y comparar `*.show.conf` entre equipos del mismo perfil.

## Guardrails

- Solo lectura: no ejecutar `execute backup`, `config`, `set`, `unset`, `delete` ni comandos de reinicio.
