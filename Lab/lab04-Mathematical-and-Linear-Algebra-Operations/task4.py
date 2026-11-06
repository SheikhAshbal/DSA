import numpy as np

values  = np.array([10, 20, 30], dtype=float)
weights = np.array([0.2, 0.5, 0.3])

method1 = np.sum(weights * values)
method2 = weights @ values

print("values         :", values)
print("weights        :", weights)
print("method1 sum(w*v):", method1)
print("method2 w @ v  :", method2)
print("identical      :", np.isclose(method1, method2))
