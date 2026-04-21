# Challenge 02 — Mejores Prácticas de Prompt Engineering

Documentación de las técnicas de prompt engineering utilizadas para implementar la feature **Difficulty Levels** en el juego Whack-a-Mole con GitHub Copilot.

---

## Resumen de técnicas

| # | Técnica | Impacto observado |
|---|---------|-------------------|
| 1 | Empezar general, luego ser específico | Copilot generó ~90 % del código final con el prompt v3 sin necesidad de ajustes manuales |
| 2 | Descomponer tareas complejas en tareas simples | Cada sub-tarea produjo código correcto a la primera; sin descomposición los resultados eran inconsistentes |
| 3 | Dar ejemplos concretos | El selector de dificultad en el menú salió listo para producción siguiendo el patrón de grid size |
| 4 | Usar contexto de archivos abiertos y comentarios descriptivos | Copilot auto-completó el dict `DIFFICULTY_SETTINGS` completo y sugirió `config.score_multiplier` en `game.py` sin pedírselo |

---

## Técnica 1 — Empezar general, luego ser específico

### El problema con prompts vagos

Un prompt vago obliga a Copilot a adivinar demasiado: qué archivo tocar, qué estructura usar, qué valores elegir.

**Prompt v1 — Demasiado general**

```
add difficulty to the game
```

Resultado: Copilot sugirió añadir una variable global `difficulty = "medium"` en `main.py` y un bloque `if/elif` para cambiar la velocidad directamente, sin usar `GameConfig` ni el patrón de dataclass frozen que ya existe.

Problema: No sabe _dónde_ vive la configuración, ignora la arquitectura existente y muta estado global.

---

**Prompt v2 — Más específico**

```
add a difficulty field to GameConfig with Easy, Medium and Hard options
```

Resultado: Copilot sugirió agregar el campo en `config.py` y usar un `Enum`, que ya es mucho mejor. Sin embargo, sólo generó tres niveles, puso los valores de velocidad hardcodeados dentro del `@dataclass` como campos simples, y no añadió los métodos `next_difficulty()` / `prev_difficulty()`.

Problema: Sin mencionar `frozen=True`, `DIFFICULTY_SETTINGS`, ni el patrón ya existente de `next_size()`, Copilot no siguió la convención del proyecto.

---

**Prompt v3 — Preciso + contexto**

```
En config.py, añade un campo `difficulty: Difficulty` al frozen dataclass
`GameConfig`. Define primero un Enum `Difficulty` con valores EASY, MEDIUM,
HARD, INSANE y un dict `DIFFICULTY_SETTINGS` que mapea cada nivel a
`mole_visible_time`, `mole_spawn_interval` y `score_multiplier` (1, 2, 3, 5
respectivamente). Añade una property `score_multiplier` que lea del dict.
Luego añade `next_difficulty()` y `prev_difficulty()` que devuelvan un nuevo
GameConfig con los valores correspondientes al nivel adyacente, siguiendo
exactamente el mismo patrón que `next_size()` y `prev_size()`.
```

Resultado: Copilot generó el bloque completo —`Difficulty`, `DIFFICULTY_SETTINGS`, `DIFFICULTY_COLORS`, la property y ambos métodos— con la misma estructura que `next_size()` y `prev_size()`. El código resultante fue prácticamente idéntico al que está hoy en `config.py`.

### Por qué funciona

- Nombrar el archivo (`config.py`) dirige la sugerencia al contexto correcto.
- Mencionar `frozen=True` y `next_size()` activa el patrón inmutable del proyecto.
- Especificar los valores numéricos concretos (1, 2, 3, 5) elimina la ambigüedad.
- Pedir que "siga exactamente el mismo patrón" ancla la sugerencia en código que Copilot ya puede ver en el editor.

### Resultado

| Elemento | Generado por Copilot | Ajuste humano |
|----------|----------------------|---------------|
| `Difficulty` Enum | Completo | Ninguno |
| `DIFFICULTY_SETTINGS` dict | Completo | Ninguno |
| `DIFFICULTY_COLORS` dict | Generado automáticamente al ver el patrón | Ajustar tonos RGB |
| Property `score_multiplier` | Completa | Ninguno |
| `next_difficulty()` / `prev_difficulty()` | Completos | Ninguno |

