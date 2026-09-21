# Geography of Sinchew — internal notes

Working notes begun 2026-09-19. Terrain, physiographic regions, and tectonics.

Related: `Climate of Sinchew.mediawiki` (published), `Native peoples of Sinchew internal.md` (peoples, deferred), agent memory `reference/sinchew_gis.md` (full technical record).

---

## 1. The DEM — which file to use

Three DEMs exist in `/Users/shubhamnaik/Developer/adonia-gis/`. **They differ and it matters which you use.**

| File | What it is | Use for |
|---|---|---|
| `Sinchew_DEM_burned.tif` | The original painted DEM, rivers burned in. **A staircase** — elevation quantised into ~13 discrete bands (0–50, 50–100, 150–200, 300–350, 500–550, 600–650 m and up). | The climate model currently reads this by default |
| `Sinchew_DEM_filled.tif` | **The finished terrain.** Despeckled, Gaussian-smoothed (σ8 = 1.8 km), fractal variation added, closed depressions filled. | **Terrain description, hydrology, anything geometric** |

Outputs and artefacts: `Sinchew_physiographic_regions.geojson` (30 regions), `physio_climate_regions.json` (region table), `Sinchew_DEM_filled_compare.png`, `Sinchew_DEM_filled_zoom.png`.

### Why the rebuild was needed
The painted DEM is a step function, so every band edge is a 250 m cliff inside one 223 m cell. Consequences: slope statistics are meaningless, rivers run across dead-flat ground with no gradient, and the climate model grew rain bands tracing the paint edges.

Rebuild pipeline (`rebuild_sinchew_dem_continuous.py`, `fill_dem_depressions.py`):
1. **Despeckle** — 34,496 isolated outlier cells (>50 m from both 3×3 and 5×5 median) replaced with the local median.
2. **Gaussian smooth** σ8 (1.8 km). This is what turns the staircase into ramps.
3. **Fractal variation** — summed random fields at scales from ~21 km down to ~1.3 km, amplitude ±60 m, weighted 0.40–1.00 by local relief so lowlands get less but not none.
4. **Depression fill** — priority-flood from the sea on an 8× downsampled grid (block-min), then upsample the fill amount. Removed closed basins created by step 3.

Result: min 2 m, median 319 m, max 2,696 m, max slope 12.7°.

### Caveat the user should know
Because the paint bands are 250 m apart, the smoothed terrain is **gentle** — max slope 12.7°. Real mountains run 20–40°. The rebuilt DEM is continuous but reads as a **gently sloping plateau**, not jagged mountains. Genuine relief would need finer painted input (50 m contours).

### Climate impact: negligible
Ran the model on old vs new DEM: median precip 2,369 → 2,285 mm, driest 795 → 845 mm, every Köppen zone within 1 percentage point. Nothing already written about the climate needs revisiting.

---

## 2. Physiographic regions (30)

Derived by crossing elevation class (6 bands) with Köppen class (6 types), median-filtering, taking connected components, discarding fragments under ~10,000 km², then growing survivors into the gaps so **100% of land is assigned**.

**User verdict:** "looks pretty good" — accepted as the working regionalisation.

Artefact: `Sinchew_physiographic_regions.geojson`, 30 features; properties `id`, `terrain`, `climate`, `km2`.

| id | Terrain | Climate | km² |
|---|---|---|---|
| 17 | Central Plateau | Aw | 358,539 |
| 22 | Upper Uplands | Am | 168,669 |
| 0 | Coastal Lowlands | Af | 166,623 |
| 19 | Uplands | Am | 143,357 |
| 29 | Eastern Highlands | Cfb | 128,326 |
| 18 | Central Plateau | Cfa | 88,926 |
| 12 | Central Plateau | Af | 84,887 |
| 14 | Central Plateau | Am | 84,249 |
| 6 | Lowlands | Af | 75,376 |
| 15 | Central Plateau | Am | 66,955 |
| 7 | Lowlands | Am | 66,525 |
| 1 | Coastal Lowlands | Am | 57,817 |
| …18 more, down to ~11,000 km² | | | |

