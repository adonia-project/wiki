#!/usr/bin/env python3
"""
International Dollar (XID) — US Dollar (USD) Exchange Rate Model
================================================================
Models the ID/USD exchange rate based on the energy standard.

The International Dollar was introduced in 1948 at 0.888671g fine gold (= $1 USD,
Bretton Woods parity). In 1952, the ID switched to an energy standard where
1 ID = one-third the cost to generate 11.11 kWh of electricity at 1952 prices.

The ID has NEVER been a floating currency — it remains on the energy standard.
The exchange rate moves because the USD (fiat since 1971) inflates and depreciates
over time, while the ID's value remains anchored to the energy standard.

The exchange rate = BASE_RATE × (USD cumulative inflation) / (ID cumulative inflation).

ID inflation reflects actual Adonia economic history, NOT Earth events.
The only equivalent event between Adonia and Earth is COVID-19 (2020).

Usage:
    python id_usd_tracker.py --historical     # Print historical annual rates
    python id_usd_tracker.py --spot            # Generate today's spot rate
    python id_usd_tracker.py --spot --seed 42 # Generate spot with specific seed
    python id_usd_tracker.py --wiki            # Generate wiki table markup
"""

import argparse
import json
import hashlib
import math
from datetime import date, datetime

# =============================================================================
# US CPI Data (BLS CPI-U, All Items, base 1982-84=100)
# Source: US Bureau of Labor Statistics (historical), estimated for 2024-2026
# This is EARTH context — real-world data.
# =============================================================================
US_CPI = {
    1948: 24.1, 1949: 23.8, 1950: 24.1, 1951: 26.0, 1952: 26.5,
    1953: 26.7, 1954: 26.9, 1955: 26.8, 1956: 27.2, 1957: 28.1,
    1958: 28.9, 1959: 29.1, 1960: 29.6, 1961: 29.9, 1962: 30.2,
    1963: 30.6, 1964: 31.0, 1965: 31.5, 1966: 32.4, 1967: 33.4,
    1968: 34.8, 1969: 36.7, 1970: 38.8, 1971: 40.5, 1972: 41.8,
    1973: 44.4, 1974: 49.3, 1975: 53.8, 1976: 56.9, 1977: 60.6,
    1978: 65.2, 1979: 72.6, 1980: 82.4, 1981: 90.9, 1982: 96.5,
    1983: 99.6, 1984: 103.9, 1985: 107.6, 1986: 109.6, 1987: 113.5,
    1988: 118.3, 1989: 124.0, 1990: 130.7, 1991: 136.2, 1992: 140.3,
    1993: 144.5, 1994: 148.2, 1995: 152.4, 1996: 156.9, 1997: 160.5,
    1998: 163.0, 1999: 166.6, 2000: 172.2, 2001: 177.1, 2002: 179.9,
    2003: 184.0, 2004: 188.9, 2005: 195.3, 2006: 201.6, 2007: 207.342,
    2008: 215.303, 2009: 214.537, 2010: 218.056, 2011: 224.939,
    2012: 229.594, 2013: 232.957, 2014: 236.736, 2015: 237.017,
    2016: 240.007, 2017: 245.120, 2018: 251.107, 2019: 255.657,
    2020: 258.811, 2021: 270.970, 2022: 292.655, 2023: 304.702,
    2024: 314.0, 2025: 322.0, 2026: 330.0,  # 2024-2026 estimated
}

