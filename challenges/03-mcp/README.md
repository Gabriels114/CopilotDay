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

## Paso 2: Exportar el token como variable de entorno

```bash
# macOS/Linux — agrégalo a ~/.zshrc o ~/.bashrc
export GITHUB_TOKEN="ghp_tu_token_aqui"

# Recarga tu shell
source ~/.zshrc
```

La configuración de este repo usa una sola variable local, `GITHUB_TOKEN`. En `.vscode/mcp.json`, VS Code la toma del entorno y la reexpone dentro del contenedor como `GITHUB_PERSONAL_ACCESS_TOKEN`, que es el nombre esperado por el servidor oficial de GitHub.

## Paso 3: Verificar la configuración MCP

El archivo `.vscode/mcp.json` ya está configurado en este repo para usar el servidor oficial `ghcr.io/github/github-mcp-server` sobre `stdio`.

Antes de abrir VS Code, valida dos cosas desde terminal:

```bash
docker pull ghcr.io/github/github-mcp-server
```

```bash
docker run --rm -i \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_TOKEN" \
  -e GITHUB_TOOLSETS="context,repos,issues,pull_requests" \
  ghcr.io/github/github-mcp-server
```

Qué esperar:

- Si Docker no está corriendo, verás un error del daemon de Docker.
- Si el token no está exportado o no tiene permisos, el servidor fallará al iniciar o al primer uso de herramientas.
- Si el contenedor arranca sin errores inmediatos y queda esperando entrada, la configuración base es válida. Sal con `Ctrl+C`.

Notas sobre la configuración:

- El filtrado de capacidades se hace con `GITHUB_TOOLSETS`, porque en Docker el servidor oficial espera esa configuración como variable de entorno.
- Este repo habilita `context,repos,issues,pull_requests`, que cubre el reto sin exponer toolsets innecesarios.

## Paso 4: Crear Issues en GitHub

Crea al menos 5 issues en el repo con labels. Usa los ejemplos en `sample-issues.md` o crea los tuyos.

```bash
# Con GitHub CLI
gh issue create --title "Add sound effects" --label "feature,game-mechanic" \
  --body "Add hit and miss sound effects using pygame.mixer"
```

O hazlo desde la UI de GitHub: **Issues → New issue**.

Labels sugeridos a crear primero:
```bash
gh label create feature --color "#0075ca"
gh label create bug --color "#d73a4a"
gh label create enhancement --color "#a2eeef"
gh label create game-mechanic --color "#e4e669"
gh label create ux --color "#f9d0c4"
gh label create devops --color "#bfd4f2"
```

## Paso 5: Activar MCP en VS Code

1. Abre VS Code en la carpeta del proyecto
2. Abre **Copilot Chat** (Ctrl+Alt+I o ⌃⌘I)
3. Ejecuta **MCP: List Servers** desde la Command Palette
4. Verifica que aparece un servidor llamado `github` y que su estado está disponible
5. Abre el selector de herramientas del chat de Copilot y confirma que `github` está habilitado

Si no aparece:

- Reinicia VS Code después de exportar `GITHUB_TOKEN`
- Revisa que Docker Desktop esté levantado
- Vuelve a correr la validación manual del paso 3
- Abre **Output** o el panel de logs de MCP en VS Code para revisar errores de arranque

## Paso 6: Usar MCP en Copilot Chat

Prueba estos prompts en el chat de Copilot:

```
@github What are the open issues in CopilotDay?
```

```
@github List all issues labeled "feature" in my CopilotDay repo
```

```
@github Create a new issue titled "Add difficulty levels" with label "feature" and body "Allow the user to select Easy/Medium/Hard that adjusts mole_visible_time and mole_spawn_interval"
```

```
@github What files changed in the last commit?
```

## Criterios de Éxito

- [ ] El proyecto está en GitHub (`Gabriels114/CopilotDay`)
- [ ] Hay al menos 5 issues con labels en el repo
- [ ] La conexión MCP funciona (Docker corriendo, token exportado y servidor `github` visible en `MCP: List Servers`)
- [ ] Puedes mostrar Copilot Chat interactuando con tus issues via MCP
