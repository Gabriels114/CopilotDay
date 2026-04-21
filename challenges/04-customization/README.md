# Challenge 04 - Personalización de GitHub Copilot en el IDE

En este reto aprendiste a personalizar GitHub Copilot para entender el contexto, estándares y preferencias de tu proyecto. La personalización se implementa con:

- **Instrucciones globales** en `.github/copilot-instructions.md`
- **Instrucciones contextuales** en `.github/instructions/*.instructions.md` (aplicadas por ruta de archivo)
- **Agentes personalizados** en `.github/agents/*.agent.md` (modos de chat especializados)

## ✅ Success Criteria Completados

- [x] **Custom instructions file**: Creado `.github/copilot-instructions.md` que define arquitectura, convenciones Python, expectativas de testing
- [x] **Custom agents**: Instalados dos agentes (`Challenge Planner` y `TDD Refactor Phase`)
- [x] **Context-aware instructions**: Cuatro archivos de instrucciones (`testing.md`, `features.md`, `python-tests.md`)
- [x] **Copilot responds aligned**: Las sugerencias de Copilot respetan frozen dataclasses, patrones de arquitectura, y convenciones de test

---

## Qué se agregó

### Instrucciones globales

**[`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)**  
Define el contexto permanente del repo: que los challenges 01–06 comparten `challenges/01-intro`, que el estado es inmutable (frozen dataclasses), los seis módulos del juego y sus responsabilidades, el stack de tests, y qué no debe hacer Copilot.

### Instrucciones por tipo de archivo

**[`.github/instructions/testing.instructions.md`](../../.github/instructions/testing.instructions.md)**  
`applyTo: challenges/01-intro/tests/**` — Setup de SDL dummy driver, qué módulos testear, convención de nombres, ejemplos de fixtures y `parametrize`, y cómo verificar inmutabilidad.

**[`.github/instructions/features.instructions.md`](../../.github/instructions/features.instructions.md)**  
`applyTo: challenges/01-intro/**` — Tabla de routing para saber qué tipo de feature va en qué archivo, además de reglas estrictas de arquitectura.

**[`.github/instructions/python-tests.instructions.md`](../../.github/instructions/python-tests.instructions.md)**  
`applyTo: challenges/01-intro/tests/**/*.py` — Reglas adicionales de estilo `pytest` para archivos de tests Python.

### Agentes personalizados

**[`.github/agents/challenge-planner.agent.md`](../../.github/agents/challenge-planner.agent.md)**  
Adaptado del patrón `task-planner` de [Awesome GitHub Copilot](https://github.com/github/awesome-copilot). Agente de solo lectura que inspecciona el repo y produce planes concretos antes de implementar.

**[`.github/agents/tdd-refactor.agent.md`](../../.github/agents/tdd-refactor.agent.md)**  
Instalado desde la colección de [Awesome GitHub Copilot](https://github.com/github/awesome-copilot), basado en el agente `tdd-refactor`. Está aterrizado al repo para refactor seguro, mejora de calidad y endurecimiento de tests sin romper el juego.

## Cómo probarlo en VS Code

**Guía completa interactiva**: Consulta [`TEST-INSTRUCTIONS.md`](./TEST-INSTRUCTIONS.md) para pasos detallados con capturas esperadas.

### Verificación rápida (5 minutos)

1. **Abre este repo en VS Code**:
   ```bash
   cd /Users/gabriels/Proyectos/CopilotDay && code .
   ```

2. **Abre Copilot Chat**: `⌃⌘I` (macOS) o `Ctrl+Alt+I` (Windows/Linux)

3. **Verifica instrucciones personalizadas**: En el panel de Copilot, haz clic en el ícono de instrucciones — debería mostrar el contenido de `.github/copilot-instructions.md`

4. **Selecciona agente `Challenge Planner`** y prueba:
   ```
   Review the current repo and recommend the next safest challenge after Challenge 01.
   ```
   
   **Esperado**: Copilot analiza el repo, reconoce que 01-06 comparten `challenges/01-intro`, sugiere Challenge 03 (MCP), y menciona archivos específicos.

5. **Selecciona agente `TDD Refactor Phase`** y prueba:
   ```
   Review challenges/01-intro/game.py and suggest one small refactor that preserves behavior.
   ```
   
   **Esperado**: Copilot propone cambio pequeño, explica riesgos, sugiere cómo verificar con tests.

6. **Prueba instrucciones contextuales por archivo**: Abre [`challenges/01-intro/tests/test_board.py`](../../challenges/01-intro/tests/test_board.py) y solicita:
   ```
   Add a parametrized pytest test for edge case bounds checking following the existing pattern.
   ```
   
   **Esperado**: Copilot genera test con `@pytest.mark.parametrize`, fixtures locales, y convenciones pytest del proyecto.

## Qué deberías observar

### Respuestas contextuales
- Copilot **no** da respuestas genéricas sobre "Whack-a-Mole" — entiende tu arquitectura específica
- Reconoce que `challenges/01-intro` es la **base compartida** de challenges 01–06
- Distingue que challenge 07 es **independiente** del juego

### Adherencia a convenciones
- **Features**: Al sugerir nuevas características, Copilot orienta al módulo correcto (config → `config.py`, visuals → `renderer.py`, etc.)
- **Tests**: En archivos bajo `tests/`, Copilot usa `@pytest.mark.parametrize`, crea fixtures locales, y respeta el setup `SDL_VIDEODRIVER=dummy`
- **Código**: Sugiere frozen dataclasses, métodos que retornan nuevas instancias, nunca mutación en lugar

### Calidad de agentes
- **Challenge Planner**: Lee el repo, resume estado en 3-5 bullets, recomienda pasos concretos (read-only)
- **TDD Refactor**: Propone cambios pequeños, explica riesgos, verifica con tests (behavior-preserving)

## Estructura de archivos de personalización

```
.github/
├── copilot-instructions.md          ← Contexto global (permanente para todos los archivos)
├── agents/
│   ├── challenge-planner.agent.md   ← Agente read-only (planning, análisis)
│   └── tdd-refactor.agent.md        ← Agente behavior-preserving (refactor, tests)
└── instructions/
    ├── features.instructions.md     ← Para: challenges/01-intro/** (nuevas features)
    ├── testing.instructions.md      ← Para: challenges/01-intro/tests/** (estructura de tests)
    └── python-tests.instructions.md ← Para: challenges/01-intro/tests/**/*.py (estilo pytest)
```

### Cómo se aplican las instrucciones

| Instrucción | Scope | Aplica cuando |
|---|---|---|
| `copilot-instructions.md` | Global | Siempre (todo archivo del repo) |
| `features.instructions.md` | `challenges/01-intro/**` | Editas archivo de lógica del juego |
| `testing.instructions.md` | `challenges/01-intro/tests/**` | Editas o generas archivos de test |
| `python-tests.instructions.md` | `challenges/01-intro/tests/**/*.py` | Generas código en archivos pytest |

---

## Demostración para la validación del challenge

Para demostrar que cumpliste los success criteria, captura pantalla de:

1. **Custom instructions file** (`copilot-instructions.md`)
   - Abre Copilot Chat
   - Haz clic en ícono de instrucciones personalizadas
   - Screenshot mostrando el contenido (Project Context, Source Modules, Conventions)

2. **Custom agents seleccionables**
   - Selector de agentes en Copilot Chat
   - Screenshot con "Challenge Planner" y "TDD Refactor Phase" visibles

3. **Copilot respondiendo a instrucciones**
   - Ejemplo: Abrir [`challenges/01-intro/config.py`](../../challenges/01-intro/config.py)
   - Pedir: "Add a new config option following the next_difficulty() pattern"
   - Screenshot del código generado mostrando:
     - Enum con valores
     - Dict SETTINGS
     - Métodos `next_X()` / `prev_X()`
     - Frozen dataclass (inmutabilidad)

4. **Instrucciones contextuales por archivo**
   - Abrir archivo de test
   - Pedir test nuevo
   - Screenshot mostrando que Copilot usa `@pytest.mark.parametrize` y respeta fixtures

5. **Agente `Challenge Planner` funcionando**
   - Seleccionar agente en VS Code
   - Screenshot de respuesta a pregunta de planificación
   - Muestra análisis del repo + recomendaciones concretas

---

## Consejo: Troubleshooting

### Si no ves los agentes en VS Code
- Verifica que tienes **GitHub Copilot 0.44.2+** instalado
- Reinicia VS Code completamente
- Asegúrate de usar el **Copilot Chat integrado** (no desktop app)
- Verifica en VS Code Extension Marketplace que `GitHub Copilot Chat` está actualizado

### Si Copilot ignora tus instrucciones
- Verifica que `.github/copilot-instructions.md` existe en la **raíz del repo**
- Reinicia Copilot Chat (cierra y abre con `⌃⌘I`)
- Revisa **View → Output → GitHub Copilot** para mensajes de error
- Prueba con un prompt simple para verificar que detecta las instrucciones

### Si las instrucciones contextuales no aplican
- Verifica que el archivo tiene la ruta correcta (ej: `challenges/01-intro/tests/test_*.py`)
- Asegúrate que el `applyTo` en el YAML frontmatter usa patrones correctos (globbing)
- Prueba abrir/cerrar el archivo y reabrirlo

### Nota importante
Las custom instructions aplican a **solicitudes de chat**, pero **no** a las inline suggestions mientras escribes código.

---

## Para ir más allá

- Custom instructions: <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- Custom agents: <https://code.visualstudio.com/docs/copilot/customization/custom-agents>
- Primer custom agent en GitHub Docs: <https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents/your-first-custom-agent>
- Awesome GitHub Copilot: <https://github.com/github/awesome-copilot>

---

**Próximo**: [Challenge 05 - Dev Workflow](../05-dev-workflow/README.md)
