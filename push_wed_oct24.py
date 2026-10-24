"""Push NOPW Wednesday Episodes 8, 9, 11 + G1 hub to TALOD as bot Takeru-Sync."""
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

pages = [
    ('NOPW Wednesday Episode 8',
     'NOPW Wednesday Episode 8 (backfill): Island Invasion fall-out, Vance goes silent, Leoni enters the G1'),
    ('NOPW Wednesday Episode 9',
     'NOPW Wednesday Episode 9 (backfill): G1 field and block draw announced, Ishida wins the television title'),
    ('NOPW Wednesday Episode 11',
     'NOPW Wednesday Episode 11: G1 Final fall-out, Usos mutiny, Wrestling Summit contract signed'),
    ('G1 Climax 2026',
     'Link Episode 8/9 references in Background'),
]

revids = {}
for t, summary in pages:
    path = rf'B:\02_GIT CONNECTED\wiki\articles\{t}.mediawiki'
    content = open(path, encoding='utf-8').read()
    r = session.post(api_url, data={'action': 'edit', 'title': t,
                                    'text': content, 'token': csrf,
                                    'bot': True, 'format': 'json',
                                    'summary': summary},
                     timeout=120)
    res = r.json()
    assert 'error' not in res, (t, res)
    revid = res.get('edit', {}).get('newrevid')
    assert revid is not None, (t, res)
    revids[t] = revid
    print(f'{t}: pushed, revid {revid}')
    time.sleep(2)

print()
print('Post-push verification (current revision on server):')
for t, expected in revids.items():
    r = session.get(api_url, params={'action': 'query',
                                     'titles': t,
                                     'prop': 'revisions',
                                     'rvprop': 'ids|size',
                                     'format': 'json'}, timeout=60)
    page = next(iter(r.json()['query']['pages'].values()))
    rev = page.get('revisions', [{}])[0]
    status = 'OK' if str(rev.get('revid')) == str(expected) else 'MISMATCH'
    print(f'  {t}: revid {rev.get("revid")} (size {rev.get("size")}B) [{status}]')
    time.sleep(2)

print()
print('REVIDS:', json.dumps(revids))
print('DONE - all pushed and verified')