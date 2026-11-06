from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)

pipe = make_pipeline(StandardScaler(), LinearRegression())
pipe.fit(Xtr, ytr)          # scaler fits on train only
pred = pipe.predict(Xte)

print('first five predictions:', pred[:5].round(2))
