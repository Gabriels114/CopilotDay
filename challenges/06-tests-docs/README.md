# Challenge 06 — Tests y Documentación con Copilot

En este reto explorarás la suite de tests ya creada para el juego Whack-a-Mole, aprenderás a ejecutarlos, a usar Copilot para generar tests adicionales y a documentar código con docstrings de calidad.

---

## 1. Estructura de tests ya creada

Los tests están en `challenges/01-intro/tests/`:

```
challenges/01-intro/
├── config.py
├── mole.py
├── board.py
├── game.py
└── tests/
    ├── conftest.py       # Inicialización de pygame (fixture de sesión)
    ├── test_config.py    # Tests para GameConfig
    ├── test_mole.py      # Tests para Mole y MoleState
    ├── test_board.py     # Tests para Board
    └── test_game.py      # Tests para GameState y Phase
```

### Descripción de cada archivo

| Archivo | Qué prueba |
|---------|-----------|
| `conftest.py` | Inicializa pygame con drivers dummy (sin pantalla real) para que todos los tests funcionen en CI |
| `test_config.py` | Valores por defecto, propiedades `grid_rows`/`grid_cols`, ciclado de `next_size`, `prev_size`, `next_duration`, `prev_duration`, inmutabilidad |
| `test_mole.py` | Máquina de estados (HIDDEN → RISING → VISIBLE → FALLING → HIDDEN), `spawn()`, `whack()`, `is_whackable()`, inmutabilidad |
| `test_board.py` | Creación con `Board.create()`, `get(row,col)`, `update()`, `try_spawn()`, `try_whack()`, inmutabilidad |
| `test_game.py` | `GameState.menu()`, `start()`, `update()` (transiciones de fase), `whack()` (score), `with_config()`, inmutabilidad |

---

## 2. Ejecutar tests localmente

Desde el directorio `challenges/01-intro/`, ejecuta:

```bash
# Instalar dependencias de testing (solo la primera vez)
pip install pytest pytest-cov

# Ejecutar todos los tests con reporte de cobertura
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
  pytest tests/ --cov=. --cov-report=term-missing -v
```

Las variables de entorno `SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy` le indican a pygame que no intente abrir una ventana ni acceder al audio — esenciales para correr tests sin interfaz gráfica.

### Comandos útiles

```bash
# Solo un archivo de tests
pytest tests/test_mole.py -v

# Solo tests que contengan "whack" en el nombre
pytest tests/ -k "whack" -v

# Ver qué líneas no están cubiertas
pytest tests/ --cov=. --cov-report=term-missing

# Fallar si la cobertura baja del 80%
pytest tests/ --cov=. --cov-fail-under=80

# Generar reporte HTML de cobertura
pytest tests/ --cov=. --cov-report=html
# Luego abre htmlcov/index.html en el navegador
```

---

## 3. Usar Copilot para generar tests adicionales

### Método 1: Completado automático en el editor

Abre cualquier archivo de tests existente, escribe el inicio de una función de test y deja que Copilot complete:

```python
def test_mole_whack_flash_decreases_to_zero_over_time():
    # Copilot completará el cuerpo del test
```

### Método 2: Copilot Chat con contexto

Abre `mole.py` y en el chat escribe:

```
Genera tests de pytest para el método `update()` de la clase `Mole`
cuando el estado es `WHACKED`. Cubre: disminución de `whack_flash`,
disminución de `progress`, y la transición a `HIDDEN` cuando `progress <= 0`.
Usa el estilo de los tests existentes en tests/test_mole.py.
```

### Método 3: Desde el código fuente

Selecciona una función en el código fuente (por ejemplo, `try_spawn` en `board.py`), haz clic derecho → **Copilot** → **Generate Tests**.

### Qué agregar para mejorar la cobertura

Areas con oportunidad de mejora:

- **`config.py`:** Tests con valores no-default para `mole_visible_time` y `mole_spawn_interval`
- **`board.py`:** Tests de `try_spawn` con tableros parcialmente llenos (algunos HIDDEN, algunos no)
- **`game.py`:** Tests del timer de spawn con múltiples actualizaciones consecutivas
- **`mole.py`:** Tests de `update()` con dt=0 (sin cambio de estado)

Ejemplo de prompt para Copilot:

```
En tests/test_board.py, agrega tests para el caso donde el tablero tiene
exactamente una celda HIDDEN y el resto no-HIDDEN. Verifica que try_spawn
siempre elige esa única celda disponible.
```

---

## 4. Tests integrados al pipeline de CI

Los tests corren automáticamente en cada push y PR gracias al workflow en `.github/workflows/ci.yml`. El pipeline:

