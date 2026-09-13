# AGENTS.md

## Run (Docker-first)

- `docker compose up -d --wait` — blocks on the Oracle healthcheck, which can take minutes.
- Then, in order:
  - `docker compose exec api alembic upgrade head`
  - `docker compose exec api python apply_schema.py` (idempotent; applies the PL/SQL layer from `app/database/esquema.sql`)
  - optional: `docker compose exec api python seed_db.py`
- Ports 8000 (API) and 1522 (host → Oracle 1521) must be free. API + Swagger at http://localhost:8000/docs.

## Tests (no DB needed)

- Fully mocked: `conftest.py` overrides the async session and API tests `AsyncMock` service functions. `pytest -q` passes with no Oracle running (CI runs it on a bare runner).
- Locally: `pip install -r requirements-dev.txt`, then `pytest -q`.
- README's `fintech-api-test-dev` container image is built manually — there is no Dockerfile or compose target for it in the repo.

## Lint gate (CI enforces both, run before commit/PR)

- `ruff check .` AND `ruff format --check .` — both must pass.
- Config in `pyproject.toml`: line-length 120, rules `E,F,W,I,B,C4,UP`; `alembic/versions` is excluded from ruff.
- mypy is NOT configured — ignore gemini.md's mention of it.

## Database / Alembic gotchas

- `alembic check` reports every table as "added" on Oracle: KNOWN false positive (lowercase SQLModel names vs uppercase Oracle). Never trust it; source of truth is `apply_schema.py` + `alembic upgrade head`.
- There is a single root migration, `2950f69ad7c4` ("initial complete migration"). Ignore the stale `*.pyc` files in `alembic/versions/__pycache__` (old revision IDs) — they are not live migrations.
- `alembic.ini`'s `sqlalchemy.url` is a placeholder; `env.py` builds the real DSN from env vars.
- Build the DSN only via `app/database/connection.py:build_dsn()` — the single source used by the API, alembic, `seed_db.py`, and `cleanup.py`. Do not duplicate DSN construction.
- PL/SQL objects (VIEW/TRIGGER/SP/FN) live in `app/database/esquema.sql`; edit there and rerun `apply_schema.py`. Services invoke them with raw `text()` + `bindparam(isoutparam=True)` and MUST pass initial values for OUT params (see `portfolio_services.transferir_saldo`; initial values are required to avoid bind/cache conflicts).

## Repo conventions & caveats

- Code comments, docstrings, and commit messages are in Spanish (types like `Fix:`, `Doc:`, or ticket prefixes `F0:`, `F2:`, `F10:`). README is English. Match the file's language when editing.
- DIRECTRICES.md prescribes Git Flow with a `develop` branch, but `develop` does NOT exist. Actual workflow: `main` + topic branches merged via PR.
- `.env` is gitignored (use `.env.example` as reference). The `FRONTEND_URL` "variable is not set" warning is benign; CORS is only added when `FRONTEND_URL` is set and is limited to GET/POST/OPTIONS. No authentication is implemented.
- Layered layout: `app/api` (FastAPI routers) → `app/services` → `app/models` (SQLModel) → Oracle. `app/core/` is currently empty.
- Connection defaults: `DB_USER=system`, `ORACLE_PWD=oracle`, `DB_HOST=localhost`, `DB_PORT=1522`, `DB_SERVICE_NAME=XEPDB1` (compose overrides DB_HOST/DB_PORT/DB_SERVICE_NAME to reach the `db` service).