**Known issue:** the 8,000-cell minimum was too aggressive. It stranded 222,346 km² (10.7%) in 979 fragments — the largest 27,271 km² — which then had to be reassigned arbitrarily. Region 12 grew 31% and region 7 grew 42% when the gaps were filled. A lower threshold (~2,000 cells) would give more honest boundaries at the cost of more regions. **Not yet redone.**

### The dominant geographic facts
- **West→east rise.** Coastal lowlands and lowlands on the western margin; a broad central plateau carrying a third of the country; uplands and highlands stacked along the eastern edge.
- **The north is the lowest part of the country.** Mean elevation by latitude: 38 m at 1–2°S, rising steadily to 548 m at 9–10°S. The upland classes are essentially absent north of 3.5°S.
- **Regions 3–6 form a diagonal stack** running northwest to southeast — the plateau doesn't run straight north–south, it angles.

### Elevation classes (for reference)
| class | area | median lon |
|---|---|---|
| Coastal Lowlands (0–125 m) | 363,786 km² (17.9%) | −110.6 |
| Lowlands (125–260 m) | 255,696 km² (12.5%) | −108.3 |
| Central Plateau (260–430 m) | 680,048 km² (33.4%) | −105.5 |
| Uplands (430–560 m) | 211,240 km² (10.4%) | −99.2 |
| Upper Uplands (560–800 m) | 392,599 km² (19.3%) | −102.4 |
| Eastern Highlands (>800 m) | 127,401 km² (6.3%) | −96.4 |

---

## 3. Tectonics

### What the world already establishes
Source: `articles/unorganized/Adonia.mediawiki`, section "Tectonic plates", and `articles/unorganized/Shendan Ocean.mediawiki`.

- Nine major plates. Named: **Shendan, Lurandian, Fosian, Almurian, Abyalan** — plus three "XXX" placeholders and **"Lurandian" listed twice**. The section is unfinished and needs repair.
- Notable minor plates: Trestan, Xtepla, Keko, Masnorte.
- **The Shendan Plate is among the fastest** (52–69 mm/yr). The Keko Plate is fastest overall (75 mm/yr).
- **The Lurandian Plate is the slowest on Adonia — about 21 mm/yr.**
- The Mariana Trench (10,911 m, deepest on Adonia) lies in the Shendan Ocean. Oldest oceanic crust (~200 myr) is in the Western Shendan.
- The Shendan Ocean is bounded **west by Fosia, east by Lurandia** — so **Lurandia's west coast faces it**. Sinchew is in western Lurandia, so the Shendan–Lurandian plate margin runs along **Sinchew's west coast**, not its east.
- Separate mention: a Pangaean orogenic belt whose strata match the Atlas Mountains in Fosia — the **"Kaskaskian range of Lurandia"**, named exactly once in the wiki with no location or article.

### The model agreed with the user (2026-09-19)

**Sinchew Subplate** — the name. A microplate that has been converging with the main Lurandian Plate. It **extends south across the Sinchew–Louyang border** into part of Louyang, because that border is a perfectly straight artificial line (see below). For the article, describe only the **Sinchew portion**.

**Great Lurandian Mountain Range** — the suture, i.e. the collision boundary between the subplate and the main Lurandian Plate. Runs north–south along Sinchew's eastern edge. This is the renamed "great range in the middle of Lurandia"; Sinchew's highlands are its western flank. **Sinchew's sub-range within it still needs a name.**

Key supporting facts, all from the data:
- The >800 m highland is **one connected belt**, ~614 km long (lat 11.0°S to 5.5°S) and ~250–310 km wide, mean 1,453 m, area 128,437 km².
- The crest curves from lon −93.9 at 2.9°S to −96.6 at 10.1°S; highest point 2,649 m near 8.9°S.
- **The convergence is slow** (Lurandian Plate at 21 mm/yr) — which explains why the range is **subdued and eroded rather than alpine**. One fact explains both its existence and its modest height.
- The range is **intraplate**, so it cannot be an active subduction arc — it must be a relict suture, which fits a collisional origin.

**E–W rift valley (internal to the subplate)** — a failed rift arm within Sinchew, holding the northern long lake. Evidence:
- The northern lake (14,705 km²) is strongly **east–west elongated: 477 km × 144 km (ratio 3.3)**. The other two large lakes run north–south.
- It sits in a **genuine trough**: N–S profile at lon −107.4 shows 576 m at 2.79°S, falling to 139–193 m at the lake, then rising to 587 m at 5.49°S. Higher ground on both sides = trough, not a simple ramp.
- Real-world analogue: the Benue Trough in Nigeria — a failed rift arm extending inland.