# =============================================================================
# ID Inflation Model — ADONIA context
# The energy standard constrains money creation to energy production growth.
# These rates reflect ACTUAL Adonia economic history, NOT Earth events.
# The only equivalent event between Adonia and Earth is COVID-19 (2020).
# =============================================================================
ID_INFLATION = {
    # 1948-1952: Gold peg; Adonian Depression; Stock Crash of 1949
    1948: 0.0, 1949: 0.0, 1950: 0.0, 1951: 0.0, 1952: 0.0,
    # 1953-1965: Energy standard; post-war boom; Sanese Industrial Miracle; Great Economic Boom
    1953: 0.5, 1954: 0.5, 1955: 0.5, 1956: 0.5, 1957: 0.5,
    1958: 0.5, 1959: 0.5, 1960: 0.6, 1961: 0.6, 1962: 0.6,
    1963: 0.6, 1964: 0.6, 1965: 0.7,
    # 1966-1967: Kwangju partition disrupts trade; Okami Stock Exchange crash ("Black Monday")
    1966: 1.0, 1967: 1.5,
    # 1968-1971: Balboa recession (mandate integration); Breislandic shock (1971)
    1968: 1.0, 1969: 1.0, 1970: 1.0, 1971: 1.2,
    # 1972-1975: ID stable on energy standard; Treaty of Areza (1973)
    1972: 1.0, 1973: 1.0, 1974: 1.0, 1975: 1.0,
    # 1976-1979: Camboriú War; Marañón oil fires; Potocsí Decade Recession; Balisca Special Period
    #   Oil shortages cause energy prices to spike across Adonia
    1976: 1.5, 1977: 2.0, 1978: 2.0, 1979: 2.0,
    # 1980-1983: Energy crisis continues; Balisca Special Period most severe; Go-go 8090 boom begins
    1980: 2.0, 1981: 1.8, 1982: 1.8, 1983: 1.5,
    # 1984-1985: Energy prices normalise; Go-go 8090 boom accelerates
    1984: 1.5, 1985: 1.5,
    # 1986-1990: Peak of Go-go 8090 bubble; Balboa real-estate bubble inflating
    1986: 1.8, 1987: 1.8, 1988: 1.8, 1989: 1.8, 1990: 1.8,
    # 1991-1996: Global recession — Okaiken bubble bursts (1991) + Balisca Special Period;
    #   two of the largest economies contracting, downstream effects across Adonia
    1991: 0.5, 1992: 0.3, 1993: 0.3, 1994: 0.5, 1995: 0.5, 1996: 0.5,
    # 1997-2007: Recovery and moderate growth; Lost Decades linger in Okaiken
    1997: 1.0, 1998: 1.0, 1999: 1.0, 2000: 1.0,
    2001: 1.0, 2002: 1.0, 2003: 1.0, 2004: 1.0, 2005: 1.0,
    2006: 1.0, 2007: 1.0,
    # 2008: Financial shock averted in Okaiken through technocratic pivot (NOT a global crisis)
    2008: 1.0,
    # 2009-2019: Stable growth; Jutsu Restoration in Okaiken
    2009: 1.2, 2010: 1.2, 2011: 1.2, 2012: 1.2, 2013: 1.2,
    2014: 1.2, 2015: 1.2, 2016: 1.2, 2017: 1.2, 2018: 1.2, 2019: 1.2,
    # 2020: COVID-19 pandemic (the only equivalent event between Adonia and Earth)
    2020: 0.5,
    # 2021: Recovery
    2021: 1.5,
    # 2022-2023: Post-COVID inflation (confirmed in Burawa articles)
    2022: 2.5, 2023: 2.5,
    # 2024-2026: Normalisation
    2024: 1.8, 2025: 1.8, 2026: 1.8,
}

# =============================================================================
# Historical events — separate Adonia and Earth context
# =============================================================================
HISTORICAL_EVENTS = {
    1948: {
        "adonia": "ID introduced (gold peg); Adonian Depression; Stock Crash of 1949",
        "earth": "[[W:Bretton Woods system|Bretton Woods]] system in effect",
    },
    1952: {
        "adonia": "Energy standard adopted; Keil-Hermann system established",
        "earth": "USD still gold-backed at $35/oz",
    },
    1967: {
        "adonia": "Kwangju partition; Okami Stock Exchange crash (\"Black Monday\")",
        "earth": "",
    },
    1971: {
        "adonia": "Breislandic shock — Breisland terminates krone-gold convertibility; ID remains on energy standard",
        "earth": "[[W:Nixon shock|Nixon shock]] — USD abandons gold convertibility",
    },
    1973: {
        "adonia": "Treaty of Areza (Balboa Canal returned); ID remains on energy standard",
        "earth": "Bretton Woods fully collapses; USD becomes fiat",
    },
    1976: {
        "adonia": "Camboriú War; Marañón oil fires; energy prices spike",
        "earth": "",
    },
    1977: {
        "adonia": "Potocsí Decade Recession begins; Balisca Special Period; oil shortages",
        "earth": "",
    },
    1980: {
        "adonia": "Balisca Special Period most severe; energy crisis continues",
        "earth": "",
    },
    1990: {
        "adonia": "OSE 225 peaks at 39,000 (Go-go 8090 bubble height)",
        "earth": "",
    },
    1991: {
        "adonia": "Okaiken bubble bursts; Balisca Special Period; global recession begins",
        "earth": "",
    },
    1994: {
        "adonia": "Global recession continues; Balboa spot recession",
        "earth": "",
    },
    2008: {
        "adonia": "Financial shock averted in Okaiken through technocratic pivot",
        "earth": "[[W:2008 financial crisis|Global financial crisis]]",
    },
    2020: {
        "adonia": "[[W:COVID-19 pandemic|COVID-19 pandemic]]",
        "earth": "[[W:COVID-19 pandemic|COVID-19 pandemic]]; massive US monetary expansion",
    },
    2022: {
        "adonia": "Post-COVID inflation in Adonia",
        "earth": "[[W:2021–2023 inflation surge|US inflation surge]]; Fed tightening cycle",
    },
}

