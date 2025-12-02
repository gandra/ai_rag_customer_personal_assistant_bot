---
title: Authorized Service & Pickup Locations
region: EMEA + North America
document_version: v1.0.0
last_reviewed: 2025-03-01
channel: service-network
---

# Authorized Service & Pickup Locations

## 1. Ovlašćeni servisi
| Grad | Adresa | Radno vreme | Napomena |
| --- | --- | --- | --- |
| Beograd | Bulevar Zorana Đinđića 44 | Pon-Pet 09-18 | Prima DOA i funkcionalne kvarove |
| Novi Sad | Futoška 19 | Pon-Sub 10-16 | Fokus na kozmetičke popravke |
| Zagreb | Avenija Dubrovnik 15 | Pon-Pet 08-17 | Regionalni hub za HR i SLO |
| Berlin | Invalidenstraße 116 | Pon-Pet 09-18 | Specijalizovani tim za industrijske uređaje |
| New York | 5th Ave 350 | Pon-Sub 09-17 | North America flagship centar |

## 2. Pickup checkpoints
- **Locker mreža** – saradnja sa InPost (EU) i UPS Access Point (US). Kupci dobijaju QR kod za preuzimanje/ostavljanje paketa.
- **Retail partneri** – odabrane prodavnice (MediaMarkt, BestBuy) imaju "Drop-off" pult.
- **Mobilni kurir** – u većim gradovima (Beograd, Berlin, NYC) moguće je zakazati preuzimanje na kućnoj adresi u terminu 4h.

## 3. Pravila zakazivanja
- Bot mora da prikupi poštanski broj kako bi filtrirao najbliže lokacije.
- Ako nema ovlašćenog servisa u krugu 100km, bot nudi besplatan kurirski pickup.
- Lokacije imaju ograničen broj slotova; sistem potvrđuje termin tek nakon sinhronizacije sa centralnim kalendarom.

## 4. Komunikacioni template
- "Najbliži ovlašćeni servis je **{location_name}**, adresa **{address}**. Radimo {working_hours}."
- Ako je izabrana locker mreža, navesti instrukcije za QR kod i rok (72h) za ostavljanje paketa.

