# Aeroístmus — Route Distances

Distances calculated from great-circle measurement using coordinates from the "Cities in Adonia" and "Points of Interest" map layers.

**Sant Cristòfor reference point:** -94.4028°, 0.6419° (Sant Cristòfor Main, from POI shapefile)

## Domestic destinations (from POI shapefile — airport coordinates)

| City | Airport | Coordinates (lon, lat) | Distance from SCI | Est. flight time |
|------|---------|----------------------|-------------------|-----------------|
| Sant Cristòfor | Sant Cristòfor Main | -94.4028, 0.6419 | — | — |
| Illes del Guano | Illes del Guano Airport | -93.1608, 0.6492 | 138 km | 20 min |
| Portnou | Portnou Airport | -94.4429, -0.0364 | 75 km | 15 min |
| Haicang | Haicang International Airport | -93.4348, 1.2607 | 128 km | 20 min |
| Sant Agneu | Marie Torres Airport | -92.3730, -2.1265 | 380 km | 45 min |
| Campdària | Amelio Perez Airport | -93.8342, 0.1041 | 87 km | 15 min |
| Altaneu | Altaneu Airport | -92.8299, 2.1582 | 242 km | 30 min |
| Costabella | Costabella Airport | -92.0262, 2.1000 | 310 km | 35 min |
| Sant Bart | Sant Bart Airport | -92.3318, 2.6032 | 316 km | 35 min |
| Badia Curta | Badia Curta Airport | -93.3348, 4.2048 | 411 km | 45 min |
| Novara | Novara Airport | -91.4093, 4.3246 | 526 km | 1h |
| Vellmar | Vellmar Airport | -91.1709, 5.0854 | 609 km | 1h 10min |
| Portblanc | Portblanc Airport | -94.1292, 6.5745 | 657 km | 1h 15min |

## International destinations (from Cities in Adonia shapefile)

| City | Country | Coordinates (lon, lat) | Distance from SCI | Est. flight time |
|------|---------|----------------------|-------------------|-----------------|
| Tamsui | Sinchew | -94.6198, -3.8485 | 497 km | 45 min |
| Gran Port de Sant Mateu | Tapuya | -75.2993, 7.8045 | 2,262 km | 3h |
| Port Soledat | Potocsí | -83.7870, 23.2130 | 2,748 km | 3h 30min |
| Guledga | Lacashe | -66.0970, 8.9142 | 3,268 km | 4h |
| Sanu-Sasso | Lacashe | TBD | ~3,568 km | 4h 30min |
| Castejón | Balisca | -57.3787, 31.0798 | 5,154 km | 6h 30min |
| Hargiesa | Galwa | -27.6078, -11.4083 | 7,504 km | 9h |
| Ampuria | Volisania | -13.0953, -23.6478 | 9,152 km | 11h |
| Kankadadka | Burawa | -15.3774, -17.2316 | 8,872 km | 11h |
| Aoyama-Maekawa | Nakamizu | 174.7178, -34.9242 | 10,129 km | 12h |
| Mariapolis | Sarta | 2.7303, -31.4995 | 10,729 km | 13h |
| Okami | Okaiken | 158.2631, -16.6647 | 11,873 km | 14h |

## SBT-based distances

| City | Country | Distance from SBT | Est. flight time |
|------|---------|-------------------|-----------------|
| Port Soledat | Potocsí | 2,470 km | 2h 54min |

Note: SBT (Sant Bart) coordinates from POI shapefile: -92.3318, 2.6032

## Sanrobonian destinations (user-provided airport coordinates)

Distances in this table use airport coordinates provided for the Sanrobonian network rather than city centroids. Coordinates are shown in longitude-latitude order.

| City / market | Airport | Coordinates (lon, lat) | Distance from SCI | Est. flight time | Planned Aeroístmus service |
|---------------|---------|----------------------|-------------------|-----------------|----------------------------|
| Pinangsiang | Pinangsiang International Airport | -102.6270, 13.4097 | 1,684 km | 2h | 2 daily from SCI; A321 |
| Sungaipura | Abdul Karim International Airport | -105.0108, 12.5577 | 1,767 km | 2h 10min | 2 daily from SCI; A321 |
| Karanu | Anacaona International Airport | -108.5359, 22.0120 | 2,827 km | 3h 20min | Daily from SCI; A321 |
| Tanjung Seroja | Tanjung Seroja International Airport | -113.4988, 23.4406 | 3,267 km | 4h | 4 daily from SCI; three A321 rotations and one peak A330 rotation |
| Tanjung Seroja / Martapura | Pasirmajang Gateway Airport | -113.2895, 23.3081 | 3,242 km | 4h | Daily from SCI; A321 |
| Sanropura | Iskandar Setiadji International Airport | -111.2176, 25.2310 | 3,277 km | 4h | 2 daily from SCI and MWF from Sant Bart; A321 |
| Kutawaringin | Marowa Sangaji International Airport | -122.5829, 19.0907 | 3,694 km | 4h 30min | Daily from SCI; A321 |
| Sayara-Tanjung Emasan | Sayamas International Airport | -115.6256, 33.8954 | 4,308 km | 5h 10min | Daily from SCI; A321 |

### Secondary Balboan origin routes

