#!/usr/bin/env python3
"""
Bidirectional sync between local wiki articles and Talod Miraheze wiki.

This script:
1. Pulls current state from wiki
2. Compares with local files
3. Uploads files that changed locally
4. Downloads files that changed on wiki

Usage:
    python sync_with_talod.py [--dry-run] [--upload-only] [--download-only]

Credentials are read from .env file or WIKI_USER/WIKI_PASSWORD environment variables.
"""

import argparse
import hashlib
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


class WikiSyncer:
    """Bidirectional sync between local files and MediaWiki instance."""

    EXCLUDED_CATEGORIES = ['basis']

    def __init__(self, site_url: str, articles_dir: Path, dry_run: bool = False,
                 username: str = None, password: str = None):
        self.site_url = site_url.rstrip('/')
        self.articles_dir = articles_dir
        self.dry_run = dry_run
        self.username = username
        self.password = password
        self.session = None
        self.csrf_token = None
        self.local_files: Dict[str, Tuple[Path, str]] = {}  # title -> (path, content_hash)
        self.wiki_pages: Dict[str, str] = {}  # title -> content_hash

    def connect(self):
        """Connect to the wiki and get edit token."""
        print(f"Connecting to {self.site_url}...")

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TalodWikiSyncer/1.0 (Bidirectional wiki sync script) python-requests/2.32.0'
        })

        try:
            response = self.session.get(f"{self.site_url}/w/api.php", params={
                'action': 'query',
                'meta': 'siteinfo',
                'format': 'json'
            })
            response.raise_for_status()
            data = response.json()

            sitename = data.get('query', {}).get('general', {}).get('sitename', 'Unknown')
            print(f"Connected to {sitename}")

            if self.username and self.password:
                print(f"Logging in as {self.username}...")
                self._login()
                print("Logged in successfully.")

                # Get CSRF token for editing
                self._get_csrf_token()

        except Exception as e:
            print(f"Error connecting to wiki: {e}")
            sys.exit(1)

    def _login(self):
        """Login to the wiki using bot password."""
        response = self.session.get(f"{self.site_url}/w/api.php", params={
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
            'format': 'json'
        })
        data = response.json()
        login_token = data['query']['tokens']['logintoken']

        response = self.session.post(f"{self.site_url}/w/api.php", data={
            'action': 'login',
            'lgname': self.username,
            'lgpassword': self.password,
            'lgtoken': login_token,
            'format': 'json'
        })
        data = response.json()

        if data.get('login', {}).get('result') != 'Success':
            print(f"Login failed: {data}")
            sys.exit(1)

    def _get_csrf_token(self):
        """Get CSRF token for editing."""
        response = self.session.get(f"{self.site_url}/w/api.php", params={
            'action': 'query',
            'meta': 'tokens',
            'format': 'json'
        })
        data = response.json()
        self.csrf_token = data.get('query', {}).get('tokens', {}).get('csrftoken')

        if not self.csrf_token:
            print("Failed to get CSRF token")
            sys.exit(1)

    def filename_to_title(self, filename: str) -> str:
        """Convert a filename back to wiki page title."""
        # Remove .mediawiki extension
        title = re.sub(r'\.mediawiki$', '', filename)
        # Handle Template: prefix
        if title.startswith('Template_'):
            title = 'Template:' + title[9:]
        return title

    def safe_filename(self, title: str) -> str:
        """Convert a wiki page title to a safe filename."""
        filename = title.replace("/", "_")
        filename = re.sub(r'[<>:"|?*]', "_", filename)
        filename = filename.strip(". ")
        if not filename:
            filename = "unnamed"
        return filename

    def get_content_hash(self, content: str) -> str:
        """Get SHA256 hash of content for comparison."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def scan_local_files(self):
        """Scan local directory for all .mediawiki files."""
        print(f"\nScanning local files in {self.articles_dir}/...")

        count = 0
        for mediawiki_file in self.articles_dir.rglob("*.mediawiki"):
            # Skip files in Countries/ subFolders (organized structure)
            # We'll sync from the flat structure perspective
            # Actually, we should sync the organized structure too

            try:
                with open(mediawiki_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Derive title from path
                rel_path = mediawiki_file.relative_to(self.articles_dir)
                title = self.filename_to_title(str(rel_path))

                content_hash = self.get_content_hash(content)
                self.local_files[title] = (mediawiki_file, content_hash)
                count += 1

            except Exception as e:
                print(f"  Error reading {mediawiki_file}: {e}")

        print(f"  Found {count} local files")

    def get_all_wiki_pages(self, namespace: int = 0) -> list:
        """Get all pages in a given namespace."""
        print(f"Listing all pages in namespace {namespace}...")

        pages = []
        apcontinue = ''

        try:
            while True:
                params = {
                    'action': 'query',
                    'list': 'allpages',
                    'apnamespace': namespace,
                    'aplimit': 500,
                    'format': 'json'
                }

                if apcontinue:
                    params['apcontinue'] = apcontinue

                response = self.session.get(f"{self.site_url}/w/api.php", params=params)
                response.raise_for_status()
                data = response.json()

                batch = data.get('query', {}).get('allpages', [])
                pages.extend([p['title'] for p in batch])

                if 'continue' in data:
                    apcontinue = data['continue'].get('apcontinue', '')
                else:
                    break

                if len(pages) % 500 == 0:
                    print(f"  Found {len(pages)} pages...", end="\r")
                    time.sleep(0.5)

            print(f"  Found {len(pages)} pages total.    ")
            return pages

        except Exception as e:
            print(f"Error listing pages: {e}")
            return []

    def fetch_wiki_page_hash(self, title: str) -> Optional[str]:
        """Fetch page content hash from wiki."""
        try:
            response = self.session.get(f"{self.site_url}/w/api.php", params={
                'action': 'query',
                'titles': title,
                'prop': 'revisions',
                'rvprop': 'content',
                'format': 'json'
            })
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'revisions' in page_data:
                    content = page_data['revisions'][0].get('*', '')
                    return self.get_content_hash(content)

            return None

        except Exception as e:
            print(f"Error fetching '{title}': {e}")
            return None

    def fetch_wiki_page_content(self, title: str) -> Optional[str]:
        """Fetch full page content from wiki."""
        try:
            response = self.session.get(f"{self.site_url}/w/api.php", params={
                'action': 'query',
                'titles': title,
                'prop': 'revisions|categories',
                'rvprop': 'content',
                'cllimit': 500,
                'format': 'json'
            })
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                # Check for excluded categories
                categories = page_data.get('categories', [])
                for cat in categories:
                    cat_name = cat.get('title', '').replace('Category:', '').lower()
                    if cat_name in self.EXCLUDED_CATEGORIES:
                        return None  # Skip excluded pages

                if 'revisions' in page_data:
                    return page_data['revisions'][0].get('*', '')

            return None

        except Exception as e:
            print(f"Error fetching '{title}': {e}")
            return None

    def upload_page(self, title: str, content: str, summary: str = "Synced from local repository") -> bool:
        """Upload a page to the wiki."""
        if self.dry_run:
            print(f"  [DRY RUN] Would upload '{title}'")
            return True

        try:
            response = self.session.post(f"{self.site_url}/w/api.php", data={
                'action': 'edit',
                'title': title,
                'text': content,
                'summary': summary,
                'token': self.csrf_token,
                'format': 'json'
            })
            response.raise_for_status()
            data = response.json()

            if data.get('edit', {}).get('result') == 'Success':
                return True
            else:
                print(f"  Upload failed for '{title}': {data}")
                return False

        except Exception as e:
            print(f"  Error uploading '{title}': {e}")
            return False

    def download_page(self, title: str, target_path: Path) -> bool:
        """Download a page from wiki to local file."""
        if self.dry_run:
            print(f"  [DRY RUN] Would download '{title}' to {target_path}")
            return True

        content = self.fetch_wiki_page_content(title)
        if content is None:
            return False

        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    def sync_namespace(self, namespace: int, upload: bool = True, download: bool = True):
        """Sync a single namespace."""
        pages = self.get_all_wiki_pages(namespace)
        if not pages:
            return

        print(f"\nSyncing {len(pages)} pages in namespace {namespace}...")

        uploads = 0
        downloads = 0
        unchanged = 0

        for i, title in enumerate(pages, 1):
            print(f"  [{i}/{len(pages)}] Checking '{title}'...", end="\r")

            wiki_hash = self.fetch_wiki_page_hash(title)

            # Check if we have this locally
            if title in self.local_files:
                local_path, local_hash = self.local_files[title]

                if wiki_hash is None:
                    # Wiki doesn't have it, upload
                    if upload:
                        with open(local_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if self.upload_page(title, content, summary="Synced from local repository"):
                            uploads += 1
                elif local_hash != wiki_hash:
                    # Both exist but differ
                    if upload:
                        # Upload our version (local wins)
                        with open(local_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if self.upload_page(title, content, summary="Synced from local repository"):
                            uploads += 1
                    else:
                        unchanged += 1
                else:
                    unchanged += 1
            else:
                # We don't have it locally, download
                if download and wiki_hash is not None:
                    filename = self.safe_filename(title) + ".mediawiki"
                    if namespace == 10:  # Template namespace
                        target_path = self.articles_dir / "Templates" / filename
                    else:
                        target_path = self.articles_dir / filename

                    if self.download_page(title, target_path):
                        downloads += 1

            if i % 20 == 0:
                time.sleep(0.2)

        print(f"\n  Done: {uploads} uploaded, {downloads} downloaded, {unchanged} unchanged")

    def upload_new_local_files(self):
        """Upload local files that don't exist on wiki."""
        print("\nChecking for new local files to upload...")

        uploads = 0

        for i, (title, (path, _)) in enumerate(self.local_files.items(), 1):
            # Determine if this is a template
            namespace = 10 if title.startswith('Template:') else 0
            wiki_title = title

            # Get corresponding wiki pages for this namespace
            wiki_pages = self.get_all_wiki_pages(namespace)

            if wiki_title not in wiki_pages:
                print(f"  [{i}] Uploading new file '{title}'...")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if self.upload_page(wiki_title, content, summary="New article from local repository"):
                    uploads += 1

        print(f"  Uploaded {uploads} new files")

    def sync(self, upload: bool = True, download: bool = True):
        """Perform bidirectional sync."""
        self.scan_local_files()

        # Sync main namespace
        self.sync_namespace(namespace=0, upload=upload, download=download)

        # Sync template namespace
        print("\nSyncing Template namespace...")
        self.sync_namespace(namespace=10, upload=upload, download=download)

        # Upload any new local files that don't exist on wiki
        if upload:
            self.upload_new_local_files()


