# Sant Cristòfor Bus Network — Internal Design Document

## Design Principles

The bus network complements the metro (9 lines, radial from Grand Train Terminal) and streetcar (3 lines, city centre). Buses serve:
1. Cross-town connections between radial metro lines
2. Low-density outer ciutats where metro doesn't reach
3. Peninsula internal circulation (Barcelona has no metro crossing)
4. Airport and industrial area connections

## Ciutat Analysis

### High-density urban core (metro + streetcar + bus feeders)
- **Original** (731K, 8,811/km²) — dense core, narrow streets. Metro + streetcar primary. Bus serves as cross-town and feeder to metro stations. Heavy bus usage for cafeteria hall lunch rush, financial district commuters.
- **Barcelona** (732K, 10,605/km²) — densest, peninsula. No metro crossing of bay. Ferry primary for cross-bay. Bus critical for internal peninsula circulation (north-south along peninsula, east-west across). High ridership.
- **Dàrsena** (575K, 3,803/km²) — nightlife, warehouses. Metro serves east-west. Bus serves north-south connections, nightlife district circulation (late night when metro closes). Sòtol gay village.

### Medium-density urban (metro + bus primary)
- **Costa Nord** (580K, 3,742/km²) — affluent, media industry. Metro along coast. Bus serves interior routes, studio/production house connections, north-south.
- **Sant Llorenç** (540K, 3,777/km²) — working class, industrial. Metro serves main corridors. Bus serves industrial areas, residential feeders, cross-town.
- **Sant Jordi** (461K, 2,214/km²) — residential. Metro through centre. Bus serves residential streets, cross-town.

### Low-density suburban (bus primary, limited metro)
- **Sant Martí** (435K, 1,204/km²) — airport, suburban. Metro Line 1 + 9 serve airport corridor. Bus essential for rest of ciutat — residential areas, commercial strips.
- **Ciutat de l'Estació** (376K, 1,205/km²) — railyard, former airport. Metro serves main corridor. Bus serves residential areas, railyard workers.
- **Mare de Déu del Mar** (232K, 915/km²) — beaches, coastal. Limited metro. Bus primary — coastal route, beach connections, residential.
- **Sant Miquel** (230K, 800/km²) — foothills, affluent. No metro. Bus primary — hill routes, connections to metro terminals.
- **Ciutat del Pujol** (266K, 506/km²) — foothills, lowest density. No metro. Bus primary — limited routes, connections to metro terminals.

## Proposed Bus Route Categories

### 1. Trunk routes (high-frequency, main corridors)
- Cross-town east-west corridors connecting metro lines
- North-south corridors along major avenues
- Peninsula spine route (Barcelona north-south)
- Airport express (limited stops)

### 2. Standard routes (regular frequency, residential coverage)
- Ciutat internal circulation
- Metro feeder routes
- Industrial area services

### 3. Night routes (late night, nightlife areas)
- Dàrsena nightlife circuit
- Sòtol connections
- Weekend beach routes

### 4. Hill routes (Sant Miquel, Ciutat del Pujol)
- Steep terrain, smaller vehicles
- Limited frequency
- Connect to metro terminals at base of hills

## Estimated Ridership by Ciutat

| Ciutat | Daily bus riders | % of total | Notes |
|--------|-----------------|------------|-------|
| Original | 180,000 | 22.5% | Cross-town + financial district feeders |
| Barcelona | 160,000 | 20.0% | Internal peninsula circulation, no metro crossing |
| Dàrsena | 90,000 | 11.3% | Nightlife, cross-town |
| Costa Nord | 75,000 | 9.4% | Studio/industry connections |
| Sant Llorenç | 70,000 | 8.8% | Industrial, working class |
| Sant Martí | 60,000 | 7.5% | Airport area, suburban |
| Sant Jordi | 55,000 | 6.9% | Residential feeders |
| Ciutat de l'Estació | 40,000 | 5.0% | Railyard, residential |
| Mare de Déu del Mar | 30,000 | 3.8% | Coastal, beach routes |
| Sant Miquel | 22,000 | 2.8% | Hill routes, low density |
| Ciutat del Pujol | 18,000 | 2.3% | Hill routes, lowest density |
| **Total** | **800,000** | **100%** | |

## Key Route Design

### Peninsula routes (Barcelona)
- **B1**: Pandao ferry terminal → Barcelona centre → El Fort (north-south spine)
- **B2**: Platja de Jordi → Barcelona centre → northern Barcelona (east-west)
- **B3**: Circular peninsula route connecting ferry terminals

### Cross-town routes
- **C1**: Costa Nord → Original → Dàrsena → Sant Llorenç (east-west, northern)
- **C2**: Mare de Déu del Mar → Sant Jordi → Original → Sant Llorenç (east-west, central)
- **C3**: Sant Martí → Ciutat de l'Estació → Original (east-west, southern)

### North-south corridors
- **N1**: Costa Nord → Sant Jordi → Sant Martí (western)
- **N2**: Sant Miquel → Dàrsena → Original (central)
- **N3**: Ciutat del Pujol → Sant Llorenç → Ciutat de l'Estació (eastern)

### Hill routes
- **H1**: Metro terminal → Sant Miquel (foothill loop)
- **H2**: Metro terminal → Ciutat del Pujol (foothill loop)

### Night routes
- **N1**: Dàrsena nightlife circuit (Sòtol, clubs, warehouse district)
- **N2**: Original → Dàrsena → Barcelona late-night connector

### Airport
- **A1**: Airport express — Grand Train Terminal → Airport (limited stops)
