# Challenge 04 - Visual Demonstration Guide

Este documento describe exactamente qué deberías ver en VS Code cuando pruebes Challenge 04.

---

## Paso 1: Verificar que VS Code Detecta Instrucciones Globales

### Acciones:
1. Abre VS Code con el repo
2. Abre Copilot Chat: `⌃⌘I` (macOS) o `Ctrl+Alt+I` (Windows/Linux)

### Qué deberías ver:

```
┌─────────────────────────────────────────────────────────┐
│ Copilot Chat                                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [📋] Custom Instructions                              │
│  [⚙️] Copilot Chat Settings                            │
│  [?] Help                                              │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  > Review the repo structure...                        │
│                                                         │
│  < Analyzing...                                        │
│                                                         │
│  [Chat input field]                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Indicador clave**: Ícono 📋 "Custom Instructions" visible

### Al hacer clic en Custom Instructions:

```
┌─────────────────────────────────────────────────────────┐
│ Custom Instructions Preview                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ # Copilot Instructions For This Repository             │
│                                                         │
│ This repository tracks progress for `WhatTheHack 071   │
│ - GitHub Copilot`.                                     │
│                                                         │
│ ## Project Context                                      │
│ - Treat the repository as a challenge-based learning   │
│   workspace, not as a polished production monolith.    │
│ - Challenges `01` through `06` evolve the same        │
│   `Whack-a-Mole` project under `challenges/01-intro`. │
│ - Challenge `07` is independent...                     │
│                                                         │
│ [Scroll to see more]                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Éxito**: ✅ `.github/copilot-instructions.md` se abre y muestra contenido

---

## Paso 2: Seleccionar Agent "Challenge Planner"

### Acciones:
1. En Copilot Chat, haz clic en el selector de agentes (usualmente arriba a la derecha del panel)
2. Busca "Challenge Planner"
3. Selecciónalo

### Qué deberías ver:

**Antes** (selector cerrado):
```
┌─────────────────────────────────────────────────────────┐
│ Copilot Chat                                       [  ] │
├─────────────────────────────────────────────────────────┤
│ Default agent                              ▼            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Después** (selector abierto):
```
┌─────────────────────────────────────────────────────────┐
│ Select an agent                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🔍 Default Agent                                       │
│    General GitHub Copilot chat                         │
│                                                         │
│ ✅ Challenge Planner                                   │
│    Read-only planning agent for WhatTheHack tasks,     │
│    adapted from the Awesome GitHub Copilot...         │
│                                                         │
│ ✅ TDD Refactor Phase - Improve Quality & Security    │
│    Installed from the Awesome GitHub Copilot          │
│    collection and lightly adapted...                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Éxito**: ✅ Ves "Challenge Planner" y "TDD Refactor Phase" en la lista

---

## Paso 3: Usar Challenge Planner Agent

### Acciones:
1. Selecciona "Challenge Planner"
2. Escribe en el chat:
```
Review the current repo state and recommend what should be the next 
challenge after Challenge 02.
```
3. Presiona Enter

### Qué deberías ver:

```
┌─────────────────────────────────────────────────────────┐
│ Copilot Chat                                            │
├─────────────────────────────────────────────────────────┤
│ Challenge Planner                            ▼          │
│                                                         │
│ You: Review the current repo state and               │
│      recommend what should be the next challenge      │
│      after Challenge 02.                              │
│                                                         │
│ Challenge Planner: Analyzing the repository...        │
│                                                         │
│ ## Current State                                        │
│ - Challenge 01: Whack-a-Mole game fully implemented  │
│   (198 tests, 99% coverage)                           │
│ - Challenge 02: Difficulty levels feature added      │
│   (4 levels: EASY/MEDIUM/HARD/INSANE)                │
│ - Challenge 03: MCP integration configured but not   │
│   yet executed                                        │
│ - Challenge 04: Customization (instructions +        │
│   agents) in progress                                │
│                                                        │
│ ## Recommended Next Step                              │
│ Complete Challenge 03 (MCP) by validating Docker    │
│ connectivity and GitHub token. This enables         │
│ real-time GitHub context in Copilot Chat.           │
│                                                        │
│ ## Files Likely Involved                              │
│ - `.vscode/mcp.json` (already configured)            │
│ - `$GITHUB_TOKEN` environment variable               │
│ - Terminal: docker pull + docker run validation      │
│                                                        │
│ ## Risks Or Dependencies                              │
│ - MCP requires Docker Desktop                        │
│ - GitHub token needs correct permissions             │
│   (Contents, Issues, PRs)                            │
│                                                        │
│ [Chat input field]                                    │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

**Éxito**: ✅ Agente proporciona análisis estructurado + recomendación

---

## Paso 4: Probar Instrucciones Contextuales (Features)

### Acciones:
1. Abre archivo: [`challenges/01-intro/config.py`](../../challenges/01-intro/config.py)
2. En Copilot Chat, escribe:
```
Add a new configuration option called 'animation_speed' with values 
SLOW (0.5), NORMAL (1.0), FAST (2.0). Follow the exact pattern of 
next_difficulty() and prev_difficulty().
```
3. Presiona Enter

### Qué deberías ver:

Copilot genera código como:

```python
# En config.py

