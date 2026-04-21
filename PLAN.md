# Plan de Trabajo — WhatTheHack 071: GitHub Copilot

## Objetivo

Completar los 8 challenges del hackathon usando GitHub Copilot como asistente principal en cada etapa.

## Stack base

- Python 3.12 + pygame 2.6.1
- pytest + pytest-cov (≥80% cobertura)
- GitHub Actions (CI headless)
- GitHub MCP Server (Docker)
- VS Code con extensión GitHub Copilot

## Hilo conductor

Los challenges **01–06** construyen progresivamente sobre el mismo juego **Whack-a-Mole**. El challenge **07** es independiente y usa código de OWASP Juice Shop.

---

## Challenges

### Challenge 00 — Prerequisitos
**Estado**: ⬜ Manual (verificar instalaciones)

- [ ] Cuenta GitHub activa con Copilot habilitado
- [ ] VS Code con extensión GitHub Copilot instalada y activa
- [ ] Python 3.12+ disponible en PATH
- [ ] Docker Desktop instalado (requerido para Challenge 03)
- [ ] Activar el entorno virtual: `source .venv/bin/activate`

**Criterio de éxito**: Copilot sugiere código al abrir un archivo `.py` en VS Code.

---

### Challenge 01 — Introducción a GitHub Copilot
**Estado**: ✅ Base implementada

**Archivos**: `challenges/01-intro/` (config, mole, board, game, renderer, main)

**Qué hacer con Copilot**:
- [ ] Ejecutar el juego: `python challenges/01-intro/main.py`
- [ ] Explorar las sugerencias de Copilot al modificar `renderer.py`
- [ ] Demostrar 3 estilos de interacción distintos:
  1. **Autocompletado** (tab): escribir el inicio de una función y aceptar sugerencia
  2. **Chat / Ask**: preguntar "explain what `board.try_spawn()` does"
  3. **Comentario como prompt**: escribir `# draw stars when mole is whacked` y aceptar

**Criterio de éxito**: Juego funciona, puedes explicar cómo Copilot ayudó con ejemplos concretos.

---

### Challenge 02 — Best Practices
**Estado**: ⬜ Pendiente (agregar feature al juego)

**Dependencia**: Challenge 01 completado.

**Qué hacer**:
- [ ] Elegir una feature del `challenges/03-mcp/sample-issues.md` (ej. "difficulty levels")
- [ ] Aplicar las 3 técnicas de prompt engineering al implementarla con Copilot:
  1. **General → Específico**: empezar con "add difficulty to the game", luego refinar
  2. **Descomponer tareas**: separar config, lógica, UI
  3. **Dar ejemplos**: mostrar la estructura existente de `GameConfig` como ejemplo
- [ ] Documentar antes/después en `challenges/02-best-practices/NOTES.md`

**Criterio de éxito**: Feature integrada al juego, puedes mostrar cómo cambiaron los prompts.

---

### Challenge 03 — Model Context Protocol
**Estado**: ⬜ Pendiente (configurar y demostrar)

**Archivos**: `.vscode/mcp.json`, `challenges/03-mcp/README.md`

**Qué hacer**:
- [ ] Crear PAT en GitHub con scopes `repo` + `read:org`
- [ ] Exportar: `export GITHUB_TOKEN="ghp_..."`
- [ ] Verificar Docker: `docker pull ghcr.io/github/github-mcp-server`
- [ ] Crear ≥5 issues en el repo usando `challenges/03-mcp/sample-issues.md`
- [ ] Demostrar Copilot Chat consultando los issues via MCP

**Criterio de éxito**: Copilot responde preguntas sobre tus issues reales del repo.

---

### Challenge 04 — Personalización en el IDE
**Estado**: ✅ Archivos creados

**Archivos**: `.github/copilot-instructions.md`, `.github/instructions/`, `.github/agents/`

**Qué hacer**:
- [ ] Abrir Copilot Chat y verificar que reconoce la arquitectura del repo
- [ ] Seleccionar el agente **Challenge Planner** en el selector de modos
- [ ] Usar el agente para planificar el Challenge 02
- [ ] Demostrar que Copilot respeta las instrucciones (ej. no sugiere mutar estado)

**Criterio de éxito**: Copilot orienta sugerencias según `copilot-instructions.md`.

---

### Challenge 05 — Dev Workflow
**Estado**: ✅ CI configurado

**Archivos**: `.github/workflows/ci.yml`, `challenges/05-dev-workflow/README.md`

**Qué hacer**:
- [ ] Hacer un commit usando Copilot para generar el mensaje (icono ✨ en VS Code)
- [ ] Verificar que el CI pasa en GitHub Actions tras el push
- [ ] Agregar badge de CI al `README.md`:
  ```
  ![CI](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml/badge.svg)
  ```

**Criterio de éxito**: Pipeline verde en GitHub Actions visible en el repo.

---

### Challenge 06 — Tests y Documentación
**Estado**: ✅ Suite de tests creada (146 tests, ~80% cobertura)

**Archivos**: `challenges/01-intro/tests/`, `challenges/06-tests-docs/README.md`

**Qué hacer**:
- [ ] Ejecutar tests: `pytest challenges/01-intro/tests/ --cov=challenges/01-intro --cov-report=term-missing`
- [ ] Usar Copilot para generar tests para la feature del Challenge 02
- [ ] Agregar docstrings a las funciones principales con ayuda de Copilot
- [ ] Verificar que los nuevos tests se integren al CI

**Criterio de éxito**: Tests de la nueva feature pasan en CI, cobertura ≥80%.

---

### Challenge 07 — Debug y Optimización
**Estado**: ✅ Código vulnerable preparado

**Archivos**: `challenges/07-debug-optimization/src/`, `challenges/07-debug-optimization/test/`

**Qué hacer**:
- [ ] Abrir `coupon-discount.vulnerable.js` en VS Code
- [ ] Usar Copilot Chat con estos prompts:
  - `Explain what calculateApplicableDiscount is doing and where the trust boundary is.`
  - `Find the security issue in this coupon validation flow.`
  - `Refactor this code to use signed coupon tokens and safer validation.`
- [ ] Identificar los 2 bugs: token sin firma + coerción de tipos (`==` vs `===`)
- [ ] Ejecutar tests: `cd challenges/07-debug-optimization && npm test`
- [ ] Comparar la versión vulnerable con `coupon-discount.fixed.js`

**Criterio de éxito**: Puedes explicar ambas vulnerabilidades y mostrar cómo Copilot las detectó.

---

## Comandos de referencia

```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar el juego
python challenges/01-intro/main.py

# Correr todos los tests Python
pytest challenges/01-intro/tests/ -v --cov=challenges/01-intro

# Tests de Challenge 07 (Node)
cd challenges/07-debug-optimization && npm test
```

## Progreso general

| Challenge | Archivos | Demostración con Copilot |
|---|---|---|
| 00 | ⬜ Manual | ⬜ |
| 01 | ✅ | ⬜ |
| 02 | ⬜ | ⬜ |
| 03 | ✅ Config | ⬜ |
| 04 | ✅ | ⬜ |
| 05 | ✅ CI | ⬜ |
| 06 | ✅ Tests | ⬜ |
| 07 | ✅ | ⬜ |
