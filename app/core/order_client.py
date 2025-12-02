"""HTTP klijent za Order servis - za sada samo skeleton."""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from .config import Settings, get_settings


@dataclass
class OrderStatus:
    order_id: str
    status: str
    eta: str | None = None
    tracking_url: str | None = None


class OrderServiceClient:
    """Wrapper oko eksternog API-ja koji vraća stanje porudžbine."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._client = httpx.AsyncClient(timeout=10)

    async def get_status(self, order_id: str) -> OrderStatus:
        """Poziva eksterni servis i vraća OrderStatus.

        Trenutno vraćamo stub dok se ne implementira pravi API poziv.
        """

        if not self._settings.order_service_url:
            return OrderStatus(order_id=order_id, status="unknown", eta=None, tracking_url=None)
        raise NotImplementedError("HTTP poziv ka order servisu će biti implementiran kada API specifikacija stigne.")


__all__ = ["OrderServiceClient", "OrderStatus"]
