"""Push a single page to the TALOD wiki, using the same .env credentials as the
sync scripts. Used for pages outside the paths the sync scripts cover, such as
the Template namespace.

    python push_page.py "Template:Country data Hachinawa" articles/Templates/Template_Country data Hachinawa.mediawiki

DRY RUN unless --go is passed.
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent

# load .env the same way the sync scripts do
env = REPO / ".env"
if env.exists():
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

WIKI_URL = os.environ.get("WIKI_URL", "talod.miraheze.org")
USERNAME = os.environ.get("WIKI_USERNAME", "")
PASSWORD = os.environ.get("WIKI_PASSWORD", "")

import requests


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    page, path = sys.argv[1], Path(sys.argv[2])
    go = "--go" in sys.argv

    if not USERNAME or not PASSWORD:
        print("ERROR: WIKI_USERNAME / WIKI_PASSWORD not set (check .env)")
        return 1
    text = path.read_text(encoding="utf-8")
    print("page:  %s" % page)
    print("file:  %s (%d chars)" % (path, len(text)))
    if not go:
        print("\nDRY RUN - pass --go to actually push")
        return 0

    api = "https://%s/w/api.php" % WIKI_URL
    s = requests.Session()
    s.headers.update({"User-Agent": "talod-sync/1.0"})

    r = s.get(api, params={"action": "query", "meta": "tokens", "type": "login",
                           "format": "json"}, timeout=30)
    token = r.json()["query"]["tokens"]["logintoken"]
    r = s.post(api, data={"action": "login", "lgname": USERNAME, "lgpassword": PASSWORD,
                          "lgtoken": token, "format": "json"}, timeout=30)
    res = r.json().get("login", {})
    print("login: %s" % res.get("result"))
    if res.get("result") != "Success":
        print(res)
        return 1

    r = s.get(api, params={"action": "query", "meta": "tokens", "format": "json"}, timeout=30)
    csrf = r.json()["query"]["tokens"]["csrftoken"]
    r = s.post(api, data={"action": "edit", "title": page, "text": text,
                          "summary": "Template:Country data Hachinawa - flag support",
                          "token": csrf, "bot": 1, "format": "json"}, timeout=30)
    d = r.json().get("edit", {})
    print("edit:  %s" % d.get("result"))
    return 0 if d.get("result") == "Success" else 1


if __name__ == "__main__":
    sys.exit(main())
