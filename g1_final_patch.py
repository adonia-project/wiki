import io

ART = r'B:\02_GIT CONNECTED\wiki\articles'
hub = ART + r'\G1 Climax 2026.mediawiki'
c = io.open(hub, encoding='utf-8').read()

subs = [
    # 1. Upcoming shows table -> winner statement
    ('=== Upcoming shows ===\n\n{| class="wikitable" style="text-align:center;"\n! Day\n! Date\n! Block\n! Round\n! City\n! Featured matches\n|-\n| Final\n| Sun Oct 18\n| \u2014\n| \u2014\n| [[Aizawa]]\n| G1 Final at the [[Aizawa Dome]] \u2014 [[Marcus Vance]] vs. [[Taumafa Vaiahi|Taumafa]]\n|}',
     '=== Winner ===\n\nThe G1 Climax 2026 was won by [[Marcus Vance]], who defeated [[Taumafa Vaiahi|Taumafa]] in the Final at the [[Aizawa Dome]] on October 18 (second Drill Driver, 27:44) and challenged [[Leoni Masua]] for the [[IGO Heavyweight Championship]] at [[Wrestling Summit 2027|Wrestling Summit]]. ([[G1 Climax 2026 Final|Full results]])'),
    # 2. results table: add Final row
    ('| [[G1 Climax 2026 Day 19]]\n|}',
     '| [[G1 Climax 2026 Day 19]]\n|-\n| Final\n| Oct 18\n| \u2014\n| \u2014\n| [[Aizawa]]\n| [[G1 Climax 2026 Final]]\n|}'),
    # 3. Final headline before Day 19 headline
    ("* '''Day 19 (Toyozawa):''' The playoff \u2014",
     "* '''G1 Final (Aizawa Dome):''' The Workhorse speaks \u2014 [[Marcus Vance|Vance]] defeats [[Taumafa Vaiahi|Taumafa]] with the second Drill Driver at 27:44 to win the G1 Climax, then breaks nine matches of silence: ''Seventeen points. No words. One more man.'' The challenge is made: [[Wrestling Summit 2027|Wrestling Summit]], January 4, Toyozawa Dome. ([[G1 Climax 2026 Final|Full results]])\n* '''Day 19 (Toyozawa):''' The playoff \u2014"),
    # 4. G1 Final section prose: past tense + result
    ("The G1 Final returns to the Aizawa Dome, the spiritual home of NOPW's Vaiahi community and the site of Leoni Masua's 2021 G1 Climax victory. The week between the final block show (October 9), the Block B playoff (October 10), and the G1 Final (October 18) allows for travel, promotion, and rest. The Aizawa Dome is expected to sell out.",
     "The G1 Final returned to the Aizawa Dome, the spiritual home of NOPW's Vaiahi community and the site of Leoni Masua's 2021 G1 Climax victory. The week between the final block show (October 9), the Block B playoff (October 10), and the G1 Final (October 18) allowed for travel, promotion, and rest. The Aizawa Dome sold out \u2014 30,000. [[Marcus Vance]] defeated [[Taumafa Vaiahi|Taumafa]] in the Final and challenged [[Leoni Masua]] for Wrestling Summit. ([[G1 Climax 2026 Final|Full results]])"),
    # 5. link the Final table event cell
    ('| G1 Climax 2026 Final\n| Sun Oct 18',
     '| [[G1 Climax 2026 Final]]\n| Sun Oct 18'),
]

fails = []
for old, new in subs:
    if old not in c:
        fails.append(old[:80])
        continue
    c = c.replace(old, new, 1)

if fails:
    print('HUB FAILS:')
    for f in fails:
        print('  ', repr(f))
else:
    io.open(hub, 'w', encoding='utf-8', newline='\n').write(c)
    print('hub ok')
