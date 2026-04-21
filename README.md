# GitHub Copilot – WhatTheHack 071

[![CI](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml/badge.svg)](https://github.com/Gabriels114/CopilotDay/actions/workflows/ci.yml)

Desarrollo personal de los retos del hackathon [WhatTheHack 071 – GitHub Copilot](https://github.com/microsoft/WhatTheHack/tree/master/071-GitHubCopilot) de Microsoft.

## Challenges

| # | Tema | Estado | 
|---|------|--------|
| [00](./challenges/00-prerequisites/) | Prerequisitos | ✅ Documentado |
| [01](./challenges/01-intro/) | Introducción a GitHub Copilot | ✅ Producción (99% cobertura) |
| [02](./challenges/02-best-practices/) | Best Practices con Copilot | ✅ Difficulty Levels + Técnicas |
| [03](./challenges/03-mcp/) | Extensión con Model Context Protocol | ⚠️ Configurado, pendiente ejecutar |
| [04](./challenges/04-customization/) | Personalización en el IDE | ✅ Instrucciones + Agentes |
| [05](./challenges/05-dev-workflow/) | Copilot en el flujo de desarrollo | ✅ Git + CI/CD |
| [06](./challenges/06-tests-docs/) | Tests y Documentación | ✅ Suite 198 tests |
| [07](./challenges/07-debug-optimization/) | Debugging y Optimización | ✅ OWASP Security Case |

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

- `00` ya tiene checklist y guía de validación, pero depende de confirmación manual del entorno.
- `01` ya es un juego funcional en Python con tests y base suficiente para `02`, `05` y `06`.
- `03` ya tiene configuración MCP corregida en el repo, pero todavía requiere validación local con Docker y `GITHUB_TOKEN`.
- `05` y `06` ya tienen base real gracias al CI, la cobertura y la suite de tests, aunque todavía falta cerrar su evidencia final.
