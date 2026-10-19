# Adonia Project Wiki Repository

This repository serves as the source of truth for all Talod wiki articles from Miraheze. Articles are organized by category and can be synced back to a MediaWiki installation.

## Repository Structure

```
wiki/
├── scripts/           # Utility scripts
│   ├── pull_wiki_articles.py
│   └── sync_with_talod.py
│   ├── pull_wiki_articles.py  # Pull from Miraheze
│   ├── sync_with_talod.py     # Bidirectional sync
│   ├── render_wiki_page.py    # Static HTML preview
│   └── start_local_wiki.sh    # Docker MediaWiki
│
└── articles/           # Wiki articles organized by category
    ├── Countries/
    │   └── [Country_Name]/
    │       ├── Laws/
    │       ├── Regions/
    │       ├── Events/
    │       ├── Customs/
    │       └── Economy/
    │
    ├── Former_Countries/
    │   └── [Country_Name]/
    │       ├── Laws/
    │       ├── Regions/
    │       ├── Events/
    │       ├── Customs/
    │       └── Economy/
    │
    ├── Regions/
    │   └── [Region_Name]/
    │       ├── Laws/
    │       ├── Regions/
    │       ├── Events/
    │       ├── Customs/
    │       └── Economy/
    │
    ├── Ethnicities/
    ├── Events/
    ├── Languages/
    ├── Religions/
    ├── Templates/
    └── Other/
```

## Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:adonia-project/wiki.git
   cd wiki
   ```

2. Install dependencies:
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

## Usage

### Pulling Articles from Miraheze

To pull all articles from the Talod Miraheze wiki:

```bash
cd scripts
python pull_wiki_articles.py
```

#### Options

- `--dry-run` - Show what would be downloaded without actually downloading:
  ```bash
  python pull_wiki_articles.py --dry-run
  ```

- `--output-dir PATH` - Custom output directory (default: `../articles`):
  ```bash
  python pull_wiki_articles.py --output-dir /path/to/articles
  ```

- `--user USERNAME` and `--password PASSWORD` - login for higher rate limits (optional):
  ```bash
  python pull_wiki_articles.py --user YourUsername --password YourPassword
  ```

### Syncing with Miraheze (Bidirectional)

To sync local changes back to the wiki and pull remote changes:

```bash
cd scripts
python sync_with_talod.py
```

#### Sync Options

- `--dry-run` - Show what would be synced without making changes:
  ```bash
  python sync_with_talod.py --dry-run
  ```

- `--upload-only` - Only upload local changes to wiki, don't download:
  ```bash
  python sync_with_talod.py --upload-only
  ```

- `--download-only` - Only download remote changes, don't upload:
  ```bash
  python sync_with_talod.py --download-only
  ```

#### How Sync Works

1. Scans all local `.mediawiki` files
2. Fetches all pages from wiki (main namespace + templates)
3. Compares content hashes (SHA256)
4. **Uploads** files that changed locally
5. **Downloads** files that changed on wiki
6. Files in "Basis" category are excluded

**Note:** Requires `WIKI_USER` and `WIKI_PASSWORD` in `.env` file.

### What Gets Downloaded

The script downloads:
- All pages from the main namespace (articles)
- All templates from the Template namespace

Articles are saved as `.mediawiki` files, preserving the original wikitext format.

## File Naming

Wiki page titles are converted to safe filenames:
- `/` characters replaced with `_`
- Invalid characters removed
- `.mediawiki` extension added

Example: `Kingdom of Burawa/History` becomes `Kingdom of Burawa_History.mediawiki`

## Organization (Phase 2)

Future development will include:
- Automatic categorization based on wiki categories
- Category mapping configuration file
- Script to organize articles into appropriate category folders

## Local Rendering (Docker MediaWiki)

Render `.mediawiki` files locally with full template support using Docker MediaWiki.

### Prerequisites
- Docker Desktop (or Docker Engine)
- Docker Compose

### Quick Start

```bash
./scripts/start_local_wiki.sh
```

This will:
1. Start MediaWiki container on port 8080
2. Import all articles from `articles/` directory
3. Serve wiki at http://localhost:8080

### Manual Control

```bash
# Start containers
docker compose up -d

# Import articles
./scripts/start_local_wiki.sh

# Stop containers
docker compose stop

# Stop and remove containers
docker compose down
```

### What Gets Imported

- All `.mediawiki` files from `articles/` directory
- Templates are imported to Template namespace
- Articles maintain their wiki structure

### First Run Setup

On first run, you'll need to complete MediaWiki installation through the web interface:
1. Go to http://localhost:8080
2. Follow the installation wizard
3. Download the generated `LocalSettings.php`
4. Replace the repository `LocalSettings.php` with it

After that, subsequent runs will use the saved configuration.

## Contributing

1. Articles can be edited directly in `.mediawiki` files
2. Use local renderer to preview changes
3. Changes should be committed to this repository
4. Use sync script to push updates back to Miraheze

## License

[Add license information here]
