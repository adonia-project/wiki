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

# A. Fix the now-wrong "no standing armed forces command" sentence (AC Navy canon: Secretariat directs AC Navy fleets)
old = "it noted also that the Adonian Community possesses no standing armed forces command, and that the amendment would in effect create one."
new = "it noted also that the Secretariat already exercised direction over the AC Navy, and had itself directed an additional fleet to the evacuation mission, so that the amendment would extend an existing command arrangement rather than create a new one."
assert wt.count(old) == 1, wt.count(old)
wt = wt.replace(old, new, 1)

# B. Insert the Zong ambassador subsection after the Jarin subsection, before the "With nine sponsors" status paragraph
content = (
"=== Objection of the Zong ambassador ===" + nl + nl +
"The problem was raised independently on the same evening by the Zong ambassador to Okami, in a d\u00e9marche delivered to the Ministry of Foreign Affairs. The ambassador's argument went to the character of the forces rather than their number: Okaiken, the d\u00e9marche held, cannot act on its own in regard to AC missions that are already being managed by the AC. \"The violation of international law is not the adding of additional forces,\" the d\u00e9marche stated. \"It is in calling the forces self-directed \u2014 and the Secretariat themselves have already directed an additional fleet of the AC Navy forces.\" Diplomatic reporting in Okami read the d\u00e9marche as a second expression, within a single evening, of the same demand made by Jarin: that the escort group be brought under the direction of the command the AC already exercises over its own naval forces." + nl + nl
)
anchor = "With nine sponsors, the draft remained eleven short"
assert wt.count(anchor) == 1, wt.count(anchor)
wt = wt.replace(anchor, content + anchor, 1)

edit(D, wt, "add Zong ambassador demarche (self-directed forces = the violation); correct AC Navy canon (user directive)")
print("DONE")
