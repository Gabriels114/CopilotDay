# GitHub Copilot – WhatTheHack 071

[![CI](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml/badge.svg)](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml)

**Estado:** 🎉 Proyecto y retos completados en su totalidad.

Desarrollo personal de los retos del hackathon [WhatTheHack 071 – GitHub Copilot](https://github.com/microsoft/WhatTheHack/tree/master/071-GitHubCopilot) de Microsoft.

## Challenges

| # | Tema | Estado | 
|---|------|--------|
| [00](./challenges/00-prerequisites/) | Prerequisitos | ✅ Documentado |
| [01](./challenges/01-intro/) | Introducción a GitHub Copilot | ✅ Producción |
| [02](./challenges/02-best-practices/) | Best Practices con Copilot | ✅ Difficulty Levels + Técnicas |
| [03](./challenges/03-mcp/) | Extensión con Model Context Protocol | ✅ Completado y validado |
| [04](./challenges/04-customization/) | Personalización en el IDE | ✅ Completo (instrucciones + agentes) |
| [05](./challenges/05-dev-workflow/) | Copilot en el flujo de desarrollo | ✅ Validado en Actions |
| [06](./challenges/06-tests-docs/) | Tests y Documentación | ✅ Suite 199 tests (99.78% cobertura) |
| [07](./challenges/07-debug-optimization/) | Debugging y Optimización | ✅ OWASP Security Case validado |

## Estructura

```
challenges/
├── 00-prerequisites/
├── 01-intro/           ← Juego Whack-a-Mole (proyecto base)
├── 02-best-practices/
├── 03-mcp/
├── 04-customization/
├── 05-dev-workflow/
├── 06-tests-docs/
└── 07-debug-optimization/ ← Ejercicio aparte basado en OWASP Juice Shop
```

## Proyecto base

El hilo conductor de los retos **01–06** es un juego **Whack-a-Mole** que se va extendiendo con cada desafío.

El reto **07** es independiente: se resuelve sobre un fragmento de **OWASP Juice Shop** para practicar debugging, seguridad y optimización con Copilot.

## Referencia

- [Guía original para estudiantes](https://github.com/microsoft/WhatTheHack/tree/master/071-GitHubCopilot/Student)

## Estado actual

- `00` ya tiene checklist y guía, pero sigue dependiendo de validación manual del entorno.
- `01` y `02` están integrados sobre el juego base: el proyecto corre y la feature de dificultad ya está documentada e implementada.
- `03` configurado y validado exitosamente en VS Code con Docker y acceso a GitHub.
- `04` está completo y documentado, con instrucciones globales, instrucciones por contexto y agentes personalizados.
- `05` está completamente implementado, validado remotamente en GitHub Actions y con evidencia.
- `06` está validado localmente con `199 passed` y `99.78%` de cobertura.
- `07` está validado localmente con `5/5` tests Node pasando sobre la versión vulnerable y la corregida.
