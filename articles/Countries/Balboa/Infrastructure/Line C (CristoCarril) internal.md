# Line C (CristoCarril) — Internal Notes

## Overview
- Third CristoCarril line, runs on the **Varakí Line** corridor
- 26 stations, 65.7 km total length
- Runs from Sant Cristòfor Central Terminal to Varakí Centra
- Serves two comarcas: Sant Cristòfor and Cumará
- Shares tracks with Rodalies de Portnou Line 4 (RdP L4) on the outer section

## Station Data (from GIS)
- Source: `/Users/shubhamnaik/Developer/adonia-gis/Points of Interest.shp`
- 26 stations total (including Varakí HSR which had name=None in shapefile)
- Distances calculated using haversine formula between consecutive POI coordinates
- Total: 65.71 km

## Corridor Name
- Used "Varakí Line" as the corridor name (line terminates at Varakí)
- Line A uses "Coastal Line", Line B uses "Portnou Line"
- GIS route field at Varakí HSR shows: "Sant Cristofor-Portnou Line, CC Line C, Sant Cristofor-Areza Line, RdP L4"
- The "Sant Cristòfor–Portnou Line" and "Sant Cristòfor–Areza Line" are intercity rail corridors passing through Varakí HSR
- These are NOT the same as the CristoCarril corridor names

## Station Name Corrections Applied
- Placa → Plaça (Plaça de la Catedral, Plaça Mario)
- Marti → Martí (Carretera de Martí)
- Unio → Unió (Unió Cr)
- Divisio → Divisió (Divisió Cr)
- Turo → Turó (Turó Vermell)
- Varaki → Varakí (Varakí Centra, Varakí HSR)
- Facil → Fàcil (Torre Fàcil)
- Cruilla → Cruïlla (in station name Autopista 68/La Cruïlla)

## Varakí HSR (Station 25)
- Name shows as None in shapefile despite user editing in QGIS
- Route field was saved: "Sant Cristofor-Portnou Line, CC Line C, Sant Cristofor-Areza Line, RdP L4"
- User confirmed the name is "Varakí HSR"
- Major interchange station connecting to intercity rail corridors
- Also served by RdP L4

## Invented Data
- Daily ridership: 71,400 (2025) — estimated based on Line A (62,990) and Line B patterns
- Daily boardings per station — estimated based on station type and location
- Travel times — estimated based on distance and average speed
- Service patterns (Short/Express/Local) — modeled after Line A
- Fare zones (3 zones) — based on comarca boundaries
- Schedule frequencies — modeled after Line A

## Service Patterns
- Short: Stations 1–18 (Sant Cristòfor Central Terminal to Torrepolis), ~42 min
- Express: 1, 2, 5, 10, 18, 25, 26 (key stops only), ~60 min
- Local: All 26 stations, ~77 min

## Shared Stations with Other Lines
- Stations 1–4 (Central Terminal to La Font): Shared with Line B
- Station 25 (Varakí HSR): Shared with Sant Cristòfor–Portnou Line, Sant Cristòfor–Areza Line, RdP L4
- Station 26 (Varakí Centra): Shared with RdP L4

## Open Questions
1. Confirm "Varakí Line" is the correct corridor name
2. Varakí HSR name needs to be saved in QGIS shapefile (currently None)
3. Verify daily ridership and boarding numbers
4. Verify fare zone boundaries
5. Verify service pattern stops for Express
