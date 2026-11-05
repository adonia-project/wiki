# -*- coding: utf-8 -*-
"""Pull live wiki state for the Lurandia roster swap."""
import json
import requests

API = "https://talod.miraheze.org/w/api.php"
s = requests.Session()
s.headers.update({"User-Agent": "Takeru-Sync/1.0"})

TITLES = [
    "Lurandia", "Template:Countries in Lurandia", "Sinchew",
    "United Midlands", "Tecala", "Balboa", "Winnipi", "Amiera", "Etawa",
]
r = s.get(API, params={
    "action": "query", "titles": "|".join(TITLES),
    "prop": "revisions|info", "rvprop": "ids|content", "rvslots": "main",
    "format": "json",
})
pages = r.json()["query"]["pages"]
out = {}
for pid, p in pages.items():
    name = p["title"]
    if "missing" in p:
        out[name] = None
        print(f"MISSING: {name}")
    else:
        wt = p["revisions"][0]["slots"]["main"]["*"]
        out[name] = wt
        print(f"{name}: rev {p['revisions'][0]['revid']}, {len(wt)} chars")

with open("lurandia_state.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved lurandia_state.json")
