# Challenge 03 — GitHub MCP Server

## Objetivo

Conectar GitHub Copilot a tu repositorio de GitHub via Model Context Protocol (MCP), para que pueda consultar issues, PRs y código directamente desde el chat.

## Prerequisitos

- Docker Desktop instalado y corriendo
- Cuenta GitHub con acceso al repo `Gabriels114/CopilotDay`
- VS Code con extensión GitHub Copilot (versión reciente con soporte MCP)

## Paso 1: Crear un Personal Access Token (PAT)

1. Ve a **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Crea un nuevo token con:
   - Repositorio: `CopilotDay`
   - Permisos: `Contents (read)`, `Issues (read/write)`, `Pull requests (read/write)`, `Metadata (read)`
3. Copia el token generado

## Paso 2: Configuración del token (VS Code lo pide automáticamente)

**No necesitas exportar variables de entorno.** El archivo `.vscode/mcp.json` usa el mecanismo de *inputs* de VS Code:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github-token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ]
}
```

La primera vez que el servidor MCP arranque, VS Code muestra un diálogo para pegar tu token. El valor queda almacenado en el llavero del sistema (Keychain en macOS) y no vuelve a pedirse.

> **¿Prefieres env var?** También puedes exportar `GITHUB_PERSONAL_ACCESS_TOKEN` en tu shell y reemplazar `"${input:github-token}"` por `"${env:GITHUB_PERSONAL_ACCESS_TOKEN}"` en `.vscode/mcp.json`.

## Paso 3: Verificar la configuración MCP

El archivo `.vscode/mcp.json` ya está configurado en este repo para usar el servidor oficial `ghcr.io/github/github-mcp-server` sobre `stdio`.

Valida que Docker funciona antes de abrir VS Code:

```bash
docker pull ghcr.io/github/github-mcp-server
```

```bash
# Prueba manual (sustituye TU_TOKEN por tu PAT)
docker run --rm -i \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="TU_TOKEN" \
  -e GITHUB_TOOLSETS="context,repos,issues,pull_requests" \
  ghcr.io/github/github-mcp-server
```

Qué esperar:

- Si Docker no está corriendo, verás un error del daemon de Docker.
- Si el token no tiene permisos, el servidor fallará al usar las herramientas.
- Si el contenedor arranca sin errores y queda esperando entrada, la configuración es válida. Sal con `Ctrl+C`.

Notas sobre la configuración:

- `GITHUB_TOOLSETS` filtra las capacidades expuestas; este repo habilita `context,repos,issues,pull_requests`.
- Los toolsets innecesarios quedan deshabilitados para seguir el principio de mínimo privilegio.

## Paso 4: Issues en GitHub

El repo ya tiene issues creados con labels. Puedes crear más desde Copilot Chat (ver Paso 6) o con CLI:

```bash
gh issue create --title "Add sound effects" --label "feature,game-mechanic" \
  --body "Add hit and miss sound effects using pygame.mixer"
```

Labels disponibles: `feature`, `bug`, `enhancement`, `game-mechanic`, `ux`, `devops`

## Paso 5: Activar MCP en VS Code

1. Abre VS Code en la carpeta del proyecto
2. Abre **Copilot Chat** (⌃⌘I / Ctrl+Alt+I)
3. Ejecuta **MCP: List Servers** desde la Command Palette
4. Verifica que aparece un servidor llamado `github` y que su estado está disponible
5. Cuando uses `@github` por primera vez, VS Code pedirá tu PAT — pégalo y presiona Enter

Si no aparece:

- Asegúrate que Docker Desktop esté corriendo
- Reinicia VS Code
- Abre **Output → MCP** para revisar errores de arranque
- Confirma que `.vscode/mcp.json` existe (no está en `.gitignore`)

## Paso 6: Usar MCP en Copilot Chat

Ver `demo.md` para los prompts de demostración completos.

Prompts de inicio rápido:

```
@github What are the open issues in CopilotDay?
```

```
@github List all issues labeled "feature" in Gabriels114/CopilotDay
```

```
@github What files changed in the last commit?
```

## Criterios de Éxito

- [ ] El proyecto está en GitHub (`Gabriels114/CopilotDay`)
- [ ] Hay al menos 5 issues con labels en el repo
- [ ] La conexión MCP funciona (Docker corriendo, servidor `github` visible en `MCP: List Servers`)
- [ ] VS Code solicitó el PAT automáticamente al primer uso de `@github`
- [ ] Puedes mostrar Copilot Chat interactuando con tus issues via MCP