---

## Técnica 2 — Descomponer tareas complejas en tareas simples

### El problema con las tareas monolíticas

Pedir "implementa la feature de dificultad completa" produce sugerencias que mezclan archivos, ignoran la separación de responsabilidades y a menudo omiten partes clave (HUD, eventos del menú, etc.).

### Descomposición aplicada

La feature se dividió en 4 sub-tareas independientes, cada una con su propio prompt y su archivo destino.

---

**Sub-tarea 1 — Definir el Enum y el dict de settings** → `config.py`

```
En config.py, define:
1. Un Enum `Difficulty` con EASY, MEDIUM, HARD, INSANE.
2. Un dict `DIFFICULTY_SETTINGS` que mapea cada Difficulty a un dict
   con keys `mole_visible_time` (float), `mole_spawn_interval` (float)
   y `score_multiplier` (int).
3. Un dict `DIFFICULTY_COLORS` que mapea cada Difficulty a un tuple RGB:
   verde para EASY, naranja para MEDIUM, rojo para HARD, morado para INSANE.
```

Resultado: Copilot generó los tres dicts y el Enum correctamente. La sub-tarea era lo suficientemente pequeña para que no hubiera ambigüedad.

---

**Sub-tarea 2 — Actualizar `GameConfig`** → `config.py`

```
Añade un campo `difficulty: Difficulty = Difficulty.MEDIUM` al dataclass
frozen `GameConfig`. Añade una property `score_multiplier` que lea
`DIFFICULTY_SETTINGS[self.difficulty]["score_multiplier"]`. Añade
`next_difficulty()` y `prev_difficulty()` siguiendo el patrón de
`next_size()`: devuelven un nuevo `GameConfig` con los valores de
`DIFFICULTY_SETTINGS[new_diff]` aplicados a `mole_visible_time` y
`mole_spawn_interval`.
```

Resultado: Copilot copió el patrón de `next_size()` con precisión, leyó los valores del dict en lugar de hardcodearlos, y mantuvo la inmutabilidad del dataclass.

---

**Sub-tarea 3 — Usar `score_multiplier` en `GameState.whack()`** → `game.py`

```
En el método `whack()` de `GameState` en game.py, reemplaza el `+ 1`
al sumar puntos por `+ self.config.score_multiplier` cuando hay un hit.
```

Resultado: Copilot encontró la línea correcta inmediatamente y aplicó el cambio. La sub-tarea era trivial porque la descripción señalaba exactamente la línea relevante.

```python
# Antes (generado originalmente)
new_score = self.score + (1 if hit else 0)

# Después (sugerido por Copilot con el prompt anterior)
new_score = self.score + (self.config.score_multiplier if hit else 0)
```

---

**Sub-tarea 4 — UI: selector en el menú y etiqueta en el HUD** → `renderer.py`

```
En `draw_menu()` de renderer.py, añade una fila de dificultad en `row_y3 = 450`
siguiendo el mismo patrón que la fila de grid size (row_y = 230):
- Caption "Difficulty" en dorado, centrado.
- Label con el nombre de la dificultad en su color (`DIFFICULTY_COLORS`).
- Botones `<` y `>` en `prev_diff_rect` y `next_diff_rect`.
- Devuelve `prev_diff` y `next_diff` en el dict de rects.

En `draw_hud()`, añade en el centro del HUD el nombre de la dificultad
actual en su color usando `DIFFICULTY_COLORS[state.config.difficulty]`.
```

Resultado: Copilot generó el bloque completo del menú y la línea del HUD. Ver Técnica 3 para el detalle de cómo el ejemplo del patrón existente guió esta sugerencia.

### Por qué funciona

- Cada sub-tarea tiene una responsabilidad única y un archivo destino claro.
- El tamaño reducido del scope permite que Copilot genere código correcto sin ambigüedad.
- El orden de las sub-tareas respeta las dependencias: el Enum debe existir antes de usarlo en `GameConfig`, y `score_multiplier` debe existir antes de usarlo en `game.py`.

