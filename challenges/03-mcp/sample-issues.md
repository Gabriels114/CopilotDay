# Sample GitHub Issues — Whack-a-Mole

Crea estos issues en el repo `Gabriels114/CopilotDay` para el Challenge 03.

---

## Issue 1: Add sound effects

**Labels**: `feature`, `game-mechanic`

**Body**:
Add hit and miss sound effects to improve game feel.

- Play a "whack" sound when a mole is hit (`pygame.mixer.Sound`)
- Play a "miss" sound when the player clicks an empty hole
- Play a countdown beep in the last 5 seconds
- All sounds should be generated programmatically (no audio files needed) using `numpy` + `pygame.sndarray`

---

## Issue 2: Leaderboard / High Score Persistence

**Labels**: `feature`, `ux`

**Body**:
Persist the top 5 scores between sessions.

- Save scores to `~/.whackamole_scores.json`
- Display leaderboard on the Game Over screen
- Include: score, grid_size, duration, timestamp
- Handle file not found gracefully (first run)

---

## Issue 3: Difficulty Levels

**Labels**: `feature`, `game-mechanic`

**Body**:
Add Easy / Medium / Hard / Insane difficulty presets.

| Difficulty | mole_visible_time | mole_spawn_interval |
|---|---|---|
| Easy | 2.0s | 1.5s |
| Medium | 1.4s | 0.9s |
| Hard | 0.9s | 0.6s |
| Insane | 0.5s | 0.4s |

- Add `difficulty` field to `GameConfig`
- Show difficulty selector in menu
- Difficulty affects score multiplier (Easy=1x, Medium=2x, Hard=3x, Insane=5x)

---

## Issue 4: Particle Effects on Whack

**Labels**: `feature`, `ux`

**Body**:
Add a particle burst effect when a mole is whacked.

- Emit 10–15 small colored particles from the mole's position
- Particles move outward with random velocities
- Particles fade out over ~0.4 seconds
- Use gold/yellow color to match the whack flash
- Implement in `renderer.py` — particle state lives in `GameState`

---

## Issue 5: Accessibility — Keyboard Mode

**Labels**: `feature`, `ux`

**Body**:
Allow playing the game without a mouse.

- Number keys 1–9 map to grid cells (1=top-left, 9=bottom-right for 3×3)
- Visual highlight shows which cell is selected via keyboard
- Press Space or Enter to whack the selected cell
- Tab cycles through cells

---

## Issue 6: Multiple Moles Active Simultaneously

**Labels**: `feature`, `game-mechanic`

**Body**:
Allow more than one mole to be active at once as the game progresses.

- Start with max 1 active mole
- After 10 seconds, allow up to 2 simultaneous moles
- After 20 seconds, allow up to 3
- Add `max_active_moles` property to `GameConfig` or compute dynamically from elapsed time
- Missed moles (fall back down without being whacked) subtract 1 point

---

## Issue 7: Power-Ups

**Labels**: `feature`, `game-mechanic`

**Body**:
Add special golden moles that grant power-ups when whacked.

- Golden mole: appears rarely (10% chance), worth 5 points
- Freeze mole: appears and pauses the timer for 3 seconds when whacked
- Double-point mole: next whack counts as 2 points
- Render with different colors to distinguish from regular moles

---

## Issue 8: CI Badge in README

**Labels**: `devops`

**Body**:
Add a GitHub Actions CI badge to the project README.

```markdown
![CI](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml/badge.svg)
```

Verify the badge shows green after the CI pipeline runs successfully.
