# -*- coding: utf-8 -*-
import requests, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
API = 'https://talod.miraheze.org/w/api.php'

def content(title):
    r = S.get(API, params={'action':'query','titles':title,'prop':'revisions','rvprop':'content','redirects':'1','format':'json'}).json()
    for p in r['query']['pages'].values():
        if 'revisions' in p:
            return p['revisions'][0]['*']
    return None

# full Pakiak article to file
pk = content('Pakiak')
with open(r'B:\02_GIT CONNECTED\wiki\pulls\2026-11-04_tabanan\Pakiak_full.txt', 'w', encoding='utf-8') as f:
    f.write(pk)
print('Pakiak chars:', len(pk))

# Almuria page via parse
r = S.get(API, params={'action':'parse','page':'Almuria','prop':'wikitext','format':'json'}).json()
if 'error' in r:
    print('Almuria parse error:', r['error']['code'])
else:
    print('Almuria parse EXISTS, chars:', len(r['parse']['wikitext']['*']))

# contexts
for t in ['Adonia', 'Foreign relations of Okaiken']:
    c = content(t)
    lines = c.split('\n')
    for i, l in enumerate(lines):
        if 'Pakiak' in l or 'Volistraya' in l or ('Almuria' in l and 'continent' in l.lower()):
            print(f'--- {t} L{i}:')
            print(l.strip())

# country data templates
for t in ['Template:Country data Pakiak', 'Template:Country data Volistraya', 'Template:Country data Tabanan']:
    c = content(t)
    print(t, ':', 'EXISTS' if c else 'missing', ('| ' + c[:150].replace('\n',' ')) if c else '')

# categories check
r = S.get(API, params={'action':'query','list':'allcategories','acprefix':'Countries in','aclimit':'50','format':'json'}).json()
print('Categories matching "Countries in":', [c['*'] for c in r['query']['allcategories']])