### Resultado comparativo

| Enfoque | Intentos hasta código correcto | Archivos afectados correctamente |
|---------|-------------------------------|----------------------------------|
| Prompt monolítico | 3-4 iteraciones | 2 de 3 |
| 4 sub-tareas independientes | 1 iteración por sub-tarea | 3 de 3 |

---

## Técnica 3 — Dar ejemplos concretos

### El problema sin ejemplo

```
add difficulty selector to the menu
```

Sin contexto, Copilot generó un menú con `pygame.draw.rect` plano para los botones, sin usar `_draw_button()`, con estilos distintos a los existentes y sin seguir la estructura de `row_y` que organiza el menú actual.

### Con ejemplo: referenciar el patrón existente

La clave fue abrir `renderer.py` y mostrar explícitamente el bloque del grid size como modelo:

```
Añade una fila de dificultad en `draw_menu()` en renderer.py siguiendo
exactamente el mismo patrón que la fila de grid size.

El patrón existente de grid size es:

    row_y = 230
    label_size = font_large.render(
        f"{state.config.grid_size}×{state.config.grid_size}", True, COLORS["text_white"]
    )
    surface.blit(label_size, (cx - label_size.get_width() // 2, row_y + 5))
    caption = font_medium.render("Grid Size", True, COLORS["text_gold"])
    surface.blit(caption, (cx - caption.get_width() // 2, row_y - 28))
    prev_size_rect = pygame.Rect(cx - 120 - btn_w, row_y, btn_w, btn_h)
    next_size_rect = pygame.Rect(cx + 120, row_y, btn_w, btn_h)
    _draw_button(surface, prev_size_rect, "<", font_large, mouse_pos)
    _draw_button(surface, next_size_rect, ">", font_large, mouse_pos)

Haz lo mismo para dificultad en `row_y3 = 450`. El label de dificultad debe
mostrarse en el color correspondiente de `DIFFICULTY_COLORS` (verde para EASY,
naranja para MEDIUM, rojo para HARD, morado para INSANE). Los rects deben
llamarse `prev_diff_rect` y `next_diff_rect` y devolverse en el dict como
`prev_diff` y `next_diff`.
```

Resultado: Copilot replicó el patrón a la perfección, incluyendo `_draw_button()`, las coordenadas simétricas y la adición de las claves al dict de retorno. El código generado fue idéntico al que está hoy en `renderer.py` (líneas 272-284 y 292-293).

### Por qué funciona

Copilot no infiere convenciones de estilo desde cero; las *aprende del contexto visible*. Al pegar el bloque de código existente como ejemplo:

1. Aprende los nombres de variables (`row_y`, `btn_w`, `btn_h`, `cx`).
2. Aprende que los botones se dibujan con `_draw_button()` y no con `draw.rect` directo.
3. Aprende la geometría: `cx - 120 - btn_w` para el botón izquierdo, `cx + 120` para el derecho.
4. Aprende que el caption va 28px arriba (`row_y - 28`) y el label 5px abajo (`row_y + 5`).

Sin el ejemplo, Copilot habría tenido que inferir todo esto desde el nombre de la función, con alta probabilidad de error.

### Resultado

| Elemento | Sin ejemplo | Con ejemplo |
|----------|-------------|-------------|
| Uso de `_draw_button()` | No (usó `draw.rect`) | Sí |
| Geometría correcta | No (valores arbitrarios) | Sí (replicó exactamente) |
| Color de dificultad | No (blanco hardcodeado) | Sí (`DIFFICULTY_COLORS`) |
| Claves en dict de retorno | Omitidas | Incluidas correctamente |

---

## Técnica 4 — Usar contexto de archivos abiertos y comentarios descriptivos

### Contexto de archivos abiertos

GitHub Copilot usa los archivos abiertos en el editor como contexto adicional, aunque no se mencionen en el prompt. Esto se puede aprovechar estratégicamente:

**Patrón aplicado:**

- Al editar `game.py` para usar `score_multiplier`, se mantuvo `config.py` abierto en otra pestaña. Copilot ya sabía que `GameConfig` tiene una property `score_multiplier` y sugirió `self.config.score_multiplier` automáticamente al escribir `self.config.`.

