import pandas as pd

df = pd.DataFrame(
    {'hours': [2, 8, 5, 1],
     'score': [50, 88, 70, 40]},
    index=['ali', 'sara', 'omar', 'hina']
)

print("DataFrame:\n", df)
print("\nloc by label 'sara':\n", df.loc['sara'])
print("\niloc by position 1:\n", df.iloc[1])
print("\nloc rows + col:", df.loc[['ali', 'omar'], 'score'].tolist())
print("\niloc block:\n", df.iloc[0:2, 0:2])
