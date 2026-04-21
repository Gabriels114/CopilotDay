# Challenge 04 - Testing Custom Instructions & Agents

Este documento proporciona instrucciones paso a paso para validar que tus instrucciones personalizadas y agentes funcionan correctamente en VS Code.

---

## ✅ Checklist de Success Criteria

- [ ] Custom instructions file visible en VS Code
- [ ] Custom agent seleccionable en Copilot Chat
- [ ] Copilot responde acorde a instrucciones personalizadas
- [ ] Agent `Challenge Planner` funciona en context-aware mode

---

## Paso 1: Verificar que VS Code detecta `.github/copilot-instructions.md`

### A. Abrir VS Code

```bash
cd /Users/gabriels/Proyectos/CopilotDay
code .
```

### B. Abrir Copilot Chat

- **macOS**: `⌃⌘I` (Ctrl + Cmd + I)
- **Windows/Linux**: `Ctrl+Alt+I`

### C. Verificar que se detectan las instrucciones

En la UI de Copilot Chat, deberías ver un ícono o mención de **"Custom Instructions"** (usualmente en la esquina superior derecha del panel de chat).

✅ **Éxito**: VS Code muestra "Custom instructions detected" o similar.

---

## Paso 2: Revisar el contenido de instrucciones

En Copilot Chat, haz clic en el ícono de **instrucciones personalizadas** y verifica que aparece:

- Project Context (Challenges 01-06 compartir `challenges/01-intro`)
- Source Modules (tabla con config.py, mole.py, board.py, etc.)
- Python Conventions (frozen dataclasses, no pygame en lógica, etc.)
- Testing Expectations (pytest, headless setup)

✅ **Éxito**: Las instrucciones aparecen en el preview de Copilot.

---

## Paso 3: Probar instrucciones específicas por archivo

### A. Abrir un archivo dentro del scope

Abre [`challenges/01-intro/config.py`](../../challenges/01-intro/config.py) en el editor.

### B. Solicitar generación de código

En Copilot Chat (con `config.py` abierto), escribe:

```
Add a new configuration option called 'animation_speed' that cycles through 
SLOW (0.5), NORMAL (1.0), FAST (2.0). Follow the exact pattern of 
next_difficulty() and prev_difficulty().
```

### C. Verificar que Copilot sigue el patrón

Copilot debería:
- ✅ Definir un Enum `AnimationSpeed` con tres valores
- ✅ Agregar un dict `ANIMATION_SETTINGS` (similar a `DIFFICULTY_SETTINGS`)
- ✅ Usar frozen dataclass (no mutación)
- ✅ Crear `next_animation_speed()` y `prev_animation_speed()` con el mismo patrón

**Esto demuestra que `.github/instructions/features.instructions.md` funciona.**

---

## Paso 4: Verificar instrucciones de testing

### A. Abrir [`challenges/01-intro/tests/test_config.py`](../../challenges/01-intro/tests/test_config.py)

### B. Pedir un nuevo test

En Copilot Chat (con `test_config.py` abierto), escribe:

```
Add a parametrized test that verifies 'animation_speed' cycles correctly
through SLOW, NORMAL, FAST and back to SLOW after calling next_animation_speed()
four times. Follow the pytest parametrize pattern already in this file.
```

### C. Verificar que Copilot sigue convenciones de test

Copilot debería:
- ✅ Usar `@pytest.mark.parametrize` (como se ve en el archivo)
- ✅ Nombrar el test como `test_config_animation_speed_cycles`
- ✅ Preservar el fixture `default_config`
- ✅ No mutar estado (verificar que retorna nuevas instancias)

**Esto demuestra que `.github/instructions/testing.instructions.md` funciona.**

---

## Paso 5: Seleccionar y probar el agente `Challenge Planner`

### A. Abrir Copilot Chat

`⌃⌘I` (macOS) o `Ctrl+Alt+I` (Windows/Linux)

### B. Cambiar a `Challenge Planner` agent

En el selector de modo (usualmente un ícono de gota o modo en la parte superior del panel de chat), elige:

```
Challenge Planner
```

Si no ves el agente, reinicia VS Code.

### C. Hacer una pregunta de planificación

```
Review the current repo state and recommend what should be the next 
challenge after 02 (Difficulty Levels).
```

### D. Verificar respuesta del agente

El agente **Challenge Planner** debería:
- ✅ Resumir el estado actual en 3-5 bullets
- ✅ Identificar desafíos (blockers)
- ✅ Recomendar pasos concretos
- ✅ Mencionar archivos específicos
- ✅ **NO editar código** (es read-only)

**Ejemplo de respuesta esperada:**

