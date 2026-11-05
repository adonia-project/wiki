import requests, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
API = 'https://talod.miraheze.org/w/api.php'

def get_page(title):
    r = S.get(API, params={'action':'query','titles':title,'prop':'revisions','rvprop':'content','redirects':'1','format':'json'}).json()
    for p in r['query']['pages'].values():
        if 'revisions' in p:
            return p['title'], p['revisions'][0]['*']
    return title, None

# Almuria redirect?
r = S.get(API, params={'action':'query','titles':'Almuria','redirects':'1','format':'json'}).json()
print('Almuria query:', r['query'])

for t in ['Adonia', 'Foreign relations of Okaiken', 'Template:Members of the Adonian Community']:
    title, content = get_page(t)
    print('\n=====', title, '=====')
    if content is None:
        print('[missing]'); continue
    lines = content.split('\n')
    hits = [(i, l.strip()[:220]) for i, l in enumerate(lines) if 'Pakiak' in l or 'Volistraya' in l]
    for i, l in hits:
        print(f'  L{i}: {l}')
    if not hits:
        print('  [no Pakiak/Volistraya mentions]')
