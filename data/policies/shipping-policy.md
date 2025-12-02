---
title: Standard Shipping Policy
region: EU & US
document_version: v1.2.0
last_reviewed: 2025-01-12
channel: ecommerce
---

# Standard Shipping Policy

## 1. Opseg
Politika se odnosi na sve online porudžbine završene putem portala ili mobilne aplikacije. Kupci dobijaju broj za praćenje i predviđeni datum isporuke (ETA) nakon otpremanja pošiljke.

## 2. SLA vremena
- **Processing**: 0–2 radna dana nakon potvrde plaćanja.
- **In Transit**: EU 2–4 dana putem DPD; SAD 3–5 dana putem UPS.
- **Delayed status**: Ako kurir prijavi izuzetak >48h, automatski otvaramo ticket i nudimo kupcu vaučer.

## 3. Statusne oznake
| Status | Opis | Akcija koju vidi bot |
| --- | --- | --- |
| PREPARING | Porudžbina se pakuje | traži da kupac proveri adresu |
| SHIPPED | Paket preuzet od kurira | prikazuje ETA i link za praćenje |
| DELIVERED | Kurir potvrdio isporuku | pita kupca da li je sve u redu |
| EXCEPTION | Kurir javio problem | pokreće refund lookup |

## 4. Politika eskalacije
- Ako `EXCEPTION` traje duže od 2 dana, logistika šalje zamenski paket.
- Nakon 7 dana bez isporuke, kupcu se vraća novac osim ako je proizvod custom.

## 5. Komunikacija prema kupcu
- Ton komunikacije treba da sadrži empatiju i praktične korake.
- Svaka poruka uključuje broj narudžbine i link ka "Praćenje pošiljke" stranici.

