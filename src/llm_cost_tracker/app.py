"""FastAPI application for the LLM Cost Tracker."""

from collections import deque

from fastapi import FastAPI

from llm_cost_tracker.schemas import EventAccepted, EventIn

app = FastAPI(
    title="LLM Cost Tracker",
    description="Telemetry service for LLM cost tracking",
    version="0.1.0",
)

_recent_events: deque[EventIn] = deque(maxlen=50)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events", status_code=200)
async def ingest_event(event: EventIn) -> EventAccepted:
    # Week 1: validates schema only. Persistence + stream come in Weeks 2-3.
    _recent_events.append(event)
    return EventAccepted()


@app.get("/debug/last-events")
async def debug_last_events(limit: int = 20) -> list[EventIn]:
    """Retorna os últimos eventos aceitos (mais recente primeiro).

    Dev convenience. Sem persistência ainda — apenas memória do processo.
    """
    return list(_recent_events)[-limit:][::-1]
