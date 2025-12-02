"""FastAPI rute (još uvek stub)."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.assistant_service import AssistantResponse, AssistantService
from ..services.order_status_service import OrderStatusRecord, OrderStatusService
from ..services.shipping_status_service import ShippingCheckpoint, ShippingStatusService

router = APIRouter(prefix="/api", tags=["assistant"])
_service = AssistantService()
_order_service = OrderStatusService()
_shipping_service = ShippingStatusService()


class AskRequest(BaseModel):
    question: str = Field(..., description="Prirodni jezik kupca")
    order_id: Optional[str] = Field(default=None, description="Opcioni broj porudžbine")


class AskResponse(BaseModel):
    answer: str
    order_status: Optional[dict] = None
    shipping_checkpoints: list[dict] | None = None
    referenced_documents: list[str] | None = None

    @classmethod
    def from_domain(cls, domain: AssistantResponse) -> "AskResponse":
        status_dict = None
        if domain.order_status:
            status_dict = domain.order_status.__dict__
        checkpoint_dicts = None
        if domain.shipping_checkpoints:
            checkpoint_dicts = [checkpoint.__dict__ for checkpoint in domain.shipping_checkpoints]
        return cls(
            answer=domain.message,
            order_status=status_dict,
            shipping_checkpoints=checkpoint_dicts,
            referenced_documents=domain.referenced_documents,
        )


@router.post("/ask", response_model=AskResponse)
async def ask_bot(payload: AskRequest) -> AskResponse:
    if not payload.question:
        raise HTTPException(status_code=400, detail="question je obavezan")
    result = await _service.handle_query(payload.question, payload.order_id)
    return AskResponse.from_domain(result)


class OrderStatusResponse(BaseModel):
    order_id: str
    status: str
    eta: str | None
    tracking_url: str | None
    note: str | None


@router.get("/orders/{order_id}", response_model=OrderStatusResponse, tags=["mock-orders"])
async def get_order_status(order_id: str) -> OrderStatusResponse:
    status = await _order_service.get_status(order_id)
    note = _order_service.get_note(order_id)
    return OrderStatusResponse(
        order_id=status.order_id,
        status=status.status,
        eta=status.eta,
        tracking_url=status.tracking_url,
        note=note,
    )


class ShippingTimelineResponse(BaseModel):
    order_id: str
    checkpoints: list[ShippingCheckpoint]


@router.get("/shipping/{order_id}", response_model=ShippingTimelineResponse, tags=["mock-orders"])
async def get_shipping_timeline(order_id: str) -> ShippingTimelineResponse:
    checkpoints = _shipping_service.list_checkpoints(order_id)
    return ShippingTimelineResponse(order_id=order_id, checkpoints=checkpoints)


__all__ = ["router", "AskRequest", "AskResponse"]
