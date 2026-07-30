# Guajicutea — Internal Notes

## Overview
Island nation in the Capuyaquiran Sea on the planet Adonia. Two islands: one large, one small islet ~38 km to the west. Total area ~3,278 km². Equatorial latitude (5.5°–6.5°). Guajicutea sits between two archipelago clusters — the Lesser Capuyaquiran (west) and the Greater Capuyaquiran (east) — and is the only large N-S oriented island in an island chain that otherwise trends E-W. Climate, population, government, culture — all TBD.

---

## Geography — Working Notes

### GIS Data (from QGIS shapefile: adonia-gis/Guajicutea.shp)

#### Main Island (Island 1)
- **Area**: ~3,253 km²
- **Dimensions**: ~57 km (E-W) × ~106 km (N-S)
- **Orientation**: Elongated north-south
- **BBox**: lon [−83.1998, −82.6827], lat [5.5503, 6.5063]
- **North tip**: (−83.0842, 6.5063)
- **South tip**: (−82.7694, 5.5503)
- **East tip**: (−82.6827, 5.6860)
- **West tip**: (−83.1998, 6.1685)
- **Coastline points**: 409

#### Small Islet (Island 0)
- **Area**: ~25 km²
- **Dimensions**: ~6 km × ~6 km (roughly oval)
- **BBox**: lon [−83.3975, −83.3404], lat [5.6008, 5.6532]
- **Centroid**: (−83.3742, 5.6246)
- **Coastline points**: 41

#### Inter-island distance
- **Closest points**: ~38.4 km
- **Centroid-to-centroid**: ~65.1 km
- The islet sits WSW of the main island's southern third

### Coastline Analysis (Main Island)

The main island has a complex, asymmetric coastline:

**North coast** (points 0–20): Broad, gently curving arc from NW to NE. Relatively smooth. The northernmost point is at (−83.0842, 6.5063). This is the widest part of the island laterally.

**Northeast coast** (points 20–40): Curves southeast from the north tip. Relatively smooth descent. Coastline trends from N to SE.

**East coast — upper** (points 40–113): Long, relatively smooth SE descent from ~lat 6.38 to ~lat 5.97. This is the longest relatively straight stretch of coastline — roughly 45 km of coast running N-S to NNE-SSW.

**East coast — indentation** (points 113–140): Significant inward curve starting around (−82.7044, 5.9581). The coastline dips westward, creating a broad bay/embayment. The indentation is most pronounced around points 114–140 (lat 5.96–5.81). The coast curves back east around point 160 (−82.6993, 5.7533). This embayment spans roughly 15 km of latitude and creates a natural harbor opportunity. **PROPOSED: This is the main harbor/bay where the capital port is located.**

**Southeast coast** (points 160–192): Curves from the embayment around to the south tip. The south tip (−82.7694, 5.5503) is a relatively sharp point.

**Southwest coast** (points 192–260): Curves NW from the south tip. Relatively smooth, gentle concavity. Coastline trends from S to NW.

**West coast — lower** (points 260–345): Complex coastline with multiple small indentations and protrusions. Notable features:
- Points 277–291: Inward curve around (−83.027, 5.88) — a smaller bay/indentation on the west coast
- Points 300–310: Another subtle indentation around (−83.08, 5.89)
- Point 345: Westernmost point (−83.1998, 6.1685) — a pronounced western bulge/protrusion in the northwestern part of the island

**Northwest coast** (points 345–408): Curves from the western bulge back to the north tip. Complex, with the coastline bulging westward around lat 6.17, then curving back NE to close the island at the north tip.

### Proposed Geographic Names (PLACEHOLDER — user to confirm or replace)

These are working labels for reference in internal notes. All subject to change once cultural/naming direction is established.

- **Main Island**: "Guajicutea Island" (placeholder) — or a distinct name
- **Small Islet**: "Cay [TBD]" or a proper name — 25 km² is too large for a typical "cay" but the term might still apply culturally
- **East coast embayment** (points 113–140): "Capital Bay" (placeholder) — the main natural harbor
- **West coast indentation** (points 277–291): "[TBD] Bay" — secondary harbor on west coast
- **Western bulge** (point 345): "[TBD] Peninsula" — the NW protrusion

### Terrain (PROPOSED — user to confirm)

