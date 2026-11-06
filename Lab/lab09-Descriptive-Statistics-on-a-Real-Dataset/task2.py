import seaborn as sns

df = sns.load_dataset('tips')

print('--- day ---')
print(df['day'].value_counts())
print('\nproportions:')
print(df['day'].value_counts(normalize=True).round(2))
