import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import numpy as np

np.random.seed(2)
n = 80
hours = np.random.uniform(1, 10, n)
df = pd.DataFrame({
    'hours':    hours,
    'score':    hours * 6 + np.random.normal(0, 6, n),
    'absences': -hours * 0.3 + np.random.normal(0, 1, n)
})

numeric_cols = df.select_dtypes(include='number').columns.tolist()
print('numeric columns:', numeric_cols)
print('number of numeric columns:', len(numeric_cols))
print('pair plot grid size:', f'{len(numeric_cols)}x{len(numeric_cols)}')
print('total subplots:', len(numeric_cols) ** 2)

g = sns.pairplot(df)
g.figure.savefig('task3_pairplot.png', dpi=100)
print('pair plot saved: task3_pairplot.png')