class AnimationSpeed(Enum):
    SLOW = 0.5
    NORMAL = 1.0
    FAST = 2.0

ANIMATION_SETTINGS = {
    AnimationSpeed.SLOW:   0.5,
    AnimationSpeed.NORMAL: 1.0,
    AnimationSpeed.FAST:   2.0,
}

@dataclass(frozen=True)
class GameConfig:
    # ... otros campos ...
    animation_speed: AnimationSpeed = AnimationSpeed.NORMAL
    
    def next_animation_speed(self) -> 'GameConfig':
        speeds = list(AnimationSettings.keys())
        idx = speeds.index(self.animation_speed)
        return GameConfig(
            ...
            animation_speed=speeds[(idx + 1) % len(speeds)],
        )
    
    def prev_animation_speed(self) -> 'GameConfig':
        speeds = list(AnimationSettings.keys())
        idx = speeds.index(self.animation_speed)
        return GameConfig(
            ...
            animation_speed=speeds[(idx - 1) % len(speeds)],
        )
```

**Indicadores de éxito**:
- ✅ Usa Enum (como Difficulty)
- ✅ Define ANIMATION_SETTINGS dict (patrón del proyecto)
- ✅ Agrega campo a dataclass (frozen=True)
- ✅ Crea next_/prev_animation_speed() (patrón existente)
- ✅ Retorna nuevo GameConfig (inmutabilidad)

**Éxito**: ✅ Copilot siguió exactamente el patrón de `features.instructions.md`

---

## Paso 5: Probar Instrucciones Contextuales (Tests)

### Acciones:
1. Abre archivo: [`challenges/01-intro/tests/test_config.py`](../../challenges/01-intro/tests/test_config.py)
2. En Copilot Chat, escribe:
```
Add a parametrized test for animation_speed cycling. Use @pytest.mark.parametrize
with the pattern already in this file. Verify immutability.
```
3. Presiona Enter

### Qué deberías ver:

Copilot genera código como:

```python
# En tests/test_config.py

@pytest.mark.parametrize("speed,next_speed", [
    (AnimationSpeed.SLOW,   AnimationSpeed.NORMAL),
    (AnimationSpeed.NORMAL, AnimationSpeed.FAST),
    (AnimationSpeed.FAST,   AnimationSpeed.SLOW),
])
def test_config_animation_speed_cycles(speed, next_speed):
    config = GameConfig(animation_speed=speed)
    next_config = config.next_animation_speed()
    
    assert next_config.animation_speed == next_speed
    assert config.animation_speed == speed  # Verificar inmutabilidad
    assert next_config is not config  # Nueva instancia
