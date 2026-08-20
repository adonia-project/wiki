#!/usr/bin/env python3
"""
TALOD Wiki Sync Bot — Sarta Article Synchronizer

Two-way sync between local .mediawiki files and the TALOD Miraheze wiki.
Only syncs articles under articles/Countries/Sarta/.

Usage:
    python sync_sarta.py              # Full sync (push + pull)
    python sync_sarta.py --push       # Push local changes to wiki only
    python sync_sarta.py --pull       # Pull wiki changes to local only
    python sync_sarta.py --status     # Show what would change (dry run)
    python sync_sarta.py --list       # List all tracked articles
"""

import argparse
import hashlib
import json
import os
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import mwclient
except ImportError:
    print("Error: mwclient not installed. Run: uv add mwclient")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(path=".env"):
        if not os.path.exists(path):
            return
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())

REPO_ROOT = Path(__file__).parent.resolve()
ENV_PATH = REPO_ROOT / ".env"
SYNC_STATE_FILE = REPO_ROOT / ".talod-sync-state-sarta.json"

load_dotenv(str(ENV_PATH))

WIKI_URL = os.environ.get("WIKI_URL", "talod.miraheze.org")
WIKI_USERNAME = os.environ.get("WIKI_USERNAME", "")
WIKI_PASSWORD = os.environ.get("WIKI_PASSWORD", "")
SARTA_DIR = REPO_ROOT / os.environ.get("SARTA_DIR", "articles/Countries/Sarta")
EDIT_SUMMARY = "Sync from local repository via sync-bot"


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {level}: {msg}")


def content_hash(text):
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).rstrip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def get_local_files():
    files = {}
    if not SARTA_DIR.exists():
        return files
    for path in SARTA_DIR.rglob("*.mediawiki"):
        files[path.stem] = path
    return files


def load_sync_state():
    if SYNC_STATE_FILE.exists():
        with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sync_state(state):
    with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True, ensure_ascii=False)


def get_wiki_connection():
    if not WIKI_USERNAME or not WIKI_PASSWORD:
        log("No credentials found. Copy .env.example to .env and fill in your bot credentials.", "ERROR")
        log(f"  Get bot password at: https://{WIKI_URL}/wiki/Special:BotPasswords", "ERROR")
        sys.exit(1)

    log(f"Connecting to {WIKI_URL}...")
    try:
        site = mwclient.Site(
            WIKI_URL,
            path="/w/",
            custom_headers={
                "User-Agent": "TALOD-Sync-Bot/1.0 (https://talod.miraheze.org/; contact@talod.miraheze.org)"
            },
        )
    except Exception as e:
        log(f"Failed to connect: {e}", "ERROR")
        sys.exit(1)

    try:
        site.login(WIKI_USERNAME, WIKI_PASSWORD)
        log(f"Authenticated as {WIKI_USERNAME}")
    except Exception as e:
        log(f"Authentication failed: {e}", "ERROR")
        sys.exit(1)

    return site


def get_wiki_pages_batch(site, page_names):
    result = {}
    batch_size = 50
    names_list = list(page_names)
    for i in range(0, len(names_list), batch_size):
        batch = names_list[i : i + batch_size]
        try:
            response = site.api(
                "query",
                prop="revisions",
                rvprop="content",
                rvslots="main",
                titles="|".join(batch),
            )
            pages = response.get("query", {}).get("pages", {})
            for _, page_data in pages.items():
                title = page_data.get("title", "")
                if "missing" in page_data:
                    continue
                revisions = page_data.get("revisions", [])
                if revisions:
                    content = revisions[0].get("slots", {}).get("main", {}).get("*", "")
                    if content:
                        result[title] = content
        except Exception as e:
            log(f"  Batch fetch error: {e}", "WARN")
    return result


def read_local_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_local_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def push_to_wiki(site, page_name, content, summary=None):
    if summary is None:
        summary = EDIT_SUMMARY
    try:
        page = site.pages[page_name]
        page.save(content, summary=summary, bot=True)
        return True
    except Exception as e:
        log(f"  Push failed for '{page_name}': {e}", "ERROR")
        return False


def do_status(site, state):
    local_files = get_local_files()
    log(f"Found {len(local_files)} local Sarta articles")

    log("Fetching wiki page contents...")
    wiki_contents = get_wiki_pages_batch(site, local_files.keys())
    log(f"  {len(wiki_contents)} pages exist on wiki, {len(local_files) - len(wiki_contents)} are new")

    to_push = []
    to_pull = []
    conflicts = []
    new_pages = []

    for page_name, local_path in sorted(local_files.items()):
        local_content = read_local_file(local_path)
        local_hash = content_hash(local_content)
        wiki_content = wiki_contents.get(page_name)

        if wiki_content is None:
            new_pages.append(page_name)
            continue

        wiki_hash = content_hash(wiki_content)
        last_sync = state.get(page_name, {})
        last_sync_hash = last_sync.get("hash")

        if local_hash == wiki_hash:
            continue

        local_changed = local_hash != last_sync_hash
        wiki_changed = wiki_hash != last_sync_hash

        if local_changed and not wiki_changed:
            to_push.append(page_name)
        elif wiki_changed and not local_changed:
            to_pull.append(page_name)
        elif local_changed and wiki_changed:
            conflicts.append(page_name)
        else:
            if last_sync_hash is None:
                to_push.append(page_name)
            else:
                conflicts.append(page_name)

    log("\nSync status:")
    log(f"  Up to date:     {len(local_files) - len(to_push) - len(to_pull) - len(conflicts) - len(new_pages)}")
    log(f"  To push:        {len(to_push)}")
    log(f"  To pull:        {len(to_pull)}")
    log(f"  Conflicts:      {len(conflicts)}")
    log(f"  New (push):     {len(new_pages)}")

    if to_push:
        log("\n  Push (local -> wiki):")
        for p in to_push:
            log(f"    {p}")
    if to_pull:
        log("\n  Pull (wiki -> local):")
        for p in to_pull:
            log(f"    {p}")
    if conflicts:
        log("\n  CONFLICTS (both sides changed):")
        for p in conflicts:
            log(f"    {p}", "WARN")
    if new_pages:
        log("\n  New pages (not yet on wiki):")
        for p in new_pages:
            log(f"    {p}")

    return to_push, to_pull, conflicts, new_pages


