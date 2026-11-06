import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("tips")
df = df.dropna().drop_duplicates().copy()
df = df[df["total_bill"] > 0].copy()
df["tip_pct"] = df["tip"] / df["total_bill"]

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(df["size"], df["tip_pct"], alpha=0.5)

ax.set_title("Tip Fraction vs Party Size")
ax.set_xlabel("Party size")
ax.set_ylabel("Tip fraction (0.15 = 15%)")

fig.tight_layout()
fig.savefig("tip_vs_size.png", dpi=150)
plt.close(fig)

print("Saved plot: tip_vs_size.png")
print("Correlation:", round(df["size"].corr(df["tip_pct"]), 3))
