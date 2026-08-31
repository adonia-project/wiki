#!/usr/bin/env python3
"""
TALOD Wiki Image Uploader — Manual single-file upload to Miraheze wiki.

Uploads image files (SVG, PNG, JPG) to the TALOD Miraheze wiki one at a time.
Reuses the same .env credentials as sync_balboa.py.

Usage:
    python upload_image.py <filepath> [--description "Optional description"]
    python upload_image.py articles/Countries/Balboa/Maps/La Serra de Llevant comarca in Tramuntana.svg
    python upload_image.py map.png --description "Locator map of La Serra de Llevant comarca"
"""

import argparse
import os
import sys
import warnings
from pathlib import Path
from datetime import datetime

# Suppress mwclient deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import mwclient
except ImportError:
    print("Error: mwclient not installed. Run: uv add mwclient")
    sys.exit(1)

# ─── Configuration ───────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.resolve()
ENV_PATH = REPO_ROOT / ".env"

# Simple .env loader
def load_dotenv(path):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

load_dotenv(str(ENV_PATH))

WIKI_URL = os.environ.get("WIKI_URL", "talod.miraheze.org")
WIKI_USERNAME = os.environ.get("WIKI_USERNAME", "")
WIKI_PASSWORD = os.environ.get("WIKI_PASSWORD", "")

# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {level}: {msg}")

def get_wiki_connection():
    """Connect to the Miraheze wiki and authenticate."""
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
                "User-Agent": "TALOD-Upload-Bot/1.0 (https://talod.miraheze.org/; contact@talod.miraheze.org)"
            }
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

def upload_file(site, filepath, description=""):
    """Upload a single file to the wiki."""
    filepath = Path(filepath).resolve()

    if not filepath.exists():
        log(f"File not found: {filepath}", "ERROR")
        sys.exit(1)

    filename = filepath.name
    file_size = filepath.stat().st_size

    # Determine MIME type from extension
    ext = filepath.suffix.lower()
    mime_types = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".pdf": "application/pdf",
    }
    mime = mime_types.get(ext, "application/octet-stream")

    log(f"Uploading '{filename}' ({file_size:,} bytes, {mime})...")

    # Check if file already exists on wiki
    image_page = site.images[filename]
    if image_page.exists:
        log(f"  File '{filename}' already exists on wiki — will be overwritten", "WARN")

    # Upload — mwclient expects a file-like object
    try:
        with open(filepath, "rb") as f:
            site.upload(
                file=f,
                filename=filename,
                description=description,
                comment=f"Upload via upload-bot: {filename}",
                ignore=True,  # Ignore warnings (e.g., file exists)
            )
        log(f"  OK — uploaded as 'File:{filename}'")
        log(f"  URL: https://{WIKI_URL}/wiki/File:{filename.replace(' ', '_')}")
        return True
    except Exception as e:
        log(f"  Upload failed: {e}", "ERROR")
        return False

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TALOD Wiki Image Uploader — upload a single image file")
    parser.add_argument("filepath", help="Path to the image file to upload")
    parser.add_argument("--description", "-d", default="", help="File description (shown on File: page)")
    args = parser.parse_args()

    site = get_wiki_connection()
    upload_file(site, args.filepath, args.description)

if __name__ == "__main__":
    main()
