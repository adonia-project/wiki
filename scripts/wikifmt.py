#!/usr/bin/env python3
"""wikifmt - repair and validate mediawiki articles before pushing.

Usage:
    python scripts/wikifmt.py --fix articles/.../*.mediawiki    # repair in place
    python scripts/wikifmt.py --check articles/.../*.mediawiki  # report only
    python scripts/wikifmt.py --fix --check FILE                # both

Exits non-zero if any problem remains, so it can gate a `&&` chain.

Faults repaired, in the order they are handled:
  1. markdown bold      **x**        -> x
  2. markdown italics   *x*          -> ''x''
  3. mediawiki bold     '''x'''      -> x            (spares '''''x''''', the title form)
  4. heading articles   == The X ==  -> == X ==
  5. heading balance    === X ==     -> === X ===
  6. heading case       == x ==      -> == X ==
  7. markdown headings  ## X         -> == X ==
  8. trailing space, and a guaranteed final newline
"""
import re
import sys
from pathlib import Path

APOS = "'"
BOLD_MW = "(?<!%s)%s(?!%s)(.+?)(?<!%s)%s(?!%s)" % ((APOS,) + (APOS * 3,) * 5)
ITAL_MD = r"(?<!\*)\*([^\s*][^*]*?)\*(?!\*)"
# a markdown table separator row - piped runs of dashes. Mediawiki has no such
# construct, so any match is a markdown table written into a .mediawiki file.
MD_TABLE = r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"

# Editorialising: a wiki article reports what happened; it does not tell the
# reader what it means, why it matters, or what is really going on. These are
# the constructions that have crept into my own drafts. Reported, never auto-fixed.
EDITORIAL = [
    (r"\b[Ww]hich is why\b", "explains-rather-than-reports"),
    (r"\b[Tt]his is why\b", "explains-rather-than-reports"),
    (r"\b[Tt]hat is why\b", "explains-rather-than-reports"),
    (r"\b[Tt]his is the (reason|point|key|whole)\b", "explains-rather-than-reports"),
    (r"\b[Tt]he point is\b", "explains-rather-than-reports"),
    (r"\b[Tt]he whole point\b", "explains-rather-than-reports"),
    (r"\bis best understood as\b", "interpretation"),
    (r"\b[Tt]he real (reason|point|story|significance|question)\b", "interpretation"),
    (r"\b[Ww]hat matters (is|here)\b", "interpretation"),
    (r"\b[Tt]he significance (of|is)\b", "interpretation"),
    (r"\b[Tt]he importance (of|is)\b", "interpretation"),
    (r"\bnot merely\b", "rhetorical elevation"),
    (r"\bnot simply\b", "rhetorical elevation"),
    (r"\bwas itself\b", "rhetorical elevation"),
    (r"\b(matters|mattered) because\b", "explains-rather-than-reports"),
    (r"\b(reveals|reflects) (that|how) (the|a) (period|era|nature|character|fact|story)\b", "interpretation"),
    (r"\b(can|could) be seen as\b", "interpretation"),
    (r"\b(serves|served) to\b", "interpretation"),
    (r"\bin effect\b", "commentary"),
    (r"\bof course\b", "commentary"),
    (r"\b[tT]he tragedy\b", "commentary"),
    (r"\b(ironically|tellingly|revealingly|significantly|importantly|notably|crucially|interestingly)\s*,", "commentary adverb"),
    (r"\barguably\b", "qualification"),
    (r"\bit (is|should be) (worth|noted)\b", "commentary aside"),
    (r"\bthe moment when\b", "meta-narrative"),
    (r"\bmarked the moment\b", "meta-narrative"),
    (r"\bcame to (represent|symbolise|embody)\b", "interpretation"),
    (r"\bthe story of the\b", "meta-narrative"),
    # essayistic framing: opening with a negation, or announcing the point.
    # "is not written in shared characters" is a plain statement of fact; what
    # makes the construction essayistic is the "in one act" shape, so require it.
    (r"\b(was|were|is|are|did|does) not (devised|invented|written|made|created|built|begun|done) in (one|a single)\b", "essayistic negation"),
    (r"\bnot in one (act|step|year|move)\b", "essayistic negation"),
    (r"\bchanged the (problem|question|calculation)\b", "essayistic framing"),
    (r"\bwould not serve\b", "argumentative"),
    (r"\bwhat (they|he|she|it|the \w+) (produced|did|found) was\b", "essayistic framing"),
    (r"\bwhich is described below\b", "meta-narrative"),
    (r"\bas (described|set out|noted) (below|above)\b", "meta-narrative"),
    (r"\bit was they who\b", "rhetorical elevation"),
    (r"\bwhat the (scribes|records|evidence) (did|show)\b", "essayistic framing"),
    # --- telling rather than showing (WP:Writing better articles, the style trilemma)
    (r"\banswered (both|the) (questions|purposes)\b", "telling not showing"),
    (r"\bboth (questions|purposes) at once\b", "telling not showing"),
    (r"\bat (a single|one) stroke\b", "cleverness"),
    (r"\btwice over\b", "cleverness"),
    (r"\bnever before\b", "cleverness"),
    # "the only X that" is often a plain fact ("the only person who may open the year");
    # flag it only where it carries a value judgement
    (r"\bthe only \w+ (that|who) (can|could|would|has|had)\b", "cleverness"),
    (r"\bas (described|set out|noted|treated) (below|above)\b", "referential commentary"),
    (r"\bis (treated|discussed|described) (below|above)\b", "referential commentary"),
    # --- peacock terms: replace with the fact that makes them true
    (r"\b(most|more) (significant|important|notable|remarkable)\b", "peacock"),
    (r"\b(highly|most|very) (significant|important|notable|remarkable|influential)\b", "peacock"),
    (r"\bone of the (most|greatest|finest|largest)\b", "peacock"),
    (r"\b(it|this) (was|is) (significant|important|notable|remarkable)\b", "peacock"),
    (r"\ba (significant|major|key|pivotal|crucial) (role|part|factor|moment|development)\b", "peacock"),
    (r"\bmarked a (turning point|new era|new chapter)\b", "peacock"),
    # --- weasel words
    (r"\b(it is|it was) (believed|thought|said|claimed|suggested)\b", "weasel"),
    (r"\b(widely|generally) (regarded|considered|seen|held)\b", "weasel"),
    (r"\b(some|many) (have|had) (claimed|suggested|argued|said)\b", "weasel"),
    (r"\blegend has it\b", "weasel"),
    # --- unearned emphasis
    (r"\b(certainly|undoubtedly|clearly|obviously|indeed|above all|unquestionably)\b", "unearned emphasis"),
    # --- emphatic punctuation
    (r"!", "exclamation mark"),
    (r"\?", "question mark (check it is not a real question)"),
]


