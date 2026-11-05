import json, requests, urllib.parse
API = 'https://talod.miraheze.org/w/api.php'
s = requests.Session(); s.headers['User-Agent'] = 'Takeru-Sync/1.0'
q = {'action':'query','titles':'File:Location of Louyang.svg|File:Location of Louyang.png','format':'json'}
r = s.get(API, params=q).json()
for p in r['query']['pages'].values():
    print(('EXISTS ' if 'missing' not in p else 'MISSING'), p['title'], p.get('pageid',''))
