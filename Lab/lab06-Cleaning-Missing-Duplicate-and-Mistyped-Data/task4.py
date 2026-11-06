import pandas as pd

df = pd.DataFrame({
    'category': [' Apple', 'apple', 'APPLE ', 'Banana']
})

print("before cleaning:\n", df['category'])

df['category'] = df['category'].str.strip().str.lower()

print("\nafter cleaning:\n", df['category'])
print("\nvalue counts:\n", df['category'].value_counts())
