# Aeroístmus — Internal Notes

## Overview
- Flag carrier of Balboa, largest airline in the country
- IATA: AB, ICAO: AERO, Callsign: AEROISTMUS
- Parent: Aeroístmus S.A., publicly traded on Bolsa de Sant Cristòfor (SCX: AER)
- HQ: Sant Cristòfor, Estret Province
- Hubs: SCI (Sant Cristòfor), SBT (Sant Bart)
- Fleet: 58 total (8 A320-200 + 18 A321neo + 6 A330-300 + 4 787-9 + 10 777-300ER + 11 ATR 72-600 + 1 777F); 2 ATR 72-600 dry-leased to AeroTerminus
- On order: 20 A321neo, 15 A330-900, 10 A350-900, 3 ATR 72-600
- Destinations: 42 (22 domestic + 20 international)
- Employees: ~1,150
- Revenue: ~B420 million (2024)

## History Timeline
1. **1948**: Formed from merger of post-GAW remaining assets of Zong Balboa Airways and Volisanian Balboa Airlines
2. **1948–1973**: Managed by AC consortium (Adonian Community) — sole carrier serving the isthmus
3. **1973**: Treaty of Areza → transferred to Balboan government as state-owned enterprise
4. **Mid-1980s**: Privatized due to high costs, mounting losses, overstaffing from consortium era
   - IPO on Bolsa de Sant Cristòfor, majority stake sold to private investors
   - Government retained minority interest (later fully divested)
5. **1985**: SCI opens — modern hub for widebody international traffic
6. **1985–1991**: Real-estate asset crisis — restructuring continues
7. **1990s**: International network expansion (Lurandia, Abyala, Kaftia); 1994 AFA World Cup boost
8. **1992**: PNU opens — Aeroístmus concentrates long-haul at SCI, maintains domestic from both
9. **2000s**: Fleet modernization — A320 replaces 737 Classic, A330/A350 replaces A310
10. **Present**: Two-tier strategy: commercial international + government-subsidized essential services

## Predecessor Airlines
- **Zong Balboa Airways**: Airline of the former Zong Balboa dependent territory (1899–1950). Heavy losses during GAW Balboa Campaign.
- **Volisanian Balboa Airlines**: Airline operated by the Volisania-aligned rump state of Balboa during the war. Also suffered losses during the Balboa Campaign.

## Essential Services Programme
- Government-subsidized routes to remote/low-demand destinations
- Funded by Ministry of Transport
- Serves: Illes del Guano, Sant Agneu, selected interior highland destinations
- Routes subject to competitive tender, reviewed periodically

## Fleet History
| Period | Aircraft | Role |
|--------|----------|------|
| 1948–c.1960 | Various pre-war types | Surviving assets from merger |
| c.1950–c.1970 | Douglas DC-3 | Domestic + short-haul international |
| c.1960–c.1975 | Douglas DC-6 | Medium-haul international |
| c.1970–c.1990 | Boeing 737-200 | First jet type; domestic |
| c.1985–c.2000s | Airbus A310 | First widebody; international |
| c.1990–c.2005 | Boeing 737-300/400 | Replaced 737-200 |
| 2000s–present | Airbus A320/A321 | Domestic + short-haul intl |
| 2000s–present | Airbus A330 | Medium-haul international |
| c.2005–present | Boeing 777-300ER | Long-haul international (Okaiken routes from 2000s) |
| On order | Airbus A330neo | Medium-haul replacement for A330 |
| On order | Airbus A350-900 | Long-haul replacement for 777-300ER |
| c.1992–present | ATR 72-600 | Regional/essential services |

## Ownership
- FIDB: 8% (retained from privatization)
- BPF: 6% (institutional anchor)
- Public float: ~86%
- Government: no direct equity, but provides essential services subsidies

## Route Schedule & Fleet Planning

### Distances from QGIS map data

See `Aeroístmus distances.md` for full distance table with coordinates.

**Reference points:**
- SCI (Sant Cristòfor): -94.4028°, 0.6419°
- SBT (Sant Bart): -92.3318°, 2.6032°

### Flight time estimates (corrected from map data)

Block time = flight time + turnaround (30 min narrowbody, 45 min ATR, 60 min widebody).

#### Domestic (from SCI)

| Destination | Distance | Flight time | Source |
|-------------|----------|-------------|--------|
| Sant Bart (SBT) | 316 km | 35 min | POI |
| Portnou (PNU) | 75 km | 15 min | POI |
| Haicang (HAI) | 128 km | 20 min | POI |
| Badia Curta (BDC) | 411 km | 45 min | POI |
| Campdària | 87 km | 15 min | POI |
| Vellmar | 609 km | 1h 10min | POI |
| Novara | 526 km | 1h | POI |
| Costabella | 310 km | 35 min | POI |
| Portblanc | 657 km | 1h 15min | POI |
| Altaneu | 242 km | 30 min | POI |
| Sant Agneu (MTR) | 380 km | 45 min | POI |
| Illes del Guano (GNG) | 138 km | 20 min | POI |
| Sant Llàtzer (SLZ) | TBD | TBD | Not on POI map |

#### International (from SCI unless noted)

| Destination | Country | Distance | Flight time | Terminal | Source |
|-------------|---------|----------|-------------|----------|--------|
| Tamsui | Sinchew | 497 km | 45 min | B | Cities in Adonia |
| Gran Port de Sant Mateu | Tapuya | 2,262 km | 3h | B | Cities in Adonia |
| Port Soledat | Potocsí | 2,748 km | 3h 30min | B | Cities in Adonia |
| Guledga | Lacashe | 3,268 km | 4h | B | Cities in Adonia |
| Castejón | Balisca | 5,154 km | 6h 30min | B | Cities in Adonia |
| Hargiesa | Galwa | 7,504 km | 9h | C | Cities in Adonia |
| Ampuria | Volisania | 9,152 km | 11h | C | POI shapefile (Ampuria International Airport, -13.0953°, -23.6478°) |
| Kankadadka | Burawa | 8,872 km | 11h | C | Cities in Adonia |
| Aoyama-Maekawa | Nakamizu | 10,129 km | 12h | C | User-provided coordinates (34°55′27″S 174°43′04″E) |
| Mariapolis | Sarta | 10,729 km | 13h | C | POI shapefile (Mariapolis International Airport, 2.7303°, -31.4995°) |
| Okami | Okaiken | 11,873 km | 14h | B | User-provided coordinates (16°39′53″S 158°15′47″E) |
| Sanu-Sasso | Asikyira | TBD | TBD | B | Not on map |
| Nanaimo | Kaneda | TBD | TBD | B | Not on map |
| Kanakou | Kaneda | TBD | TBD | B | Not on map |
| Kuluba | Asikyira | TBD | TBD | C | Not on map |
| Iskhal | Burawa | TBD | TBD | C | Not on map |
| Auxin | Daras | TBD | TBD | C | Not on map |
| Sanropura | Sanrobonia | TBD | TBD | C | Not on map |

