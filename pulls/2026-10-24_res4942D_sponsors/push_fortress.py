import json, requests, sys
sys.stdout.reconfigure(encoding="utf-8")
API = "https://talod.miraheze.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent":"Takeru-Sync/1.0 (Letta agent; Okaiken wiki maintenance)"})
cfg = json.load(open(r"B:\02_GIT CONNECTED\wiki\sync_config.json", encoding="utf-8-sig"))
w = cfg["wiki"]
t = S.get(API, params={"action":"query","meta":"tokens","type":"login","format":"json"}).json()["query"]["tokens"]["logintoken"]
r = S.post(API, data={"action":"login","lgname":w["bot_username"],"lgpassword":w["bot_password"],"lgtoken":t,"format":"json"}).json()
assert r.get("login",{}).get("result") == "Success", r
print("login OK")

T = "Fortress State"
art = open(r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Fortress State.mediawiki", encoding="utf-8-sig").read()
tok = S.get(API, params={"action":"query","meta":"tokens","type":"csrf","format":"json"}).json()["query"]["tokens"]["csrftoken"]
r = S.post(API, data={"action":"edit","title":T,"text":art,"summary":"Create: Yōsai Kokka, the governing doctrine of the Ikazaki Cabinet","token":tok,"createonly":"1","format":"json"}).json()
assert "edit" in r and r["edit"].get("result") == "Success", json.dumps(r)[:300]
print(f"OK {T} -> {r['edit'].get('newrevid')}")
v = S.get(API, params={"action":"parse","page":T,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]
print("verify:", len(v), "ch | Yōsai:", v.count("Yōsai"), "| Ninety:", v.count("ninety"), "| Kuronomics:", v.count("Kuronomics"))
print("DONE")