def do_push(site, state, page_names=None):
    local_files = get_local_files()
    if page_names is None:
        to_push, _, conflicts, new_pages = do_status(site, state)
        to_push = to_push + conflicts + new_pages
    else:
        to_push = page_names

    if not to_push:
        log("Nothing to push.")
        return

    log(f"Pushing {len(to_push)} pages to wiki...")
    pushed = 0
    for page_name in to_push:
        local_path = local_files[page_name]
        content = read_local_file(local_path)
        log(f"  Pushing '{page_name}'...")
        if push_to_wiki(site, page_name, content):
            state[page_name] = {
                "hash": content_hash(content),
                "last_sync": datetime.now(timezone.utc).isoformat(),
                "direction": "push",
            }
            pushed += 1
            log("    OK")
        else:
            log("    FAILED", "ERROR")

    save_sync_state(state)
    log(f"Pushed {pushed}/{len(to_push)} pages.")


def do_pull(site, state, page_names=None):
    local_files = get_local_files()
    if page_names is None:
        _, to_pull, _, _ = do_status(site, state)
    else:
        to_pull = page_names

    if not to_pull:
        log("Nothing to pull.")
        return

    log(f"Pulling {len(to_pull)} pages from wiki...")
    wiki_contents = get_wiki_pages_batch(site, to_pull)
    pulled = 0
    for page_name in to_pull:
        local_path = local_files[page_name]
        wiki_content = wiki_contents.get(page_name)
        if wiki_content is None:
            log(f"  '{page_name}' does not exist on wiki, skipping", "WARN")
            continue
        log(f"  Pulling '{page_name}'...")
        write_local_file(local_path, wiki_content)
        state[page_name] = {
            "hash": content_hash(wiki_content),
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "direction": "pull",
        }
        pulled += 1
        log("    OK")

    save_sync_state(state)
    log(f"Pulled {pulled}/{len(to_pull)} pages.")


def do_sync(site, state):
    to_push, to_pull, conflicts, new_pages = do_status(site, state)

    if conflicts:
        log(f"\n{len(conflicts)} conflict(s) detected. Resolve manually:", "WARN")
        for c in conflicts:
            log(f"  {c}")
        log("\nOptions:")
        log("  --push <page>   Force push local version")
        log("  --pull <page>   Force pull wiki version")
        log("  Resolve on wiki, then re-run sync.")

    if to_pull:
        do_pull(site, state, to_pull)

    all_to_push = to_push + new_pages
    if all_to_push:
        do_push(site, state, all_to_push)

    if not to_pull and not all_to_push and not conflicts:
        log("Everything is in sync.")


def do_list():
    local_files = get_local_files()
    log(f"{len(local_files)} Sarta articles found:")
    for name in sorted(local_files.keys()):
        rel_path = local_files[name].relative_to(REPO_ROOT)
        log(f"  {name:50s}  ({rel_path})")


def main():
    parser = argparse.ArgumentParser(description="TALOD Wiki Sync Bot for Sarta articles")
    parser.add_argument("--push", action="store_true", help="Push local changes to wiki only")
    parser.add_argument("--pull", action="store_true", help="Pull wiki changes to local only")
    parser.add_argument("--status", action="store_true", help="Show sync status (dry run)")
    parser.add_argument("--list", action="store_true", help="List all tracked articles")
    parser.add_argument("--force-push", metavar="PAGE", help="Force push a specific page (resolve conflict)")
    parser.add_argument("--force-pull", metavar="PAGE", help="Force pull a specific page (resolve conflict)")
    args = parser.parse_args()

    if args.list:
        do_list()
        return

    state = load_sync_state()
    site = get_wiki_connection()

    if args.status:
        do_status(site, state)
    elif args.push:
        do_push(site, state)
    elif args.pull:
        do_pull(site, state)
    elif args.force_push:
        local_files = get_local_files()
        if args.force_push in local_files:
            do_push(site, state, [args.force_push])
        else:
            log(f"Page '{args.force_push}' not found locally", "ERROR")
    elif args.force_pull:
        local_files = get_local_files()
        if args.force_pull in local_files:
            do_pull(site, state, [args.force_pull])
        else:
            log(f"Page '{args.force_pull}' not found locally", "ERROR")
    else:
        do_sync(site, state)


if __name__ == "__main__":
    main()
