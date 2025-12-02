# rag_customer_personal_assistant_bot

RAG-based bot koji spaja znanje iz internih politika/procedura sa operativnim servisima za porudžbine, fakture i zalihe. Projekat je podeljen na ingestion+retrieval sloj (vektor store + BM25), orkestraciju (LlamaIndex/LangChain), i klijente za real-time API-je. 

- Kompletnu arhitektonsku analizu i poređenje pristupa potraži u `docs/analysis.md`.
- Kod je za sada samo skeleton (FastAPI + Typer + core config). Nakon potvrde arhitekture i PoC plana slede konkretne implementacije.

## Brzi start
1. Kreiraj virtuelno okruženje i instaliraj zavisnosti iz `pyproject.toml`:
   ```bash
   cd rag_customer_personal_assistant_bot
   uv venv --python 3.12
   uv sync
   ```
2. Kopiraj `.env.example` u `.env` i postavi URL-ove (order/inventory/billing) i LLM kredencijale.
3. Pokreni FastAPI skeleton (samo health + stub endpoint):
   ```bash
   uv run uvicorn app.api.main_api:app --reload
   ```
4. CLI prototip (stub):
   ```bash
   uv run python -m app.cli.main_cli ask "Gde je moja porudžbina?"
   ```

> Napomena: Dok se ne razvije ingestion i servisi, API/CLI vraćaju placeholder odgovore sa uputom na `docs/analysis.md`.
