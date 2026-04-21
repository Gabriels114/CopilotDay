# Demo Script - Challenge 05: Dev Workflow con GitHub Copilot

Guion para una demo de 5 a 8 minutos. Sigue el orden de las secciones.

---

## 1. La historia: cómo Copilot generó el workflow de CI

### Contexto para la audiencia

> "No escribí este workflow a mano. Le hice tres preguntas a Copilot Chat y llegué
> al archivo final en menos de diez minutos. Esto es lo que le pregunté."

---

### Prompt 1 — Arranque: generar la estructura base

**Prompt que escribiste en Copilot Chat:**

```
Generate a GitHub Actions CI workflow for a Python project that:
- Triggers on push and pull_request to main
- Runs on ubuntu-latest
- Tests against Python 3.11 and 3.12 using a matrix
- Installs dependencies from challenges/01-intro/requirements.txt
- Runs pytest with coverage and fails if coverage is below 80%
- Uploads coverage.xml and junit.xml as artifacts
```

**Respuesta esperada de Copilot (fragmento):**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r challenges/01-intro/requirements.txt pytest pytest-cov
      - run: pytest tests/ --cov=. --cov-fail-under=80 --cov-report=xml
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-py${{ matrix.python-version }}
          path: coverage.xml
```

---

### Prompt 2 — Refinamiento: dependencias del sistema para pygame

**Prompt:**

```
The project uses pygame which requires native SDL2 libraries on Linux.
Add a step to install libsdl2-dev, libsdl2-image-dev, libsdl2-mixer-dev,
libsdl2-ttf-dev and libportmidi-dev before the Python install step.
Also set SDL_VIDEODRIVER=dummy and SDL_AUDIODRIVER=dummy as env vars
so tests run headless.
```

**Respuesta esperada de Copilot (fragmento):**

```yaml
env:
  SDL_VIDEODRIVER: dummy
  SDL_AUDIODRIVER: dummy

steps:
  - name: Install system dependencies for pygame
    run: |
      sudo apt-get update
      sudo apt-get install -y \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libportmidi-dev
```

---

### Prompt 3 — Pulido final: concurrencia, permisos y step summary

**Prompt:**

```
Add three finishing touches:
1. A concurrency group that cancels in-progress runs on the same ref.
2. Minimal permissions (contents: read only).
3. A step at the end that writes a Markdown summary to GITHUB_STEP_SUMMARY
   showing the Python version, project dir, and test command used.
Also add workflow_dispatch so we can trigger it manually from the Actions tab.
```

**Respuesta esperada de Copilot (fragmento):**

```yaml
on:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# ... (al final del job)
      - name: Add workflow summary
        if: always()
        run: |
          {
            echo "## CI run summary"
            echo "- Python: \`${{ matrix.python-version }}\`"
            echo "- Test command: \`pytest tests/ --cov=. --cov-fail-under=80 -v\`"
          } >> "$GITHUB_STEP_SUMMARY"
