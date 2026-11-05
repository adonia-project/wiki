import requests, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
r = S.get('https://talod.miraheze.org/w/api.php', params={
    'action':'query','titles':'Pakiak|Almuria (continent)|Tabanan|Volistraya',
    'prop':'revisions','rvprop':'content','format':'json'}).json()
for p in r['query']['pages'].values():
    print('=====', p['title'], '=====')
    if 'revisions' in p:
        print(p['revisions'][0]['*'][:9000])
    else:
        print('[MISSING]')
