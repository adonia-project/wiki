import requests, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
API = 'https://talod.miraheze.org/w/api.php'
# backlinks to Pakiak
r = S.get(API, params={'action':'query','list':'backlinks','bltitle':'Pakiak','bllimit':'100','format':'json'}).json()
print('Backlinks to Pakiak:')
for b in r['query']['backlinks']:
    print(' -', b['title'])
# check specific pages
r2 = S.get(API, params={'action':'query','titles':'Almuria|List of Almurian countries|Bayani language|Treaty of Dharuk|Guild of Almuria|The Five Families|History of Almuria|Muri people','prop':'revisions','rvprop':'ids|size','redirects':'1','format':'json'}).json()
print('\nPage status:')
for p in r2['query']['pages'].values():
    print(' -', p['title'], 'missing' if 'missing' in p else f"size={p['revisions'][0]['size']}")
print('\nRedirects:', r2['query'].get('redirects'))