1. Instala las dependencias del sistema (libSDL2) y de Python
2. Corre `pytest` con cobertura mínima del 80%
3. Falla el build si la cobertura cae por debajo del umbral
4. Sube el reporte de cobertura como artefacto descargable

Si agregas nuevos tests, se ejecutarán automáticamente en el próximo push. No requiere configuración adicional.

---

## 5. Cobertura actual y áreas de mejora

### Qué cubren los tests actuales

- Todas las transiciones de estado de `Mole` (HIDDEN → RISING → VISIBLE → FALLING → HIDDEN, y WHACKED)
- La inmutabilidad de `Mole`, `Board`, `GameState` y `GameConfig`
- Todas las operaciones de `Board` incluyendo casos borde (tablero lleno, celda no whackable)
- El ciclo completo de `GameState`: menú → juego → game over
- Todos los métodos de ciclo de `GameConfig` con wrap-around

### Áreas que podrían mejorarse

| Área | Mejora posible |
|------|---------------|
| `renderer.py` | Tests de renderizado con superficie dummy de pygame |
| `board.py` | Property-based testing con `hypothesis` para tableros de tamaños aleatorios |
| `game.py` | Tests de integración que simulen un juego completo de principio a fin |
| `mole.py` | Tests con dt muy pequeños (near-zero) para verificar estabilidad numérica |

---

## 6. Documentar código con docstrings

Los docstrings permiten que Copilot entienda mejor el código y genere sugerencias más precisas. También son la base de la documentación automática.

### Formato recomendado (Google Style)

```python
def try_whack(self, row: int, col: int) -> Tuple["Board", bool]:
    """Intenta golpear al topo en la posición (row, col).

    Si el topo en esa posición es whackable (estado RISING o VISIBLE),
    lo marca como WHACKED y retorna el tablero actualizado con True.
    Si no es whackable, retorna el mismo tablero con False.

    Args:
        row: Fila del topo a golpear (0-indexed).
        col: Columna del topo a golpear (0-indexed).

    Returns:
        Tuple con el nuevo Board (o el mismo si no hubo golpe) y un
        booleano indicando si el golpe fue exitoso.

    Example:
        >>> board = Board.create(3, 3)
        >>> board, hit = board.try_whack(0, 0)
        >>> hit
        False  # Todos los topos están HIDDEN al inicio
    """
```

### Documentar una clase completa

```python
@dataclass(frozen=True)
class GameConfig:
    """Configuración inmutable del juego Whack-a-Mole.

    Define el tamaño de la grilla, la duración de la partida y los
    parámetros de comportamiento de los topos. Todos los métodos de
    mutación retornan una nueva instancia — esta clase nunca se modifica
    en lugar.

    Attributes:
        grid_size: Tamaño de la grilla cuadrada (3, 4 o 5).
        game_duration: Duración de la partida en segundos.
        mole_visible_time: Tiempo máximo que un topo permanece visible.
        mole_spawn_interval: Segundos entre apariciones de topos.
    """
```

### Usar Copilot para generar docstrings

1. Coloca el cursor dentro de una función sin docstring.
2. En Copilot Chat escribe: `/doc` o "Genera un docstring para esta función".
3. Copilot analizará el cuerpo de la función y generará la documentación.

Alternativa: escribe `"""` justo debajo de `def nombre_funcion():` y Copilot completará el docstring automáticamente.

### Generar documentación HTML con pdoc

```bash
pip install pdoc

# Genera docs HTML para todos los módulos
SDL_VIDEODRIVER=dummy pdoc mole.py board.py config.py game.py --output-dir docs/

# Abre docs/index.html en el navegador
```

---

## 7. Tips para usar Copilot en testing y documentación

**Para tests:**
- Describe el comportamiento esperado en un comentario antes de la función — Copilot lo convertirá en código
- Usa `pytest.mark.parametrize` con ejemplos concretos y pide a Copilot que los amplíe
- Pregunta: "¿Qué casos borde podría estar perdiendo en este test?"

**Para documentación:**
- Selecciona un módulo completo y pide: "Agrega docstrings Google-style a todas las funciones públicas"
- Pide a Copilot que genere ejemplos de uso en los docstrings: "Incluye un ejemplo de `Example:` en cada docstring"
- Usa `/explain` sobre código complejo para entenderlo antes de documentarlo

**Flujo recomendado:**
1. Escribe el código
2. Usa Copilot para generar los tests (`/tests`)
3. Usa Copilot para generar los docstrings (`/doc`)
4. Verifica que los tests pasan: `pytest tests/ --cov=. --cov-fail-under=80`
5. Haz push — el CI verificará todo automáticamente
