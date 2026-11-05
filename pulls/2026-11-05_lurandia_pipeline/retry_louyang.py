import json, requests
cfg = json.load(open(r'B:\02_GIT CONNECTED\wiki\sync_config.json'))
U, P = cfg['wiki']['bot_username'], cfg['wiki']['bot_password']
API = 'https://talod.miraheze.org/w/api.php'
s = requests.Session(); s.headers['User-Agent'] = 'Takeru-Sync/1.0'
r = s.post(API, data={'action':'login','lgname':U,'lgpassword':P,'format':'json'}).json()
r = s.post(API, data={'action':'login','lgname':U,'lgpassword':P,'lgtoken':r['login']['token'],'format':'json'}).json()
assert r['login']['result'] == 'Success', r
token = s.get(API, params={'action':'query','meta':'tokens','format':'json'}).json()['query']['tokens']['csrftoken']
fn = r'B:\02_GIT CONNECTED\map\Location of Louyang.svg'
with open(fn,'rb') as f:
    res = s.post(API, files={'file':('Location of Louyang.svg', f, 'image/svg+xml')},
        data={'action':'upload','filename':'Location of Louyang.svg','comment':'Location globe for Louyang (orthographic, house style)','ignorewarnings':1,'format':'json','token':token}).json()
print(json.dumps(res['upload'], indent=1)[:600])
