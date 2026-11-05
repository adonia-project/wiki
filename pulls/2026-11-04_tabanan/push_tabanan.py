# -*- coding: utf-8 -*-
"""Almuria crosswalk master push: Tabanan onboarding.
Login-asserted; exact-string replacements with verification; NO anonymous edits."""
import requests, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API = 'https://talod.miraheze.org/w/api.php'
UA = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
S = requests.Session()
S.headers['User-Agent'] = UA

# ---------- LOGIN (abort on failure) ----------
r = S.get(API, params={'action':'query','meta':'tokens','type':'login','format':'json'}).json()
lgtoken = r['query']['tokens']['logintoken']
r = S.post(API, data={'action':'login','lgname':'Takeru-Sync@Letta_Takeru','lgpassword':'mt54tvf8s22mcsdu02jf0jknt02ao3pc','lgtoken':lgtoken,'format':'json'}).json()
if r.get('login',{}).get('result') != 'Success':
    print('LOGIN FAILED:', r); sys.exit(1)
print('LOGIN OK as', r['login']['lgusername'])
r = S.get(API, params={'action':'query','meta':'tokens','type':'csrf','format':'json'}).json()
CSRF = r['query']['tokens']['csrftoken']

def get_page(title):
    r = S.get(API, params={'action':'query','titles':title,'prop':'revisions','rvprop':'content','rvslots':'main','format':'json'}).json()
    for pg in r['query']['pages'].values():
        if 'revisions' in pg:
            return pg['revisions'][0]['slots']['main']['*']
    return None

def edit(title, text, summary, minor=False):
    r = S.post(API, data={'action':'edit','title':title,'text':text,'summary':summary,'token':CSRF,
                          'assert':'user','format':'json',
                          **({'minor':1} if minor else {})}).json()
    if 'error' in r:
        print('  EDIT ERROR', title, r['error']['code'], r['error'].get('info',''))
        return False
    res = r.get('edit',{}).get('result')
    print('  edit', title, '->', res, '(newrevid', r.get('edit',{}).get('newrevid','nochange'), ')')
    return True

def replace_in(title, pairs, summary):
    txt = get_page(title)
    if txt is None:
        print('  MISSING PAGE:', title); return False
    ok = True
    for old, new in pairs:
        if old not in txt:
            print('  !! NOT FOUND in', title, ':', old[:70].replace('\n','\\n'))
            ok = False
        else:
            txt = txt.replace(old, new)
    if not ok:
        print('  ABORTING edit of', title, '(string mismatch - no push)')
        return False
    return edit(title, txt, summary)

SUM = 'Almuria crosswalk: Tabanan onboarding (northern Almuria); Pakiak migrated south; Volistraya retired'

# ---------- 1. Uploads ----------
for fn, comment in [
    (r'B:\02_GIT CONNECTED\map\Location of Tabanan.svg', 'Location map for Tabanan (house-style orthographic globe, GIS-derived)'),
    (r'B:\02_GIT CONNECTED\map\Location of Pakiak.svg', 'Location map for Pakiak (house-style orthographic globe, GIS-derived)'),
]:
    name = fn.split('\\')[-1]
    with open(fn, 'rb') as fh:
        r = S.post(API, files={'file': (name, fh.read(), 'image/svg+xml')},
                   data={'action':'upload','filename':name,'comment':comment,
                         'text':comment + ' - generated from the Adonia continental GIS data.',
                         'ignorewarnings':1,'token':CSRF,'assert':'user','format':'json'}).json()
    if 'error' in r:
        print('  UPLOAD ERROR', name, r['error']); sys.exit(1)
    print('  upload', name, '->', r.get('upload',{}).get('result'))

# ---------- 2. Tabanan article + Talk ----------
tab = open(r'B:\02_GIT CONNECTED\wiki\articles\Countries\Tabanan\Tabanan.mediawiki', encoding='utf-8-sig').read()
edit('Tabanan', tab, 'Expand Tabanan: GIS-grounded geography/infobox (795,306 km2), structured TBA sections; original lead preserved')
talk = open(r'B:\02_GIT CONNECTED\wiki\articles\Countries\Tabanan\Talk Tabanan.mediawiki', encoding='utf-8-sig').read()
edit('Talk:Tabanan', talk, 'Archivist welcome note: crosswalk summary, canon facts, recommended next steps', minor=True)

