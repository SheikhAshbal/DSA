import numpy as np

a = np.array([1, 2])
b = np.array([3, 4])

vstacked = np.vstack([a, b])
print("vstack result:\n", vstacked)
print("vstack shape :", vstacked.shape)

hconcat = np.concatenate([a.reshape(1, -1), b.reshape(1, -1)], axis=1)
print("\nconcatenate axis=1 result:", hconcat)
print("concatenate shape        :", hconcat.shape)
