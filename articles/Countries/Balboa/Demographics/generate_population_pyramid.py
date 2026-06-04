import matplotlib.pyplot as plt
import numpy as np

# Age structure data (Balboa 2026) — reflecting GAW demographic catastrophe
# GAW: 1935-1947. Population 18M → 11.7M (lost 1/3)
# Key cohorts:
#   80+ (born <1946): Very small — born during/just before GAW, famine, siege, displacement
#   65-79 (born 1947-1961): Post-war baby boom — LARGER cohort
#   50-64 (born 1962-1976): Pre-reunification / reunification era, moderate
#   35-49 (born 1977-1991): Post-reunification, economic growth
#   20-34 (born 1992-2006): Fertility declining toward replacement
#   0-19 (born 2007-2026): Near-replacement fertility, flat base

age_groups = ['0–4', '5–9', '10–14', '15–19', '20–24', '25–29', '30–34', '35–39',
              '40–44', '45–49', '50–54', '55–59', '60–64', '65–69', '70–74', '75–79', '80+']

# Male (thousands) — with GAW pinch and post-war boom
# Total target: ~35.2M, so male total ~17.3M, female ~17.9M
male = [
    1080,  # 0-4    (2022-2026, replacement fertility)
    1110,  # 5-9    (2017-2021)
    1140,  # 10-14  (2012-2016)
    1170,  # 15-19  (2007-2011)
    1200,  # 20-24  (2002-2006)
    1230,  # 25-29  (1997-2001)
    1250,  # 30-34  (1992-1996)
    1200,  # 35-39  (1987-1991, post-reunification)
    1140,  # 40-44  (1982-1986)
    1080,  # 45-49  (1977-1981)
    1020,  # 50-54  (1972-1976, reunification era)
    970,   # 55-59  (1967-1971)
    930,   # 60-64  (1962-1966)
    900,   # 65-69  (1957-1961, late post-war boom)
    870,   # 70-74  (1952-1956, post-war boom)
    810,   # 75-79  (1947-1951, early post-war boom)
    340,   # 80+     (pre-1946, GAW pinch — very small cohort
]

# Female (thousands) — same pattern, slightly more at older ages
female = [
    1040,  # 0-4
    1070,  # 5-9
    1100,  # 10-14
    1130,  # 15-19
    1160,  # 20-24
    1200,  # 25-29
    1220,  # 30-34
    1170,  # 35-39
    1120,  # 40-44
    1060,  # 45-49
    1000,  # 50-54
    970,   # 55-59
    940,   # 60-64
    920,   # 65-69
    910,   # 70-74
    880,   # 75-79
    630,   # 80+     (GAW pinch — more female survivors
]

# Convert to percentages of total population
total_pop = sum(male) + sum(female)
male_pct = [m / total_pop * 100 for m in male]
female_pct = [f / total_pop * 100 for f in female]

fig, ax = plt.subplots(figsize=(10, 8))

y = np.arange(len(age_groups))
bar_height = 0.8

# Male bars (left side, negative)
bars_m = ax.barh(y, [-m for m in male_pct], bar_height, color='#3b82f6', label='Male', edgecolor='white', linewidth=0.3)

# Female bars (right side)
bars_f = ax.barh(y, female_pct, bar_height, color='#ec4899', label='Female', edgecolor='white', linewidth=0.3)

# Labels
ax.set_yticks(y)
ax.set_yticklabels(age_groups, fontsize=10)
ax.set_xlabel('Percentage of population', fontsize=11)
ax.set_title('Population Pyramid of Balboa (2026)', fontsize=14, fontweight='bold', pad=15)

# X-axis formatting
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{abs(x):.1f}%'))
ax.set_xlim(-5.5, 5.5)

# Add value labels on bars
for i, (m, f) in enumerate(zip(male_pct, female_pct)):
    if m > 0.3:
        ax.text(-m - 0.1, i, f'{m:.1f}%', ha='right', va='center', fontsize=7, color='#3b82f6')
    if f > 0.3:
        ax.text(f + 0.1, i, f'{f:.1f}%', ha='left', va='center', fontsize=7, color='#ec4899')

# Add Male/Female labels
ax.text(-2.8, len(age_groups) + 0.3, 'Male', ha='center', fontsize=12, fontweight='bold', color='#3b82f6')
ax.text(2.8, len(age_groups) + 0.3, 'Female', ha='center', fontsize=12, fontweight='bold', color='#ec4899')

# Center line
ax.axvline(0, color='#374151', linewidth=0.5)

# Grid
ax.xaxis.grid(True, alpha=0.2)
ax.set_axisbelow(True)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend
ax.legend(loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/shubhamnaik/Developer/wiki/articles/Countries/Balboa/Demographics/Balboa_population_pyramid.png', dpi=200, bbox_inches='tight')
print("Chart saved!")

# Print summary stats
total = sum(male) + sum(female)
under_18 = sum(male[:4]) + sum(female[:4])  # 0-19 approx for under 18
under_14 = sum(male[:3]) + sum(female[:3])  # 0-14
age_18_44 = sum(male[4:9]) + sum(female[4:9])  # 20-44
age_45_64 = sum(male[9:13]) + sum(female[9:13])  # 45-64
age_65_plus = sum(male[13:]) + sum(female[13:])  # 65+
total_male = sum(male)
total_female = sum(female)

print(f"\n--- Infobox stats ---")
print(f"Total pop: {total:,}k = {total*1000:,}")
print(f"Under 18: {under_18/total*100:.1f}%")
print(f"18-44: {age_18_44/total*100:.1f}%")
print(f"45-64: {age_45_64/total*100:.1f}%")
print(f"65+: {age_65_plus/total*100:.1f}%")
print(f"0-14: {under_14/total*100:.1f}%")
print(f"15-64: {(total - under_14 - age_65_plus)/total*100:.1f}%")
print(f"Male/Female ratio: {total_male/total_female:.3f}")
