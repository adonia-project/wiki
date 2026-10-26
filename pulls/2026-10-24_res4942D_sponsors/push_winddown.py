import json, requests, sys, re
sys.stdout.reconfigure(encoding="utf-8")
API = "https://talod.miraheze.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent":"Takeru-Sync/1.0 (Letta agent; Okaiken wiki maintenance)"})
cfg = json.load(open(r"B:\02_GIT CONNECTED\wiki\sync_config.json", encoding="utf-8-sig"))
w = cfg["wiki"]
t = S.get(API, params={"action":"query","meta":"tokens","type":"login","format":"json"}).json()["query"]["tokens"]["logintoken"]
r = S.post(API, data={"action":"login","lgname":w["bot_username"],"lgpassword":w["bot_password"],"lgtoken":t,"format":"json"}).json()
assert r.get("login",{}).get("result") == "Success", r
tok = S.get(API, params={"action":"query","meta":"tokens","type":"csrf","format":"json"}).json()["query"]["tokens"]["csrftoken"]
def wt(p):
    return S.get(API, params={"action":"parse","page":p,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]
def push(p, txt, summary):
    r = S.post(API, data={"action":"edit","title":p,"text":txt,"summary":summary,"token":tok,"format":"json"}).json()
    assert "edit" in r and r["edit"].get("result")=="Success", json.dumps(r)[:300]
    print(f"  {p} -> rev {r['edit'].get('newrevid')}")

WD = "On the morning of 26 October, the Adonian Community formally requested that Okaiken provide no further vessels to the sealift, asking that Sanese-flagged shipping be withdrawn from the evacuation lanes in an orderly wind-down. The communication stated that the evacuation was a common enterprise conducted under a single chain of command, which a member state whose vessels would not accept that command could not be permitted to carry: \"if it is for the safety of their people, the Community must work in collaboration, not disunity.\" Replacement capacity — vessels volunteered by other member states, [[Balisca]] the largest contributor, together with requisitioned ships — would be phased in as the Sanese hulls stood down. The communication concluded that \"for the safety of all involved in this mission, it is best for Okaiken to wind down operations.\"\r\n\r\nThe government accepted the request the same morning. The Ministry of Foreign Affairs announced that Sanese-flagged vessels would be withdrawn from the lift in an orderly wind-down, and that the [[Escort Flotilla]]'s tasking would end with the departure of the last Sanese hull. The announcement did not concede the command question: Okaiken had withdrawn its vessels rather than their command, and remained, in the ministry's phrasing, \"bound by the treaties it has signed, and by nothing else.\""

# --- 1. Sanese involvement ---
p = "Sanese involvement in the Wolffrean War"
c = wt(p)
print(p)
lead_end = c.find("\r\n\r\n")
print("LEAD:", c[:lead_end][:400])
c = c[:lead_end] + " On 26 October 2026, the government accepted a Community request that Okaiken provide no further vessels to the lift, and began an orderly wind-down of Sanese participation." + c[lead_end:]
i = c.find("== Reception ==")
assert i > 0
c = c[:i] + "== Wind-down of Sanese participation ==\r\n\r\n" + WD + "\r\n\r\n" + c[i:]
push(p, c, "Wind-down of Sanese vessel participation (26 October Community request, accepted)")

# --- 2. 4942D ---
p = "Adonian Community Resolution 4942D"
c = wt(p); print(p)
i = c.find("Should the draft be confirmed for floor debate")
assert i > 0
c = c[:i] + "On the morning of 26 October, the Adonian Community requested that Okaiken provide no further vessels to the evacuation lift, stating that the mission required a single chain of command; replacement capacity — vessels volunteered by other member states and requisitioned ships — would be phased in as Sanese hulls stood down. The government accepted the same morning and announced an orderly wind-down of Sanese-flagged participation. The sponsorship of the draft was unaffected: its subject is the codification of the corridors in Assembly law, not the flag of the ships that serve them.\r\n\r\n" + c[i:]
push(p, c, "26 October Community wind-down request and Okaiken acceptance")

# --- 3. Fortress State ---
p = "Fortress State"
c = wt(p); print(p)
i = c.find("==Reception and criticism==")
assert i > 0
c = c[:i] + "The doctrine's first wartime test concluded within a day of that formulation. On the morning of 26 October the Community requested the wind-down of Sanese vessel participation — judging that ships which would not accept the mission's chain of command could not safely carry its civilians — and the government accepted. Editorialists observed that the outcome was the doctrine rendered literally: offered the choice between subordinating its ships' command and surrendering the mission, the fortress declined the sortie.\r\n\r\n" + c[i:]
a = "recalling the flotilla entirely rather than defending it."
assert c.count(a) == 1
c = c.replace(a, a + " The Community's 26 October request, and the government's acceptance of it, drew from commentators the observation that the doctrine had converged under pressure with the OIP's position — an analogy ministers rejected, on the ground that Okaiken had withdrawn its vessels rather than their command.")
push(p, c, "Doctrine's first wartime test: 26 October wind-down")

# --- 4. Okaiken-Wolffrea relations ---
p = "Okaiken-Wolffrea relations"
c = wt(p); print(p)
i = c.find("==Diplomatic representation==")
assert i > 0
c = c[:i] + "On the morning of 26 October, the Adonian Community requested that Okaiken provide no further vessels to the sealift, citing the government's refusal to accept the mission's chain of command; replacement capacity would be volunteered by other member states and requisitioned into service. The government accepted the same morning, announcing an orderly wind-down of Sanese-flagged participation and the end of the escort flotilla's tasking.\r\n\r\n" + c[i:]
push(p, c, "26 October: Community wind-down request accepted")

# --- 5. 4942E ---
p = "Adonian Community Resolution 4942E"
c = wt(p); print(p)
i = c.find("== See also ==")
assert i > 0
c = c[:i] + "On 26 October, the Community requested that Okaiken wind down its vessel participation in the sealift, and the government accepted the same morning — withdrawing the vessels whose conduct the draft had proposed to sanction.\r\n\r\n" + c[i:]
push(p, c, "26 October wind-down overtakes the draft's premise")

# --- 6. Emergency resolution + Diet debate (generic aftermath append) ---
for p in ["October 2026 Diet emergency resolution on the Wolffrean War", "October 2026 Diet debate on the Wolffrean War"]:
    c = wt(p); print(p)
    m = re.search(r"==+ *Aftermath *==+", c)
    if not m:
        print("  no Aftermath header; headers:", [x.group(0) for x in re.finditer(r"^==+.*?==+", c, re.M)][:8]); continue
    i = m.end()
    j = re.search(r"\r\n==+[^=]", c[i:])
    j = i + j.start() if j else len(c)
    add = "\r\n\r\nOn the morning of 26 October, the Adonian Community requested that Okaiken wind down its vessel participation in the sealift; the government accepted, and the escort flotilla's tasking ended with the departure of the last Sanese-flagged hull."
    c = c[:j] + add + c[j:]
    push(p, c, "26 October wind-down of Sanese vessel participation")
print("ALL DONE")
