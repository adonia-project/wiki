import json, requests
API = 'https://talod.miraheze.org/w/api.php'
s = requests.Session(); s.headers['User-Agent'] = 'Takeru-Sync/1.0'
def get(t):
    r = s.get(API, params={'action':'query','titles':t,'prop':'revisions','rvprop':'ids|content','format':'json'}).json()
    for p in r['query']['pages'].values():
        return p['revisions'][0]
for t in ['Kalanua','Balboa','Winnipi']:
    rv = get(t)
    c = rv['*']
    checks = {
        'navbox': '{{Countries in Lurandia}}' in c,
        'infobox': '{{Infobox country' in c,
        'map svg': 'Location of %s.svg' % t in c,
        'stub tag': '{{Stub}}' in c,
        'no artifact': "+ '" not in c and "@'" not in c,
        'cats': '[[Category:Countries in Lurandia]]' in c or '[[Category:' in c,
    }
    print(t, 'revid', rv['revid'], checks)
