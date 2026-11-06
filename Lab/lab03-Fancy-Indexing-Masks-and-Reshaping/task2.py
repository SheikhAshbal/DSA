import numpy as np

a = np.array([10, 25, 40, 55, 70])

result = a[(a > 50) | (a < 20)]

print("original:", a)
print("result  :", result)
