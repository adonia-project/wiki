import json, requests
API = 'https://talod.miraheze.org/w/api.php'
s = requests.Session(); s.headers['User-Agent'] = 'Takeru-Sync/1.0'
for t in ['Etawa','Winnipi']:
    r = s.get(API, params={'action':'query','titles':t,'prop':'revisions','rvprop':'content','format':'json'}).json()
    for p in r['query']['pages'].values():
        print('='*15, t, '='*15)
        print(p['revisions'][0]['*'])
