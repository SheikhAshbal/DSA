"""Reproduce the lesson's paired correlations and optional relationship plots."""
import argparse
from pathlib import Path

import numpy as np

NAMES = ["hours", "score", "absences", "shoe"]
DATA = np.array([
    [1, 50, 8, 7], [2, 55, 6, 9], [3, 61, 5, 6],
    [4, 67, 3, 10], [5, 72, 2, 8], [6, 80, 1, 7],
], dtype=float)
X_CURVE = np.arange(-3, 4, dtype=float)
Y_CURVE = X_CURVE ** 2


def pearson(x, y):
    """Require paired finite vectors; do not silently drop missing records."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) < 2:
        raise ValueError("Need equally sized 1-D paired inputs with at least two rows.")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Choose an explicit missing/invalid-data policy first.")
    if np.ptp(x) == 0 or np.ptp(y) == 0:
        raise ValueError("Pearson correlation is undefined for a constant input.")
    return float(np.corrcoef(x, y)[0, 1])


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype": "none", "font.size": 10})
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    fig.suptitle("Correlation: direction, shape, and limits", fontsize=17)
    blue = "#2166ac"
    hours, score, absences = DATA[:, 0], DATA[:, 1], DATA[:, 2]
    ax = axes[0, 0]
    ax.scatter(hours, score, color=blue, s=65)
    ax.set(xlabel="Study hours", ylabel="Score",
           title=f"Strong positive association: r = {pearson(hours, score):+.3f}")
    ax.text(0.03, 0.95, "Six illustrative observations; no causal conclusion",
            transform=ax.transAxes, va="top", fontsize=9)
    ax = axes[0, 1]
    ax.scatter(score, absences, color=blue, s=65)
    ax.set(xlabel="Score", ylabel="Absences",
           title=f"Strong negative association: r = {pearson(score, absences):+.3f}")
    ax = axes[1, 0]
    ax.scatter(X_CURVE, Y_CURVE, color="#c85b16", s=65)
    ax.set(xlabel="x", ylabel="y = x squared",
           title=f"Exact curved relation, zero Pearson r = {pearson(X_CURVE, Y_CURVE):.2f}")
    ax = axes[1, 1]
    matrix = np.corrcoef(DATA, rowvar=False)
    picture = ax.imshow(matrix, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set(xticks=range(4), xticklabels=NAMES, yticks=range(4),
           yticklabels=NAMES, title="Pearson heatmap: scan, then inspect")
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{matrix[i, j]:+.2f}", ha="center", va="center",
                    color="white" if abs(matrix[i, j]) > 0.6 else "#111111", fontsize=9)
    fig.colorbar(picture, ax=ax, label="Pearson r", shrink=0.8)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, format="svg")
    fig.savefig(output.with_suffix(".png"), dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true", help="Requires Matplotlib")
    args = parser.parse_args()
    print(f"hours vs score: {pearson(DATA[:, 0], DATA[:, 1]):+.5f}")
    print(f"score vs absences: {pearson(DATA[:, 1], DATA[:, 2]):+.5f}")
    print(f"x vs x squared: {pearson(X_CURVE, Y_CURVE):+.5f}")
    matrix = np.corrcoef(DATA, rowvar=False)
    for name, row in zip(NAMES, matrix):
        print(name.ljust(9), " ".join(f"{value:+.2f}" for value in row))
    print("Distinct pairs among 50 variables:", 50 * 49 // 2)
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson02-correlation-plots.svg"))


if __name__ == "__main__":
    main()