**Dropped routes:**
- ~~Luanjing (Daras)~~ — 16,056 km, not economical
- ~~Akyatan (Dagit)~~ — 15,535 km, not economical
- ~~Okami-Tobu~~ — Okami-Tobu is the airport serving Okami; route listed as SBT↔Okami
- ~~Aoyama (Okaiken)~~ — now served via Aoyama-Maekawa International Airport (Nakamizu), 10,129 km / 12h
- ~~Miyagami (Nakamizu)~~ — dropped, replaced by Aoyama-Maekawa (closer to SCI, 3,351 km shorter)

### Proposed aircraft assignment by route

#### ATR 72-600 (7 aircraft) — Regional & essential services

**Seat configuration:**

| Parameter | Value |
|-----------|-------|
| Capacity | 72 seats |
| Layout | 2-2 (4 seats per row, 18 rows) |
| Class | All economy |
| Seat pitch | 30" |
| Seat width | 17" |
| Seat type | Leather (standard for ATR) |
| Cabin crew | 2 (1 per 50 pax, EASA standard) |

**Registrations:** BL-ATA through BL-ATG (7 aircraft owned; 5 operated by Aeroístmus, 2 dry-leased to [[AeroTerminus]])

**Leasing:** Aeroístmus owns 7 ATR 72-600s but operates only 5. The remaining 2 are dry-leased to [[AeroTerminus]] (aircraft only; AeroTerminus provides crew, maintenance, and insurance). Replaced AeroTerminus's previous E175s c. 2024.

**Block schedule:** See `Aeroístmus ATR schedule.csv` for full day-of-operations schedule with flight numbers (AB301–AB360), aircraft registrations, departure/arrival times, and block times.

| Route | Flight time | Frequency | Sectors/day | Block hrs/day |
|------|------------|------------|-------------|---------------|
| SCI↔Campdària | 15 min | 3x daily | 6 | 2.0 |
| SCI↔Costabella | 35 min | 3x daily | 6 | 4.0 |
| SCI↔Portblanc | 1h 15min | 2x daily | 4 | 5.7 |
| SCI↔Altaneu | 30 min | 2x daily | 4 | 2.7 |
| SCI↔Sant Agneu | 45 min | daily | 2 | 1.7 |
| SCI↔Illes del Guano | 20 min | daily | 2 | 1.1 |
| SCI↔Novara | 1h | 3x daily | 6 | 6.7 |
| SBT↔Sant Llàtzer | TBD | 3x daily | 6 | TBD |
| SBT↔Campdària | 30 min | 2x daily | 4 | 2.5 |
| SBT↔Costabella | 35 min | 2x daily | 4 | 2.7 |
| SBT↔Altaneu | 30 min | daily | 2 | 1.3 |
| SBT↔Novara | 1h | 2x daily | 4 | 4.5 |
| **Total** | | | **~48** | **~29.6** (excl. SLZ) |

Capacity: 5 aircraft, 4 effective (1 in maintenance), 4 × 8h = 32h/day
**Verdict: Fits with ~2.4h/day headroom.** Vellmar and Portblanc moved to A321 narrowbody.

Note: Portblanc at 657 km / 1h 15min is at the upper end of ATR 72-600 comfortable range. Novara (526 km) and Vellmar (609 km) are also long ATR sectors. Consider moving these to narrowbody if ATR capacity is insufficient.

#### A321 (8 aircraft) — Domestic trunk + short-haul international

**Seat configurations:**

Two configurations across the fleet:

**J/W/Y config (Business + Premium Economy + Economy) — 4 aircraft:**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| Business | BL-J-3 | 2-2 with divider | 40" | 20.5" | 12 |
| Premium Economy | BL-W-3 | 3-3 | 34" | 17.5" | 42 |
| Economy | BL-Y-4 | 3-3 | 30" | 17" | 144 |
| **Total** | | | | | **198** |

**W/Y config (Premium Economy + Economy) — 4 aircraft:**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| Premium Economy | BL-W-3 | 3-3 | 34" | 17.5" | 54 |
| Economy | BL-Y-4 | 3-3 | 30" | 17" | 150 |
| **Total** | | | | | **204** |

**Registrations:** BL-ABA through BL-ABH (8 aircraft)
- J/W/Y: BL-ABA, BL-ABB, BL-ABC, BL-ABD
- W/Y: BL-ABE, BL-ABF, BL-ABG, BL-ABH

**Fleet history:**
- 2013: Initial A321 deliveries (BL-ABA through BL-ABD) replacing older A320s
- 2016–2018: Fleet expansion (BL-ABE through BL-ABH) for route growth
- 2021–2023: Pandemic refit — all 8 aircraft unified with current product line (BL-J-3, BL-W-3, BL-Y-4). Business class dividers added during refit. Individual underseat power installed at all seats.
- 2024: A321neo on order to begin replacing oldest A321s from 2026; additional airframes planned as new routes are added

**Route assignments:**

J/W/Y routes (4 aircraft):

