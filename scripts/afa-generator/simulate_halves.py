#!/usr/bin/env python3
"""Simulate a match in two halves with separate seeds."""

import sys
import random
import csv
from pathlib import Path

# Import from the main generator
sys.path.insert(0, str(Path(__file__).parent))
from generate_afc_match_playstring import (
    TeamInput, MinuteEvent, GoalEvent,
    build_weighted_seed, resolve_team, derive_match_profile, venue_advantage,
    minute_label, weighted_choice, clamp, goal_context, scorer_label,
    STATUS_CODES, DEFAULT_RANKINGS_CSV, DEFAULT_ROSTERS_CSV,
    stable_int, rotate_left, load_rosters, load_rankings,
)


def simulate_half(home, away, match_id, noise_seed, venue_country,
                  start_minute, end_minute, start_home_score, start_away_score,
                  profile, venue_home_bias, total_minutes):
    """Simulate a range of minutes and return events, goals, and final score."""
    seed_info = build_weighted_seed(home, away, match_id, noise_seed, venue_country)
    weighted_seed = seed_info["weighted_seed"]
    match_rng = random.Random(weighted_seed)
    noise_rng = random.Random(rotate_left(weighted_seed ^ stable_int("afc-noise"), 17))

    home_score = start_home_score
    away_score = start_away_score
    home_goal_index = 0
    away_goal_index = 0
    timeline = []
    goals = []
    ball_status_counts = {key: 0 for key in STATUS_CODES}
    playstring_chars = []

    for minute in range(start_minute, end_minute + 1):
        label = minute_label(minute)
        score_diff = home_score - away_score

        control_noise = noise_rng.uniform(-0.025, 0.025)
        comeback_bias = clamp(-score_diff * 0.018, -0.08, 0.08)
        if minute > 75:
            comeback_bias += (minute - 75) / 15.0 * 0.02

        home_control = clamp(
            0.5 + profile["strength_edge"] * 0.18 + venue_home_bias + comeback_bias + control_noise,
            0.18, 0.82
        )

        tempo = profile["tempo"]
        status = weighted_choice(match_rng, [
            ("home_possession", 18.0 + 20.0 * home_control),
            ("away_possession", 18.0 + 20.0 * (1.0 - home_control)),
            ("neutral", 10.0 + max(0.0, 4.0 - tempo)),
            ("home_build", 8.0 + 7.0 * home_control * tempo),
            ("away_build", 8.0 + 7.0 * (1.0 - home_control) * tempo),
            ("home_attack", 3.0 + 5.0 * home_control * (1.0 + (0.10 if minute > 70 else 0.0))),
            ("away_attack", 3.0 + 5.0 * (1.0 - home_control) * (1.0 + (0.10 if minute > 70 else 0.0))),
            ("home_set_piece", 1.5 + 1.5 * home_control),
            ("away_set_piece", 1.5 + 1.5 * (1.0 - home_control)),
        ])

        # Goal hazard roll (this was missing!)
        home_goal_rate = (profile["home_xg"] / total_minutes) * goal_context(status, "home", score_diff, minute)
        away_goal_rate = (profile["away_xg"] / total_minutes) * goal_context(status, "away", score_diff, minute)
        combined_goal_rate = home_goal_rate + away_goal_rate
        goal_roll = match_rng.random()

        note = None
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
        timeline.append(MinuteEvent(
            minute=minute, minute_label=label, status=status, code=code,
            home_score=home_score, away_score=away_score,
            home_control=round(home_control, 3), note=note
        ))

    return {
        "timeline": timeline,
        "goals": goals,
        "home_score": home_score,
        "away_score": away_score,
        "ball_status_counts": ball_status_counts,
        "playstring": "".join(playstring_chars),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simulate a match in two halves")
    parser.add_argument("--home-team", required=True)
    parser.add_argument("--home-country", required=True)
    parser.add_argument("--home-elo", type=float, required=True)
    parser.add_argument("--away-team", required=True)
    parser.add_argument("--away-country", required=True)
    parser.add_argument("--away-elo", type=float, required=True)
    parser.add_argument("--venue-country", default="")
    parser.add_argument("--match-id", required=True)
    parser.add_argument("--first-half-seed", default="first-half")
    parser.add_argument("--second-half-seed", default="second-half")
    parser.add_argument("--stoppage", type=int, default=4)
    args = parser.parse_args()

    # Load rosters and rankings
    roster_lookup = load_rosters(DEFAULT_ROSTERS_CSV)
    ranking_lookup = load_rankings(DEFAULT_RANKINGS_CSV)

    home = TeamInput(team_name=args.home_team, country_name=args.home_country, elo=args.home_elo,
                     players=roster_lookup.get(args.home_country, []))
    away = TeamInput(team_name=args.away_team, country_name=args.away_country, elo=args.away_elo,
                     players=roster_lookup.get(args.away_country, []))

    home = resolve_team(home, ranking_lookup, roster_lookup, "home")
    away = resolve_team(away, ranking_lookup, roster_lookup, "away")

    total_minutes = 90 + args.stoppage

    # Derive match profile once (shared)
    seed_info = build_weighted_seed(home, away, args.match_id, args.first_half_seed, args.venue_country)
    profile_rng = random.Random(seed_info["weighted_seed"])
    profile = derive_match_profile(home, away, profile_rng)
    venue_home_bias = venue_advantage(home, away, args.venue_country)

    # First half: minutes 1-45
    first_half = simulate_half(
        home, away, args.match_id, args.first_half_seed, args.venue_country,
        start_minute=1, end_minute=45,
        start_home_score=0, start_away_score=0,
        profile=profile, venue_home_bias=venue_home_bias, total_minutes=total_minutes
    )

    print("=== FIRST HALF ===")
    print(f"Score at half-time: {first_half['home_score']}-{first_half['away_score']}")
    for g in first_half["goals"]:
        print(f"  {g.minute}' {g.team}: {g.scorer}")
    for ev in first_half["timeline"]:
        if ev.note:
            print(f"  {ev.minute_label}: {ev.code} {ev.note}")
        else:
            print(f"  {ev.minute_label}: {ev.code} {ev.status} | {ev.home_score}-{ev.away_score} | control={ev.home_control:.3f}")

    # Second half: minutes 46-90+stoppage
    second_half = simulate_half(
        home, away, args.match_id, args.second_half_seed, args.venue_country,
        start_minute=46, end_minute=90 + args.stoppage,
        start_home_score=first_half["home_score"], start_away_score=first_half["away_score"],
        profile=profile, venue_home_bias=venue_home_bias, total_minutes=total_minutes
    )

    print("\n=== SECOND HALF ===")
    print(f"Full-time score: {second_half['home_score']}-{second_half['away_score']}")
    for g in second_half["goals"]:
        print(f"  {g.minute}' {g.team}: {g.scorer}")
    for ev in second_half["timeline"]:
        if ev.note:
            print(f"  {ev.minute_label}: {ev.code} {ev.note}")
        else:
            print(f"  {ev.minute_label}: {ev.code} {ev.status} | {ev.home_score}-{ev.away_score} | control={ev.home_control:.3f}")

    # Combined result
    all_goals = first_half["goals"] + second_half["goals"]
    print(f"\n=== FULL MATCH ===")
    print(f"Result: {second_half['home_score']}-{second_half['away_score']}")
    print("Goals:")
    for g in all_goals:
        print(f"  {g.minute}' {g.team}: {g.scorer}")


if __name__ == "__main__":
    main()