# ---------- 3. Pakiak edits ----------
pakiak_pairs = [
    ('|area                        = 795,306', '|area                        = 2,284,129'),
    ('|area_km2                    = 795,306', '|area_km2                    = 2,284,129'),
    ('|area_sq_mi                  = 307,070', '|area_sq_mi                  = 881,906'),
    ('|population_density_km2      = 67.5', '|population_density_km2      = 23.5'),
    ('|population_density_sq_mi    = 174.8', '|population_density_sq_mi    = 60.9'),
    ('|image_map                   = Location of Almuria.svg', '|image_map                   = Location of Pakiak.svg'),
    ("is a country occupying the northern portion of the continent of [[Almuria]]. At 795,306 square kilometers, it is the smaller of the two countries on the continent and, with a population of over 53 million, is the more densely populated. Pakiak does not share land borders with any other sovereign state, separated from [[Volistraya]] by the <> mountain range.",
     "is a country occupying the southern portion of the continent of [[Almuria]]. At 2,284,129 square kilometers, it is by far the larger of the two countries on the continent and, with a population of over 53 million, the more populous. Pakiak shares its only land border with [[Tabanan]] to the north, from which it is separated by the <> mountain range."),
]
replace_in('Pakiak', pakiak_pairs, 'Almuria crosswalk: Pakiak migrates to the southern portion (2,284,129 km2); land border with Tabanan; new location map')

# ---------- 4. Almuria (continent) ----------
almuria_pairs = [
    ('| population     = 53,736,708+ <small>(2025 est.)</small>', '| population     = 72,736,708+ <small>(2025 est.)</small>'),
    ('| languages      = [[Bayani language|Bayani]], indigenous languages', '| languages      = [[Bayani language|Bayani]], [[Tabanese language|Tabanese]], indigenous languages'),
    ("'''Almuria''' is the smallest continent on [[Adonia]] by both area and number of sovereign states. Located in the northern hemisphere, it comprises two countries — [[Pakiak]] and [[Volistraya]] — and covers",
     "'''Almuria''' is the second-smallest continent on [[Adonia]] by area. Located in the northern hemisphere, it comprises two countries — [[Tabanan]] and [[Pakiak]] — and covers"),
    ('| {{flag|Pakiak}} || [[File:Coats of arms of None.svg|20px]] || [[Pakiak]] || 795,306 || 53,736,708 || 67.5 || [[Al-Bayda]] || بلاد المُرِّية, Bilād al-Murriyya',
     '| [[Tabanan]] || [[File:Coats of arms of None.svg|20px]] || [[Tabanan]] || 795,306 || 19,000,000 || 23.9 || [[Balete City|Balete]] || Karahanan Sabyang it Tabanan'),
    ('| {{flag|Volistraya}} || [[File:Coats of arms of None.svg|20px]] || [[Volistraya]] || 2,284,129 || {{formatnum:2025}} || 0.00 || TBD || TBD',
     '| {{flag|Pakiak}} || [[File:Coats of arms of None.svg|20px]] || [[Pakiak]] || 2,284,129 || 53,736,708 || 23.5 || [[Al-Bayda]] || بلاد المُرِّية, Bilād al-Murriyya'),
]
replace_in('Almuria (continent)', almuria_pairs, 'Almuria crosswalk: Tabanan (north) + Pakiak (south); population 72.7M; Tabanese added to languages')

# ---------- 5. Adonia ----------
adonia_pairs = [
    ('comprises a single sovereign state, [[Sanrobonia]] — one of only two continents governed by a single country, alongside [[Almuria]].',
     'comprises a single sovereign state, [[Sanrobonia]] — the only continent on Adonia governed by a single country.'),
    ('Almuria is the smallest inhabited continent (approximately 3.1 million km²), located in the southern ocean. It comprises two sovereign states: [[Pakiak]] and [[Volistraya]], with a combined population of approximately 54 million.',
     'Almuria is the second-smallest continent (approximately 3.1 million km²), located in the northern tropics. It comprises two sovereign states: [[Tabanan]] and [[Pakiak]], with a combined population of approximately 73 million.'),
]
replace_in('Adonia', adonia_pairs, 'Almuria crosswalk: two Almurian states (Tabanan + Pakiak); Haitan now the sole single-country continent')