| Route | Flight time | Frequency | Sectors/day | Block hrs/day |
|------|------------|------------|-------------|---------------|
| SCI↔SBT | 35 min | 10x daily | 20 | 13.3 |
| SCI↔Badia Curta | 45 min | 4x daily | 8 | 6.7 |
| SCI↔Tamsui | 45 min | 2x daily (non-Sanu-Sasso days), 1x daily (Sanu-Sasso days) | ~3.4 | ~3.1 |
| SCI↔Sanu-Sasso | 4h 30min | 4x weekly (J/W/Y) + 3x weekly (W/Y) | 2.0 | 9.0 |
| SBT↔Gran Port de Sant Mateu | 2h 45min | weekly (Sat) | 0.29 | 1.1 |
| **Total** | | | **~25.4** | **~23.2** (excl. Sanu-Sasso) |

W/Y routes (4 aircraft):

| Route | Flight time | Frequency | Sectors/day | Block hrs/day |
|------|------------|------------|-------------|---------------|
| SCI↔Haicang | 20 min | daily | 2 | 0.9 |
| SCI↔Sanu-Sasso (W/Y) | 4h 30min | 3x weekly (Tue/Thu/Sat) | 0.86 | 3.9 |
| SCI↔Vellmar | 1h 10min | 3x daily | 6 | 7.7 |
| SCI↔Portblanc | 1h 15min | 2x daily | 4 | 5.7 |
| SBT↔Portnou | 30 min | 3x daily | 6 | 3.5 |
| SBT↔Haicang | 20 min | daily | 2 | 0.9 |
| SBT↔Badia Curta | 45 min | 3x daily | 6 | 5.0 |
| SBT↔Portnou | 65 min | daily | 2 | 2.2 |
| SCI↔Gran Port de Sant Mateu | 3h | daily | 2 | 7.0 |
| SCI↔Guledga | 4h | 3x weekly | 0.86 | 4.0 |
| SBT↔Guledga | 3h 30min | weekly | 0.29 | 1.2 |
| SBT↔Vellmar | 1h 10min | 2x daily | 4 | 5.3 |
| SBT↔Portblanc | 1h 15min | 2x daily | 4 | 5.7 |
| **Total** | | | **~40.3** | **~49.1** |

**Combined narrowbody utilization:**
- J/W/Y: ~23.2h/day (excl. Sanu-Sasso) + ~5.1h/day Sanu-Sasso = ~28.3h/day — 4 aircraft, 3.5 effective × 12h = 42h/day capacity
- W/Y: ~49.1h/day — 4 aircraft, 3.5 effective × 12h = 42h/day capacity
- Total: ~77.4h/day, 7 effective × 12h = 84h/day capacity
- **Headroom: ~6.6h/day** — tight but workable

Note: Guledga at 3,268 km / 4h and Sanu-Sasso at ~3,568 km / 4h 30min are within A321 range (~6,100 km) but at the edge of comfortable single-aisle operation. Consider A330 if demand grows.

#### A330 (5 aircraft) — Medium-haul international + high-demand short-haul

**Seat configuration (standard across all 5 aircraft):**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| Business | BL-J-2 | 2-2-2 | 68" | 20" | 24 |
| Premium Economy | BL-W-2 | 2-3-2 | 36" | 18" | 49 |
| Economy | BL-Y-3 | 2-4-2 | 31" | 17" | 176 |
| **Total** | | | | | **249** |

**Registrations:** BL-WBA, BL-WBB, BL-WBC, BL-WBD, BL-WBE

**Fleet history:**
- 2012: BL-WBA and BL-WBB delivered (first 2 × A330-300, replacing A300 on medium-haul)
- 2015: BL-WBC and BL-WBD delivered (fleet expansion for Castejón 2x daily + Hargiesa)
- 2018: BL-WBE delivered (5th A330 for Port Soledat daily from both hubs)
- 2012–2019: Previous-generation products (angled lie-flat business, no premium economy)
- 2021–2023: Pandemic refit — all 5 aircraft refurbished with current product line (BL-J-2, BL-W-2, BL-Y-3). Premium economy (BL-W-2) added during this refit.
- 2025–present: A330neo on order to eventually replace A330-300

| Route | Distance | Flight time | Frequency | Sectors/day | Block hrs/day |
|------|----------|------------|------------|-------------|---------------|
| SCI↔Castejón | 5,154 km | 6h 30min | 2x daily | 4 | 26.0 |
| SCI↔Hargiesa | 7,504 km | 9h | 3x weekly | 0.86 | 8.6 |
| SCI↔Port Soledat | 2,748 km | 3h 30min | daily | 2.0 | 7.0 |
| SBT↔Port Soledat | 2,470 km | 2h 54min | daily | 2.0 | 5.8 |
| SBT↔Castejón | ~5,000 km | 6h | 2x weekly | 0.57 | 4.0 |
| **Total** | | | | **~9.43** | **~51.4** |

Capacity: 5 aircraft, 4.5 effective, 4.5 × 14h = 63h/day
**Headroom: ~11.6h/day.** Iskhal moved to 777 fleet (BL-WAE, 1x weekly). TBD routes (Nanaimo, Kanakou, Kuluba, Sanropura) deferred — distances unknown.

Note: Castejón has 2x daily A330 service. Ampuria (business hub) is served daily by 777 fleet (BL-WAD + BL-WAJ). Port Soledat has daily service from both SCI and SBT.

#### 777-300ER — Long-haul international

**Seat configurations:**

**Fleet history:**
- 2009: BL-WAA and BL-WAB delivered (first 2 × 777-300ER, replacing A310 on long-haul)
- 2014: BL-WAC and BL-WAD delivered (fleet expansion to 4 aircraft for daily Miyagami + Okami)
- 2016: BL-WAE delivered (5th 777-300ER for Ampuria + Iskhal routes)
- 2009–2019: Previous-generation premium products (older first class suites, angled lie-flat business, no premium economy)
- 2020–2022: Pandemic refit — all 5 aircraft refurbished with current product line (BL-F-1, BL-J-1, BL-W-1, BL-Y-1/BL-Y-2). Premium economy (BL-W-1) added during this refit. BL-WAD configured as business-heavy for Okami; BL-WAA/WAB/WAC/WAE configured as mixed for Miyagami/Ampuria/Iskhal.
- 2024: BL-WAF and BL-WAG delivered (6th and 7th 777-300ER for Aoyama-Maekawa 2x daily expansion)
- 2026: BL-WAH and BL-WAI delivered (8th and 9th 777-300ER for Mariapolis route)
- 2024–present: A350-900 on order to eventually replace 777-300ER (planned full-height suite first class product)

