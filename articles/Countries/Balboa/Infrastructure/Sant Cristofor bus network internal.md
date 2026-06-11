# Sant Cristòfor Surface Transit — Internal Design Document

## Design Principles

The surface transit network (streetcar + bus) complements the metro (9 lines, radial from Sant Cristòfor Grand Train Terminal) and ferries (8 routes across the bay). The hierarchy is:

1. **Metro** — backbone, high-capacity, radial from Sant Cristòfor Grand Train Terminal
2. **Streetcar** — medium-capacity commuter corridors in dense ciutats, key transport hub connections
3. **Bus** — flexible coverage, cross-town connections, low-density areas, night service
4. **Ferry** — cross-bay connections (no alternative for Barcelona peninsula)

## Streetcar Network

The streetcar system has three lines, each with a distinct character. The original private tramways were absorbed into the metro system in 1964, but the streetcar lines were retained and upgraded rather than closed.

### Line T1 — Original (LRV)
- **Route**: Sant Cristòfor Grand Train Terminal → Original bay shore → financial district → Carrer del Canal → Original southern neighbourhoods
- **Character**: Full commuter service, upgraded to modern LRVs in the 2000s. Connects the three major transport hubs (Sant Cristòfor Grand Train Terminal, ferry terminal, financial district) through the narrow streets of the historic core where metro stations are too far apart. High frequency (4 min peak). Carries approximately 95,000 passengers daily.
- **Role**: The T1 is the spine of Original's surface transport. It serves the financial sector lunch rush, the cafeteria halls, and the dense residential neighbourhoods of the southern districts. It connects directly to the ferry terminal at Sant Cristòfor Main, making it the primary last-mile connection for ferry passengers heading into the city centre.

### Line T2 — Barcelona (LRV)
- **Route**: Pandao ferry terminal → Barcelona centre → Pandao neighbourhoods → El Fort ferry terminal
- **Character**: Full commuter service, upgraded to modern LRVs in the 2010s. The T2 is critical infrastructure for Barcelona — with no metro crossing of the bay, the streetcar provides the primary north-south spine along the peninsula, connecting the two major ferry terminals (Pandao and El Fort) and serving the dense residential core. High frequency (5 min peak). Carries approximately 110,000 passengers daily — the highest-ridership streetcar line in the city.
- **Role**: The T2 is Barcelona's lifeline. It connects the ferry terminals to the residential neighbourhoods, the commercial centre, and the community facilities of the peninsula. Without it, Barcelona's 732,000 residents would rely entirely on buses for internal circulation. The LRV upgrade was prioritised because of the line's importance to peninsula commuters.

### Line T3 — Costa Nord (mixed historic + LRV)
- **Route**: Costa Nord waterfront → studio district → Els Aiguamolls border
- **Character**: Mixed fleet — the northern section (waterfront to studio district) operates modern LRVs for commuter service, while the southern section (studio district to Els Aiguamolls) retains historic heritage trams as a tourist and cultural attraction. The heritage section runs at lower frequency and is popular with visitors to the Costa Nord media district. Carries approximately 45,000 passengers daily (35K LRV, 10K heritage).
- **Role**: The T3 serves a dual purpose. The LRV section provides genuine commuter service for the media industry workforce — connecting studios, production houses, and post-production facilities along the waterfront. The heritage section is a cultural amenity, preserving the original tram infrastructure that served the area during the Shining Star era. The mixed operation is unusual but reflects Costa Nord's identity as both a working media district and a tourist destination.

## Bus Network

The bus network complements the metro and streetcar with surface-level routes covering the entire metropolitan area.

### Design Principles
1. Cross-town connections between radial metro lines
2. Coverage of low-density outer ciutats where metro doesn't reach
3. Feeder service to metro and streetcar terminals
4. Night service when metro and streetcar close
5. Industrial area and airport connections

### Ciutat Analysis

#### High-density urban core (metro + streetcar + bus feeders)
- **Original** (731K, 8,811/km²) — dense core, narrow streets. Metro + T1 streetcar primary. Bus serves as cross-town and feeder to metro stations. Heavy bus usage for cafeteria hall lunch rush, financial district commuters.
- **Barcelona** (732K, 10,605/km²) — densest, peninsula. No metro crossing of bay. Ferry + T2 streetcar primary for internal circulation. Bus supplements streetcar with east-west cross-peninsula routes and connections to less-served neighbourhoods.
- **Dàrsena** (575K, 3,803/km²) — nightlife, warehouses. Metro serves east-west. Bus serves north-south connections, nightlife district circulation (late night when metro closes). Sòtol gay village.

#### Medium-density urban (metro + bus primary)
- **Costa Nord** (580K, 3,742/km²) — affluent, media industry. Metro along coast + T3 streetcar along waterfront. Bus serves interior routes, studio/production house connections, north-south.
- **Sant Llorenç** (540K, 3,777/km²) — working class, industrial. Metro serves main corridors. Bus serves industrial areas, residential feeders, cross-town.
- **Sant Jordi** (461K, 2,214/km²) — residential. Metro through centre. Bus serves residential streets, cross-town.

