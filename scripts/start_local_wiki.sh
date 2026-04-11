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

# Check if LocalSettings.php exists, copy from example if not
if [ ! -f "$WIKI_DATA/LocalSettings.php" ]; then
    echo "First run detected. Creating LocalSettings.php..."
    if [ -f "$WIKI_DIR/LocalSettings.php.example" ]; then
        cp "$WIKI_DIR/LocalSettings.php.example" "$WIKI_DATA/LocalSettings.php"
        echo "Created LocalSettings.php from example."
    else
        echo "Error: LocalSettings.php.example not found"
        exit 1
    fi
fi

# Check if containers are running
MW_RUNNING=$(docker ps -q -f name=talod-wiki 2>/dev/null)

if [ "$MW_RUNNING" = "" ]; then
    echo "Starting MediaWiki container..."
    cd "$WIKI_DIR"
    docker compose up -d mediawiki

    echo "Waiting for MediaWiki to start..."
    sleep 5

    # Check if container is ready
    until docker exec talod-wiki true 2>/dev/null; do
        sleep 2
    done

    echo "MediaWiki is running at http://localhost:8080"
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
