import pandas as pd

df1 = pd.DataFrame({
    'ID':   [1, 2, 3],
    'Name': ['Ali', 'Sara', 'Omar']
})

df2 = pd.DataFrame({
    'ID':    [2, 3, 4],
    'Score': [88, 72, 95]
})

print("df1:\n", df1)
print("\ndf2:\n", df2)

inner = pd.merge(df1, df2, on='ID', how='inner')
print("\ninner merge:\n", inner)
print("inner row count:", len(inner))

left = pd.merge(df1, df2, on='ID', how='left')
print("\nleft merge:\n", left)
print("left row count:", len(left))
