from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)

pipe = make_pipeline(StandardScaler(), LinearRegression())
pipe.fit(Xtr, ytr)

coefs = pipe.named_steps['linearregression'].coef_
intercept = pipe.named_steps['linearregression'].intercept_

print('coefficients:', coefs.round(2))
print('intercept:', round(intercept, 2))
