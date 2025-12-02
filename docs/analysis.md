# Customer Personal Assistant Bot – Architecture Analysis

## 1. Business kontekst i cilj
Digitalni asistent treba da odgovori na pitanja ulogovanih kupaca o statusu porudžbina i o servisnim/garantnim politikama. Bot mora da kombinuje **interna dokumenta** (politike, procedure, uputstva) sa **operativnim sistemima** (magacin, billing, logistika) i da iz odgovora ukloni poverljive podatke drugih kupaca. Fokus je na:
- WISMO („Where Is My Order?“) upitima sa dovođenjem broja porudžbine.
- Incidentima kvaliteta („proizvod pokvaren“) gde je potrebno voditi kupca kroz pravila i eskalacije.
- Proširivosti na dodatne scenarije (lojalti, fakture, proactive alerts).

## 2. Glavne persone i use-case scenariji
| Persona / Scenario | Opis potrebe | Izvori podataka | Obrada |
| --- | --- | --- | --- |
| Kupac ulogovan na portal – WISMO | Postavlja pitanje o statusu svoje narudžbine, bot traži broj porudžbine ako nije prisutan, proverava shipping API i sintetizuje odgovor sa narednim koracima. | Order Service, Shipping Provider API, Notification service | Tool-call → status → šablon odgovora sa ETA + link za praćenje |
| Kupac sa reklamacijom | Kupac opisuje problem (pokvaren uređaj). Bot klasifikuje tip problema, pronalazi relevantnu politiku/proceduru i predlaže opcije (zamena, servis, refund). | Dokument baza (politike, procedure), CRM tiket sistem | Dense retrieval + reasoning, eventualni workflow ticket |
| (Predlog) Kupac traži dokumente o fakturi i stanju plaćanja | Korisnik traži poslednju fakturu, želi da zna da li je plaćena. Bot validira identitet, dohvaća invoice status i generiše rezime. | ERP/Billing API, dokument storage | Retrieval + tool calling + sintetisanje |

**Dodatni scenario za razmatranje:** proaktivno informisanje o „Recall/Service Advisory“ događajima – kada kupac pita bilo šta u vezi uređaja, bot proverava da li postoji važeće sigurnosno obaveštenje i automatski ga uključuje u odgovor.

## 3. Domene podataka i konektori
1. **Knowledge Base** – PDF/Markdown politika, procedure, FAQ. Prelazi kroz ingestion pipeline: Firecrawl ili SharePoint connector → chunking → metadata tagging (tip dokumenta, jurisdikcija, datum). Čuva se u Milvus indeksu (lokalno koristimo Milvus Lite preko Docker Compose-a, produkciono Milvus Standalone / distributed) + `bm25` indeks za precizno pretraživanje.
2. **Operational APIs** – Order status, Inventory availability, Invoice service, Shipment tracking. Dostupno kroz REST/GraphQL, svaki servis obmotan Typer/FastAPI „tool“ endpointom sa keširanjem i audit logom.
3. **Customer Context** – Token iz sesije daje ID korisnika, preferirani jezik, istoriju porudžbina. Koristi se za autorizaciju upita i personalizaciju odgovora.

## 4. Arhitektonski zahtevi
- **Sigurnost i izolacija podataka** (nema curenja drugih kupaca).
- **Kompozicija odgovora** koji kombinuje retrieved tekst sa rezultatima eksternih servisa.
- **Ekstenzibilni orkestracioni sloj** (LlamaIndex ili LangChain) za brzo dodavanje novih toolova.
- **Ops posmatranje** – structured logging + tracing (OpenTelemetry).

## 5. Kandidat arhitekture
| Pristup | Opis | Prednosti | Mane | Kada ga birati |
| --- | --- | --- | --- | --- |
| **A. LlamaIndex Multi-Retriever + Tool Runner** | Koristiti LlamaIndex workflow: QueryEngine (hibridni retriever) + ToolExecutor za Order/Invoice API pozive. Graph bazirani workflows triggeruju follow-up pitanja (npr. broj porudžbine). | Native event-driven workflows, lako kombinovanje više izvora, dobra integracija sa Firecrawl čitačima. | Manje zajednice za production tooling, potrebno ručno upravljanje state-om korisnika. | Kada treba brzo integrisati više izvora u jedan orchestrator i koristiti LlamaIndex features (SubQuestionQueryEngine, QueryTransform). |
| **B. LangChain Agent sa funkcijama (OpenAI/Bedrock)** | Structured Chat Agent (ReAct) sa toolovima: `order_status_tool`, `policy_search_tool`, `invoice_lookup_tool`. Retrieval radi preko LangChain retriever protokola (FAISS/Qdrant). | Široka zajednica, mnogo plug-in konektora, lako koristiti OpenAI function calling ili Bedrock Agents. | Potencijalno skuplji token trošak zbog chain-of-thought, teža deterministička kontrola agenta. | Kada se želi fleksibilan agentic pristup sa bogatom ekosistemom i function-calling modelima. |
| **C. AWS-native (Bedrock + SageMaker Knowledge Bases)** | Koristiti Bedrock (Claude/LLM) za reasoning, a SageMaker za custom embeddings & hosting. Data ingestion kroz AWS Glue/S3, a operational APIs kroz Lambda tools. | Upravljanje podacima, compliance, integracija sa IAM i privatnim VPC-om. Država/enterprise compliant. | Viša cena i veća kompleksnost setup-a. Vendor lock-in, teža lokalna simulacija. | Kada je primarni zahtev compliance/enterprise ili već postoji AWS data lake. |

