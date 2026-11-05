import json, requests, os
cfg = json.load(open(r'B:\02_GIT CONNECTED\wiki\sync_config.json'))
U, P = cfg['wiki']['bot_username'], cfg['wiki']['bot_password']
API = 'https://talod.miraheze.org/w/api.php'
s = requests.Session(); s.headers['User-Agent'] = 'Takeru-Sync/1.0'
r = s.post(API, data={'action':'login','lgname':U,'lgpassword':P,'format':'json'}).json()
r = s.post(API, data={'action':'login','lgname':U,'lgpassword':P,'lgtoken':r['login']['token'],'format':'json'}).json()
assert r['login']['result'] == 'Success', r
token = s.get(API, params={'action':'query','meta':'tokens','format':'json'}).json()['query']['tokens']['csrftoken']

def get(title):
    r = s.get(API, params={'action':'query','titles':title,'prop':'revisions','rvprop':'content','format':'json'}).json()
    for p in r['query']['pages'].values():
        return p['revisions'][0]['*'] if 'revisions' in p else None

def edit(title, text, summary):
    r = s.post(API, data={'action':'edit','title':title,'text':text,'summary':summary,'bot':1,'token':token,'format':'json'}).json()
    res = r.get('edit', {})
    print(f"{title}: {res.get('result')} (revid {res.get('newrevid', res.get('nochange','?'))})")
    assert res.get('result') == 'Success', r
    return res

NAV = '{{Countries in Lurandia}}'
ART = r'B:\02_GIT CONNECTED\wiki\articles\Countries'

# --- 1. Eight new stub pages ---
for n in ['Kalanua','Kawalidipa','Markland','Mishko','Nawat','Neakyrena','Nuuchi','Tuvayo']:
    c = open(os.path.join(ART, n, f'{n}.mediawiki'), encoding='utf-8').read()
    edit(n, c, 'Create country stub (Lurandia roster completion: infobox, location globe, borders)')

# --- 2. Amiera expansion ---
c = get('Amiera'); assert c
old = "'''Amiera''' is a country in northern [[Lurandia]]."
new = "'''Amiera''' is a small country in northern [[Lurandia]]. It covers an area of approximately 101,662 km² and borders [[Etawa]] and [[Sinchew]]."
assert old in c; c = c.replace(old, new).replace('{{Stub}}', '{{Stub}}\n' + NAV)
edit('Amiera', c, 'Expand stub: area, borders; add Lurandia navbox')

# --- 3. Etawa expansion ---
c = get('Etawa'); assert c
old = "'''Etawa''' is a country in northern [[Lurandia]]."
new = "'''Etawa''' is a country in northern [[Lurandia]]. It covers an area of approximately 588,942 km² and borders [[Amiera]], [[Louyang]], [[Sinchew]] and the [[United Midlands]]."
assert old in c; c = c.replace(old, new).replace('{{Stub}}', '{{Stub}}\n' + NAV)
edit('Etawa', c, 'Expand stub: area, borders; add Lurandia navbox')

# --- 4. Winnipi expansion ---
c = get('Winnipi'); assert c
old = "'''Winnipi''' is a country in southern [[Lurandia]]. Its population is predominantly [[w:Cree|Cree]] and [[w:Anishinaabe|Anishinaabe]]."
new = ("'''Winnipi''' is a country in the far south of [[Lurandia]]. It is the second-largest country on the continent after [[Louyang]], "
       "covering an area of approximately 7,431,406 km². Its population is predominantly [[w:Cree|Cree]] and [[w:Anishinaabe|Anishinaabe]]. "
       "It borders [[Kaneda]], [[Kavik]], [[Kawalidipa]], [[Markland]], [[Mishko]], [[Neakyrena]], [[Nuuchi]], [[Tuvayo]] and the [[United Midlands]].")
assert old in c; c = c.replace(old, new).replace('{{Stub}}', '{{Stub}}\n' + NAV)
edit('Winnipi', c, 'Expand stub: area, borders; add Lurandia navbox')

# --- 5. Sinchew full stub ---
sin = """{{Infobox country
|common_name                 = Sinchew
|image_map                   = Location of Sinchew.svg
|map_caption                 = Location of Sinchew
|area_km2                    = 2017722
}}

'''Sinchew''' is a country in northern [[Lurandia]]. It covers an area of approximately 2,017,722 km², making it one of the larger countries of the continent's north. It borders [[Amiera]], [[Balboa]], [[Etawa]] and [[Louyang]].

{{Stub}}
""" + NAV + """
[[Category:Lurandia]]
[[Category:Countries in Lurandia]]
"""
edit('Sinchew', sin, 'Add infobox, location globe, borders; add Lurandia navbox')

# --- 6. United Midlands: borders sentence + navbox ---
c = get('United Midlands'); assert c
old = "a colonial possession of the [[Kingdom of Merica]]."
new = old + " It borders [[Etawa]], [[Kawalidipa]], [[Louyang]], [[Nawat]] and [[Winnipi]]."
assert old in c; c = c.replace(old, new).replace('{{Stub}}', '{{Stub}}\n' + NAV)
edit('United Midlands', c, 'Add borders; add Lurandia navbox')

# --- 7. Navbox on the four full articles ---
for t in ['Balboa','Kaneda','Kavik','Louyang']:
    c = get(t); assert c
    if NAV in c:
        print(t, ': navbox already present'); continue
    if '[[Category:' in c:
        c = c.replace('[[Category:', NAV + '\n[[Category:', 1)
    else:
        c = c.rstrip() + '\n\n' + NAV + '\n'
    edit(t, c, 'Add Lurandia countries navbox')
print('ALL DONE')
