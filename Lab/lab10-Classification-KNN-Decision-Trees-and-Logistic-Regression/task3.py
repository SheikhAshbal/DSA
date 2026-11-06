from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

X, y = make_classification(
    n_samples=400,
    n_features=6,
    n_informative=4,
    random_state=1
)

Xtr, Xte, ytr, yte = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=1
)

for k in [1, 20]:
    model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=k)
    )
    model.fit(Xtr, ytr)

    accuracy = model.score(Xte, yte)
    print(f"k={k:2d} | Test accuracy: {accuracy:.3f}")