## 6. Poređenje LLM/hosting opcija
| Opcija | Snage | Slabosti | Preporučeni use-case |
| --- | --- | --- | --- |
| **OpenAI GPT-4o/4.1** | Najbolji kvalitet odgovora i function calling, odličan za složene politike i generisanje empatije. | SaaS, potrebno čuvati PII, token trošak. | Produkcioni chatbot uz stroge monitoringe i data redaction. |
| **Ollama (Mistral, Llama 3 lokalno)** | Lokalno izvršavanje, nema slanja podataka van okruženja, brzi PoC. | Potrebni GPU/CPU resursi, nešto slabiji reasoning, nema managed hosting. | Local PoC, offline režim, testiranje promptova. |
| **Bedrock (Claude/Command)** | Enterprise SLA, integracija sa AWS IAM, podrška za govorne/structured tool pozive. | Viša cena, regionalna dostupnost, vendor lock. | Kada postoji AWS strategija i potreba za usklađenošću. |
| **SageMaker + custom fine-tune** | Potpuna kontrola nad treniranjem i hostingom, mogućnost specifičnih stilova odgovora. | Potreban ML tim i ops, veći trošak. | Specijalizovani domeni, lokalizovani jezici, offline deployment. |

## 7. Preporučeni dodatni use-case
**„Bundle Recommendation + Stock Check“** – Kada kupac pita o dodatnoj opremi za postojeći uređaj, bot koristi embeddings da pronađe kompatibilne artikle, proverava `inventory_service` da li su na stanju i predlaže kupcu paket (npr. punjač + zaštita) uz napomenu o dostupnosti i ceni. Ovaj scenario povećava dodatnu prodaju i kombinuje policy + inventory podatke.

## 8. Proof-of-Concept (lokalno okruženje)
Najjednostavniji PoC u lokalnom okruženju:
1. **Orkestracija:** LlamaIndex QueryEngine + ToolExecutor.
2. **LLM:** Ollama (Mistral 7B) za lokalne eksperimente; omogućava rad bez eksternih servisa.
3. **Embeddings:** `nomic-embed-text` iz Ollama ili `sentence-transformers` (all-MiniLM). Vector store: Milvus Lite (docker servis `milvus-lite` na portu `19530`) kako bi se lokalno koristio isti API kao u produkciji.
4. **Knowledge ingestion:** lokalni folder `data/policies/*.md`. Upotrebi `SimpleDirectoryReader` + metadata.
5. **Order status stub:** lokalni JSON + FastAPI endpoint koji simulira 2 porudžbine.
6. **CLI prototip:** `uv run python -m app.cli.bot ask "Gde mi je porudžbina?"` – CLI pita za order ID pa poziva stub.
7. **Metrics:** logovanje svih tool poziva, ručno proveravanje tačnosti.

**Napomena o Milvus Lite-u:** Docker Compose sada sadrži servis `milvus-lite` (image `milvusdb/milvus-lite`) koji izlaže gRPC (`19530`) i HTTP (`9091`) portove i čuva podatke u lokalnom volume-u. Startuje se komandama `docker compose up -d milvus-lite` i `docker compose logs -f milvus-lite`. Ovo omogućava da lokalni PoC koristi isti Milvus API i schema lifecycle kao buduće produkciono okruženje.

Ovaj pristup omogućava da se iterate lokalno bez troškova, a kada su promptovi i tok pod pitanjima validirani, zameniti Ollama sa OpenAI/Bedrock modelom i prebaciti Milvus Lite na Milvus Standalone/Distributed (ili managed Milvus) bez promene koda.

## 9. Sledeći koraci
1. Potvrditi pravila klasifikacije i šta se sme vraćati kupcu (pravna, privacy).
2. Mapirati sva API-čka polja operativnih servisa i definisati adapter interface.
3. Implementirati ingestion pipeline sa automatskim tagovanjem dokumenta i testovima preciznosti.
4. Izgraditi PoC orchestrator (LlamaIndex + Ollama) prema gorenavedenom planu.
5. Nakon validacije, evaluirati koju produkcionu arhitekturu (A, B ili C) biramo i optimizovati TCO.