**Still to name:** the Sinchew sub-range, the rift valley.

### A caution on the rift trace
Tracing the trough automatically is unreliable. A "minimum elevation per column" search snaps to the northern coast (the lowest ground in the country, 2–38 m) unless the latitude band is tightly restricted to 2.6–5.2°S. The cleanest representation is to **use the lake's own long axis** as the rift floor. A naive full-resolution priority-flood also fails — propagation is one cell per pass and needs 1,300+ passes.

---

## 4. Borders

**The Sinchew–Louyang border is perfectly straight.** A single 10.94° segment from (−96.15, −11.01) to (−107.09, −10.98), with **maximum deviation from a straight line of 0.0000°** — artificial, colonial-style. This is why the subplate extends into Louyang: a plate boundary cannot follow a straight political line.

The long straight border along ~11°S is elsewhere attributed to Etowah in earlier notes; the geodatabase records it as shared with Louyang. Worth resolving which is correct.

---

## 5. Geographic feature register

Describes the geography descriptively first; every feature carries a **placeholder identifier** so that when the language work is done there is a definitive list of what still needs naming.

- **File:** `/Users/shubhamnaik/Developer/adonia-gis/Sinchew_geographic_feature_register.csv`
- **416 features:** 191 rivers (`RIV-001…RIV-191`) + 225 lakes (`LAK-001…LAK-225`)
- **Columns:** feature_id, type, named, proposed_name, length_km, area_km2, lon, lat, region_id, region, notes
- `named` is blank for all 416 — that is the future-labelling flag. `proposed_name` is the slot for the in-world name.

### Rivers
191 features, **12,627 km total**. Longest 640 km, median 47 km. The shapefile `Tamsui Rivers.shp` has only one named feature ("R1"). Note: 191, not the 126 recorded in older notes — the file has been updated.

Largest: RIV-001 (640 km, source 925 m → mouth 289 m), RIV-002 (608 km, **source 2,325 m → mouth 44 m**), RIV-003 (364 km).

**Two kinds of river appear in the data.** RIV-002 and RIV-007 descend from above 2,300 m — genuine trans-continental rivers draining the eastern highlands westward. But RIV-008, RIV-011, RIV-012 and RIV-016 each drop only ~10 m over 150–250 km — artifacts of the flat painted bands. **This is fixed in `Sinchew_DEM_filled.tif`** and should be re-measured before writing drainage descriptions.

### Lakes
225 features, **39,348 km² total** (1.9% of the country). Largest 14,705 km², median 29.6 km². 47 exceed 100 km²; 7 exceed 500 km². The count differs from the 233 recorded earlier because connected-component labelling at working resolution merges some.

| id | km² | lon, lat | region |
|---|---|---|---|
| LAK-001 | 14,705 | −107.38, −3.64 | Lowlands / Am — **the rift lake** |
| LAK-002 | 7,173 | −107.03, −8.17 | Central Plateau / Aw |
| LAK-003 | 1,967 | −105.72, −6.20 | Central Plateau / Aw |

The three largest sit in different regions. LAK-002, at 7,173 km² and 8.17°S, dominates the southern interior.

---

## 6. Open questions

1. **Names** — Sinchew's sub-range within the Great Lurandian Range; the E–W rift valley.
2. **Deepen the rift?** The trough is real but shallow. A rift valley would normally have more pronounced shoulders — a painting change of maybe 100–200 m depth over a 40–80 km width.
3. **How far does the subplate extend into Louyang?** And does the suture continue south of the border? (No Louyang DEM available to check.)
4. **Redo the region boundaries at a lower threshold** (~2,000 cells) for more honest edges.
5. **Repair the Adonia plate list** — duplicate "Lurandian", three "XXX" placeholders.
6. **The Kaskaskian range** — is it the same feature as the Great Lurandian Range under a different name, or a separate belt? Currently named once with no location.
7. **Resolve the Etowah/Louyang attribution** for the straight southern border.
