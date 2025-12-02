"""Typer CLI za eksperimentisanje sa botom."""

from __future__ import annotations

import asyncio

import typer

from typing import Optional

from ..services.assistant_service import AssistantService

app = typer.Typer(help="CLI interfejs za customer assistant bota.")
_service = AssistantService()


@app.callback()
def main() -> None:
    """Osnovni interfejs za pomoć API pozivima."""


@app.command()
def ask(question: str, order_id: Optional[str] = typer.Option(None, help="Opcioni broj porudžbine")) -> None:
    """Postavlja pitanje botu i ispisuje stub odgovor."""

    result = asyncio.run(_service.handle_query(question, order_id))
    typer.echo(result.message)
    if result.order_status:
        status = result.order_status
        typer.echo(
            f"Status porudžbine {status.order_id}: {status.status}"
            + (f", ETA {status.eta}" if status.eta else "")
        )
        if status.tracking_url:
            typer.echo(f"Link za praćenje: {status.tracking_url}")
    if result.shipping_checkpoints:
        typer.echo("Shipping timeline:")
        for checkpoint in result.shipping_checkpoints:
            typer.echo(
                f" - {checkpoint.timestamp} | {checkpoint.location} | {checkpoint.status}: {checkpoint.description}"
            )
    if result.referenced_documents:
        typer.echo("Reference: " + ", ".join(result.referenced_documents))


if __name__ == "__main__":
    app()
