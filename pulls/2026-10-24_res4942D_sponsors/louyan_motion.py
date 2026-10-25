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

def wikitext(title):
    return S.get(API, params={"action":"parse","page":title,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]

def edit(title, text, summary):
    tok = S.get(API, params={"action":"query","meta":"tokens","type":"csrf","format":"json"}).json()["query"]["tokens"]["csrftoken"]
    r = S.post(API, data={"action":"edit","title":title,"text":text,"summary":summary,"token":tok,"format":"json"}).json()
    assert "edit" in r and r["edit"].get("result") == "Success", json.dumps(r)[:300]
    print(f"OK {title} -> {r['edit'].get('newrevid')}")

login()
D = "Adonian Community Resolution 4942D"
wt = wikitext(D)
nl = "\r\n" if "\r\n" in wt else "\n"

# 1. Lead co-sponsor list: add Pangkajene (infobox already lists it as 10th sponsor)
old = "[[Kavik]] and the [[Vaiahi Islands]] by the end of October."
assert wt.count(old) == 1, ("lead", wt.count(old))
wt = wt.replace(old, "[[Kavik]], the [[Vaiahi Islands]] and [[Pangkajene]] by the end of October.", 1)

# 2. Sponsor counts nine -> ten (match infobox)
old = "the co-sponsorship grew from three sponsors to nine."
assert wt.count(old) == 1, ("c1", wt.count(old))
wt = wt.replace(old, "the co-sponsorship grew from three sponsors to ten.", 1)
old = "With nine sponsors, the draft remained eleven short"
assert wt.count(old) == 1, ("c2", wt.count(old))
wt = wt.replace(old, "With ten sponsors, the draft remained ten short", 1)

# 3. Insert Louyan motion + Ayorin reservation after the Zong ambassador subsection
tail = "that the escort group be brought under the direction of the command the AC already exercises over its own naval forces."
assert wt.count(tail) == 1, ("tail", wt.count(tail))
content = (
tail + nl + nl +
"=== Motion to dismiss (Louyan) ===" + nl + nl +
"On 25 October 2026, the delegation of [[Louyan]] gave notice of a motion to dismiss the draft, to be moved when the [[Committee on Resolutions]] convenes on the text on Monday 26 October. The Louyan emissary argued that the resolution was redundant in its operative parts: the Adonian Community Military (ACM) already has systems in place for investigating the ''Aozora Maru'' attack, self-defence rules already exist and are defined by the admirals, and the shipping lanes are already guaranteed by the convoys themselves. The bill, the delegation argued, is meant to add unneeded bureaucracy to the operation of the ACM. The underlying question posed by the three points, in the delegation's framing, was whether the AC civilian government should micromanage the AC Secretariat." + nl + nl +
"The emissary's final point went to the draft's fourth provision. The ban on ground troops and the separation from coalition command, the delegation argued, acts as a rider to the resolution, and Louyan proposed that the provision be split from the text for its own discussion. Louyan, which is not among the draft's co-sponsors and has no vessels in the operation, framed its objection as institutional rather than operational. The committee had dismissed a draft, 4942C, as recently as 21 October." + nl + nl +
"=== Reservation of Ayorin ===" + nl + nl +
"The representative of [[Ayorin]] remarked that the draft's deconfliction system, under which the [[Adonian Community Observer Mission in Northern Kaftia]] broadcasts the routes and transponder identifiers of evacuation convoys to all parties including the Wolffrean and Bonandian governments, would report the position of evacuation ships to enemy combatants. Reporting transponder messages for evacuation ships to enemy combatants, the representative stated, is \"incredibly dangerous and not a good strategy for evacuating people.\" The remark came from a delegation of a JWG-PNK coalition state, and was directed at the provision that replaced the private route-notification channel whose 20 October leak had seen both sides accuse the intermediaries of passing targeting intelligence."
)
wt = wt.replace(tail, content, 1)

edit(D, wt, "Louyan motion to dismiss (rider split proposal) + Ayorin transponder reservation; sponsor counts to ten (Pangkajene)")
print("DONE")
