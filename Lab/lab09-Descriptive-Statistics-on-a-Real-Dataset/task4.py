import seaborn as sns

df = sns.load_dataset('tips')

print('total_bill grouped by day:\n')
print(df.groupby('day')['total_bill'].describe().round(2))

print('\ntotal_bill grouped by time:\n')
print(df.groupby('time')['total_bill'].describe().round(2))