## 10. CLI pomoć i completion opcije

```
uv run python -m app.cli.main_cli --help
                                                
 Usage: python -m app.cli.main_cli [OPTIONS] COMMAND [ARGS]...
 CLI interfejs za customer assistant bota.
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                              │
│ --show-completion             Show completion for the current shell, to copy it or customize the     │
│                               installation.                                                          │
│ --help                        Show this message and exit.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────╮
│ ask   Postavlja pitanje botu i ispisuje stub odgovor.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

- **Struktura komande** – bazni `Typer` app je sada roditeljski komandni group, a `ask` je podkomanda koja prihvata pitanje i opciono `--order-id`. Svi novi CLI alati treba registrovati kao dodatne komande da bi help ostao konzistentan.
- **`--install-completion`** – Typer generiše skript za auto-complete (bash/zsh/fish). Ova opcija instalira skriptu za aktivnu shell sesiju (npr. `eval "$(uv run python -m app.cli.main_cli --install-completion bash)`), pa korisnik dobija tab-completion za komande i argumente.
- **`--show-completion`** – umesto automatske instalacije, ispiše generisanu skriptu za autocomplete na stdout (npr. `uv run python -m app.cli.main_cli --show-completion zsh`). Tipično se rezultat preusmeri u fajl ili direktno u `source` komandu kako bi se ručno dodao u `.zshrc`, `.bashrc` ili specifičan CI shell bez potrebe da Typer pokušava da upisuje u korisničke konfiguracije.

Ukratko, obavezno u dokumentaciji referencirati `uv run python -m app.cli.main_cli ask "Pitanje"` kada treba stub odgovor i naglasiti da completion flagovi olakšavaju rad developera dok iteriraju nad CLI komandama.

## 11. Korak-po-korak implementacija (trenutni fokus)

### Korak 1 – Generisanje internih dokumenata
- Kreiran je folder `data/policies/` sa pet markdown fajlova: `shipping-policy.md`, `returns-policy.md`, `warranty-playbook.md`, `authorized-service-locations.md`, `returns-howto.md`. Svaki dokument sadrži front-matter metapodatke (`region`, `document_version`, `last_reviewed`, `channel`) i sekcije koje pokrivaju SLA, eskalacije, servisne lokacije i korak-po-korak vodiče (fotografije, RMA, pickup checkpoints).
- Sažeci i mapiranje tema → tagova dodati su u `docs/policy-summaries.md`, čime QA i ops tim odmah vide šta je pokriveno (logistika, servisne adrese, proces reklamacije) i kako to mapira na personas/use-case scenarije iz poglavlja 2.
- Ingestion pipeline treba da mapira front-matter u tagove `jurisdikcija`, `kanal`, `tip_politike`, plus dodatne oznake za lokacije (`city`, `pickup_type`) i guidelines (`korak`, `instrukcija`) kako bi RAG retrieval mogao da pruži precizne odgovore (npr. "najbliži servis" ili "uputstvo za reklamaciju").

### Korak 2 – Mock servisi za stanje i statuse
- Napraviti `app/services/order_status_service.py` i `app/services/shipping_status_service.py` koji vraćaju statičke JSON-ove (2-3 porudžbine) i jasno označene statusne tranzicije (`PREPARING`, `SHIPPED`, `DELIVERED`).
- Izložiti te servise kroz Typer/FastAPI stubove (npr. `app/api/mock_order_api.py`) kako bi CLI `ask` komanda mogla da se poveže kad se implementira tool-calling. U response strukturu uključiti polja sa opisom na srpskom (`status: str  # kratki opis logističkog statusa`).
- Dodati unit testove koji pokrivaju „poznati order ID“ i „nepoznat order ID“ scenarije da bi se kasnije lako zamenilo mock implementacijama realnih konektora.

### Korak 3 – Sumarni plan naredna 2-3 koraka
1. **Povezati CLI sa mock servisima** – ažurirati `AssistantService.handle_query` da koristi nove stubove i da kroz `ask` komandu vraća kombinovani odgovor (tekst + statusna tabela).
2. **Automatizovati ingestion internih dokumenata** – napisati skriptu `uv run python -m app.ingest.policies` koja učitava markdown fajlove iz Koraka 1, taguje ih i puni Milvus Lite.
3. **Dodati observability hook-ove** – nakon što CLI koristi mock servise i ingestion pipeline, povezati `structlog`/OpenTelemetry tako da svako pitanje dobije trace ID i jasno logovane tool pozive (ključni zahtev iz poglavlja 4).
