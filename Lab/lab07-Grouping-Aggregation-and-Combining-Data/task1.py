import pandas as pd

df = pd.DataFrame({
    'Region': ['North', 'South', 'North', 'South', 'North'],
    'Sales':  [200, 150, 300, 250, 100]
})

print("DataFrame:\n", df)
result = df.groupby('Region')['Sales'].sum()
print("\ntotal sales per region:\n", result)
