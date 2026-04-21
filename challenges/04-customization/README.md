# Challenge 04 - Personalización de GitHub Copilot en el IDE

Este reto usa el formato actual de VS Code donde la personalización se hace con:

- instrucciones globales en `.github/copilot-instructions.md`
- instrucciones por tipo de archivo en `.github/instructions/*.instructions.md`
- agentes personalizados en `.github/agents/*.agent.md`

## Qué se agregó

### Instrucciones globales

**[`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)**  
Define el contexto permanente del repo: que los challenges 01–06 comparten `challenges/01-intro`, que el estado es inmutable (frozen dataclasses), los seis módulos del juego y sus responsabilidades, el stack de tests, y qué no debe hacer Copilot (mutar estado, importar pygame en lógica, etc.).

### Instrucciones por tipo de archivo

**[`.github/instructions/testing.instructions.md`](../../.github/instructions/testing.instructions.md)**  
`applyTo: challenges/01-intro/tests/**` — Setup de SDL dummy driver, qué módulos testear, convención de nombres, ejemplos de fixtures y parametrize, cómo verificar inmutabilidad.

**[`.github/instructions/features.instructions.md`](../../.github/instructions/features.instructions.md)**  
`applyTo: challenges/01-intro/**` — Tabla de routing (qué tipo de feature va en qué archivo), patrones de código para nueva config, nuevas pantallas y reglas estrictas de arquitectura.

**[`.github/instructions/python-tests.instructions.md`](../../.github/instructions/python-tests.instructions.md)**  
`applyTo: challenges/01-intro/tests/**/*.py` — Reglas adicionales de estilo pytest para archivos de test Python.

### Agente personalizado

**[`.github/agents/challenge-planner.agent.md`](../../.github/agents/challenge-planner.agent.md)**  
Adaptado del patrón `task-planner` de [Awesome GitHub Copilot](https://github.com/github/awesome-copilot). Agente de solo lectura que inspecciona el repo y produce planes concretos antes de implementar.

## Cómo probarlo en VS Code

1. Abre este repo en VS Code.
2. Abre **Copilot Chat** (⌃⌘I en macOS / Ctrl+Alt+I en Windows).
3. Verifica que VS Code detecte `.github/copilot-instructions.md` (aparece en la UI del chat).
4. En el selector de agentes (ícono de modo), elige **Challenge Planner**.
5. Prueba estos prompts:

```
Review the current repo and recommend the next safest challenge after 01.
```

```
Plan Challenge 02 on top of the current Whack-a-Mole codebase and list the files that should change first.
```

```
Explain how the current CI and test structure should influence Challenge 06.
```

## Qué deberías observar

- Copilot debería responder con contexto del repo, no con respuestas genéricas.
- Debería reconocer que `challenges/01-intro` es la base compartida de los challenges 01–06.
- Debería distinguir que el challenge 07 es independiente del juego.
- En archivos de tests, debería sugerir estilo `pytest` y respetar el setup headless de pygame.
- Al sugerir nuevas features, debería orientarte al módulo correcto (lógica en `game.py`, rendering en `renderer.py`).

## Nota importante

Las custom instructions aplican a solicitudes de chat (agent mode y ask mode), pero **no** a las inline suggestions mientras escribes. Las sugerencias de autocompletado siguen usando el contexto local del archivo.

## Fuentes

- Custom instructions: <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- Custom agents: <https://code.visualstudio.com/docs/copilot/customization/custom-agents>
- Awesome GitHub Copilot: <https://github.com/github/awesome-copilot>
