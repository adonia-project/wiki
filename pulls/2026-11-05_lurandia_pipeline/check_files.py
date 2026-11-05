import json, urllib.request, urllib.parse
names = ['Amiera','Balboa','Etawa','Kalanua','Kaneda','Kavik','Kawalidipa','Louyang','Markland','Mishko','Nawat','Neakyrena','Nuuchi','Sinchew','Tuvayo','United Midlands','Winnipi']
titles = ['File:Location of %s.svg' % n for n in names]
q = urllib.parse.urlencode({'action':'query','titles':'|'.join(titles),'format':'json'})
req = urllib.request.Request('https://talod.miraheze.org/w/api.php?'+q, headers={'User-Agent':'Takeru-Sync/1.0'})
r = json.load(urllib.request.urlopen(req))
have, miss = [], []
for p in r['query']['pages'].values():
    n = p['title'].replace('File:Location of ','').replace('.svg','')
    (have if 'missing' not in p else miss).append(n)
print('HAVE SVG:', sorted(have))
print('NEED SVG:', sorted(miss))
