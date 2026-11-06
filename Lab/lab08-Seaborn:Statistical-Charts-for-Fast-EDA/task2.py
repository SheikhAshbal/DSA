import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import numpy as np

np.random.seed(1)
n = 100
hours = np.random.uniform(1, 10, n)
df = pd.DataFrame({
    'hours':    hours,
    'score':    hours * 6 + np.random.normal(0, 5, n),
    'absences': -hours * 0.5 + np.random.normal(0, 2, n),
    'noise':    np.random.normal(0, 1, n)
})

corr = df.corr()
print('correlation matrix:\n', corr.round(2))

ax = sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
ax.set_title('Correlation heatmap')
ax.figure.savefig('task2_heatmap.png', dpi=150, bbox_inches='tight')
print('\nheatmap saved: task2_heatmap.png')
