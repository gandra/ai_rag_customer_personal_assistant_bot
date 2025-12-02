"""Placeholder za pristup politikama/procedurama."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import Settings, get_settings


@dataclass
class PolicyDocument:
    title: str
    path: Path
    summary: str


class PolicyStore:
    """Trenutno čita dokumenta iz lokalnog foldera dok ne nastupi pravi RAG."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def list_documents(self) -> list[PolicyDocument]:
        base = self._settings.knowledge_base_path
        if not base.exists():
            return []
        docs = []
        for path in base.rglob("*.md"):
            docs.append(PolicyDocument(title=path.stem, path=path, summary="N/A"))
        return docs


__all__ = ["PolicyStore", "PolicyDocument"]
