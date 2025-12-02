# Policy Summaries

| Dokument | Opis | Ključne teme | Tagovi |
| --- | --- | --- | --- |
| `data/policies/shipping-policy.md` | Definiše standardne shipping SLA-ove i statusne kodove (PREPARING, SHIPPED, DELIVERED, EXCEPTION). | logistika, ETA, kuriri, eskalacija | region: EU/US, channel: ecommerce |
| `data/policies/returns-policy.md` | Pokriva pravila za povraćaje, RMA proces i refund opcije uključujući store kredit. | returns, refund, RMA, QC | region: global, channel: ecommerce+retail |
| `data/policies/warranty-playbook.md` | Detaljan playbook za garancijske slučajeve (DOA, funkcionalni kvar, kozmetičko oštećenje) i eskalacione matrice. | warranty, servis, eskalacija, SLA | region: EMEA, channel: support-center |
| `data/policies/authorized-service-locations.md` | Lista ovlašćenih servisnih centara i pickup checkpoint-a (locker mreža, retail partneri, mobilni kuriri) sa pravilima zakazivanja. | lokacije, pickup, servis, logistika | region: EMEA+NA, channel: service-network |
| `data/policies/returns-howto.md` | Korak-po-korak vodič za kupce kako da pokrenu reklamaciju/RMA (fotografije, formular, logistika, refund). | returns-guide, RMA, instrukcije | region: global, channel: customer-support |

Svaki dokument sadrži front-matter metapodatke (`region`, `document_version`, `last_reviewed`, `channel`) koje ingestion pipeline treba da mapira na tagove `jurisdikcija`, `kanal`, `tip_politike`.
