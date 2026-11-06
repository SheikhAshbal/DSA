import numpy as np

values = np.array([12, 45, 7, 89, 32, 15])

mask = values > 20

filtered = values[mask]

print("original:", values)
print("mask    :", mask)
print("filtered:", filtered)
