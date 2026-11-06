import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)

print("original:", x)
print("log     :", np.log(x).round(4))
print("sqrt    :", np.sqrt(x).round(4))
