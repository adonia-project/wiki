"""Minimal TALOD wiki push script — pushes a single article with safety guards."""
import sys, json, hashlib, requests
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = r"B:\02_GIT CONNECTED\wiki\sync_config.json"
STATE_PATH = r"B:\02_GIT CONNECTED\wiki\sync_state.json"
MAX_EDITS = 2  # Safety: max pages per run

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_login_token(session, api_url):
    r = session.get(api_url, params={"action": "query", "meta": "tokens", "type": "login", "format": "json"})
    return r.json()["query"]["tokens"]["logintoken"]

def login(session, api_url, username, password):
    token = get_login_token(session, api_url)
    r = session.post(api_url, data={
        "action": "login", "lgname": username, "lgpassword": password, "lgtoken": token, "format": "json"
    })
    result = r.json()
    if result["login"]["result"] != "Success":
        print(f"ERROR: Login failed: {result['login']}")
        sys.exit(1)
    print(f"Logged in as {username}")

def get_csrf_token(session, api_url):
    r = session.get(api_url, params={"action": "query", "meta": "tokens", "format": "json"})
    return r.json()["query"]["tokens"]["csrftoken"]

def file_to_wiki_title(filepath, local_root):
    """Convert local file path to wiki title."""
    import os
    rel = os.path.relpath(filepath, local_root)
    rel = rel.replace("\\", "/")
    # Remove category subfolders and extension
    parts = rel.split("/")
    title = parts[-1].replace(".mediawiki", "")
    return title

def push_file(session, api_url, filepath, config, state, edit_count, allow_new=False):
    """Push a single file to the wiki with safety guards."""
    local_root = config["sync"]["local_root"]
    title = file_to_wiki_title(filepath, local_root)
    
    # Read local file
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    # SAFETY GUARD 0: No new page creation (unless --allow-new flag)
    r = session.get(api_url, params={
        "action": "query", "titles": title, "format": "json"
    })
    pages = r.json()["query"]["pages"]
    page_id = list(pages.keys())[0]
    is_new_page = (page_id == "-1")
    if is_new_page and not allow_new:
        print(f"SKIP: '{title}' does not exist on wiki (use --allow-new to create)")
        return edit_count
    
    # SAFETY GUARD 1: Unchanged file skip
    if title in state.get("page_hashes", {}):
        if state["page_hashes"][title] == content_hash:
            print(f"SKIP: '{title}' unchanged since last sync")
            return edit_count
    
    # SAFETY GUARD 2: Conflict detection
    r = session.get(api_url, params={
        "action": "query", "titles": title, "prop": "revisions", "rvprop": "timestamp|user|size",
        "format": "json"
    })
    pages = r.json()["query"]["pages"]
    page_info = list(pages.values())[0]
    if "revisions" in page_info:
        rev = page_info["revisions"][0]
        wiki_size = rev.get("size", 0)
        local_size = len(content.encode("utf-8"))
        # SAFETY GUARD 3: Data loss prevention (>20% shorter)
        if wiki_size > 0 and local_size < wiki_size * 0.8:
            print(f"BLOCKED: '{title}' local is >20% shorter than wiki ({local_size} vs {wiki_size} bytes)")
            return edit_count
    
    # SAFETY: Max edits check
    if edit_count >= MAX_EDITS:
        print(f"LIMIT: Already pushed {edit_count} pages (max {MAX_EDITS}). Stopping.")
        return edit_count
    
    # Push
    csrf = get_csrf_token(session, api_url)
    summary = config["sync"]["edit_summary_new"] if is_new_page else config["sync"]["edit_summary_push"]
    r = session.post(api_url, data={
        "action": "edit", "title": title, "text": content,
        "summary": summary, "token": csrf, "format": "json",
        "bot": "true"
    })
    result = r.json()
    if "error" in result:
        print(f"ERROR pushing '{title}': {result['error']}")
    else:
        rev_id = result["edit"].get("newrevid", result["edit"].get("oldrevid", "?"))
        print(f"Pushed '{title}' to wiki (rev {rev_id})")
        state["page_hashes"][title] = content_hash
        edit_count += 1
    
    return edit_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python push_article.py [--allow-new] <file.mediawiki> [file2.mediawiki ...]")
        sys.exit(1)
    
    allow_new = "--allow-new" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)
    api_url = config["wiki"]["url"]
    
    session = requests.Session()
    session.headers.update({"User-Agent": "Takeru-Sync/2.0 (Letta Code)"})
    login(session, api_url, config["wiki"]["bot_username"], config["wiki"]["bot_password"])
    
    edit_count = 0
    for filepath in files:
        edit_count = push_file(session, api_url, filepath, config, state, edit_count, allow_new=allow_new)
    
    if edit_count > 0:
        save_json(STATE_PATH, state)
        print(f"State updated. Pushed {edit_count} page(s).")

if __name__ == "__main__":
    main()
