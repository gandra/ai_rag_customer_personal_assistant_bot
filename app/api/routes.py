"""FastAPI rute (još uvek stub)."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.assistant_service import AssistantResponse, AssistantService

router = APIRouter(prefix="/api", tags=["assistant"])
_service = AssistantService()


class AskRequest(BaseModel):
    question: str = Field(..., description="Prirodni jezik kupca")
    order_id: Optional[str] = Field(default=None, description="Opcioni broj porudžbine")


class AskResponse(BaseModel):
    answer: str
    order_status: Optional[dict] = None
    referenced_documents: list[str] | None = None

    @classmethod
    def from_domain(cls, domain: AssistantResponse) -> "AskResponse":
        status_dict = None
        if domain.order_status:
            status_dict = domain.order_status.__dict__
        return cls(answer=domain.message, order_status=status_dict, referenced_documents=domain.referenced_documents)


@router.post("/ask", response_model=AskResponse)
async def ask_bot(payload: AskRequest) -> AskResponse:
    if not payload.question:
        raise HTTPException(status_code=400, detail="question je obavezan")
    result = await _service.handle_query(payload.question, payload.order_id)
    return AskResponse.from_domain(result)


__all__ = ["router", "AskRequest", "AskResponse"]
