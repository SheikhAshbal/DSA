import seaborn as sns
df = sns.load_dataset('tips')
df['tip_pct'] = df['tip'] / df['total_bill'] * 100
corr = df[['total_bill','tip','size','tip_pct']].corr()
print(corr.round(2))
print('\nstrongest with tip:', corr['tip'].drop('tip').abs().idxmax())
