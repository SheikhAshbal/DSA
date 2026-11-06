import numpy as np

table = np.arange(1, 13).reshape(3, 4).astype(float)
vec = np.array([10.0, 20.0, 30.0])

# Step 1: show the error
print("table shape:", table.shape)
print("vec shape  :", vec.shape)

try:
    result = table - vec
except ValueError as e:
    print("\nError:", e)

# Step 2: fix it with reshape
vec_col = vec.reshape(-1, 1)
print("\nvec reshaped to:", vec_col.shape)

result = table - vec_col
print("\nresult:\n", result)
