# -*- coding: utf-8 -*-
import requests, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
API = 'https://talod.miraheze.org/w/api.php'
out = r'B:\02_GIT CONNECTED\wiki\pulls\2026-11-04_tabanan'
pages = ['Pakiak','Almuria (continent)','Adonia','Foreign relations of Okaiken','Template:Members of the Adonian Community','Volistraya','Tabanan']
for p in pages:
    r = S.get(API, params={'action':'query','titles':p,'prop':'revisions','rvprop':'content','rvslots':'main','format':'json'}).json()
    for pid, pg in r['query']['pages'].items():
        if 'revisions' in pg:
            txt = pg['revisions'][0]['slots']['main']['*']
            fn = os.path.join(out, 'live_' + p.replace(' ','_').replace(':','_') + '.txt')
            open(fn,'w',encoding='utf-8').write(txt)
            print(p, '| chars', len(txt), '->', os.path.basename(fn))
        else:
            print(p, '| MISSING')
