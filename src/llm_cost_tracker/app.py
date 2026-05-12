"""FastAPI application for the LLM Cost Tracker."""

from fastapi import FastAPI

from llm_cost_tracker.schemas import EventAccepted, EventIn

app = FastAPI(
    title="LLM Cost Tracker",
    description="Telemetry service for LLM cost tracking",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events", status_code=200)
async def ingest_event(event: EventIn) -> EventAccepted:
    # Week 1: validates schema only. Persistence + stream come in Weeks 2-3.
    _ = event
    return EventAccepted()
