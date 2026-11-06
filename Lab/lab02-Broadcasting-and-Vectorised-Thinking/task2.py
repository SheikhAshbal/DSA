import numpy as np

data = np.array([[1,  2,  3],
                 [4,  5,  6],
                 [7,  8,  9],
                 [10, 11, 12]])

row_vec = np.array([10, 20, 30])

result = data + row_vec

print("data shape    :", data.shape)
print("row_vec shape :", row_vec.shape)
print("result shape  :", result.shape)
print("\nresult:\n", result)
