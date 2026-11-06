import seaborn as sns
df = sns.load_dataset('tips')
print('mean total_bill by day:')
print(df.groupby('day')['total_bill'].mean().round(2))
print('\nfull summary stats by day:')
print(df.groupby('day')['total_bill'].describe().round(2))