**Fleet requirement justification:**
- 2 aircraft (WAA/WAB) for daily Aoyama-Maekawa daytime: each does 1 RT every ~1.5 days (~18h/aircraft/day), with maintenance buffer
- 2 aircraft (WAF/WAG) for daily Aoyama-Maekawa overnight: same pattern, offset rotation
- 2 aircraft (WAC/WAE) for daily Okami: each does 1 RT every ~2 days (~14h/aircraft/day)
- 1 aircraft (WAD) for daily Ampuria (777): 22h/day utilization, continuous rotation
- 2 aircraft (WAH/WAI) for daily Mariapolis: each does same-day RT every 2 days (~13h/aircraft/day)
- Total: 9 aircraft, 8 effective × 14h = 112h/day capacity vs ~111h/day scheduled
- **Headroom: ~1h/day** — tight but manageable with maintenance scheduling

Two subfleets with different configurations:

**Miyagami (mixed) — BL-WAA, WAB, WAC:**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| First | BL-F-1 | 1-2-1 | 84" | 29" | 8 |
| Business | BL-J-1 | 1-2-1 herringbone | 76" | 21" | 32 |
| Economy+ | BL-W-1 | 2-4-2 | 38" | 18.5" | 36 |
| Economy | BL-Y-2 | 3-3-3 | 33" | 18" | 198 |
| **Total** | | | | | **274** |

**Okami (business-heavy) — BL-WAD:**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| First | BL-F-1 | 1-2-1 | 84" | 29" | 4 |
| Business | BL-J-1 | 1-2-1 herringbone | 76" | 21" | 48 |
| Economy+ | BL-W-1 | 2-4-2 | 38" | 18.5" | 32 |
| Economy | BL-Y-1 | 3-4-3 | 32" | 17" | 166 |
| **Total** | | | | | **250** |

**Ampuria/Iskhal (mixed) — BL-WAE:**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| First | BL-F-1 | 1-2-1 | 84" | 29" | 8 |
| Business | BL-J-1 | 1-2-1 herringbone | 76" | 21" | 32 |
| Economy+ | BL-W-1 | 2-4-2 | 38" | 18.5" | 36 |
| Economy | BL-Y-2 | 3-3-3 | 33" | 18" | 198 |
| **Total** | | | | | **274** |

**Mariapolis (mixed) — BL-WAH, BL-WAI:**

| Class | Seat type | Layout | Pitch | Width | Seats |
|-------|-----------|--------|-------|-------|-------|
| First | BL-F-1 | 1-2-1 | 84" | 29" | 8 |
| Business | BL-J-1 | 1-2-1 herringbone | 76" | 21" | 32 |
| Economy+ | BL-W-1 | 2-4-2 | 38" | 18.5" | 36 |
| Economy | BL-Y-2 | 3-3-3 | 33" | 18" | 198 |
| **Total** | | | | | **274** |

**Registrations:** BL-WAA, BL-WAB, BL-WAC (Aoyama-Maekawa), BL-WAD (Ampuria), BL-WAE (Okami), BL-WAF, BL-WAG (Aoyama-Maekawa overnight), BL-WAH, BL-WAI (Mariapolis)

### Seat type catalogue

#### BL-F-1 — First Class (Long-Haul)

Designed to compete with Okaiken Airlines' first class product. Not full-enclosure suites (planned for A350), but partial-height "rooms" offering privacy and space.

| Parameter | Specification |
|-----------|--------------|
| Layout | 1-2-1 |
| Pitch | 84" (7 ft) |
| Seat width | 29" |
| Enclosure | Partial-height walls — not a full suite, but enough to create a "room" feel. Walls high enough for seated privacy, low enough to avoid claustrophobia. |
| Bed | Lie-flat, 80" extended length, 29" width, with mattress pad and bedding |
| Guest capability | Space for a guest to sit across — fold-out companion seat / dining surface. Designed for in-flight meetings or shared dining. |
| IFE screen | 42-inch 4K display, seat-mounted |
| Tablet | Seat-mounted tablet for controls: seat position, lighting, temperature, IFE navigation, meal ordering, crew call |
| Storage | Personal wardrobe, under-seat storage, overhead bin |
| Privacy | Sliding privacy divider between paired center seats |
| Power | Universal AC, USB-A, USB-C |
| Lighting | Personal reading light, adjustable ambient lighting |
| Audio | Noise-canceling headphones provided |
| Other | Personal air vent, water bottle holder, amenity kit |

**Design philosophy:** Aeroístmus cannot yet match the ultra-luxury full-height suites of top-tier carriers (planned for A350 delivery), but BL-F-1 offers a competitive "room" product — partial enclosure, generous personal space, guest seating, and a class-leading 42" screen. The emphasis is on functionality and privacy for business travelers on 16-17h sectors.

#### BL-J-1 — Business Class (Long-Haul)

Standard herringbone layout — angled lie-flat seats offering direct aisle access and natural privacy from the herringbone geometry.

| Parameter | Specification |
|-----------|--------------|
| Layout | 1-2-1 herringbone (seats angled ~45° to cabin wall) |
| Pitch | 76" |
| Seat width | 21" |
| Bed | Lie-flat 180°, 76" extended length, 21" width, with cushioned pad and bedding |
| Privacy | Herringbone angle provides natural privacy; no additional divider needed |
| IFE screen | 18-inch 4K display, seat-mounted |
| Controls | Touch-screen seat panel for seat position, IFE, lighting, crew call |
| Storage | Personal side stowage, overhead bin |
| Power | Universal AC, USB-A, USB-C |
| Lighting | Personal reading light |
| Audio | Noise-canceling headphones provided |
| Other | Personal air vent, water bottle holder, amenity kit |

