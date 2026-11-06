import pandas as pd

df = pd.DataFrame({
    'name':  ['ali', 'sara', 'omar', 'ali', 'sara'],
    'score': [88, 72, 55, 88, 72]
})

print("original DataFrame:\n", df)
print("\nduplicate count:", df.duplicated().sum())
print("which rows are duplicates:\n", df[df.duplicated()])

clean = df.drop_duplicates()
print("\ncleaned DataFrame:\n", clean)
print("rows remaining:", len(clean))
