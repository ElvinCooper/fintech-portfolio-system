# GEMINI.md

## Dev Environment Tips

Usa siempre un entorno virtual:

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Instala dependencias

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

> Para desarrollo rápido usa `pip install -e .` (si tienes `setup.py` o `pyproject.toml`).
> Evita instalar paquetes globales. Siempre trabaja dentro del `venv`.

---

## Tests

Corre todos los tests con:

```bash
pytest -v
```

O con cobertura:

```bash
pytest --cov=src --cov-report=term-missing
open htmlcov/index.html
```

Desde la raíz del proyecto también puedes usar:

```bash
python -m pytest
```

Para ejecutar tests específicos:

```bash
pytest -k "nombre_del_test"
```

O con patrón:

```bash
pytest -k "scraping or pdf"
```

---

## Linting & Tipos

Después de mover archivos o cambiar imports, siempre corre:

```bash
ruff check .        # linting rápido
ruff format .       # formateo (Black compatible)
mypy src            # verificación de tipos estáticos
```

> Todos los tests deben pasar y el linting debe estar limpio antes de hacer commit.
> Agrega o actualiza tests por cada cambio que hagas (aunque nadie te lo pida).

---

## PR Instructions

**Título del PR:** Descripción corta y clara

**Ejemplos:**
- `Añadir extracción de tablas de PDF`
- `Mejorar logging y manejo de errores en scraper`

Antes de hacer commit siempre ejecuta:

```bash
ruff check --fix .
ruff format .
pytest
```

> El CI de GitHub Actions (`.github/workflows/ci.yml`) debe pasar en verde.

**Incluye en la descripción del PR:**
- Qué se cambió
- Por qué
- Cómo probarlo

---

## Integración Continua (CI/CD)

Ejemplo básico `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements-dev.txt
      - run: ruff check .
      - run: ruff format --check .
      - run: pytest --cov=src
```