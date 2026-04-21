---
applyTo: "challenges/01-intro/tests/**"
---

# Testing Instructions

## Setup Obligatorio

Siempre configura las variables de entorno antes de importar pygame:

```python
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
```

Esto ya está en `conftest.py` — no lo dupliques en cada archivo de tests.

## Qué Testear

Testea los módulos de lógica pura: `mole.py`, `board.py`, `game.py`, `config.py`.
No testees `renderer.py` directamente (requiere display).

## Naming Convention

```
test_<module>_<behavior>
test_mole_whack_sets_whacked_state
test_board_try_spawn_picks_hidden_mole
test_gamestate_update_decrements_timer
```

## Fixtures

Usa el fixture `pygame_init` de `conftest.py` (scope=session, autouse=True).

Para objetos de juego comunes:

```python
@pytest.fixture
def default_config():
    return GameConfig()

@pytest.fixture
def fresh_board():
    return Board.create(3, 3)

@pytest.fixture
def playing_state():
    return GameState.menu(GameConfig()).start()
```

## Parametrize para Transiciones de Estado

```python
@pytest.mark.parametrize("state,whackable", [
    (MoleState.HIDDEN,  False),
    (MoleState.RISING,  True),
    (MoleState.VISIBLE, True),
    (MoleState.FALLING, False),
    (MoleState.WHACKED, False),
])
def test_mole_is_whackable(state, whackable):
    mole = Mole(state=state, progress=0.5)
    assert mole.is_whackable() == whackable
```

## Verificar Inmutabilidad

Siempre verifica que los métodos retornen nuevas instancias:

```python
def test_mole_update_returns_new_instance():
    original = Mole().spawn()
    updated = original.update(0.1, 1.5)
    assert updated is not original
    assert original.state == MoleState.RISING  # sin cambios
```
