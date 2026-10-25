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

# ============ 1. Okaiken-Zong relations: new section ============
R = "Okaiken-Zong relations"
wt = wikitext(R)
nl = "\r\n" if "\r\n" in wt else "\n"
sec = (
"===October 2026: The rice-for-protection offer===" + nl + nl +
"On the evening of 24 October 2026, hours after the Zong ambassador to Okami delivered his government's d\u00e9marche on the command of the escort flotilla in Alwana, a second Zong initiative reached Okami through different channels: the Government of [[Yanbaru]] conveyed an offer from Huwei under which the Zong navy would extend protection to Sanese-flagged merchant shipping in the Shendan approaches and the sealift lanes, with Zong rice supplied at concessionary terms, in exchange for the loosening of Okaiken's long-standing restrictions on imported rice. The offer revived, in formal dress, the intermediary role Yanbaru had played between the two states since the [[Maritime Accords of Okami]], and was associated in diplomatic reporting with [[Jang Di|Prime Minister Jang Di]], whose government had cultivated a reputation as a peacemaker in the region." + nl + nl +
"The rice restrictions are among the oldest complaints in the bilateral trade relationship. Okaiken shelters its domestic crop behind steep import quotas and tariffs, a regime tightened further during the Omaika\u2013Zong data dispute, while Zong is one of Adonia's largest rice exporters, and successive Zong governments have pressed for access to the Sanese market without success. The October offer was the first to link the question to security." + nl + nl +
"The offer's purposes were read in opposite ways in Okami. One reading, resting on the Jang Di government's peacemaker reputation, held that the prime minister was insuring the sealift against a breakdown of the AC command arrangements: whatever the chain-of-command dispute produced, Sanese shipping would remain under protection. The other noted that the offer had arrived on the same evening as the ambassador's hardline d\u00e9marche, and that an arrangement of this kind would make Sanese shipping dependent on the Zong navy at a moment when the AC's own security guarantees had been drawn into the command dispute. Commentators observed that the two readings were not mutually exclusive. The government entered no formal reply by the close of the day." + nl + nl +
"Yanbaru's willingness to carry the offer was itself read as significant. A co-sponsor of [[Adonian Community Resolution 4942D|Resolution 4942D]] and a fellow member of the [[East Fosian Sphere]], Yanbaru has a direct interest in the sealift lanes that pass near its own waters, and its mediation spared both governments the appearance of negotiating the arrangement directly \u2014 sparing Okami, in particular, the optics of accepting protection from the old rival. No date had been set for a response by the close of 24 October." + nl + nl
)
anchor = "==See also=="
assert wt.count(anchor) == 1, wt.count(anchor)
wt = wt.replace(anchor, sec + anchor, 1)
edit(R, wt, "add October 2026 rice-for-protection offer section (Yanbaru intermediary; Zong intentions left ambiguous)")

# ============ 2. 4942D: short paragraph after Zong ambassador subsection ============
D = "Adonian Community Resolution 4942D"
wt = wikitext(D)
nl = "\r\n" if "\r\n" in wt else "\n"
tail = "that the escort group be brought under the direction of the command the AC already exercises over its own naval forces."
assert wt.count(tail) == 1, wt.count(tail)
para = (
nl + nl +
"Hours after the d\u00e9marche, a second Zong initiative arrived through other channels: the Government of Yanbaru conveyed an offer under which the Zong navy would protect Sanese-flagged merchant shipping in the sealift lanes, with Zong rice supplied at concessionary terms, in exchange for the loosening of Okaiken's long-standing restrictions on imported rice. The offer was read in Okami either as insurance for the sealift against a breakdown of the command arrangements, or as an attempt to make Sanese shipping dependent on the Zong navy at a moment when the AC's own security guarantees had been drawn into the dispute; the government entered no formal reply by the close of the day. The offer is described in [[Okaiken-Zong relations]]."
)
wt = wt.replace(tail, tail + para, 1)
edit(D, wt, "note Zong rice-for-protection offer conveyed via Yanbaru (cross-ref Okaiken-Zong relations)")
print("DONE")
