total_votes = 67304209
total_seats = 475
total_smd = 289

blocks = {
    "Okami Block": {"smd": 92, "pr": 59, "total": 151},
    "Miseto Block": {"smd": 60, "pr": 39, "total": 99},
    "Asuka Block": {"smd": 34, "pr": 22, "total": 56},
    "Urakawa Block": {"smd": 15, "pr": 10, "total": 25},
    "Mutsu Block": {"smd": 14, "pr": 9, "total": 23},
    "Nishi-Yagikoshu Block": {"smd": 14, "pr": 9, "total": 23},
    "Nankai Block": {"smd": 14, "pr": 9, "total": 23},
    "Oku Block": {"smd": 13, "pr": 8, "total": 21},
    "Kihoku Block": {"smd": 12, "pr": 8, "total": 20},
    "Suzuka Block": {"smd": 10, "pr": 6, "total": 16},
    "Minami Harujima Block": {"smd": 8, "pr": 5, "total": 13},
    "Ogasawara Block": {"smd": 3, "pr": 2, "total": 5},
}

cities = {
    "Okami Metropolis": 56,
    "Toyozawa Metropolis": 29,
    "Aizawa Prefecture": 10,
}

print("=== THREE BIGGEST BLOCKS: VOTE SHARE ===")
big3_seats = blocks["Okami Block"]["total"] + blocks["Miseto Block"]["total"] + blocks["Asuka Block"]["total"]
big3_pct = big3_seats / total_seats * 100
big3_votes = big3_pct / 100 * total_votes
print("Okami + Miseto + Asuka: " + str(big3_seats) + "/" + str(total_seats) + " seats = " + str(round(big3_pct, 1)) + "% = ~" + f"{big3_votes:,.0f}" + " votes")
for name in ["Okami Block", "Miseto Block", "Asuka Block"]:
    b = blocks[name]
    pct = b["total"] / total_seats * 100
    votes = pct / 100 * total_votes
    print("  " + name + ": " + str(b["total"]) + " seats (" + str(round(pct, 1)) + "%) = ~" + f"{votes:,.0f}" + " votes")

print()
print("=== THREE BIGGEST CITIES: VOTE SHARE ===")
city_smd_total = sum(cities.values())
city_pct = city_smd_total / total_smd * 100
city_votes = city_pct / 100 * total_votes
print("Okami + Toyozawa + Aizawa: " + str(city_smd_total) + "/" + str(total_smd) + " SMD seats = " + str(round(city_pct, 1)) + "% of electorate = ~" + f"{city_votes:,.0f}" + " votes")
for name, smd in cities.items():
    pct = smd / total_smd * 100
    votes = pct / 100 * total_votes
    print("  " + name + ": " + str(smd) + " SMD seats (" + str(round(pct, 1)) + "%) = ~" + f"{votes:,.0f}" + " votes")

print()
print("=== SCENARIO: PARTY DOMINATES OKAMI, TOYOZAWA, AIZAWA ===")
print()
print("--- Option A: Sweep just the 3 cities' SMD seats ---")
smd_won = city_smd_total
okami_pr_share = 56 / 92
miseto_pr_share = 29 / 60
asuka_pr_share = 10 / 34
okami_pr_won = round(okami_pr_share * 59)
miseto_pr_won = round(miseto_pr_share * 39)
asuka_pr_won = round(asuka_pr_share * 22)
total_pr_won = okami_pr_won + miseto_pr_won + asuka_pr_won
total_won = smd_won + total_pr_won
print("SMD seats won (city sweep): " + str(smd_won))
print("PR seats won (proportional to city vote share):")
print("  Okami Block PR: " + str(okami_pr_won) + " of 59")
print("  Miseto Block PR: " + str(miseto_pr_won) + " of 39")
print("  Asuka Block PR: " + str(asuka_pr_won) + " of 22")
print("  PR total: " + str(total_pr_won))
print("TOTAL seats from 3 cities: " + str(total_won) + " of 475 (" + str(round(total_won/475*100, 1)) + "%)")
print("Majority threshold: 238")
print("Shortfall: " + str(238 - total_won) + " seats")

print()
print("--- Option B: Sweep ENTIRE Okami+Miseto+Asuka blocks ---")
full_smd = blocks["Okami Block"]["smd"] + blocks["Miseto Block"]["smd"] + blocks["Asuka Block"]["smd"]
full_pr = blocks["Okami Block"]["pr"] + blocks["Miseto Block"]["pr"] + blocks["Asuka Block"]["pr"]
full_total = full_smd + full_pr
print("Full block sweep: " + str(full_smd) + " SMD + " + str(full_pr) + " PR = " + str(full_total) + " seats (" + str(round(full_total/475*100, 1)) + "%)")
print("Majority threshold: 238")
print("Shortfall: " + str(238 - full_total) + " seats")
print("Vote share for full block sweep: ~" + f"{big3_votes:,.0f}" + " (" + str(round(big3_pct, 1)) + "%)")

print()
print("--- Option C: Sweep cities + realistic PR + pick up rural seats ---")
# Win all 3 cities SMD, proportional PR in those blocks, plus some rural pickups
rural_pickups = 238 - total_won
print("Need " + str(rural_pickups) + " more seats for majority")
print("That's " + str(rural_pickups) + " seats from the remaining 9 blocks (169 seats total)")
print("Would need " + str(round(rural_pickups/169*100, 1)) + "% of remaining block seats")

print()
print("=== COMPARISON: 2026 ELECTION ACTUAL RESULTS ===")
actual = {"SCP": 115, "LDP": 110, "OSP": 100, "PPO": 63, "SDP": 36, "NKP": 32, "OIP": 18, "IND": 1}
print("SCP won 115 seats - could they have done it with city dominance?")
print("SCP 2026 city seats (Okami+Miseto+Asuka blocks): 48+28+10 = 86 seats")
print("SCP needed from rural blocks: 238-86 = 152... nope, only 115 total")
print()
print("The 3 big blocks (306 seats) are " + str(round(306/475*100,1)) + "% of the Diet.")
print("No party has ever won a majority from cities alone.")
