import numpy as np

np.random.seed(0)
data = np.random.randint(1, 100, size=(5, 2)).astype(float)

print("original:\n", data)
print("col means:", data.mean(axis=0))
print("col stds :", data.std(axis=0))

standardised = (data - data.mean(axis=0)) / data.std(axis=0)

print("\nstandardised:\n", standardised.round(2))
print("col means after:", standardised.mean(axis=0).round(6))
print("col stds  after:", standardised.std(axis=0).round(6))
