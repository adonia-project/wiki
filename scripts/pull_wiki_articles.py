#!/usr/bin/env python3
"""
Pull all articles from Talod Miraheze wiki and save locally.

This script connects to the Miraheze wiki and downloads all articles
from the main namespace and template namespace, saving them as .mediawiki files.

Usage:
    python pull_wiki_articles.py [--dry-run] [--output-dir PATH]

Options:
    --dry-run        Show what would be downloaded without actually downloading
    --output-dir     Custom output directory (default: ../articles)
    --user           MediaWiki username (optional, for higher rate limits)
    --password       MediaWiki password (optional)
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

try:
    import mwclient
except ImportError:
    print("Error: mwclient is required. Install with: pip install mwclient")
    sys.exit(1)


class WikiPuller:
    """Pull articles from a MediaWiki instance."""

    def __init__(self, site_url: str, output_dir: Path, dry_run: bool = False,
                 username: str = None, password: str = None):
        self.site_url = site_url
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.username = username
        self.password = password
        self.site = None

    def connect(self):
        """Connect to the wiki."""
        print(f"Connecting to {self.site_url}...")

        # mwclient expects site without protocol
        site_host = self.site_url.replace("https://", "").replace("http://", "")

        try:
            self.site = mwclient.Site(site_host)

            if self.username and self.password:
                print(f"Logging in as {self.username}...")
                self.site.login(self.username, self.password)
                print("Logged in successfully.")
            else:
                print("Connected anonymously.")

        except Exception as e:
            print(f"Error connecting to wiki: {e}")
            sys.exit(1)

    def safe_filename(self, title: str) -> str:
        """Convert a wiki page title to a safe filename."""
        # Replace slashes with underscores
        filename = title.replace("/", "_")

        # Remove or replace other problematic characters
        filename = re.sub(r'[<>:"|?*]', "_", filename)

        # Remove leading/trailing spaces and dots
        filename = filename.strip(". ")

        # Ensure we have a valid filename
        if not filename:
            filename = "unnamed"

        return filename

    def get_all_pages(self, namespace: int) -> list:
        """Get all pages in a given namespace."""
        print(f"Listing all pages in namespace {namespace}...")

        pages = []
        try:
            for page in self.site.allpages(namespace=namespace):
                pages.append(page.name)
                # Progress indicator every 50 pages
                if len(pages) % 50 == 0:
                    print(f"  Found {len(pages)} pages...", end="\r")

            print(f"  Found {len(pages)} pages total.    ")
            return pages

        except Exception as e:
            print(f"Error listing pages: {e}")
            return []

    def download_page(self, title: str, output_path: Path) -> bool:
        """Download a single page and save to disk."""
        try:
            page = self.site.pages[title]
            content = page.text()

            if content is None:
                print(f"  Warning: No content for '{title}'")
                return False

            if self.dry_run:
                print(f"  [DRY RUN] Would save '{title}' to {output_path}")
                return True

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"  Error downloading '{title}': {e}")
            return False

    def pull_namespace(self, namespace: int, target_dir: Path):
        """Pull all pages from a namespace."""
        pages = self.get_all_pages(namespace)

        if not pages:
            print(f"No pages found in namespace {namespace}")
            return

        print(f"\nDownloading {len(pages)} pages to {target_dir}/...")

        success_count = 0
        error_count = 0

        for i, title in enumerate(pages, 1):
            filename = self.safe_filename(title) + ".mediawiki"
            output_path = target_dir / filename

            # Skip if already exists (can add --force flag later if needed)
            if output_path.exists() and not self.dry_run:
                print(f"  [{i}/{len(pages)}] Skipping '{title}' (already exists)")
                success_count += 1
                continue

            print(f"  [{i}/{len(pages)}] Pulling '{title}'...", end="\r")

            if self.download_page(title, output_path):
                success_count += 1
            else:
                error_count += 1

            # Small delay to be nice to the server
            if not self.dry_run and i % 10 == 0:
                time.sleep(0.5)

        print(f"\n  Completed: {success_count} successful, {error_count} failed")

    def pull_all(self):
        """Pull all articles from configured namespaces."""
        # Main namespace (0)
        self.pull_namespace(namespace=0, target_dir=self.output_dir)

        # Template namespace (10)
        templates_dir = self.output_dir / "Templates"
        self.pull_namespace(namespace=10, target_dir=templates_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Pull all articles from Talod Miraheze wiki"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Custom output directory (default: ../articles relative to script)"
    )
    parser.add_argument(
        "--user",
        type=str,
        default=None,
        help="MediaWiki username (optional, for higher rate limits)"
    )
    parser.add_argument(
        "--password",
        type=str,
        default=None,
        help="MediaWiki password (optional)"
    )

    args = parser.parse_args()

    # Determine output directory
    script_dir = Path(__file__).parent
    output_dir = args.output_dir or (script_dir.parent / "articles")

    # Create output dir if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create the puller and run
    puller = WikiPuller(
        site_url="https://talod.miraheze.org",
        output_dir=output_dir,
        dry_run=args.dry_run,
        username=args.user,
        password=args.password
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
