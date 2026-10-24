import json, requests, sys
sys.stdout.reconfigure(encoding="utf-8")
API = "https://talod.miraheze.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent":"Takeru-Sync/1.0 (Letta agent; Okaiken wiki maintenance)"})
cfg = json.load(open(r"B:\02_GIT CONNECTED\wiki\sync_config.json", encoding="utf-8-sig"))
w = cfg["wiki"]

def login():
    t = S.get(API, params={"action":"query","meta":"tokens","type":"login","format":"json"}).json()["query"]["tokens"]["logintoken"]
    r = S.post(API, data={"action":"login","lgname":w["bot_username"],"lgpassword":w["bot_password"],"lgtoken":t,"format":"json"}).json()
    assert r.get("login",{}).get("result") == "Success", r
    print("login OK")

def revid(title):
    r = S.get(API, params={"action":"query","prop":"revisions","titles":title,"rvprop":"ids","format":"json"}).json()
    return list(r["query"]["pages"].values())[0].get("revisions",[{}])[0].get("revid")

def wikitext(title):
    return S.get(API, params={"action":"parse","page":title,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]

def edit(title, text, summary):
    tok = S.get(API, params={"action":"query","meta":"tokens","type":"csrf","format":"json"}).json()["query"]["tokens"]["csrftoken"]
    r = S.post(API, data={"action":"edit","title":title,"text":text,"summary":summary,"token":tok,"format":"json"}).json()
    assert "edit" in r and r["edit"].get("result") == "Success", json.dumps(r)[:300]
    print(f"OK {title} -> {r['edit'].get('newrevid')}")

def apply(wt, reps):
    for old, new in reps:
        n = wt.count(old)
        assert n == 1, f"expected 1, found {n}: {old[:70]!r}"
        wt = wt.replace(old, new, 1)
    return wt

login()

# 1. Debate article
D1 = "October 2026 Diet debate on the Wolffrean War"
assert revid(D1) == 34651
wt = wikitext(D1)
wt = apply(wt, [
 ("Operating under the defensive provisions of the [[Kurosawa Doctrine]] and the humanitarian umbrella of [[Adonian Community Resolution 4935]]",
  "Operating under the defensive provisions of the [[Constitution of Okaiken|Ninth Amendment]] and the humanitarian umbrella of [[Adonian Community Resolution 4935]]"),
 ("the Kurosawa Doctrine does not require us to cower behind the escarpments",
  "the Ninth Amendment does not require us to cower behind the escarpments"),
])
edit(D1, wt, "replace Kurosawa Doctrine with the Ninth Amendment's constitutional self-defence provisions (doctrine ended with the LDP government in 2016; the SCP government operates under the constitutional framework)")

# 2. Emergency resolution article
D2 = "October 2026 Diet emergency resolution on the Wolffrean War"
assert revid(D2) == 34652
wt = wikitext(D2)
wt = apply(wt, [
 ("operating under the defensive provisions of the [[Kurosawa Doctrine]] and remaining under sovereign national command",
  "operating under the defensive provisions of the [[Constitution of Okaiken|Ninth Amendment]] and remaining under sovereign national command"),
 ("remains under sovereign national command in accordance with the Kurosawa Doctrine",
  "remains under sovereign national command in accordance with the defensive provisions of the Ninth Amendment"),
 ("* [[Wolffrean War]]\r\n* [[Kurosawa Doctrine]]",
  "* [[Wolffrean War]]\r\n* [[Constitution of Okaiken]]"),
])
edit(D2, wt, "replace Kurosawa Doctrine with the Ninth Amendment (constitutional self-defence framework, government-independent)")

# 3. 4942E
D3 = "Adonian Community Resolution 4942E"
assert revid(D3) == 34653
wt = wikitext(D3)
wt = apply(wt, [
 ("The deployment operated under the defensive provisions of the Kurosawa Doctrine and remained under sovereign national command",
  "The deployment operated under the defensive provisions of the Ninth Amendment to the [[Constitution of Okaiken]] and remained under sovereign national command"),
])
edit(D3, wt, "replace Kurosawa Doctrine with the Ninth Amendment (constitutional self-defence framework)")

print("ALL DONE")
