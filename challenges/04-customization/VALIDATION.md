# Challenge 04 - Validation Checklist

Use this checklist to verify that Challenge 04 is complete and all customizations are working.

## Pre-check: File Structure Validation

```bash
# Verify all required files exist
find .github -type f -name "*.md" | grep -E "(copilot-instructions|agents|instructions)"
```

**Expected output:**
```
.github/copilot-instructions.md
.github/agents/challenge-planner.agent.md
.github/agents/tdd-refactor.agent.md
.github/instructions/features.instructions.md
.github/instructions/testing.instructions.md
.github/instructions/python-tests.instructions.md
```

---

## Checkpoint 1: Global Instructions Detected

**Action**: Open VS Code and check if global instructions are loaded

```bash
1. Open Copilot Chat (⌃⌘I on macOS)
2. Look for "Custom instructions" indicator
3. Click to view content
```

**Verify**:
- [ ] `.github/copilot-instructions.md` detected by VS Code
- [ ] Content includes sections: Project Context, Source Modules, Python Conventions, Testing Expectations
- [ ] No YAML syntax errors in the file

**File to check**: [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md)

---

## Checkpoint 2: File-Scoped Instructions Validation

### For features.instructions.md

**Action**: Open [`challenges/01-intro/config.py`](../../challenges/01-intro/config.py)

```
In Copilot Chat, type:
  "Add a color_mode config option with LIGHT, DARK, AUTO following the 
   next_difficulty() pattern. Return a new GameConfig instance when cycled."
```

**Verify**:
- [ ] Copilot generates Enum with three values
- [ ] Generates `COLOR_MODE_SETTINGS` dict (parallel to `DIFFICULTY_SETTINGS`)
- [ ] Creates `next_color_mode()` and `prev_color_mode()` methods
- [ ] Uses frozen dataclass (no in-place mutation)
- [ ] Suggests adding property for accessing the setting

**File to check**: [`.github/instructions/features.instructions.md`](../../.github/instructions/features.instructions.md)

---

### For testing.instructions.md

**Action**: Open [`challenges/01-intro/tests/test_config.py`](../../challenges/01-intro/tests/test_config.py)

```
In Copilot Chat, type:
  "Add a parametrized pytest test for color_mode cycling. Use @pytest.mark.parametrize 
   with the pattern already in this file."
```

**Verify**:
- [ ] Uses `@pytest.mark.parametrize("mode,next_mode", [...])`
- [ ] Follows existing fixture pattern (`default_config`)
- [ ] Test name is `test_config_color_mode_cycles` (or similar)
- [ ] Verifies immutability (original config unchanged)
- [ ] SDL_VIDEODRIVER/AUDIODRIVER setup honored (headless)

**File to check**: [`.github/instructions/testing.instructions.md`](../../.github/instructions/testing.instructions.md)

---

### For python-tests.instructions.md

**Action**: Open any file under `challenges/01-intro/tests/`

```
Request:
  "Create a pytest fixture that returns a GameState in PLAYING phase 
   with difficulty set to HARD."
```

**Verify**:
- [ ] Uses `@pytest.fixture` decorator
- [ ] Has descriptive name (e.g., `hard_playing_state`)
- [ ] Returns proper type (GameState)
- [ ] Follows local fixture pattern (not module-level)
- [ ] Test-focused naming

**File to check**: [`.github/instructions/python-tests.instructions.md`](../../.github/instructions/python-tests.instructions.md)

---

## Checkpoint 3: Custom Agents Verification

### Agent 1: Challenge Planner

**Action**: 
1. Open Copilot Chat
2. Select "Challenge Planner" from agent dropdown
3. Type: `"Analyze challenges 01-02 and recommend what should come next."`

**Verify**:
- [ ] Agent responds with 3-5 bullet summary of current state
- [ ] Identifies that challenges 01-06 share `challenges/01-intro`
- [ ] Suggests concrete next step (e.g., Challenge 03 MCP)
- [ ] Mentions specific files or areas to focus on
- [ ] **Does NOT edit code** (read-only agent)
- [ ] Response references repo structure correctly

