---
description: 'Guidance for Python test files in the Whack-a-Mole project.'
applyTo: 'challenges/01-intro/tests/**/*.py'
---

# Python Test Instructions

- Use `pytest` style tests with descriptive names.
- Prefer direct behavior assertions over implementation-detail assertions.
- Keep fixtures small and local unless they are reused broadly.
- When adding new tests for game logic, mirror the existing module naming pattern.
- Preserve the current headless pygame setup from `conftest.py`.
- Avoid random or time-sensitive assertions unless the test controls the source of randomness or time.
