import json, urllib.request, urllib.parse
titles = ['Amiera','Etawa','Winnipi','United Midlands','Sinchew','Balboa','Louyang','Kalanua','Kaneda','Kavik','Kawalidipa','Markland','Mishko','Nawat','Neakyrena','Nuuchi','Tuvayo','Template:Countries in Lurandia']
q = urllib.parse.urlencode({'action':'query','titles':'|'.join(titles),'format':'json'})
req = urllib.request.Request('https://talod.miraheze.org/w/api.php?'+q, headers={'User-Agent':'Takeru-Sync/1.0'})
r = json.load(urllib.request.urlopen(req))
for p in r['query']['pages'].values():
    print(('EXISTS ' if 'missing' not in p else 'MISSING'), p['title'], p.get('pageid',''))
