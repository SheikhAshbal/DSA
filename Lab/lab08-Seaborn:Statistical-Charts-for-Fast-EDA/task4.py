import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(3)
df = pd.DataFrame({
    'batch': ['A']*20 + ['B']*20,
    'score': list(np.random.normal(75, 8, 20)) +
             list(np.random.normal(65, 12, 20))
})

ax = sns.boxplot(data=df, x='batch', y='score')

# drop down to Matplotlib for fine control
ax.set_title('Batch A consistently outperforms Batch B')
ax.set_xlabel('Student Batch (group)')
ax.set_ylabel('Exam Score (out of 100)')
ax.axhline(70, color='red', linestyle='--', label='pass threshold')
ax.legend()

ax.figure.savefig('task4_refined.png', dpi=150, bbox_inches='tight')
print('chart saved: task4_refined.png')
print('title added: Batch A consistently outperforms Batch B')
print('xlabel added: Student Batch (group)')
print('ylabel added: Exam Score (out of 100)')
print('threshold line added at score = 70')
