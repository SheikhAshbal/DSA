"""Draw six plot types and two standalone Seaborn examples using offline fixtures."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

COURSES = ["Data Science", "Security", "SQL"]
BATCHES = ["A", "B", "C"]
BINS = np.arange(40, 101, 10)


def fixtures():
    students = pd.DataFrame({
        "batch": ["A"] * 4 + ["B"] * 4 + ["C"] * 4,
        "course": ["Data Science"] * 5 + ["Security"] * 4 + ["SQL"] * 3,
        "hours": [1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6],
        "score": [48, 56, 64, 72, 62, 70, 78, 86, 74, 82, 90, 98],
        "absences": [7, 5, 5, 4, 5, 4, 2, 3, 4, 2, 2, 1],
    })
    weekly = pd.DataFrame({"week": [1, 2, 3, 4, 5, 6],
                           "logins": [10, 14, 12, 18, 20, 24]})
    return students, weekly


def plotting_tools():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({"svg.fonttype": "none", "font.size": 10})
    return plt, sns


def make_gallery():
    plt, sns = plotting_tools()
    students, weekly = fixtures()
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), layout="constrained")
    fig.suptitle("Synthetic portal examples: match the plot to the question", fontsize=17)
    blue = "#2166ac"

    sns.histplot(data=students, x="score", bins=BINS, color=blue, ax=axes[0, 0])
    axes[0, 0].set(title="1. Score distribution: histogram", xlabel="Score (10-point bins)", ylabel="Count")

    sns.countplot(data=students, x="course", order=COURSES, color=blue, ax=axes[0, 1])
    axes[0, 1].set(title="2. Enrolments per course: bar chart", xlabel="Course", ylabel="Count", ylim=(0, 6))
    for container in axes[0, 1].containers:
        axes[0, 1].bar_label(container, padding=3)

    sns.lineplot(data=weekly, x="week", y="logins", marker="o",
                 errorbar=None, color=blue, ax=axes[0, 2])
    axes[0, 2].set(title="3. Weekly logins: line chart", xlabel="Week", ylabel="Logins", xticks=weekly["week"])

    sns.scatterplot(data=students, x="hours", y="score", color=blue, s=55, ax=axes[1, 0])
    axes[1, 0].set(title="4. Hours and score: scatter plot", xlabel="Study hours", ylabel="Score")

    sns.boxplot(data=students, x="batch", y="score", order=BATCHES,
                color="#b9d5ed", ax=axes[1, 1])
    sns.stripplot(data=students, x="batch", y="score", order=BATCHES,
                  jitter=False, color="#222222", size=4, ax=axes[1, 1])
    axes[1, 1].set(title="5. Score by batch: box plot", xlabel="Batch (4 records each)", ylabel="Score")

    matrix = students[["hours", "score", "absences"]].corr(method="pearson")
    sns.heatmap(matrix, vmin=-1, vmax=1, center=0, cmap="RdBu_r",
                annot=True, fmt=".2f", square=True,
                cbar_kws={"label": "Pearson r", "shrink": 0.7}, ax=axes[1, 2])
    axes[1, 2].set_title("6. Linear associations: heatmap")
    return fig, axes


def save_examples(output_dir):
    plt, sns = plotting_tools()
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, _ = make_gallery()
    fig.savefig(output_dir / "lesson02-plot-gallery.svg", format="svg")
    fig.savefig(output_dir / "lesson02-plot-gallery.png", dpi=120)
    plt.close(fig)

    students, _ = fixtures()
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    sns.histplot(data=students, x="score", bins=BINS, ax=ax, color="#2166ac")
    ax.set(title="Synthetic student scores", xlabel="Score", ylabel="Count")
    fig.savefig(output_dir / "hist.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    sns.boxplot(data=students, x="batch", y="score", order=BATCHES, ax=ax, color="#b9d5ed")
    sns.stripplot(data=students, x="batch", y="score", order=BATCHES, ax=ax,
                  jitter=False, color="#222222", size=4)
    ax.set(title="Synthetic scores by batch", xlabel="Batch", ylabel="Score", ylim=(0, 100))
    fig.savefig(output_dir / "box.png", dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    save_examples(args.output_dir)
    students, _ = fixtures()
    print("Records:", len(students))
    print("Course counts:", students["course"].value_counts().reindex(COURSES).to_dict())
    print("Saved lesson02-plot-gallery.svg, lesson02-plot-gallery.png, hist.png, and box.png")


if __name__ == "__main__":
    main()
