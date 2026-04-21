# Copilot Instructions For This Repository

This repository tracks progress for `WhatTheHack 071 - GitHub Copilot`.

## Project Context

- Treat the repository as a challenge-based learning workspace, not as a polished production monolith.
- Challenges `01` through `06` evolve the same `Whack-a-Mole` project under `challenges/01-intro`.
- Challenge `07` is independent and lives under `challenges/07-debug-optimization`.
- Prefer extending the existing challenge structure instead of creating unrelated top-level projects.

## Working Style

- Preserve the current architecture unless there is a clear reason to simplify it.
- Prefer small, reviewable changes over broad rewrites.
- When suggesting a change, mention the concrete files that should be touched.
- Explain tradeoffs briefly when proposing refactors or new dependencies.
- Do not invent frameworks, services, or files that do not exist in the workspace.

## Source Modules (challenges/01-intro)

| File | Responsibility |
|---|---|
| `config.py` | `GameConfig` frozen dataclass + `COLORS` dict. No pygame. |
| `mole.py` | `MoleState` enum + `Mole` frozen dataclass (state machine). No pygame. |
| `board.py` | `Board` frozen dataclass — flat tuple of `Mole`s, spawn/whack logic. No pygame. |
| `game.py` | `Phase` enum + `GameState` frozen dataclass — timer, score, phase transitions. No pygame. |
| `renderer.py` | All `pygame.draw` calls. No game logic. Imports `config`, `mole`, `board`, `game` types only. |
| `main.py` | `pygame.init()` + 60 FPS event loop. Wires events to `GameState` transitions. |

Game phases: `MENU → PLAYING → GAMEOVER`. `update(dt)` is a no-op outside `PLAYING`.

## Python Conventions

- All game state is **immutable**: every state transition returns a new frozen dataclass instance. Never mutate existing objects with `object.field = value`.
- `pygame` must not be imported in `config.py`, `mole.py`, `board.py`, or `game.py`.
- Follow the style already present in `challenges/01-intro`.
- Prefer dataclasses, small pure methods, and explicit state transitions.
- Keep imports simple and consistent with the current flat module layout.
- Preserve type hints when editing Python files.
- Avoid unnecessary abstraction for this project size.

## Testing Expectations

- Prefer `pytest` for Python tests because that is the stack already in use.
- When changing game logic, suggest or add tests near the affected behavior.
- Keep tests deterministic and focused on observable behavior.
- For pygame-related tests, preserve the current headless test setup.

## Documentation Expectations

- Keep README content action-oriented.
- When documenting a challenge, include: objective, what was added, how to run it, and how to prove success.
- If a feature depends on IDE behavior, say explicitly what the user should do in VS Code to verify it.

## Safety

- Do not remove challenge folders or restructure the repo without a clear request.
- Do not overwrite user work or generated challenge evidence.
- If the request is ambiguous, prefer asking for the next smallest useful step.
