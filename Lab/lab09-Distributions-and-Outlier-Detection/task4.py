import seaborn as sns, numpy as np
df = sns.load_dataset('tips')
col = df['total_bill']

z = (col - col.mean()) / col.std()
outliers = df[np.abs(z) > 3]
extreme = outliers.loc[outliers['total_bill'].idxmax()]

print("Detected outliers (|z| > 3):")
print(outliers[['total_bill', 'tip', 'size']])
print("\nMost extreme outlier:")
print(extreme)
