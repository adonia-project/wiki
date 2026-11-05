# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import requests, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

img = Image.open(r'B:\02_GIT CONNECTED\map\Location of Tabanan.png').convert('RGBA')
a = np.array(img)
print('size:', img.size)
# count highlight pixels (terracotta ~ #b0532e)
hl = ((abs(a[:,:,0].astype(int)-176)<40) & (abs(a[:,:,1].astype(int)-83)<40) & (abs(a[:,:,2].astype(int)-46)<40)).sum()
grey = ((abs(a[:,:,0].astype(int)-200)<15) & (abs(a[:,:,1]-a[:,:,0])<8) & (abs(a[:,:,2]-a[:,:,0])<8)).sum()
print('highlight px:', hl, '| land grey px:', grey)
ys, xs = np.where((abs(a[:,:,0].astype(int)-176)<40) & (abs(a[:,:,1].astype(int)-83)<40) & (abs(a[:,:,2].astype(int)-46)<40))
if len(xs):
    print('highlight bbox: x', xs.min(), '-', xs.max(), ' y', ys.min(), '-', ys.max())

S = requests.Session()
S.headers['User-Agent'] = 'Takeru-Sync/1.0 (Okaiken project; contact: carlsotomil42)'
API = 'https://talod.miraheze.org/w/api.php'
for f in ['File:Flag of Almuria.png', 'File:Seal of Almuria.png', 'File:Flag of Pakiak.svg', 'File:Flag of Tabanan.svg']:
    r = S.get(API, params={'action':'query','titles':f,'format':'json'}).json()
    p = list(r['query']['pages'].values())[0]
    print(f, '->', 'EXISTS' if 'missing' not in p else 'missing')