- Al escribir los tests de `renderer.py`, se mantuvo `renderer.py` abierto. Copilot entendió que `draw_menu()` devuelve un dict con claves `prev_diff`, `next_diff`, `prev_size`, `next_size`, `prev_dur`, `next_dur` y `play`, y los sugirió en los asserts sin pedirlo.

### Comentarios descriptivos como prompts implícitos

Un comentario bien redactado es un prompt que Copilot ve justo antes del código que va a generar.

**Ejemplo concreto — autocomplete del dict de settings:**

Antes de escribir `DIFFICULTY_SETTINGS`, se añadió este comentario:

```python
# EASY: 1x score, slow moles. MEDIUM: 2x, normal. HARD: 3x, fast. INSANE: 5x, very fast.
DIFFICULTY_SETTINGS = {
```

Copilot completó el dict entero:

```python
# EASY: 1x score, slow moles. MEDIUM: 2x, normal. HARD: 3x, fast. INSANE: 5x, very fast.
DIFFICULTY_SETTINGS = {
    Difficulty.EASY:   {"mole_visible_time": 2.0, "mole_spawn_interval": 1.5, "score_multiplier": 1},
    Difficulty.MEDIUM: {"mole_visible_time": 1.4, "mole_spawn_interval": 0.9, "score_multiplier": 2},
    Difficulty.HARD:   {"mole_visible_time": 0.9, "mole_spawn_interval": 0.6, "score_multiplier": 3},
    Difficulty.INSANE: {"mole_visible_time": 0.5, "mole_spawn_interval": 0.4, "score_multiplier": 5},
}
```

Sin el comentario, Copilot generó valores arbitrarios (1.0, 0.8, 0.5, 0.3) que no coincidían con la intención de diseño.

**Contraste de comentarios:**

| Comentario | Sugerencia de Copilot |
|------------|----------------------|
| `# apply score` | `new_score = self.score + 1` |
| `# apply score with difficulty multiplier` | `new_score = self.score + self.config.score_multiplier` |
| `# difficulty multiplier from config` | `return DIFFICULTY_SETTINGS[self.difficulty]["score_multiplier"]` |

### Nombre de variables como señal

Copilot también usa los nombres de variables como señal. Al nombrar `prev_diff_rect` y `next_diff_rect` (en lugar de `btn1` y `btn2`), las sugerencias posteriores en el manejador de eventos de `main.py` asociaron automáticamente esos rects con `config.prev_difficulty()` y `config.next_difficulty()`.

### Por qué funciona

Copilot modela la probabilidad del siguiente token basándose en todo el contexto visible: archivos abiertos, imports, nombres de variables, comentarios. Cuanto más específico y consistente sea ese contexto, más precisa es la sugerencia. Los comentarios actúan como "especificación en línea" que Copilot puede leer justo antes de generar el código.

### Resultado

| Señal de contexto | Resultado |
|-------------------|-----------|
| `config.py` abierto al editar `game.py` | `score_multiplier` sugerido automáticamente en `whack()` |
| `renderer.py` abierto al escribir tests | Claves del dict de rects sugeridas correctamente en los asserts |
| Comentario con valores explícitos | `DIFFICULTY_SETTINGS` completo sin valores arbitrarios |
| Nombres descriptivos (`prev_diff_rect`) | Asociación correcta con `config.prev_difficulty()` en el event loop |

---

## Lecciones aprendidas

1. **La especificidad elimina ambigüedad**: cada grado de detalle añadido al prompt reduce el espacio de sugerencias y acerca el resultado al código deseado.
2. **Copilot aprende el estilo del proyecto**: al darle un ejemplo del patrón existente, no hay que describir el estilo; lo replica.
3. **Tareas pequeñas = sugerencias correctas**: cuanto menor es el scope, mayor es la tasa de acierto en el primer intento.
4. **El contexto invisible importa**: los archivos abiertos y los comentarios son prompts implícitos que Copilot usa aunque no se mencionen explícitamente en el chat.
