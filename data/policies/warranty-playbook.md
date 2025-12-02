---
title: Warranty Resolution Playbook
region: EMEA
document_version: v0.9.4
last_reviewed: 2024-11-30
channel: support-center
---

# Warranty Resolution Playbook

## 1. Pokrivenost garancije
- Standardna garancija: 24 meseca za uređaje kupljene posredstvom ovlašćenih partnera.
- Proširena garancija: +12 meseci ako je kupac aktivirao plan u roku od 30 dana od kupovine.

## 2. Tipovi slučajeva
1. **DOA (Dead on Arrival)** – rešava se u roku od 48h, prioritetni ticket.
2. **Funkcionalni kvar** – bot prikuplja serijski broj i verziju firmware-a.
3. **Kozmetičko oštećenje** – potrebno dokazati transportnu štetu.

## 3. Koraci za bot asistenta
- Validacija serijskog broja kroz `inventory_service`.
- Provera statusa garancije (aktivna, istekla, suspendovana).
- Ako je garancija aktivna, ponuditi tri opcije: servisni centar, zamena, kredit za novu kupovinu.

## 4. Matrica eskalacije
| Prioritet | SLA odgovor | Eskalacija |
| --- | --- | --- |
| P1 (bez funkcije) | 2h | L3 inženjer + SMS obaveštenje kupcu |
| P2 (degradacija) | 1 radni dan | L2 tim |
| P3 (kosmetika) | 3 radna dana | lokalni servis |

## 5. Dokumentacija
- Bot mora da sačuva zapisnik (transkript) i priložene dokaze u CRM tiket.
- Sve zamene moraju proći kroz "Warranty Compliance" checklistu.

