# Line F (CristoCarril) — Internal Notes

## Overview
- Sixth CristoCarril line, operates on the Old Grand Subdivision corridor
- 13 stations, 85.4 km total length
- ~18,300 daily ridership (2025)
- Runs from Sant Cristòfor Central Terminal to L'Estany (Ciutat del Llac Sud municipality, L'Estany comarca)
- Restricted to 2-car train formations due to steep gradients and tight curve radii on the switchback section
- Maximum speed: 80 km/h (lowest of any CristoCarril line)

## Route Summary
- Stations 1-4: Shared with Lines B, C, D, E — on Sant Bart Line corridor through Original ciutat
- Station 5: Mas Blanc — shared with D, E — Sant Bart Line / Old Grand Subdivision junction in Sant Jordi
- Stations 6-10: Shared with Line D only — on Old Grand Subdivision through central Sant Jordi
- Stations 11-13: F-exclusive — on Old Grand Subdivision through switchback section into L'Estany comarca

## Branch Point
Line F diverges from Line D at Polígon Sud (station 10). Line D continues to Riera Seca then diverges onto the Via Sud Subdivision toward Ciutat del Pujol and Cumará. Line F continues east on the Old Grand Subdivision through the switchback section.

## F-Exclusive Stations (invented names)
| # | Name | Coordinates | Comarca | Municipality | km from Mas Blanc | km from CT |
|---|------|-------------|--------|--------------|-------------------|------------|
| 11 | La Colònia | (-94.13, 0.58) | Sant Cristòfor | Sant Jordi | 23.1 | 31.0 |
| 12 | Coll Alt | (-94.06, 0.58) | Sant Cristòfor | Sant Jordi | 44.7 | 52.6 |
| 13 | L'Estany | (-93.98, 0.72) | L'Estany | Ciutat del Llac Sud | 77.5 | 85.4 |

### Naming Rationale
- **La Colònia** ("The Colony"): Former industrial workers' colony at the eastern edge of Sant Jordi, where the switchbacks begin. Suggests a historical industrial settlement that has been absorbed into the Sant Cristòfor metropolitan area.
- **Coll Alt** ("High Pass"): Mountain pass station at the highest point on the line, in the middle of the switchback section. Named to distinguish from the El Coll stations in Portnou (El Coll on Line B, El Coll Oest on Line A). The name directly describes the topographic feature — a high mountain pass. Coll Alt is the highest elevated station in the entire CristoCarril system. The platform offers a panoramic view overlooking Sant Cristòfor and the coastal plain below. After Coll Alt, the line enters the Sant Cristòfor–L'Estany Rail Tunnel, which carries it through the Serralada d'Estret into the L'Estany comarca.
- **L'Estany** ("The Lake"): Terminus station in the municipality of Ciutat del Llac Sud, serving the lakeside resort community near the Estany de Panacú. Named after the comarca/municipality, consistent with other terminus stations (Els Camps, Brises).

## Switchback Section
The Old Grand Subdivision east of Polígon Sud features numerous switchbacks as it climbs from the coastal plain (around 0.58° latitude) into the interior highlands of Estret Province. The direct distance from Polígon Sud to L'Estany is approximately 40 km, but the track length is approximately 60 km due to the switchbacks. Key switchback points are at approximately km 34, 55, and 70 along the Old Grand (measured from Mas Blanc). The steep gradients and tight curve radii restrict trains to 2-car formations only.

## Sant Cristòfor–L'Estany Rail Tunnel
After Coll Alt (the highest elevated CC station), the line enters the Sant Cristòfor–L'Estany Rail Tunnel, bored through the Serralada d'Estret. The tunnel carries the line beneath the highland divide from Sant Cristòfor comarca into L'Estany comarca. Upon emerging, the line descends toward the Estany de Panacú lowlands and the terminus at L'Estany station in Ciutat del Llac Sud.

## GIS Data
- POI shapefile route field: "CC Line F" identifies 13 stations
- Old Grand Subdivision shapefile: 132 points, 77.6 km total length, starts at (-94.33, 0.61), ends at (-93.98, 0.72)
- Switchbacks concentrated in eastern half (points 60-131)
- Via Sud Subdivision branches off Old Grand at approximately km 19.6 (point 25) — this is where Line D diverges

## Service Patterns
- **Express**: Stops 1, 2, 10, 13 (Central Terminal, Portal, Polígon Sud, L'Estany), ~75 min — skips all intermediate stations including entire switchback section
- **Local**: All 13 stations, ~100 min — only service to La Colònia and Coll Alt
- NO short service — Line F does not operate a short-turn service within Sant Cristòfor

## Ridership Estimates
- Shared stations (1-10): Lower than Line D since Line F is less frequent and uses 2-car trains. Total ~15,300.
- F-exclusive stations: La Colònia 500, Coll Alt 300, L'Estany 1,600. Total ~2,400.
- Grand total: ~18,300.
- L'Estany terminus has relatively high boardings (1,600) due to serving as the primary rail connection for the L'Estany comarca resort communities.

## Speed
- Maximum speed: 80 km/h (lower than Line D's 120 km/h due to switchback curves)
- Average speed (local): ~51 km/h (85.4 km / 100 min)
- Average speed (express): ~68 km/h (85.4 km / 75 min)

## Open Questions
1. Are La Colònia and Coll Alt in Sant Jordi ciutat or in a separate/unincorporated area of Sant Cristòfor comarca? Currently assigned to Sant Jordi based on the Original (ciutat) article's description of Line F going "Original–Sant Jordi".
2. Should the L'Estany station article be named "L'Estany (CristoCarril)" to disambiguate from the comarca, municipality, and airport? Yes — following the pattern of other CristoCarril station articles.
3. Precise track distances for F-exclusive stations need verification against more detailed track geometry. Current distances are estimated from POI projections onto the Old Grand Subdivision line geometry.
4. Ciutat del Llac Sud — is this a new municipality that needs its own article? No existing wiki article found as of 2026-09-02.
5. Does Line F connect to L'Estany Airport? The airport article mentions it's served by Aeroístmus from Sant Bart. No rail connection mentioned. The Line F terminus is in Ciutat del Llac Sud, which may or may not be near the airport. GIS shows the airport is ~23 km from the F terminus station.

## File
- `articles/Countries/Balboa/Infrastructure/Line F (CristoCarril).mediawiki` — wiki article
