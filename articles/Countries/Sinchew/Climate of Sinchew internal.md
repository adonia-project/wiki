# Climate of Sinchew — internal notes

## Status
Article written 2026-09-18. Derived entirely from the GIS climate model in
`/Users/shubhamnaik/Developer/adonia-gis/sinchew_climate.py`. Not yet synced to
TALOD (no sync script covers `articles/Countries/Sinchew/` yet — see "Sync" below).

## How the climate was produced
The maps are the output of a purpose-built climate model, not hand-authored. The
pipeline lives in `/Users/shubhamnaik/Developer/adonia-gis/`:

- `Sinchew_DEM_burned.tif` — elevation, painted by hand in Affinity Photo and
  hydrologically corrected (rivers burned in).
- `build_sinchew_sea_mask.py` → `Sinchew_sea_mask.tif` — a TRUE sea mask built by
  rasterising the Adonia country polygons. Needed because the DEM marks everything
  outside Sinchew as nodata, which would otherwise treat neighbouring countries'
  land (Louyang, Etowah, Amiera, Balboa) as ocean.
- `sinchew_climate.py` — the model. Monthly loop marching moisture from the east
  across the country, with ITCZ migration, orographic lift, maritime recharge,
  lake handling, and a Köppen classification pass.

### Physics as implemented
- Easterly trade winds enter at the east coast and march west cell by cell.
- ITCZ migrates seasonally between ~12°S and ~8°N, traversing the whole country.
- Orographic rainfall where terrain rises along the flow, producing the eastern
  highland wet belt and the western rain shadow.
- No cold-current coastal taper (deliberately removed — see below).
- Maritime moderation of the annual temperature range near all coasts.
- Lake moisture effects are currently DISABLED (`SINCHEW_LAKES=1` to re-enable).
  They inflated precipitation ~30–47% at every large lake edge because the
  recharge term added q_sat=0.9 on top of an ambient column of ~1.0, and the
  two-cell-blurred lake mask drew that as a sharp rim tracing each nodata hole.
  The user saw this as "streaking from the lakes".

### Key numbers (current run)
- Median annual precipitation 2,369 mm; range 795–5,719 mm.
- Median annual temperature 21.9 °C; range 5.3–27.0 °C.
- Köppen shares: Am 34.8%, Aw 29.0%, Af 17.6%, Cfb 9.3%, Cfa 9.1%, ET 0.2%.
- No arid zone anywhere. The driest point (795 mm) is comparable to a wet
  Mediterranean climate.

## Design decisions worth remembering
1. **The country is a peninsula-continent.** Measuring every boundary cell:
   86.7% of Sinchew's perimeter is sea (N 95%, W 97%, E 80%, S 78%). This was a
   surprise — earlier notes assumed a land flank to the south. It means distance
   to water governs the climate far more than any single coastline.
2. **The northern ocean is open; the west/south is a marginal sea.** The
   semi-enclosed sea cannot sustain a cold boundary current (those are
   eastern-boundary upwelling features of open basins: Canary, Benguela,
   Humboldt, California). The original design had a cold-current fog desert on
   the west coast; that was physically unsupported and was removed. West-coast
   dryness now comes from the rain shadow, which is the honest mechanism.
3. **No desert.** The user liked the look of the old fog desert and asked whether
   to reinstate it as an authored choice. Open question, below.

## Climate regions
The 23 regions in the article come from k-means clustering (k=14) on annual
precipitation, temperature, elevation and rainfall seasonality, then spatial
cleanup (median filter, component size threshold, absorption of fragments into
nearest neighbours). Naming is derived from latitude band + east/central/west
position + dominant Köppen type, with elevation overrides for highlands.

Some names repeat with Roman numerals appended (e.g. "Upper-central west monsoon
belt II–V") because the clustering found genuinely separate areas with near-
identical statistics. **These need better names before the article is final** —
ideally real in-world region names rather than descriptive labels.

## Open questions
1. **Region naming.** Do the regions correspond to any administrative or cultural
   divisions the user has in mind? Real names would be much better than the
   current descriptive labels.
2. **Reinstate a dry zone?** The physics says no arid climate. If the user wants
   one as an authored choice, the hand-painted precipitation canvas supports it
   (`export_sinchew_precip_paint.py` → paint → `convert_sinchew_precip_paint.py`
   → run with `SINCHEW_PRECIP_PAINTED=1`), and painted edits rescale the monthly
   fields so the Köppen map stays consistent.
3. **Lake effects.** Currently off. A gentler version (much smaller q_sat, wider
   lake mask blur) could give local lake wetness without the rim artifact.
4. **Weather box templates.** The article has no monthly climate tables because no
   weather stations exist yet. Burawa's geography article uses
   `{{Weather box <City>}}` templates. If named settlements are established for
   Sinchew, monthly tables could be generated from the model's per-month output
   (`Sinchew_precip_monthly.tif`). **This would strengthen the article
   considerably** — the model already produces monthly data.
5. **Cyclones.** The marginal sea plausibly supports tropical cyclones; no
   cyclone history has been written. Worth developing.
6. **Elevation of named features.** The article refers to "the eastern highlands"
   but no peak or range has been named yet.

## Sync
`sync_other.py` handles `articles/Other/` and a few listed former-country files.
There is no sync script covering `articles/Countries/Sinchew/`, so this article is
local only. Either add Sinchew to a sync script or extend `sync_other.py`.
Images upload separately via `upload_image.py`.

## Files
- Article: `articles/Countries/Sinchew/Climate of Sinchew.mediawiki`
- Maps: `articles/Countries/Sinchew/Maps/Sinchew {annual precipitation,mean annual
  temperature,Koppen climate classification,climate regions}.png`
- Model outputs: `/Users/shubhamnaik/Developer/adonia-gis/Sinchew_{precip_annual,
  temp_annual,koppen,precip_monthly}.tif`
- Region table: `/Users/shubhamnaik/Developer/adonia-gis/region_table.json`
- Full technical record: agent memory `reference/sinchew_gis.md`
