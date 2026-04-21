# Custom Instructions & Agents - Quick Reference

Este documento es una guía rápida para entender la estructura de personalización de GitHub Copilot en este repo.

---

## 📋 Estructura de Archivos

```
.github/
├── copilot-instructions.md              (Global context)
├── agents/
│   ├── challenge-planner.agent.md       (Planning agent - read-only)
│   └── tdd-refactor.agent.md            (Refactoring agent - behavior-preserving)
└── instructions/
    ├── features.instructions.md         (For: challenges/01-intro/**)
    ├── testing.instructions.md          (For: challenges/01-intro/tests/**)
    └── python-tests.instructions.md     (For: challenges/01-intro/tests/**/*.py)
```

---

## 🎯 Instrucciones Globales

**File**: `.github/copilot-instructions.md`

**Applies to**: Every file in the repo

**Purpose**: Define permanent context that Copilot needs to understand:

- Project is a learning workspace (WhatTheHack 071)
- Challenges 01-06 share `challenges/01-intro` codebase
- Challenge 07 is independent
- Game state is **immutable** (frozen dataclasses)
- Architecture: 6 modules with clear separation

**Example impact**:
```
User asks: "How should I store the current difficulty?"
Copilot responds: "Add a field to GameConfig (frozen dataclass) 
and create next_difficulty() method, following the existing pattern."
```

---

## 🎯 File-Scoped Instructions

### 1. features.instructions.md

**File**: `.github/instructions/features.instructions.md`

**Applies to**: `challenges/01-intro/**` (all game logic files)

**When**: When you ask Copilot to add a new feature to the game

**What it teaches**:
- Where each type of feature goes (config/mole/board/game/renderer)
- Pattern for new config options (Enum + SETTINGS dict + next_X/prev_X)
- Pattern for new game screens (renderer.py → draw_X function)
- Strict rules (no pygame in logic, frozen dataclasses, etc.)

**Example impact**:
```
User: "Add a sound toggle to the settings"
→ Copilot suggests config.py (not main.py or renderer.py)
→ Creates SoundLevel enum with OFF/LOW/HIGH
→ Adds next_sound_level() / prev_sound_level() methods
→ Returns new GameConfig instance (immutable)
```

---

### 2. testing.instructions.md

**File**: `.github/instructions/testing.instructions.md`

**Applies to**: `challenges/01-intro/tests/**` (all test directories)

**When**: When you ask Copilot to write or improve tests

**What it teaches**:
- SDL dummy driver setup (for headless testing)
- Which modules to test (logic, not renderer)
- Test naming convention (test_module_behavior)
- Fixture patterns (parametrize, scope, autouse)
- Immutability verification (return new instances)

**Example impact**:
```
User: "Write a test for the difficulty cycling"
→ Copilot uses @pytest.mark.parametrize
→ Creates fixture `default_config()`
→ Test verifies new instances returned (immutability)
→ Respects SDL_VIDEODRIVER=dummy setup
```

---

### 3. python-tests.instructions.md

**File**: `.github/instructions/python-tests.instructions.md`

**Applies to**: `challenges/01-intro/tests/**/*.py` (all Python test files)

**When**: When generating pytest code specifically

**What it teaches**:
- Use pytest style (not unittest)
- Descriptive names over implementation details
- Keep fixtures small and reusable
- Preserve headless pygame setup
- Avoid flaky tests (no random without control)

**Example impact**:
```
User: "Create a fixture for a board in PLAYING state"
→ @pytest.fixture decorator
→ Name: playing_board (descriptive)
→ Returns Board instance with correct size
→ Small fixture (focused responsibility)
```

---

## 🤖 Agents (Chat Modes)

### Challenge Planner (Read-Only)

**File**: `.github/agents/challenge-planner.agent.md`

**Purpose**: Plan next steps before implementation

**How to use**:
1. Open Copilot Chat
2. Select **Challenge Planner** from agent dropdown
3. Ask planning questions

