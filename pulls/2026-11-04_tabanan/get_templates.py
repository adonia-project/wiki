# -*- coding: utf-8 -*-
import requests, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
API = 'https://talod.miraheze.org/w/api.php'
r = S.get(API, params={'action':'query','titles':'Template:Country data Louyan|Template:Country data Ntungwe','prop':'revisions','rvprop':'content','format':'json'}).json()
for p in r['query']['pages'].values():
    print('=====', p['title'], '=====')
    print(p['revisions'][0]['*'] if 'revisions' in p else '[missing]')