```

> Muestra en pantalla el archivo `.github/workflows/ci.yml` final y señala que
> es exactamente el resultado de combinar estas tres respuestas con ajustes mínimos.

---

## 2. Mostrar el pipeline corriendo en GitHub Actions

### Pasos en pantalla

1. Abre el repositorio en GitHub.
2. Haz clic en la pestaña **Actions**.
3. En el panel izquierdo selecciona el workflow **CI**.
4. Abre la corrida verde más reciente.

**Qué señalar durante la demo:**

| Elemento a mostrar | Por qué importa |
|--------------------|-----------------|
| Badge verde en la lista de runs | Demuestra que el pipeline pasa |
| Matrix de versiones (3.11 / 3.12) | Muestra cobertura multi-versión |
| Step "Install system dependencies for pygame" | Muestra que Copilot sugirió el setup nativo |
| Step "Run tests with coverage" — log completo | Muestra `199 passed`, cobertura `99.78%` |
| Step summary al final del job | Muestra el resumen Markdown generado automáticamente |
| Sección "Artifacts" — `test-artifacts-py3.11` | Demuestra que el artefacto se subió |

**URL a tener preparada:**

```
https://github.com/<owner>/<repo>/actions/workflows/ci.yml
```

Sustituye `<owner>/<repo>` con los valores reales del repositorio antes de la demo.
Ábrela en una pestaña del navegador ya cargada para no perder tiempo.

---

## 3. Commit messages con Copilot (en VS Code)

### Flujo paso a paso

1. Haz un cambio pequeño y real en el repo (por ejemplo, ajusta un comentario en
   `challenges/01-intro/` o agrega una línea en `LOCAL-VALIDATION.md`).
2. En VS Code, abre el panel **Source Control** (`Ctrl+Shift+G` / `Cmd+Shift+G`).
3. Marca los archivos modificados con **Stage Changes** (el icono `+`).
4. Haz clic en el icono de **chispa/estrella de Copilot** que aparece a la derecha
   del campo de mensaje de commit (tooltip: "Generate Commit Message with Copilot").
5. Copilot analiza el diff staged y propone un mensaje. Ejemplo de sugerencia:

```
docs(ch05): update LOCAL-VALIDATION timestamp and coverage note

Add run date and clarify that coverage.xml is the artifact
uploaded by the CI workflow.
```

6. Acepta, edita si lo quieres afinar, y haz commit.
7. En la terminal muestra:

```bash
git log --oneline -n 5
```

**Captura de pantalla sugerida:**

- Panel Source Control con archivos staged visibles a la izquierda.
- Campo de mensaje de commit con la sugerencia de Copilot ya insertada.
- Botón de chispa resaltado (puedes hacer zoom en VS Code con `Cmd++` antes de capturar).

> Tip: si la audiencia no puede ver bien el botón, usa Copilot Chat en su lugar con
> el prompt de la sección siguiente y pega el resultado en el campo de commit.

**Prompt alternativo para Copilot Chat (si el botón no está disponible):**

```
Look at the staged changes in this repository and write a Conventional Commits
message for them. Use an imperative subject line under 72 characters.
If the change warrants it, add a short body (2-3 lines) explaining the why.
```

---

## 4. (Opcional) PR Summary con Copilot

> Solo muestra esta sección si tienes un PR real abierto. No la presentes como
> completada si no hay evidencia.

### Prompt para generar el resumen del PR

En GitHub, al abrir un Pull Request, Copilot puede generar el summary automáticamente
desde el botón **Copilot** que aparece en el campo de descripción. Si prefieres usar
Copilot Chat:

```
Based on the commits in this branch, write a Pull Request description that includes:
- A one-sentence summary of what changed and why
- A bullet list of the main changes
- A "How to test" section with the exact commands to run
- Any risks or follow-up tasks

Use Markdown formatting.
```

**Respuesta esperada (estructura):**

```markdown
## Summary
Update CI workflow to support pygame headless testing and add commit message
automation demo materials for Challenge 05.

## Changes
- Add SDL2 system dependencies step to `ci.yml`
- Set `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy` for headless runs
- Rewrite `DEMO-SCRIPT.md` with Copilot prompt history and screen guidance
- Add `EVIDENCE-CHECKLIST.md` with per-criterion checkboxes

## How to test
```bash
cd challenges/01-intro
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=80 -q
```

## Risks / follow-up
- None for CI changes; pygame headless already validated locally.
```

---

## Frase de cierre para la demo

```
En este reto usé Copilot en tres momentos del flujo de desarrollo:
para escribir el pipeline de CI desde cero con prompts iterativos,
para generar mensajes de commit descriptivos sin pensar en el formato,
y —de forma opcional— para redactar el resumen de un PR.
El resultado es un workflow que corre verde en GitHub Actions con cobertura del 99 %.
```
