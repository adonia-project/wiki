# Okheng — internal notes

Begun 2026-09-21. The polity at the bay of Oktalwa, 1521–1535.

Article: `Okheng.mediawiki`. Related: `Hokta internal.md`, `Chiu Khéng-gio̍k internal.md`, `Tamsui Company internal.md`.

---

## 1. Measurements — from the GIS layer
From `mahik_war_base.gpkg`, layer `draft_language_territories`, feature 16 = **"Zong Controlled Tamsui"**:

| | |
|---|---|
| longitude | −112.04 … −111.17 |
| latitude | −4.29 … −3.79 |
| extent | ~97 km (E–W) × 55 km (N–S) |
| **area** | **3,301 km²** (equal-area, Mollweide) |

**The layer's own note reads `DRAFT - replace with hand-drawn`** — so this is provisional and may be replaced.

**For scale:** 3,301 km² is **0.8% of the Kawesa family's 413,722 km²**. The Akwesa were a *small* chiefdom inside a very large linguistic family — consistent with the user's ruling that **the Akwesa were in the north, with the smaller chiefdoms**.

**Note: the layer is EPSG:4326.** Do not reproject from ESRI:54030 — that produced zeros. Use the coordinates as-is and project only for the equal-area area calculation.

---

## 2. Population — estimates
**User: "it was mainly akwesa and a small amount of zong, we can estimate the akwesa populations."**

| component | estimate | basis |
|---|---|---|
| **Akwesa (before the epidemics)** | **~12,000** | 3,301 km² at ~3.6/km² — coastal + riverine, 1,900 mm tropical climate, but a chiefdom with no cities |
| **Akwesa (by the 1530s)** | **~5,000–8,000** | heavy plague losses 1527 onward; "the chiefdom was much reduced by the deaths" |
| **Zong** | **150–300** | company employees, garrison, a few merchant families — "a small amount" |

**Sanity check against the First Mahik War:** the Hahkina fielded ~45,000 men and the chiefdoms *in aggregate* outnumbered them. Seven chiefdoms at ~12,000 each gives ~84,000 people and only ~15,000 fighting men — **which would not outnumber the Hahkina**. The user's answer resolves this: **the northern chiefdoms were small and the southern ones large**, so the 45,000+ came mostly from the south. A workable distribution: 3 northern chiefdoms at 5,000–12,000, 4 southern at 40,000–70,000 → ~225,000 total Kawesa, ~45,000 fighting men. **This has not been written into any article yet.**

---

## 3. Government — "basically managed by the company"
**User ruling.** The article therefore says plainly that **Okheng possessed no institutions of its own that the colonial record describes** — no assembly, court, treasury or officials; no coinage, written law or separate taxation. It was run as a commercial enterprise with a ruling family attached.

**The division of function:** the company held the commercial establishment, ships and armed men and conducted the diplomacy and wars; **the chiefly family supplied the standing** — land held by grant, the allegiance of the people, and a claim of rule the company could not assert for itself alone.

**This shapes the whole article.** Okheng is not a kingdom that happened to have a trading company in it; it is a **trading company that acquired a crown**. The infobox government field says so directly.

---

