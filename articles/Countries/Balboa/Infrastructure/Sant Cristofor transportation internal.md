# Sant Cristòfor Transportation — Internal Design Document

## Overview

Sant Cristòfor is the transport hub of the Isthmus of Balboa, with a multimodal network serving 5.16 million residents across 11 ciutats. The system is managed by the [[Autoritat de Transport de Sant Cristòfor]] (ATS), created in 1964 to merge the city's three private streetcar companies into a unified public transport authority. The ATS now oversees metro, streetcar, bus, and ferry operations; commuter rail and air are managed separately.

| Mode | Daily ridership | Operator | Notes |
|------|----------------|----------|-------|
| Metro | 2,100,000 | Metro de Sant Cristòfor (ATS) | 9 lines, backbone |
| Streetcar | 250,000 | Tramvia de Sant Cristòfor (ATS) | 13 lines (4 Original, 7 Barcelona, 2 Costa Nord) |
| Bus | 760,000 | Autobusos de Sant Cristòfor (ATS) | Full network coverage |
| Ferry | 118,500 | Ferries de la Badia (ATS) | 8 routes, bay crossings |
| Commuter rail | 350,000 | Ferrocarrils de l'Istme (national) | 3 terminals, suburban comarcas |
| Regional rail | TBD | Ferrocarrils de l'Istme (national) | All provinces, 3 terminals |
| High-speed rail | TBD | Ferrocarrils de l'Istme (national) | Portnou, Areza (Intercon halted) |
| **Total** | **3,578,500** | | |

## 1. Metro

{{main|Metro de Sant Cristòfor}}

### Network topology
The metro is NOT a simple radial system. Only Lines 1 and 2 originate from Grand Train Terminal. The remaining lines have varied configurations — cross-city routes, peninsula routes, an outer ring, and a regional connector. Original is the network hub (7 of 9 lines converge there); Dàrsena is the second hub (6 lines).

### Line details
- **Line 1** (31.6 km): Sant Jordi → Original → Sant Martí → Sant Miquel. Radial from Grand Train Terminal eastward. Extended to airport 1986. ~107,300 daily.
- **Line 2** (37.8 km): Sant Martí → Original → Ciutat de l'Estació → Dàrsena. Radial from Grand Train Terminal northeastward. ~152,900 daily.
- **Line 3** (33.3 km): Costa Nord → Original → Dàrsena/Sant Llorenç. North-south connector, completed from GAW-halted tunnels (1964). First direct north-south metro link. ~daily TBD.
- **Line 4** (26.8 km): Dàrsena → Original → Mare de Déu del Mar. East-west cross-city. ~86,700 daily.
- **Line 5** (42.8 km): Original → Barcelona → Costa Nord → Dàrsena. First rail link to the peninsula. Goes around the northern bay shore (NOT a tunnel). **Busiest line** at ~257,600 daily.
- **Line 6** (26.8 km): Dàrsena → Original → Barcelona → Sant Miquel. Also goes around the bay to Barcelona. ~156,000 daily.
- **Line 7** (53.4 km): Original → Sant Llorenç → Sant Miquel → Dàrsena → Ciutat de l'Estació. Long cross-city route. ~168,200 daily.
- **Line 8** (48.2 km): Ciutat de l'Estació → Sant Martí → Sant Llorenç → Sant Jordi → Sant Miquel → Dàrsena. **Outer ring — does NOT serve Original.** ~123,300 daily.
- **Line 9** (51.2 km): Sant Martí → Ciutat de l'Estació → Cumará → Areza. Regional connector to Areza Metro and airport. ~47,900 daily.

### Ciutat coverage
- **Original**: Lines 1, 2, 3, 4, 5, 6, 7 (hub)
- **Dàrsena**: Lines 2, 4, 5, 6, 7, 8 (second hub)
- **Sant Martí**: Lines 1, 2, 8, 9
- **Barcelona**: Lines 5, 6 (plus ferry)
- **Costa Nord**: Lines 3, 5
- **Sant Llorenç**: Lines 3, 7, 8
- **Sant Jordi**: Lines 1, 8
- **Sant Miquel**: Lines 1, 6, 7, 8
- **Ciutat de l'Estació**: Lines 2, 7, 8, 9
- **Mare de Déu del Mar**: Line 4 only
- **Ciutat del Pujol**: No metro (elite, car-dependent)

