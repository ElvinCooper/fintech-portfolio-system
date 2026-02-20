# DIRECTRICES TÉCNICAS DEL PROYECTO

## 1. Filosofía y Principios Generales

- **KISS (Keep It Simple, Stupid):** Prefiere soluciones simples y claras sobre las complejas.
- **DRY (Don't Repeat Yourself):** Reutiliza la lógica a través de funciones o clases. Evita el código duplicado.
- **YAGNI (You Ain't Gonna Need It):** No implementes funcionalidades que no sean estrictamente necesarias para los requisitos actuales.
- **Comentarios:** El código debe ser autoexplicativo. Usa comentarios solo para explicar el *porqué* de una implementación compleja, no el *qué*.

## 2. Git y Control de Versiones

### Estrategia de Ramas (Git Flow Simplificado)

- `main`: Rama principal. Siempre debe estar en un estado desplegable. Las fusiones a `main` solo se hacen a través de Pull Requests (PRs).
- `develop`: Rama de integración. Aquí se fusionan las nuevas funcionalidades.
- `feature/<nombre-descriptivo>`: Ramas para nuevas funcionalidades. Se crean a partir de `develop`. Ejemplo: `feature/crud-usuarios`.
- `fix/<nombre-descriptivo>`: Ramas para corrección de errores. Se crean a partir de `develop` (o `main` si es un hotfix urgente). Ejemplo: `fix/error-calculo-impuestos`.

### Commits

- **Atómicos:** Cada commit debe representar un cambio lógico y completo.
- **Mensajes Claros (Conventional Commits):** Sigue el formato `tipo(alcance): mensaje`.
  - `feat`: Una nueva funcionalidad.
  - `fix`: Una corrección de error.
  - `docs`: Cambios en la documentación.
  - `style`: Cambios de formato (espacios, puntos y comas, etc.).
  - `refactor`: Refactorización de código que no altera la funcionalidad.
  - `test`: Añadir o corregir tests.
  - `chore`: Tareas de mantenimiento (actualizar dependencias, etc.).
- **Ejemplo:** `feat(auth): implementar endpoint para login con JWT`

## 3. Python y FastAPI

- **Estilo de Código:** Sigue estrictamente **PEP 8**. Usa un formateador como `black` y un linter como `ruff` para asegurar la consistencia.
- **Estructura del Proyecto:** Mantén la estructura modular actual (`app/api`, `app/services`, `app/models`, etc.).
- **Dependencias:** Gestiona las dependencias con `pip` y `requirements.txt`. Usa `pip-tools` para compilar las dependencias y mantener el entorno reproducible.
- **Asincronía:** Usa `async` y `await` en todas las operaciones de I/O (consultas a base de datos, llamadas a otras APIs) para no bloquear el servidor.
- **Inyección de Dependencias:** Utiliza el sistema de inyección de dependencias de FastAPI (`Depends`) para gestionar recursos como las sesiones de base de datos.
- **Validación de Datos:** Usa **Pydantic** para definir los esquemas de entrada y salida (`schemas`). Esto garantiza la validación, serialización y documentación automática.
- **Manejo de Errores:** Centraliza el manejo de excepciones con `Exception Handlers` de FastAPI para devolver respuestas de error consistentes y claras.

## 4. SQLAlchemy y PostgreSQL

- **Migraciones:** Usa **Alembic** para todas las migraciones de base de datos. Nunca modifiques el esquema de la base de datos de producción manualmente.
  - Genera una nueva migración para cada cambio en los modelos.
- **Modelos:** Define todos los modelos de SQLAlchemy en `app/models`. Deben reflejar las tablas de la base de datos de manera clara.
- **Optimización de Consultas:**
  - Evita el problema "N+1". Utiliza `selectinload` o `joinedload` para cargar relaciones de forma eficiente.
  - Selecciona solo las columnas que necesites (`.with_entities(Model.columna)`).
- **Sesiones:** La sesión de base de datos (`Session`) debe ser gestionada por petición. Usa `Depends` para inyectarla y asegúrate de que se cierre al final de cada petición.

## 5. Docker

- **Imágenes Base:** Usa imágenes base oficiales y ligeras, como `python:3.11-slim`.
- **Builds Multi-etapa:** Utiliza builds multi-etapa para separar las dependencias de compilación de las de ejecución, manteniendo la imagen final lo más pequeña posible.
- **Usuario no-root:** Ejecuta el contenedor con un usuario sin privilegios de `root` por seguridad.
- **`.dockerignore`:** Utiliza un archivo `.dockerignore` para excluir archivos innecesarios del contexto de build (ej. `venv/`, `__pycache__/`, `.git/`).
- **Composición:** Define los servicios de la aplicación (`api`, `db`) en `docker-compose.yml` para facilitar el desarrollo y despliegue local.

## 6. Seguridad

- **Autenticación:** Implementa **OAuth2 con JWT** para proteger los endpoints. El token debe tener una vida corta.
- **Autorización:** Define roles y permisos claros. Valida los permisos del usuario en los endpoints que lo requieran (ej. un usuario `admin` puede hacer más que un usuario `viewer`).
- **Validación de Entradas:** FastAPI con Pydantic se encarga de la mayoría de las validaciones. Nunca confíes en los datos que provienen del cliente.
- **Gestión de Secretos:**
  - **NUNCA** guardes secretos (contraseñas, API keys, claves de JWT) en el código.
  - Cárgalos desde variables de entorno. En Docker, usa el archivo `.env` y el parámetro `env_file`.
  - Para producción, utiliza un gestor de secretos como HashiCorp Vault, AWS Secrets Manager o Google Secret Manager.
- **Escaneo de Dependencias:** Regularmente, escanea las dependencias del proyecto en busca de vulnerabilidades conocidas usando herramientas como `pip-audit` o `Snyk`.

## 7. Pruebas (Testing)

- **Unit Tests:** Cada función de lógica de negocio (en `app/services`) debe tener su propia prueba unitaria.
- **Integration Tests:** Crea pruebas de integración para los endpoints de la API. Estas pruebas deben usar una base de datos de prueba separada.
- **Cobertura de Código:** Apunta a una alta cobertura de código (idealmente >80%). Usa herramientas como `pytest-cov`.
- **Framework:** Utiliza `pytest` como el framework de pruebas.
