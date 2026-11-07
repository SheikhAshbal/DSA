"""Calculate axis-truncation examples and optionally regenerate the figure."""
import argparse
import math
from pathlib import Path


def visible_length_ratio(larger, smaller, baseline=0):
    if not all(math.isfinite(value) for value in (larger, smaller, baseline)):
        raise ValueError("Values and baseline must be finite.")
    if not baseline < smaller <= larger:
        raise ValueError("This demonstration needs baseline < smaller <= larger.")
    return (larger - baseline) / (smaller - baseline)


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype": "none", "font.size": 10})
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.8), layout="constrained")
    fig.suptitle("The same values (100 and 102), three different baselines", fontsize=16)
    configurations = [
        (0, 108, "#2166ac", "Zero baseline", [0, 25, 50, 75, 100]),
        (90, 104, "#c85b16", "Warning: truncated at 90", [90, 92, 94, 96, 98, 100, 102, 104]),
        (99, 103.2, "#c85b16", "Warning: truncated at 99", [99, 100, 101, 102, 103]),
    ]
    for ax, (base, top, colour, title, ticks) in zip(axes, configurations):
        values = [100, 102]
        ax.bar(["A", "B"], [value-base for value in values],
               bottom=base, color=colour, width=0.55)
        ax.set(ylim=(base, top), yticks=ticks, ylabel="Value (illustrative units)", title=title)
        for x, value in enumerate(values):
            ax.text(x, value + (top-base)*0.012, str(value), ha="center", va="bottom")
        ratio = visible_length_ratio(102, 100, base)
        ax.set_xlabel(f"Displayed length B / A = {ratio:.2f}")
        ax.spines[["top", "right"]].set_visible(False)
        ax.yaxis.grid(True, color="#dddddd", linewidth=0.6)
        ax.set_axisbelow(True)
    fig.savefig(output, format="svg")
    fig.savefig(output.with_suffix(".png"), dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true", help="Requires Matplotlib")
    args = parser.parse_args()
    print(f"Actual increase from 100 to 102: {(102-100)/100*100:.1f}%")
    for baseline in (0, 90, 99):
        print(f"Baseline {baseline}: displayed length ratio = {visible_length_ratio(102,100,baseline):.2f}")
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson01-axis-comparison.svg"))


if __name__ == "__main__":
    main()
