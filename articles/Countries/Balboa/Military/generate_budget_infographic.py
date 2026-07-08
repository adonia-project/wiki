#!/usr/bin/env python3
"""Generate BDF budget infographic for the Balboan Defence Forces article."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── Data ──────────────────────────────────────────────────────────────────
TOTAL_BUDGET = 2.4  # billion USD
GDP_PERCENT = 0.7

# By branch (millions)
branch_data = {
    "Naval and Air Service": 1200,
    "Army": 960,
    "Joint / Ministry": 240,
}

# By category (millions)
category_data = {
    "Personnel": 1200,
    "Operations & Maintenance": 600,
    "Equipment Procurement": 360,
    "Infrastructure": 240,
}

# Personnel totals for context
personnel_data = {
    "Naval and Air Service": 17900,
    "Army": 12000,
    "Civilian": 3375,
}

# ── Style ──────────────────────────────────────────────────────────────────
NAVY = "#1B3A5C"
STEEL = "#4A7BA8"
LIGHT_BLUE = "#7BA7CC"
GOLD = "#C4A544"
DARK_TEXT = "#1A1A1A"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "text.color": DARK_TEXT,
    "axes.edgecolor": "#CCCCCC",
})

fig = plt.figure(figsize=(12, 8), facecolor=WHITE)
fig.set_constrained_layout(False)

# ── Title ──────────────────────────────────────────────────────────────────
fig.text(0.5, 0.95, "Balboan Defence Forces — Budget 2026",
         fontsize=20, fontweight="bold", color=NAVY, ha="center", va="top")

# ── Top banner: total & GDP ─────────────────────────────────────────────────
banner = FancyBboxPatch(
    (0.03, 0.84), 0.94, 0.07,
    boxstyle="round,pad=0.01", transform=fig.transFigure,
    facecolor=NAVY, edgecolor="none",
)
fig.patches.append(banner)

fig.text(0.20, 0.882, f"~${TOTAL_BUDGET:.1f} billion",
         fontsize=26, fontweight="bold", color=WHITE,
         ha="center", va="center")
fig.text(0.20, 0.853, "Total Budget",
         fontsize=11, color="#AACCDD", ha="center", va="center")

fig.text(0.50, 0.882, f"~{GDP_PERCENT:.1f}%",
         fontsize=26, fontweight="bold", color=WHITE,
         ha="center", va="center")
fig.text(0.50, 0.853, "of GDP",
         fontsize=11, color="#AACCDD", ha="center", va="center")

fig.text(0.80, 0.882, "~30,000",
         fontsize=26, fontweight="bold", color=WHITE,
         ha="center", va="center")
fig.text(0.80, 0.853, "Active Personnel",
         fontsize=11, color="#AACCDD", ha="center", va="center")

# ── Left panel: by branch (donut) ──────────────────────────────────────────
ax1 = fig.add_axes([0.06, 0.40, 0.40, 0.40])
ax1.set_aspect("equal")
ax1.set_title("Budget by Branch", fontsize=14, fontweight="bold", color=NAVY, pad=15)

branch_vals = list(branch_data.values())
branch_labels = list(branch_data.keys())
branch_colors = [NAVY, STEEL, LIGHT_BLUE]

wedges, texts, autotexts = ax1.pie(
    branch_vals, labels=None,
    autopct=lambda p: f"${p/100*sum(branch_vals)/1000:.1f}B\n({p:.0f}%)",
    startangle=90, colors=branch_colors,
    pctdistance=0.75, wedgeprops=dict(width=0.42, edgecolor=WHITE, linewidth=2),
    textprops=dict(fontsize=11, color=WHITE, fontweight="bold"),
)
for autotext in autotexts:
    autotext.set_color(WHITE)
    autotext.set_fontsize(11)
    autotext.set_fontweight("bold")
ax1.legend(wedges, branch_labels, loc="lower center",
           bbox_to_anchor=(0.5, -0.16), fontsize=10, frameon=False, ncol=1)

# ── Right panel: by category (horizontal bars) ─────────────────────────────
ax2 = fig.add_axes([0.52, 0.40, 0.44, 0.40])
ax2.set_title("Budget by Category", fontsize=14, fontweight="bold", color=NAVY, pad=15)

cat_labels = list(category_data.keys())
cat_vals = list(category_data.values())
cat_colors = [NAVY, STEEL, LIGHT_BLUE, GOLD]

y_pos = np.arange(len(cat_labels))
bars = ax2.barh(y_pos, cat_vals, color=cat_colors, edgecolor=WHITE, height=0.6)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(cat_labels, fontsize=10)
ax2.invert_yaxis()
ax2.set_xlabel("Million USD", fontsize=10, color="#666666")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.tick_params(axis="x", colors="#999999", labelsize=9)
ax2.set_xlim(0, 1350)

for bar, val in zip(bars, cat_vals):
    pct = val / sum(cat_vals) * 100
    ax2.text(bar.get_width() + 18, bar.get_y() + bar.get_height()/2,
             f"${val}M ({pct:.0f}%)", va="center", fontsize=9, color=DARK_TEXT)

# ── Bottom panel: personnel breakdown ──────────────────────────────────────
ax3 = fig.add_axes([0.06, 0.07, 0.90, 0.22])
ax3.set_title("Personnel Breakdown", fontsize=14, fontweight="bold", color=NAVY, pad=10)
ax3.axis("off")

personnel_labels = list(personnel_data.keys())
personnel_vals = list(personnel_data.values())
total_personnel = sum(personnel_vals)
personnel_colors = [NAVY, STEEL, LIGHT_BLUE]

cumulative = 0
bar_height = 0.50
bar_y = 0.30

for label, val, color in zip(personnel_labels, personnel_vals, personnel_colors):
    width = val / total_personnel
    rect = FancyBboxPatch(
        (cumulative, bar_y), width, bar_height,
        boxstyle="square,pad=0", facecolor=color, edgecolor=WHITE, linewidth=2,
        transform=ax3.transAxes,
    )
    ax3.add_patch(rect)
    pct = val / total_personnel * 100
    text_x = cumulative + width / 2
    if width > 0.08:
        ax3.text(text_x, bar_y + bar_height/2,
                 f"{val:,}\n({pct:.1f}%)",
                 ha="center", va="center", fontsize=10, color=WHITE, fontweight="bold",
                 transform=ax3.transAxes)
    cumulative += width

cumulative = 0
for label, val, color in zip(personnel_labels, personnel_vals, personnel_colors):
    width = val / total_personnel
    text_x = cumulative + width / 2
    ax3.text(text_x, bar_y + bar_height + 0.08, label,
             ha="center", va="bottom", fontsize=9, color=DARK_TEXT,
             transform=ax3.transAxes)
    cumulative += width

ax3.text(0.5, 0.05, f"Total: {total_personnel:,} (military + civilian)",
         ha="center", va="center", fontsize=10, color="#666666",
         transform=ax3.transAxes)
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)

# ── Footer ─────────────────────────────────────────────────────────────────
fig.text(0.5, 0.02,
         "Source: Ministry of Defence (Balboa) — Internal reference data",
         ha="center", fontsize=9, color="#666666", style="italic")

plt.savefig(
    "/Users/shubhamnaik/Developer/wiki/articles/Countries/Balboa/Military/BDF budget infographic.png",
    dpi=200, bbox_inches="tight", pad_inches=0.15, facecolor=WHITE,
)
print("Saved: BDF budget infographic.png")
