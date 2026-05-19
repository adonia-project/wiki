#!/usr/bin/env python3
"""Generate 61st Diet Members article based on 60th Diet template and 2026 election results.
Preserves original subsection order from the 60th Diet file."""

import re
import random

random.seed(2026)

TARGETS_61 = {"PPO": 63, "LDP": 110, "OSP": 100, "SCP": 115, "NKP": 32, "SDP": 36, "OIP": 18, "IND": 1}

BLOCKS_61 = {
    "Okami Block": {"total": 151, "smd": 92, "pr": 59, "PPO": 10, "LDP": 21, "OSP": 42, "SCP": 48, "NKP": 11, "SDP": 11, "OIP": 8},
    "Miseto Block": {"total": 99, "smd": 60, "pr": 39, "PPO": 6, "LDP": 15, "OSP": 25, "SCP": 28, "NKP": 10, "SDP": 9, "OIP": 6},
    "Asuka Block": {"total": 56, "smd": 34, "pr": 22, "PPO": 17, "LDP": 14, "OSP": 8, "SCP": 10, "NKP": 4, "SDP": 2, "OIP": 1},
    "Urakawa Block": {"total": 25, "smd": 15, "pr": 10, "PPO": 5, "LDP": 8, "OSP": 4, "SCP": 4, "NKP": 2, "SDP": 2},
    "Mutsu Block": {"total": 23, "smd": 14, "pr": 9, "PPO": 4, "LDP": 9, "OSP": 3, "SCP": 4, "NKP": 1, "SDP": 2},
    "Nishi-Yagikoshu Block": {"total": 23, "smd": 14, "pr": 9, "PPO": 4, "LDP": 7, "OSP": 4, "SCP": 5, "NKP": 1, "SDP": 1, "OIP": 1},
    "Nankai Block": {"total": 23, "smd": 14, "pr": 9, "PPO": 3, "LDP": 9, "OSP": 4, "SCP": 4, "NKP": 1, "SDP": 2},
    "Oku Block": {"total": 21, "smd": 13, "pr": 8, "PPO": 3, "LDP": 7, "OSP": 3, "SCP": 4, "NKP": 1, "SDP": 2, "OIP": 1},
    "Kihoku Block": {"total": 20, "smd": 12, "pr": 8, "PPO": 3, "LDP": 7, "OSP": 3, "SCP": 4, "NKP": 1, "SDP": 2},
    "Suzuka Block": {"total": 16, "smd": 10, "pr": 6, "PPO": 5, "LDP": 5, "OSP": 2, "SCP": 2, "SDP": 1, "OIP": 1},
    "Minami Harujima Block": {"total": 13, "smd": 8, "pr": 5, "PPO": 2, "LDP": 5, "OSP": 2, "SCP": 2, "SDP": 2},
    "Ogasawara Block": {"total": 5, "smd": 3, "pr": 2, "PPO": 1, "LDP": 3, "IND": 1},
}

# Verify totals
pt = {}
for block, dist in BLOCKS_61.items():
    bs = sum(v for k, v in dist.items() if k not in ("total", "smd", "pr"))
    assert bs == dist["total"], f"{block}: {bs} != {dist['total']}"
    for party, count in dist.items():
        if party not in ("total", "smd", "pr"):
            pt[party] = pt.get(party, 0) + count
for party, target in TARGETS_61.items():
    assert pt.get(party, 0) == target, f"{party}: {pt.get(party,0)} != {target}"
print("All block and party totals verified!")

