import matplotlib.pyplot as plt
import numpy as np

# Data
ethnic_groups = ['White', 'Fosian', 'Mixed', 'Black', 'Birú']

# Estret: relatively equal incomes (canal corridor economy)
estret = [16000, 17200, 15000, 13200, 9800]

# Tramuntana: everyone poor, white slightly better, Birú extreme poverty
tramuntana = [3800, 3500, 2800, 2200, 1200]

# National medians for reference
national = [7800, 11800, 7600, 6500, 2100]

x = np.arange(len(ethnic_groups))
width = 0.25

fig, ax = plt.subplots(figsize=(12, 7))

bars1 = ax.bar(x - width, estret, width, label='Estret Province', color='#2b6cb0', edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x, tramuntana, width, label='Tramuntana Province', color='#d97706', edgecolor='white', linewidth=0.5)
bars3 = ax.bar(x + width, national, width, label='National median', color='#6b7280', edgecolor='white', linewidth=0.5, alpha=0.7)

# Labels and formatting
ax.set_ylabel('Median Household Income (International Dollar)', fontsize=12)
ax.set_title('Median Household Income by Ethnic Group\nEstret Province vs Tramuntana Province vs National Median', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(ethnic_groups, fontsize=11)
ax.legend(fontsize=11, loc='upper right')

# Y-axis formatting
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_ylim(0, 20000)

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

# Add a subtle grid
ax.yaxis.grid(True, alpha=0.3)
ax.set_axisbelow(True)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



plt.tight_layout()
plt.savefig('/Users/shubhamnaik/Developer/wiki/articles/Countries/Balboa/Economy/estret_tramuntana_income_comparison.png', dpi=200, bbox_inches='tight')
print("Chart saved!")
