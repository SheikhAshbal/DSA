import pandas as pd
import os

# create and write JSON first
df_raw = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'price':   [100, 250, 80],
    'qty':     [3, 1, 5]
})
df_raw.to_json('data.json')

# read JSON back
df = pd.read_json('data.json')
print("DataFrame from JSON:\n", df)

# save as Excel
df.to_excel('converted_data.xlsx', index=False)

# verify file was written
print("\nFile exists:", os.path.exists('converted_data.xlsx'))
print("File size  :", os.path.getsize('converted_data.xlsx'), "bytes")
