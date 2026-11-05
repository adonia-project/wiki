# -*- coding: utf-8 -*-
"""Upload Location of {Amiera,Etawa,Winnipi,United Midlands}.svg to TALOD."""
import json
import requests

API = "https://talod.miraheze.org/w/api.php"
BASE = r"B:\02_GIT CONNECTED\map"
NAMES = ["Amiera", "Etawa", "Winnipi", "United Midlands"]

cfg = json.load(open(r"B:\02_GIT CONNECTED\wiki\sync_config.json", encoding="utf-8"))
s = requests.Session()
s.headers.update({"User-Agent": "Takeru-Sync/1.0"})

t = s.get(API, params={"action": "query", "meta": "tokens", "type": "login", "format": "json"}).json()
lg = s.post(API, data={"action": "login", "lgname": cfg["wiki"]["bot_username"], "lgpassword": cfg["wiki"]["bot_password"],
                       "lgtoken": t["query"]["tokens"]["logintoken"], "format": "json"}).json()
assert lg.get("login", {}).get("result") == "Success", f"LOGIN FAILED: {lg}"
print("login OK")
csrf = s.get(API, params={"action": "query", "meta": "tokens", "format": "json"}).json()["query"]["tokens"]["csrftoken"]

for n in NAMES:
    path = BASE + rf"\Location of {n}.svg"
    with open(path, "rb") as f:
        r = s.post(API, files={"file": (f"Location of {n}.svg", f, "image/svg+xml")},
                   data={"action": "upload", "filename": f"Location of {n}.svg",
                         "comment": "Orthographic location globe (EU-globe style)",
                         "ignorewarnings": 1, "token": csrf, "format": "json"}).json()
    if "error" in r:
        print(f"  ERROR {n}: {r['error'].get('info')}")
    else:
        print(f"  Location of {n}.svg: {r['upload'].get('result')}")
print("uploads done")