```
## Current State
- Challenge 01: Whack-a-Mole game fully implemented (198 tests, 99% coverage)
- Challenge 02: Difficulty levels feature added (4 levels: EASY/MEDIUM/HARD/INSANE)
- Challenge 03: MCP integration configured but not yet executed
- Challenge 04: Customization (instructions + agents) in progress

## Recommended Next Step
Complete Challenge 03 (MCP) by validating Docker connectivity and GitHub token.
This enables real-time GitHub context in Copilot Chat.

## Files Likely Involved
- `.vscode/mcp.json` (already configured)
- `$GITHUB_TOKEN` environment variable (needs to be set)
- Terminal: docker pull + docker run validation

## Risks Or Dependencies
- MCP requires Docker Desktop
- GitHub token needs correct permissions (Contents, Issues, PRs)
```

---

## Paso 6: Probar el segundo agente `TDD Refactor Phase`

### A. Cambiar a `TDD Refactor Phase - Improve Quality & Security` agent

En el selector de agentes, elige:

```
TDD Refactor Phase - Improve Quality & Security
```

### B. Hacer una solicitud de refactor

```
Review board.py and suggest one small improvement to make the code 
more readable or maintainable without changing behavior. Then show me 
how to test that the change doesn't break anything.
```

### C. Verificar respuesta del agente

El agente debería:
- ✅ Analizar `board.py`
- ✅ Proponer cambio behavior-preserving pequeño
- ✅ Explicar riesgos
- ✅ Sugerir cómo verificar con tests

---

## Paso 7: Validar que instrucciones por archivo se aplican

### A. Abrir [`challenges/01-intro/tests/test_board.py`](../../challenges/01-intro/tests/test_board.py)

### B. Pedir mejora de test

Con `test_board.py` abierto, en Copilot Chat pide:

```
Improve the test_try_whack_out_of_bounds_returns_miss_and_same_board test 
to be more descriptive. The test name should reflect which bounds were tested.
```

### C. Verificar respuesta

Copilot debería:
- ✅ Reconocer que es un archivo de test (por el path `tests/`)
- ✅ Aplicar convenciones de pytest
- ✅ Mantener fixtures y parametrize
- ✅ No alterar el setup SDL dummy

**Esto valida que `testing.instructions.md` (applyTo: challenges/01-intro/tests/**)  se aplica.**

---

## ✅ Checklist Final - Validación Completa

| Criterio | Validado | ✓ |
|----------|----------|---|
| `.github/copilot-instructions.md` existe y VS Code lo detecta | Paso 1-2 | ☐ |
| Instrucciones guían generación de código (feature pattern) | Paso 3 | ☐ |
| Instrucciones guían generación de tests (pytest pattern) | Paso 4 | ☐ |
| `Challenge Planner` agent seleccionable y funcional | Paso 5 | ☐ |
| `Challenge Planner` produce planes concretos (read-only) | Paso 5 | ☐ |
| `TDD Refactor Phase` agent seleccionable y funcional | Paso 6 | ☐ |
| Instrucciones de test se aplican por scope (challenges/01-intro/tests/**) | Paso 7 | ☐ |

---

## Notas Importantes

### Si no ves los agentes en VS Code

1. Asegúrate de tener **GitHub Copilot 0.44.2+** instalado
2. Reinicia VS Code completamente
3. Verifica que estés usando el **Copilot Chat integrado** (no la app de desktop)

### Si Copilot ignora las instrucciones

1. Verifica que el archivo esté en `.github/copilot-instructions.md` (ubicación exacta)
2. Reinicia Copilot Chat (cierra y abre de nuevo con `⌃⌘I`)
3. Revisa la consola de output de Copilot (View → Output → GitHub Copilot)

### Estructura esperada de archivos

```
.github/
├── copilot-instructions.md       ← Instrucciones globales
├── agents/
│   ├── challenge-planner.agent.md
│   └── tdd-refactor.agent.md
└── instructions/
    ├── features.instructions.md   (applyTo: challenges/01-intro/**)
    ├── testing.instructions.md    (applyTo: challenges/01-intro/tests/**)
    └── python-tests.instructions.md (applyTo: challenges/01-intro/tests/**/*.py)
```

---

## Cómo demostrar para el Challenge

Captura pantalla de:

1. **Copilot Chat mostrando instrucciones personalizadas**
   - Abre Copilot Chat
   - Haz clic en el ícono de instrucciones
   - Screenshot del preview

2. **Agente `Challenge Planner` seleccionado y funcionando**
   - Selector de agentes con `Challenge Planner` elegido
   - Respuesta a una pregunta de planificación
   - Screenshot mostrando análisis del repo

3. **Copilot siguiendo instrucciones personalizadas**
   - Pide una feature nueva con el patrón específico
   - Copilot genera código que sigue exactamente el patrón frozen dataclass + next_X()
   - Screenshot del código generado

4. **Instrucciones específicas por archivo**
   - Abre un archivo en `challenges/01-intro/tests/`
   - Pide un test nuevo
   - Copilot genera test que respeta `@pytest.mark.parametrize` y fixtures
   - Screenshot del test generado

Juntos, estos screenshots demuestran que:
- ✅ Custom instructions file exists and is detected
- ✅ Custom agents are installed and selectable
- ✅ Copilot responds in alignment with custom instructions