At ~3,253 km² and equatorial latitude, the main island is large enough to support significant elevation. Options:

**Option A: Volcanic origin (recommended)**
- The island is a volcanic island (or cluster of overlapping volcanic centers), similar to e.g. Réunion, Mauritius, or the Galápagos
- Interior highlands with volcanic peaks reaching 1,500–2,500m
- Coastal lowlands narrowing to plains in some areas
- Volcanic soils support agriculture
- Possible active/dormant volcano as a geographic landmark
- Rivers radiating from central highlands to the coast
- Coral reefs fringing parts of the coastline (especially the east coast embayment)

**Option B: Coral atoll / raised limestone**
- Low-lying, max elevation <100m
- Less likely given the island's size — 3,253 km² is very large for a pure coral island
- Could be a mix: volcanic core with limestone fringing

**Option C: Continental fragment**
- The island is a continental fragment that broke off from a nearby landmass
- More varied geology: sedimentary, metamorphic, some volcanic
- Less dramatic elevation but still hilly interior

### Climate (PROPOSED — user to confirm)

At 5.5°–6.5° latitude, the island is firmly in the equatorial zone.

**Equatorial rainforest climate (Af in Köppen)**
- Temperature: 24–30°C year-round, minimal seasonal variation
- Humidity: High (80–90%) year-round
- Rainfall: 2,500–4,000 mm/year, distributed relatively evenly (no true dry season, but possible wetter/drier periods)
- Two rainfall peaks around the equinoxes (March–April and September–October) — typical of inner-tropical climates
- If interior elevation is significant (1,500m+), highland climate would be cooler (18–22°C) and wetter (orographic precipitation)
- Tropical storms/cyclones: At 5.5–6.5°, the island is very close to the equator — cyclone formation is rare within 5° of the equator, but possible at the northern edge (6.5°). Occasional tropical depressions possible but not a dominant feature.
- ENSO variability: El Niño years may bring drier conditions; La Niña wetter

### Biogeography (PROPOSED — user to confirm)

- **Lowland tropical rainforest**: Original vegetation cover. High biodiversity, endemism expected on an isolated oceanic island
- **Montane forest / cloud forest**: If elevation >1,200m, transition to montane forest with cooler temperatures and persistent mist
- **Coastal mangroves**: Estuarine areas, especially around river mouths and the embayment
- **Coral reefs**: Fringing reefs, especially on leeward (western) coast and around the small islet
- **Endemism**: As an oceanic island, expect high endemism — unique bird species, reptiles, plants. Level of endemism depends on island age and isolation.
- **Small islet**: Possible seabird colony, turtle nesting site, or uninhabited nature reserve

### Rivers & Watershed (PROPOSED — to be developed)

If volcanic with central highlands:
- Multiple short rivers radiating from interior highlands to the coast
- Longest river probably 30–40 km (island is only 57 km wide)
- Principal rivers would flow to the east coast (toward the embayment) and to the west/southwest coast
- Waterfalls in the interior highlands
- Freshwater availability not a problem given equatorial rainfall

### Archipelago Context (from Adonia 2026 Shape File REHASHED.shp)

Guajicutea is part of a larger island chain spanning roughly lon −100 to −70, lat −4 to 11, all within the Capuyaquiran Sea. The chain has two main clusters with Guajicutea sitting between them:

#### Lesser Capuyaquiran Archipelago (western cluster, lon −100 to −95)
- ~17 islands >5 km², total ~857 km²
- Mostly E-W oriented islands (10 of 17 have aspect ratio <0.7, meaning wider than tall)
- Largest islands: 200 km² (99×47 km, E-W), 289 km² (86×53 km, E-W), 127 km² (55×32 km, E-W)
- Latitude range: ~4.6–6.9 (concentrated around 5–6°)
- The dominant E-W orientation suggests these islands formed along an E-W trending tectonic feature

#### Greater Capuyaquiran Archipelago (eastern cluster, lon −75 to −70)
- ~14 islands >5 km², total ~1,031 km²
- Mixed orientation but predominantly E-W (largest islands: 306 km² at 65×74 km, 316 km² at 81×54 km E-W, 100 km² at 65×29 km E-W)
- Latitude range: ~3.5–10.7
- Also E-W dominant, consistent with the same regional tectonic trend

