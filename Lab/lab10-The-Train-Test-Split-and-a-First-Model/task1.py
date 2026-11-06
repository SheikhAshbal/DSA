from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)

print('train rows:', Xtr.shape[0], '| test rows:', Xte.shape[0])
print('Xtr shape:', Xtr.shape)
print('Xte shape:', Xte.shape)
print('ytr shape:', ytr.shape)
print('yte shape:', yte.shape)
print('train fraction:', Xtr.shape[0] / X.shape[0])