**File to check**: [`.github/agents/challenge-planner.agent.md`](../../.github/agents/challenge-planner.agent.md)

---

### Agent 2: TDD Refactor Phase

**Action**:
1. Open Copilot Chat  
2. Select "TDD Refactor Phase - Improve Quality & Security" agent
3. Type: `"Review challenges/01-intro/board.py and suggest one behavior-preserving refactor."`

**Verify**:
- [ ] Agent analyzes the file correctly
- [ ] Suggests small change (not major rewrite)
- [ ] Preserves existing behavior
- [ ] Explains testing strategy to validate change
- [ ] Mentions how to keep tests green
- [ ] References `pytest` as testing framework

**File to check**: [`.github/agents/tdd-refactor.agent.md`](../../.github/agents/tdd-refactor.agent.md)

---

## Checkpoint 4: Context-Aware Behavior

### Test 1: Architecture Understanding

```
In Copilot Chat with Challenge Planner agent:
  "Why should pygame never be imported in config.py or game.py?"
```

**Verify**:
- [ ] Agent references `.github/copilot-instructions.md`
- [ ] Explains the separation: logic modules vs. renderer
- [ ] Mentions benefits (testability, modularity)
- [ ] Connects to current project structure

---

### Test 2: Immutability Understanding

```
In Copilot Chat (any agent):
  "Show me an example of immutable state transition in game.py"
```

**Verify**:
- [ ] References frozen dataclass pattern
- [ ] Shows example of returning new instance
- [ ] Explains why no in-place mutation
- [ ] Matches actual code style

---

### Test 3: File-Specific Routing

**Open** [`challenges/01-intro/renderer.py`](../../challenges/01-intro/renderer.py)

```
Request: "Add a visual indicator for difficulty level in the HUD"
```

**Verify**:
- [ ] Suggests adding drawing function in `renderer.py` (correct file)
- [ ] Suggests modifying `draw_hud()` to call new function
- [ ] Does NOT suggest adding logic to `config.py` or `game.py`
- [ ] Follows existing `draw_*()` pattern

---

## Final Validation Checklist

| Item | Status |
|------|--------|
| All instruction files exist with correct paths | ☐ |
| `.github/copilot-instructions.md` detected by VS Code | ☐ |
| `challenge-planner.agent.md` selectable in Copilot Chat | ☐ |
| `tdd-refactor.agent.md` selectable in Copilot Chat | ☐ |
| `features.instructions.md` applied to game feature requests | ☐ |
| `testing.instructions.md` applied to test generation | ☐ |
| `python-tests.instructions.md` applied to pytest fixtures | ☐ |
| Copilot understands frozen dataclass immutability pattern | ☐ |
| Copilot knows pygame restrictions (not in logic modules) | ☐ |
| Copilot recognizes module routing (config/mole/board/game/renderer) | ☐ |
| Both agents are read-only / behavior-preserving as intended | ☐ |
| Instructions respect existing code style and conventions | ☐ |

---

## Troubleshooting

### Agents not appearing in dropdown

```bash
# Verify file format has YAML frontmatter
head -5 .github/agents/challenge-planner.agent.md
# Should show: ---
#             name: Challenge Planner
#             ...
```

### Instructions not being applied

```bash
# Verify applyTo pattern in instruction files
grep -n "applyTo" .github/instructions/*.md
# Check that patterns match file paths (use globbing correctly)
```

### No "Custom instructions" indicator in VS Code

- Restart VS Code completely
- Check VS Code version: `code --version`
- Verify GitHub Copilot extension version 0.44.2+
- Check `.github/copilot-instructions.md` exists in repo root

---

## Success Criteria Met

✅ **Custom instructions file**: `.github/copilot-instructions.md` created and detected  
✅ **Custom agents**: Two agents installed and selectable  
✅ **Context-aware responses**: Copilot follows project conventions  
✅ **File-scoped instructions**: Applied based on file paths  

---

**Next Step**: Move to [Challenge 05 - Dev Workflow](../05-dev-workflow/README.md)
