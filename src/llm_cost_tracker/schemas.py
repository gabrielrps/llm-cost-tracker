"""Pydantic schemas for LLM cost tracking events."""

from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class EventIn(BaseModel):
    """Input schema for ingesting an LLM usage event."""

    model_config = ConfigDict(
        extra="forbid",
        protected_namespaces=(),
    )

    model_id: Annotated[str, Field(min_length=1, max_length=128)]
    tenant_id: Annotated[str, Field(min_length=1, max_length=128)]
    tokens_in: Annotated[int, Field(ge=0)]
    tokens_out: Annotated[int, Field(ge=0)]
    timestamp: AwareDatetime


class EventAccepted(BaseModel):
    """Acknowledgement returned after an event is accepted."""

    status: str = "accepted"