## 4. Decisions and flags
- **Dates 1521–1535** — from the marriage (joint holding begins) to the purchase. **The name Okheng may only date from 1527** (Hokta's death, when CKG ruled alone); the article says the polity is *usually dated* from 1521 but does not claim the name is that old. **The user may want this pinned down.**
- **No other name for it is recorded** — the user confirmed it was called Okheng, so the Zong coinage is the name and there is no hidden Akwesa alternative.
- **`p1`/`s1` — I was WRONG to remove them. Re-added on the user's instruction.**

  I removed them believing they rendered as blank flags. **They render fine.** `Template:Infobox country_formernext` emits `[[File:Blank.png|22px]]` when no flag is supplied, then `[[{{{p1}}}]]` **as a text link** — so a flagless entity shows a blank spacer plus the linked name. The fields work for entities with no country data.

  **What misled me:** my verification regex used `re.search(r'<table class="infobox.*?</table>')` with a non-greedy match, which **stops at the FIRST `</table>`** — and `formernext` builds an *inner* sub-table, so the extraction was truncated before the successor field. I concluded the fields were broken when I was simply not reading far enough.

  **Current state:** `p1 = Akwesa`, `s1 = Sinchew Colony`, `flag_s1 = Flag of Colonial Sinchew.svg`. Both render.

  **Lesson: do not verify a wiki render with a non-greedy `.*?</table>` — infoboxes contain nested tables.** Read from a known anchor to the end of the box instead.

---

## 5. Open questions
1. **Was the name Okheng older than 1527**, or coined when CKG ruled alone?
2. **Did the Akwesa understand themselves as living in "Okheng"?** The name is Zong, formed from a Zong company and a Zong rendering of an Akwesa place-name. **A people ruled by a polity whose name is a foreign coinage is worth a sentence.**
3. **What were the wars actually about?** The company helped the Akwesa against neighbouring chiefdoms and the territory expanded. **Whose land was taken, and were those chiefdoms among the six destroyed in 1538–42?** If the Akwesa and the colony had already dispossessed them in the 1520s, the First Mahik War has a longer fuse than the current articles suggest.
4. **Did Okheng have a flag or emblem?** Nothing recorded — realistic for a company territory, and the empty `image_flag` is honest.
5. **Where was the seat of rule** — the depot at Oktalwa, or an Akwesa settlement elsewhere? The infobox names Oktalwa as the capital, which is an assumption.
6. **Was there an Akwesa council or chiefly body** that the company dealt with, even if the colonial record does not name it?

---

## Map added (2026-09-21)
User: *"we can also add a map"* → *"hmm can we zoom out a bit so we can see all of mdoern sinchew"* → *"whats witht he circle?"* → *"thats fine for the image size"*.

**`File:Okheng locator.svg`** — framed on **modern Sinchew + 1.4° padding** (lon −120.82…−91.71, lat −12.41…0.71), 660 × 299.

| layer | colour |
|---|---|
| Ocean | `#C7E7FB` |
| Okheng (focus) | `#C12838` red |
| Other Kawesa chiefdoms | `#FDFBEA` cream |
| Other peoples' land | `#DFDFDF` grey |

Built from `mahik_war_base.gpkg` → `draft_language_territories` (focus = "Zong Controlled Tamsui"; cream = the four "Kawesa" features) plus the `countries` layer for wider land. Script: `adonia-gis/okheng_map.py`.

**I removed a circle I had added** around Okheng. My reasoning was that at Sinchew-wide zoom the subject is only ~10 px across. **But a callout circle is not a locator-map convention** — WikiProject Maps highlights the subject by colour alone — and the user queried it immediately. **Do not add markers to locator maps.** The red is small but legible against cream.

Geometry simplified (Kawesa/other `simplify(0.004)`, focus `0.0005`) to cut the file from **769 KB → 364 KB**. Edges pixel-checked: all ocean or land, no white sliver.

---

## TWO MISTAKES WORTH RECORDING

### 1. A silent failed replace — check your `assert`s land on what you think
I set `image_map` with `s.replace("| image_map              = \n", ...)` — **but the field has no trailing space**, so the replace matched nothing and the field stayed empty. **The script printed its success message anyway**, because the `assert` was on a *different* edit (the body image) in the same script. I then spent several steps diagnosing a phantom "SVG doesn't work in infoboxes" problem.

**Fix: use a regex anchored to the line (`^\| image_map\s*=\s*$`) and assert the substitution count.** `re.subn` returns the count — check it.

### 2. SVG in `image_map` DOES work — tested
My conclusion that `{{Infobox former country}}` needs a raster `image_map` was **wrong**. Once the field was actually populated, the SVG rendered in the infobox fine (and on this wiki SVG thumbs work). The PNG I generated as a workaround was unnecessary and has been deleted.

**Lesson: when a template field appears not to work, first verify the field is actually populated.** Read the stored wikitext (`action=raw`) rather than trusting your own edit.
