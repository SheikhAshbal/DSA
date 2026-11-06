import seaborn as sns, numpy as np
df = sns.load_dataset('tips')
col = df['total_bill']
z = (col - col.mean()) / col.std()
z_out = df[np.abs(z) > 3]
print("z-score outliers (|z|>3):", len(z_out))
print(z_out[['total_bill']])
