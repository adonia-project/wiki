import json, urllib.request, urllib.parse
def get(title):
    q = urllib.parse.urlencode({'action':'query','titles':title,'prop':'revisions','rvprop':'content','format':'json'})
    req = urllib.request.Request('https://talod.miraheze.org/w/api.php?'+q, headers={'User-Agent':'Takeru-Sync/1.0'})
    r = json.load(urllib.request.urlopen(req))
    for p in r['query']['pages'].values():
        if 'revisions' in p: return p['revisions'][0]['*']
    return None
for t in ['Template:Countries in Lurandia','Sinchew','Amiera']:
    c = get(t)
    print('='*20, t, '='*20)
    print(c)
