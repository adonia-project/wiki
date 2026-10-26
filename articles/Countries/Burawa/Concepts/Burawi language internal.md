# Burawi language — internal notes

## Vowel merger (decided 2026-10-26; timing corrected by user same day)

**User decision:** Modern Burawi no longer promotes double characters. Double vowels (aa, ee, ii, oo, uu) merge to single vowels in the modern language, for writing efficiency.

### How it was implemented in the article

- **Nature of the change:** Orthographic. The modern standard writes every vowel with a single letter. Vowel length survives in speech (Classical register, conservative Western varieties) but is unmarked in writing; colloquial speech has largely neutralized it.
- **In-world history (user-specified):** The merger happened **between the 15th and 16th centuries**, complete by the close of the 16th century. It PREDATES the Modern Shift (Beddelka Casriga, 16th–19th c.), which is presented as a separate, following series of changes. (Initial draft wrongly placed codification in a 1934 spelling reform — corrected.)
- **What keeps the double spellings:**
  - The **Classical register** (Af-Burawi Hore) — liturgy, poetry, legal texts.
  - **Proper names fixed before the merger** (grandfathered historical spellings).
  - **Doubled consonants** (dd, ll) are unaffected — the reform covers vowels only.

### Forms updated in the article

| Classical | Modern |
|---|---|
| baa / waa / ayaa (focus particles) | ba / wa / aya |
| aan, aad, uu (subject clitics) | an, ad, u |
| Rebuublik | Rebublik |
| Wasarada | Wasarada (ministry native name) |
| Af-Burawi Caadi | Af-Burawi Cadi |
| Noolada Rebublik | Nolada Rebublik |
| Article 1 text (wa, o, xuquq, Waxa, siy-ay, wana, dhaqm-an, midk-od, walal-nimo) | respelled accordingly |

### Consequence: pronoun homography

3rd person masculine subject clitic (uu → u) and object clitic (u) are now both written ⟨u⟩. Distinction survives in speech and is resolved in writing by syntax. Noted in article; acceptable.

## Open questions (for user)

1. **Proper names across the repo — RESOLVED (2026-10-26):** Proper names conventionally preserve their historical/etymological double-vowel spellings (comparable to archaic English surnames), even for names coined after the merger. **No repo-wide renames** — Maana Kadar, Xirsi Xaashi, Casar, etc. keep their established double-vowel spellings. Common nouns and vocabulary follow the merger; proper names do not. **Exception applied:** surnames are personal names — "Antoni Varaan", "Qaasim Varaan", "Bene Varaan" keep ⟨aa⟩ even though the city they come from is now Varan.
2. **Post-merger coinages** — any Burawi words/names invented for the modern era should use single vowels going forward (new placenames, company names, given names of modern-era characters).
3. **Spoken length** — currently described as surviving in speech but unmarked. Alternative: full phonological merger (length gone entirely). User said "merge... to be more efficient" — interpreted as orthographic; confirm if pronunciation should also merge.
4. **Other Burawi-language articles** — the Farisnimo article, housing/economy articles, etc. contain Burawi words (e.g. "faris", "hanti", "Dhaqso"). Check for double-vowel words in modern contexts when touching those articles.

## Repo-wide sweep (applied 2026-10-26)

A case-preserving text sweep over all `articles/**.mediawiki` and `*.md` applied the merger to placenames, institutions, agencies, events, common nouns, and Burawi native names of works/products. ~85 files changed; 9 article files git-mv'd. Main renames:

| Old | New |
|---|---|
| Buur Waaq (mountain) | Bur Waq |
| Dhulsarren | Dhulsaren |
| Kaysoor | Kaysor |
| Hooyal | Hoyal |
| Galbeed / Galbeedi | Galbed / Galbedi |
| kaas (fort common noun) | kas |
| Hoggaanka (decree/system) | Hoganka |
| Dagaalka / Waqooyi | Dagalka / Waqoyi |
| Hoose (Dafar Hoose, Hooyal Hoose) | Hose |
| Laasqoray | Lasqoray |
| Lagaani | Lagani |
| Maayo Weela | Mayo Wela |
| Caasar | Casar |
| Buuldheerta / Beledweenga / Dhaltoona / Dhardheer | Buldheerta / Beledwenga / Dhaltona / Dhardher |
| Buuraha / Buurdhuubo / Buurweyne / Buurhakaba / Buurta / Buuran / Buurawaat / standalone buur | Buraha / Burdhubo / Burweyne / Burhakaba / Burta / Buran / Burawat / bur |
| Koonfur | Konfur |
| Daarta / Cagaarka / Xiriirka / Liistinta / Laanta | Darta / Cagarka / Xirirka / Listinta / Lanta |
| Wasaaradda / Kaniisada Katooliga / Jamhuuriyad / Boqortooyad / Hal-abuurka | Wasarada / Kanisada Katoliga / Jamhuriyad / Boqortoyad / Hal-aburka |
| BMC Hooyo / BMC Aabbe (car models) | BMC Hoyo / BMC Abe |
| Sare Suuq / Sare Baaskiil | Sare Suq / Sare Baskil |
| Koobka Gobolada | Kobka Gobolada |
| Varaan (city) / Varaan United | Varan / Varan United |
| Jasiiradaha Dakare | Jasiradaha Dakare |
| Qiritaalka Weyn / Xogga Dhammaan Dadka (work titles) | Qiritalka Weyn / Xoga Dhaman Dadka |
| "ee" genitive in native names (Fotbal e Burawi, Weyn e Kaftia, Taksiga e Ugu Weyn, Qaranka e Burawi, Deganka e Hudur, Wadada Tirtarka e Jawi-Sago) | "e" |

**Kept doubles (intentional):** all personal names and dynasties (Geedi, Nuur, Faarax, Garaad, Qaasim, Saleebaan, Warfaa, Guleed/Guuleed, Rooble, Ciise, Cigaal, Aadan, Siciid, Liibaan, Maana, Xaashi, Dheere, Kunciil, Koofur, Jaamac, Hayaan, Varaan as surname); the deity Waaq; Bariites (English demonym formation); Alaafia Party (Sanyan language); all Sanese/Okaiken/Dagit/non-Burawi words; doubled consonants; Classical register text.

**Flagged for live wiki (Miraheze):** renamed articles need page moves there (sync maps filename → page title); image file `Kaas_Hilltop_Fort.jpg` was NOT renamed and would need a file move on the live wiki.

## General article notes

- Article: `articles/Countries/Burawa/Concepts/Burawi language.mediawiki`
- Register system: Classical (Af-Burawi Hore), Formal Modern (Af-Burawi Casri), Colloquial (Af-Burawi Cadi)
- Modern Shift (Beddelka Casriga): 16th–19th c. phonological changes; vowel merger (15th–16th c.) predates it
- Related: [[Burano-Ormaic languages]], Orma languages, Mesogean loanword strata
