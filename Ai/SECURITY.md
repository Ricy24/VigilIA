# SECURITY.md — Consideraciones de Seguridad

---

## Principios de Seguridad del Sistema

### 1. Privacidad por Diseño (SAD §1.9, Ley 1581 de 2012)

VigilIA procesa video de personas en entornos laborales. Esto implica:

- **Informar a los trabajadores:** Las empresas que implementen VigilIA DEBEN informar a sus trabajadores
  sobre el tratamiento de imágenes con IA, en el marco de sus políticas de videovigilancia.
- **Minimización de datos:** Solo se almacena la información necesaria para el propósito de SST.
  No se almacena video crudo de forma indefinida — solo snapshots de eventos detectados.
- **No identificación biométrica:** La v1.0 NO hace reconocimiento facial. Los tracks son IDs temporales
  de sesión, no vinculados a la identidad del trabajador.
- **Retención limitada:** Los snapshots de eventos tienen una política de retención configurable.

### 2. Seguridad de la API

#### Autenticación JWT
- Access tokens con expiración corta (60 minutos por defecto)
- Refresh tokens con expiración larga (7 días) almacenados de forma segura
- Algoritmo HS256 con SECRET_KEY de al menos 32 bytes generada con `secrets.token_hex(32)`
- **NUNCA** usar la SECRET_KEY por defecto en producción

#### Autorización por roles
Roles del sistema (Fase 1):
- `admin`: acceso total, gestión de usuarios y cámaras
- `supervisor`: visualización de dashboard y alertas, sin gestión
- `hse`: gestión de incidentes y reportes, sin administración de cámaras

#### CORS
- En desarrollo: permitir `localhost:5173`
- En producción: ONLY el dominio real del frontend. NO usar `*`

### 3. Seguridad de la Infraestructura

```bash
# Variables de entorno sensibles: NUNCA en el código
# ✅ Correcto
SECRET_KEY = settings.SECRET_KEY

# ❌ Nunca
SECRET_KEY = "mi_clave_secreta_123"
```

- PostgreSQL y Redis NO deben estar expuestos a internet en producción
  (solo accesibles dentro de la red Docker o VPN)
- Usar contraseñas fuertes para PostgreSQL (generadas, no mnemónicas)
- Redis en producción: habilitar `requirepass`

### 4. Seguridad del Pipeline de IA

**Regla crítica:** El sistema de IA detecta y alerta. **NUNCA automatiza consecuencias.**

- Una alerta de VigilIA → notificación a supervisor humano → el humano decide la acción
- Ningún proceso automático sanciona, reporta formalmente o para maquinaria basándose solo en
  la detección de IA (sin revisión humana)
- El LLM solo narra — ver `Ai/DECISIONS.md` para el detalle

### 5. Checklist de Seguridad antes de Producción

- [ ] `SECRET_KEY` generada con `secrets.token_hex(32)` y almacenada en secret manager
- [ ] `DEBUG=false` en producción
- [ ] `ALLOWED_ORIGINS` restringido al dominio real
- [ ] PostgreSQL y Redis NO expuestos a internet
- [ ] Contraseñas de BD generadas y almacenadas de forma segura
- [ ] HTTPS habilitado (TLS terminado en Nginx o load balancer)
- [ ] Trabajadores informados sobre el tratamiento de datos de videovigilancia
- [ ] Política de retención de snapshots configurada y documentada
- [ ] Acceso a la sala de control / dashboard restringido por VPN o IP allowlist

---

## Gestión de Vulnerabilidades

- Revisar dependencias con `pip audit` (Python) y `npm audit` (Node.js) periódicamente
- Mantener imágenes Docker base actualizadas (especialmente `python:3.12-slim` y `node:22-alpine`)
- Reportar vulnerabilidades de seguridad del proyecto en privado (no como issues públicos)
