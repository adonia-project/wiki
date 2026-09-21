#!/usr/bin/env python3
"""Build data/adonia_people.csv — a registry of named individuals across Adonia,
to prevent duplicate names unless deliberately reused.

Scans articles/ for infoboxes describing individuals and extracts name, nation,
role and dates. Rerun after adding people; it is idempotent and merges with
existing rows rather than overwriting hand-edits.
"""
import csv, re, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "articles"
OUT = ROOT / "data" / "adonia_people.csv"

# note: the regex captures what follows "Infobox ", so compare bare names here
INDIVIDUAL_BOXES = (
    "officeholder", "person", "royalty", "monarch",
    "military person", "scientist", "writer", "religious biography",
    "philosopher", "artist", "athlete", "engineer", "economist",
)
SKIP_BOXES = ("ethnic group", "country", "settlement", "former country")

FIELDS = ["name", "nation", "era", "role", "dob", "dod", "description", "source"]


def nation_of(path: Path) -> str:
    parts = path.parts
    if "Countries" in parts:
        i = parts.index("Countries")
        if i + 1 < len(parts):
            return parts[i + 1]
    if "Former_Countries" in parts:
        i = parts.index("Former_Countries")
        if i + 1 < len(parts):
            return parts[i + 1].replace("_", " ")
    return ""


def parse_infobox(text: str):
    m = re.search(r"^\{\{Infobox ([A-Za-z ]+)", text, re.M)
    if not m:
        return None
    box = m.group(1).strip()
    if box.lower() in SKIP_BOXES:
        return None
    if box not in INDIVIDUAL_BOXES:
        return None
    # collect top-level | key = value lines up to the closing }}
    body = text[m.start():]
    props = {}
    for line in body.split("\n")[1:]:
        if line.startswith("}}"):
            break
        km = re.match(r"\|\s*([A-Za-z_0-9 ]+?)\s*=\s*(.*)$", line)
        if km:
            k, v = km.group(1).strip(), km.group(2).strip()
            if k not in props:
                props[k] = v
    return props


def clean(v: str) -> str:
    if not v:
        return ""
    v = re.sub(r"<ref.*?</ref>", "", v, flags=re.S)
    v = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", v)
    v = re.sub(r"\[\[([^\]]+)\]\]", r"\1", v)
    v = re.sub(r"\{\{[^}]*\}\}", "", v)
    v = v.replace("'''", "").replace("''", "")
    return v.strip()


def year(v: str):
    m = re.search(r"(\d{3,4})", v or "")
    return m.group(1) if m else ""


def main():
    rows = {}
    for p in ART.rglob("*.mediawiki"):
        if "worktrees" in p.parts:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        props = parse_infobox(text)
        if not props:
            continue
        name = clean(props.get("name", "")) or p.stem
        rows[name] = {
            "name": name,
            "nation": nation_of(p),
            "era": clean(props.get("era", "")),
            "role": clean(props.get("office", "") or props.get("title", "") or props.get("occupation", "")),
            "dob": year(props.get("birth_date", "") or props.get("born", "")),
            "dod": year(props.get("death_date", "") or props.get("died", "")),
            "description": "",
            "source": str(p.relative_to(ROOT)),
        }

    # preserve hand-edits in an existing file
    if OUT.exists():
        with OUT.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                n = (r.get("name") or "").strip()
                if not n:
                    continue
                if n in rows:
                    for k in FIELDS:
                        if r.get(k) and not rows[n].get(k):
                            rows[n][k] = r[k]
                else:
                    rows[n] = {k: (r.get(k) or "") for k in FIELDS}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for n in sorted(rows, key=lambda s: s.lower()):
            w.writerow(rows[n])
    print("wrote %s with %d people" % (OUT.relative_to(ROOT), len(rows)))


if __name__ == "__main__":
    main()
