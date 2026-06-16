# AFA game generator

This folder contains the deterministic simulator used to generate AFA World Cup match playstrings and result output.

## Contents

- `generate_afc_match_playstring.py` — simulates one match or a batch of fixtures
- `data/afa_mens_world_ranking.csv` — fallback Elo/ranking lookup for teams
- `data/afa_team_rosters.csv` — fallback player-roster lookup for teams
- `data/afa_world_cup_results.csv` — tournament reference results for historical context

## How it works

The generator resolves missing ratings and player lists from the CSV data in this folder. If a fixture row omits `home_elo`, `away_elo`, `home_players`, or `away_players`, the script will look up the values from the ranking and roster files.

The batch mode accepts a CSV with `home_*` and `away_*` columns, which makes it convenient for simulating an entire matchday from a fixture list.

## Example commands

Single match:

```bash
python scripts/afa-generator/generate_afc_match_playstring.py \
  --home-country Balboa \
  --away-country Tondano \
  --format text
```

Batch mode:

```bash
python scripts/afa-generator/generate_afc_match_playstring.py \
  --fixture-csv scripts/afa-generator/data/june16_fixtures.csv \
  --pretty
```

## Fixture CSV columns

A fixture CSV can include the following columns:

- `match_id`
- `noise_seed`
- `home_team`
- `home_country`
- `home_elo`
- `home_players`
- `away_team`
- `away_country`
- `away_elo`
- `away_players`
- `min_stoppage`
- `max_stoppage`

Player lists should be semicolon-separated if provided directly in the fixture file.

## Notes

- Keep new team rosters in `data/afa_team_rosters.csv`.
- Keep new ranking values in `data/afa_mens_world_ranking.csv`.
- Use `--format text` when you want human-readable output for a wiki match report.
- Use `--format json --pretty` when you want machine-readable match data for later article generation.