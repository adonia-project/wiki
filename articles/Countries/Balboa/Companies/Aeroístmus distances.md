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
| Castejón | Balisca | -57.3787, 31.0798 | 5,154 km | 6h 30min |
| Hargiesa | Galwa | -27.6078, -11.4083 | 7,504 km | 9h |
| Kankadadka | Burawa | -15.3774, -17.2316 | 8,872 km | 11h |
| Miyagami | Nakamizu | 140.3520, -27.5510 | 13,480 km | 16h |
| Okami | Okaiken | 132.6175, -15.8769 | 14,605 km | 17h |

## Unmatched destinations (not on any map layer)

### International
- Sanu-Sasso (Asikyira)
- Nanaimo (Kaneda)
- Kanakou (Kaneda)
- Kuluba (Asikyira)
- Iskhal (Burawa) — Kankadadka is on the map but Iskhal is a different city
- Auxin (Daras) — no Daras city on the map (Luanjing dropped from network)
- Sanropura (Abyala)
- Aoyama (Okaiken) — Okami is on the map but Aoyama is a different city

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
