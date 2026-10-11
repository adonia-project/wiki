import io, re, sys

EM = "\u2014"
ART = r'B:\02_GIT CONNECTED\wiki\articles'

def read(p): return io.open(ART + '\\' + p, encoding='utf-8').read()
def write(p, c): io.open(ART + '\\' + p, 'w', encoding='utf-8', newline='\n').write(c)

fails = []
def rep(c, old, new, tag):
    if old in c:
        return c.replace(old, new, 1)
    fails.append(tag)
    return c

# ================= DAY 8 (storyline note) =================
c = read('G1 Climax 2026 Day 8.mediawiki')
c = rep(c, "* '''Three perfect records, three collisions coming.''' KAZUKI, Takagi, and Taumafa are all 4-0 " + EM + " and the round-robin guarantees the collisions: KAZUKI vs. Takagi (Round 5, Naruto), Taumafa vs. Takagi (Round 8, Tsuda), KAZUKI vs. Taumafa (Round 9, Toyozawa). Only one man can run the table.",
           "* '''Two perfect records, and the Dragon bleeds.''' KAZUKI and Taumafa are 4-0 " + EM + " but Takagi is 3-1, submitted by the Ishida Lock in the night's second match. The collisions still come: KAZUKI vs. Takagi (Round 5, Naruto), KAZUKI vs. Taumafa (Round 6, Tosa), Taumafa vs. Takagi (Round 8, Tsuda). Only one man can run the table " + EM + " and the Dragon no longer can.", 'd8-note')
write('G1 Climax 2026 Day 8.mediawiki', c)

# ================= DAY 10 =================
c = read('G1 Climax 2026 Day 10.mediawiki')
c = rep(c, "The night is remembered for the first collision of the block's undefeated three " + EM + " [[KAZUKI (wrestler)|KAZUKI]] against [[Takagi Yuto]], the shooting star against the dragon " + EM + " and for the champions' war:",
           "The night is remembered for the end of the block's perfect era " + EM + " [[KAZUKI (wrestler)|KAZUKI]] against [[Takagi Yuto]], the shooting star against the dragon " + EM + " and for the champions' war:", 'd10-intro')
c = rep(c, "and Ishida, whose G1 has been a quiet rebuilding since the 8:56 humiliation, answered with the mat game",
           "and Ishida, two days removed from submitting the Dragon, answered with the mat game", 'd10-m3-a')
c = rep(c, "Ishida is 2-3; Reyes falls to 0-5", "Ishida is 3-2; Reyes falls to 0-5", 'd10-m3-b')
c = rep(c, "The main event " + EM + " the first collision of the block's undefeated three. KAZUKI's artistry",
           "The main event " + EM + " the Shooting Star against the Dragon, the block's last perfect record against its most dangerous lariat. KAZUKI's artistry", 'd10-m5-a')
c = rep(c, "Takagi falls to 4-1, and the block's math now runs through KAZUKI",
           "Takagi falls to 3-2, and the block's math now runs through KAZUKI", 'd10-m5-b')
c = rep(c, "'''Takagi is the spoiler with a stake.''' 4-1, 8 points, with Taumafa (Round 8, Tsuda) still to come. The Dragon's lariat remains the block's most decisive single move " + EM + " and the projected Tsuda collision is now for second place, at minimum.",
           "'''Takagi is the spoiler with a stake.''' 3-2, 6 points, with Taumafa (Round 8, Tsuda) still to come. The Dragon's lariat remains the block's most decisive single move " + EM + " and the projected Tsuda collision is now a fight to stay in the race at all.", 'd10-note-tak')
c = rep(c, "with Taumafa (Round 9, Toyozawa) and the rest of the schedule still to come",
           "with Diallo (Round 9, Toyozawa) and the rest of the schedule still to come", 'd10-note-kaz')
c = rep(c, "* '''The middle is tightening.''' Kuroki, Ishida, Ono, and Diallo all sit at 4 points " + EM + " the block's middle tier is stacked, and the rounds ahead will sort the chasers from the passed.",
           "* '''The middle is tightening.''' Kuroki, Ono, and Diallo sit at 4 points " + EM + " and Ishida, at 6, has joined the chase pack with Jusuf and the Dragon. The rounds ahead will sort the chasers from the passed.", 'd10-note-mid')
