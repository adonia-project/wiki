# Adonia Project Wiki Repository

This repository serves as the source of truth for all Talod wiki articles from Miraheze. Articles are organized by category and can be synced back to a MediaWiki installation.

## Repository Structure

```
wiki/
├── scripts/           # Utility scripts
│   └── pull_wiki_articles.py
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

## Contributing

1. Articles can be edited directly in `.mediawiki` files
2. Changes should be committed to this repository
3. Future scripts will allow pushing updates back to MediaWiki

## License

[Add license information here]