| Origin | Destination | Airport | Distance | Est. flight time | Planned service |
|--------|-------------|---------|----------|-----------------|-----------------|
| Sant Bart | Sanropura | Iskandar Setiadji International Airport | 3,228 km | 4h | Monday, Wednesday, Friday; A321 |
| Badia Curta | Tanjung Seroja | Tanjung Seroja International Airport | 3,043 km | 3h 40min | Daily; business-heavy A321neo |

### Sanrobonia scheduling concept

The network creates 108 weekly Aeroístmus departures to Sanrobonia: 98 weekly departures from Sant Cristòfor, 3 weekly departures from Sant Bart, and 7 weekly departures from Badia Curta. The Tanjung Seroja financial-hub services use premium-heavy A321neo and A330 aircraft; other Sanrobonian services use narrowbody aircraft. Tanjung Seroja operates as a higher-yield business route with four daily frequencies from Sant Cristòfor, three operated by A321neo aircraft and one peak rotation operated by an A330 with a premium-heavy configuration.

| Route | Frequency | Aircraft | Weekly departures | Notes |
|-------|-----------|----------|-------------------|-------|
| SCI-Tanjung Seroja | 4 daily | 3× A321neo, 1× A330 peak rotation | 28 | Primary financial-hub route; premium-heavy cabins |
| SCI-Sanropura | 2 daily | A321 | 14 | Capital route |
| SBT-Sanropura | Monday, Wednesday, Friday | A321 | 3 | Secondary Jala highland connection |
| BDC-Tanjung Seroja | Daily | A321neo | 7 | Industrial and financial business route from Badia Curta |
| SCI-Pasirmajang / Martapura | Daily | A321 | 7 | Secondary Tanjung Seroja-Martapura airport |
| SCI-Kutawaringin | Daily | A321 | 7 | Longer western Sanrobonian route |
| SCI-Sayara-Tanjung Emasan | Daily | A321 | 7 | Longest A321 sector in the Sanrobonian network |
| SCI-Karanu | Daily | A321 | 7 | Mid-range Sanrobonian route |
| SCI-Sungaipura | 2 daily | A321 | 14 | Shorter high-frequency regional route |
| SCI-Pinangsiang | 2 daily | A321 | 14 | Shorter high-frequency regional route |

### Tanjung Seroja business schedule concept

| Direction | Departure | Arrival | Aircraft | Market purpose |
|-----------|-----------|---------|----------|----------------|
| Tanjung Seroja → SCI | 06:30 | 12:00 | A321neo | Sanrobonia-origin same-day business travel to Sant Cristòfor |
| SCI → Tanjung Seroja | 07:00 | 10:35 | A330 | Balboa-origin morning business travel to Tanjung Seroja |
| SCI → Tanjung Seroja | 11:00 | 14:35 | A321neo | Midday departure and connection bank |
| Tanjung Seroja → SCI | 12:30 | 18:00 | A321neo | Midday return and late-afternoon arrival in Sant Cristòfor |
| SCI → Tanjung Seroja | 15:00 | 18:35 | A321neo | Afternoon business and leisure departure |
| Tanjung Seroja → SCI | 15:30 | 21:00 | A321neo | Afternoon return |
| Tanjung Seroja → SCI | 18:00 | 23:30 | A330 | Peak evening return from Tanjung Seroja |
| SCI → Tanjung Seroja | 21:30 | 01:05+1 | A321neo | Late departure / overnight-positioning option |

## Unmatched destinations (not on any map layer)

### International
- Sanu-Sasso (Asikyira)
- Nanaimo (Kaneda)
- Kanakou (Kaneda)
- Kuluba (Asikyira)
- Iskhal (Burawa) — 9,243 km from SCI (user-provided, not from map)
- Auxin (Daras) — no Daras city on the map (Luanjing dropped from network)
- Aoyama (Nakamizu) — now served via Aoyama-Maekawa International Airport (coordinates: 174.7178, -34.9242)
- Miyagami (Nakamizu) — dropped from network, replaced by Aoyama-Maekawa (closer to SCI, shorter flight time)
- Akyatan (Dagit) — served via codeshare with Sanesair (Okami→Akyatan, 1,696 km, 2h on 787-9). Coordinates: 146.6897, -6.4417

## Other airports on POI layer (not Aeroístmus destinations)

| Airport | Coordinates (lon, lat) | Distance from SCI |
|---------|----------------------|-------------------|
| Illa Daurada Airport | -94.5223, 0.9571 | 37 km |
| L'Estany Airport | -94.1045, 0.8872 | 43 km |
| Santa Caterina Airport | -93.8495, -1.0215 | 194 km |
| Platja d'Aro Airport | -92.5532, -0.4705 | 240 km |
| Foia Gran Airport | -91.5624, 5.1818 | 593 km |
| Sant Jorge Airport | -92.3285, 8.0236 | 848 km |

## Notes

- Distances are great-circle (orthodrome) distances, not actual flight path distances. Actual routes may be longer due to air traffic control routing.
- Flight times estimated at ~850 km/h cruise speed; actual block times will be longer due to taxi, climb, descent, and routing.
- Domestic airport coordinates from Points of Interest shapefile (EPSG:4326).
- International city coordinates from Cities in Adonia shapefile (EPSG:3857, converted to EPSG:4326).
