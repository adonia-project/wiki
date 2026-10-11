"""Push G1 hub + Days 16/17/18 to TALOD as bot Takeru-Sync."""
import requests, json, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'B:\02_GIT CONNECTED\wiki\sync_config.json', 'r') as f:
    config = json.load(f)

api_url = config['wiki']['url']
username = config['wiki']['bot_username']
password = config['wiki']['bot_password']

session = requests.Session()
session.headers.update({'User-Agent': 'Takeru-Sync/1.0'})

r = session.get(api_url, params={'action': 'query', 'meta': 'tokens',
                                 'type': 'login', 'format': 'json'}, timeout=60)
token = r.json()['query']['tokens']['logintoken']
r = session.post(api_url, data={'action': 'login', 'lgname': username,
                                 'lgpassword': password, 'lgtoken': token,
                                 'format': 'json'}, timeout=60)
assert r.json().get('login', {}).get('result') == 'Success', r.text
print('Logged in as', username)

r = session.get(api_url, params={'action': 'query', 'meta': 'tokens',
                                 'format': 'json'}, timeout=60)
csrf = r.json()['query']['tokens']['csrftoken']

titles = ['G1 Climax 2026 Day 16', 'G1 Climax 2026 Day 17', 'G1 Climax 2026 Day 18', 'G1 Climax 2026']
for t in titles:
    path = rf'B:\02_GIT CONNECTED\wiki\articles\{t}.mediawiki'
    content = open(path, encoding='utf-8').read()
    r = session.post(api_url, data={'action': 'edit', 'title': t,
                                    'text': content, 'token': csrf,
                                    'bot': True, 'format': 'json',
                                    'summary': f'G1 Climax 2026 update ({t})'},
                     timeout=120)
    res = r.json()
    assert 'error' not in res, (t, res)
    revid = res.get('edit', {}).get('newrevid')
    if revid is None:
        print(f'{t}: WARNING - no newrevid! Response: {res}')
    else:
        print(f'{t}: pushed, revid {revid}')
    time.sleep(2)

print('DONE - all pushed')
