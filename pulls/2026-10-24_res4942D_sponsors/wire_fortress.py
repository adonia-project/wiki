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

# 1. Debate article: narrative basis + package sentence
D1 = "October 2026 Diet debate on the Wolffrean War"
assert revid(D1) == 34655
wt = wikitext(D1)
wt = apply(wt, [
 ("Operating under the defensive provisions of the [[Constitution of Okaiken|Ninth Amendment]] and the humanitarian umbrella of [[Adonian Community Resolution 4935]], the Sanese naval group was tasked",
  "Operating under the defensive provisions of the [[Constitution of Okaiken|Ninth Amendment]], the Fortress State policy of the [[Ikazaki Cabinet]], and the humanitarian umbrella of [[Adonian Community Resolution 4935]], the Sanese naval group was tasked"),
 ("The package was brought to the floor for a sequential vote on the afternoon of 24 October.",
  "The package was brought to the floor for a sequential vote on the afternoon of 24 October. Government spokesmen described it as the Fortress State doctrine given statutory form: defensive sufficiency, civilian protection, and no expeditionary force."),
])
edit(D1, wt, "ground the debate in the Ikazaki Cabinet's Fortress State policy alongside the Ninth Amendment (user directive)")

# 2. Emergency resolution: narrative basis + aftermath sentence
D2 = "October 2026 Diet emergency resolution on the Wolffrean War"
assert revid(D2) == 34656
wt = wikitext(D2)
wt = apply(wt, [
 ("operating under the defensive provisions of the [[Constitution of Okaiken|Ninth Amendment]] and remaining under sovereign national command",
  "operating under the defensive provisions of the [[Constitution of Okaiken|Ninth Amendment]] and the Fortress State policy of the [[Ikazaki Cabinet]], and remaining under sovereign national command"),
 ("adopted a concurrent resolution by voice vote in a late sitting the same night without amendment.",
  "adopted a concurrent resolution by voice vote in a late sitting the same night without amendment. Sanese editorial commentary described the resolution as the [[Ikazaki Cabinet]]'s Fortress State doctrine applied to the sea."),
])
edit(D2, wt, "ground the emergency session in the Fortress State policy alongside the Ninth Amendment (user directive)")

# 3. 4942E: deployment basis
D3 = "Adonian Community Resolution 4942E"
assert revid(D3) == 34657
wt = wikitext(D3)
wt = apply(wt, [
 ("The deployment operated under the defensive provisions of the Ninth Amendment to the [[Constitution of Okaiken]] and remained under sovereign national command",
  "The deployment operated under the defensive provisions of the Ninth Amendment to the [[Constitution of Okaiken]] and the Fortress State policy of the [[Ikazaki Cabinet]], and remained under sovereign national command"),
])
edit(D3, wt, "add Fortress State policy as co-basis of the escort deployment (consistency with Diet cluster)")

# 4. Kousuke Ikazaki: fix double-quote artifact
D4 = "Kousuke Ikazaki"
wt = wikitext(D4)
wt = apply(wt, [
 ('the ""Fortress State"" doctrine\'s credibility',
  'the "Fortress State" doctrine\'s credibility'),
])
edit(D4, wt, "fix doubled quotation marks around Fortress State (typo)")

print("ALL DONE")
