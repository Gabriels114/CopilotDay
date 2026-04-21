# Challenge 03 — Demo Script

Guía paso a paso para demostrar GitHub MCP Server funcionando en Copilot Chat.

## Prerequisitos de la demo

- Docker Desktop corriendo
- VS Code abierto en `CopilotDay/`
- Servidor `github` visible en `MCP: List Servers` (verde / disponible)

---

## Prompt 1 — Listar issues abiertos

**Propósito:** Verificar que MCP puede leer el estado del repositorio.

```
@github What are the open issues in Gabriels114/CopilotDay?
```

**Resultado esperado:** Copilot lista los issues con su número, título y labels.  
**Criterio:** Al menos 5 issues aparecen con labels correctos.

---

## Prompt 2 — Filtrar por label

**Propósito:** Demostrar filtrado semántico sin escribir queries manuales.

```
@github Show me all issues labeled "feature" in Gabriels114/CopilotDay
```

**Resultado esperado:** Solo issues con label `feature` aparecen.  
**Criterio:** Issues como "Add difficulty levels" y "Add sound effects" aparecen; bugs no.

---

## Prompt 3 — Crear un issue desde el chat

**Propósito:** Demostrar escritura al repo desde Copilot Chat.

```
@github Create an issue in Gabriels114/CopilotDay titled "Add keyboard shortcuts" with label "ux" and body "Allow whacking moles with number keys 1-9 as an alternative to mouse clicks. Useful for accessibility and speedrunning."
```

**Resultado esperado:** Copilot confirma el issue creado con número y URL.  
**Criterio:** Issue aparece en GitHub con el título, label y body correctos.

---

## Prompt 4 — Consultar historia de commits

**Propósito:** Mostrar que MCP accede al historial del repo, no solo issues.

```
@github What files changed in the last 3 commits of Gabriels114/CopilotDay?
```

**Resultado esperado:** Lista de commits con archivos modificados.  
**Criterio:** Los commits de Challenge 01 y 02 aparecen con sus archivos.

---

## Prompt 5 — Asistencia de código con contexto del repo

**Propósito:** Demostrar el caso de uso más poderoso: Copilot usa el contexto del repo para generar código relevante.

```
@github Look at the open issues in Gabriels114/CopilotDay and suggest which one is easiest to implement next based on the current codebase structure
```

**Resultado esperado:** Copilot analiza issues + código y da una recomendación con justificación.  
**Criterio:** La sugerencia menciona archivos concretos del repo (`game.py`, `config.py`, etc.).

---

## Troubleshooting

| Síntoma | Causa probable | Solución |
|---------|---------------|----------|
| `@github` no aparece en el chat | Servidor MCP no arrancó | Verificar Docker + Output→MCP |
| "Tool not found" | Toolset no habilitado | Revisar `GITHUB_TOOLSETS` en `mcp.json` |
| "Unauthorized" / 401 | Token sin permisos o expirado | Crear nuevo PAT con los scopes del Paso 1 |
| Respuestas lentas | Docker pull tardío | `docker pull ghcr.io/github/github-mcp-server` antes de la demo |
| VS Code no pide el token | Input prompt no soportado en versión antigua | Actualizar VS Code o usar `${env:...}` |

---

## Mapping: Prompts → Criterios de Éxito

| Prompt | Criterio del reto |
|--------|------------------|
| 1 — Listar issues | "Hay al menos 5 issues con labels" |
| 2 — Filtrar por label | "Copilot interactúa con tus issues via MCP" |
| 3 — Crear issue | Capacidad de escritura al repo |
| 4 — Historia de commits | MCP accede a repos, no solo issues |
| 5 — Sugerencia contextual | Caso de uso real de productividad |