### Key constraint
No metro crossing of the Badia de Sant Cristòfor. Peninsula residents must use ferry or overland routes via Lines 5 and 6. Proposed cross-bay tunnel (Line 1 extension under bay to Barcelona) approved by referendum 2025 but faces opposition from dockworkers' union and Maritime Workers' Party.

### Ridership
~2.1M daily (2025). Line 5 is the busiest (peninsula overland route).

## 2. Streetcar

The streetcar system has 13 lines across three ciutats, each network with a distinct character. The original private tramways were absorbed into the metro system in 1964 (Sant Cristòfor Tramway Company, Costa Nord Light Railway, Pandao Tram Company), but the streetcar lines were retained and upgraded rather than closed. Total daily ridership: ~250,000.

### Original — 4 lines (LRV)
Four lines radiating from Grand Train Terminal along the main boulevards, spining outward through the historic core. All upgraded to modern LRVs in the 2000s. Connect the major transport hubs (Grand Train Terminal, ferry terminal, financial district) through the narrow streets of the historic core where metro stations are too far apart. High frequency (4 min peak on all lines).

- **T1**: Grand Train Terminal → bay shore → financial district → Carrer del Canal → southern neighbourhoods
- **T2**: Grand Train Terminal → eastern boulevard → Dàrsena border
- **T3**: Grand Train Terminal → northern boulevard → Costa Nord border
- **T4**: Grand Train Terminal → western boulevard → Sant Jordi border

**Role**: The four Original lines are the spine of the city centre's surface transport. They serve the financial sector lunch rush, the cafeteria halls, and the dense residential neighbourhoods. T1 connects directly to the ferry terminal at Sant Cristòfor Main, making it the primary last-mile connection for ferry passengers heading into the city centre. ~95,000 daily combined.

### Barcelona — 7 lines (LRV)
Seven lines following the peninsula's grid pattern — 4 east-west, 3 north-south. All upgraded to modern LRVs in the 2010s. The Barcelona network is critical infrastructure: with no metro crossing of the bay, the streetcar grid provides the primary internal circulation for the peninsula's 732,000 residents. High frequency (5 min peak on spine lines, 8 min on secondary).

East-west lines:
- **T5**: Platja de Jordi → Barcelona centre → eastern Barcelona
- **T6**: Southern Barcelona → Barcelona centre → Pandao neighbourhoods
- **T7**: El Fort → Barcelona centre → central Barcelona
- **T8**: Western Barcelona → Barcelona centre → eastern Barcelona

North-south lines:
- **T9**: Pandao ferry terminal → Barcelona centre → El Fort ferry terminal (north-south spine)
- **T10**: Northern Barcelona → Barcelona centre → southern Barcelona
- **T11**: Southern Barcelona waterfront → Barcelona centre → northern Barcelona waterfront

**Role**: The Barcelona grid is the peninsula's lifeline. T9 (north-south spine connecting the two major ferry terminals) carries the highest ridership of any streetcar line. Without the grid, Barcelona's residents would rely entirely on buses for internal circulation. The LRV upgrade was prioritised because of the network's importance to peninsula commuters. ~110,000 daily combined.

### Costa Nord — 2 lines (mixed historic + LRV)
Two lines with mixed fleet operation, reflecting Costa Nord's dual identity as a working media district and a tourist destination.

- **T12**: Costa Nord ferry building → grand boulevard → waterfront (LRV + heritage). The LRV section provides commuter service along the grand boulevard from the ferry building; the heritage section retains original Shining Star era trams as a tourist/cultural attraction along the waterfront promenade.
- **T13**: Waterfront → inland → main studio district (LRV). Provides genuine commuter service for the media industry workforce, connecting studios, production houses, and post-production facilities to the waterfront and ferry connection.

**Role**: T12 serves a dual purpose — commuter service on the grand boulevard and heritage tourist experience on the waterfront. T13 is purely functional, connecting the media workforce to the transport network. ~45,000 daily combined (35K LRV, 10K heritage).

## 3. Bus

### Design Principles
1. Cross-town connections between radial metro lines
2. Coverage of low-density outer ciutats where metro doesn't reach
3. Feeder service to metro and streetcar terminals
4. Night service when metro and streetcar close
5. Industrial area and airport connections

### Ciutat Analysis

#### High-density urban core (metro + streetcar + bus feeders)
- **Original** (731K, 8,811/km²) — Metro (7 lines) + 4 streetcar lines primary. Bus: cross-town between boulevards, feeders to metro stations, financial district. ~120K daily.
- **Barcelona** (732K, 10,605/km²) — Ferry + 7 streetcar lines primary (grid coverage). Bus: supplements streetcar grid in less-served areas, night service. ~80K daily.
- **Dàrsena** (575K, 3,803/km²) — Metro (6 lines) east-west. Bus: north-south, nightlife (late night). ~90K daily.

