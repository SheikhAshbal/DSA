import numpy as np

np.random.seed(42)
data = np.random.randint(1, 100, size=6)

print("original:", data)

data[data < 50] = 0

print("modified:", data)
