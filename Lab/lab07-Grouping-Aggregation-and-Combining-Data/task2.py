import pandas as pd

df = pd.DataFrame({
    'Batch': ['A', 'B', 'A', 'B', 'A', 'B'],
    'Score': [88, 72, 90, 60, 55, 95]
})

summary = df.groupby('Batch')['Score'].agg(['mean', 'max', 'count'])
print(summary)
