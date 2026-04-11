#!/bin/bash
# Initialize local MediaWiki with articles from the repository
# This script imports all .mediawiki files into a local Docker MediaWiki

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WIKI_DIR="$(dirname "$SCRIPT_DIR")"
ARTICLES_DIR="$WIKI_DIR/articles"
WIKI_DATA="$WIKI_DIR/wiki-data"

echo "=== Talod Wiki Local Renderer ==="
echo ""

# Check Docker is running
if ! docker info &>/dev/null; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Ensure wiki-data directory exists
mkdir -p "$WIKI_DATA"

# DON'T create LocalSettings.php on first run
# MediaWiki needs to show its web installer without LocalSettings.php
# After user completes installation, they download LocalSettings.php

# Recreate container to pick up new volume mounts
echo "Recreating MediaWiki container..."
cd "$WIKI_DIR"
docker compose down 2>/dev/null || true
docker compose up -d mediawiki

echo "Waiting for MediaWiki to start..."
sleep 5

# Check if container is ready
until docker exec talod-wiki true 2>/dev/null; do
    sleep 2
done

echo "MediaWiki is running at http://localhost:8080"

# Check if database exists and has tables
# Database name is configured during web installer (default: my_wiki.sqlite)
DB_FILE=$(ls "$WIKI_DATA"/*.sqlite 2>/dev/null | grep -v jobqueue | grep -v l10n | grep -v cache | head -1 || echo "")
NEEDS_INIT=false

if [ -z "$DB_FILE" ]; then
    NEEDS_INIT=true
fi

if [ "$NEEDS_INIT" = true ]; then
    echo ""
    echo "=== First-Time Setup Required ==="
    echo ""
    echo "MediaWiki needs to be initialized. Please:"
    echo ""
    echo "1. Open http://localhost:8080 in your browser"
    echo "2. Click 'set up the wiki' to start the installer"
    echo "3. Use these settings:"
    echo ""
    echo "   Language: Your choice"
    echo "   Database type: SQLite"
    echo "   SQLite data directory: /var/www/data (default)"
    echo "   Wiki name: Talod Wiki"
    echo "   Admin username: Admin"
    echo "   Admin password: (your choice)"
    echo ""
    echo "4. After setup completes, download LocalSettings.php"
    echo "5. Place it in: $WIKI_DATA/LocalSettings.php"
    echo "6. Re-run this script to import articles"
    echo ""
    echo "Container is running. Waiting for setup..."
    exit 0
fi

# Import articles using maintenance script
echo ""
echo "=== Importing Articles ==="
echo ""

# Create import XML from .mediawiki files
IMPORT_XML="$WIKI_DIR/wiki-data/import.xml"
mkdir -p "$(dirname "$IMPORT_XML")"

python3 "$SCRIPT_DIR/generate_import_xml.py" "$ARTICLES_DIR" "$IMPORT_XML"

echo "Importing articles into MediaWiki..."
docker exec -i talod-wiki php maintenance/importDump.php < "$IMPORT_XML"

echo ""
echo "=== Import Complete ==="
echo ""
echo "View your local wiki: http://localhost:8080"
echo ""
echo "Commands:"
echo "  docker compose stop      # Stop containers"
echo "  docker compose start     # Start containers again"
echo "  docker compose down      # Stop and remove containers"