# Name generation
FIRST_MALE = [
    "Akihiro", "Akira", "Atsushi", "Daiki", "Daisuke", "Eiji", "Fumiya", "Goro",
    "Hajime", "Haruki", "Haruto", "Hayato", "Hideo", "Hiroaki", "Hiroshi", "Hirotaka",
    "Isamu", "Jun", "Junichi", "Kaito", "Katsuya", "Kazuki", "Kazuya", "Ken",
    "Kenichi", "Kenji", "Kenta", "Kiyoshi", "Kohei", "Koji", "Kosuke", "Makoto",
    "Mamoru", "Masaki", "Masao", "Masashi", "Minoru", "Mitsuhiro", "Naoki", "Naoya",
    "Noboru", "Osamu", "Riku", "Ryota", "Ryohei", "Ryu", "Satoshi", "Shigeru",
    "Shin", "Shinichi", "Shinji", "Shoji", "Shohei", "Shota", "Soichiro", "Sora",
    "Sosuke", "Takashi", "Takuya", "Tatsuya", "Tetsuya", "Tomoya", "Toshiki",
    "Tsuyoshi", "Wataru", "Yasuhiro", "Yoshio", "Yosuke", "Yuki", "Yuta", "Yuto"
]
FIRST_FEMALE = [
    "Ai", "Akiko", "Aoi", "Asami", "Ayaka", "Ayumi", "Chiaki", "Eri",
    "Erika", "Haruka", "Hina", "Kaori", "Kana", "Keiko", "Mai", "Maki",
    "Manami", "Megumi", "Mika", "Miki", "Mio", "Miyuki", "Natsuki", "Rie",
    "Rina", "Rin", "Sachiko", "Sakura", "Sayuri", "Shiori", "Shizuka", "Tomoko",
    "Yoko", "Yuka", "Yuki", "Yumi", "Yuri"
]
LAST_NAMES = [
    "Abe", "Ando", "Aoki", "Aoyama", "Arai", "Chiba", "Doi", "Endo",
    "Fujii", "Fujimoto", "Fujita", "Fujiwara", "Fukuda", "Furukawa", "Goto", "Hara",
    "Harada", "Hashimoto", "Hasegawa", "Hayashi", "Hirano", "Honda", "Horie", "Ichikawa",
    "Igarashi", "Iida", "Iinuma", "Ikeda", "Imai", "Inoue", "Ishida", "Ishii",
    "Ishikawa", "Ito", "Iwamoto", "Iwasaki", "Kaneko", "Kato", "Katayama", "Kawamura",
    "Kikuchi", "Kimura", "Kinoshita", "Kishi", "Kobayashi", "Kojima", "Kondo", "Kubota",
    "Kudo", "Kumagai", "Kurosawa", "Maruyama", "Matsuda", "Matsui", "Matsumoto", "Matsuo",
    "Matsushita", "Minami", "Miura", "Miyamoto", "Miyazaki", "Mizuno", "Mori", "Morita",
    "Murakami", "Murata", "Nakagawa", "Nakajima", "Nakamura", "Nakano", "Nakata", "Nakayama",
    "Nishimura", "Noguchi", "Nomura", "Ogawa", "Okada", "Okamoto", "Ono", "Otsuka",
    "Saito", "Sakai", "Sakamoto", "Sano", "Sasaki", "Sato", "Shibata", "Shimizu",
    "Shinoda", "Sugimoto", "Sugiyama", "Suzuki", "Takahashi", "Takagi", "Takeda", "Takeuchi",
    "Tamura", "Tanaka", "Taniguchi", "Tateishi", "Tsuboi", "Uchida", "Ueda", "Ueno",
    "Wada", "Watanabe", "Yamada", "Yamaguchi", "Yamamoto", "Yamashita", "Yamazaki", "Yoshida",
    "Yoshikawa", "Yoshimura", "Yoshioka"
]

PARTY_COLORS = {
    "PPO": "#008e00", "LDP": "#b01717", "OSP": "#FF4719", "SCP": "#d40000",
    "NKP": "#E8BF19", "SDP": "#0029A3", "OIP": "{{Okaiken Innovation Party/meta/color}}", "IND": "#808080",
}
PARTY_NAMES = {
    "PPO": "[[Progressive Party of Okaiken|PPO]]",
    "LDP": "[[Liberal Democratic Party (Okaiken)|LDP]]",
    "OSP": "[[Okaiken Socialist Party|OSP]]",
    "SCP": "[[Sanese Communist Party|SCP]]",
    "NKP": "[[New Komeito Party|NKP]]",
    "SDP": "[[Social Democratic Party (Okaiken)|SDP]]",
    "OIP": "[[Okaiken Innovation Party|OIP]]",
    "IND": "Independent",
}


