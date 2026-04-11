#!/bin/bash
# Initialize local MediaWiki with articles from the repository
# This script imports all .mediawiki files into a local Docker MediaWiki

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WIKI_DIR="$(dirname "$SCRIPT_DIR")"
ARTICLES_DIR="$WIKI_DIR/articles"

echo "=== Talod Wiki Local Renderer ==="
echo ""

# Check Docker is running
if ! docker info &>/dev/null; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if containers are running
MW_RUNNING=$(docker ps -q -f name=talod-wiki 2>/dev/null)

if [ "$MW_RUNNING" = "" ]; then
    echo "Starting MediaWiki container..."
    cd "$WIKI_DIR"
    docker compose up -d mediawiki

    echo "Waiting for MediaWiki to start..."
    sleep 10

    # Check if initialized
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
