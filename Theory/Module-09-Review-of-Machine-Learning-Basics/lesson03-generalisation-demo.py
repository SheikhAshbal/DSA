"""Reproducible synthetic examples for Module IX, Lesson 3."""
import argparse
from pathlib import Path
import numpy as np
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits

def run_examples():
    X, y = make_classification(n_samples=300, n_features=10, random_state=0)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
    # Source omits the tree seed; fix it so the reported example is reproducible.
    tree = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
    # Integer cv=5 uses unshuffled stratified folds for a binary classifier.
    source_scores = cross_val_score(
        DecisionTreeClassifier(max_depth=4, random_state=0), X, y, cv=5)
    # Selection diagnostic: keep the final test partition out of this comparison.
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    depths = [1, 2, 4, 8, None]
    curves = []
    for depth in depths:
        result = cross_validate(DecisionTreeClassifier(max_depth=depth, random_state=0),
                                Xtr, ytr, cv=folds, return_train_score=True)
        curves.append((float(result["train_score"].mean()),
                       float(result["test_score"].mean())))
    # Separate leakage illustration: test values do not determine the imputation mean.
    imputer = SimpleImputer(strategy="mean").fit([[20.0], [40.0], [np.nan]])
    held_out = imputer.transform([[100.0], [np.nan]])
    # Illustrative imbalanced classifier, not a real churn dataset.
    Xc, yc = make_classification(n_samples=600, n_features=10,
                                 weights=[0.85, 0.15], random_state=7)
    Xct, Xce, yct, yce = train_test_split(
        Xc, yc, test_size=0.25, random_state=7, stratify=yc)
    Xct = Xct.copy()
    Xce = Xce.copy()
    Xct[::13, 0] = np.nan
    Xce[::11, 0] = np.nan
    pipeline = make_pipeline(SimpleImputer(strategy="median"),
                             StandardScaler(),
                             LogisticRegression(max_iter=1000, random_state=0))
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)
    # All preprocessing is refitted inside each CV training fold.
    protocol = cross_validate(pipeline, Xct, yct, cv=cv,
                              scoring=["average_precision", "recall", "f1"])
    # No hyperparameters/threshold are selected from final test performance here.
    pipeline.fit(Xct, yct)
    from sklearn.metrics import average_precision_score, confusion_matrix
    final_ap = average_precision_score(yce, pipeline.predict_proba(Xce)[:, 1])
    final_cm = confusion_matrix(yce, pipeline.predict(Xce), labels=[0, 1])
    return dict(train=tree.score(Xtr, ytr), test=tree.score(Xte, yte),
                source_scores=source_scores, depths=depths, curves=np.array(curves),
                imputer_mean=imputer.statistics_[0], held_out=held_out,
                protocol=protocol, final_ap=final_ap, final_cm=final_cm,
                train_size=len(ytr), test_size=len(yte))

def make_plot(results, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    plt.rcParams["svg.fonttype"] = "none"
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), layout="constrained")
    ax = axes[0]
    ax.bar(["Train", "Held-out test"], [results["train"], results["test"]],
           color=["#2878b5", "#e07a20"])
    ax.set_ylim(0, 1.13)
    ax.set_ylabel("Accuracy")
    ax.set_title("Seeded unrestricted tree")
    for i, v in enumerate([results["train"], results["test"]]):
        ax.text(i, v + .025, f"{v:.3f}", ha="center")
    ax = axes[1]
    ax.plot(range(5), results["curves"][:, 0], "o-", label="CV training mean")
    ax.plot(range(5), results["curves"][:, 1], "s-", label="CV validation mean")
    ax.set_xticks(range(5), ["1", "2", "4", "8", "Unlimited"])
    ax.set_xlabel("Maximum tree depth")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(.65, 1.03)
    ax.set_title("Depth diagnostic: development data only")
    ax.legend(loc="lower right", fontsize=9)
    ax = axes[2]
    matrix = np.zeros((5, 5))
    np.fill_diagonal(matrix, 1)
    ax.imshow(matrix, cmap=ListedColormap(["#cfe3f1", "#e07a20"]), vmin=0, vmax=1)
    for i in range(5):
        for j in range(5):
            ax.text(j, i, "Validate" if i == j else "Train", ha="center", va="center",
                    fontsize=9)
    ax.set_xticks(range(5), [f"Fold {i+1}" for i in range(5)])
    ax.set_yticks(range(5), [f"Fit {i+1}" for i in range(5)])
    ax.set_title("Five-fold rotation (schematic)")
    fig.suptitle("Generalisation: held-out scores, complexity, and fold rotation", fontsize=15)
    fig.savefig(output)
    fig.savefig(output.with_suffix(".png"), dpi=130)
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    with threadpool_limits(limits=1):
        result = run_examples()
    for key in ["train", "test", "source_scores", "curves", "imputer_mean",
                "held_out", "final_ap", "final_cm"]:
        print(key, result[key])
    scores = result["source_scores"]
    print("CV mean / population std:", scores.mean(), scores.std(ddof=0))
    print("Protocol CV average precision:",
          result["protocol"]["test_average_precision"].mean())
    if args.plot:
        make_plot(result, Path(__file__).with_name("lesson03-generalisation.svg"))

if __name__ == "__main__":
    main()
