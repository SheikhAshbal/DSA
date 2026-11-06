import numpy as np

a = np.arange(1, 7)

reshaped = a.reshape(3, -1)

print("original :", a)
print("shape    :", a.shape)
print("\nreshaped :\n", reshaped)
print("new shape:", reshaped.shape)
