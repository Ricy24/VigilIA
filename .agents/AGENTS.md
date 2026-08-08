# AGENTS.md — Reglas del Agente para el Workspace VigilIA

## Documentación viva en `Ai/`

Los archivos de la carpeta `Ai/` son **documentación viva** que debe mantenerse actualizada
de forma incremental. El agente DEBE seguir estas reglas:

### Regla 1 — Actualizaciones quirúrgicas
**NUNCA reescribir un archivo `Ai/` completo** si solo necesita modificar una sección.
Usar siempre `replace_file_content` o `multi_replace_file_content` para editar solo
las líneas que cambian.

Excepciones aceptables para reescritura completa:
- El archivo está vacío (solo contiene una línea o está en blanco)
- El usuario pide explícitamente "reescribe" o "recrea" ese archivo

### Regla 2 — Al finalizar cualquier fase o tarea importante
Actualizar siempre estos archivos antes de terminar la sesión:
- `Ai/TASKS.md` → marcar tareas completadas, agregar pendientes de la siguiente fase
- `Ai/ROADMAP.md` → actualizar el estado de la fase (✅ Completada / 🔄 En progreso)
- `Ai/DECISIONS.md` → agregar cualquier nueva decisión técnica tomada
- `Ai/PROJECT_CONTEXT.md` → actualizar "Estado del Proyecto" si cambió de fase

### Regla 3 — Al agregar dependencias
Si se modifican `requirements.txt` o `package.json`, actualizar `Ai/TECH_STACK.md`
con las versiones reales instaladas.

### Regla 4 — Registro de desvíos del SAD
Si se toma una decisión que difiere de lo planteado en el SAD (`docs/VigilIA_SAD_v1.0.docx`),
registrarlo en `Ai/DECISIONS.md` con la justificación del cambio.

---

## Contexto del proyecto

Ver `Ai/AI_AGENT.md` para el contexto completo, estructura de directorios y comandos frecuentes.

---

## Regla de seguridad crítica (no negociable)

El LLM **NUNCA** participa en decisiones de seguridad del sistema.
Solo genera narrativa de eventos ya detectados y estructurados por el Vision Pipeline.
Ver `Ai/SECURITY.md` y `Ai/DECISIONS.md` para el contexto completo.
