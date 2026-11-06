import seaborn as sns

df = sns.load_dataset("tips")
df = df.dropna().drop_duplicates().copy()
df = df[df["total_bill"] > 0].copy()

df["tip_pct"] = df["tip"] / df["total_bill"]

print("Maximum tip_pct:", df["tip_pct"].max())
