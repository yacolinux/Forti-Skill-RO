# FortiGate SSH Skills (FortiOS 7.x)

Colección de **skills operativos read-only** para diagnóstico de FortiGate por SSH, orientados a FortiOS 7.x. Cada skill es un documento autocontenido en `SKILL.md` con placeholders, procedimiento, interpretación y guardrails.

> **Idioma:** Español.  
> **Acceso:** SSH directo a la CLI de FortiGate.  
> **Restricción:** Exclusivamente comandos de lectura (`show`, `get`, `diagnose`, `execute log display/filter`).  
> **Prohibido:** `config`, `set`, `unset`, `delete`, `move`, `execute reboot` o cualquier comando de mutación.

---

## Catálogo de Skills por Dominio Operativo

### 🔧 Sistema y Plataforma

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **system-status-ssh** | `get system status`, `get system performance status`, `diagnose hardware sysinfo memory`, `diagnose sys top-summary` | Versión FortiOS, serial, uptime, hostname, CPU, memoria |
| **resources-status-ssh** | `get system performance status`, `diagnose hardware sysinfo memory`, `diagnose sys top-summary` | Procesos con mayor consumo de CPU/RAM, picos de recursos |
| **config-audit-vs-defaults-ssh** | `show`, `show full-configuration`, `get system status` (+ `rg`, `diff` locales) | Features en uso, diferencias vs defaults, secciones configuradas |

### 🔌 Interfaces y Conectividad

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **interfaces-status-ssh** | `get system interface`, `diagnose netlink interface list`, `get system arp` | Estado admin/operativo, direccionamiento, velocidad/duplex, tabla ARP |

### 🔥 Firewall y Políticas

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **firewall-policy-review-ssh** | `show firewall policy`, `show firewall policy6`, `show firewall address`, `show firewall addrgrp`, `show firewall service custom/group`, `diagnose firewall iprope list/lookup` | Políticas IPv4/IPv6, objetos, orden de reglas, match teórico de flujo |
| **firewall-policy-hit-status-ssh** | `show firewall policy`, `diagnose firewall iprope list`, `diagnose firewall iprope lookup` | Estado de políticas activas, validación match de tráfico por flujo |

### 🌐 Routing

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **routing-status-ssh** | `get router info routing-table all/details/database` | Rutas activas, default route, next-hop, origen (static/connected/dynamic) |

### 🔁 Alta Disponibilidad (HA)

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **ha-status-ssh** | `get system ha status`, `diagnose sys ha status`, `diagnose sys ha checksum cluster` | Rol primary/secondary, sincronización, miembros, checksum de configuración |

### 📊 Sesiones y Tráfico

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **sessions-status-ssh** | `diagnose sys session stat`, `diagnose sys session list`, `diagnose sys session filter` | Volumen de sesiones activas, tasas de creación/expiración, drops, sesiones por IP |

### 🔐 VPN

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **vpn-ipsec-status-ssh** | `get vpn ipsec tunnel summary`, `diagnose vpn tunnel list`, `diagnose vpn ike gateway list` | Tuneles IPsec up/down, SAs, rekeys, errores IKE, contadores |
| **vpn-ssl-status-ssh** | `get vpn ssl monitor`, `diagnose vpn ssl statistics`, `diagnose vpn ssl list` | Usuarios SSL-VPN conectados, duración de sesión, IPs asignadas |

### 📋 Logs y Eventos

| Skill | Comandos Principales | Qué detecta |
|---|---|---|
| **logs-alerts-status-ssh** | `execute log filter reset`, `execute log filter category 0`, `execute log display` (heredoc) | Eventos de sistema/seguridad recientes, filtrado por texto |

---

## Estructura del Repositorio

```
.agents/skills/
├── fortigate-config-audit-vs-defaults-ssh/SKILL.md
├── fortigate-firewall-policy-hit-status-ssh/SKILL.md
├── fortigate-firewall-policy-review-ssh/SKILL.md
├── fortigate-ha-status-ssh/SKILL.md
├── fortigate-interfaces-status-ssh/SKILL.md
├── fortigate-logs-alerts-status-ssh/SKILL.md
├── fortigate-resources-status-ssh/SKILL.md
├── fortigate-routing-status-ssh/SKILL.md
├── fortigate-sessions-status-ssh/SKILL.md
├── fortigate-system-status-ssh/SKILL.md
├── fortigate-vpn-ipsec-status-ssh/SKILL.md
└── fortigate-vpn-ssl-status-ssh/SKILL.md
Makefile
README.md
Tests/
├── test_skills_syntax.py
├── test_skills_docs_check.py
└── run_all.py
.github/
└── workflows/
    └── tests.yml
```

Cada skill es un archivo `SKILL.md` autocontenido con:

- **YAML frontmatter**: `name`, `description`.
- **Placeholders**: `<usuario>`, `<host>`, `<policyid-opcional>`, etc.
- **Notas operativas 7.4.x**: restricciones de perfil, comportamiento de `diagnose`, diferencias con otros fabricantes.
- **Procedimiento**: bloques `bash` con comandos SSH listos para copiar/pegar.
- **Interpretación rápida**: qué buscar en la salida de cada comando.
- **Guardrails**: recordatorio de qué no hacer.

---

## Seguridad de Contenido

- ❌ No incluir credenciales, IPs reales, dominios reales, hostnames reales ni datos de clientes.
- ✅ Usar placeholders con formato `<nombre>`.
- ❌ No incluir comandos de mutación (`config`, `set`, `unset`, `delete`, `move`, `execute reboot`).
- ✅ Solo `show`, `get`, `diagnose`, `execute log display/filter/reset`.

> ⚠️ **Hallazgo**: El skill `fortigate-vpn-ssl-status-ssh` contiene placeholders `<admin2>` y `<NJH3889nsdf>` con apariencia de datos reales. Se recomienda reemplazar por `<usuario>` y `<host>` respectivamente.

---

## Validación y CI

### Local

```bash
# Ejecutar todas las validaciones offline
make test

# Incluir verificación opcional contra docs públicas de Fortinet
make test-online
```

### GitHub Actions

El workflow en `.github/workflows/tests.yml` se ejecuta automáticamente en cada `push` y `pull_request`:

- Ubuntu latest + Python 3.11.
- `make test` (validación offline de frontmatter, comandos read-only y catálogo 7.x).

### Qué valida cada test

| Test | Propósito |
|---|---|
| `test_skills_syntax.py` | Frontmatter requerido, bloques bash, comandos read-only, ausencia de mutación |
| `test_skills_docs_check.py` (offline) | Comandos dentro del catálogo permitido FortiOS 7.x |
| `test_skills_docs_check.py --online` | Consulta búsqueda pública de Fortinet por cada comando base |

---

## Referencia Rápida de Comandos Base

```
show, show full-configuration
show firewall policy, show firewall policy6
show firewall address, show firewall addrgrp
show firewall service custom, show firewall service group
get system status, get system performance status
get system interface, get system arp
get system ha status
get router info routing-table all/details/database
get vpn ipsec tunnel summary
get vpn ssl monitor
diagnose hardware sysinfo memory
diagnose sys top-summary
diagnose sys session stat, diagnose sys session list
diagnose sys session filter (clear/src/dst/dport/sport/proto)
diagnose netlink interface list
diagnose firewall iprope list, diagnose firewall iprope lookup
diagnose sys ha status, diagnose sys ha checksum cluster
diagnose vpn tunnel list, diagnose vpn ike gateway list
diagnose vpn ssl statistics, diagnose vpn ssl list
execute log filter reset, execute log filter category, execute log display
```
