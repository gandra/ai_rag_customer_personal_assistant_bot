"""Typer komande za direktan pristup mock order/shipping servisima."""

from __future__ import annotations

import asyncio
import json

import typer

from ..services.order_status_service import OrderStatusService
from ..services.shipping_status_service import ShippingStatusService


app = typer.Typer(help="Mock helper komande za order i shipping servise.")
_order_service = OrderStatusService()
_shipping_service = ShippingStatusService()


@app.command()
def order_status(order_id: str) -> None:
    """Prikaži mock status porudžbine."""

    status = asyncio.run(_order_service.get_status(order_id))
    note = _order_service.get_note(order_id)
    output = status.__dict__ | {"note": note}
    typer.echo(json.dumps(output, ensure_ascii=False, indent=2))


@app.command()
def shipping_timeline(order_id: str) -> None:
    """Prikaži shipping checkpoint timeline."""

    checkpoints = _shipping_service.list_checkpoints(order_id)
    data = [checkpoint.__dict__ for checkpoint in checkpoints]
    typer.echo(json.dumps({"order_id": order_id, "checkpoints": data}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
