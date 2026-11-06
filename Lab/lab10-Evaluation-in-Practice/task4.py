from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

X, y = make_classification(
    n_samples=600,
    n_features=6,
    weights=[0.8, 0.2],
    random_state=0
)

pipe = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    pipe,
    X,
    y,
    cv=cv,
    scoring="f1"
)

print("F1 scores per fold:", scores.round(3))
print("Mean F1 score:", round(scores.mean(), 3))
print("Standard deviation:", round(scores.std(), 3))
