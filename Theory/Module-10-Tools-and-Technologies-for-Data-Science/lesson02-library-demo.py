"""Examples for Module X, Lesson 2: the essential scientific Python stack."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from threadpoolctl import threadpool_limits

def array_examples():
    df = pd.DataFrame({"score": [52, 63, 71, 88]})
    column = df["score"]
    # This ordinary numeric column has ndarray-backed .values.
    nullable = pd.Series([52, None, 71], dtype="Int64")
    converted = nullable.to_numpy(dtype=float, na_value=np.nan)
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    rng = np.random.default_rng(0)
    normals = rng.normal(size=1000)
    sales = pd.DataFrame({"region": ["East", "West", "East"],
                          "revenue": [100, 80, 50]})
    return dict(column_type=type(column).__name__,
                values_type=type(column.values).__name__,
                is_ndarray=isinstance(column.values, np.ndarray),
                mean=float(np.mean(column.values)),
                nullable_type=type(nullable.array).__name__,
                nullable_numpy=converted, product=a @ b, normals=normals,
                grouped=sales.groupby("region")["revenue"].sum())

def model_examples():
    # Preserve the source dataset/split. Fix the tree seed for reproducibility.
    X, y = make_classification(n_samples=200, random_state=0)
    Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
    source = []
    for model in [DecisionTreeClassifier(random_state=0),
                  KNeighborsClassifier(),
                  LogisticRegression(max_iter=1000, random_state=0)]:
        model.fit(Xtr, ytr)
        predicted = model.predict(Xte)
        source.append(dict(name=type(model).__name__,
                           score=float(model.score(Xte, yte)),
                           accuracy=float(accuracy_score(yte, predicted))))
    # Separate development-only comparison. No test scores are used for selection.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    candidates = {
        "Tree": DecisionTreeClassifier(random_state=0),
        "Scaled KNN": make_pipeline(StandardScaler(), KNeighborsClassifier()),
        "Scaled logistic": make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=1000, random_state=0)),
    }
    validation = {}
    for name, estimator in candidates.items():
        result = cross_validate(estimator, Xtr, ytr, cv=cv, scoring="accuracy")
        validation[name] = result["test_score"]
    # Demonstrate labelled tabular input to the plotting stage.
    development = pd.DataFrame(Xtr[:, :3], columns=["Feature 0", "Feature 1", "Feature 2"])
    return dict(source=source, validation=validation, development=development,
                train_size=len(ytr), test_size=len(yte))

def make_plot(arrays, models, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.rcParams["svg.fonttype"] = "none"
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), layout="constrained")
    axes[0].hist(arrays["normals"], bins=25, color="#2878b5", edgecolor="white")
    axes[0].set(title="NumPy samples → Matplotlib histogram",
                xlabel="Seeded standard-normal draw", ylabel="Count")
    sns.heatmap(models["development"].corr(), annot=True, fmt=".2f",
                vmin=-1, vmax=1, center=0, cmap="vlag", square=True, ax=axes[1],
                cbar_kws={"label": "Pearson r", "shrink": .7})
    # Seaborn created the chart; Matplotlib adjusts labels and tick layout.
    axes[1].set_title("pandas correlation → seaborn heatmap")
    axes[1].tick_params(axis="x", labelrotation=35)
    names = list(models["validation"])
    values = np.array([models["validation"][name] for name in names])
    axes[2].bar(names, values.mean(axis=1), color=["#2878b5", "#e07a20", "#40947d"])
    axes[2].set(ylim=(0, 1.1), ylabel="Accuracy",
                title="Development CV: same folds / metric")
    axes[2].tick_params(axis="x", labelrotation=25)
    for i, value in enumerate(values.mean(axis=1)):
        axes[2].text(i, value+.025, f"{value:.3f}", ha="center")
    fig.suptitle("The essential library stack: arrays, tables, plots, and models", fontsize=15)
    fig.savefig(output)
    fig.savefig(output.with_suffix(".png"), dpi=130)
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    with threadpool_limits(limits=1):
        arrays = array_examples()
        models = model_examples()
    for key in ["column_type", "values_type", "is_ndarray", "mean",
                "nullable_type", "nullable_numpy", "product", "grouped"]:
        print(key, arrays[key])
    print("Source-style held-out classifier scores:", models["source"])
    for name, scores in models["validation"].items():
        print(name, "development fold scores:", scores,
              "mean:", scores.mean(), "std:", scores.std(ddof=0))
    if args.plot:
        make_plot(arrays, models, Path(__file__).with_name("lesson02-library-stack.svg"))

if __name__ == "__main__":
    main()
