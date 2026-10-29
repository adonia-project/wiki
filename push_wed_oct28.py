"""Push NOPW Wednesday Episodes 12, 13 + Marauder streak fixes to TALOD as bot Takeru-Sync."""
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
    ('NOPW Wednesday Episode 12',
     'NOPW Wednesday Episode 12: Power Struggle road opens, Leoni ends the Marauder streak, Vance raises one finger'),
    ('NOPW Wednesday Episode 13',
     'NOPW Wednesday Episode 13: Power Struggle build escalates, Leoni protects the road to Toyozawa'),
    ('Island Invasion Tour 2026',
     'Correct Marauder streak: 3-0 in singles (Morita twice, Iwata once), first victim at Episode 5'),
    ('NOPW Wednesday Episode 6',
     'Correct Marauder streak: Episode 6 win was his second, not third'),
    ('NOPW Wednesday Episode 7',
     'Correct Marauder streak: 3-0 in singles on Wednesday nights (four references)'),
]

revids = {}
for t, summary in pages:
    path = rf'B:\02_GIT CONNECTED\wiki\articles\{t}.mediawiki'
    content = open(path, encoding='utf-8').read()
    r = session.post(api_url, data={'action': 'edit', 'title': t,
                                    'text': content, 'token': csrf,
                                    'bot': True, 'format': 'json',
                                    'summary': summary}, timeout=120)
    res = r.json()
    assert 'error' not in res, (t, res)
    revid = res.get('edit', {}).get('newrevid')
    assert revid is not None, (t, res)
    revids[t] = revid
    print(f'{t}: pushed, revid {revid}')
    time.sleep(2)

print()
print('Post-push verification (current revision on server):')
ok = True
for t, expected in revids.items():
    r = session.get(api_url, params={'action': 'query',
                                     'titles': t,
                                     'prop': 'revisions',
                                     'rvprop': 'ids',
                                     'format': 'json'}, timeout=60)
    pages_res = r.json()['query']['pages']
    info = list(pages_res.values())[0]
    cur = info.get('revisions', [{}])[0].get('revid')
    status = 'OK' if cur == expected else 'MISMATCH'
    if cur != expected:
        ok = False
    print(f'  {t}: server revid {cur} (expected {expected}) -> {status}')
print()
print('ALL VERIFIED' if ok else 'VERIFICATION FAILED')
