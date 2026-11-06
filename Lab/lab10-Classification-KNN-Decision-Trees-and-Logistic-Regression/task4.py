from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=400,
    n_features=8,
    n_informative=5,
    random_state=2
)

Xtr, Xte, ytr, yte = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=2
)

models = [
    ("Unlimited-depth tree",
     DecisionTreeClassifier(random_state=2)),
    ("Shallow tree (depth=2)",
     DecisionTreeClassifier(max_depth=2, random_state=2))
]

for name, model in models:
    model.fit(Xtr, ytr)

    print(name)
    print(f"Training accuracy: {model.score(Xtr, ytr):.3f}")
    print(f"Test accuracy:     {model.score(Xte, yte):.3f}")
    print()