```

**Indicadores de éxito**:
- ✅ Usa `@pytest.mark.parametrize` (per testing.instructions)
- ✅ Nombre descriptivo: `test_config_animation_speed_cycles`
- ✅ Fixture `GameConfig()` (patrón local del proyecto)
- ✅ Verifica inmutabilidad (original sin cambios)
- ✅ Verifica nueva instancia (not config)

**Éxito**: ✅ Copilot siguió exactamente el patrón de `testing.instructions.md`

---

## Paso 6: Usar TDD Refactor Phase Agent

### Acciones:
1. Selecciona "TDD Refactor Phase - Improve Quality & Security" agent
2. Escribe:
```
Review challenges/01-intro/board.py and suggest one small 
behavior-preserving refactor that would improve readability.
```
3. Presiona Enter

### Qué deberías ver:

```
┌─────────────────────────────────────────────────────────┐
│ Copilot Chat                                            │
├─────────────────────────────────────────────────────────┤
│ TDD Refactor Phase - Improve Quality & Security  ▼     │
│                                                         │
│ You: Review challenges/01-intro/board.py and         │
│      suggest one small behavior-preserving refactor   │
│      that would improve readability.                  │
│                                                         │
│ TDD Refactor Phase: Analyzing board.py...            │
│                                                         │
│ ## Identified Opportunity                              │
│ The `_index()` method is called in three places       │
│ (get, update, try_spawn, try_whack). Extracting      │
│ boundary checking into a reusable helper would       │
│ reduce duplication.                                   │
│                                                         │
│ ## Proposed Change                                     │
│ Extract a `_get_mole_safe()` method that handles    │
│ both boundary checking and retrieval:                │
│                                                         │
│ def _get_mole_safe(self, row: int, col: int)       │
│     -> Optional[Mole]:                               │
│     if not self._in_bounds(row, col):               │
│         return None                                  │
│     return self.moles[self._index(row, col)]        │
│                                                         │
│ ## Testing Strategy                                    │
│ Run existing tests before/after refactor:           │
│ ```bash                                              │
│ pytest tests/test_board.py -v                       │
│ ```                                                   │
│ Behavior should be identical. Coverage unchanged.   │
│                                                         │
│ ## Risk Assessment                                     │
│ Low risk: This is a pure extraction. The original   │
│ methods still exist and work the same way.          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Indicadores de éxito**:
- ✅ Propone cambio pequeño (no rewrite)
- ✅ Preserva comportamiento (refactor, no feature)
- ✅ Explica testing strategy
- ✅ Identifica riesgos
- ✅ Sugiere cómo validar (pytest)

**Éxito**: ✅ TDD Refactor Phase agent funciona correctamente

---

## Checklist Visual Final

| Checkpoint | Qué Ver | Estado |
|-----------|---------|--------|
| 1. Instrucciones globales | Ícono 📋 en Copilot Chat | ☐ |
| 2. Contenido instrucciones | `.github/copilot-instructions.md` visible | ☐ |
| 3. Selector de agentes | "Challenge Planner" + "TDD Refactor..." en dropdown | ☐ |
| 4. Challenge Planner respuesta | Análisis en 4 secciones (State/Step/Files/Risks) | ☐ |
| 5. Features instruction | Copilot genera Enum + SETTINGS + next_/prev_() | ☐ |
| 6. Testing instruction | Copilot usa @parametrize + verifica inmutabilidad | ☐ |
| 7. TDD Refactor respuesta | Cambio pequeño + testing strategy + riesgo | ☐ |

---

## Troubleshooting Visual

### ❌ No ves "Custom Instructions"
```
Solución:
1. Restart VS Code (⌘Q then reopen)
2. Check: Copilot Chat panel → Look for 📋 icon
3. If missing: Upgrade Copilot to 0.44.2+
```

### ❌ No ves los agentes en dropdown
```
Solución:
1. Close Copilot Chat panel
2. Reopen with ⌃⌘I
3. Look for dropdown selector (should be near top)
4. If still missing: Restart VS Code
```

### ❌ Copilot ignora instrucciones
```
Solución:
1. Verify file exists: .github/copilot-instructions.md ✓
2. Close Copilot Chat
3. Reopen with ⌃⌘I
4. Check View → Output → GitHub Copilot for errors
```

---

## Screenshots Ready for Demo

Save these as evidence that Challenge 04 is complete:

1. **Copilot Chat with "Custom Instructions"**
   - Show 📋 icon
   - Click to show content preview

2. **Agent Dropdown Showing Both Agents**
   - "Challenge Planner" visible
   - "TDD Refactor Phase" visible

3. **Challenge Planner Response**
   - Full analysis of current repo state
   - Recommendation for next steps

4. **Features Pattern Followed**
   - Generated code shows Enum + SETTINGS
   - Includes next_/prev_() methods
   - Frozen dataclass used

5. **Testing Pattern Followed**
   - @pytest.mark.parametrize used
   - Immutability verified
   - Fixtures preserved

---

**Next**: Compare your screen with these examples. If everything matches, Challenge 04 is successfully complete! ✅
