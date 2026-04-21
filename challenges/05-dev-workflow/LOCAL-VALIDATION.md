# Local Validation - Challenge 05

Validación ejecutada localmente el `2026-04-21 16:43:23 CST`.

## Comando

```bash
cd challenges/01-intro
pytest tests/ --cov=. --cov-report=term-missing --cov-report=xml --cov-fail-under=80 -q
```

## Resultado

```text
199 passed, 1 warning in 0.46s
Required test coverage of 80% reached. Total coverage: 99.78%
Coverage XML written to file coverage.xml
```

## Lectura del resultado

- El conjunto de pruebas pasó completo.
- La cobertura supera ampliamente el umbral exigido por el workflow.
- El archivo `coverage.xml` se genera correctamente, que es lo que luego sube el workflow como artefacto.

## Nota

Esta validación demuestra que el comando equivalente al CI funciona en local. La evidencia final del reto requiere además una corrida visible en GitHub Actions con su URL y estado verde.