#### Medium-density urban (metro + bus primary)
- **Costa Nord** (580K, 3,742/km²) — Metro (2 lines) + 2 streetcar lines. Bus: interior routes, studio connections, north-south. ~70K daily.
- **Sant Llorenç** (540K, 3,777/km²) — Metro (3 lines) main corridors. Bus: industrial, residential feeders. ~70K daily.
- **Sant Jordi** (461K, 2,214/km²) — Metro (2 lines) centre. Bus: residential, cross-town. ~55K daily.

#### Low-density suburban (bus primary, limited metro)
- **Sant Martí** (435K, 1,204/km²) — Metro L1+L9 airport corridor. Bus: rest of ciutat. ~65K daily.
- **Ciutat de l'Estació** (376K, 1,205/km²) — Metro main corridor. Bus: residential, railyard. ~45K daily.
- **Mare de Déu del Mar** (232K, 915/km²) — Limited metro. Bus primary: coastal, beach. ~35K daily.
- **Sant Miquel** (230K, 800/km²) — No metro. Bus primary: hill routes. ~25K daily.
- **Ciutat del Pujol** (266K, 506/km²) — No metro. Bus primary: limited routes. ~20K daily.

### Route Categories
1. **Trunk** — high-frequency cross-town corridors, peninsula cross-connections, airport express
2. **Standard** — residential coverage, metro feeders, industrial areas
3. **Night** — Dàrsena nightlife circuit, Sòtol connections, weekend beach
4. **Hill** — Sant Miquel, Ciutat del Pujol (smaller vehicles, limited frequency)

## 4. Ferry

{{main|Ferries de la Badia de Sant Cristòfor}}

### Network
8 routes from 7 terminals, hub-and-spoke from Sant Cristòfor Main. ~118,500 daily (2025).

| Route | From → To | Distance | Frequency (peak) | Daily ridership | Notes |
|-------|-----------|----------|-----------------|-----------------|-------|
| 1 | Main → Pandao | 6.4 km | 5 min | 68,700 | Primary commuter crossing, no bridge/metro |
| 2 | Main → Illa del Portal | 16.3 km | 90 min | 2,300 | Nature reserve access |
| 3 | Main → Daurada | 30.6 km | Hourly | 8,200 | Island service, residents + tourists |
| 4 | Main → Costa Nord | 20.6 km | Rush hour only | 3,100 | Commuter, limited |
| 5 | Main → Parc Nacional | 46.6 km | 2–3 hrs | 1,900 | Recreational, weekends/holidays |
| 6 | Main → Platja de Jordi | 6.7 km | 10 min | 15,800 | Southern Barcelona peninsula |
| 7 | Main → El Fort | 8.6 km | 10 min | 12,400 | Northern Barcelona peninsula |
| O | Circular (Main→Platja→Pandao→El Fort→Main) | 24.5 km | 30 min | 7,000 | Cross-peninsula |

### Key facts
- Route 1 carries 58% of all ferry ridership — only direct link between peninsula and city centre
- 4 Barcelona peninsula routes (1, 6, 7, O) = 88% of total ridership
- Fares integrated with metro under Tarifa Integrada (90-min free transfers)
- Fleet: 25 vessels across 7 classes (Badia-class double-ended catamarans for Route 1)
- ~160 employees

### Cross-bay tunnel controversy
Proposed Line 1 extension under the bay to Barcelona (~7 km tunnel). Approved by referendum 2025 but opposed by dockworkers' union and Maritime Workers' Party (PTM), who argue it would eliminate ferry jobs. Protests have drawn thousands. Remains in planning stage.

## 5. Rail

Sant Cristòfor is the rail hub of Balboa — the major terminus for all rail in the country, with services connecting to every province. The rail network operates at three tiers: commuter, regional, and high-speed. There are three major terminals.

### Terminals

- **Grand Train Terminal** — the primary hub, located in Original. Serves commuter rail, regional rail, and high-speed rail. The busiest station in the country.
- **Costa Nord terminal** — serves regional rail services heading north along the Shendan coast and into the northern provinces.
- **Barcelona terminal** — serves commuter rail (Barcelona → Mare de Déu del Mar → Cumará) and a regional line to Portnou. Provides the peninsula with direct rail access without requiring a cross-bay journey.

