#!/usr/bin/env python3
"""Generate a deterministic AFC match playstring and result.

The script mixes team names, country names, current Elo ratings, and an
optional noise seed into a weighted match seed. It then simulates minute-by-
minute ball status through stoppage time and emits a final result.

Example:
    python scripts/generate_afc_match_playstring.py \
        --home-team "Balboa XI" --home-country Balboa --home-elo 1587 \
        --away-team "Orma XI" --away-country Orma --away-elo 1695 \
        --match-id june15-01 --noise-seed 42

The output is JSON by default so it can be consumed by downstream tests.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
import unicodedata
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Iterable, Sequence


STATUS_CODES = {
    "home_possession": "p",
    "away_possession": "q",
    "neutral": ".",
    "home_build": "b",
    "away_build": "d",
    "home_attack": "h",
    "away_attack": "a",
    "home_set_piece": "s",
    "away_set_piece": "t",
    "home_goal": "H",
    "away_goal": "A",
}

DEFAULT_RANKINGS_CSV = Path(__file__).resolve().parents[1] / "data" / "afa_mens_world_ranking.csv"
DEFAULT_ROSTERS_CSV = Path(__file__).resolve().parents[1] / "data" / "afa_team_rosters.csv"


@dataclass(slots=True)
class TeamInput:
    team_name: str
    country_name: str
    elo: float | None
    players: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return self.team_name.strip() or self.country_name.strip() or "Unknown"


@dataclass(slots=True)
class MinuteEvent:
    minute: int
    minute_label: str
    status: str
    code: str
    home_score: int
    away_score: int
    home_control: float
    note: str | None = None


@dataclass(slots=True)
class GoalEvent:
    minute: int
    minute_label: str
    team: str
    scorer: str


@dataclass(slots=True)
class SimulationResult:
    match_id: str | None
    home: TeamInput
    away: TeamInput
    seed: dict
    stoppage_minutes: int
    total_minutes: int
    playstring: str
    timeline: list[MinuteEvent]
    goals: list[GoalEvent]
    score: dict
    result: str
    ball_status_counts: dict[str, int]


def normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return "".join(ch for ch in stripped.lower() if ch.isalnum() or ch in {" ", "-", "_"}).strip()


def stable_int(value: str) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def rotate_left(value: int, bits: int, width: int = 64) -> int:
    mask = (1 << width) - 1
    bits %= width
    return ((value << bits) & mask) | (value >> (width - bits))


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def weighted_choice(rng: random.Random, choices: Sequence[tuple[str, float]]) -> str:
    total = 0.0
    positive: list[tuple[str, float]] = []
    for label, weight in choices:
        w = max(0.0, float(weight))
        if w > 0:
            positive.append((label, w))
            total += w
    if not positive:
        return choices[0][0]

    needle = rng.random() * total
    cumulative = 0.0
    for label, weight in positive:
        cumulative += weight
        if needle <= cumulative:
            return label
    return positive[-1][0]


def minute_label(minute: int) -> str:
    if minute <= 90:
        return str(minute)
    return f"90+{minute - 90}"


def scorer_label(team: TeamInput, goal_index: int) -> str:
    if team.players:
        return team.players[goal_index % len(team.players)]
    return chr(ord("a") + (goal_index % 26))


def parse_players(values: list[str] | None) -> list[str]:
    if not values:
        return []
    players: list[str] = []
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                players.append(item)
    return players


def name_variants(value: str | None) -> set[str]:
    normalized = normalize_text(value)
    if not normalized:
        return set()

    variants = {normalized}
    for suffix in (" xi", " team", " national team", " national", " fc", " club"):
        if normalized.endswith(suffix):
            variants.add(normalized[: -len(suffix)].strip())
    return {variant for variant in variants if variant}


def load_rankings(path: Path | None) -> dict[str, float]:
    if path is None or not path.exists():
        return {}

    ranking_lookup: dict[str, float] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            elo_raw = (row.get("elo") or row.get("points") or "").strip()
            if not elo_raw:
                continue
            try:
                elo = float(elo_raw.replace(",", ""))
            except ValueError:
                continue

            keys: set[str] = set()
            for field_name in ("team", "country", "name", "aliases"):
                raw_value = (row.get(field_name) or "").strip()
                if not raw_value:
                    continue
                for alias in raw_value.replace(";", "|").split("|"):
                    keys.update(name_variants(alias))

            for key in keys:
                ranking_lookup[key] = elo

    return ranking_lookup


def load_rosters(path: Path | None) -> dict[str, list[str]]:
    if path is None or not path.exists():
        return {}

    roster_lookup: dict[str, list[str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            players_raw = (row.get("players") or "").strip()
            if not players_raw:
                continue
            players = [item.strip() for item in players_raw.replace("|", ";").split(";") if item.strip()]
            if not players:
                continue

            keys: set[str] = set()
            for field_name in ("team", "country", "name", "aliases"):
                raw_value = (row.get(field_name) or "").strip()
                if not raw_value:
                    continue
                for alias in raw_value.replace(";", "|").split("|"):
                    keys.update(name_variants(alias))

            for key in keys:
                roster_lookup[key] = players

    return roster_lookup


def resolve_team_elo(team: TeamInput, ranking_lookup: dict[str, float], role: str) -> float:
    if team.elo is not None:
        return team.elo

    for candidate in name_variants(team.team_name) | name_variants(team.country_name):
        if candidate in ranking_lookup:
            return ranking_lookup[candidate]

    raise SystemExit(
        f"Unable to resolve {role} Elo for {team.label}. Provide --{role}-elo or add an entry to {DEFAULT_RANKINGS_CSV}."
    )


def resolve_team_players(team: TeamInput, roster_lookup: dict[str, list[str]]) -> list[str]:
    if team.players:
        return team.players

    for candidate in name_variants(team.team_name) | name_variants(team.country_name):
        if candidate in roster_lookup:
            return roster_lookup[candidate]

    return []


def resolve_team(team: TeamInput, ranking_lookup: dict[str, float], roster_lookup: dict[str, list[str]], role: str) -> TeamInput:
    return replace(
        team,
        elo=resolve_team_elo(team, ranking_lookup, role),
        players=resolve_team_players(team, roster_lookup),
    )


def build_weighted_seed(
    home: TeamInput,
    away: TeamInput,
    match_id: str | None,
    noise_seed: str | None,
) -> dict:
    payload = {
        "home": {
            "team_name": home.team_name,
            "country_name": home.country_name,
            "elo": home.elo,
        },
        "away": {
            "team_name": away.team_name,
            "country_name": away.country_name,
            "elo": away.elo,
        },
        "match_id": match_id or "",
        "noise_seed": noise_seed or "",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).digest()
    primary = int.from_bytes(digest[:8], "big", signed=False)
    secondary = int.from_bytes(digest[8:16], "big", signed=False)
    noise = stable_int(f"noise::{noise_seed or match_id or canonical}")
    elo_delta = int(round((home.elo - away.elo) * 1000))
    weighted_seed = primary ^ rotate_left(secondary, 13) ^ rotate_left(noise, 29) ^ abs(elo_delta)
    weighted_seed &= (1 << 64) - 1
    return {
        "canonical_input": payload,
        "canonical_hash": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "weighted_seed": weighted_seed,
        "weighted_seed_hex": f"{weighted_seed:016x}",
        "elo_delta": home.elo - away.elo,
    }


def derive_match_profile(home: TeamInput, away: TeamInput, noise_rng: random.Random) -> dict:
    elo_delta = home.elo - away.elo
    strength_edge = math.tanh(elo_delta / 360.0)
    total_xg = clamp(2.35 + noise_rng.uniform(-0.25, 0.35), 1.45, 4.85)
    home_share = clamp(0.5 + strength_edge * 0.22 + noise_rng.uniform(-0.05, 0.05), 0.18, 0.82)
    home_xg = clamp(total_xg * home_share + noise_rng.uniform(-0.08, 0.08), 0.20, 4.20)
    away_xg = clamp(total_xg - home_xg + noise_rng.uniform(-0.08, 0.08), 0.20, 4.20)
    if home_xg + away_xg < 1.0:
        home_xg += 0.35
        away_xg += 0.35
    tempo = clamp(0.95 + abs(elo_delta) / 1800.0 + noise_rng.uniform(-0.10, 0.10), 0.75, 1.45)
    return {
        "strength_edge": strength_edge,
        "total_xg": total_xg,
        "home_xg": home_xg,
        "away_xg": away_xg,
        "tempo": tempo,
    }


def compute_stoppage_minutes(
    rng: random.Random,
    noise_rng: random.Random,
    profile: dict,
    min_stoppage: int,
    max_stoppage: int,
) -> int:
    base = 2
    base += rng.randint(0, 3)
    if profile["total_xg"] >= 2.9:
        base += 1
    if abs(profile["strength_edge"]) < 0.15:
        base += 1
    if profile["tempo"] >= 1.2:
        base += 1
    base += 1 if noise_rng.random() < 0.25 else 0
    return int(clamp(base, min_stoppage, max_stoppage))


def goal_context(status: str, side: str, score_diff: int, minute: int) -> float:
    factor = 1.0
    if status == f"{side}_attack":
        factor += 0.18
    elif status == f"{side}_build":
        factor += 0.10
    elif status == f"{side}_possession":
        factor += 0.05
    elif status == f"{side}_set_piece":
        factor += 0.16
    elif status == "neutral":
        factor += 0.00
    else:
        factor -= 0.08

    if minute >= 75:
        factor += 0.08
    if abs(score_diff) <= 1 and minute >= 88:
        factor += 0.12
    if score_diff < 0 and side == "home":
        factor += min(0.18, abs(score_diff) * 0.05)
    if score_diff > 0 and side == "away":
        factor += min(0.18, abs(score_diff) * 0.05)

    return clamp(factor, 0.55, 1.60)


def simulate_match(
    home: TeamInput,
    away: TeamInput,
    match_id: str | None = None,
    noise_seed: str | None = None,
    min_stoppage: int = 2,
    max_stoppage: int = 8,
    ranking_lookup: dict[str, float] | None = None,
    roster_lookup: dict[str, list[str]] | None = None,
) -> SimulationResult:
    ranking_lookup = ranking_lookup or {}
    roster_lookup = roster_lookup or {}
    home = resolve_team(home, ranking_lookup, roster_lookup, "home")
    away = resolve_team(away, ranking_lookup, roster_lookup, "away")

    seed_info = build_weighted_seed(home, away, match_id, noise_seed)
    weighted_seed = seed_info["weighted_seed"]
    match_rng = random.Random(weighted_seed)
    noise_rng = random.Random(rotate_left(weighted_seed ^ stable_int("afc-noise"), 17))

    profile = derive_match_profile(home, away, noise_rng)
    stoppage_minutes = compute_stoppage_minutes(match_rng, noise_rng, profile, min_stoppage, max_stoppage)
    total_minutes = 90 + stoppage_minutes

    home_score = 0
    away_score = 0
    home_goal_index = 0
    away_goal_index = 0
    playstring_chars: list[str] = []
    timeline: list[MinuteEvent] = []
    goals: list[GoalEvent] = []
    ball_status_counts: dict[str, int] = {key: 0 for key in STATUS_CODES}

    for minute in range(1, total_minutes + 1):
        label = minute_label(minute)
        score_diff = home_score - away_score

        control_noise = noise_rng.uniform(-0.10, 0.10)
        comeback_bias = clamp(-score_diff * 0.035, -0.16, 0.16)
        if minute > 75:
            comeback_bias += (minute - 75) / 15.0 * 0.04

        home_control = clamp(
            0.5 + profile["strength_edge"] * 0.18 + comeback_bias + control_noise,
            0.18,
            0.82,
        )

        tempo = profile["tempo"]
        status = weighted_choice(
            match_rng,
            [
                ("home_possession", 18.0 + 20.0 * home_control),
                ("away_possession", 18.0 + 20.0 * (1.0 - home_control)),
                ("neutral", 10.0 + max(0.0, 4.0 - tempo)),
                ("home_build", 8.0 + 7.0 * home_control * tempo),
                ("away_build", 8.0 + 7.0 * (1.0 - home_control) * tempo),
                ("home_attack", 3.0 + 5.0 * home_control * (1.0 + (0.10 if minute > 70 else 0.0))),
                ("away_attack", 3.0 + 5.0 * (1.0 - home_control) * (1.0 + (0.10 if minute > 70 else 0.0))),
                ("home_set_piece", 1.5 + 1.5 * home_control),
                ("away_set_piece", 1.5 + 1.5 * (1.0 - home_control)),
            ],
        )

        # Convert the base phase into a goal on a separate hazard roll.
        home_goal_rate = (profile["home_xg"] / total_minutes) * goal_context(status, "home", score_diff, minute)
        away_goal_rate = (profile["away_xg"] / total_minutes) * goal_context(status, "away", score_diff, minute)
        combined_goal_rate = home_goal_rate + away_goal_rate
        goal_roll = match_rng.random()

        note: str | None = None
        if goal_roll < combined_goal_rate:
            if goal_roll < home_goal_rate:
                status = "home_goal"
                home_score += 1
                scorer = scorer_label(home, home_goal_index)
                home_goal_index += 1
                goals.append(GoalEvent(minute=minute, minute_label=label, team=home.label, scorer=scorer))
                note = f"goal: {home.label} scorer {scorer}"
            else:
                status = "away_goal"
                away_score += 1
                scorer = scorer_label(away, away_goal_index)
                away_goal_index += 1
                goals.append(GoalEvent(minute=minute, minute_label=label, team=away.label, scorer=scorer))
                note = f"goal: {away.label} scorer {scorer}"

        code = STATUS_CODES[status]
        ball_status_counts[status] = ball_status_counts.get(status, 0) + 1
        playstring_chars.append(code)
        timeline.append(
            MinuteEvent(
                minute=minute,
                minute_label=label,
                status=status,
                code=code,
                home_score=home_score,
                away_score=away_score,
                home_control=round(home_control, 3),
                note=note,
            )
        )

    if home_score > away_score:
        result = "home_win"
    elif away_score > home_score:
        result = "away_win"
    else:
        result = "draw"

    return SimulationResult(
        match_id=match_id,
        home=home,
        away=away,
        seed=seed_info,
        stoppage_minutes=stoppage_minutes,
        total_minutes=total_minutes,
        playstring="".join(playstring_chars),
        timeline=timeline,
        goals=goals,
        score={"home": home_score, "away": away_score},
        result=result,
        ball_status_counts=ball_status_counts,
    )


def result_to_dict(result: SimulationResult) -> dict:
    return {
        "match_id": result.match_id,
        "home": asdict(result.home),
        "away": asdict(result.away),
        "seed": result.seed,
        "stoppage_minutes": result.stoppage_minutes,
        "total_minutes": result.total_minutes,
        "playstring": result.playstring,
        "timeline": [asdict(entry) for entry in result.timeline],
        "goals": [asdict(goal) for goal in result.goals],
        "score": result.score,
        "result": result.result,
        "ball_status_counts": result.ball_status_counts,
    }


def format_text(result: SimulationResult) -> str:
    lines = []
    lines.append(f"Match: {result.home.label} vs {result.away.label}")
    if result.match_id:
        lines.append(f"Match ID: {result.match_id}")
    lines.append(f"Seed: {result.seed['weighted_seed_hex']} ({result.seed['weighted_seed']})")
    lines.append(f"Stoppage: {result.stoppage_minutes} minutes")
    lines.append(f"Result: {result.score['home']}-{result.score['away']} ({result.result})")
    if result.goals:
        lines.append("Goals:")
        for goal in result.goals:
            lines.append(f"  - {goal.minute_label} {goal.team}: {goal.scorer}")
    lines.append("Timeline:")
    for entry in result.timeline:
        suffix = f" | {entry.note}" if entry.note else ""
        lines.append(
            f"  - {entry.minute_label:>4}: {entry.code} {entry.status}"
            f" | {entry.home_score}-{entry.away_score} | control={entry.home_control:.3f}{suffix}"
        )
    lines.append(f"Playstring: {result.playstring}")
    return "\n".join(lines)


def load_fixture_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def team_from_row(prefix: str, row: dict[str, str]) -> TeamInput:
    team_name = row.get(f"{prefix}_team", "").strip() or row.get(f"{prefix}_country", "").strip()
    country_name = row.get(f"{prefix}_country", "").strip() or team_name
    elo_raw = row.get(f"{prefix}_elo", "").strip()
    players_raw = row.get(f"{prefix}_players", "")
    players = [item.strip() for item in players_raw.split(";") if item.strip()] if players_raw else []
    elo = float(elo_raw) if elo_raw else None
    return TeamInput(team_name=team_name, country_name=country_name, elo=elo, players=players)


def simulate_from_row(
    row: dict[str, str],
    ranking_lookup: dict[str, float],
    roster_lookup: dict[str, list[str]],
) -> SimulationResult:
    home = team_from_row("home", row)
    away = team_from_row("away", row)
    match_id = row.get("match_id", "").strip() or None
    noise_seed = row.get("noise_seed", "").strip() or None
    min_stoppage = int(row.get("min_stoppage", 2) or 2)
    max_stoppage = int(row.get("max_stoppage", 8) or 8)
    return simulate_match(
        home=home,
        away=away,
        match_id=match_id,
        noise_seed=noise_seed,
        min_stoppage=min_stoppage,
        max_stoppage=max_stoppage,
        ranking_lookup=ranking_lookup,
        roster_lookup=roster_lookup,
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic AFC match playstring and result.",
    )

    parser.add_argument("--fixture-csv", type=Path, help="Batch mode CSV with home_* and away_* columns.")
    parser.add_argument("--match-id", help="Optional fixture identifier used in the seed.")
    parser.add_argument("--noise-seed", help="Optional extra seed mixed into the noise layer.")
    parser.add_argument(
        "--rankings-csv",
        type=Path,
        default=DEFAULT_RANKINGS_CSV,
        help="CSV file used to resolve Elo ratings when they are omitted.",
    )
    parser.add_argument(
        "--rosters-csv",
        type=Path,
        default=DEFAULT_ROSTERS_CSV,
        help="CSV file used to resolve team player names when they are omitted.",
    )
    parser.add_argument("--home-team", help="Home team name. Defaults to the country name if omitted.")
    parser.add_argument("--home-country", help="Home country name.")
    parser.add_argument("--home-elo", type=float, help="Home team Elo.")
    parser.add_argument("--away-team", help="Away team name. Defaults to the country name if omitted.")
    parser.add_argument("--away-country", help="Away country name.")
    parser.add_argument("--away-elo", type=float, help="Away team Elo.")
    parser.add_argument(
        "--home-player",
        action="append",
        default=[],
        help="Optional home player name. Repeat the flag or provide comma-separated names.",
    )
    parser.add_argument(
        "--away-player",
        action="append",
        default=[],
        help="Optional away player name. Repeat the flag or provide comma-separated names.",
    )
    parser.add_argument("--min-stoppage", type=int, default=2, help="Minimum stoppage minutes.")
    parser.add_argument("--max-stoppage", type=int, default=8, help="Maximum stoppage minutes.")
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format for single-match mode.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output with indentation.",
    )

    return parser.parse_args(argv)


def require_single_match_args(args: argparse.Namespace) -> tuple[TeamInput, TeamInput]:
    missing = []
    for field_name in ("home_country", "away_country"):
        if getattr(args, field_name) is None:
            missing.append(field_name)
    if missing:
        raise SystemExit(f"Missing required arguments for single-match mode: {', '.join(missing)}")

    home = TeamInput(
        team_name=args.home_team or args.home_country,
        country_name=args.home_country,
        elo=args.home_elo,
        players=parse_players(args.home_player),
    )
    away = TeamInput(
        team_name=args.away_team or args.away_country,
        country_name=args.away_country,
        elo=args.away_elo,
        players=parse_players(args.away_player),
    )
    return home, away


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ranking_lookup = load_rankings(args.rankings_csv)
    roster_lookup = load_rosters(args.rosters_csv)

    if args.fixture_csv:
        rows = load_fixture_rows(args.fixture_csv)
        outputs = [result_to_dict(simulate_from_row(row, ranking_lookup, roster_lookup)) for row in rows]
        if args.format == "text":
            for index, output in enumerate(outputs, start=1):
                home = TeamInput(**output["home"])
                away = TeamInput(**output["away"])
                result = SimulationResult(
                    match_id=output["match_id"],
                    home=home,
                    away=away,
                    seed=output["seed"],
                    stoppage_minutes=output["stoppage_minutes"],
                    total_minutes=output["total_minutes"],
                    playstring=output["playstring"],
                    timeline=[MinuteEvent(**entry) for entry in output["timeline"]],
                    goals=[GoalEvent(**entry) for entry in output["goals"]],
                    score=output["score"],
                    result=output["result"],
                    ball_status_counts=output["ball_status_counts"],
                )
                if index > 1:
                    print("\n---\n")
                print(format_text(result))
            return 0

        indent = 2 if args.pretty else None
        print(json.dumps(outputs, indent=indent, ensure_ascii=False))
        return 0

    home, away = require_single_match_args(args)
    result = simulate_match(
        home=home,
        away=away,
        match_id=args.match_id,
        noise_seed=args.noise_seed,
        min_stoppage=args.min_stoppage,
        max_stoppage=args.max_stoppage,
        ranking_lookup=ranking_lookup,
        roster_lookup=roster_lookup,
    )

    if args.format == "text":
        print(format_text(result))
        return 0

    output = result_to_dict(result)
    indent = 2 if args.pretty else None
    print(json.dumps(output, indent=indent, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
