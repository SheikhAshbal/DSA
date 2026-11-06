import seaborn as sns

df = sns.load_dataset('tips')

std  = df['total_bill'].std()
skew = df['total_bill'].skew()
q25  = df['total_bill'].quantile(0.25)
q75  = df['total_bill'].quantile(0.75)
iqr  = q75 - q25

print('total_bill stats:')
print(f'  std  : {std:.2f}')
print(f'  skew : {skew:.2f}')
print(f'  Q25  : {q25:.2f}')
print(f'  Q75  : {q75:.2f}')
print(f'  IQR  : {iqr:.2f}')