def fix_text(s: str):
    """Return (repaired_text, list_of_changes)."""
    log = []

    n = len(re.findall(r"\*\*(.+?)\*\*", s))
    if n:
        s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
        log.append("markdown bold removed: %d" % n)

    n = len(re.findall(ITAL_MD, s))
    if n:
        s = re.sub(ITAL_MD, r"''\1''", s)
        log.append("markdown italics converted: %d" % n)

    # Mediawiki bold is removed ONLY outside the lead paragraph.
    # The lead's bold IS the article title (`'''Balboa'''`, `'''Flag of Sinchew'''`),
    # so stripping it would damage every article. Polish it only after the first prose line.
    lines = s.split("\n")
    lead_idx = None
    for i, line in enumerate(lines):
        t = line.strip()
        depth += l.count("{{") - l.count("}}")
        in_template = depth > 0 or l.strip().startswith("{{") or l.strip().startswith("|")
        if t and not t.startswith(("{", "|", "}", "=", "#", "<", "[")):
            lead_idx = i
            break
    if lead_idx is not None:
        head, tail = lines[:lead_idx + 1], lines[lead_idx + 1:]
        tail_s = "\n".join(tail)
        n = len(re.findall(BOLD_MW, tail_s))
        if n:
            tail_s = re.sub(BOLD_MW, r"\1", tail_s)
            log.append("mediawiki bold removed after the lead: %d" % n)
        s = "\n".join(head) + "\n" + tail_s

    # markdown headings -> mediawiki
    out, n = [], 0
    for line in s.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            lvl = len(m.group(1))
            out.append("=" * lvl + " " + m.group(2) + " " + "=" * lvl)
            n += 1
        else:
            out.append(line)
    if n:
        s = "\n".join(out)
        log.append("markdown headings converted: %d" % n)

    # headings: balance the equals, drop a leading article, capitalise
    out, arts, bal, caps = [], 0, 0, 0
    for line in s.split("\n"):
        m = re.match(r"^(=+)([^=].*?)(=+)\s*$", line.rstrip())
        if not m:
            out.append(line)
            continue
        lead, text, trail = m.group(1), m.group(2).strip(), m.group(3)
        if len(lead) != len(trail):
            trail = lead
            bal += 1
        t2 = re.sub(r"^(the|a|an)\s+", "", text, flags=re.I)
        if t2 != text:
            arts += 1
            text = t2
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
            caps += 1
        out.append("%s %s %s" % (lead, text, trail))
    if bal:
        log.append("unbalanced headings repaired: %d" % bal)
    if arts:
        log.append("leading articles removed from headings: %d" % arts)
    if caps:
        log.append("headings capitalised: %d" % caps)
    s = "\n".join(out)

    # whitespace hygiene
    s = "\n".join(l.rstrip() for l in s.split("\n"))
    while "\n\n\n" in s:
        s = s.replace("\n\n\n", "\n\n")
    if s and not s.endswith("\n"):
        s += "\n"

    return s, log


