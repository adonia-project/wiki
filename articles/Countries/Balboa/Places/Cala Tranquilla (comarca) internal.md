# Cala Tranquilla (comarca) — Internal Notes

## Source Data

### GIS Data (authoritative)
- **Shapefile**: `/Users/shubhamnaik/Developer/adonia-gis/Tramuntana.shp` (EPSG:4326)
- **Comarca ID**: 7
- **Name**: Cala Tranquilla
- **Capital**: Portblanc
- **Population**: 648,247
- **Notes**: Provincial capital, E1/E2/E8/E116
- **Area**: 1,285.4 km² (calculated from shapefile via EPSG:6933 equal-area projection)
- **Bounds**: W=-94.2975, S=6.2771, E=-93.8549, N=6.6527
- **Centroid**: (-94.0900, 6.4450)
- **Coastline**: ~27 km on Shendan Ocean (western boundary)
- **N-S extent**: ~41.7 km
- **E-W extent**: ~45.2 km

### Neighbors (from shapefile)
- **La Cruïlla** (east) — touches, capital Sant Antoni
- **El Mas** (south) — touches, capital El Mas
- **Cala Negra** (offshore west) — MultiPolygon (island comarca), distance=0, E2

### POIs within comarca (from Points of Interest.shp)
- Portblanc Military Academy (at ~6°27'N, 94°12'W)
- Portblanc Airport (at ~6°34'N, 94°08'W)

### Expressways through comarca (from Balboa Expressways.shp)
- E1, E2, E8, E116 (all confirmed in GIS)

### Railroads through comarca (from baboa_railroads.shp)
- Portblanc Subdivision

### Tramuntana Province table (from Tramuntana Province article)
- Area: 1,286 km², Population: 648,247, Density: 504.1/km², Coast: Shendan

## Cross-References Consulted

1. **Portblanc.mediawiki** — main city article; geography, history, economy, demographics, government, education, transport sections all referenced
2. **Tramuntana Province.mediawiki** — comarca table, provincial context
3. **Sant Cristòfor (comarca).mediawiki** — format reference for comarca article
4. **La Serra de Llevant.mediawiki** — format reference for Tramuntana comarca article
5. **Portblanc Airport.mediawiki** — airport details
6. **2024 Portblanc fires.mediawiki** — fire event details
7. **2026 Portblanc fires.mediawiki** — fire event details
8. **Portblanc internal.md** — internal notes for Portblanc article

## Invented Details (flagged for review)

1. **Etymology**: "Cala Tranquilla" = Volisanian for "quiet cove" or "tranquil bay" — plausible given Volisanian naming conventions (cala = cove, tranquilla = quiet/tranquil), but user has not confirmed this etymology
2. **Rural population figure**: Listed as "~–32,000" — this is a residual calculation (648,247 comarca - 680,000 city = negative, which means city boundary extends beyond comarca). This is awkward. The actual rural population should be positive. The issue is that Portblanc city (680k) is larger than the comarca (648k). This likely means the city population figure includes areas outside the comarca, or the comarca population includes some areas not counted in the city. The settlement table notes this discrepancy. User should clarify.
3. **Comarca commissioner**: No name invented — left blank as with La Serra de Llevant
4. **Municipalities**: Number left blank — user has not specified how many municipalities the comarca contains
5. **Coastline length**: ~27 km — estimated from shapefile western boundary coordinates, approximate

## Open Questions

1. Is the etymology "quiet cove" correct?
2. How many municipalities does Cala Tranquilla contain? Is Portblanc the only one?
3. The population discrepancy (city 680k > comarca 648k) — should the city population be revised down, or the comarca population up?
4. What is the comarca commissioner's name?
5. Should there be a Tramuntana Province comarcas nav template (similar to {{Estret Province comarcas}})?
6. Are there any smaller settlements in the comarca besides Portblanc that should be named?
7. Does the comarca include any of the offshore islands, or is Cala Negra entirely separate?

## File
- `articles/Countries/Balboa/Places/Cala Tranquilla (comarca).mediawiki` — wiki article
- `articles/Countries/Balboa/Places/Cala Tranquilla (comarca) internal.md` — this file