c = rep(c, """|-
| 2
| {{face}} [[Takagi Yuto]]
| 4-1-0
| 8
|-
| 3
| {{face}} [[Taumafa Vaiahi]] (c)
| 4-1-0
| 8
|-
| 4
| {{heel}} [[Jusuf Muntasir]] (c)
| 3-2-0
| 6
|-
| 5
| {{face}} [[Daigo Kuroki]]
| 2-3-0
| 4
|-
| 6
| {{face}} [[Tadayoshi Ishida]]
| 2-3-0
| 4
|-
| 7
| {{face}} [[Yuto Ono]] (c)
| 2-3-0
| 4
|-
| 8
| {{heel}} [[Mamadou Diallo|Mamadou "The Hammer" Diallo]]
| 2-3-0
| 4""",
"""|-
| 2
| {{face}} [[Taumafa Vaiahi]] (c)
| 4-1-0
| 8
|-
| 3
| {{heel}} [[Jusuf Muntasir]] (c)
| 3-2-0
| 6
|-
| 4
| {{face}} [[Takagi Yuto]]
| 3-2-0
| 6
|-
| 5
| {{face}} [[Tadayoshi Ishida]]
| 3-2-0
| 6
|-
| 6
| {{face}} [[Daigo Kuroki]]
| 2-3-0
| 4
|-
| 7
| {{face}} [[Yuto Ono]] (c)
| 2-3-0
| 4
|-
| 8
| {{heel}} [[Mamadou Diallo|Mamadou "The Hammer" Diallo]]
| 2-3-0
| 4""", 'd10-standings')
write('G1 Climax 2026 Day 10.mediawiki', c)

# ================= DAY 12 =================
c = read('G1 Climax 2026 Day 12.mediawiki')
c = rep(c, "Ishida falls to 2-4.", "Ishida falls to 3-3.", 'd12-m2')
c = rep(c, "the move that ended Jusuf's and KAZUKI's undefeated runs now lands on the Hammer",
           "the move that ended Jusuf's undefeated run now lands on the Hammer", 'd12-m4')
c = rep(c, "the family war, and the block's second collision of undefeated names",
           "the family war, and the collision the block had circled since the schedule was drawn", 'd12-m5')
c = rep(c, """| 7
| {{face}} [[Tadayoshi Ishida]]
| 2-4-0
| 4""",
"""| 7
| {{face}} [[Tadayoshi Ishida]]
| 3-3-0
| 6""", 'd12-standings')
write('G1 Climax 2026 Day 12.mediawiki', c)

# ================= DAY 18 (pileup note) =================
c = read('G1 Climax 2026 Day 18.mediawiki')
c = rep(c, "* '''The 12-point pileup.''' KAZUKI, Jusuf, Kuroki " + EM + " three men tied behind the Dragon, the block's middle a photograph. The truth-teller, the enforcer, and the fallen star all finish one point behind the man who beat them all in Tsuda.",
           "* '''The 12-point pileup.''' KAZUKI, Jusuf, Kuroki " + EM + " three men tied two points behind the leaders, the block's middle a photograph. The truth-teller, the enforcer, and the fallen star all finish watching a playoff they could not reach.", 'd18-pileup')
# playoff footnote after the Big Stan note
stan_note = "''Note: [[Big Stan]] withdrew from the tournament on September 16. His remaining matches (Rounds 6\u20139) were recorded as forfeit losses, with each opponent receiving two points.''"
c = rep(c, stan_note, stan_note + "\n\n''Taumafa and Takagi finished level on 14 points. Per G1 regulations, a first-place tie is decided by a playoff match, not the head-to-head " + EM + " [[G1 Climax 2026 Day 19|October 10, Toyozawa]].''", 'd18-footnote')
write('G1 Climax 2026 Day 18.mediawiki', c)

# ================= HUB =================
c = read('G1 Climax 2026.mediawiki')