def parse_60th_diet(filepath):
    """Parse 60th Diet file preserving original order with position indices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = []
    current_block = None
    current_subsection = None
    members = []
    pos = 0  # Global position counter for ordering

    for line in content.split('\n'):
        line = line.strip()
        if 'background:#87CEEB' in line:
            m = re.search(r'\[\[([^\]]+ Block)\]\]', line)
            if m:
                if current_block and members:
                    blocks.append({"name": current_block, "members": members})
                current_block = m.group(1)
                members = []
                current_subsection = None
                continue
        if 'background:#E0FFFF' in line and 'Proportional Representation' in line:
            current_subsection = "PR"
            continue
        if 'colspan' in line and ('Prefecture' in line or 'Metropolis' in line):
            m = re.search(r'\[\[([^\]]+)\]\]', line)
            if m:
                current_subsection = m.group(1)
                continue
        m = re.match(r'\|\s*\[\[([^\]]+)\]\]\s*(?:<!-- [MF] -->)?\s*\|\|\s*([^|]+?)\s*\|\|\s*style="background:([^"]+);"\s*\|\s*\|\|\s*(\w+)\s*\|\|\s*(\d+)', line)
        if m:
            members.append({
                "name": m.group(1),
                "constituency": m.group(2).strip(),
                "party": m.group(4),
                "since": int(m.group(5)),
                "subsection": current_subsection,
                "block": current_block,
                "pos": pos,
            })
            pos += 1

    if current_block and members:
        blocks.append({"name": current_block, "members": members})

    return blocks


def generate_61st_diet(blocks_60th):
    """Generate 61st Diet preserving original seat order."""
    used_names = set()
    for block in blocks_60th:
        for member in block["members"]:
            used_names.add(member["name"])

    def gen_name():
        for _ in range(1000):
            last = random.choice(LAST_NAMES)
            first = random.choice(FIRST_FEMALE) if random.random() < 0.4 else random.choice(FIRST_MALE)
            name = f"{last} {first}"
            if name not in used_names:
                used_names.add(name)
                return name
        return "Unknown"

    output_blocks = []

    for block_60 in blocks_60th:
        block_name = block_60["name"]
        if block_name not in BLOCKS_61:
            continue

        block_61 = BLOCKS_61[block_name]
        members_60 = block_60["members"]

        # Group 60th Diet members by party, sorted by seniority (most senior first)
        by_party = {}
        for m in members_60:
            by_party.setdefault(m["party"], []).append(m)
        for p in by_party:
            by_party[p].sort(key=lambda x: x["since"])

        targets = {k: v for k, v in block_61.items() if k not in ("total", "smd", "pr")}

        # Determine which incumbents survive
        surviving = {}  # pos -> member dict
        removed = []  # list of (member, pos) for removed incumbents

        for party, target in targets.items():
            if party == "IND":
                continue
            incumbents = by_party.get(party, [])
            keep = min(len(incumbents), target)
            for i in range(keep):
                m = incumbents[i]
                surviving[m["pos"]] = {
                    "name": m["name"],
                    "constituency": m["constituency"],
                    "party": m["party"],
                    "since": m["since"],
                    "subsection": m["subsection"],
                    "block": block_name,
                    "pos": m["pos"],
                }
            for i in range(keep, len(incumbents)):
                m = incumbents[i]
                removed.append(m)

        # Sort removed members by position (original order)
        removed.sort(key=lambda x: x["pos"])

        # Determine new members needed per party
        new_needed = {}
        for party, target in targets.items():
            if party == "IND":
                new_needed[party] = target
                continue
            incumbents = by_party.get(party, [])
            keep = min(len(incumbents), target)
            new_needed[party] = target - keep

        # Assign new members to vacated seats in original order
        new_members = {}  # pos -> member dict
        seat_idx = 0

        for party, count in sorted(new_needed.items()):
            if count == 0:
                continue
            if party == "IND":
                name = gen_name()
                # Find the Ogasawara PR position
                # Create a new position at the end
                max_pos = max(m["pos"] for m in members_60) if members_60 else 0
                new_members[max_pos + 1] = {
                    "name": name,
                    "constituency": "Ogasawara PR",
                    "party": "IND",
                    "since": 2026,
                    "subsection": "PR",
                    "block": block_name,
                    "pos": max_pos + 1,
                }
                continue

            for i in range(count):
                name = gen_name()
                if seat_idx < len(removed):
                    # Take the next available seat
                    old_member = removed[seat_idx]
                    seat_idx += 1
                    new_members[old_member["pos"]] = {
                        "name": name,
                        "constituency": old_member["constituency"],
                        "party": party,
                        "since": 2026,
                        "subsection": old_member["subsection"],
                        "block": block_name,
                        "pos": old_member["pos"],
                    }
                else:
                    # No more available seats - this shouldn't happen if totals are correct
                    print(f"WARNING: No available seat for {party} in {block_name}")

        # Combine surviving and new members, sort by original position
        all_members_dict = {}
        all_members_dict.update(surviving)
        all_members_dict.update(new_members)

        all_members = sorted(all_members_dict.values(), key=lambda x: x["pos"])

        output_blocks.append({
            "name": block_name,
            "members": all_members,
            "smd": block_61["smd"],
            "pr": block_61["pr"],
            "total": block_61["total"],
        })

    return output_blocks


def generate_wikicode(blocks, output_path):
    lines = []
    lines.append("{{Short description|List of members of the House of Commoners of Okaiken}}")
    lines.append("{{Use mdy dates|date=May 2026}}")
    lines.append("{{Politics of Okaiken}}")
    lines.append("")
    lines.append("This is a list of members of the [[House of Commoners (Okaiken)|House of Commoners]] of Okaiken in the 61st Diet, elected in the [[Okaiken general election, 2026|2026 general election]].")
    lines.append("")
    lines.append("==Standings in the 61st Diet==")
    lines.append("")
    lines.append('{| class="wikitable" style="text-align:center;"')
    lines.append("|+ Standings in the 61st Diet")
    lines.append("|-")
    lines.append('! colspan="2" rowspan="2" | Affiliation !! colspan="3" | House of Commoners')
    lines.append("|-")
    lines.append("! 2026 election results !! Present !! +/&ndash;")

    standings = [
        ("SCP", 115, 45, "+70"),
        ("LDP", 110, 128, "&minus;18"),
        ("OSP", 100, 50, "+50"),
        ("PPO", 63, 181, "&minus;118"),
        ("SDP", 36, 25, "+11"),
        ("NKP", 32, 30, "+2"),
        ("OIP", 18, 16, "+2"),
        ("IND", 1, 0, "+1"),
    ]
    for party, current, prev, change in standings:
        color = PARTY_COLORS[party]
        pname = PARTY_NAMES[party]
        lines.append(f'| style="background:{color};" | || {pname} || {current} || {current} || {change}')

    lines.append("|-")
    lines.append('! colspan="2" | Total members !! 475 !! 475 !! 0')
    lines.append("|-")
    lines.append('| colspan="2" | Vacant || 0 || 0 || 0')
    lines.append("|-")
    lines.append('! colspan="2" | Total seats !! 475 !! colspan="2" | &mdash;')
    lines.append("|}")
    lines.append("")
    lines.append("==Members==")
    lines.append("")
    lines.append('{| class="wikitable sortable"')
    lines.append("|+ Members of the House of Commoners of the 61st Diet")
    lines.append("|-")
    lines.append('! Member !! Constituency !! colspan="2" | Party !! Party held electorally since')

    for block in blocks:
        block_name = block["name"]
        smd = block["smd"]
        pr = block["pr"]
        total = block["total"]

        lines.append("|-")
        lines.append(f'! colspan="5" style="background:#87CEEB;" | [[{block_name}]] ({smd} SMD + {pr} PR = {total} seats)')

        # Group members by subsection, preserving order
        current_sub = None
        for member in block["members"]:
            sub = member["subsection"]
            if sub != current_sub:
                current_sub = sub
                if sub == "PR":
                    lines.append("|-")
                    lines.append(f'! colspan="5" style="background:#E0FFFF;" | Proportional Representation ({pr} seats)')
                else:
                    sub_count = sum(1 for m in block["members"] if m["subsection"] == sub)
                    lines.append("|-")
                    lines.append(f'! colspan="5" | [[{sub}]] ({sub_count} SMD)')

            name = member["name"]
            constituency = member["constituency"]
            party = member["party"]
            color = PARTY_COLORS[party]
            since = member["since"]
            lines.append(f'| [[{name}]] || {constituency} || style="background:{color};" | || {party} || {since}')

    lines.append("|}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return len(lines)


if __name__ == "__main__":
    filepath_60th = r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Events\60th Diet Members.mediawiki"
    filepath_61st = r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Events\61st Diet Members.mediawiki"

    print("Parsing 60th Diet...")
    blocks_60th = parse_60th_diet(filepath_60th)
    print(f"Found {len(blocks_60th)} blocks, {sum(len(b['members']) for b in blocks_60th)} members")

    print("Generating 61st Diet...")
    blocks_61st = generate_61st_diet(blocks_60th)
    total_61 = sum(len(b['members']) for b in blocks_61st)
    print(f"Total 61st Diet members: {total_61}")

    party_totals = {}
    for block in blocks_61st:
        for m in block["members"]:
            party_totals[m["party"]] = party_totals.get(m["party"], 0) + 1
    print("61st Diet Party Totals:")
    for party in ["PPO", "LDP", "OSP", "SCP", "NKP", "SDP", "OIP", "IND"]:
        actual = party_totals.get(party, 0)
        target = TARGETS_61.get(party, 0)
        status = "OK" if actual == target else f"MISS (need {target})"
        print(f"  {party}: {actual} {status}")

    print("Generating wikicode...")
    line_count = generate_wikicode(blocks_61st, filepath_61st)
    print(f"Generated {line_count} lines")
