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
def wt(p): return S.get(API, params={"action":"parse","page":p,"prop":"wikitext","format":"json"}).json()["parse"]["wikitext"]["*"]
def edit(title, text, summary, create=False):
    tok = S.get(API, params={"action":"query","meta":"tokens","type":"csrf","format":"json"}).json()["query"]["tokens"]["csrftoken"]
    data = {"action":"edit","title":title,"text":text,"summary":summary,"token":tok,"format":"json"}
    if create: data["createonly"] = "1"
    r = S.post(API, data=data).json()
    assert "edit" in r and r["edit"].get("result") == "Success", json.dumps(r)[:300]
    print(f"OK {title} -> {r['edit'].get('newrevid')}")

# --- 1. Patch Sanese involvement with constitutional text ---
P = "Sanese involvement in the Wolffrean War"
c = wt(P)
nl = "\r\n" if "\r\n" in c else "\n"

a1 = "The Ninth Amendment, ratified the following year, is the settlement of that account: Sanese forces would defend the archipelago, protect Sanese assets and allies, and fight nothing else."
assert c.count(a1) == 1, ("a1", c.count(a1))
add1 = a1 + nl + nl + "The amendment's original text was blunt about where the lesson had been learned: the Sanese people \"shall not permit the deployment of Sanese military personnel overseas for combat operations, even under Adonian Community authorization\" — the Lacashe account reduced to a single sentence. When the Thirteenth Amendment revised Article 9 in 2014, the clause was replaced by the current text, under which Okaiken's forces are maintained \"to protect Okaiken's most valuable assets\" and the Sanese people \"retain the right to protect their assets and their foreign allies from threats of intimidation and war\". The scepticism outlived the clause that expressed it."
c = c.replace(a1, add1, 1)

a2 = "The Ninth Amendment is the settlement of that account, and the account stays settled."
assert c.count(a2) == 1, ("a2", c.count(a2))
add2 = a2 + nl + nl + "The Constitution is not silent on the question, and the Government will not be either. Article 9, in its original form, forbade the deployment of Sanese forces overseas for combat operations even under Adonian Community authorization; that clause was written by a generation that had just come home from Lacashe. As amended in 2014, the same article provides that Okaiken's forces are maintained to protect its most valuable assets, and that the Sanese people retain the right to protect their assets and their foreign allies from threats of intimidation and war. The Government asks the Community to accept what the Constitution already commands: the protection of Sanese lives is Sanese work, wherever those lives are found."
c = c.replace(a2, add2, 1)
edit(P, c, "Ground the 25 October response and the Lacashe account in the verbatim text of Article 9 (original 1984 clause and 2014 amendment)")

# sync local file
open(r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Sanese involvement in the Wolffrean War.mediawiki","w",encoding="utf-8",newline=nl).write(c)

# --- 2. Create Kenichi Mori ---
T = "Kenichi Mori"
art = open(r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Kenichi Mori.mediawiki", encoding="utf-8-sig").read()
edit(T, art, "Create: Foreign Minister, OSP, architect of the receipt doctrine and the 25 October response", create=True)

# verify
for p in [P, T]:
    v = wt(p)
    print(p, len(v), "ch | Article 9:", v.count("Article 9"), "| Lacashe:", v.count("Lacashe"))
print("DONE")