# --- headlines ---
c = rep(c, "* '''Day 8 (Ogasawara):''' The Kuroshio reunion " + EM + " KAZUKI def. Kuroki, then the bow of the brothers. Takagi, KAZUKI, and Taumafa stay perfect; the block's three undefeated men are on collision course.",
           "* '''Day 8 (Ogasawara):''' The Kuroshio reunion " + EM + " KAZUKI def. Kuroki, then the bow of the brothers. And the Dragon bleeds: Ishida submits Takagi, the Ishida Lock's first giant-killing. KAZUKI and Taumafa stay perfect atop the block.", 'hub-h8')
c = rep(c, "KAZUKI def. Takagi in 21:12, the Dragon's first loss.",
           "KAZUKI def. Takagi in 21:12, the Dragon's second straight loss.", 'hub-h10')
c = rep(c, "Tadayoshi Ishida, written off at 2-4, makes KAZUKI tap",
           "Tadayoshi Ishida, written off at 3-3, makes KAZUKI tap", 'hub-h14')
c = rep(c, "* '''Day 18 (Toyozawa):''' The family closes the block " + EM + " Taumafa def. Ishida to win Block B at 8-1, and books the Aizawa Dome against Vance. KAZUKI stops the slide but finishes in the 12-point pileup behind the Dragon. The Final is set: Vance vs. Taumafa, October 18. ([[G1 Climax 2026 Day 18|Full results]])",
           "* '''Day 18 (Toyozawa):''' The block ends in a tie " + EM + " Taumafa def. Ishida to pull level with Takagi at 14 points, and Block B will be decided by the first playoff in G1 history. KAZUKI stops the slide but finishes in the 12-point pileup. ([[G1 Climax 2026 Day 18|Full results]])\n* '''Day 19 (Toyozawa):''' The playoff " + EM + " Taumafa kicks out of the Dragon lariat and fells Takagi with the Samoan driver to win Block B. The Final is set: Vance vs. Taumafa, October 18, Aizawa Dome. ([[G1 Climax 2026 Day 19|Full results]])", 'hub-h18')

# --- schedule: Leg 4 ---
c = rep(c, "=== Leg 4: Yagikoshu Southwest (October 3" + EM + "9) ===",
           "=== Leg 4: Yagikoshu Southwest (October 3" + EM + "10) ===", 'hub-leg4-h')
c = rep(c, """| 18
| Fri Oct 9
| B
| Round 9
| [[Toyozawa]]
| Toyozawa Municipal Gymnasium
|}""",
"""| 18
| Fri Oct 9
| B
| Round 9
| [[Toyozawa]]
| Toyozawa Municipal Gymnasium
|-
| 19
| Sat Oct 10
| B
| Playoff
| [[Toyozawa]]
| Toyozawa Municipal Gymnasium
|}""", 'hub-leg4-row')
c = rep(c, "The final block shows in Toyozawa will determine the block winners.",
           "The final block shows in Toyozawa determined the block winners " + EM + " and, for the first time in G1 history, a playoff was required: Taumafa and Takagi finished Block B level at 14 points, and the Toyozawa building was held over one more night to settle it.", 'hub-leg4-foot')
c = rep(c, "The nine-day gap between the final block shows (October 9) and the G1 Final (October 18) allows for travel, promotion, and rest.",
           "The week between the final block show (October 9), the Block B playoff (October 10), and the G1 Final (October 18) allows for travel, promotion, and rest.", 'hub-final-gap')

# --- results section: intro + day 19 row ---
c = rep(c, "The G1 Climax 2026 tour consists of 18 tournament shows plus the G1 Final.",
           "The G1 Climax 2026 tour consists of 18 tournament shows, the Block B playoff, and the G1 Final.", 'hub-res-intro')
c = rep(c, "| [[G1 Climax 2026 Day 18]]",
           "| [[G1 Climax 2026 Day 18]]\n|-\n| 19\n| Oct 10\n| B\n| Playoff\n| [[Toyozawa]]\n| [[G1 Climax 2026 Day 19]]", 'hub-res-row19')

# --- upcoming shows ---
c = rep(c, "| G1 Final at the [[Aizawa Dome]] " + EM + " Block A winner vs. Block B winner",
           "| G1 Final at the [[Aizawa Dome]] " + EM + " [[Marcus Vance]] vs. [[Taumafa Vaiahi|Taumafa]]", 'hub-upcoming')

