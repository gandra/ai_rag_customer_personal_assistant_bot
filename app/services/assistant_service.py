"""Centralna servisna logika za bot – trenutno samo stub koji koristi skeleton klijente."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..core.config import Settings, get_settings
from ..core.order_client import OrderServiceClient, OrderStatus
from ..core.policy_store import PolicyStore


@dataclass
class AssistantResponse:
    message: str
    order_status: Optional[OrderStatus] = None
    referenced_documents: list[str] | None = None


class AssistantService:
    """Spoj retrieval-a i poslovnih servisa (stub varianta)."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._order_client = OrderServiceClient(self._settings)
        self._policy_store = PolicyStore(self._settings)

    async def handle_query(self, question: str, order_id: str | None = None) -> AssistantResponse:
        """Na nivou PoC-a vraća statičan odgovor i eventualno stub status."""

        referenced_docs = [doc.title for doc in self._policy_store.list_documents()[:3]] or None
        status: OrderStatus | None = None
        if order_id:
            status = await self._order_client.get_status(order_id)
        msg = (
            "Skeleton odgovor: konsultuj docs/analysis.md za arhitekturu. "
            "Kada se implementira RAG orkestracija, ovde će se kombinovati order status i politike."
        )
        return AssistantResponse(message=msg, order_status=status, referenced_documents=referenced_docs)


__all__ = ["AssistantService", "AssistantResponse"]
