import seaborn as sns
import numpy as np

df = sns.load_dataset('tips')
predictors = ['total_bill', 'size']   # target ('tip') deliberately excluded
corr = df[predictors].corr()
print(corr.round(2))

vals = corr.abs().values.copy()
np.fill_diagonal(vals, 0)
max_pair = np.unravel_index(np.argmax(vals), vals.shape)
f1, f2 = corr.columns[max_pair[0]], corr.columns[max_pair[1]]
print(f"\nStrongest predictor-predictor correlation: {f1} vs {f2} = {corr.loc[f1, f2]:.2f}")