def main():
    parser = argparse.ArgumentParser(description="Sync local wiki articles with Talod Miraheze")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be synced")
    parser.add_argument("--upload-only", action="store_true", help="Only upload changes, don't download")
    parser.add_argument("--download-only", action="store_true", help="Only download changes, don't upload")
    parser.add_argument("--user", type=str, default=None, help="MediaWiki username")
    parser.add_argument("--password", type=str, default=None, help="MediaWiki password")

    args = parser.parse_args()

    username = args.user or os.environ.get("WIKI_USER")
    password = args.password or os.environ.get("WIKI_PASSWORD")

    if not username or not password:
        print("Error: WIKI_USER and WIKI_PASSWORD must be set (via .env or arguments)")
        sys.exit(1)

    script_dir = Path(__file__).parent
    articles_dir = script_dir.parent / "articles"

    if not articles_dir.exists():
        print(f"Error: Articles directory not found: {articles_dir}")
        sys.exit(1)

    upload = not args.download_only
    download = not args.upload_only

    syncer = WikiSyncer(
        site_url="https://talod.miraheze.org",
        articles_dir=articles_dir,
        dry_run=args.dry_run,
        username=username,
        password=password
    )

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No changes will be made")
        print("=" * 60)

    syncer.connect()
    syncer.sync(upload=upload, download=download)

    print("\nSync complete!")


if __name__ == "__main__":
    main()