### Commuter rail
Suburban services connecting Sant Cristòfor to the surrounding comarcas of Estret Province. ~350,000 daily (2025).
- From Grand Train Terminal: services to suburban towns and the canal corridor
- From Barcelona terminal: commuter service through Mare de Déu del Mar to Cumará

### Regional rail
Conventional-speed intercity rail connecting Sant Cristòfor to every province in Balboa. The city is the country's major rail terminus — all major national routes converge here.
- From Grand Train Terminal: services to all provinces
- From Costa Nord terminal: services heading north along the Shendan coast and into the northern provinces
- From Barcelona terminal: regional line to Portnou

### High-speed rail
HSR services on dedicated high-speed lines:
- **Sant Cristòfor → Portnou**: operational HSR line along the canal corridor
- **Sant Cristòfor → Areza**: operational HSR line, connecting to the International City of Areza
- **Sant Cristòfor → Sant Bart**: the Intercon project was building HSR to the interior capital, but construction was halted due to budget shortfalls. Traditional rail remains the only connection to Sant Bart.

## 6. Air

### Sant Cristòfor International Airport
- Location: Sant Martí ciutat
- Opened: 1985 (replacing former airport at Ciutat de l'Estació)
- Metro connections: Lines 1 and 9
- Bus connection: Airport express trunk route
- Status: Busiest airport in Balboa
- Routes: Domestic and international (Abyala, Fosia, Illypnia)

### Former airport
- Ciutat de l'Estació airport (1954–2003), redesignated Areza International Airport until closure

## 7. Roads

### Major highways
- **Eastern Highway** — elevated expressway through Original, built during AC mandate (Mayor Crespo, 1956–1960). Most criticised element of the rebuild. Runs east-west through the city.
- **Coastal highway prohibition** — ban on coastal highway along Shendan Ocean coast, imposed during AC mandate, remains in force. Preserves coastal character of Costa Nord and Mare de Déu del Mar.
- **Canal corridor road** — connects to Portnou and Areza along the Balboa Canal

### Urban roads
- Boulevard system — created during AC rebuild, wide boulevards connecting ciutats
- "Mini city" concept — Sant Cristòfor Central's pedestrian-oriented neighbourhoods
- Original's narrow historic streets — not suited to heavy vehicle traffic, streetcar (T1) preferred

### Key constraint
No road bridge across the Badia de Sant Cristòfor. All cross-bay travel is by ferry. The absence of a bridge is a deliberate policy — proposals have been rejected on environmental, aesthetic, and urban-planning grounds, and the ferry lobby has successfully opposed bridge construction for decades.

## 8. Cycling

Cycling infrastructure is limited but growing, concentrated in:
- Original's flat bay shore and boulevard system
- Costa Nord's waterfront promenade
- Dàrsena's warehouse district (wide, flat streets)
- Barcelona's peninsula (flat, but constrained by streetcar tracks)

Cycling is impractical in the hill ciutats (Sant Miquel, Ciutat del Pujol) and limited in the industrial areas (Sant Llorenç). The city has no bike-share programme as of 2026, though proposals have been discussed.

## 9. Fare Integration

All ATS services (metro, streetcar, bus, ferry) operate under the **Tarifa Integrada** — a unified fare system allowing free transfers between modes within a 90-minute window. The system is zoned, with Zone 1 covering the core ciutats (Original, Barcelona, Dàrsena, Costa Nord) and outer zones extending to the suburban ciutats.

Commuter rail and air are not integrated into the Tarifa Integrada.

## 10. Governance

- **Autoritat de Transport de Sant Cristòfor (ATS)** — created 1964, merged three private streetcar companies. Oversees metro, streetcar, bus, and ferry.
- **Metro de Sant Cristòfor** — operates metro and ferry under ATS
- **Tramvia de Sant Cristòfor** — operates streetcar under ATS
- **Autobusos de Sant Cristòfor** — operates bus under ATS
- **Ferrocarrils de l'Istme** — national rail operator, commuter rail and (formerly) Intercon
- **Autoritat Aeroportuària de Balboa** — national airport authority

## 11. Total Daily Ridership Summary

| Mode | Daily ridership | % of total |
|------|----------------|------------|
| Metro | 2,100,000 | 58.7% |
| Bus | 760,000 | 21.2% |
| Streetcar | 250,000 | 7.0% |
| Commuter rail | 350,000 | 9.8% |
| Ferry | 118,500 | 3.3% |
| **Total** | **3,578,500** | **100%** |
