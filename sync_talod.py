"""
TALOD Wiki Bidirectional Sync Script
=====================================
Syncs articles between TALOD Miraheze wiki and local filesystem.

Features:
- Pull: Detects wiki changes via RecentChanges API, downloads updated pages
- Push: Watches local .mediawiki files, uploads changes to wiki
- Category-based folder organization
- Conflict detection (local vs wiki both changed)
- 15-minute polling interval (configurable)

Usage:
  python sync_talod.py --full       # Full pull of all content pages
  python sync_talod.py --update     # Incremental pull (only changed pages)
  python sync_talod.py --watch      # Start background sync service (pull + push)
  python sync_talod.py --push FILE  # Push a single file to wiki
  python sync_talod.py --status     # Show sync status
"""

import json
import os
import sys
import time
import re
import hashlib
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Third-party
try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip install requests")
    sys.exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("WARNING: 'watchdog' not installed. File watching disabled.")
    Observer = None

# ─── Configuration ───────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "sync_config.json"
STATE_PATH = SCRIPT_DIR / "sync_state.json"
LOG_PATH = SCRIPT_DIR / "sync.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("sync_talod")


def load_config():
    """Load sync configuration."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state():
    """Load sync state (timestamps, hashes)."""
    if STATE_PATH.exists():
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_pull": None,
        "page_hashes": {},
        "push_queue": [],
        "conflicts": [],
    }


def save_state(state):
    """Save sync state."""
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ─── Wiki API Layer ──────────────────────────────────────────────────────────

class TALODWiki:
    """Direct MediaWiki API client for TALOD."""

    def __init__(self, config):
        self.api_url = config["wiki"]["url"]
        self.script_path = config["wiki"]["script_path"]
        self.bot_username = config["wiki"].get("bot_username", "")
        self.bot_password = config["wiki"].get("bot_password", "")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TALOD-Sync/1.0 (Letta Code)"})
        self.edit_token = None
        self.logged_in = False

    def _api_get(self, params):
        """Make a GET request to the API."""
        params["format"] = "json"
        resp = self.session.get(self.api_url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _api_post(self, params, data=None):
        """Make a POST request to the API."""
        params["format"] = "json"
        resp = self.session.post(self.api_url, params=params, data=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def login(self):
        """Log in using bot credentials (if configured)."""
        if not self.bot_username or not self.bot_password:
            log.info("No bot credentials configured — running in read-only mode")
            return False

        try:
            # Step 1: Get login token
            result = self._api_get({"action": "query", "meta": "tokens", "type": "login"})
            login_token = result["query"]["tokens"]["logintoken"]

            # Step 2: Log in
            result = self._api_post(
                {"action": "login"},
                data={
                    "lgname": self.bot_username,
                    "lgpassword": self.bot_password,
                    "lgtoken": login_token,
                },
            )

            if result["login"]["result"] == "Success":
                self.logged_in = True
                log.info(f"Logged in as {self.bot_username}")
                return True
            else:
                log.warning(f"Login failed: {result['login']['reason']}")
                return False
        except Exception as e:
            log.error(f"Login error: {e}")
            return False

    def get_edit_token(self):
        """Get an edit token (CSRF token) for writing."""
        if not self.logged_in:
            return None
        try:
            result = self._api_get({"action": "query", "meta": "tokens"})
            self.edit_token = result["query"]["tokens"]["csrftoken"]
            return self.edit_token
        except Exception as e:
            log.error(f"Failed to get edit token: {e}")
            return None

    def get_page_content(self, title):
        """Get the raw wikitext of a page."""
        try:
            result = self._api_get({
                "action": "query",
                "titles": title,
                "prop": "revisions",
                "rvprop": "content|timestamp",
                "rvlimit": 1,
            })
            pages = result["query"]["pages"]
            page_id = list(pages.keys())[0]
            if page_id == "-1":
                return None, None  # Page doesn't exist
            page = pages[page_id]
            if "revisions" not in page:
                return None, None
            content = page["revisions"][0]["*"]
            timestamp = page["revisions"][0]["timestamp"]
            return content, timestamp
        except Exception as e:
            log.error(f"Failed to get page '{title}': {e}")
            return None, None

    def get_page_categories(self, title):
        """Get the categories a page belongs to."""
        try:
            result = self._api_get({
                "action": "query",
                "titles": title,
                "prop": "categories",
                "cllimit": 50,
            })
            pages = result["query"]["pages"]
            page_id = list(pages.keys())[0]
            if page_id == "-1" or "categories" not in pages[page_id]:
                return []
            return [cat["title"].replace("Category:", "") for cat in pages[page_id]["categories"]]
        except Exception as e:
            log.error(f"Failed to get categories for '{title}': {e}")
            return []

    def get_all_content_pages(self, namespace=0):
        """Get all content page titles (non-redirects only)."""
        pages = []
        apcontinue = None
        while True:
            params = {
                "action": "query",
                "list": "allpages",
                "aplimit": 500,
                "apfilterredir": "nonredirects",
                "apnamespace": namespace,
            }
            if apcontinue:
                params["apcontinue"] = apcontinue
            result = self._api_get(params)
            pages.extend([p["title"] for p in result["query"]["allpages"]])
            if "continue" in result:
                apcontinue = result["continue"]["apcontinue"]
            else:
                break
            time.sleep(0.5)  # Be polite
        return pages

    def get_recent_changes(self, since_iso):
        """Get pages changed since a given ISO timestamp."""
        changes = []
        rccontinue = None
        while True:
            params = {
                "action": "query",
                "list": "recentchanges",
                "rclimit": 500,
                "rcprop": "title|timestamp|type",
                "rctype": "edit|new",
                "rcnamespace": 0,
                "rcdir": "newer",
                "rcstart": since_iso,
            }
            if rccontinue:
                params["rccontinue"] = rccontinue
            result = self._api_get(params)
            changes.extend(result["query"]["recentchanges"])
            if "continue" in result:
                rccontinue = result["continue"]["rccontinue"]
            else:
                break
            time.sleep(0.5)
        return changes

    def get_category_members(self, category, limit=500):
        """Get all pages in a category."""
        members = []
        cmcontinue = None
        while True:
            params = {
                "action": "query",
                "list": "categorymembers",
                "cmtitle": f"Category:{category}",
                "cmlimit": min(limit, 500),
                "cmtype": "page",
            }
            if cmcontinue:
                params["cmcontinue"] = cmcontinue
            result = self._api_get(params)
            members.extend(result["query"]["categorymembers"])
            if "continue" in result:
                cmcontinue = result["continue"]["cmcontinue"]
            else:
                break
            time.sleep(0.5)
        return [m["title"] for m in members]

    def edit_page(self, title, content, summary="Updated via TALOD sync"):
        """Edit a page on the wiki."""
        if not self.logged_in or not self.edit_token:
            log.error("Cannot edit: not logged in or no edit token")
            return False
        try:
            result = self._api_post(
                {"action": "edit"},
                data={
                    "title": title,
                    "text": content,
                    "summary": summary,
                    "token": self.edit_token,
                    "bot": True,
                },
            )
            if result.get("edit", {}).get("result") == "Success":
                log.info(f"Pushed '{title}' to wiki (rev {result['edit'].get('newrevid', '?')})")
                return True
            else:
                log.error(f"Edit failed for '{title}': {result}")
                return False
        except Exception as e:
            log.error(f"Failed to edit '{title}': {e}")
            return False


# ─── File System Layer ───────────────────────────────────────────────────────

def sanitize_filename(title):
    """Convert a wiki page title to a safe filename."""
    # Replace slashes with underscores (subpages)
    name = title.replace("/", "_")
    # Remove characters invalid in Windows filenames
    name = re.sub(r'[<>:"|?*]', '', name)
    # Collapse multiple spaces/underscores
    name = re.sub(r'[\s_]+', ' ', name).strip()
    return name


# Category priority: higher number = higher priority when multiple categories match
# Specific country categories beat generic regional ones
CATEGORY_PRIORITY = {
    # Sub-categories (highest priority — most specific)
    "Okaiken politicians": 100,
    "Okaiken actors": 100,
    "Okaiken bodybuilders": 100,
    "Okaiken rugby union players": 100,
    "Okaiken international rugby union players": 100,
    "Okaiken Basketball Super League players": 100,
    "Okaiken Democratic Party politicians": 100,
    "Okaiken Socialist Party politicians": 100,
    "Okaiken Railways": 100,
    "Okaiken railways": 100,
    "Okaiken hip hop": 100,
    "Okaiken legislation": 100,
    "Okaiken national football team": 100,
    "Okaiken general election, 2026": 100,
    "Okaiken-related lists": 90,
    "Okaiken history navigational boxes": 80,
    "Okaiken political leader navigational boxes": 80,
    "Okaiken political party colour templates": 80,
    "Okaiken sidebar templates": 80,
    "Okaiken stub templates": 80,
    "Okaiken subdivision templates": 80,
    "Okaiken campaignbox templates": 80,
    "Okaiken topics": 80,
    # Country categories (high priority)
    "Okaiken": 70,
    "Balisca": 70,
    "Burawa": 70,
    "Nakamizu": 70,
    "Dagit": 70,
    "Yanbaru": 70,
    "Fenia": 70,
    "Qym": 70,
    "Geno": 70,
    # Topic categories (medium priority)
    "Languages": 50,
    "Religions": 50,
    "Ethnicities": 50,
    "Events": 50,
    "Former countries": 50,
    # Regional categories (low priority — too generic)
    "Adonia": 10,
    "Fosia": 10,
    "Illypnia": 10,
    "Lurandia": 10,
    "Abyala": 10,
}


def _best_category_path(categories, config):
    """Find the best category→folder mapping using priority, skipping meta categories."""
    local_root = Path(config["sync"]["local_root"])
    ext = config["sync"]["file_extension"]
    skip_cats = set(config.get("skip_categories", []))

    best_cat = None
    best_priority = -1

    for cat in categories:
        # Skip maintenance/meta categories
        if cat in skip_cats:
            continue
        if cat in config["category_mapping"]:
            priority = CATEGORY_PRIORITY.get(cat, 30)  # Default priority for unmapped
            if priority > best_priority:
                best_priority = priority
                best_cat = cat

    return best_cat


def get_local_path(title, config, wiki=None):
    """Determine the local file path for a wiki page based on its categories."""
    local_root = Path(config["sync"]["local_root"])
    ext = config["sync"]["file_extension"]

    if wiki:
        categories = wiki.get_page_categories(title)
        best_cat = _best_category_path(categories, config)
        if best_cat:
            folder = config["category_mapping"][best_cat]
            return local_root / folder / f"{sanitize_filename(title)}{ext}"

    default = config.get("default_category", "Other")
    return local_root / default / f"{sanitize_filename(title)}{ext}"


def get_local_path_from_categories(title, categories, config):
    """Determine local path from pre-fetched categories (avoids extra API call)."""
    local_root = Path(config["sync"]["local_root"])
    ext = config["sync"]["file_extension"]

    best_cat = _best_category_path(categories, config)
    if best_cat:
        folder = config["category_mapping"][best_cat]
        return local_root / folder / f"{sanitize_filename(title)}{ext}"

    default = config.get("default_category", "Other")
    return local_root / default / f"{sanitize_filename(title)}{ext}"


def ensure_dir(filepath):
    """Create directory if it doesn't exist."""
    filepath.parent.mkdir(parents=True, exist_ok=True)


