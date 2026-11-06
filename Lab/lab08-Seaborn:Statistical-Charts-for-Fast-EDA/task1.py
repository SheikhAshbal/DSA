import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import numpy as np

np.random.seed(0)
df = pd.DataFrame({
    'batch': ['A']*20 + ['B']*20,
    'score': list(np.random.normal(75, 8, 20)) +
             list(np.random.normal(65, 12, 20))
})

ax = sns.boxplot(data=df, x='batch', y='score')
ax.set_title('Score distribution by batch')

ax.figure.savefig('task1_box.png', dpi=150, bbox_inches='tight')
print('box plot saved: task1_box.png')
print('\nDataFrame sample:\n', df.groupby('batch')['score'].describe().round(2))
