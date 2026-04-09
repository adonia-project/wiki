#!/usr/bin/env python3
"""
Pull all articles from Talod Miraheze wiki and save locally.

This script connects to the Miraheze wiki and downloads all articles
from the main namespace and template namespace, saving them as .mediawiki files.

Usage:
    python pull_wiki_articles.py [--dry-run] [--output-dir PATH]

Credentials are read from .env file or WIKI_USER/WIKI_PASSWORD environment variables.
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

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


class WikiPuller:
    """Pull articles from a MediaWiki instance using direct API calls."""

    EXCLUDED_CATEGORIES = ['basis']  # Lowercase for case-insensitive matching

    def __init__(self, site_url: str, output_dir: Path, dry_run: bool = False,
                 username: str = None, password: str = None):
        self.site_url = site_url.rstrip('/')
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.username = username
        self.password = password
        self.session = None

    def connect(self):
        """Connect to the wiki with proper user-agent."""
        print(f"Connecting to {self.site_url}...")

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TalodWikiPuller/1.0 (Automated wiki backup script) python-requests/2.32.0'
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

    def safe_filename(self, title: str) -> str:
        """Convert a wiki page title to a safe filename."""
        filename = title.replace("/", "_")
        filename = re.sub(r'[<>:"|?*]', "_", filename)
        filename = filename.strip(". ")
        if not filename:
            filename = "unnamed"
        return filename

    def get_all_pages(self, namespace: int = 0) -> list:
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

    def download_page_with_categories(self, title: str) -> tuple:
        """Download page content and check categories in ONE API call."""
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
                content = None
                has_excluded = False

                # Get content
                if 'revisions' in page_data:
                    content = page_data['revisions'][0].get('*', '')

                # Check categories
                categories = page_data.get('categories', [])
                for cat in categories:
                    cat_name = cat.get('title', '').replace('Category:', '').lower()
                    if cat_name in self.EXCLUDED_CATEGORIES:
                        has_excluded = True
                        break

                return (content, has_excluded)

            return (None, False)

        except Exception as e:
            print(f"Error downloading '{title}': {e}")
            return (None, False)

    def pull_namespace(self, namespace: int, target_dir: Path):
        """Pull all pages from a namespace."""
        pages = self.get_all_pages(namespace)

        if not pages:
            print(f"No pages found in namespace {namespace}")
            return

        print(f"\nDownloading {len(pages)} pages to {target_dir}/...")

        success_count = 0
        error_count = 0
        skip_count = 0
        excluded_count = 0

        for i, title in enumerate(pages, 1):
            filename = self.safe_filename(title) + ".mediawiki"
            output_path = target_dir / filename

            # Skip if already exists
            if output_path.exists() and not self.dry_run:
                skip_count += 1
                if i % 50 == 0:
                    print(f"  [{i}/{len(pages)}] {skip_count} skipped, {success_count} downloaded", end="\r")
                continue

            if self.dry_run:
                print(f"  [DRY RUN] Would save '{title}'")
                success_count += 1
                continue

            print(f"  [{i}/{len(pages)}] Pulling '{title}'...", end="\r")

            # ONE call for both content and categories
            content, has_excluded = self.download_page_with_categories(title)

            if has_excluded:
                excluded_count += 1
                continue

            if content is not None:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                success_count += 1
            else:
                error_count += 1

            # Small delay every 20 pages
            if i % 20 == 0:
                time.sleep(0.2)

        print(f"\n  Completed: {success_count} downloaded, {skip_count} skipped, {excluded_count} excluded, {error_count} failed")

    def pull_all(self):
        """Pull all articles from configured namespaces."""
        self.pull_namespace(namespace=0, target_dir=self.output_dir)

        templates_dir = self.output_dir / "Templates"
        self.pull_namespace(namespace=10, target_dir=templates_dir)


def main():
    parser = argparse.ArgumentParser(description="Pull all articles from Talod Miraheze wiki")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded")
    parser.add_argument("--output-dir", type=Path, default=None, help="Custom output directory")
    parser.add_argument("--user", type=str, default=None, help="MediaWiki username")
    parser.add_argument("--password", type=str, default=None, help="MediaWiki password")

    args = parser.parse_args()

    username = args.user or os.environ.get("WIKI_USER")
    password = args.password or os.environ.get("WIKI_PASSWORD")

    script_dir = Path(__file__).parent
    output_dir = args.output_dir or (script_dir.parent / "articles")
    output_dir.mkdir(parents=True, exist_ok=True)

    puller = WikiPuller(
        site_url="https://talod.miraheze.org",
        output_dir=output_dir,
        dry_run=args.dry_run,
        username=username,
        password=password
    )

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No files will be downloaded")
        print("=" * 60)

    puller.connect()
    puller.pull_all()

    print("\nDone!")


if __name__ == "__main__":
    main()
