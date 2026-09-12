# Customer Portfolio System

> **Oracle Database + PL/SQL + FastAPI + Modern Backend Architecture**

An independent portfolio project that combines Oracle Database and PL/SQL
business logic with a modern Python backend built on FastAPI and SQLModel.

The project explores how traditional enterprise database technologies can
coexist with modern REST API architectures, containerization, automated
testing, and CI/CD practices.

## Why I Built This Project

My professional background is primarily in the Oracle ecosystem: SQL,
PL/SQL, Oracle Forms and Reports, and enterprise transactional applications.

In parallel, I have been building practical experience with modern backend
technologies — Python, FastAPI, REST APIs, Docker, automated testing, and
CI/CD — through independent projects and training.

This project brings both areas together and demonstrates how to work with
Oracle database logic while applying modern backend development practices.

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
│             Oracle Database 21c XE           │
│                                              │
│   PL/SQL Procedures · Triggers · Views       │
└──────────────────────────────────────────────┘
```

Architecture principles:

- FastAPI handles HTTP requests and exposes REST endpoints.
- The service layer contains application logic and coordinates database operations.
- SQLModel provides data models and database interaction.
- PL/SQL implements selected database-level operations and auditing.
- Alembic manages database migrations (single initial migration as Alembic root).
- Docker + Docker Compose provide a reproducible development environment.

### Oracle + Modern Backend

One of the main goals of this project is to demonstrate the coexistence of
Oracle database technologies with a modern Python backend:

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
```

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

## Repository Layout

```text
.
├── alembic/                    # Migration environment
│   └── versions/               # Initial complete migration (Alembic root)
├── app/
│   ├── api/                    # FastAPI routers (clientes, cartera, healthcheck)
│   ├── core/                   # Cross-cutting concerns
│   ├── database/               # Connection, schema bootstrap
│   ├── models/                 # SQLModel models
│   └── services/               # Business logic / PL/SQL integration
├── tests/                      # Pytest suite (API + services)
├── apply_schema.py             # Applies Oracle objects from app/database/esquema.sql
├── cleanup.py                  # Optional environment cleanup
├── seed_db.py                  # Demo data loader
├── docker-compose.yml          # API + Oracle XE services
└── Dockerfile                  # API image
```

## Prerequisites

- Docker with Docker Compose (the whole stack runs in containers; no local
  Python or Oracle installation is required).
- Ports **8000** (API) and **1522** (Oracle host port) must be free.

## Quick Start

```bash
# 1. Configure environment (optional overrides)
#    cp .env.example .env   (defaults connect to the compose service)

# 2. Build and start the stack (waits for the DB healthcheck)
docker compose up -d --wait

# 3. Apply database migrations and bootstrap Oracle objects
docker compose exec api alembic upgrade head
docker compose exec api python apply_schema.py

# 4. Load demo data (optional)
docker compose exec api python seed_db.py
```

The API is then available at [http://localhost:8000](http://localhost:8000).

> Note: `docker compose up -d --wait` ensures the Oracle container is truly
> up before the API starts; the Oracle image takes a bit to initialize.

## Database Bootstrap

The schema is versioned with Alembic:

1. The initial migration creates the eight tables used by the application.
   Every primary key uses a **database-generated identity column**
   (`GENERATED BY DEFAULT AS IDENTITY`), so the schema is atomic and works
   with SQLAlchemy out of the box.
2. `apply_schema.py` applies the PL/SQL layer defined in `app/database/esquema.sql`
   (idempotent, safe to re-run):
   - `VW_RESUMEN_CARTERA` — consolidated portfolio view.
   - `TRG_AUDIT_CARTERA` — audit trigger on `CARTERA` writing to `AUD_CARTERA`.
   - `SP_TRANSFERIR_SALDO` — stored procedure for balance transfers.
   - `SP_GET_MOVIMIENTOS` — stored procedure for audit history.
   - `FN_CALCULAR_TASAS` — function for rate calculations.

## API Usage

Interactive documentation is available at:
👉 **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Main Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/clientes/` | List all clients. |
| GET | `/cartera/resumen` | Consolidated balance report (PL/SQL view). |
| POST | `/cartera/transferir` | Transfer between portfolios (PL/SQL procedure). |
| GET | `/cartera/movimientos/{id}` | Audit history for a portfolio (trigger + `AUD_CARTERA`). |
| GET | `/health` | Service health check. |

## Testing & Code Quality

Run the test suite and linter inside a dev container (no local Python needed):

```bash
# Unit + integration tests
docker run --rm -v "C:/path/to/repo:/src" -w /src fintech-api-test-dev sh -c "pytest -q"

# Linting
docker run --rm -v "C:/path/to/repo:/src" -w /src fintech-api-test-dev sh -c "ruff check ."
```

The CI pipeline (GitHub Actions) runs: Ruff (`lint`), Bandit and Safety
(`security`, safety failures are non-fatal), a Docker build, and the
full Pytest suite (`test`).

## Troubleshooting & Known Limitations

- **`alembic check` reports every table as "added" on Oracle.** This is a
  known false positive of the Alembic autogenerate reflection on Oracle:
  models use lowercase names while Oracle stores them uppercase, so the
  `compare_metadata` comparison reports clean tables as new. There is no real
  schema drift — use `docker compose exec api python apply_schema.py` and
  `alembic upgrade head` as the source of truth.
- **`The "FRONTEND_URL" variable is not set` warning.** The compose file
  forwards `FRONTEND_URL` when defined; it is read from `.env` and has no
  effect on the backend when unset. It is informational only.
- **Oracle healthcheck.** The compose healthcheck runs the container's own
  `/opt/oracle/checkDBStatus.sh`; startup can take several seconds. Use
  `docker compose up -d --wait` to block until the stack is ready.

## Configuration

Database connection settings are read from environment variables (defaults
shown in `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `DB_USER` | `system` | Oracle user. |
| `ORACLE_PWD` | *(required)* | Oracle password (`oracle` for the demo image). |
| `DB_HOST` | `localhost` | Database host (`db` inside the compose network). |
| `DB_PORT` | `1522` | Host port mapped to Oracle's `1521`. |
| `DB_SERVICE_NAME` | `XEPDB1` | Oracle pluggable database service name. |