def write_local_file(filepath, content):
    """Write content to a local file."""
    ensure_dir(filepath)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    log.info(f"Saved: {filepath}")


def read_local_file(filepath):
    """Read content from a local file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def file_hash(content):
    """Compute SHA-256 hash of content for change detection."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def should_ignore(title, config):
    """Check if a page should be ignored based on namespace patterns."""
    for pattern in config.get("ignore_patterns", []):
        if re.match(pattern, title):
            return True
    return False


def local_file_to_title(filepath, config):
    """Convert a local file path back to a wiki page title."""
    # Remove extension and directory path
    name = filepath.stem
    # This is a best-effort reverse mapping
    return name


# ─── Pull: Wiki → Local ─────────────────────────────────────────────────────

def full_pull(wiki, config, state):
    """Pull all content pages from the wiki."""
    log.info("=== Starting full pull ===")
    all_pages = wiki.get_all_content_pages()
    log.info(f"Found {len(all_pages)} content pages")

    pulled = 0
    skipped = 0
    errors = 0

    for i, title in enumerate(all_pages, 1):
        if should_ignore(title, config):
            skipped += 1
            continue

        try:
            content, timestamp = wiki.get_page_content(title)
            if content is None:
                skipped += 1
                continue

            # Get categories for folder mapping
            categories = wiki.get_page_categories(title)
            local_path = get_local_path_from_categories(title, categories, config)

            # Check if local file already has this content
            content_hash = file_hash(content)
            existing_hash = state["page_hashes"].get(title)

            if existing_hash == content_hash and local_path.exists():
                skipped += 1
                continue  # No change

            # Write the file
            write_local_file(local_path, content)
            state["page_hashes"][title] = content_hash
            pulled += 1

            if i % 50 == 0:
                log.info(f"Progress: {i}/{len(all_pages)} ({pulled} pulled, {skipped} skipped)")
                save_state(state)

            time.sleep(0.3)  # Rate limiting

        except Exception as e:
            log.error(f"Error pulling '{title}': {e}")
            errors += 1

    state["last_pull"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    log.info(f"=== Full pull complete: {pulled} pulled, {skipped} skipped, {errors} errors ===")


def incremental_pull(wiki, config, state):
    """Pull only pages changed since last sync."""
    since = state.get("last_pull")
    if not since:
        log.info("No last_pull timestamp found — running full pull instead")
        full_pull(wiki, config, state)
        return

    log.info(f"=== Starting incremental pull (since {since}) ===")

    changes = wiki.get_recent_changes(since)
    # Deduplicate by title (keep latest)
    seen = set()
    unique_titles = []
    for change in reversed(changes):
        title = change["title"]
        if title not in seen and not should_ignore(title, config):
            seen.add(title)
            unique_titles.append(title)

    log.info(f"Found {len(unique_titles)} changed pages")

    pulled = 0
    for title in unique_titles:
        try:
            content, timestamp = wiki.get_page_content(title)
            if content is None:
                continue

            categories = wiki.get_page_categories(title)
            local_path = get_local_path_from_categories(title, categories, config)

            content_hash = file_hash(content)
            existing_hash = state["page_hashes"].get(title)

            # Conflict detection: local file changed but wiki also changed
            if local_path.exists() and existing_hash != file_hash(read_local_file(local_path)):
                # Local file was modified independently — CONFLICT
                handle_conflict(title, local_path, content, config, state)
                state["page_hashes"][title] = content_hash
                continue

            if existing_hash == content_hash:
                continue  # No actual change

            write_local_file(local_path, content)
            state["page_hashes"][title] = content_hash
            pulled += 1
            time.sleep(0.3)

        except Exception as e:
            log.error(f"Error pulling '{title}': {e}")

    state["last_pull"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    log.info(f"=== Incremental pull complete: {pulled} updated ===")


def handle_conflict(title, local_path, wiki_content, config, state):
    """Handle an edit conflict by saving both versions."""
    conflict_dir = Path(config["sync"]["conflict_dir"])
    conflict_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = sanitize_filename(title)
    ext = config["sync"]["file_extension"]

    # Save wiki version
    wiki_file = conflict_dir / f"{safe_title}_WIKI_{timestamp}{ext}"
    write_local_file(wiki_file, wiki_content)

    # Copy local version
    local_file = conflict_dir / f"{safe_title}_LOCAL_{timestamp}{ext}"
    import shutil
    shutil.copy2(local_path, local_file)

    log.warning(f"CONFLICT: '{title}' -- both local and wiki changed. Saved both versions to {conflict_dir}")
    state["conflicts"].append({
        "title": title,
        "timestamp": timestamp,
        "local_file": str(local_file),
        "wiki_file": str(wiki_file),
    })


# ─── Push: Local → Wiki ─────────────────────────────────────────────────────

def validate_new_page(title, content):
    """Validate that a new page is safe to create on the wiki.
    
    Returns (is_valid, reason) tuple.
    """
    # ── Minimum content length ──
    if len(content.strip()) < 200:
        return False, f"Content too short ({len(content.strip())} chars, minimum 200)"
    
    # ── Must contain wikitext markers ──
    wikitext_markers = ["{{", "[[", "'''", "==", "|"]
    has_wikitext = any(marker in content for marker in wikitext_markers)
    if not has_wikitext:
        return False, "No wikitext formatting detected (missing {{, [[, =, etc.)"
    
    # ── Must not be a redirect-only page ──
    if content.strip().startswith("#REDIRECT") or content.strip().startswith("#redirect"):
        return False, "Page is a redirect — create manually on the wiki"
    
    # ── Title must be meaningful ──
    if len(title.strip()) < 3:
        return False, "Title too short"
    
    return True, "Valid"


def push_new_file(filepath, wiki, config, state, dry_run=False):
    """Push a new local file to the wiki (creates a new page).
    
    SAFETY GUARDS for new page creation:
    1. Content must be at least 200 characters
    2. Must contain wikitext formatting markers
    3. Must not be a redirect-only page
    4. Title must be meaningful (3+ chars)
    5. Page must not already exist on the wiki
    """
    if not wiki.logged_in:
        log.error("Cannot push new page: not logged in to wiki")
        return False

    title = local_file_to_title(filepath, config)

    # ── NEVER PUSH CHECK ──
    never_push = config.get("never_push", [])
    if title in never_push:
        log.info(f"Skip push '{title}': page is on the never_push list")
        return False

    content = read_local_file(filepath)

    # ── Validate the new page ──
    is_valid, reason = validate_new_page(title, content)
    if not is_valid:
        log.warning(f"BLOCKED NEW PAGE '{title}': {reason}")
        return False

    # ── Check page doesn't already exist ──
    wiki_content, _ = wiki.get_page_content(title)
    if wiki_content:
        log.info(f"Skip new page '{title}': page already exists on wiki — use regular push instead")
        return False

    if dry_run:
        log.info(f"[DRY RUN] Would create new page: '{title}' ({len(content)} chars)")
        return True

    summary = config["sync"].get("edit_summary_new", "Created via Takeru (Letta Code auto-sync)")
    success = wiki.edit_page(title, content, summary)

    if success:
        local_hash = file_hash(content)
        state["page_hashes"][title] = local_hash
        save_state(state)
        log.info(f"Created new page: '{title}'")

    return success


def push_file(filepath, wiki, config, state, allow_new=False):
    """Push a single local file to the wiki.
    
    SAFETY GUARD: Before pushing, this function verifies that:
    1. The local file has actually been modified (its hash differs from what we last pulled/pushed)
    2. The wiki version hasn't been changed by someone else since our last pull
    3. The push would not cause data loss (local content is not significantly shorter than wiki)
    
    If allow_new=True, new pages can be created with validation safeguards.
    """
    if not wiki.logged_in:
        log.error("Cannot push: not logged in to wiki")
        return False

    title = local_file_to_title(filepath, config)

    # ── NEVER PUSH CHECK: Pages explicitly blacklisted ──
    never_push = config.get("never_push", [])
    if title in never_push:
        log.info(f"Skip push '{title}': page is on the never_push list")
        return False

    content = read_local_file(filepath)
    local_hash = file_hash(content)

    # ── SAFETY GUARD 1: Check if local file was actually modified ──
    # If the local hash matches what we have stored, the file hasn't changed
    # since our last pull/push — no need to push.
    stored_hash = state["page_hashes"].get(title)
    if stored_hash and stored_hash == local_hash:
        log.info(f"Skip push '{title}': local file unchanged since last sync")
        return False

    # ── Check if page exists on wiki ──
    wiki_content, _ = wiki.get_page_content(title)
    if not wiki_content:
        if allow_new:
            # Delegate to push_new_file with its own validation
            return push_new_file(filepath, wiki, config, state)
        else:
            log.warning(
                f"BLOCKED PUSH '{title}': page does not exist on wiki. "
                f"Use --push-new to create new pages, or create the page on the wiki first."
            )
            return False

    # ── SAFETY GUARD 2: Check if wiki version has changed since we last pulled ──
    wiki_hash = file_hash(wiki_content)
    
    if stored_hash and stored_hash != wiki_hash:
        # Wiki was edited by someone else since our last pull
        handle_conflict(title, filepath, wiki_content, config, state)
        return False

    # ── SAFETY GUARD 3: Data loss prevention ──
    # If the local content is significantly shorter than the wiki version,
    # it's likely a stale copy that would destroy data. Block the push.
    local_len = len(content)
    wiki_len = len(wiki_content)
    
    # Allow 10% tolerance for minor edits, but block if local is >20% shorter
    if local_len > 0 and wiki_len > 100 and local_len < wiki_len * 0.8:
        log.warning(
            f"BLOCKED PUSH '{title}': local ({local_len} chars) is "
            f"{wiki_len - local_len} chars shorter than wiki ({wiki_len} chars). "
            f"This looks like a stale local copy that would cause data loss. "
            f"Run --update first to pull the latest wiki version."
        )
        return False

    summary = config["sync"].get("edit_summary_push", "Updated via TALOD sync")
    success = wiki.edit_page(title, content, summary)

    if success:
        state["page_hashes"][title] = local_hash
        save_state(state)

    return success


# ─── File Watcher ────────────────────────────────────────────────────────────

class WikiFileSyncHandler(FileSystemEventHandler):
    """Watches for local .mediawiki file changes and pushes to wiki."""

    def __init__(self, wiki, config, state):
        self.wiki = wiki
        self.config = config
        self.state = state
        self.debounce = {}  # Prevent double-pushes
        super().__init__()

    def on_modified(self, event):
        self._handle_change(event.src_path)

    def on_created(self, event):
        self._handle_change(event.src_path)

    def _handle_change(self, path_str):
        path = Path(path_str)
        ext = self.config["sync"]["file_extension"]

        if path.suffix != ext:
            return
        if path.name.startswith("~"):  # Temp files
            return
        if ".letta" in path.parts:  # Letta internal files
            return

        # Debounce: ignore if same file changed within 5 seconds
        now = time.time()
        if path_str in self.debounce and now - self.debounce[path_str] < 5:
            return
        self.debounce[path_str] = now

        if not self.config["sync"].get("push_enabled", True):
            return

        log.info(f"Detected local change: {path}")
        push_file(path, self.wiki, self.config, self.state)


# ─── Watch Mode (Background Service) ────────────────────────────────────────

def watch_mode(wiki, config, state):
    """Run as a background service: pull on interval + push on file change."""
    poll_interval = config["sync"]["poll_interval_seconds"]

    log.info(f"=== Starting watch mode (poll every {poll_interval}s = {poll_interval//60}min) ===")
    log.info(f"Watching: {config['sync']['local_root']}")

    # Set up file watcher
    observer = None
    if Observer and config["sync"].get("push_enabled", True):
        handler = WikiFileSyncHandler(wiki, config, state)
        observer = Observer()
        observer.schedule(handler, config["sync"]["local_root"], recursive=True)
        observer.daemon = True
        observer.start()
        log.info("File watcher started — local edits will be pushed to wiki")
    else:
        log.info("File watcher disabled (watchdog not installed or push disabled)")

    # Main loop: pull on interval
    try:
        while True:
            try:
                if config["sync"].get("pull_enabled", True):
                    incremental_pull(wiki, config, state)
            except Exception as e:
                log.error(f"Pull error: {e}")

            log.info(f"Next pull in {poll_interval // 60} minutes...")
            time.sleep(poll_interval)

    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        if observer:
            observer.stop()
            observer.join()


# ─── Bulk Rename (Safe) ─────────────────────────────────────────────────────

def bulk_rename(wiki, config, state, replacements, dry_run=False):
    """Safely rename terms across all wiki articles.
    
    This function:
    1. Uses the wiki search API to find articles containing the old terms
    2. Pulls the LATEST version of each matching article from the wiki
    3. Applies the replacements to the fresh content
    4. Pushes the renamed content back
    5. Updates local copies and state hashes
    
    This avoids the data-loss risk of pushing stale local copies.
    
    Args:
        wiki: TALODWiki instance (must be logged in)
        config: Sync configuration
        state: Sync state
        replacements: List of (old, new) string tuples
        dry_run: If True, show what would change without pushing
    """
    if not wiki.logged_in:
        log.error("Cannot bulk rename: not logged in to wiki")
        return
    
    # Use search API to find articles containing old terms (much faster than scanning all pages)
    titles_to_rename = set()
    for old, new in replacements:
        if old[0].isupper() and len(old) > 2:  # Only search for primary terms, not case variants
            result = wiki._api_get({
                'action': 'query',
                'list': 'search',
                'srsearch': old,
                'srlimit': 500,
                'srnamespace': 0,
            })
            for hit in result['query']['search']:
                titles_to_rename.add(hit['title'])
            time.sleep(0.5)
    
    log.info(f"Found {len(titles_to_rename)} pages containing rename targets")
    
    changed = 0
    skipped = 0
    errors = 0
    
    for title in sorted(titles_to_rename):
        # Get the LATEST content from the wiki
        content, timestamp = wiki.get_page_content(title)
        if not content:
            continue
        
        # Check if any old terms exist in this article
        has_old = any(old in content for old, new in replacements)
        if not has_old:
            skipped += 1
            continue
        
        # Apply replacements
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
        
        if new_content == content:
            skipped += 1
            continue
        
        # Count changes
        change_count = sum(content.count(old) for old, new in replacements if old in content)
        log.info(f"  {title}: {change_count} replacement(s)")
        
        if dry_run:
            log.info(f"  [DRY RUN] Would update: {title}")
            changed += 1
            continue
        
        # Push the renamed content
        summary = "Bulk rename: " + ", ".join(f"{old}->{new}" for old, new in replacements if old[0].isupper()) + " (Takeru auto-sync)"
        success = wiki.edit_page(title, new_content, summary)
        
        if success:
            # Update state hash
            state["page_hashes"][title] = file_hash(new_content)
            
            # Update local file
            local_root = Path(config["sync"]["local_root"])
            matches = list(local_root.rglob(title + ".mediawiki"))
            if matches:
                matches[0].write_text(new_content, encoding="utf-8")
            
            changed += 1
        else:
            errors += 1
            log.error(f"  Failed to push: {title}")
        
        time.sleep(0.5)  # Rate limit
    
    save_state(state)
    log.info(f"Bulk rename complete: {changed} updated, {skipped} unchanged, {errors} errors")


# ─── Push All: Scan & Push ─────────────────────────────────────────────────

def scan_and_push(wiki, config, state, push_new=False, dry_run=False):
    """Scan all local .mediawiki files and push changes/new pages.
    
    This is the main entry point for automated sync (e.g., cron jobs).
    It finds all local files, checks which have changed or are new,
    and pushes them to the wiki.
    
    Args:
        wiki: TALODWiki instance (must be logged in)
        config: Sync configuration
        state: Sync state
        push_new: If True, also create new pages (with validation)
        dry_run: If True, only show what would happen
    
    Returns:
        dict with counts: {pushed, new, skipped, blocked, errors}
    """
    if not wiki.logged_in:
        log.error("Cannot push: not logged in to wiki")
        return {"pushed": 0, "new": 0, "skipped": 0, "blocked": 0, "errors": 0}

    local_root = Path(config["sync"]["local_root"])
    ext = config["sync"]["file_extension"]
    
    counts = {"pushed": 0, "new": 0, "skipped": 0, "blocked": 0, "errors": 0}
    
    # Find all local .mediawiki files
    all_files = list(local_root.rglob(f"*{ext}"))
    # Skip .letta directories and unorganized archives
    all_files = [f for f in all_files if ".letta" not in f.parts and "unorganized_archive" not in str(f)]
    
    log.info(f"=== Scanning {len(all_files)} local files for changes ===")
    
    for filepath in all_files:
        title = local_file_to_title(filepath, config)
        
        # Skip never_push pages
        if title in config.get("never_push", []):
            counts["skipped"] += 1
            continue
        
        content = read_local_file(filepath)
        local_hash = file_hash(content)
        stored_hash = state["page_hashes"].get(title)
        
        # Check if file has changed since last sync
        if stored_hash and stored_hash == local_hash:
            counts["skipped"] += 1
            continue
        
        # Check if this is a new page or an update
        wiki_content, _ = wiki.get_page_content(title)
        
        if not wiki_content:
            # New page
            if push_new:
                is_valid, reason = validate_new_page(title, content)
                if not is_valid:
                    log.warning(f"BLOCKED new page '{title}': {reason}")
                    counts["blocked"] += 1
                    continue
                
                if dry_run:
                    log.info(f"[DRY RUN] Would create new page: '{title}' ({len(content)} chars)")
                    counts["new"] += 1
                else:
                    summary = config["sync"].get("edit_summary_new", "Created via Takeru (Letta Code auto-sync)")
                    success = wiki.edit_page(title, content, summary)
                    if success:
                        state["page_hashes"][title] = local_hash
                        counts["new"] += 1
                        log.info(f"Created new page: '{title}'")
                    else:
                        counts["errors"] += 1
            else:
                log.info(f"Skip new page '{title}': use --push-new to create")
                counts["skipped"] += 1
        else:
            # Existing page — update
            wiki_hash = file_hash(wiki_content)
            
            # Conflict check
            if stored_hash and stored_hash != wiki_hash:
                log.warning(f"CONFLICT: '{title}' — wiki was edited since last pull. Skipping.")
                handle_conflict(title, filepath, wiki_content, config, state)
                counts["blocked"] += 1
                continue
            
            # Data loss check
            local_len = len(content)
            wiki_len = len(wiki_content)
            if local_len > 0 and wiki_len > 100 and local_len < wiki_len * 0.8:
                log.warning(f"BLOCKED: '{title}' — local is {wiki_len - local_len} chars shorter than wiki")
                counts["blocked"] += 1
                continue
            
            if dry_run:
                log.info(f"[DRY RUN] Would update: '{title}'")
                counts["pushed"] += 1
            else:
                summary = config["sync"].get("edit_summary_push", "Updated via Takeru (Letta Code auto-sync)")
                success = wiki.edit_page(title, content, summary)
                if success:
                    state["page_hashes"][title] = local_hash
                    counts["pushed"] += 1
                else:
                    counts["errors"] += 1
        
        time.sleep(0.5)  # Rate limit
    
    save_state(state)
    log.info(f"=== Scan complete: {counts['pushed']} updated, {counts['new']} new, "
             f"{counts['skipped']} skipped, {counts['blocked']} blocked, {counts['errors']} errors ===")
    return counts


# ─── Status Display ──────────────────────────────────────────────────────────

def show_status(config, state):
    """Display current sync status."""
    print("\n" + "=" * 60)
    print("  TALOD WIKI SYNC STATUS")
    print("=" * 60)
    print(f"  Last pull:       {state.get('last_pull', 'Never')}")
    print(f"  Tracked pages:   {len(state.get('page_hashes', {}))}")
    print(f"  Active conflicts: {len(state.get('conflicts', []))}")
    print(f"  Poll interval:    {config['sync']['poll_interval_seconds'] // 60} min")
    print(f"  Push enabled:     {config['sync'].get('push_enabled', True)}")
    print(f"  Pull enabled:     {config['sync'].get('pull_enabled', True)}")
    print(f"  Local root:       {config['sync']['local_root']}")

    if state.get("conflicts"):
        print(f"\n  WARNING - CONFLICTS:")
        for c in state["conflicts"][-5:]:
            print(f"    - {c['title']} ({c['timestamp']})")

    print("=" * 60 + "\n")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TALOD Wiki Bidirectional Sync")
    parser.add_argument("--full", action="store_true", help="Full pull of all wiki pages")
    parser.add_argument("--update", action="store_true", help="Incremental pull (changed pages only)")
    parser.add_argument("--watch", action="store_true", help="Start background sync service")
    parser.add_argument("--push", type=str, help="Push a single file to the wiki")
    parser.add_argument("--push-new", action="store_true", help="Push new pages (pages that don't exist on wiki yet) with validation")
    parser.add_argument("--push-all", action="store_true", help="Scan all local files and push changes + new pages")
    parser.add_argument("--status", action="store_true", help="Show sync status")
    parser.add_argument("--dry-run", action="store_true", help="Don't write anything, just show what would happen")
    parser.add_argument("--bulk-rename", type=str, nargs="+", help="Bulk rename: --bulk-rename Old1=New1 Old2=New2 ...")
    args = parser.parse_args()

    config = load_config()
    state = load_state()

    if args.dry_run:
        config["sync"]["dry_run"] = True
        log.info("DRY RUN MODE — no files will be written")

    wiki = TALODWiki(config)

    # Try to log in (for push capability)
    if config["wiki"].get("bot_username"):
        wiki.login()
        if wiki.logged_in:
            wiki.get_edit_token()

    if args.status:
        show_status(config, state)
        return

    if args.full:
        full_pull(wiki, config, state)
        return

    if args.update:
        incremental_pull(wiki, config, state)
        return

    if args.push:
        filepath = Path(args.push)
        if not filepath.exists():
            log.error(f"File not found: {filepath}")
            sys.exit(1)
        push_file(filepath, wiki, config, state, allow_new=args.push_new)
        return

    if args.push_all:
        scan_and_push(wiki, config, state, push_new=args.push_new, dry_run=args.dry_run)
        return

    if args.push_new and not args.push and not args.push_all:
        # --push-new alone: scan for new pages only
        scan_and_push(wiki, config, state, push_new=True, dry_run=args.dry_run)
        return

    if args.watch:
        watch_mode(wiki, config, state)
        return

    if args.bulk_rename:
        # Parse replacements from "Old=New" format
        replacements = []
        for pair in args.bulk_rename:
            if "=" not in pair:
                log.error(f"Invalid rename format '{pair}'. Use Old=New")
                sys.exit(1)
            old, new = pair.split("=", 1)
            replacements.append((old, new))
            # Also add case variations
            if old[0].isupper():
                replacements.append((old[0].lower() + old[1:], new[0].lower() + new[1:]))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_replacements = []
        for pair in replacements:
            if pair not in seen:
                seen.add(pair)
                unique_replacements.append(pair)
        
        log.info(f"Bulk rename: {unique_replacements}")
        bulk_rename(wiki, config, state, unique_replacements, dry_run=args.dry_run)
        return

    # Default: show help
    parser.print_help()
    print("\nQuick start:")
    print("  python sync_talod.py --full       # First time: pull everything")
    print("  python sync_talod.py --watch      # Start background sync service")
    print("  python sync_talod.py --push-all   # Push all local changes to wiki")
    print("  python sync_talod.py --push-new   # Create new wiki pages from local files")
    print("  python sync_talod.py --push-all --push-new  # Push changes + create new pages")


if __name__ == "__main__":
    main()
