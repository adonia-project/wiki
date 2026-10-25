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

login()

# --- 4942D ---
D = "Adonian Community Resolution 4942D"
rv = revid(D)
if rv != 34636: print("ABORT 4942D changed:", rv); sys.exit(1)
wt = wikitext(D)
open(r"B:\02_GIT CONNECTED\wiki\pulls\2026-10-24_res4942D_sponsors\4942D_before.txt","w",encoding="utf-8").write(wt)

old_spon = "| sponsors = {{ubl|{{flagicon|Okaiken}} [[Okaiken]]|{{flagicon|Yanbaru}} [[Yanbaru]]|{{flagicon|Dagit}} [[Dagit]]}}"
new_spon = "| sponsors = {{ubl|{{flagicon|Okaiken}} [[Okaiken]]|{{flagicon|Yanbaru}} [[Yanbaru]]|{{flagicon|Dagit}} [[Dagit]]|{{flagicon|Echia}} [[Echia]]|{{flagicon|Pavia}} [[Pavia]]|{{flagicon|Tortona}} [[Tortona]]|{{flagicon|Rufusia}} [[Rufusia]]|{{flagicon|Kavik}} [[Kavik]]|{{flagicon|Vaiahi Islands}} [[Vaiahi Islands]]}}"
assert old_spon in wt; wt = wt.replace(old_spon, new_spon, 1)

old_lead = "submitted by [[Okaiken]] on 24 October 2026 and co-sponsored by [[Yanbaru]] and [[Dagit]]."
new_lead = "submitted by [[Okaiken]] on 24 October 2026, co-sponsored at its introduction by [[Yanbaru]] and [[Dagit]], and by [[Echia]], [[Pavia]], [[Tortona]], [[Rufusia]], [[Kavik]] and the [[Vaiahi Islands]] by the end of October."
assert old_lead in wt; wt = wt.replace(old_lead, new_lead, 1)

growth = """
=== Growth of the co-sponsorship ===

The [[October 2026 Diet emergency resolution on the Wolffrean War|emergency resolution adopted by the Diet on 27 October]] directed the government to pursue the draft's adoption and to seek co-sponsorships among member states. In the days that followed, the co-sponsorship grew from three sponsors to nine.

On 28 October, the delegation of [[Echia]] acceded to the co-sponsorship, followed within a day by those of [[Pavia]], [[Tortona]] and [[Rufusia]]. The four delegations — described in diplomatic reporting as the "Echian block" — circulated a joint memorandum describing the draft as the first text before the Assembly to write the protection of civilian shipping into law rather than leave it to the discretion of belligerents, and citing the exposure of their merchant fleets in wartime waters. The accessions were widely read as a rebuff to draft [[Adonian Community Resolution 4942E|4942E]]; none of the four joined the Sindewand text's co-sponsorship.

On 29 October, [[Kavik]] and the [[Vaiahi Islands]] acceded. The Kavik delegation cited the protection of small-state shipping far from home waters and the interests of the Kavik Sanese community; the Vaiahi delegation, representing an East Fosian Sphere partner of Okaiken whose seafarers serve widely aboard Sanese-flagged merchant hulls, described the fifteen-nautical-mile protection zone as "the difference between the sea as a highway and the sea as a lottery."

With nine sponsors, the draft remained eleven short of the twenty member states required to enter discussion without the approval of the [[Committee on Resolutions]]. Reporting at the end of October noted that draft 4942E had attracted no co-sponsor beyond its sponsor state, while the co-sponsorship of 4942D continued to grow.

Should the draft be confirmed for floor debate"""
old_tail = "\nShould the draft be confirmed for floor debate"
assert old_tail in wt; wt = wt.replace(old_tail, growth, 1)
edit(D, wt, "Echian block (Echia, Pavia, Tortona, Rufusia), Kavik and Vaiahi Islands join co-sponsorship (28-29 Oct); sponsors now nine")

# --- emergency resolution article aftermath ---
R = "October 2026 Diet emergency resolution on the Wolffrean War"
rv = revid(R)
if rv != 34646: print("ABORT resolution article changed:", rv); sys.exit(1)
wt = wikitext(R)
old = "The Committee on Resolutions continued to hold draft 4942E without discussion as of the end of October, while draft 4942D remained pending with its three original sponsors."
new = "The co-sponsorship diplomacy directed by the resolution bore fruit within days: between 28 and 29 October, Echia, Pavia, Tortona and Rufusia — the Echian block — acceded to the co-sponsorship of draft Resolution 4942D, followed by Kavik and the Vaiahi Islands, bringing its sponsors to nine while draft 4942E attracted none. The Committee on Resolutions continued to hold draft 4942E without discussion as of the end of October, while draft 4942D remained pending with its expanded co-sponsorship."
assert old in wt; wt = wt.replace(old, new, 1)
edit(R, wt, "aftermath: co-sponsorship diplomacy results - Echian block, Kavik, Vaiahi Islands join 4942D (nine sponsors)")
print("ALL DONE")
