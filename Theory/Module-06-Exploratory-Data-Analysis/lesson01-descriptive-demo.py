"""Verify the lesson's summaries; optionally generate the four-panel visual."""
import argparse
from pathlib import Path
import statistics as st

import numpy as np

SCORES = [68, 70, 71, 69, 72, 70]
TIGHT = [68, 69, 70, 71, 72]
WIDE = [40, 55, 70, 85, 100]
SKEWED = [12, 15, 18, 20, 22, 25, 28, 35, 60, 95]
A = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
B = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]


def five_number(data):
    if not data:
        raise ValueError("At least one observation is required.")
    return np.percentile(data, [0, 25, 50, 75, 100], method="linear").tolist()


def describe(data):
    minimum, q1, median, q3, maximum = five_number(data)
    return {
        "n": len(data), "mean": st.mean(data), "median": median,
        "modes": st.multimode(data), "population_sd": st.pstdev(data),
        "sample_sd": st.stdev(data) if len(data) > 1 else None,
        "range": maximum - minimum, "IQR": q3 - q1,
        "five_number": [minimum, q1, median, q3, maximum],
    }


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams.update({"svg.fonttype": "none", "font.size": 10})
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), layout="constrained")
    fig.suptitle("Descriptive statistics: look beyond the average", fontsize=17)
    blue, orange = "#2166ac", "#c85b16"

    ax = axes[0, 0]
    ax.scatter(TIGHT, [1] * len(TIGHT), color=blue, s=55, label="Tight")
    ax.scatter(WIDE, [0] * len(WIDE), color=orange, s=55, label="Wide")
    ax.axvline(70, color="#777777", linestyle="--", linewidth=1)
    ax.set(yticks=[0, 1], yticklabels=["Wide", "Tight"], ylim=(-0.5, 1.5),
           xlim=(35, 105), xlabel="Score", title="Same mean (70), different spread")
    ax.text(0.02, 0.95, "Population SD: tight 1.41; wide 21.21",
            transform=ax.transAxes, va="top", fontsize=9)

    ax = axes[0, 1]
    ax.hist([A, B], bins=np.arange(3.5, 20.5, 1), histtype="step",
            linewidth=2, color=[blue, orange], label=["A: spread out", "B: repeated 8s"])
    ax.set(xlabel="Value", ylabel="Frequency", title="Same mean (9) and population SD (3.16)")
    ax.legend(frameon=False, fontsize=9)

    ax = axes[1, 0]
    ax.hist(SKEWED, bins=np.arange(0, 101, 10), color=blue, edgecolor="white")
    ax.set(xlabel="Value (10-unit bins)", ylabel="Frequency",
           title="Histogram: upper tail and gaps")

    ax = axes[1, 1]
    ax.boxplot(SKEWED, orientation="horizontal", whis=1.5,
               patch_artist=True, boxprops={"facecolor": "#b9d5ed"},
               medianprops={"color": "#111111", "linewidth": 2})
    ax.set(xlabel="Value", yticks=[], title="Box plot: 1.5 x IQR convention", xlim=(0, 105))
    ax.text(0.02, 0.95, "Q1 18.5 | median 23.5 | Q3 33.25\nWhiskers: 12 to 35; flagged: 60, 95",
            transform=ax.transAxes, va="top", fontsize=9)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, format="svg")
    fig.savefig(output.with_suffix(".png"), dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true", help="Requires Matplotlib")
    args = parser.parse_args()
    for name, data in [
        ("scores", SCORES), ("with low outlier", SCORES + [5]),
        ("tight", TIGHT), ("wide", WIDE),
        ("skewed", SKEWED), ("A", A), ("B", B),
    ]:
        print(name, describe(data))
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson01-summary-plots.svg"))


if __name__ == "__main__":
    main()
