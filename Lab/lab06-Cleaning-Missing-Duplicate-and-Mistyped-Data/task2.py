import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name':  ['ali', 'sara', 'omar', 'hina', 'zed'],
    'score': [88, np.nan, 55, np.nan, 91]
})

print("before imputation:\n", df)

df['score'] = df['score'].fillna(df['score'].median())

print("\nafter imputation:\n", df)
print("median used:", 88 + 55 + 91)
