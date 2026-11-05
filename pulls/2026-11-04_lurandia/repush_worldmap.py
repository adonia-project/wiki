# -*- coding: utf-8 -*-
"""Re-push Adonia Robinson Map.svg (205+ countries, new Lurandia labels) to TALOD."""
import json
import requests

API = "https://talod.miraheze.org/w/api.php"
PATH = r"C:\Users\Carl\Dropbox\Adonia\Adonia Robinson Map.svg"

cfg = json.load(open(r"B:\02_GIT CONNECTED\wiki\sync_config.json", encoding="utf-8"))
s = requests.Session()
s.headers.update({"User-Agent": "Takeru-Sync/1.0"})

t = s.get(API, params={"action": "query", "meta": "tokens", "type": "login", "format": "json"}).json()
lg = s.post(API, data={"action": "login", "lgname": cfg["wiki"]["bot_username"],
                       "lgpassword": cfg["wiki"]["bot_password"],
                       "lgtoken": t["query"]["tokens"]["logintoken"], "format": "json"}).json()
assert lg.get("login", {}).get("result") == "Success", f"LOGIN FAILED: {lg}"
print("login OK")
csrf = s.get(API, params={"action": "query", "meta": "tokens", "format": "json"}).json()["query"]["tokens"]["csrftoken"]

with open(PATH, "rb") as f:
    r = s.post(API, files={"file": ("Adonia Robinson Map.svg", f, "image/svg+xml")},
               data={"action": "upload", "filename": "Adonia Robinson Map.svg",
                     "comment": "Re-render: Lurandia roster update (Amiera, Etawa, Winnipi added; Tecala removed; United Midlands relocated)",
                     "ignorewarnings": 1, "token": csrf, "format": "json"}).json()
print(r.get("upload", r))
