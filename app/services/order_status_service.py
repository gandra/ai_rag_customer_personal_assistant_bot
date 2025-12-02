"""Lokalni mock servis za order status – koristi statičke podatke za PoC."""

from __future__ import annotations

from dataclasses import dataclass

from ..core.order_client import OrderStatus


@dataclass(frozen=True)
class OrderStatusRecord:
    """Detalji o porudžbini koje prikazuje mock servis."""

    status: str
    eta: str | None
    tracking_url: str | None
    note: str


_DEFAULT_ORDERS: dict[str, OrderStatusRecord] = {
    "A1001": OrderStatusRecord(
        status="PREPARING",
        eta="2025-03-20",
        tracking_url="https://tracking.example.com/A1001",
        note="Plaćanje potvrđeno, čeka preuzimanje od kurira.",
    ),
    "A1002": OrderStatusRecord(
        status="SHIPPED",
        eta="2025-03-18",
        tracking_url="https://tracking.example.com/A1002",
        note="Paket je kod kurira DPD i putuje ka Beogradu.",
    ),
    "A1003": OrderStatusRecord(
        status="DELIVERED",
        eta="2025-03-15",
        tracking_url="https://tracking.example.com/A1003",
        note="Kurir je potvrdio isporuku kupcu 15. marta.",
    ),
}


class OrderStatusService:
    """In-memory mock koji simulira eksterni order servis."""

    def __init__(self, orders: dict[str, OrderStatusRecord] | None = None) -> None:
        self._orders = orders or _DEFAULT_ORDERS

    async def get_status(self, order_id: str) -> OrderStatus:
        record = self._orders.get(order_id)
        if not record:
            return OrderStatus(order_id=order_id, status="unknown", eta=None, tracking_url=None)
        return OrderStatus(
            order_id=order_id,
            status=record.status,
            eta=record.eta,
            tracking_url=record.tracking_url,
        )

    def get_note(self, order_id: str) -> str | None:
        record = self._orders.get(order_id)
        return record.note if record else None


__all__ = ["OrderStatusService", "OrderStatusRecord"]
