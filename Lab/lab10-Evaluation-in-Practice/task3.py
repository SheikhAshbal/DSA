from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression

X, y = make_classification(
    n_samples=600,
    n_features=6,
    weights=[0.8, 0.2],
    random_state=0
)

model = LogisticRegression(max_iter=1000)

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="f1"
)

print("F1 scores per fold:", scores.round(3))
