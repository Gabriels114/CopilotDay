# Challenge 02 — Mejores Prácticas con GitHub Copilot

## Qué se hizo en este challenge

Se implementó la feature **Difficulty Levels** sobre el juego Whack-a-Mole construido en el Challenge 01. La feature añade cuatro niveles de dificultad preconfigurados que ajustan la velocidad de los topos y aplican un multiplicador al puntaje:

| Nivel | Tiempo visible | Intervalo de spawn | Multiplicador |
|-------|---------------|--------------------|---------------|
| EASY | 2.0 s | 1.5 s | ×1 |
| MEDIUM | 1.4 s | 0.9 s | ×2 |
| HARD | 0.9 s | 0.6 s | ×3 |
| INSANE | 0.5 s | 0.4 s | ×5 |

Los cambios se distribuyeron en tres archivos:

- `config.py` — Enum `Difficulty`, dict `DIFFICULTY_SETTINGS`, dict `DIFFICULTY_COLORS`, campo `difficulty` en `GameConfig`, property `score_multiplier`, métodos `next_difficulty()` y `prev_difficulty()`.
- `game.py` — `GameState.whack()` usa `config.score_multiplier` en lugar de `+1` fijo.
- `renderer.py` — Selector de dificultad en el menú (fila con botones `<` / `>`) y etiqueta de dificultad en el HUD con su color correspondiente.

## Las 4 técnicas de prompt engineering demostradas

### 1. Empezar general, luego ser específico

Se muestran tres versiones del mismo prompt, de vago a preciso. El prompt v1 ("add difficulty to the game") produjo código que ignoraba la arquitectura; el prompt v3 mencionaba el archivo, la clase, los valores numéricos y el patrón a seguir, y Copilot generó ~90 % del código final sin ajustes.

### 2. Descomponer tareas complejas en tareas simples

La feature completa se dividió en 4 sub-tareas con un prompt y un archivo destino cada una. Cada sub-tarea produjo código correcto en el primer intento, algo que no ocurrió al pedir la feature entera en un solo prompt.

### 3. Dar ejemplos concretos

Al añadir el selector de dificultad en el menú se pegó el bloque de código de la fila de grid size como ejemplo. Copilot replicó el patrón exacto —incluyendo `_draw_button()`, las coordenadas y las claves del dict de retorno— sin ningún ajuste manual.

### 4. Usar contexto de archivos abiertos y comentarios descriptivos

Mantener `config.py` abierto al editar `game.py` hizo que Copilot sugiriera `config.score_multiplier` automáticamente. Un comentario con los valores explícitos antes del dict `DIFFICULTY_SETTINGS` fue suficiente para que Copilot lo completara entero con los valores correctos.

## Como ejecutar el juego

```bash
cd /ruta/a/CopilotDay
python challenges/01-intro/main.py
```

En el menú principal aparece la fila **Difficulty** con botones `<` y `>`. El nivel seleccionado se muestra en el HUD durante la partida con su color identificador.

## Detalles y ejemplos

Consulta [NOTES.md](./NOTES.md) para ver los prompts exactos, los fragmentos de código generados por Copilot y el análisis de por qué cada técnica funciona.
