# Line E (CristoCarril) — Internal Notes

## GIS Data Source
- **Shapefile**: `/Users/shubhamnaik/Developer/adonia-gis/Points of Interest.shp`
- **POI indices (in order)**: 68, 67, 66, 65, 136, 149, 148, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159
- **Railroad corridor**: Sant bart Subdivision (from `baboa_railroads.shp`)
- **Total corridor length**: ~360 km (Sant Cristòfor to Sant Bart); Line E uses only first ~42 km

## Station Details

| # | POI Index | Name | Lat | Lon | Cumulative km | Ciutat | Comarca |
|---|-----------|------|-----|-----|---------------|--------|---------|
| 1 | 68 | Sant Cristòfor Central Terminal | 0.6400 | -94.4000 | 0.0 | Original | Sant Cristòfor |
| 2 | 67 | Portal de Sant Cristòfor | 0.6300 | -94.3850 | 3.0 | Original | Sant Cristòfor |
| 3 | 66 | Sant Pere | 0.6250 | -94.3700 | 4.6 | Original | Sant Cristòfor |
| 4 | 65 | La Font | 0.6200 | -94.3550 | 6.7 | Original | Sant Cristòfor |
| 5 | 136 | Mas Blanc | 0.6175 | -94.3400 | 7.9 | Sant Jordi | Sant Cristòfor |
| 6 | 149 | Parc de Sant Jordi | 0.6175 | -94.3221 | 9.9 | Sant Jordi | Sant Cristòfor |
| 7 | 148 | Sant Miquel Sud | 0.6250 | -94.3050 | 11.6 | Sant Miquel | Sant Cristòfor |
| 8 | 150 | Sant Miquel Centre | 0.6500 | -94.2850 | 15.8 | Sant Miquel | Sant Cristòfor |
| 9 | 151 | Sant Miquel Nord | 0.6650 | -94.2700 | 17.1 | Sant Miquel | Sant Cristòfor |
| 10 | 152 | Les Dunes | 0.6900 | -94.2500 | 20.1 | Costa Nord | Sant Cristòfor |
| 11 | 153 | Costa Centre | 0.7150 | -94.2300 | 22.4 | Costa Nord | Sant Cristòfor |
| 12 | 154 | El Far | 0.7400 | -94.2100 | 24.7 | Costa Nord | Sant Cristòfor |
| 13 | 155 | Platja Llevant | 0.7650 | -94.1900 | 26.6 | Costa Nord | Sant Cristòfor |
| 14 | 156 | Costa Nord | 0.7900 | -94.1700 | 28.6 | Costa Nord | Sant Cristòfor |
| 15 | 157 | Aiguamolls Sud | 0.8250 | -94.1500 | 32.4 | — | Els Aiguamolls |
| 16 | 158 | Els Canyars | 0.8650 | -94.1300 | 36.8 | — | Els Aiguamolls |
| 17 | 159 | La Llacuna | 0.9250 | -94.1000 | 42.4 | — | Els Aiguamolls |

## Shared Stations
- Stations 1-4 (Central Terminal, Portal, Sant Pere, La Font): Shared with Lines B, C, D
- Station 5 (Mas Blanc): Shared with Line D — this is the divergence point where Line D turns onto Old Grand Subdivision and Line E continues on Sant Bart Line
- **Note**: Line D article currently says "Line D diverges from the shared mainline at La Font onto the Old Grand Subdivision" but GIS data shows Mas Blanc (station 136) is on the Sant bart Subdivision, shared between D and E. The divergence to Old Grand Subdivision happens after Mas Blanc. Line D article may need correction.

## Station Naming Rationale

### Already Named (from GIS or other line articles)
- Stations 1-5: Named in Line D article and GIS data

### Proposed Names (new)
- **Parc de Sant Jordi** (stn 6): "Park of Sant Jordi" — suggests a park area in northern Sant Jordi ciutat
- **Sant Miquel Sud/Centre/Nord** (stns 7-9): Directional naming for the three stations in Sant Miquel ciutat, following the pattern of "Pujol Sud" on Line D
- **Les Dunes** (stn 10): "The Dunes" — coastal geographic feature, entry to Costa Nord from the south
- **Costa Centre** (stn 11): Central station in Costa Nord ciutat
- **El Far** (stn 12): "The Lighthouse" — landmark name suggesting a coastal lighthouse
- **Platja Llevant** (stn 13): "Eastern Beach" — coastal area name
- **Costa Nord** (stn 14): Namesake station for the ciutat
- **Aiguamolls Sud** (stn 15): "Aiguamolls South" — southern entry to Els Aiguamolls comarca
- **Els Canyars** (stn 16): "The Reed Beds" — wetland settlement name
- **La Llacuna** (stn 17): "The Lagoon" — wetland settlement name, terminus

## Ridership Estimates
- Total: 36,100 (2025)
- Based on Line D's 48,200 but adjusted for shorter line (42.4 km vs 64.2 km) and less dense northern suburbs
- Shared stations (1-5) have same ridership as Line D article
- New stations estimated lower (700-3,100) based on suburban/commuter patterns

## Service Pattern Logic
- **Short** (stns 1-14): All stops within Sant Cristòfor to Costa Nord, ~37 min — most frequent, serves dense urban ridership
- **Express** (stns 1,2,5,8,11,14,17): Selected stops to La Llacuna, ~45 min — for long-distance commuters to Els Aiguamolls
- **Local** (all 17): All stops, ~55 min — provides service to intermediate stations skipped by express

## Open Questions
1. **Line D article correction**: Line D article says divergence happens "at La Font" but GIS data shows Mas Blanc is shared (on Sant bart Subdivision). Should Line D article be updated to say divergence happens at Mas Blanc?
2. **Els Aiguamolls municipalities**: The three Els Aiguamolls stations (15-17) don't have ciutat/municipality names in the GIS data. Are they in specific municipalities?
3. **Fleet allocation**: Line E not yet mentioned in Alcántara Corrent article. Should be added as 4-car formation (similar to Line D).
4. **Corridor article**: "Sant Bart Line" article doesn't exist yet (same as other corridor articles). Should it be created?
5. **Nav template update**: `Template:CristoCarril lines` on the wiki already includes Line E in the lines list, but the "Corridors" section does not include "Sant Bart Line". Needs updating.
6. **Corrent article update**: Alcántara Corrent article needs Line E added to fleet allocation section.
