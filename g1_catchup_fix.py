import io, re

EM = "\u2014"
ART = r'B:\02_GIT CONNECTED\wiki\articles'

def read(p): return io.open(ART + '\\' + p, encoding='utf-8').read()
def write(p, c): io.open(ART + '\\' + p, 'w', encoding='utf-8', newline='\n').write(c)

fails = []
def rep(c, old, new, tag):
    if old in c:
        return c.replace(old, new)
    fails.append(tag)
    return c

# ================= DAY 8 =================
c = read('G1 Climax 2026 Day 8.mediawiki')
c = rep(c, "| {{face}} [[Takagi Yuto]]\n| Takagi wins " + EM + " Dragon lariat\n| 13:12",
           "| {{face}} [[Takagi Yuto]]\n| Ishida wins " + EM + " Ishida Lock\n| 13:12", 'd8-result')
# match detail rewrite
old_detail_start = "* '''Match 2: Takagi def. Ishida.'''"
i0 = c.index(old_detail_start)
i1 = c.index('\n', i0)
new_detail = ("* '''Match 2: Ishida def. Takagi.''' The Dragon against the Regular Army's veteran " + EM +
  " the grudge of the block's honest men. Ishida, still rebuilding from the 8:56 Jusuf humiliation, took Takagi to the mat and made him work for everything; Takagi's chest was red from the exchange by the ten-minute mark. "
  "The finish: Ishida went for the Ishida Lock at 12 " + EM + " Takagi powered toward the ropes, but the veteran rolled through, kept the hold, and dragged him back to center. "
  "The Dragon tapped at 13:12 " + EM + " the Ishida Lock's first giant-killing of the tournament. Ishida is 2-2; Takagi falls to 3-1, his first loss of the G1. "
  "'''Crowd:''' Dueling '''TAKAGI''' / '''ISHIDA''' chants. '''THIS IS WRESTLING''' during the mat exchanges. STANDING OVATION for the tap " + EM + " the veteran's redemption, live.")
c = c[:i0] + new_detail + c[i1:]
# standings: Takagi 4-0-0/8 -> 3-1-0/6 ; Ishida 1-3-0/2 -> 2-2-0/4 ; reorder Takagi below Taumafa, Ishida above Ono
c = rep(c, """| 2
| {{face}} [[Takagi Yuto]]
| 4-0-0
| 8
|-
| 3
| {{face}} [[Taumafa Vaiahi]] (c)
| 4-0-0
| 8""",
"""| 2
| {{face}} [[Taumafa Vaiahi]] (c)
| 4-0-0
| 8
|-
| 3
| {{face}} [[Takagi Yuto]]
| 3-1-0
| 6""", 'd8-stand-top')
c = rep(c, """| 6
| {{face}} [[Tadayoshi Ishida]]
| 1-3-0
| 2
|-
| 7
| {{face}} [[Yuto Ono]] (c)
| 1-3-0
| 2""",
"""| 6
| {{face}} [[Tadayoshi Ishida]]
| 2-2-0
| 4
|-
| 7
| {{face}} [[Yuto Ono]] (c)
| 1-3-0
| 2""", 'd8-stand-ish')
write('G1 Climax 2026 Day 8.mediawiki', c)
# print storyline notes for review
if '== Storyline notes ==' in c:
    print('=== DAY 8 NOTES (review) ===')
    print(c.split('== Storyline notes ==')[1].split('== See also ==')[0][:1200])

# ================= DAY 14 =================
c = read('G1 Climax 2026 Day 14.mediawiki')
c = rep(c, "written off at 2-4", "written off at 3-3", 'd14-intro')
c = rep(c, "Written off at 2-4", "Written off at 3-3", 'd14-note')
c = rep(c, "Ishida, written off at 3-3, absorbed it", "Ishida, written off at 3-3, absorbed it", 'd14-m4-a')
c = rep(c, "Ishida, written off at 2-4, absorbed it", "Ishida, written off at 3-3, absorbed it", 'd14-m4-b')
c = rep(c, "the same hold that submitted Kuroki on Day 4 and Diallo on Day 2",
           "the same hold that submitted Diallo on Day 4 and Takagi on Day 8", 'd14-hold')
c = rep(c, "Ishida is 3-4, 6 points, alive in the middle",
           "Ishida is 4-3, 8 points, level with Kuroki in the chasers' tier", 'd14-ish-pts')
