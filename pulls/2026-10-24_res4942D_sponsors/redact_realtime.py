import json, requests, sys
sys.stdout.reconfigure(encoding="utf-8")
API = "https://talod.miraheze.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "Takeru-Sync/1.0 (Letta agent; Okaiken wiki maintenance)"})
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
        assert n == 1, f"expected 1 occurrence, found {n}: {old[:70]!r}"
        wt = wt.replace(old, new, 1)
    return wt

login()

# ---------- 1. Diet debate article: 24-25 Oct -> 23-24 Oct ----------
D1 = "October 2026 Diet debate on the Wolffrean War"
assert revid(D1) == 34648, "debate revid moved"
wt = wikitext(D1)
reps = [
 ("| date          = 24–25 October 2026", "| date          = 23–24 October 2026"),
 ("emergency debate held in the [[House of Commoners of Okaiken]] on 24–25 October 2026", "emergency debate held in the [[House of Commoners of Okaiken]] on 23–24 October 2026"),
 ("By 24 October, intelligence confirmed", "By 23 October, intelligence confirmed"),
 ("== Plenary debates (24–25 October 2026) ==", "== Plenary debates (23–24 October 2026) =="),
 ("convened at 14:00 on 24 October", "convened at 14:00 on 23 October"),
 ("Overnight on 24 October, Cabinet Secretariat staff", "Overnight on 23 October, Cabinet Secretariat staff"),
 ("sequential vote on the afternoon of 25 October", "sequential vote on the afternoon of 24 October"),
 ("On the afternoon of 25 October 2026, the four measures", "On the afternoon of 24 October 2026, the four measures"),
 ("Vote on Motion of No Confidence in Foreign Minister Kenichi Mori (25 October 2026)", "Vote on Motion of No Confidence in Foreign Minister Kenichi Mori (24 October 2026)"),
 ("strike notice on the evening of 25 October", "strike notice on the evening of 24 October"),
 ("On 26 October, confirmation reached Okami that the Sindewand delegation had submitted draft [[Adonian Community Resolution 4942E]] to the Adonian Assembly", "On the evening of 24 October, confirmation reached Okami that the Sindewand delegation had submitted draft [[Adonian Community Resolution 4942E]] to the Adonian Assembly"),
 ("convened an extraordinary session on 27 October and adopted", "convened an extraordinary session the same night and adopted"),
]
wt = apply(wt, reps)
edit(D1, wt, "re-date debate to 23-24 October; compress response chain to 24 October (real-time chronology, no events narrated ahead of the present)")

# ---------- 2. Emergency resolution article: 27 Oct -> night sitting 24 Oct ----------
D2 = "October 2026 Diet emergency resolution on the Wolffrean War"
assert revid(D2) == 34650, "resolution revid moved"
wt = wikitext(D2)
reps = [
 ("| date          = 27 October 2026", "| date          = 24 October 2026"),
 ("Concurrent resolution adopted by the [[House of Officers of Okaiken]] (28 October)", "Concurrent resolution adopted by the [[House of Officers of Okaiken]] (same night)"),
 ("was an emergency resolution adopted by the [[House of Commoners of Okaiken]] on 27 October 2026, two days after the conclusion of the [[October 2026 Diet debate on the Wolffrean War|October emergency debate]].", "was an emergency resolution adopted by the [[House of Commoners of Okaiken]] in a night sitting on 24 October 2026, hours after the conclusion of the [[October 2026 Diet debate on the Wolffrean War|October emergency debate]]."),
 ("On 24–25 October 2026, the House of Commoners had adopted", "On 23–24 October 2026, the House of Commoners had adopted"),
 ("On 24 October, the same day the emergency debate opened in Okami, the delegation of Sindewand submitted draft Resolution 4942E", "On 24 October, the closing day of the emergency debate in Okami, the delegation of Sindewand submitted draft Resolution 4942E"),
 ("Confirmation of the referral reached the Sanese delegation on 26 October, and the Speaker convened an extraordinary session of the House of Commoners for the following morning on the government's request.", "Confirmation of the referral reached the Sanese delegation on the evening of 24 October, and the Speaker convened an extraordinary night session of the House of Commoners on the government's request."),
 ("Vote on the Emergency Resolution (27 October 2026)", "Vote on the Emergency Resolution (night sitting, 24 October 2026)"),
 ("The remark drew formal protest from the Sindewand delegation the following day; the Prime Minister's office declined to withdraw it.", "The remark drew formal protest from the Sindewand delegation within hours; the Prime Minister's office declined to withdraw it."),
 ("Delegation diplomacy in the following week concentrated on the twenty-member co-sponsorship threshold.", "Delegation diplomacy concentrated on the twenty-member co-sponsorship threshold."),
 ("adopted a concurrent resolution by voice vote on 28 October without amendment", "adopted a concurrent resolution by voice vote in a late sitting the same night without amendment"),
 ("bore fruit within days: between 28 and 29 October, Echia, Pavia, Tortona and Rufusia — the Echian block — acceded to the co-sponsorship of draft Resolution 4942D, followed by Kavik and the Vaiahi Islands, bringing its sponsors to nine while draft 4942E attracted none.", "bore fruit within hours: on the evening of 24 October, Echia, Pavia, Tortona and Rufusia — the Echian block — acceded to the co-sponsorship of draft Resolution 4942D, followed by Kavik and the Vaiahi Islands, bringing its sponsors to nine by the end of the day while draft 4942E attracted none."),
 ("as of the end of October, while draft 4942D remained pending", "as of the end of 24 October, while draft 4942D remained pending"),
]
wt = apply(wt, reps)
edit(D2, wt, "re-date emergency session to night sitting of 24 October; House of Officers same night; accessions same evening (real-time chronology)")

