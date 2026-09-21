# Administrative divisions of Balboa — Internal Notes

## Article Structure
- **Infobox**: `{{Infobox political system}}` with country, government type, levels, province/comarca counts, largest/smallest/most/least populated
- **Lead**: Overview of four-level system, unitary state framework, constitutional basis
- **Structure**: Table showing all four levels with native names, heads, legislatures, constituencies
- **Provinces**: Summary table with all 5 provinces, provincial powers, current governors
- **Comarcas**: Summary by province with comarca counts, totals, largest/smallest; per-province descriptions
- **Municipalitats**: Basic description of the municipal level
- **Ciutats and districtes**: General description + Sant Cristòfor ciutat-districte system with full 11-ciutat table
- **International City of Areza**: Special status section
- **Electoral system**: STV, concurrent elections, Third Guarantee
- **Historical development**: 1974 constitution, reunification context
- **See also**: Related articles

## Data Sources
- **Politics of Balboa** — Province table, local government section, electoral system details
- **Government of Balboa** — Local government section, judicial organisation by province/comarca
- **Tramuntana Province article** — 27 comarcas, area 109,965 km², pop 1,900,000, governor Lluís Vidal i Soler (Liberal)
- **Estret Province article** — 13 comarcas, area 20,600 km², pop 14,500,000
- **Jala Province article** — 22 comarcas, area 65,977 km², pop 8,500,000, governor Gaspar Mas i Bonet (BPP)
- **Sant Cristofor ciutats internal.md** — 11 ciutats with population, area, density, character
- **GIS shapefiles** (source of truth for boundaries):
  - Tramuntana.shp: 27 comarcas (GIS area: 109,881 km²)
  - Nurra.shp: 25 comarcas (GIS area: 70,380 km²)
  - Jala.shp: 35 features, 22 non-null comarcas (GIS area: 65,539 km²)
  - Migjorn.shp: 19 comarcas (GIS area: 30,539 km²)
  - Balboa.shp: 13 comarcas = Estret (GIS area: 19,096 km²)

## Area Discrepancies
- All province areas updated to GIS-computed values (EPSG:6933 equal-area projection) per user instruction to "follow GIS."
- **Tramuntana**: GIS 109,881 km² (article had 109,965)
- **Nurra**: GIS 70,380 km² (article had 70,753)
- **Jala**: GIS 65,539 km² (article had 65,977)
- **Estret**: GIS 19,096 km² (article had 20,600; difference likely Areza enclave)
- **Migjorn**: GIS 30,539 km² (article had 26,909; significant difference, GIS may include water or different boundaries)
- **Total**: GIS sum 295,435 km²

## Comarca Counts
- Tramuntana: 27 (confirmed by article and shapefile)
- Nurra: 25 (from shapefile; no province article exists yet)
- Jala: 22 (confirmed by article and shapefile — 35 features but 13 have null names, leaving 22 actual comarcas)
- Estret: 13 (confirmed by article and shapefile)
- Migjorn: 19 (from shapefile; no province article exists yet)
- Total: 106

## Population Data
- Populations made "noisy" (realistic census-style figures) per user request, summing to 35,234,000 (country total).
- Tramuntana: 1,873,412
- Nurra: 4,487,219
- Jala: 8,514,902
- Estret: 14,523,847
- Migjorn: 5,834,620
- Total: 35,234,000

## Provincial Governors
- Tramuntana: Lluís Vidal i Soler (Liberal) — from Tramuntana Province article
- Jala: Gaspar Mas i Bonet (BPP) — from Jala Province article
- Nurra, Estret, Migjorn: Not yet documented in existing articles. Left as "—" in the table.

## Sant Cristòfor Ciutat Data
- 11 ciutats with total population 5,159,000 and total area 2,550 km²
- Data from Sant Cristofor ciutats internal.md (derived from San Cristofer.shp shapefile)
- The Municipalitat de les Illes is separate from the ciutat structure

## Open Questions
1. What are the names and parties of the governors of Nurra, Estret, and Migjorn?
2. Should the Migjorn area discrepancy (26,909 vs 30,539 km²) be investigated?
3. Should the Estret area figure (20,600 km²) include or exclude Areza?
4. How many municipalitats are there in total in Balboa?
5. What is the exact population of each Migjorn comarca? (Shapefile has no population data for Migjorn)
6. What is the exact population of each Estret comarca? (Shapefile has no population data for Estret)
7. Are there any other cities besides Sant Cristòfor that use the ciutat-districte system? (Article says no, but Portnou and Sant Bart may have districte systems)
8. What are the exact terms of office for each level? (4 years confirmed but term limits vary)
9. Should a "Provinces of Balboa" redirect/article be created, or does it redirect to this article?
10. Should a "Comarcas of Balboa" article be created as a list of all 106 comarcas?

## Links to Create
- [[Provinces of Balboa]] — may redirect to this article or be a separate list
- [[Comarcas of Balboa]] — may redirect to this article or be a separate list
- [[Municipalitats of Balboa]] — may redirect to this article or be a separate list
