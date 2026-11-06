from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = make_classification(
    n_samples=300,
    n_features=5,
    random_state=0
)

Xtr, Xte, ytr, yte = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=0
)

model = LogisticRegression(max_iter=1000)
model.fit(Xtr, ytr)

sample = Xte[:5]
labels = model.predict(sample)
probabilities = model.predict_proba(sample)

print("Probability columns correspond to classes:", model.classes_)
print("Predicted label | Probability array")

for label, probs in zip(labels, probabilities):
    print(f"{label:15d} | {probs.round(3)}")
