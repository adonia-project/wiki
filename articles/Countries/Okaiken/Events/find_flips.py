import re

def parse_diet_full(filepath):
    """Parse a Diet file and return ALL members with position index."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    members = []
    idx = 0
    for line in content.split('\n'):
        line = line.strip()
        m = re.match(r'\|\s*\[\[([^\]]+)\]\]\s*(?:<!-- [MF] -->)?\s*\|\|\s*([^|]+?)\s*\|\|\s*style="background:([^"]+);"\s*\|\s*\|\|\s*(\w+)\s*\|\|\s*(\d+)', line)
        if m:
            name = m.group(1)
            constituency = m.group(2).strip()
            party = m.group(4)
            members.append((idx, constituency, party, name))
            idx += 1
    
    return members

diet_60 = parse_diet_full(r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Events\60th Diet Members.mediawiki")
diet_61 = parse_diet_full(r"B:\02_GIT CONNECTED\wiki\articles\Countries\Okaiken\Events\61st Diet Members.mediawiki")

print(f"60th Diet: {len(diet_60)} members")
print(f"61st Diet: {len(diet_61)} members")

# Match by position index (same seat)
flips = []
held = []
for i in range(min(len(diet_60), len(diet_61))):
    idx60, c60, p60, n60 = diet_60[i]
    idx61, c61, p61, n61 = diet_61[i]
    if c60 == c61:  # Same constituency
        if p60 != p61:
            flips.append((c60, p60, n60, p61, n61))
        else:
            held.append((c60, p60, n60, n61))

print(f"\nSame constituency, same party (held): {len(held)}")
print(f"Same constituency, different party (flipped): {len(flips)}")

# Summary by flip type
from collections import Counter
flip_paths = Counter()
for c, p60, n60, p61, n61 in flips:
    flip_paths[f"{p60} -> {p61}"] += 1

print("\n=== FLIP SUMMARY ===")
for path, count in sorted(flip_paths.items(), key=lambda x: -x[1]):
    print(f"  {path}: {count}")

# Separate SMD and PR flips
smd_flips = [(c, p60, n60, p61, n61) for c, p60, n60, p61, n61 in flips if 'PR' not in c]
pr_flips = [(c, p60, n60, p61, n61) for c, p60, n60, p61, n61 in flips if 'PR' in c]

print(f"\nSMD flips: {len(smd_flips)}")
print(f"PR flips: {len(pr_flips)}")

print("\n=== ALL SMD FLIPS (for map update) ===")
for c, p60, n60, p61, n61 in sorted(smd_flips, key=lambda x: x[0]):
    print(f"  {c}: {p60} -> {p61}  ({n60} lost to {n61})")

print("\n=== ALL PR FLIPS ===")
for c, p60, n60, p61, n61 in sorted(pr_flips, key=lambda x: x[0]):
    print(f"  {c}: {p60} -> {p61}  ({n60} lost to {n61})")

# Count held by party
held_by_party = Counter()
for c, p, n60, n61 in held:
    held_by_party[p] += 1

print("\n=== SEATS HELD BY SAME PARTY ===")
for p, count in sorted(held_by_party.items(), key=lambda x: -x[1]):
    print(f"  {p}: {count} seats held")