c = rep(c, "Takagi is 5-1, 10 points", "Takagi is 5-2, 10 points", 'd14-tak-pts')
c = rep(c, "the Ishida Lock has submitted Kuroki, Diallo, and now KAZUKI",
           "the Ishida Lock has submitted Diallo, Takagi, and now KAZUKI", 'd14-lock-note')
# standings: Takagi record + Ishida record/reorder
c = rep(c, """| 3
| {{face}} [[Takagi Yuto]]
| 5-1-0
| 10""",
"""| 3
| {{face}} [[Takagi Yuto]]
| 5-2-0
| 10""", 'd14-stand-tak')
c = rep(c, """| 6
| {{face}} [[Yuto Ono]]
| 3-4-0
| 6
|-
| 7
| {{face}} [[Tadayoshi Ishida]]
| 3-4-0
| 6""",
"""| 6
| {{face}} [[Tadayoshi Ishida]]
| 4-3-0
| 8
|-
| 7
| {{face}} [[Yuto Ono]]
| 3-4-0
| 6""", 'd14-stand-ish')
write('G1 Climax 2026 Day 14.mediawiki', c)

# ================= DAY 16 =================
c = read('G1 Climax 2026 Day 16.mediawiki')
c = rep(c, "made it four submissions of the tournament", "made it five submissions of the tournament", 'd16-sub')
c = rep(c, "Ishida is 4-4, 8 points, a winning record now live with Taumafa remaining in Round 9",
           "Ishida is 5-3, 10 points, level with Jusuf and Kuroki in the chasers' tier, with Taumafa remaining in Round 9", 'd16-ish-pts')
c = rep(c, "Takagi is 6-1, 12 points", "Takagi is 6-2, 12 points", 'd16-tak-pts')
c = rep(c, "'''Ishida's resurrection complete.''' 4-4, 8 points, with Taumafa remaining in Round 9",
           "'''Ishida's resurrection complete.''' 5-3, 10 points, with Taumafa remaining in Round 9", 'd16-ish-note')
c = rep(c, "the block's best story " + EM + " four submissions, including KAZUKI",
           "the block's best story " + EM + " five submissions, including KAZUKI and Takagi", 'd16-sub-note')
c = rep(c, "'''Jusuf and Kuroki: the 10-point chasers.''' Both 5-3",
           "'''The 10-point chasers.''' Jusuf, Kuroki, and now Ishida " + EM + " all 5-3", 'd16-chasers')
c = rep(c, """| 3
| {{face}} [[Takagi Yuto]]
| 6-1-0
| 12""",
"""| 3
| {{face}} [[Takagi Yuto]]
| 6-2-0
| 12""", 'd16-stand-tak')
c = rep(c, """| 6
| {{face}} [[Tadayoshi Ishida]]
| 4-4-0
| 8
|-
| 7
| {{face}} [[Yuto Ono]]
| 4-4-0
| 8""",
"""| 6
| {{face}} [[Tadayoshi Ishida]]
| 5-3-0
| 10
|-
| 7
| {{face}} [[Yuto Ono]]
| 4-4-0
| 8""", 'd16-stand-ish')
write('G1 Climax 2026 Day 16.mediawiki', c)

# ================= DAY 18 =================
c = read('G1 Climax 2026 Day 18.mediawiki')
c = rep(c, "remembered for the family closing the block " + EM + " [[Taumafa Vaiahi|Taumafa]] defeating [[Tadayoshi Ishida]] to win Block B and book the family's place in the Aizawa Dome, and [[KAZUKI (wrestler)|KAZUKI]] stopping the slide with a win that could not save his tournament.",
           "remembered for the block going to a playoff " + EM + " [[Taumafa Vaiahi|Taumafa]] defeating [[Tadayoshi Ishida]] to pull level with [[Takagi Yuto]] at 14 points, forcing the first Block B playoff in G1 history, and [[KAZUKI (wrestler)|KAZUKI]] stopping the slide with a win that could not save his tournament.", 'd18-intro')
c = rep(c, "Takagi finishes 7-2, 14 points " + EM + " second in the block on tiebreakers, the Dragon's G1 ending two points behind the giant.",
           "Takagi finishes the block stage 7-2, 14 points " + EM + " level with the giant, and the Dragon's G1 goes one night further: the October 10 playoff, in this same building.", 'd18-tak-detail')