#### Low-density suburban (bus primary, limited metro)
- **Sant Martí** (435K, 1,204/km²) — airport, suburban. Metro Line 1 + 9 serve airport corridor. Bus essential for rest of ciutat — residential areas, commercial strips.
- **Ciutat de l'Estació** (376K, 1,205/km²) — railyard, former airport. Metro serves main corridor. Bus serves residential areas, railyard workers.
- **Mare de Déu del Mar** (232K, 915/km²) — beaches, coastal. Limited metro. Bus primary — coastal route, beach connections, residential.
- **Sant Miquel** (230K, 800/km²) — foothills, affluent. No metro. Bus primary — hill routes, connections to metro terminals.
- **Ciutat del Pujol** (266K, 506/km²) — foothills, lowest density. No metro. Bus primary — limited routes, connections to metro terminals.

### Bus Route Categories

#### 1. Trunk routes (high-frequency, main corridors)
- Cross-town east-west corridors connecting metro lines
- North-south corridors along major avenues
- Peninsula cross-connections supplementing T2 streetcar
- Airport express (limited stops)

#### 2. Standard routes (regular frequency, residential coverage)
- Ciutat internal circulation
- Metro feeder routes
- Industrial area services

#### 3. Night routes (late night, nightlife areas)
- Dàrsena nightlife circuit
- Sòtol connections
- Weekend beach routes

#### 4. Hill routes (Sant Miquel, Ciutat del Pujol)
- Steep terrain, smaller vehicles
- Limited frequency
- Connect to metro terminals at base of hills

### Estimated Ridership by Ciutat

| Ciutat | Daily bus riders | % of total | Notes |
|--------|-----------------|------------|-------|
| Original | 150,000 | 18.8% | Cross-town + financial district feeders (T1 absorbs some) |
| Barcelona | 120,000 | 15.0% | Supplements T2 streetcar, east-west cross-peninsula |
| Dàrsena | 90,000 | 11.3% | Nightlife, cross-town |
| Costa Nord | 70,000 | 8.8% | Interior routes (T3 absorbs waterfront) |
| Sant Llorenç | 70,000 | 8.8% | Industrial, working class |
| Sant Martí | 65,000 | 8.1% | Airport area, suburban |
| Sant Jordi | 55,000 | 6.9% | Residential feeders |
| Ciutat de l'Estació | 45,000 | 5.6% | Railyard, residential |
| Mare de Déu del Mar | 35,000 | 4.4% | Coastal, beach routes |
| Sant Miquel | 25,000 | 3.1% | Hill routes, low density |
| Ciutat del Pujol | 20,000 | 2.5% | Hill routes, lowest density |
| **Total** | **800,000** | **100%** | |

Note: Original and Barcelona bus ridership is lower than it would be without streetcars, since T1 and T2 absorb significant commuter demand. Costa Nord bus ridership is similarly reduced by T3.

### Key Route Design

#### Peninsula routes (Barcelona) — supplementing T2
- **B1**: Platja de Jordi → Barcelona centre → northern Barcelona (east-west, supplements T2's north-south spine)
- **B2**: Pandao neighbourhoods → El Fort neighbourhoods (cross-peninsula)
- **B3**: Circular peninsula route connecting ferry terminals (supplements ferry Route O)

#### Cross-town routes
- **C1**: Costa Nord → Original → Dàrsena → Sant Llorenç (east-west, northern)
- **C2**: Mare de Déu del Mar → Sant Jordi → Original → Sant Llorenç (east-west, central)
- **C3**: Sant Martí → Ciutat de l'Estació → Original (east-west, southern)

#### North-south corridors
- **N1**: Costa Nord → Sant Jordi → Sant Martí (western)
- **N2**: Sant Miquel → Dàrsena → Original (central)
- **N3**: Ciutat del Pujol → Sant Llorenç → Ciutat de l'Estació (eastern)

#### Hill routes
- **H1**: Metro terminal → Sant Miquel (foothill loop)
- **H2**: Metro terminal → Ciutat del Pujol (foothill loop)

#### Night routes
- **N1**: Dàrsena nightlife circuit (Sòtol, clubs, warehouse district)
- **N2**: Original → Dàrsena → Barcelona late-night connector

#### Airport
- **A1**: Airport express — Sant Cristòfor Grand Train Terminal → Airport (limited stops)

## Total Daily Surface Transit Ridership

| Mode | Daily ridership | Notes |
|------|----------------|-------|
| Metro | 2,100,000 | 9 lines, backbone |
| Streetcar | 250,000 | T1 (95K) + T2 (110K) + T3 (45K) |
| Bus | 800,000 | Full network coverage |
| Ferry | 118,500 | 8 routes, bay crossings |
| **Total** | **3,268,500** | |
