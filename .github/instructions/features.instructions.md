---
applyTo: "challenges/01-intro/**"
---

# Feature Development Instructions

## Dónde Va Cada Cosa

| Qué quieres agregar | Archivo |
|---|---|
| Nueva opción de configuración | `config.py` → campo en `GameConfig` + métodos `next_X()`/`prev_X()` |
| Nuevo comportamiento de topo | `mole.py` → caso en `MoleState` + rama en `Mole.update()` |
| Nuevo evento de juego | `game.py` → lógica en `GameState.update()` o `GameState.whack()` |
| Nuevo elemento visual | `renderer.py` → función `draw_X()`, llamada desde `draw_grid()` o `draw_hud()` |
| Nueva pantalla | `renderer.py` → función `draw_X_screen()`, retorna dict de button rects |

## Patrón para Nueva Config

```python
# config.py
MY_OPTIONS = [opt1, opt2, opt3]

@dataclass(frozen=True)
class GameConfig:
    my_option: int = opt1
    # ...

    def next_my_option(self) -> 'GameConfig':
        idx = MY_OPTIONS.index(self.my_option)
        return GameConfig(..., my_option=MY_OPTIONS[(idx + 1) % len(MY_OPTIONS)])
```

## Patrón para Nueva Pantalla en el Menú

```python
# renderer.py
def draw_menu(surface, state, ..., mouse_pos) -> dict:
    # ...
    # Agrega tu nuevo control aquí
    # Retorna sus rects en el dict
    return {
        'prev_size': ..., 'next_size': ...,
        'prev_dur': ..., 'next_dur': ...,
        'prev_my_option': ..., 'next_my_option': ...,  # nuevo
        'play': ...,
    }

# main.py — maneja el click
if event.type == pygame.MOUSEBUTTONDOWN:
    if button_rects.get('next_my_option', pygame.Rect(0,0,0,0)).collidepoint(event.pos):
        state = state.with_config(state.config.next_my_option())
```

## Reglas Estrictas

- Nunca pongas código de pygame en `game.py`, `board.py`, `mole.py`, o `config.py`
- Nunca importes `game.py` o `board.py` desde `renderer.py` — usa los tipos como parámetros
- Toda transición de estado retorna una nueva instancia (dataclass frozen)
- Agrega tests para cualquier lógica nueva en `tests/`
