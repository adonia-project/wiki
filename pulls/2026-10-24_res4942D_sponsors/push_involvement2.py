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

D = "Adonian Community Resolution 4942D"
wt = S.get(API, params={"action":"parse","page":D,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]
nl = "\r\n" if "\r\n" in wt else "\n"
tail = 'directed at the provision that replaced the private route-notification channel whose 20 October leak had seen both sides accuse the intermediaries of passing targeting intelligence.'
assert wt.count(tail) == 1, ("tail", wt.count(tail))
content = tail + nl + nl + "=== Response of the sponsoring state ===" + nl + nl + "{{Main|Sanese involvement in the Wolffrean War}}" + nl + nl + "On the afternoon of 25 October, with demands that the escort flotilla be brought under AC or coalition command pressed from three directions and Louyan's dismissal motion pending, the Ministry of Foreign Affairs issued a formal response in the name of Foreign Minister [[Kenichi Mori]]. The statement reiterated that Okaiken is not a belligerent and will not become one; that under the [[Ninth Amendment]] the protection of Sanese ships and crews belongs to Okaiken alone, \"whether a hull is leased to the Community or is not\"; that \"coordination is not command, and participation is not subordination\"; and — invoking the 925 Sanese personnel who served under a Community command in the [[Adonian Community Mission for Lacashe]] — that Okaiken is \"bound by the treaties it has signed, and by nothing else.\" The full statement and its context are set out in [[Sanese involvement in the Wolffrean War]]."
wt = wt.replace(tail, content, 1)
tok = S.get(API, params={"action":"query","meta":"tokens","type":"csrf","format":"json"}).json()["query"]["tokens"]["csrftoken"]
r = S.post(API, data={"action":"edit","title":D,"text":wt,"summary":"Okaiken's formal response of 25 October (Ninth Amendment, Lacashe precedent)","token":tok,"format":"json"}).json()
assert "edit" in r and r["edit"].get("result") == "Success", json.dumps(r)[:300]
print(f"OK {D} -> {r['edit'].get('newrevid')}")

# verify both pages
for p in [D, "Sanese involvement in the Wolffrean War"]:
    c = S.get(API, params={"action":"parse","page":p,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]
    print(p, len(c), "ch | Lacashe:", c.count("Lacashe"), "| Ninth:", c.count("Ninth Amendment"))
open(r"B:\02_GIT CONNECTED\wiki\pulls\2026-10-24_res4942D_sponsors\pull_4942D.txt", "w", encoding="utf-8", newline="\n").write(wt)
print("DONE")
