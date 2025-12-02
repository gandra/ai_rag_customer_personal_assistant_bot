"""Mock servis koji simulira shipping timeline sa checkpointovima."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class ShippingCheckpoint:
    """Jedna stanica u dostavnoj ruti."""

    order_id: str
    timestamp: str
    location: str
    status: str
    description: str


_DEFAULT_EVENTS: dict[str, List[ShippingCheckpoint]] = {
    "A1001": [
        ShippingCheckpoint(
            order_id="A1001",
            timestamp="2025-03-16T09:10:00Z",
            location="Centralni magacin",
            status="PREPARING",
            description="Paket se pakuje i dobija etiketu.",
        ),
        ShippingCheckpoint(
            order_id="A1001",
            timestamp="2025-03-17T07:45:00Z",
            location="Beograd HUB",
            status="HANDOFF",
            description="Predato kuriru DPD, čeka prevoz.",
        ),
    ],
    "A1002": [
        ShippingCheckpoint(
            order_id="A1002",
            timestamp="2025-03-14T08:15:00Z",
            location="Berlin Sort Center",
            status="IN_TRANSIT",
            description="Špedicija je preuzela pošiljku.",
        ),
        ShippingCheckpoint(
            order_id="A1002",
            timestamp="2025-03-16T15:30:00Z",
            location="DPD Novi Sad",
            status="OUT_FOR_DELIVERY",
            description="Kurir je na ruti, očekivana isporuka danas.",
        ),
    ],
    "A1003": [
        ShippingCheckpoint(
            order_id="A1003",
            timestamp="2025-03-12T10:00:00Z",
            location="New York Warehouse",
            status="IN_TRANSIT",
            description="UPS je preuzeo paket za LA.",
        ),
        ShippingCheckpoint(
            order_id="A1003",
            timestamp="2025-03-15T18:00:00Z",
            location="Los Angeles",
            status="DELIVERED",
            description="Kupac je potpisao prijem.",
        ),
    ],
}


class ShippingStatusService:
    """In-memory servis za praćenje checkpointova."""

    def __init__(self, events: dict[str, List[ShippingCheckpoint]] | None = None) -> None:
        self._events = events or _DEFAULT_EVENTS

    def list_checkpoints(self, order_id: str) -> list[ShippingCheckpoint]:
        return list(self._events.get(order_id, []))

    def latest_checkpoint(self, order_id: str) -> ShippingCheckpoint | None:
        checkpoints = self._events.get(order_id, [])
        return checkpoints[-1] if checkpoints else None

    def all_orders(self) -> Iterable[str]:
        return self._events.keys()


__all__ = ["ShippingStatusService", "ShippingCheckpoint"]
