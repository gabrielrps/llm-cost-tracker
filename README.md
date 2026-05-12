# LLM Cost Tracker

Telemetry service for LLM cost tracking. Ingests usage events, computes cost per tenant in real time, alerts on budget overruns.

Build âncora da Fase 0 da trajetória AI Platform Engineer.

## Done quando (Fase 0)

- Ingere 10k eventos/s via Redis Streams
- Grafana mostra custo por tenant em tempo real
- Alerta de budget dispara em <30s

## Stack

- **API:** FastAPI + Pydantic v2
- **DB:** Postgres 16 (SQLAlchemy 2.0 async + Alembic)
- **Queue:** Redis Streams
- **Observability:** OpenTelemetry (traces) + Prometheus (metrics) + Grafana (dashboards)
- **Tooling:** uv, ruff, mypy --strict, pytest

## Pré-requisitos

- Python 3.12 (`.python-version` fixa)
- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just) — `winget install Casey.Just`
- Docker Desktop

## Quickstart

```powershell
just sync       # instala deps
just up         # sobe Postgres + Redis
just dev        # roda servidor com auto-reload
```

Em outro terminal:

```powershell
curl.exe -X POST http://localhost:8000/events `
  -H "Content-Type: application/json" `
  -d '{\"model_id\":\"claude-opus-4-7\",\"tenant_id\":\"tenant-a\",\"tokens_in\":1200,\"tokens_out\":350,\"timestamp\":\"2026-05-14T10:00:00Z\"}'
```

Health probe: `curl http://localhost:8000/health`

## Comandos (justfile)

```powershell
just              # lista todas as recipes
just test         # roda testes
just test-cov     # testes + coverage report
just lint         # ruff check
just lint-fix     # ruff check --fix
just fmt          # ruff format
just typecheck    # mypy --strict
just check        # lint + fmt-check + typecheck + test (paridade CI)
just up           # sobe infra
just down         # para infra
just nuke         # para infra + apaga volumes
```

## Estrutura

```
src/llm_cost_tracker/
├── __init__.py
├── app.py           # FastAPI app + endpoints
└── schemas.py       # Pydantic models

tests/
├── __init__.py
└── test_events.py
```

## Roadmap interno

- **Semana 1:** schema validation, FastAPI esqueleto, CI verde
- **Semana 2:** SQLAlchemy 2.0 async, Alembic, persistência, `GET /costs`
- **Semana 3:** Redis Streams, worker async, backpressure (429 em lag alto)
- **Semana 4:** OTel traces E2E, Prometheus metrics, Grafana dashboard, alerta budget

## Decisões de design

- **`extra="forbid"`** nos schemas: rejeita campos inesperados. Trade-off conhecido: clientes têm que ser exatos. Em troca, pega typo na origem.
- **`AwareDatetime`**: timestamp sem timezone é rejeitado. Em produção, naive datetime é fonte de bug.
- **Sem dependência de DB na Semana 1**: endpoint só valida. Persistência é problema da Semana 2.
- **`protected_namespaces=()`**: necessário porque `model_id` colide com namespace reservado do Pydantic v2.