# ---------- 3. 4942E article (Shub's): align dates ----------
D3 = "Adonian Community Resolution 4942E"
assert revid(D3) == 34647, "4942E revid moved"
wt = wikitext(D3)
reps = [
 ("On 24 October the House of Commoners of Okaiken convened an emergency debate on the war, and on 25 October it adopted the October Maritime Security and Non-Belligerence Legislative Package.", "On 23 October the House of Commoners of Okaiken convened an emergency debate on the war, and on 24 October it adopted the October Maritime Security and Non-Belligerence Legislative Package."),
 ("on 24 October 2026, the opening day of the emergency debate in the House of Commoners of Okaiken.", "on 24 October 2026, the closing day of the emergency debate in the House of Commoners of Okaiken."),
 ("As of 25 October 2026, the draft has not entered discussion.", "As of 24 October 2026, the draft has not entered discussion."),
 ("On 27 October 2026, the [[House of Commoners of Okaiken]] adopted an [[October 2026 Diet emergency resolution on the Wolffrean War|emergency resolution]]", "On the night of 24 October 2026, the [[House of Commoners of Okaiken]] adopted an [[October 2026 Diet emergency resolution on the Wolffrean War|emergency resolution]]"),
]
wt = apply(wt, reps)
edit(D3, wt, "align dates with real-time chronology: debate 23-24 Oct, emergency resolution night of 24 Oct")

# ---------- 4. 4942D article: accessions same day ----------
D4 = "Adonian Community Resolution 4942D"
assert revid(D4) == 34649, "4942D revid moved"
wt = wikitext(D4)
reps = [
 ("and reports on 24 October that [[Joint Working Group for Peace in Northern Kaftia]] (JWG-PNK) amphibious landing craft were gathering", "and reports on 23 October that [[Joint Working Group for Peace in Northern Kaftia]] (JWG-PNK) amphibious landing craft were gathering"),
 ("On 24 October 2026, reports circulated that coalition military forces", "On 23 October 2026, reports circulated that coalition military forces"),
 ("emergency resolution adopted by the Diet on 27 October]] directed the government to pursue the draft's adoption and to seek co-sponsorships among member states. In the days that followed, the co-sponsorship grew from three sponsors to nine.", "emergency resolution adopted by the Diet on the night of 24 October]] directed the government to pursue the draft's adoption and to seek co-sponsorships among member states. Within hours, the co-sponsorship grew from three sponsors to nine."),
 ("On 28 October, the delegation of [[Echia]] acceded to the co-sponsorship, followed within a day by those of [[Pavia]], [[Tortona]] and [[Rufusia]].", "On the evening of 24 October, the delegation of [[Echia]] acceded to the co-sponsorship, followed within hours by those of [[Pavia]], [[Tortona]] and [[Rufusia]]."),
 ("On 29 October, [[Kavik]] and the [[Vaiahi Islands]] acceded.", "Later that night, [[Kavik]] and the [[Vaiahi Islands]] acceded."),
 ("Reporting at the end of October noted that draft 4942E had attracted no co-sponsor beyond its sponsor state, while the co-sponsorship of 4942D continued to grow.", "By the end of the day, draft 4942E had attracted no co-sponsor beyond its sponsor state, while the co-sponsorship of 4942D had tripled."),
]
wt = apply(wt, reps)
edit(D4, wt, "re-date co-sponsorship accessions to the evening of 24 October (real-time chronology)")

print("ALL DONE")
