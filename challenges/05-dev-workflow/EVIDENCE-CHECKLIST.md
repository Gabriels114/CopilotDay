# Evidence Checklist - Challenge 05: Dev Workflow con GitHub Copilot

Marca cada item cuando tengas evidencia real. No marques nada sin captura,
URL o log que lo respalde.

---

## Criterio 1 — CI pipeline funcional con runs verdes

- [ ] El workflow `.github/workflows/ci.yml` existe en el repositorio.
- [ ] Se disparó una ejecución real (por push, PR o `workflow_dispatch`).
- [ ] URL de la ejecución en GitHub Actions (pégala aquí):

  ```
  https://github.com/<owner>/<repo>/actions/runs/<run-id>
  ```

- [ ] La ejecución muestra estado **verde** (Success) en ambas versiones de la matrix (3.11 y 3.12).
- [ ] Screenshot o grabación que muestra:
  - [ ] Lista de runs con badge verde.
  - [ ] Job `Tests (Python 3.11)` y `Tests (Python 3.12)` ambos en verde.
  - [ ] Step `Run tests with coverage` expandido con el log de pytest.
  - [ ] Línea de cobertura en el log (`Total coverage: 99.78%` o similar).
  - [ ] Step summary con el resumen Markdown generado automáticamente.
- [ ] Sección **Artifacts** de la ejecución muestra `test-artifacts-py3.11` y `test-artifacts-py3.12`.

---

## Criterio 2 — Commit message generado con Copilot

- [ ] Cambio real staged en VS Code (archivos visibles en el panel Source Control).
- [ ] Screenshot del panel **Source Control** con los archivos staged y el campo de commit visible.
- [ ] Copilot generó el mensaje de commit usando alguna de estas vías:
  - [ ] Botón de chispa/estrella de Copilot en el campo de commit de VS Code, **o**
  - [ ] Prompt en Copilot Chat con la instrucción de Conventional Commits.
- [ ] Screenshot o captura del mensaje sugerido por Copilot antes de aceptarlo.
- [ ] Commit aplicado con el mensaje generado (o ajustado) por Copilot.
- [ ] El mensaje sigue el formato Conventional Commits (`feat:`, `fix:`, `ci:`, `docs:`, etc.).
- [ ] Commit visible en el historial:

  ```bash
  git log --oneline -n 5
  ```

  Resultado esperado (ejemplo):

  ```
  abc1234 ci: add headless SDL2 env vars for pygame tests
  ```

---

## Criterio 3 (Opcional) — PR Summary generado con Copilot

No marques esta sección sin evidencia real en GitHub.

- [ ] PR abierto en el repositorio con URL (pégala aquí):

  ```
  https://github.com/<owner>/<repo>/pull/<number>
  ```

- [ ] Copilot generó el summary del PR usando alguna de estas vías:
  - [ ] Botón **Copilot** en el campo de descripción del PR en GitHub, **o**
  - [ ] Prompt en Copilot Chat con instrucción de generar el body del PR.
- [ ] Screenshot del summary generado por Copilot visible en el PR.
- [ ] El summary incluye al menos: descripción del cambio, lista de modificaciones
      y sección de cómo probar.

---

## Resumen de estado

| Criterio | Estado |
|----------|--------|
| CI pipeline funcional con runs verdes | Pendiente evidencia |
| Commit message con Copilot | Pendiente evidencia |
| PR Summary con Copilot (opcional) | Pendiente evidencia |