c = rep(c, "Taumafa is 8-1, 16 points, the Block B winner " + EM + " the family's second finalist in two years, and the Aizawa Dome on October 18 now has its other man.",
           "Taumafa is 7-2, 14 points " + EM + " level with Takagi, and Block B will be decided by a playoff on October 10 in this same building. The Aizawa Dome waits one more night for its other man.", 'd18-tau-detail')
c = rep(c, "Ishida finishes 4-5, 8 points " + EM + " the television champion's G1 ends with the block's best story and four submissions, including the man who ended the 1,095-day reign.",
           "Ishida finishes 5-4, 10 points " + EM + " the television champion's G1 ends with the block's best story and five submissions, including the Dragon and the man who ended the 1,095-day reign.", 'd18-ish-detail')
c = rep(c, """| 1
| {{face}} [[Taumafa Vaiahi]] (c)
| 8-1-0
| 16""",
"""| 1
| {{face}} [[Taumafa Vaiahi]] (c)
| 7-2-0
| 14""", 'd18-stand-tau')
c = rep(c, """| 6
| {{face}} [[Tadayoshi Ishida]]
| 4-5-0
| 8""",
"""| 6
| {{face}} [[Tadayoshi Ishida]]
| 5-4-0
| 10""", 'd18-stand-ish')
c = rep(c, "''Note: [[Big Stan]] withdrew from the tournament on September 16. His remaining matches (Rounds 6\\u20139) were recorded as forfeit losses, with each opponent receiving two points.''",
           "''Note: [[Big Stan]] withdrew from the tournament on September 16. His remaining matches (Rounds 6\\u20139) were recorded as forfeit losses, with each opponent receiving two points.''\n\n''Taumafa and Takagi finished level on 14 points. Per G1 regulations, a first-place tie is decided by a playoff match, not the head-to-head " + EM + " [[G1 Climax 2026 Day 19|October 10, Toyozawa]].''", 'd18-footnote')
c = rep(c, "* '''Taumafa wins Block B.''' 8-1, 16 points, the only loss to Takagi's Dragon lariat in Tsuda. The family's G1 ends the way it began: the giant at the top, the Fono's warrior in the Aizawa Dome, and the chief waiting at Wrestling Summit for whoever survives October 18.",
           "* '''The block ends in a tie.''' Taumafa 7-2, Takagi 7-2 " + EM + " 14 points each, and per G1 regulations first place is decided by a playoff, not the head-to-head. The Dragon beat the giant in Tsuda; on October 10, in this same building, they do it again for everything.", 'd18-note-tau')
c = rep(c, "* '''The Final is set.''' [[Marcus Vance|Marcus \"The Drill\" Vance]] vs. Taumafa, October 18, Aizawa Dome " + EM + " the perfect block against the family's giant, the Workhorse's silence against the family's ceremony. The winner challenges [[Leoni Masua]] at Wrestling Summit.",
           "* '''The Final awaits.''' [[Marcus Vance|Marcus \"The Drill\" Vance]] watches on October 10 " + EM + " the playoff winner meets the Workhorse at the Aizawa Dome on October 18, and the winner of that challenges [[Leoni Masua]] at Wrestling Summit.", 'd18-note-final')
c = rep(c, "* '''Ishida's resurrection ends one win short.''' 4-5, 8 points, four submissions, the block's best story.",
           "* '''Ishida's resurrection ends one win short " + EM + " and changes everything.''' 5-4, 10 points, five submissions, the block's best story. And the Day 8 tap he took from the Dragon is the reason there is a playoff at all.", 'd18-note-ish')
c = rep(c, "| nextevent = [[G1 Climax 2026|G1 Final 2026]]", "| nextevent = [[G1 Climax 2026 Day 19]]", 'd18-next')
c = rep(c, "* [[G1 Climax 2026 Day 17]]\n* [[G1 Climax 2026|G1 Final 2026]]",
           "* [[G1 Climax 2026 Day 17]]\n* [[G1 Climax 2026 Day 19]]", 'd18-seealso')
write('G1 Climax 2026 Day 18.mediawiki', c)

print()
print('FAILED REPLACES:', fails if fails else 'none')