**Type of responses**:
- Current repo state summary (3-5 bullets)
- Recommended next step (concrete and small)
- Files likely involved
- Risks or dependencies
- **Never edits code** (read-only)

**Example prompts**:
```
"What should we do after Challenge 02?"
"Plan Challenge 05 work and list files to touch first"
"Analyze test coverage — what's missing?"
```

---

### TDD Refactor Phase (Behavior-Preserving)

**File**: `.github/agents/tdd-refactor.agent.md`

**Purpose**: Improve code quality without changing behavior

**How to use**:
1. Open Copilot Chat
2. Select **TDD Refactor Phase - Improve Quality & Security** from agent dropdown
3. Ask refactoring questions

**Type of responses**:
- Behavior-preserving refactors (no logic changes)
- Quality improvements (readability, safety, maintainability)
- Testing strategy to validate changes
- Risks identified
- How to keep tests green

**Example prompts**:
```
"Refactor board.py for readability without changing behavior"
"Improve test coverage in test_game.py"
"Suggest a small change that reduces duplication"
```

---

## 🔄 How VS Code Applies Instructions

```
┌─────────────────────────────────────────────────────┐
│ User asks Copilot something in Chat                │
├─────────────────────────────────────────────────────┤
│ 1. Load .github/copilot-instructions.md (global)  │
│ 2. Check current file path                        │
│ 3. Find matching .instructions.md (by applyTo)    │
│ 4. Load matching agent (if selected)              │
│ 5. Combine all context                            │
│ 6. Generate response aligned to instructions      │
└─────────────────────────────────────────────────────┘
```

### Example: Adding a new feature

```
Current file: challenges/01-intro/config.py

Instructions loaded (in order):
  1. copilot-instructions.md         ← Global rules
  2. features.instructions.md        ← Matches challenges/01-intro/**
  3. challenge-planner agent (if)    ← Selected agent

Result: Copilot knows:
  ✓ Whack-a-Mole game structure
  ✓ Frozen dataclass pattern
  ✓ Module routing (this is config.py)
  ✓ Naming conventions
  ✓ How to add config options
```

---

## ✅ Validation

### Quick Test: Are Instructions Working?

**Test 1 - Global instructions**:
```
Open Copilot Chat → Check custom instructions shown
Should see sections: Project Context, Source Modules, etc.
```

**Test 2 - Feature-scoped instructions**:
```
Open challenges/01-intro/config.py
Ask: "Add a lives field with next_lives() and prev_lives()"
Should get: Enum + SETTINGS dict + methods (frozen dataclass pattern)
```

**Test 3 - Test-scoped instructions**:
```
Open challenges/01-intro/tests/test_config.py
Ask: "Add parametrized test for lives cycling"
Should get: @pytest.mark.parametrize + fixture + immutability check
```

**Test 4 - Agents**:
```
Select Challenge Planner agent
Ask: "What's the next challenge after 02?"
Should get: Analysis + concrete recommendation (no code)
```

---

## 🚀 Pro Tips

### Maximize Instruction Impact

1. **Be specific about file location** in prompts
   ```
   Good: "In challenges/01-intro/config.py, add..."
   Better: [Open the file first, then ask]
   ```

2. **Reference existing patterns**
   ```
   Good: "Following the next_difficulty() pattern..."
   Better: [Open config.py with next_difficulty() visible]
   ```

3. **Use agents for specialized tasks**
   ```
   Planning? → Use Challenge Planner
   Refactoring? → Use TDD Refactor Phase
   General coding? → Default agent
   ```

4. **Include test context**
   ```
   "Add feature X. Show me how to test it using the 
    @pytest.mark.parametrize pattern from test_config.py"
   ```

---

## 📚 Learn More

- [VS Code Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Awesome GitHub Copilot](https://github.com/github/awesome-copilot)
- [Challenge 04 README](./README.md) - Full context

---

**Status**: ✅ Challenge 04 Complete

**Next**: [Challenge 05 - Dev Workflow](../05-dev-workflow/README.md)