# --- block B header ---
c = rep(c, ";Block B (final " + EM + " Taumafa wins the block)",
           ";Block B (final " + EM + " Taumafa wins the October 10 playoff)", 'hub-b-header')

# --- crosstable cell edits via parser ---
lines = c.split('\n')

def edit_table(lines, tbl_start, edits, tag):
    # tbl_start: index of '{|' line
    # parse header
    cols = []
    i = tbl_start + 1
    while lines[i].startswith('!'):
        name = lines[i][1:].strip()
        if name not in ('Wrestler', 'W-L-D', 'Pts'):
            cols.append(name)
        i += 1
    # parse rows
    row_start = None
    while i < len(lines):
        if lines[i] == '|-':
            i += 1
            row_line = lines[i]
            cells = []
            i += 1
            while i < len(lines) and lines[i].startswith('|') and lines[i] not in ('|-', '|}'):
                cells.append(i)
                i += 1
            # apply edits matching this row
            for e in edits:
                if e['row'] in row_line:
                    if e['col'] == 'W-L-D':
                        li = cells[10]
                    elif e['col'] == 'Pts':
                        li = cells[11]
                    else:
                        li = cells[cols.index(e['col'])]
                    cur = lines[li][1:].strip()
                    if cur != e['old']:
                        fails.append('%s: %s/%s expected [%s] found [%s]' % (tag, e['row'], e['col'], e['old'], cur))
                    else:
                        lines[li] = '| ' + e['new'] if e['new'] else '|'
        elif lines[i] == '|}':
            return i
        else:
            i += 1
    return i

a_edits = [
    {'row': '[[Marcus Vance|Vance]]', 'col': 'Nakamura', 'old': '', 'new': 'W'},
    {'row': '[[Nakamura Shinsuke|Nakamura]]', 'col': 'Vance', 'old': '', 'new': 'L'},
    {'row': '[[Honda Masanori|Honda]]', 'col': 'Morita', 'old': '', 'new': 'W'},
    {'row': 'Morita', 'col': 'Honda', 'old': '', 'new': 'L'},
    {'row': '[[Honda Masanori|Honda]]', 'col': 'Stan', 'old': 'W', 'new': 'L'},
    {'row': 'Stan', 'col': 'Honda', 'old': 'L', 'new': 'W'},
]
b_edits = [
    {'row': '[[Takagi Yuto|Takagi]]', 'col': 'Ishida', 'old': '', 'new': 'L'},
    {'row': 'Ishida', 'col': 'Takagi', 'old': '', 'new': 'W'},
    {'row': 'Ishida', 'col': 'Reyes', 'old': '', 'new': 'W'},
    {'row': 'Reyes', 'col': 'Ishida', 'old': '', 'new': 'L'},
    {'row': 'Tanaka', 'col': 'Reyes', 'old': '', 'new': 'W'},
    {'row': 'Reyes', 'col': 'Tanaka', 'old': '', 'new': 'L'},
    {'row': 'Taumafa', 'col': 'W-L-D', 'old': '8-1-0', 'new': '7-2-0'},
    {'row': 'Taumafa', 'col': 'Pts', 'old': '16', 'new': '14'},
    {'row': 'Ishida', 'col': 'W-L-D', 'old': '4-5-0', 'new': '5-4-0'},
    {'row': 'Ishida', 'col': 'Pts', 'old': '8', 'new': '10'},
]

# locate tables
sec = c.index('=== Final standings ===')
sec_end = c.index('=== Tournament headlines ===')
seg = c[sec:sec_end]
seg_lines = seg.split('\n')
tbl_starts = [i for i, l in enumerate(seg_lines) if l.startswith('{|')]
edit_table(seg_lines, tbl_starts[0], a_edits, 'hubA')
edit_table(seg_lines, tbl_starts[1], b_edits, 'hubB')
c = c[:sec] + '\n'.join(seg_lines) + c[sec_end:]

write('G1 Climax 2026.mediawiki', c)

print('FAILED REPLACES:', fails if fails else 'none')