# Base year for the energy standard
# In 1952, the ID was set on the energy standard. The base rate is calibrated so
# that 1 ID = $1.00 USD in 2015 (the year the ID and USD reached parity).
# 1 ID = $0.2187 USD in 1952, or equivalently ~4.57 ID = $1.00 USD in 1952.
BASE_YEAR = 1952
BASE_RATE = 0.218651  # Calibrated: 1 ID = $1.00 USD in 2015


def compute_cumulative_id_inflation():
    """Compute cumulative ID inflation factor from 1952 to each year."""
    cumulative = {BASE_YEAR: 1.0}
    for year in range(BASE_YEAR + 1, 2027):
        rate = ID_INFLATION.get(year, 1.2) / 100.0
        cumulative[year] = cumulative[year - 1] * (1 + rate)
    return cumulative


def compute_cumulative_usd_inflation():
    """Compute cumulative USD inflation factor from 1952 to each year using CPI."""
    base_cpi = US_CPI[BASE_YEAR]
    cumulative = {BASE_YEAR: 1.0}
    for year in range(BASE_YEAR + 1, 2027):
        if year in US_CPI:
            cumulative[year] = US_CPI[year] / base_cpi
        else:
            # Interpolate from last known
            last = max(y for y in US_CPI if y < year)
            cumulative[year] = US_CPI[last] / base_cpi
    return cumulative


def compute_exchange_rates():
    """
    Compute the ID/USD exchange rate for each year.

    Rate = BASE_RATE × (USD cumulative inflation) / (ID cumulative inflation)

    The ID remains on the energy standard; the USD is fiat.
    The rate moves because the USD inflates, not because the ID floats.
    """
    usd_infl = compute_cumulative_usd_inflation()
    id_infl = compute_cumulative_id_inflation()

    rates = {}
    for year in range(1948, 2027):
        if year < BASE_YEAR:
            # Gold peg period: 3 ID = $1 USD
            rates[year] = BASE_RATE
        else:
            rates[year] = BASE_RATE * (usd_infl[year] / id_infl[year])

    return rates


def generate_spot_rate(seed_date=None, base_rate=None):
    """
    Generate a daily spot rate by applying simulated daily noise to the
    current annual rate. Uses a deterministic seed based on the date.
    """
    if seed_date is None:
        seed_date = date.today()

    if base_rate is None:
        rates = compute_exchange_rates()
        base_rate = rates[2026]

    # Deterministic seed from date
    seed_str = seed_date.isoformat()
    seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    seed = seed_hash % (2**31)

    # Simple LCG random number generator
    def lcg():
        nonlocal seed
        seed = (1103515245 * seed + 12345) & 0x7fffffff
        return seed / 0x7fffffff

    # Daily noise: ±0.5% with slight mean reversion
    noise = (lcg() - 0.5) * 0.01  # ±0.5%

    # Apply noise
    spot_rate = base_rate * (1 + noise)

    return round(spot_rate, 4)


def generate_historical_table():
    """Generate a table of historical ID/USD rates."""
    rates = compute_exchange_rates()
    usd_infl = compute_cumulative_usd_inflation()
    id_infl = compute_cumulative_id_inflation()

    rows = []
    for year in range(1948, 2027):
        rate = rates[year]
        usd_factor = usd_infl.get(year, 1.0)
        id_factor = id_infl.get(year, 1.0)
        event = HISTORICAL_EVENTS.get(year, {"adonia": "", "earth": ""})

        rows.append({
            "year": year,
            "rate": round(rate, 4),
            "usd_infl_factor": round(usd_factor, 2),
            "id_infl_factor": round(id_factor, 4),
            "id_inflation_pct": ID_INFLATION.get(year, 0.0),
            "adonia_context": event.get("adonia", ""),
            "earth_context": event.get("earth", ""),
        })

    return rows


