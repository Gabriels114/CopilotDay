# Challenge 05 - Copilot en el flujo de desarrollo (CI/CD)

Este reto demuestra cómo GitHub Copilot acelera la creación y mantenimiento de pipelines de CI/CD, mensajes de commit de calidad y la integración general de Copilot en el flujo de trabajo diario.

## Pipeline de CI: qué hace y cómo está estructurado

El workflow vive en `.github/workflows/ci.yml` y se dispara en `push` y `pull_request` hacia `main`, así como manualmente via `workflow_dispatch`.

### Diagrama de jobs

```
lint ──► test (matrix: 3.11, 3.12)
```

El job `test` tiene `needs: lint`, lo que garantiza que el código nunca se prueba si primero no pasa el análisis de calidad.

---

### Job `lint` — Lint & Format

| Paso | Herramienta | Qué valida |
|------|-------------|-----------|
| Set up Python | `actions/setup-python@v5` (3.12) | Entorno reproducible con cache de pip |
| Install lint tools | `pip install ruff` | Instala el linter/formatter único |
| Check formatting | `ruff format --check .` | Falla si el código no está bien formateado (equivalente a Black) |
| Lint | `ruff check .` | Aplica reglas de estilo y errores comunes (equivalente a flake8) |
| Add lint summary | `GITHUB_STEP_SUMMARY` | Resume herramienta y checks en la UI de Actions |

**Por qué ruff:** una sola herramienta reemplaza flake8 + black, es 10-100x más rápida y se configura con `pyproject.toml` o `ruff.toml`.

---

### Job `test` — Tests (matrix Python 3.11 y 3.12)

| Paso | Qué hace |
|------|----------|
| Checkout | Descarga el código fuente |
| Set up Python | Configura la versión de la matriz con cache de pip |
| Install system deps | Instala librerías SDL2 necesarias para `pygame` en Ubuntu |
| Install Python deps | Instala `requirements.txt` + `pytest` + `pytest-cov` |
| Run tests with coverage | `pytest tests/ --cov=. --cov-report=term-missing --cov-report=xml --junitxml=test-results/junit.xml --cov-fail-under=80 -v` |
| Upload test artifacts | Sube `coverage.xml` y `junit.xml` como artefactos descargables |
| Add workflow summary | Escribe resumen del run en la UI de Actions |

La matrix `["3.11", "3.12"]` garantiza compatibilidad con ambas versiones activas de Python. `fail-fast: false` permite ver los resultados de ambas versiones aunque una falle.

El threshold `--cov-fail-under=80` convierte la cobertura insuficiente en fallo de pipeline.

---

## Cómo se usó Copilot para generarlo

### Estrategia de prompt engineering

El workflow no se escribió manualmente línea a línea. Se usó Copilot Chat con prompts estructurados que siguen el principio de **contexto + restricciones + ejemplo de salida esperada**.

#### Prompt inicial para el esqueleto del workflow

```
Genera un GitHub Actions workflow para un proyecto Python con pygame.
Requisitos:
- Trigger en push y pull_request a main
- Matrix con Python 3.11 y 3.12
- Instalar dependencias SDL2 del sistema (libsdl2-dev y relacionadas)
- Ejecutar pytest con cobertura mínima del 80%
- Subir coverage.xml como artefacto
- Variable SDL_VIDEODRIVER=dummy para headless
El proyecto está en el directorio challenges/01-intro.
```

#### Prompt para añadir el job de lint

```
Añade un job llamado "lint" que corra antes del job "test" usando needs:.
El job debe:
- Usar ruff para format check (ruff format --check) y lint (ruff check)
- Correr solo en Python 3.12 (no necesita matrix)
- Escribir un summary en GITHUB_STEP_SUMMARY
No instales flake8 ni black por separado; ruff los reemplaza ambos.
```

#### Prompt para mensajes de commit

```
Resume estos cambios como un commit de Conventional Commits. Usa un subject corto,
imperativo y específico. Si hace falta, añade un cuerpo de 2-3 líneas explicando
el porqué del cambio.
```

### Qué aportó Copilot vs. qué se ajustó manualmente

| Parte | Copilot | Ajuste manual |
|-------|---------|---------------|
| Estructura de jobs y steps | Generó el esqueleto completo | Añadir `needs: lint` y orden correcto |
| Instalación de SDL2 | Listó las librerías correctas | Verificar que existen en Ubuntu 22.04 |
| Flags de pytest | Generó flags estándar | Añadir `--junitxml` para artefacto XML |
| `GITHUB_STEP_SUMMARY` | No lo incluyó en el primer draft | Añadido manualmente en segunda iteración |
| Mensajes de commit | Generó borradores precisos | Revisión de tono e imperativo |

---

## Criterios de éxito verificables

### 1. Pipeline verde en GitHub Actions

- [ ] El workflow `CI` aparece en la pestaña `Actions` del repositorio.
- [ ] El job `lint` pasa (verde) antes de que corra `test`.
- [ ] Los jobs `Tests (Python 3.11)` y `Tests (Python 3.12)` pasan en verde.
- [ ] Ambos jobs muestran un `## CI run summary` en la pestaña Summary de la corrida.

Cómo verificarlo: `https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml`

### 2. Artefactos publicados

- [ ] La corrida tiene artefactos `test-artifacts-py3.11` y `test-artifacts-py3.12`.
- [ ] Cada artefacto contiene `coverage.xml` y `test-results/junit.xml`.
- [ ] `coverage.xml` muestra cobertura >= 80%.

### 3. Lint y formato

- [ ] `ruff format --check .` no reporta archivos mal formateados.
- [ ] `ruff check .` no reporta errores de lint.

Verificación local equivalente:

```bash
cd challenges/01-intro
pip install ruff
ruff format --check .
ruff check .
```

### 4. Cobertura mínima

- [ ] `pytest` sale con código 0 (cobertura >= 80%).
- [ ] El pipeline falla si se introduce código no cubierto que baje la cobertura.

Verificación local equivalente:

```bash
cd challenges/01-intro
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=80 -q
```

### 5. Badge de CI en el README principal

- [ ] El README raíz muestra el badge `[![CI](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml/badge.svg)](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml)`.
- [ ] El badge muestra estado `passing` tras un push exitoso.

### 6. Commit messages con Copilot

- [ ] Al menos un commit en el historial fue redactado con asistencia de Copilot.
- [ ] El commit sigue el formato `<tipo>: <descripción imperativa corta>`.
- [ ] Existe evidencia (screenshot o grabación) del prompt usado en Copilot Chat o la sugerencia en la caja de commit de VS Code.

```bash
git log --oneline -n 5   # muestra los últimos 5 commits
```

---

## Archivos de referencia en esta carpeta

- [DEMO-SCRIPT.md](./DEMO-SCRIPT.md): guion para demostrar el reto en vivo.
- [EVIDENCE-CHECKLIST.md](./EVIDENCE-CHECKLIST.md): checklist de capturas y datos a recolectar.
- [LOCAL-VALIDATION.md](./LOCAL-VALIDATION.md): comandos locales equivalentes al CI para validar antes de push.

---

## Parte opcional: PR summaries y discusiones

No marcar como completada sin evidencia real en GitHub.

- `PR summaries`: usar Copilot Chat dentro de un PR para generar un resumen de los cambios.
- `PR discussions`: usar Copilot para redactar comentarios de revisión o responder a threads.

Evidencia requerida si se completa:
- Screenshot del resumen generado por Copilot en un PR abierto.
- URL del PR con el comentario/review asistido.
