# Challenge 05 — Flujo de Trabajo con Copilot y CI/CD

En este reto aprenderás a usar GitHub Copilot para mejorar tu flujo de trabajo de desarrollo: escribir mejores mensajes de commit, entender el pipeline de CI ya configurado y verificar que tus cambios pasan las pruebas automáticas.

---

## 1. Mensajes de commit descriptivos con Copilot

Un buen mensaje de commit explica **por qué** se hizo el cambio, no solo el qué. Copilot puede ayudarte a redactarlos.

### Cómo pedirle a Copilot que redacte un mensaje de commit

En la terminal integrada o en un comentario de código, escribe:

```
# Genera un mensaje de commit para los siguientes cambios:
# - Se agregó detección de colisiones al método try_whack en board.py
# - Se corrigió el temporizador de spawn que no reiniciaba al pasar de GAMEOVER a MENU
```

Copilot sugerirá algo como:

```
fix: reset spawn timer on GAMEOVER-to-MENU transition and add whack collision detection

The spawn_timer was not zeroed when returning to the menu, causing moles to
spawn immediately at game start. Also wired try_whack to properly detect hits
on RISING and VISIBLE moles.
```

### Formato recomendado (Conventional Commits)

```
<tipo>: <descripción corta en presente>

<cuerpo opcional — explica el por qué>
```

| Tipo       | Cuándo usarlo                              |
|------------|--------------------------------------------|
| `feat`     | Nueva funcionalidad                        |
| `fix`      | Corrección de bug                          |
| `refactor` | Cambio de estructura sin alterar comportamiento |
| `test`     | Agregar o corregir pruebas                 |
| `docs`     | Cambios en documentación                   |
| `chore`    | Tareas de mantenimiento (deps, config)     |
| `perf`     | Mejora de rendimiento                      |
| `ci`       | Cambios en el pipeline de CI               |

### Ejemplos concretos

```bash
# Bueno
git commit -m "feat: add configurable mole spawn interval to GameConfig"

# Malo
git commit -m "changes"

# Bueno con cuerpo
git commit -m "fix: clamp mole progress to [0.0, 1.0] in RISING state

Without the clamp, a large dt could push progress above 1.0, causing
the mole to skip the VISIBLE state entirely on the next frame."
```

**Tip con Copilot:** En VS Code, abre el panel de Source Control. Haz clic en el campo de mensaje de commit y escribe `/` para activar las sugerencias de Copilot en el cuadro de texto.

---

## 2. El workflow de CI ya está configurado

El archivo `.github/workflows/ci.yml` en la raíz del repositorio define el pipeline de integración continua. Se ejecuta automáticamente en cada push y pull request a la rama `main`.

Para verlo:

```bash
cat ../../.github/workflows/ci.yml
```

No necesitas crear ni modificar este archivo — ya está listo.

---

## 3. Qué hace cada sección del workflow

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```
**Disparadores:** El pipeline corre cuando haces push a `main` o abres/actualizas un Pull Request hacia `main`.

```yaml
- name: Install system dependencies for pygame
  run: sudo apt-get install -y libsdl2-dev ...
```
**Dependencias del sistema:** pygame necesita las bibliotecas SDL2. Se instalan con `apt-get` en el runner de Ubuntu.

```yaml
- name: Install Python dependencies
  working-directory: challenges/01-intro
  run: pip install -r requirements.txt && pip install pytest pytest-cov
```
**Dependencias Python:** Se instalan las dependencias del juego más las herramientas de testing.

```yaml
- name: Run tests with coverage
  env:
    SDL_VIDEODRIVER: dummy
    SDL_AUDIODRIVER: dummy
  run: pytest tests/ --cov=. --cov-fail-under=80 -v
```
**Ejecución de tests:** Se corren todos los tests con cobertura mínima del 80%. Las variables `SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy` evitan que pygame intente abrir una ventana real (en CI no hay pantalla).

```yaml
- name: Upload coverage report
  uses: actions/upload-artifact@v4
```
**Artefacto:** Se sube el reporte de cobertura como artefacto descargable desde la interfaz de GitHub Actions.

---

## 4. Verificar que el pipeline pasa en GitHub Actions

1. Haz push de tus cambios a la rama `main` (o abre un PR).
2. Ve a tu repositorio en GitHub.
3. Haz clic en la pestaña **Actions**.
4. Selecciona el workflow **CI** en la lista de la izquierda.
5. Verás la ejecución más reciente. El ícono verde indica éxito; el rojo indica fallo.
6. Haz clic en el job **Run Tests** para ver los logs detallados.
7. Si hay errores de cobertura, el log mostrará qué líneas no están cubiertas.

Para ejecutar los mismos checks localmente antes de hacer push:

```bash
cd challenges/01-intro
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
  pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=80 -v
```

---

## 5. Tips para usar Copilot al escribir workflows de GitHub Actions

- **Autocompletar steps:** Escribe `- name: ` y Copilot sugerirá steps comunes basados en el contexto del archivo.
- **Preguntar en el chat:** "¿Cómo agrego caché de dependencias pip en GitHub Actions?" — Copilot generará el step completo con `actions/cache`.
- **Explicar secciones:** Selecciona un bloque del YAML y pide `/explain` para que Copilot lo describa.
- **Generar matrices de testing:** "Agrega una matrix strategy para Python 3.11 y 3.12" — Copilot escribe la configuración de `matrix`.

Ejemplo de prompt para Copilot Chat:

```
En el archivo ci.yml, agrega un step para publicar el reporte de cobertura
como comentario en el Pull Request usando la action MishaKav/pytest-coverage-comment.
```

---

## 6. Challenge avanzado: Badge de CI en el README

Agrega un badge que muestre el estado del pipeline directamente en el README del proyecto.

1. Ve a tu repositorio en GitHub → pestaña **Actions** → selecciona el workflow **CI**.
2. Haz clic en los tres puntos (`...`) → **Create status badge**.
3. Copia el Markdown generado, que tendrá esta forma:

```markdown
![CI](https://github.com/<usuario>/<repo>/actions/workflows/ci.yml/badge.svg)
```

4. Pégalo al inicio del `README.md` principal del proyecto.

Pídele a Copilot que te ayude a posicionarlo correctamente:

```
Inserta el badge de CI al inicio del README, después del título principal
y antes de la descripción del proyecto.
```

El badge se actualizará automáticamente a verde o rojo según el último resultado del pipeline.
