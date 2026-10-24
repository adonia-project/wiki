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

# 1. Debate article: Burawan objection to the separation-of-command provision
D1 = "October 2026 Diet debate on the Wolffrean War"
assert revid(D1) == 34658
wt = wikitext(D1)
wt = apply(wt, [
 ("Its separation-of-command provisions mandate that Sanese naval units remain under sovereign national command liaised to the AC Secretariat, legally barring subordination to the JWG-PNK coalition headquarters at [[Joint Base Ajowa]].",
  "Its separation-of-command provisions mandate that Sanese naval units remain under sovereign national command liaised to the AC Secretariat, legally barring subordination to the JWG-PNK coalition headquarters at [[Joint Base Ajowa]]. The provision drew a formal objection from [[Burawa]], the largest of the JWG-PNK lead nations, whose joint headquarters communiqu\u00e9 stated that a warship answering to no coalition command in a strike theater is a hazard to every vessel in it. The government replied that liaison through the AC Secretariat satisfied the requirement of deconfliction; Burawan state commentary, noting the ideological alignment of the two governments, did not moderate the demand, and the dispute remained unresolved at the close of the debate."),
])
edit(D1, wt, "add Burawan objection to sovereign national command (user directive)")

# 2. Emergency resolution: renewed objection in aftermath
D2 = "October 2026 Diet emergency resolution on the Wolffrean War"
assert revid(D2) == 34659
wt = wikitext(D2)
wt = apply(wt, [
 ("Sanese editorial commentary described the resolution as the [[Ikazaki Cabinet]]'s Fortress State doctrine applied to the sea.",
  "Sanese editorial commentary described the resolution as the [[Ikazaki Cabinet]]'s Fortress State doctrine applied to the sea. The reaffirmation of sovereign national command drew a renewed objection from [[Burawa]], a lead nation of the JWG-PNK command, which held that warships operating in the strike theater must accept coalition deconfliction authority; the Sanese position \u2014 liaison under the AC Secretariat without subordination of command \u2014 was unchanged, and the dispute remained open at the close of the night sitting."),
])
edit(D2, wt, "add Burawan objection to sovereign national command (user directive)")

# 3. 4942E: background context
D3 = "Adonian Community Resolution 4942E"
assert revid(D3) == 34660
wt = wikitext(D3)
wt = apply(wt, [
 ("Sanese naval units were barred by cabinet policy from subordination to the coalition headquarters of the Joint Working Group for Peace in Northern Kaftia.",
  "Sanese naval units were barred by cabinet policy from subordination to the coalition headquarters of the Joint Working Group for Peace in Northern Kaftia. The arrangement had been formally protested by [[Burawa]], a lead nation of the coalition command, which insisted that warships in the strike theater accept coalition deconfliction authority; Okaiken maintained that liaison through the AC Secretariat satisfied that requirement."),
])
edit(D3, wt, "add Burawan protest over command arrangement (background)")

print("ALL DONE")
