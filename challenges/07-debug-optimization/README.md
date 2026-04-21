# Challenge 07 - Debugging y Optimización con Copilot

Este reto está resuelto como un ejercicio autocontenido inspirado en `routes/order.ts` de `OWASP Juice Shop`, tal como sugiere la guía oficial de `WhatTheHack 071`.

## Objetivo

- Entender un fragmento de código heredado.
- Detectar una vulnerabilidad realista en el flujo de cupones.
- Corregirla.
- Mejorar legibilidad y mantenibilidad.

## Qué incluye esta carpeta

- `src/coupon-discount.vulnerable.js`: versión inspirada en Juice Shop con validación insegura.
- `src/coupon-discount.fixed.js`: versión corregida y refactorizada.
- `test/coupon-discount.test.js`: pruebas que demuestran el problema y la mitigación.
- `package.json`: script mínimo para ejecutar tests con Node.

## Vulnerabilidades modeladas

La versión vulnerable (`coupon-discount.vulnerable.js`) tiene **dos bugs distintos** — ideal para practicar detección con Copilot:

**Bug 1 — Token sin firma (bug de diseño / seguridad crítica)**
El token es simplemente `base64(CODIGO-TIMESTAMP)`. Cualquier cliente puede fabricar un cupón válido sin conocer ningún secreto. El servidor confía ciegamente en datos controlados por el atacante.

**Bug 2 — Comparación con coerción de tipos (bug sutil de JavaScript)**
```js
if (campaign && couponDate == campaign.validOn) {
```
`couponDate` es un `string`; `campaign.validOn` es un `number` (resultado de `Date.parse`). El operador `==` aplica coerción de tipos, por lo que `"1741392000000" == 1741392000000` es `true`. Usar `===` haría fallar silenciosamente todos los cupones de campaña. La versión correcta convierte explícitamente antes de comparar. Este es exactamente el tipo de bug que Copilot detecta bien cuando le preguntas "find subtle type bugs".

Ambos bugs replican la idea del snippet oficial: pedirle a Copilot que explique el código, encuentre los problemas y proponga correcciones.

## Solución aplicada

La versión corregida cambia el enfoque:

- Reemplaza el token Base64 sin firma por un token firmado con `HMAC-SHA256`.
- Valida estructura, longitud y firma antes de aceptar el cupón.
- Define ventanas de validez por campaña usando `validFrom` y `validUntil`.
- Separa helpers pequeños para que el flujo sea más legible y testeable.

> **Nota para el ejercicio**: `DEFAULT_SIGNING_SECRET` está hardcodeado en `coupon-discount.fixed.js` como simplificación para el demo. En producción, el secreto debe cargarse desde una variable de entorno (ej. `process.env.COUPON_SECRET`). Copilot señalará esto si le preguntas "are there any remaining security issues in the fixed version?"

## Cómo correrlo

Necesitas Node.js 18+.

```bash
cd challenges/07-debug-optimization
npm test
```

## Qué demostrar para el challenge

- Explicar qué hacía la versión vulnerable y por qué era insegura.
- Mostrar que un cupón forjado funcionaba antes y ya no funciona.
- Mostrar que un cupón firmado sí funciona dentro de la ventana válida.
- Explicar qué sugirió Copilot y qué criterio humano usaste para aceptar o rechazar cambios.

## Prompts útiles para Copilot

- `Explain what calculateApplicableDiscount is doing and where the trust boundary is.`
- `Find the security issue in this coupon validation flow.`
- `Refactor this code to use signed coupon tokens and safer validation.`
- `Write tests that prove the vulnerable version can be forged and the fixed version rejects tampering.`
- `Suggest readability and maintainability improvements without changing behavior.`

## Fuentes

- Challenge oficial: <https://github.com/microsoft/WhatTheHack/blob/master/071-GitHubCopilot/Student/Challenge-07.md>
- Guía del coach: <https://github.com/microsoft/WhatTheHack/blob/master/071-GitHubCopilot/Coach/Solution-07.md>
- Archivo de referencia en Juice Shop: <https://github.com/juice-shop/juice-shop/blob/master/routes/order.ts>