**Design philosophy:** No-frills competitive business class. The herringbone layout is a proven, industry-standard configuration that maximizes privacy and aisle access without the expense of custom suite enclosures. BL-J-1 prioritizes a comfortable lie-flat bed and functional workspace over luxury features — appropriate for the mixed Miyagami route where business class demand is moderate.

#### BL-W-1 — Premium Economy (Long-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 2-4-2 |
| Pitch | 38" |
| Seat width | 18.5" |
| Recline | 8" (deep recline with cradle mechanism) |
| Headrest | Adjustable 4-way headrest |
| Footrest | Extendable footrest from seat |
| IFE screen | 13-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Headphones provided (over-ear, not noise-canceling) |
| Other | Personal air vent, water bottle holder, amenity kit, priority boarding |

**Design philosophy:** Solid premium economy — meaningfully better than economy without approaching business class. The 38" pitch and 8" recline make 16-17h sectors tolerable for price-sensitive travelers who need more than standard economy. Individual underseat AC + USB-A power at every seat. The 13" screen is a clear step up from economy IFE.

#### BL-Y-1 — Economy (Long-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 3-4-3 |
| Pitch | 32" |
| Seat width | 17" |
| Recline | 4" |
| Headrest | Adjustable 2-way headrest |
| IFE screen | 11-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Earbuds provided |
| Other | Personal air vent, water bottle holder |

**Design philosophy:** Standard long-haul economy — competitive but not exceptional. The 32" pitch and 17" width are industry standard for 777-300ER 3-4-3 configuration. Individual underseat AC + USB-A power at every seat. The 11" screen is adequate for the sector length. This is the volume product — the majority of seats on the Okami subfleet.

#### BL-Y-2 — Economy (Long-Haul, Spacious)

| Parameter | Specification |
|-----------|--------------|
| Layout | 3-3-3 |
| Pitch | 33" |
| Seat width | 18" |
| Recline | 5" |
| Headrest | Adjustable 4-way headrest |
| IFE screen | 12-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Earbuds provided |
| Other | Personal air vent, water bottle holder |

**Design philosophy:** A more spacious economy product — 3-3-3 instead of 3-4-3 gives an extra inch of width and personal space. Individual AC power (not shared USB) and a slightly larger screen. Intended for aircraft where the overall seat count is lower and the route profile warrants a better economy experience. Used on the Miyagami subfleet; the Okami aircraft retains BL-Y-1 (3-4-3).

### A330 seat type catalogue

#### BL-J-2 — Business Class (Medium-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 2-2-2 |
| Pitch | 68" |
| Seat width | 20" |
| Recline | Full lie-flat, 68"×20" bed |
| Headrest | Adjustable 4-way headrest |
| IFE screen | 15-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, personal item stowage, overhead bin |
| Power | Universal AC, USB-A (individual) |
| Lighting | Personal reading light, adjustable overhead |
| Audio | Noise-cancelling headphones provided |
| Other | Personal air vent, water bottle holder, blanket + pillow |

**Design philosophy:** Medium-haul business class for the A330 fleet. 2-2-2 layout is the natural fit for the A330's narrower cabin (5.28m vs 777's 5.87m). Full lie-flat beds are essential for the longest A330 routes (Hargiesa 9h, Castejón 6.5h). Slightly less premium than BL-J-1 (68" vs 76" pitch, 15" vs 18" IFE, no herringbone privacy) but still a competitive product. No aisle access from window seat — acceptable for medium-haul but would be inadequate on long-haul.

#### BL-W-2 — Premium Economy (Medium-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 2-3-2 |
| Pitch | 36" |
| Seat width | 18" |
| Recline | 7" cradle recline |
| Headrest | Adjustable 4-way headrest |
| Footrest | Extendable footrest |
| IFE screen | 11-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Earbuds provided |
| Other | Personal air vent, water bottle holder |

**Design philosophy:** Medium-haul premium economy, slightly tighter than the long-haul BL-W-1 (36" vs 38" pitch, 11" vs 13" IFE). 2-3-2 is the standard A330 premium economy layout. Individual underseat AC + USB-A power at every seat. Provides a clear step up from economy on routes like Castejón (6.5h) and Hargiesa (9h) without the cost overhead of the long-haul product.

#### BL-Y-3 — Economy (Medium-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 2-4-2 |
| Pitch | 31" |
| Seat width | 17" |
| Recline | 4" |
| Headrest | Adjustable 2-way headrest |
| IFE screen | 10-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Earbuds provided |
| Other | Personal air vent, water bottle holder |

**Design philosophy:** Standard medium-haul economy for the A330 fleet. 2-4-2 is the native A330 layout — no middle-seat-pair issues like the 777's 3-4-3 (only the 4-across center section has middle seats). 31" pitch is competitive for the sector lengths. Individual underseat AC + USB-A power at every seat. The 10" screen is adequate for 3-9h flights.

### A321 seat type catalogue

#### BL-J-3 — Business Class (Short-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 2-2 with privacy divider |
| Pitch | 40" |
| Seat width | 20.5" |
| Recline | 8" cradle recline (deep recliner, not lie-flat) |
| Headrest | Adjustable 4-way headrest |
| Footrest | Extendable footrest |
| IFE screen | 12-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, personal item stowage, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Noise-cancelling headphones provided |
| Other | Personal air vent, water bottle holder, privacy divider between seats |

**Design philosophy:** Short-haul narrowbody business class for the A321 fleet. 2-2 with privacy divider gives every passenger direct aisle access and a sense of personal space — important for the trunk SCI↔SBT route where business travellers are the primary market. 40" pitch and 8" cradle recline make 3h sectors (Gran Port de Sant Mateu) comfortable without the weight penalty of lie-flat beds. No herringbone or staggered layout needed — the A321's narrow cabin makes 2-2 the efficient choice.

#### BL-W-3 — Premium Economy (Short-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 3-3 |
| Pitch | 34" |
| Seat width | 17.5" |
| Recline | 5" |
| Headrest | Adjustable 4-way headrest |
| Footrest | Extendable footrest |
| IFE screen | 10-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Earbuds provided |
| Other | Personal air vent, water bottle holder |

