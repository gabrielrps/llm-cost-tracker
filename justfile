# LLM Cost Tracker — recipes
# Install just: winget install Casey.Just

# Default: show available recipes
default:
    @just --list

# Install/sync dependencies (creates .venv if needed)
sync:
    uv sync

# Run the dev server with auto-reload
dev:
    uv run uvicorn llm_cost_tracker.app:app --reload --host 0.0.0.0 --port 8000

# Start Postgres + Redis via docker compose
up:
    docker compose up -d

# Stop infra (keeps volumes)
down:
    docker compose down

# Stop infra and wipe volumes (nukes data)
nuke:
    docker compose down -v

# Run tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=src/llm_cost_tracker --cov-report=term-missing

# Lint with ruff
lint:
    uv run ruff check .

# Auto-fix lint issues where possible
lint-fix:
    uv run ruff check . --fix

# Format with ruff
fmt:
    uv run ruff format .

# Check formatting without writing
fmt-check:
    uv run ruff format --check .

# Type-check with mypy --strict
typecheck:
    uv run mypy src tests

# Run lint + format-check + typecheck + tests (CI parity locally)
check: lint fmt-check typecheck test
