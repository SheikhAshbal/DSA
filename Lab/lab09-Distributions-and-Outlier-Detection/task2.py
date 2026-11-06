import seaborn as sns
df = sns.load_dataset('tips')
col = df['total_bill']
q1, q3 = col.quantile(0.25), col.quantile(0.75)
iqr = q3 - q1
low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
outliers = df[(col < low) | (col > high)]
print(f"Q1={q1:.2f} Q3={q3:.2f} IQR={iqr:.2f}")
print(f"bounds: [{low:.2f}, {high:.2f}]")
print("outliers flagged:", len(outliers))
print(outliers[['total_bill','tip']])