**Design philosophy:** Short-haul premium economy on the A321. 3-3 layout with 34" pitch — 4" more than economy and a wider seat. Clear step up from economy on longer narrowbody sectors (Gran Port de Sant Mateu 3h, Guledga 4h) while keeping the same 3-3 layout for operational flexibility. Individual underseat power at every seat.

#### BL-Y-4 — Economy (Short-Haul)

| Parameter | Specification |
|-----------|--------------|
| Layout | 3-3 |
| Pitch | 30" |
| Seat width | 17" |
| Recline | 3" |
| Headrest | Adjustable 2-way headrest |
| IFE screen | 8-inch 1080p display, seat-mounted |
| Controls | Touch-screen controller in armrest |
| Storage | Seat pocket, overhead bin |
| Power | Universal AC, USB-A (individual, underseat) |
| Lighting | Personal reading light |
| Audio | Earbuds provided |
| Other | Personal air vent, water bottle holder |

**Design philosophy:** Standard short-haul economy for the A321 fleet. 30" pitch is competitive for sectors up to 4h. 3-3 is the native A321 layout. Individual underseat AC + USB-A power at every seat — a differentiator against competing carriers on domestic trunk routes. The 8" screen is adequate for short sectors; streaming to personal devices also available via onboard WiFi.

**Route 1: SCI↔Aoyama-Maekawa (AYM) — Daily**

| Flight | From | To | Dep | Arr | Block | Aircraft rotation |
|--------|------|----|-----|-----|-------|-------------------|
| AB101 | SCI | AYM | 10:00 | 22:00 | 12h | Daily departure |
| AB102 | AYM | SCI | 23:55 | 11:55 | 12h | Daily departure (next day arrival) |

Each round trip: 12h + ~2h turnaround + 12h = ~26h
Daily service requires 2 aircraft rotating (each does 1 RT every ~1.5 days, ~18h/aircraft/day)
Aircraft: BL-WAA, BL-WAB

**Route 2: SCI↔Okami-Tobu (OKI) — 2x weekly business pattern**

| Flight | From | To | Dep | Arr | Block | Notes |
|--------|------|----|-----|-----|-------|-------|
| AB103 | OKI | SCI | Mon 06:00 | Mon 20:00 | 14h | Arrives SCI Monday evening for business week |
| AB104 | SCI | OKI | Fri 22:00 | Sat 12:00 | 14h | Departs SCI Friday night, arrives Saturday |
| AB105 | OKI | SCI | Sun 06:00 | Sun 20:00 | 14h | 2nd weekly frequency — Sunday arrival |
| AB106 | SCI | OKI | Wed 22:00 | Thu 12:00 | 14h | 2nd weekly frequency — Wednesday departure |

2 round trips/week = 56h block/week = ~8.0h/day average
Aircraft: BL-WAD (1st frequency) + BL-WAC (2nd frequency, freed from Aoyama switch)

**Codeshare with Sanesair (Adonian Arrow alliance):**
- Sanesair operates Okami-Tobu → Akyatan (Dagit) sector: 1,696 km, ~2h flight time
- Sanesair uses 787-9 (215 seats: 48J/21W/146Y) — existing fleet, no reconfiguration
- Through-fare SCI → Okami → Akyatan, revenue split ~40% Aeroístmus / ~60% Sanesair
- Serves Dagit community in Balboa (VFR/repatriation traffic) and Dagit visitors to Balboa
- Sanesair's 220-destination network provides onward connectivity from Okami hub
- Avoids need for dedicated high-density 777 config on SCI→Akyatan direct (13,209 km, 15.5h)
- Sanesair 787-9 Okami→Akyatan sector cost: ~$31.5K/sector, profitable at all load factors above 65%

**BL-WAD weekly timeline (1st Okami frequency + Ampuria):**
- Mon 06:00–20:00: Fly OKI→SCI (AB103, 14h)
- Tue 08:00–19:00: Fly SCI→AMP (AB109, 11h)
- Wed 09:00–20:00: Fly AMP→SCI (AB110, 11h)
- Thu 08:00–19:00: Fly SCI→AMP (AB109, 11h)
- Fri 09:00–20:00: Fly AMP→SCI (AB110, 11h)
- Fri 22:00–Sat 12:00: Fly SCI→OKI (AB104, 14h)
- Sat 12:00–Mon 06:00: On ground at OKI (~1.75 days)

**BL-WAC weekly timeline (2nd Okami frequency + Ampuria):**
- Sun 06:00–20:00: Fly OKI→SCI (AB105, 14h)
- Mon 08:00–19:00: Fly SCI→AMP (AB109, 11h)
- Tue 09:00–20:00: Fly AMP→SCI (AB110, 11h)
- Wed 22:00–Thu 12:00: Fly SCI→OKI (AB106, 14h)
- Thu 12:00–Sun 06:00: On ground at OKI (~2.75 days, maintenance window)

**Route 3: SCI↔Ampuria (AMP) — 5x weekly (business hub)**

Operated by two aircraft: BL-WAE (3x weekly) and BL-WAD (2x weekly, mid-week between Okami flights).

BL-WAE (AB105/AB106):

| Flight | From | To | Dep | Arr | Block | Notes |
|--------|------|----|-----|-----|-------|-------|
| AB105 | SCI | AMP | Sun 20:00 | Mon 07:00 | 11h | Red-eye, arrives Mon morning for business week |
| AB106 | AMP | SCI | Mon 12:00 | Mon 23:00 | 11h | Returns same day, 5h turnaround at AMP |
| AB105 | SCI | AMP | Tue 08:00 | Tue 19:00 | 11h | Daytime departure |
| AB106 | AMP | SCI | Wed 09:00 | Wed 20:00 | 11h | 14h overnight at AMP |
| AB105 | SCI | AMP | Thu 08:00 | Thu 19:00 | 11h | Daytime departure |
| AB106 | AMP | SCI | Fri 09:00 | Fri 20:00 | 11h | 14h overnight at AMP |

BL-WAD (AB109/AB110):

