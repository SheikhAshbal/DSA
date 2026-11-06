import pandas as pd

df = pd.DataFrame({
    'price': ['10.5', '12.0', 'missing', '8.99', '15.0']
})

print("dtype before:", df['price'].dtype)
print("column before:\n", df['price'])

df['price'] = pd.to_numeric(df['price'], errors='coerce')

print("\ndtype after:", df['price'].dtype)
print("column after:\n", df['price'])
