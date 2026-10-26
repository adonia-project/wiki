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
def push(p, txt, summary, create=False):
    data = {"action":"edit","title":p,"text":txt,"summary":summary,"token":tok,"format":"json"}
    if create: data["createonly"] = "1"
    r = S.post(API, data=data).json()
    assert "edit" in r and r["edit"].get("result")=="Success", json.dumps(r)[:300]
    print(f"  {p} -> rev {r['edit'].get('newrevid')}")

d = wt("Adonian Community Resolution 4942D")
cats = re.findall(r"\[\[Category:.*?\]\]", d)
print("4942D categories:", cats)

ART = """{{Short description|Draft Adonian Assembly resolution separating the refugee sealift from coalition command}}
'''Adonian Community Resolution 4942F''' is a draft resolution of the [[Adonian Assembly]] submitted by [[Okaiken]] on 26 October 2026. It is the fourth provision of draft [[Adonian Community Resolution 4942D|Resolution 4942D]] — the ban on ground troops and the separation of the refugee sealift from coalition command — resubmitted as a standalone text after the delegation of [[Louyan]] proposed that the provision be split from the parent draft for its own discussion. The resubmission was made on the morning of 26 October, hours after the government of Okaiken accepted the Community's request that it provide no further vessels to the sealift.

The draft proposes to place all naval escorts and chartered or volunteered ferries assigned to the refugee sealift strictly under the humanitarian authority of the [[Adonian Secretariat]], separate from the [[JWG-PNK]] war command at [[Joint Base Ajowa]]; to forbid the requisitioning of evacuation ferries or escorts to carry troops or support amphibious landings; and to reaffirm that [[Adonian Community Resolution 4940|Resolution 4940]] does not authorize the deployment of ground forces into [[Wolffrea]] or [[Bonande]].

== Background ==
{{Main|Adonian Community Resolution 4942D|Sanese involvement in the Wolffrean War}}

The provision originates in the command dispute of October 2026. Demands that the Sanese escort flotilla be brought under Community or coalition command were pressed from three directions — the [[Burawa]]n objection through the JWG-PNK, the proposed [[Jarin]] amendment, and the [[Zong]] demarche — and were refused in the government's formal response of 25 October, which held that "coordination is not command, and participation is not subordination". On the morning of 26 October the Community requested that Okaiken provide no further vessels to the sealift, judging that ships which would not accept the mission's chain of command could not safely carry its civilians; the government accepted, and the Sanese-flagged hulls began an orderly wind-down.

The immediate procedural occasion was different. On 25 October the delegation of Louyan gave notice of a motion to dismiss draft 4942D, to be moved when the [[Committee on Resolutions]] convened on the text on 26 October, and proposed in the alternative that the draft's fourth provision — the ground-troop ban and the separation from coalition command — be split from the text for its own discussion. Rather than contest the point, the delegation of Okaiken split the provision itself: the rider was withdrawn from 4942D, leaving the parent draft a corridors-codification measure, and resubmitted under a new designation.

== Proposed provisions ==
The draft resolution sets out three measures:

* '''Separation from coalition command:''' Keeps all naval escorts and chartered, volunteered or requisitioned ferries assigned to the refugee sealift strictly under the humanitarian authority of the Adonian Secretariat, separate from the JWG-PNK war command at [[Joint Base Ajowa]].
* '''Ban on requisition:''' Forbids requisitioning evacuation ferries or escorts to carry troops or support amphibious landings.
* '''Reaffirmation of the ground-troop prohibition:''' Reaffirms that Resolution 4940 does not authorize sending ground forces into [[Wolffrea]] or [[Bonande]].

== Submission and proceedings ==
{{main|Adonian Community legislative procedure}}

Okaiken submitted the draft to the Assembly on the morning of 26 October 2026. Under the numbering procedure of the Assembly, the draft received the designation '''4942F''', following the Sindewand draft [[Adonian Community Resolution 4942E|4942E]] of 24 October. As with the parent draft, Okaiken is not a sitting member of the Committee on Resolutions for the stint beginning in October 2026, and the text was referred to the committee for review while the delegation circulated it to the co-sponsors of 4942D.

The split removes the target of Louyan's noticed motion while conceding its procedural premise: the corridors codification continues under the 4942D designation, and the provision Louyan proposed to divide for its own discussion now stands for that discussion on its own text.

== Significance ==
With the Sanese hulls in wind-down, the provision applies chiefly to the replacement capacity — vessels volunteered by other member states, [[Balisca]] the largest contributor, together with requisitioned ships. For contributing states, the draft offers a statutory guarantee that volunteered ferries cannot be diverted to military uses. Commentators noted the apparent paradox that the state whose vessels were withdrawn for refusing the coalition's chain of command was now asking the Assembly to write the humanitarian chain of command into law — a paradox the government rejects, on the ground it has drawn since 25 October: the sealift's command belongs to the Secretariat, and it has never been the coalition's to refuse.

== See also ==
* [[Adonian Community Resolution 4942D]]
* [[Adonian Community Resolution 4942E]]
* [[Adonian Community Resolution 4940]]
* [[Sanese involvement in the Wolffrean War]]
* [[Wolffrean War]]
* [[Wolffrean refugee crisis]]

[[Category:Wolffrean War]]
[[Category:Adonian Community]]
[[Category:2026 in Okaiken]]
"""
push("Adonian Community Resolution 4942F", ART, "Create: split of 4942D fourth provision (ground-troop ban, separation from coalition command)", create=True)

# --- patch 4942D: split subsection ---
i = d.find("=== Reservation of Ayorin ===")
assert i > 0
d = d[:i] + "=== Split of the fourth provision (26 October) ===\r\n\r\nOn the morning of 26 October, before the Committee convened on the text, the delegation of Okaiken withdrew the draft's fourth provision — the ban on ground troops and the separation from coalition command — and resubmitted it as a standalone text, [[Adonian Community Resolution 4942F|Resolution 4942F]]. The split conceded the procedural premise of Louyan's noticed motion while leaving the corridors codification intact; the remaining provisions — the ''Aozora Maru'' investigation, the deconfliction system, and the escort self-defence rules — continue under the 4942D designation.\r\n\r\n" + d[i:]
push("Adonian Community Resolution 4942D", d, "Split of fourth provision; resubmitted as 4942F")

# --- patch involvement ---
c = wt("Sanese involvement in the Wolffrean War")
i = c.find("== Reception ==")
assert i > 0
c = c[:i] + "The same morning, the delegation resubmitted the ground-troop ban and the separation of the sealift from coalition command — split from draft 4942D at the suggestion of the Louyan motion — as a standalone text, [[Adonian Community Resolution 4942F|draft Resolution 4942F]].\r\n\r\n" + c[i:]
push("Sanese involvement in the Wolffrean War", c, "Resubmission of split provisions as 4942F")

# --- patch Fortress State ---
f = wt("Fortress State")
a = "the fortress declined the sortie."
assert f.count(a) == 1
f = f.replace(a, a + " The government's answer to the withdrawal was legislative rather than naval: the same morning it split the ground-troop ban and the separation of humanitarian operations from coalition command out of draft 4942D and resubmitted them as [[Adonian Community Resolution 4942F|draft Resolution 4942F]] — asking the Assembly to make the separation a rule rather than an exception.")
push("Fortress State", f, "4942F: the separation made a rule rather than an exception")
print("ALL DONE")