| Flight | From | To | Dep | Arr | Block | Notes |
|--------|------|----|-----|-----|-------|-------|
| AB109 | SCI | AMP | Mon 12:00 | Mon 23:00 | 11h | Departs after Okami arrival, 3h turnaround |
| AB110 | AMP | SCI | Tue 09:00 | Tue 20:00 | 11h | 10h overnight at AMP |
| AB109 | SCI | AMP | Wed 08:00 | Wed 19:00 | 11h | Daytime departure |
| AB110 | AMP | SCI | Thu 09:00 | Thu 20:00 | 11h | 14h overnight at AMP |

5 round trips/week = 110h block/week = ~15.7h/day total.

**Route 4: SCI↔Iskhal (ISK) — 1x weekly (tourist)**

| Flight | From | To | Dep | Arr | Block | Notes |
|--------|------|----|-----|-----|-------|-------|
| AB107 | SCI | ISK | Sat 08:00 | Sat 19:00 | 11h | Weekend leisure departure |
| AB108 | ISK | SCI | Sun 09:00 | Sun 20:00 | 11h | Sunday return |

Operated by BL-WAE (mixed config). 1 round trip/week = 22h block/week = ~3.1h/day.

**BL-WAE weekly timeline:**
- Sun 20:00–Mon 07:00: Fly SCI→AMP (AB105)
- Mon 12:00–Mon 23:00: Fly AMP→SCI (AB106)
- Tue 08:00–Tue 19:00: Fly SCI→AMP (AB105)
- Wed 09:00–Wed 20:00: Fly AMP→SCI (AB106)
- Thu 08:00–Thu 19:00: Fly SCI→AMP (AB105)
- Fri 09:00–Fri 20:00: Fly AMP→SCI (AB106)
- Sat 08:00–Sat 19:00: Fly SCI→ISK (AB107)
- Sun 09:00–Sun 20:00: Fly ISK→SCI (AB108)

#### SCI↔Mariapolis (MAR) — Daily

Operated by two aircraft: BL-WAH (Mon/Wed/Fri/Sun) and BL-WAI (Tue/Thu/Sat). Each does same-day round trips. Distance: 10,729 km, block time: 13h.

**BL-WAH (AB123/AB124) — Mon, Wed, Fri, Sun:**
- 20:00 SCI → 09:00+1 MAR (AB123, overnight, 13h)
- 11:00 MAR → 18:00 SCI (AB124, daytime, 13h)
- 2h turnaround at MAR, 2h turnaround at SCI
- Cycle: 30h (13h out + 2h turn + 13h back + 2h turn)
- Next departure: 2 days later (Mon→Wed, Wed→Fri, Fri→Sun, Sun→Tue)

**BL-WAI (AB123/AB124) — Tue, Thu, Sat:**
- 20:00 SCI → 09:00+1 MAR (AB123, overnight, 13h)
- 11:00 MAR → 18:00 SCI (AB124, daytime, 13h)
- Same 30h cycle, offset by 1 day from BL-WAH

Time zones: SCI = UTC-5, MAR = UTC-1 (4h difference).

**Fleet summary:**

| Route | Frequency | Sectors/day | Block hrs/day |
|------|------------|-------------|---------------|
| SCI↔Aoyama-Maekawa | 2x daily | 4.0 | 48.0 |
| SCI↔Okami | daily | 2.0 | 28.0 |
| SCI↔Ampuria | daily | 2.0 | 22.0 |
| SCI↔Mariapolis | daily | 2.0 | 26.0 |
| **Total** | | **~10.0** | **~124.0** |

Fleet needed: 9 aircraft (2 for Aoyama-Maekawa daytime + 2 for Aoyama-Maekawa overnight + 2 for Okami + 1 for Ampuria + 2 for Mariapolis). At 8 effective × 14h = 112h/day — tight utilization.
Codeshare: Sanesair operates Okami→Akyatan (Dagit) sector — no Aeroístmus aircraft needed for Akyatan.
Time zones: SCI = UTC-5, MAR (Mariapolis) = UTC-1.
Full schedule: See `Aeroístmus 777 schedule.csv`

### Fleet summary

| Type | Current | Needed (est.) | Spare/shortfall | Notes |
|------|---------|---------------|-----------------|-------|
| ATR 72-600 | 11 | 11 | ~0 | Vellmar & Portblanc moved to A321; ~29.6h/day vs 32h capacity |
| A321 | 18 | 18 | ~0 | 4 J/W/Y (198 seats) + 4 W/Y (204 seats); ~77.4h/day vs 84h capacity |
| A330 | 6 | 6 | ~0 | Castejón 2x daily + Hargiesa 3x weekly + Port Soledat daily (SCI+SBT) + SBT-Castejón 2x weekly = 51.4h; ~11.6h spare |
| 777-300ER | 9 | 9 | ~0 | 2 for Aoyama-Maekawa daytime + 2 for Aoyama-Maekawa overnight + 2 for Okami + 1 for Ampuria + 2 for Mariapolis |
| **Total** | **23** | **22-24** | **+1 to +3** | Vellmar & Portblanc moved from ATR to A321 W/Y |

### Key observations

1. **ATR fleet now fits** — 5 aircraft (4 effective), ~29.6h/day vs 32h/day capacity. Vellmar and Portblanc moved to A321 narrowbody.

2. **Narrowbody fleet has significant spare capacity** — 10 aircraft but only ~55h/day needed. Could absorb Novara/Vellmar/Portblanc from ATR and still have room. Consider reducing to 8 narrowbodies.

3. **A330 fleet is now well-utilized** — Castejón 2x daily (26h) + Hargiesa 3x weekly (8.6h) + Port Soledat 3x weekly (3.4h) + SBT-Castejón (4h) = ~42h/day. Only ~7h spare for TBD routes. If Castejón reduced to 1x daily, frees 13h.

4. **777-300ER fleet well-utilized with codeshare** — Aoyama-Maekawa (12h daily) + Okami (14h, 2x weekly) + Ampuria (11h, 5x weekly) + Iskhal (11h, weekly) = ~50.8h/day against 63h capacity. ~12.2h spare. Akyatan served via Sanesair codeshare (Okami→Akyatan 2h sector on 787-9), avoiding dedicated high-density 777 config. A350-900 on order to replace 777-300ER.

