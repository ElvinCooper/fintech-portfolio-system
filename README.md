# Customer Portfolio System

> **Oracle + PL/SQL + FastAPI + Modern Backend Architecture**

An independent portfolio project that combines Oracle Database and PL/SQL
business logic with a modern Python backend built with FastAPI and SQLModel.

The project was created to explore how traditional enterprise database
technologies can work together with modern REST API architectures,
containerization, automated testing, and CI/CD practices.

## Why I Built This Project

My professional background is primarily focused on the Oracle ecosystem,
including SQL, PL/SQL, Oracle Forms and Reports, and enterprise
transactional applications.

At the same time, I have been developing practical experience with
modern backend technologies such as Python, FastAPI, REST APIs, Docker,
automated testing, and CI/CD through independent projects and training.

This project brings both areas together.

It is an opportunity to demonstrate how I can work with Oracle database
logic while applying modern backend development practices.

## Architecture

The application follows a layered architecture:

```text
┌──────────────────────────────────────────────┐
│              FastAPI REST API                │
│              API Layer                       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              Service Layer                   │
│        Business Logic / PL/SQL Integration   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        Persistence Layer                     │
│        SQLModel + Oracle + Alembic           │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             Oracle Database 21c              │
│                                              │
│   PL/SQL Procedures · Triggers · Views       │
└──────────────────────────────────────────────┘


```


## Architecture principles
- FastAPI handles HTTP requests and REST endpoints.
- Service Layer contains application logic and coordinates database operations.
- SQLModel provides data models and database interaction.
- PL/SQL handles selected database-level operations and auditing.
- Alembic manages database migrations.
- Docker provides a reproducible development environment.

### `Oracle + Modern Backend`

```markdown
## Oracle + Modern Backend

One of the main goals of this project is to demonstrate the coexistence
of Oracle database technologies with a modern Python backend.

```text
Oracle / PL/SQL
      │
      │ Business Logic
      ▼
FastAPI / Python
      │
      │ REST API
      ▼
Modern Application Clients

## 🔌 Uso de la API

Una vez levantado el sistema, puedes acceder a la documentación interactiva:
👉 **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Endpoints Principales:
- `GET /clientes/`: Listado completo de clientes.
- `GET /cartera/resumen`: Vista consolidada de saldos.
- `POST /cartera/transferir`: Transferencia entre cuentas (Procedimiento PL/SQL).
- `GET /cartera/movimientos/{id}`: Historial de auditoría (Trigger).

## 🧪 Pruebas
Ejecuta la suite de pruebas unitarias y de integración:
```bash
pytest
```

# 8. Tech Stack

```markdown
## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Data Modeling | SQLModel |
| Database | Oracle Database 21c XE |
| Database Logic | PL/SQL |
| Migrations | Alembic |
| Testing | Pytest |
| Code Quality | Ruff |
| Security Analysis | Bandit, Safety |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| API Documentation | OpenAPI / Swagger |

```
