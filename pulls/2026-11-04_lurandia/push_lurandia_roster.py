# -*- coding: utf-8 -*-
"""Push Lurandia roster swap: stubs, table, navbox, country data, Talk:Balboa."""
import json
import os
import requests

API = "https://talod.miraheze.org/w/api.php"
HERE = os.path.dirname(os.path.abspath(__file__))
ART = r"B:\02_GIT CONNECTED\wiki\articles\Countries"

cfg = json.load(open(r"B:\02_GIT CONNECTED\wiki\sync_config.json", encoding="utf-8"))
s = requests.Session()
s.headers.update({"User-Agent": "Takeru-Sync/1.0"})

# ---- login (HARD ABORT on failure - never edit anonymously) ----
t = s.get(API, params={"action": "query", "meta": "tokens", "type": "login", "format": "json"}).json()
lg = s.post(API, data={
    "action": "login", "lgname": cfg["wiki"]["bot_username"], "lgpassword": cfg["wiki"]["bot_password"],
    "lgtoken": t["query"]["tokens"]["logintoken"], "format": "json",
}).json()
assert lg.get("login", {}).get("result") == "Success", f"LOGIN FAILED: {lg}"
print("login OK:", cfg["wiki"]["bot_username"])
csrf = s.get(API, params={"action": "query", "meta": "tokens", "format": "json"}).json()["query"]["tokens"]["csrftoken"]

def edit(title, text, summary, createonly=False):
    data = {"action": "edit", "title": title, "text": text, "summary": summary,
            "token": csrf, "bot": 1, "format": "json"}
    if createonly:
        data["createonly"] = 1
    r = s.post(API, data=data).json()
    if "error" in r:
        print(f"  ERROR {title}: {r['error']['code']} {r['error'].get('info','')}")
    else:
        print(f"  {title}: {r['edit'].get('result')} (new revid {r['edit'].get('newrevid','?')})")
    return r

# ---- 1. country data templates (Tabanan pattern, no flag alias) ----
for n in ("Amiera", "Etawa", "Winnipi"):
    tpl = ("{{ {{{1<noinclude>|country showdata</noinclude>}}}\n"
           f"| alias = {n}\n"
           "| size = {{{size|}}}\n| name = {{{name|}}}\n"
           "| altlink = {{{altlink|}}}\n| altvar = {{{altvar|}}}\n"
           "| variant = {{{variant|}}}\n}}")
    edit(f"Template:Country data {n}", tpl, "Country data template for new Lurandian country", createonly=True)

# ---- 2. stub articles ----
for n in ("Amiera", "Etawa", "Winnipi"):
    text = open(os.path.join(ART, n, f"{n}.mediawiki"), encoding="utf-8").read()
    edit(n, text, "New country stub (Lurandia roster update)")

um = open(os.path.join(ART, "United Midlands", "United Midlands.mediawiki"), encoding="utf-8").read()
edit("United Midlands", um, "Rewrite as stub for relocated United Midlands (new territory, 2,348,969 kmÂ²; prior demographic data retained)")

sc = open(os.path.join(ART, "Sinchew", "Sinchew.mediawiki"), encoding="utf-8").read()
edit("Sinchew", sc, "Add area (2,017,722 kmÂ²) per updated GIS")

# ---- 3. Lurandia continent article ----
state = json.load(open(os.path.join(HERE, "lurandia_state.json"), encoding="utf-8"))
L = state["Lurandia"]

tecala_row = "|-\n| {{flag|Tecala}} || [[File:Coats of arms of None.svg|20px]] || [[Tecala]] || 3,399,111.20 || TBD || TBD || TBD || TBD\n"
assert tecala_row in L
L = L.replace(tecala_row, "")

um_row_old = "| {{flag|United Midlands}} || [[File:United Midlands Emblem.png|20px]] || [[United Midlands]] || 7,431,417.78 || 185,950,995 || 25.0 || 24.6 || United Midlands"
assert um_row_old in L
um_row_new = "| {{flag|United Midlands}} || [[File:United Midlands Emblem.png|20px]] || [[United Midlands]] || 2,348,969.00 || 185,950,995 || 79.2 || TBD || United Midlands"
L = L.replace(um_row_old, um_row_new)