5. **Possible fleet adjustment**: 4 ATR + 8 narrowbody + 4 A330 + 2 777-300ER = 18 aircraft (saves 4 aircraft). Or: 5 ATR + 8 narrowbody + 4 A330 + 2 777-300ER = 19 aircraft (if Aoyama added with reduced frequency). A350-900 delivery will replace 777-300ER 1:1.

6. **TBD routes that need map coordinates**: Sanu-Sasso, Nanaimo, Kanakou, Kuluba, Iskhal, Auxin, Sanropura, Aoyama, Sant Llàtzer

### Open scheduling questions for user

1. Should Novara, Vellmar, and Portblanc move from ATR to narrowbody? (Long ATR sectors, narrowbody has spare capacity)
2. Should Castejón be 2x daily or 1x daily on A330? (2x daily = 26h/day, dominant route)
3. ~~Should Aoyama be added or dropped?~~ — Dropped, not economical
4. Frequencies for TBD routes once distances are known?
5. Any routes that should be seasonal only?

## Employee headcount

Total: ~1,150 employees (~50 per aircraft)

### Flight crew (pilots) — 289

| Fleet | Aircraft | Pilots/aircraft | Subtotal | Notes |
|-------|----------|-----------------|----------|-------|
| A321 | 8 | 11 | 88 | High-utilization narrowbody, 5 crew pairs + buffer |
| A330 | 5 | 13 | 65 | Medium-haul widebody |
| 777-300ER | 9 | 16 | 144 | Ultra-long-haul, augmented crews (4 pilots) for 13h Mariapolis / 12h Aoyama-Maekawa flights |
| ATR 72-600 | 5 | 8 | 40 | Regional, lower utilization |

### Cabin crew — 358

| Fleet | Aircraft | FAs/flight | Coverage sets | Subtotal | Notes |
|-------|----------|------------|---------------|----------|-------|
| A321 J/W/Y | 4 | 5 | 2.5 | 50 | Business class service |
| A321 W/Y | 4 | 4 | 2.5 | 40 | |
| A330 | 5 | 8 | 2.5 | 100 | 3-class service |
| 777-300ER | 9 | 12 | 2.5 | 270 | Long-haul 3-class + first class on BL-WAD |
| ATR 72-600 | 5 | 1 | 2.5 | 12 | Single FA |

### In-house catering division — 115

Aeroístmus operates an in-house catering division showcasing Balboan cuisine across all cabin classes, from economy to first class. Silverware is provided in all classes. The division partners with top Sant Cristòfor restaurants — including [[Atsui]] and [[Després]] — on menu development and signature dishes.

| Function | Headcount | Notes |
|----------|-----------|-------|
| Main kitchen SCI | 45 | Primary production facility — chefs, cooks, prep, packaging |
| Secondary kitchen SBT | 25 | Satellite kitchen for SBT-departed flights |
| Loading & delivery SCI | 15 | Catering trucks, aircraft loading |
| Loading & delivery SBT | 10 | |
| Menu development & chef partnerships | 8 | Liaison with Atsui, Després; seasonal menu design |
| Quality control & food safety | 7 | HACCP compliance, temperature checks, taste testing |
| Catering management | 5 | |

### Ground operations — 205

| Station | Headcount | Notes |
|---------|-----------|-------|
| SCI (main hub) | 85 | Check-in, gate, ramp, baggage, cleaning, customer service, cargo, management |
| SBT (secondary hub) | 48 | |
| BDC | 18 | |
| Portnou | 7 | |
| Haicang | 3 | |
| Domestic outstations | 12 | Tamsui, Sanu-Sasso, Gran Port, Guledga — minimal staff, contracted ground handling |
| International stations | 34 | Castejón, Hargiesa, Port Soledat, Miyagami, Okami, Ampuria, Iskhal, Mariapolis |

### Maintenance & engineering — 90

| Function | Headcount |
|----------|-----------|
| Line maintenance SCI | 30 |
| Line maintenance SBT | 15 |
| Base maintenance SCI | 25 |
| Engineering & parts | 20 |

### Operations & dispatch — 28

| Function | Headcount |
|----------|-----------|
| 24/7 ops center (SCI) | 20 |
| Crew scheduling | 8 |

### Administration — 88

| Function | Headcount |
|----------|-----------|
| Executive management | 8 |
| Sales & revenue | 15 |
| Marketing | 8 |
| IT | 12 |
| HR | 10 |
| Finance & accounting | 15 |
| Legal & compliance | 5 |
| Training | 15 |

### Summary

| Category | Headcount | % of total |
|----------|-----------|------------|
| Pilots | 273 | 23.7% |
| Cabin crew | 352 | 30.6% |
| Catering | 115 | 10.0% |
| Ground operations | 205 | 17.8% |
| Maintenance | 85 | 7.4% |
| Ops & dispatch | 28 | 2.4% |
| Administration | 88 | 7.7% |
| **Total** | **1,146** | **100%** |
6. Cargo operations — does Aeroístmus operate cargo flights (e.g., A330F)?

## Open Questions
1. Key people — CEO, founder figures? (No specific names invented yet)
2. Exact privatization date (mid-1980s is approximate)
3. When did A310 get replaced by A330/A350?
4. Aeroístmus dry-leases E175s to AeroTerminus — when did this arrangement begin?
5. SBT international routes — when were these added? (SBT-Okami, SBT-Castejón, SBT-Gran Port, SBT-Guledga)
6. Revenue breakdown: domestic vs international, cargo, ancillary
7. Lounge network? ~~Frequent flyer programme?~~ — Star Circle created, see `Star Circle internal.md` and `Star Circle.mediawiki`
8. Accidents and incidents?

## Files
- `articles/Countries/Balboa/Companies/Aeroístmus.mediawiki` — wiki article
- `articles/Countries/Balboa/Companies/Aeroístmus internal.md` — this file
- `articles/Countries/Balboa/Companies/Aeroístmus distances.md` — distance calculations from QGIS map data
