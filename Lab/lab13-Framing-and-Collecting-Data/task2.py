from sklearn.datasets import load_iris

iris = load_iris()

print("Feature dataset shape:", iris.data.shape)
print("Target shape:", iris.target.shape)