def check_text(s: str):
    problems = []
    for i, l in enumerate(s.split("\n"), 1):
        stripped = l.strip()
        # a line beginning with one or more asterisks is a mediawiki bullet,
        # and "**bold**" must be PAIRED to be markdown
        if not stripped.startswith("*") and re.search(r"\*\*.+?\*\*", l):
            problems.append("L%-4d markdown bold: %s" % (i, stripped[:60]))
        if re.match(r"^#{1,6}\s", l):
            problems.append("L%-4d markdown heading: %s" % (i, l.strip()[:60]))
        if re.match(MD_TABLE, l):
            problems.append("L%-4d MARKDOWN TABLE separator (no wikitable): %s" % (i, l.strip()[:60]))
        m = re.match(r"^(=+)([^=].*?)(=+)\s*$", l.rstrip())
        if m:
            if len(m.group(1)) != len(m.group(3)):
                problems.append("L%-4d unbalanced heading: %s" % (i, l.strip()[:60]))
            t = m.group(2).strip()
            if re.match(r"^(the|a|an)\s", t, re.I):
                problems.append("L%-4d leading article in heading: %s" % (i, l.strip()[:60]))
            if t and t[0].islower():
                problems.append("L%-4d lowercase heading: %s" % (i, l.strip()[:60]))
    # mediawiki bold is acceptable in exactly two places:
    #   - the lead paragraph, where the bold IS the article title
    #   - a bulleted line inside an infobox or {{tree list}}, e.g. *'''Entity''' ~25,000
    # anywhere else it is emphasis, which the project bans.
    lead_done = False
    for i, l in enumerate(s.split("\n"), 1):
        stripped = l.strip()
        is_prose = stripped and not stripped.startswith(("{", "|", "}", "=", "#", "<", "[", "*", "!"))
        if is_prose and not lead_done:
            lead_done = True            # this is the lead; its bold is the title
            continue
        if stripped.startswith(("*", "|")):
            continue                    # bulleted tree-list entry, or an infobox field
        if re.search(BOLD_MW, l):
            problems.append("L%-4d mediawiki bold (emphasis, not a title): %s" % (i, stripped[:60]))
    if s.count("{|") != s.count("|}"):
        problems.append("table markup unbalanced: %d open, %d close" % (s.count("{|"), s.count("|}")))
    # editorialising: reported, never repaired - judgement is required
    for i, l in enumerate(s.split("\n"), 1):
        t = l.strip()
        if not t or t.startswith(("|", "{", "}", "=", "*", "#", "<", "!")):
            continue
        for pat, kind in EDITORIAL:
            if re.search(pat, l):
                problems.append("L%-4d EDITORIAL (%s): %s" % (i, kind, t[:70]))
    return problems


def main(argv):
    do_fix = "--fix" in argv
    do_check = "--check" in argv or not do_fix
    files = [a for a in argv[1:] if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 0

    remaining = 0
    for f in files:
        p = Path(f)
        if not p.exists():
            print("missing: %s" % f)
            remaining += 1
            continue
        s = p.read_text(encoding="utf-8")
        if do_fix:
            s2, log = fix_text(s)
            if s2 != s:
                p.write_text(s2, encoding="utf-8")
                print("fixed  %s" % p.name)
                for x in log:
                    print("         %s" % x)
            s = s2
        if do_check:
            probs = check_text(s)
            if probs:
                remaining += 1
                print("PROBLEMS %s" % p.name)
                for x in probs:
                    print("         %s" % x)
            elif do_fix:
                print("clean  %s" % p.name)

    if remaining and do_check:
        print("\n%d file(s) with problems" % remaining)
    return 1 if remaining else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