# ---------- 6. Foreign relations of Okaiken ----------
fro_pairs = [
    ("Okaiken's relations with the Almurian states—[[Pakiak]] and [[Volistraya]]—are limited",
     "Okaiken's relations with the Almurian states—[[Tabanan]] and [[Pakiak]]—are limited"),
]
replace_in('Foreign relations of Okaiken', fro_pairs, 'Almuria crosswalk: update Almurian states (Tabanan + Pakiak)')

# ---------- 7. AC membership template ----------
replace_in('Template:Members of the Adonian Community',
           [('* [[Volistraya]]', '* [[Tabanan]]')],
           'Almuria crosswalk: Volistraya -> Tabanan')

# ---------- 8. Redirects ----------
edit('Volistraya', '#REDIRECT [[Pakiak]]\n', 'Almuria crosswalk: Volistraya retired; redirects to Pakiak (southern Almuria)')
edit('Almuria', '#REDIRECT [[Almuria (continent)]]\n', 'Redirect to the continent article (fixes [[Almuria]] links across Almurian articles)')

# ---------- 9. Country data templates ----------
cd_tabanan = ('{{ {{{1<noinclude>|country showdata</noinclude>}}}\n'
              '| alias = Tabanan\n'
              '| size = {{{size|}}}\n'
              '| name = {{{name|}}}\n'
              '| altlink = {{{altlink|}}}\n'
              '| altvar = {{{altvar|}}}\n'
              '| variant = {{{variant|}}}\n'
              '<noinclude>\n'
              '| related1 = Pakiak\n'
              '</noinclude>}}\n')
edit('Template:Country data Tabanan', cd_tabanan, 'Create country data for Tabanan (flag alias pending flag upload)')
cd_pakiak = ('{{ {{{1<noinclude>|country showdata</noinclude>}}}\n'
             '| alias = Pakiak\n'
             '| flag alias = Flag of Almuria.png\n'
             '| size = {{{size|}}}\n'
             '| name = {{{name|}}}\n'
             '| altlink = {{{altlink|}}}\n'
             '| altvar = {{{altvar|}}}\n'
             '| variant = {{{variant|}}}\n'
             '<noinclude>\n'
             '| related1 = Tabanan\n'
             '</noinclude>}}\n')
edit('Template:Country data Pakiak', cd_pakiak, 'Create country data for Pakiak (fixes {{flag|Pakiak}} in continent table)')

# ---------- 10. Verification ----------
print('\n=== VERIFICATION ===')
checks = [
    ('Tabanan', [('Karahanan Sabyang it Tabanan', True), ('Location of Tabanan.svg', True), ('795,306', True)]),
    ('Talk:Tabanan', [('Recommended next steps', True)]),
    ('Pakiak', [('2,284,129', True), ('Location of Pakiak.svg', True), ('Volistraya', False), ('[[Tabanan]]', True)]),
    ('Almuria (continent)', [('Tabanan', True), ('Volistraya', False), ('72,736,708', True)]),
    ('Adonia', [('Volistraya', False), ('[[Tabanan]] and [[Pakiak]]', True)]),
    ('Foreign relations of Okaiken', [('Volistraya', False)]),
    ('Template:Members of the Adonian Community', [('Volistraya', False), ('[[Tabanan]]', True)]),
    ('Volistraya', [('#REDIRECT [[Pakiak]]', True)]),
    ('Almuria', [('#REDIRECT [[Almuria (continent)]]', True)]),
    ('Template:Country data Tabanan', [('alias = Tabanan', True)]),
    ('Template:Country data Pakiak', [('flag alias = Flag of Almuria.png', True)]),
]
allok = True
for title, conds in checks:
    txt = get_page(title)
    if txt is None:
        print('FAIL - page missing:', title); allok = False; continue
    for s, want in conds:
        got = (s in txt)
        status = 'ok' if got == want else 'FAIL'
        if got != want: allok = False
        print(f'  [{status}] {title}: {s[:50]!r} {"present" if want else "absent"}')
print('\nALL VERIFICATIONS PASSED' if allok else '\nSOME CHECKS FAILED - review above')