#### Central Capuyaquiran Sea (lon −95 to −75, between the two clusters)
- Scattered smaller islands, ~58 islands >5 km²
- Guajicutea (323 km², 47×102 km) is by far the largest island in this central zone
- Most central islands are small (5–60 km²) and roughly circular
- A few N-S oriented islands exist here (e.g. 32 km² at 20×39 km, 60 km² at 18×36 km, 35 km² at 18×43 km) — but Guajicutea is the only LARGE N-S oriented island

#### Key observation: Guajicutea's anomalous orientation
- Aspect ratio 2.19 (N-S) — the most elongated N-S island in the entire chain
- All other large islands (>100 km²) in the chain have E-W or round orientation
- The nearest large N-S oriented island is 35 km² at (−85.27, 6.28) — 18×43 km, about 250 km to the west
- This N-S orientation is the central tectonic puzzle

### Tectonic Theory (CONFIRMED: convergent boundary + slab tear)

The Capuyaquiran island chain is a volcanic arc above an E-W trending subduction zone where two plates converge:

- **North plate**: Abyalan plate (overriding)
- **South plate**: Capuyaquiran plate (subducting northward under the Abyalan plate)
- The volcanic arc (Lesser and Greater Capuyaquiran archipelagos) forms on the Abyalan plate side, trending E-W along the boundary
- The Capuyaquiran Sea is the back-arc basin between the arc and the Abyalan mainland to the north (or the fore-arc / inter-arc basin — TBD)

#### The N-S fracture zone (slab tear)

A N-S trending fracture zone cuts through the subducting Capuyaquiran plate at approximately lon −83°. This is a **slab tear** — a rupture in the subducting plate that allows decompression melting and enhanced magma ascent.

Where the slab tear intersects the subduction zone, it produces more voluminous magmatism than the rest of the arc. This is why:
1. Guajicutea is the largest island in the central zone — the tear feeds more magma
2. Guajicutea is oriented N-S — the volcanic complex aligns along the tear rather than along the arc
3. Guajicutea sits in the gap between the two archipelago clusters — the tear disrupts the continuity of the arc, creating a magmatic gap to either side
4. The small islet (25 km², 38 km WSW) is a satellite vent on the same fracture system — the tear extends further west but only produced enough magma for a small edifice

Real-world analogue: the Galápagos Islands, where the Wolf-Darwin lineament (a fracture zone) produces N-S aligned volcanoes perpendicular to the main E-W hotspot track. Closer analogue: the Panamanian slab tear, where a tear in the subducting plate produces distinct volcanic patterns.

#### Tectonic Features for QGIS Plotting
1. **E-W subduction zone**: A line through the centers of the Lesser and Greater Capuyaquiran clusters (approximately along lat ~5–6°). Trench would be south of the arc (on the Capuyaquiran plate side).
2. **N-S slab tear / fracture zone**: A line through Guajicutea's long axis (approximately along lon ~−83°). Should extend north and south of Guajicutea.
3. **Subduction direction**: Capuyaquiran plate moving north, subducting under Abyalan plate
4. **Volcanic arc position**: Islands sit on the Abyalan plate, ~100-200 km north of the trench
5. **Slab tear extent**: The fracture zone likely extends south into the Capuyaquiran plate and north into the mantle wedge under the Abyalan plate

### Open Questions
1. **Terrain type**: Volcanic — confirmed by tectonic setting (slab tear magmatism)
2. **Max elevation**: How high should the interior be? (1,500–2,500m proposed)
3. **Active volcano**: Should there be an active/dormant volcano on the slab tear?
4. **Slab tear name**: What should the N-S fracture zone be called?
5. **Small islet**: Inhabited? Nature reserve? Satellite volcanic vent on the tear?
6. **Coral reefs**: Should the island have significant reef systems?
7. **Naming conventions**: What language/culture should geographic names follow?
8. **Climate refinement**: Any reason to deviate from standard equatorial rainforest?
9. **Back-arc or fore-arc**: Is the Capuyaquiran Sea a back-arc basin (behind the arc, on the Abyalan side) or fore-arc (between trench and arc)?
10. **Abyalan mainland**: Is there a continental landmass to the north on the Abyalan plate?

---

## Files
- `articles/Countries/Guajicutea/Guajicutea internal.md` — this file
- `articles/Countries/Guajicutea/Guajicutea.mediawiki` — main country article (to be created)