assert "|| [[Sinchew]] || 1,649,672.29 ||" in L
L = L.replace("|| [[Sinchew]] || 1,649,672.29 ||", "|| [[Sinchew]] || 2,017,722.00 ||")

amiera_row = "|-\n| {{flag|Amiera}} || [[File:Coats of arms of None.svg|20px]] || [[Amiera]] || 101,662.00 || TBD || TBD || TBD || TBD\n"
etawa_row = "|-\n| {{flag|Etawa}} || [[File:Coats of arms of None.svg|20px]] || [[Etawa]] || 588,942.00 || TBD || TBD || TBD || TBD\n"
winnipi_row = "|-\n| {{flag|Winnipi}} || [[File:Coats of arms of None.svg|20px]] || [[Winnipi]] || 7,431,406.00 || TBD || TBD || TBD || TBD\n"

balboa_row = "|-\n| {{flag|Balboa}} ||"
assert balboa_row in L
L = L.replace(balboa_row, amiera_row + balboa_row, 1)  # Amiera before Balboa

kalanua_row = "|-\n| {{flag|Kalanua}} ||"
assert kalanua_row in L
L = L.replace(kalanua_row, etawa_row + kalanua_row, 1)  # Etawa after Balboa, before Kalanua

um_row_marker = "|-\n" + um_row_new
assert um_row_marker in L
L = L.replace(um_row_marker, um_row_marker + "\n" + winnipi_row.rstrip("\n"), 1)  # Winnipi after UM

L = L.replace("| countries      = 15", "| countries      = 17")
L = L.replace("It comprises fifteen sovereign states", "It comprises seventeen sovereign states")
assert "seventeen sovereign states" in L and "Tecala" not in L
edit("Lurandia", L, "Roster swap: add Amiera, Etawa, Winnipi; remove Tecala; update United Midlands + Sinchew areas (15 â†’ 17 countries)")

# ---- 4. navbox ----
nav = state["Template:Countries in Lurandia"]
old_list = nav[nav.index("* [[Balboa]]"):nav.index("* [[United Midlands]]") + len("* [[United Midlands]]")]
new_list = ("* [[Amiera]]\n* [[Balboa]]\n* [[Etawa]]\n* [[Kalanua]]\n* [[Kaneda]]\n* [[Kavik]]\n"
            "* [[Kawalidipa]]\n* [[Louyang]]\n* [[Markland]]\n* [[Mishko]]\n* [[Nawat]]\n"
            "* [[Neakyrena]]\n* [[Nuuchi]]\n* [[Sinchew]]\n* [[Tuvayo]]\n* [[United Midlands]]\n* [[Winnipi]]")
nav = nav.replace(old_list, new_list)
assert "Tecala" not in nav and "Winnipi" in nav
edit("Template:Countries in Lurandia", nav, "Roster swap: add Amiera, Etawa, Winnipi; remove Tecala (17 countries)")

# ---- 5. Talk:Balboa message to Shub ----
talk = (
 "== GIS area update (November 2026) ==\n"
 "Shub â€” the updated Lurandia GIS package (merged 4 November) now draws Balboa at '''296,063 kmÂ²''' across 15 features "
 "(including islands), versus the article's current canon of '''39,240.84 kmÂ²''', population 35,234,000, and density 897.9/kmÂ². "
 "Carl has confirmed the redraw is intentional. Before the article numbers are updated, could you confirm: "
 "(1) whether the population/density figures should be rescaled for the larger territory, and (2) whether the new islands are named? "
 "The continent table row is being held at the old figure until this is settled. â€” ~~~~\n"
)
r = s.get(API, params={"action": "query", "titles": "Talk:Balboa", "prop": "revisions",
                       "rvprop": "content", "rvslots": "main", "format": "json"}).json()
pg = list(r["query"]["pages"].values())[0]
if "missing" in pg:
    edit("Talk:Balboa", talk, "Query to Shub: Balboa area change 39,241 â†’ 296,063 kmÂ² (GIS redraw)", createonly=True)
else:
    old = pg["revisions"][0]["slots"]["main"]["*"]
    edit("Talk:Balboa", old.rstrip() + "\n\n" + talk, "Query to Shub: Balboa area change 39,241 â†’ 296,063 kmÂ² (GIS redraw)")

print("\nALL DONE")
