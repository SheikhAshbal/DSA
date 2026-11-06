import numpy as np

X = np.array([[2.0, 3.0],
              [4.0, 1.0],
              [6.0, 2.0]])

w = np.array([1.5, 2.0])

predictions = X @ w

print("feature matrix X:\n", X)
print("weights w       :", w)
print("predictions     :", predictions)
print("X shape:", X.shape, "| w shape:", w.shape, "| result shape:", predictions.shape)
