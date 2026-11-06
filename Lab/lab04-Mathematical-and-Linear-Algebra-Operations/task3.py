import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

elementwise = a * b
dot_product = a @ b

print("a              :", a)
print("b              :", b)
print("a * b (element-wise):", elementwise, "| shape:", elementwise.shape)
print("a @ b (dot product) :", dot_product)
print("verify (a*b).sum() == a@b :", (a * b).sum() == a @ b)