def generate_wiki_markup():
    """Generate wiki table markup for the historical rates."""
    rows = generate_historical_table()

    lines = []
    lines.append("{| class='wikitable sortable'")
    lines.append("! Year !! 1 ID = USD !! 1 USD = ID !! USD cum. infl. !! ID cum. infl. !! Adonia context !! Earth context")
    lines.append("|-")

    for row in rows:
        lines.append(
            f"| {row['year']} "
            f"|| ${row['rate']:.4f} "
            f"|| {1/row['rate']:.4f} ID "
            f"|| {row['usd_infl_factor']:.2f}x "
            f"|| {row['id_infl_factor']:.4f}x "
            f"|| {row['adonia_context']} "
            f"|| {row['earth_context']}"
        )
        lines.append("|-")

    lines.append("|}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="ID/USD Exchange Rate Model")
    parser.add_argument("--historical", action="store_true",
                        help="Print historical annual rates")
    parser.add_argument("--spot", action="store_true",
                        help="Generate today's spot rate")
    parser.add_argument("--seed", type=int, default=None,
                        help="Specific seed for spot rate (default: date-based)")
    parser.add_argument("--wiki", action="store_true",
                        help="Generate wiki table markup")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    args = parser.parse_args()

    if args.historical:
        rows = generate_historical_table()
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print(f"{'Year':<6} {'1 ID = USD':>10} {'USD infl':>10} {'ID infl':>10} {'ID %':>6}  Adonia context")
            print("-" * 100)
            for row in rows:
                print(f"{row['year']:<6} ${row['rate']:>9.4f} {row['usd_infl_factor']:>9.2f}x {row['id_infl_factor']:>9.4f}x {row['id_inflation_pct']:>5.1f}%  {row['adonia_context']}")

    elif args.spot:
        if args.seed is not None:
            # Use provided seed
            rates = compute_exchange_rates()
            base = rates[2026]
            # Use seed directly
            seed = args.seed
            noise = ((seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff
            noise = (noise - 0.5) * 0.01
            spot = round(base * (1 + noise), 4)
        else:
            spot = generate_spot_rate()

        today = date.today().isoformat()
        rates = compute_exchange_rates()
        annual = rates[2026]

        if args.json:
            print(json.dumps({
                "date": today,
                "spot_rate": spot,
                "annual_rate": round(annual, 4),
                "rate_usd_per_id": spot,
                "rate_id_per_usd": round(1/spot, 4),
            }, indent=2))
        else:
            print(f"Date: {today}")
            print(f"Spot rate: 1 ID = ${spot:.4f} USD")
            print(f"Inverse:   1 USD = {1/spot:.4f} ID")
            print(f"Annual baseline (2026): 1 ID = ${annual:.4f} USD")
            print(f"Daily deviation: {((spot/annual)-1)*100:+.2f}%")

    elif args.wiki:
        print(generate_wiki_markup())

    else:
        # Default: print current rate
        rates = compute_exchange_rates()
        current = rates[2026]
        print(f"International Dollar / US Dollar Exchange Rate Model")
        print(f"===================================================")
        print(f"Base year: {BASE_YEAR} (1 ID = ${BASE_RATE:.4f} USD)")
        print(f"Current (2026): 1 ID = ${current:.4f} USD")
        print(f"                1 USD = {1/current:.4f} ID")
        print()
        print(f"Model: Energy standard (1 ID = 11.11 kWh at 1952 prices)")
        print(f"ID remains on energy standard; USD is fiat since 1971")
        print(f"USD cumulative inflation since 1952: {compute_cumulative_usd_inflation()[2026]:.2f}x")
        print(f"ID cumulative inflation since 1952:  {compute_cumulative_id_inflation()[2026]:.4f}x")
        print(f"Ratio: {compute_cumulative_usd_inflation()[2026] / compute_cumulative_id_inflation()[2026]:.4f}")


if __name__ == "__main__":
    main()
