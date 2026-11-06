import matplotlib; matplotlib.use('Agg')
import seaborn as sns
df = sns.load_dataset('tips')
ax = sns.histplot(df['total_bill'], kde=True, bins=25)
ax.set_title('Distribution of total_bill')
ax.figure.savefig('dist.png', dpi=120, bbox_inches='tight')
print('skew of total_bill:', round(df['total_bill'].skew(), 2))
print('saved histogram + KDE')
