import pandas as pd

df = pd.DataFrame({
    'Batch':   ['A', 'A', 'B', 'B', 'A', 'B'],
    'Subject': ['Math', 'CS', 'Math', 'CS', 'Math', 'CS'],
    'Grade':   [88, 90, 60, 72, 55, 95]
})

print("original:\n", df)
grid = df.pivot_table(index='Batch', columns='Subject',
                      values='Grade', aggfunc='mean')
print("\npivot table:\n", grid)
