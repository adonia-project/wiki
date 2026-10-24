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

# 1. Fix the false parenthetical: the sealift is AC-managed (AC-flagged vessels), not an example of unmanaged national volunteering
old_bullet = "Gives warships already assigned to escort the AC refugee sealift (such as Okaiken's escort group in Alwana) clear permission to defend their convoys"
new_bullet = "Gives warships already assigned to the AC-managed refugee sealift clear permission to defend their convoys"
assert wt.count(old_bullet) == 1, wt.count(old_bullet)
wt = wt.replace(old_bullet, new_bullet, 1)

# 2. Insert the Jarin amendment subsection before the "With nine sponsors" status paragraph
content = (
"=== Proposed amendment by Jarin ===" + nl + nl +
"On the evening of 24 October, the delegation of [[Jarin]] formally requested that Okaiken, as the draft's sponsoring state, amend the text to require that the defense of the proposed deconfliction zones be orchestrated by the [[Adonian Community]] itself rather than provided by volunteering member states, in order to streamline coordination of the protection zone. The proposed provision would require vessels engaged in the zone defense to remain AC-flagged and to be volunteered for command under the armed forces command of the Adonian Community. The Jarin delegation's statement to the sponsoring state was direct: \"Okaiken must follow international cooperation treaties if all nations are expected to follow the same; they must volunteer their vessels for command under the AC armed forces command.\"" + nl + nl +
"The request placed the Sanese delegation in a delicate position. The draft as written already places the refugee sealift under the humanitarian authority of the AC Secretariat \u2014 the ferries of the lift are AC-flagged, and the escort group at Alwana operates within the AC-managed evacuation operation \u2014 but it preserves national command of the escorting warships, in accordance with the defensive provisions of the Ninth Amendment and the separation-of-command provisions of the Emergency Maritime Civilian Protection Act. Diplomatic reporting noted that Jarin's request paralleled the unresolved Burawan objection to the flotilla's sovereign national command, though routed through AC authority rather than the JWG-PNK coalition command; it noted also that the Adonian Community possesses no standing armed forces command, and that the amendment would in effect create one. The request remained under consideration at the close of the day." + nl + nl
)
anchor = "With nine sponsors, the draft remained eleven short"
assert wt.count(anchor) == 1, wt.count(anchor)
wt = wt.replace(anchor, content + anchor, 1)

edit(D, wt, "fix false parenthetical (sealift is AC-managed); add Jarin amendment request (user directive)")
print("DONE")
