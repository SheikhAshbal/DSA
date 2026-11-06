import pandas as pd
import numpy as np

# create a sample CSV file first
df_raw = pd.DataFrame({
    'name':   ['Ali', 'Sara', 'Omar', 'Hina', 'Zed'],
    'age':    [22, 35, np.nan, 19, 28],
    'score':  [88, 72, 55, np.nan, 91],
    'batch':  ['A', 'B', 'A', 'B', 'A'],
})
df_raw.to_csv('students.csv', index=False)

# load it back
df = pd.read_csv('students.csv')

# five-command first look
print("1. HEAD:\n", df.head())
print("\n2. SHAPE:", df.shape)
print("\n3. INFO:")
df.info()
print("\n4. DESCRIBE:\n", df.describe())
print("\n5. NULLS:\n", df.isnull().sum())
