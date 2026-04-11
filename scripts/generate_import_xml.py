#!/usr/bin/env python3
"""
Generate MediaWiki XML import file from local .mediawiki files.

This creates an XML dump that can be imported via `maintenance/importDump.php`
or via the Special:Import page.

Usage:
    python generate_import_xml.py /path/to/articles /path/to/output.xml
"""

import os
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

def filename_to_title(filename: str, articles_dir: Path, filepath: Path) -> str:
    """Convert filename back to wiki title."""
    # Get relative path from articles directory
    rel_path = filepath.relative_to(articles_dir)

    # Remove .mediawiki extension
    title = str(rel_path)[:-len('.mediawiki')]

    # Convert path separators back to wiki namespace conventions
    # Countries/Burawa/History/Ancient Southwestern Kaftia -> Ancient Southwestern Kaftia
    # Templates/Template_Infobox -> Template:Infobox

    parts = title.split('/')
    if parts:
        # Last part is the actual title
        title = parts[-1]

        # Handle Templates folder specially
        if 'Templates' in parts:
            # Convert Template_Name -> Template:Name
            if title.startswith('Template_'):
                title = 'Template:' + title[9:]

    return title

def generate_xml(articles_dir: Path, output_file: Path):
    """Generate MediaWiki XML import file."""

    print(f"Scanning {articles_dir} for .mediawiki files...")

    pages = []

    for mediawiki_file in articles_dir.rglob("*.mediawiki"):
        # Skip Templates subfolder in the wrong location
        parts = mediawiki_file.relative_to(articles_dir).parts
        if '.gitkeep' in str(mediawiki_file):
            continue

        title = filename_to_title(
            mediawiki_file.name,
            articles_dir,
            mediawiki_file
        )

        with open(mediawiki_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pages.append((title, content, mediawiki_file.stat().st_mtime))
        print(f"  Found: {title}")

    print(f"\nFound {len(pages)} pages")

    # Generate XML
    print(f"\nGenerating XML to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" ')
        f.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
        f.write('xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.11/ ')
        f.write('http://www.mediawiki.org/xml/export-0.11.xsd" ')
        f.write('version="0.11" xml:lang="en">\n')

        for title, content, mtime in pages:
            # Determine namespace based on title
            ns = 0
            if title.startswith('Template:'):
                ns = 10
                title = title[9:]  # Remove Template: prefix from title
            elif title.startswith('Category:'):
                ns = 14
                title = title[9:]

            f.write('  <page>\n')
            f.write(f'    <title>{escape(title)}</title>\n')
            f.write(f'    <ns>{ns}</ns>\n')
            f.write('    <id>1</id>\n')
            f.write('    <revision>\n')
            f.write('      <id>1</id>\n')
            f.write(f'      <timestamp>{mtime:.0f}</timestamp>\n')
            f.write('      <contributor>\n')
            f.write('        <username>Local Import</username>\n')
            f.write('        <id>0</id>\n')
            f.write('      </contributor>\n')
            f.write(f'      <text xml:space="preserve">{escape(content)}</text>\n')
            f.write('    </revision>\n')
            f.write('  </page>\n')

        f.write('</mediawiki>\n')

    print(f"Generated XML with {len(pages)} pages")

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_import_xml.py <articles_dir> <output.xml>")
        sys.exit(1)

    articles_dir = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not articles_dir.exists():
        print(f"Error: Articles directory not found: {articles_dir}")
        sys.exit(1)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    generate_xml(articles_dir, output_file)

if __name__ == "__main__":
    main()
