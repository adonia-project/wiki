import json, requests
cfg = json.load(open(r'B:\02_GIT CONNECTED\wiki\sync_config.json'))
U, P = cfg['wiki']['bot_username'], cfg['wiki']['bot_password']
API = 'https://talod.miraheze.org/w/api.php'
s = requests.Session(); s.headers['User-Agent'] = 'Takeru-Sync/1.0'
r = s.post(API, data={'action':'login','lgname':U,'lgpassword':P,'format':'json'}).json()
assert r['login']['result'] == 'NeedToken', r
r = s.post(API, data={'action':'login','lgname':U,'lgpassword':P,'lgtoken':r['login']['token'],'format':'json'}).json()
assert r['login']['result'] == 'Success', r
print('LOGIN OK')
token = s.get(API, params={'action':'query','meta':'tokens','format':'json'}).json()['query']['tokens']['csrftoken']
names = ['Balboa','Kalanua','Kawalidipa','Louyang','Markland','Mishko','Nawat','Neakyrena','Nuuchi','Sinchew','Tuvayo']
for n in names:
    fn = rf'B:\02_GIT CONNECTED\map\Location of {n}.svg'
    with open(fn,'rb') as f:
        res = s.post(API, files={'file':(f'Location of {n}.svg', f, 'image/svg+xml')},
            data={'action':'upload','filename':f'Location of {n}.svg','comment':f'Location globe for {n} (orthographic, house style)','format':'json','token':token}).json()
    print(n, res['upload'].get('result'), res['upload'].get('warnings',''))
