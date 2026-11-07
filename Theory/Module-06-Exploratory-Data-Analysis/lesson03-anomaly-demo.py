"""Reproduce the lesson's IQR and z-score examples; no records are deleted."""
import argparse
from pathlib import Path
import numpy as np

VALUES = np.array([12, 13, 14, 15, 16, 15, 14, 13, 200, 12, 15, -5], dtype=float)
MASKING = np.array([10, 11, 12, 13, 14, 12, 11, 10, 13, 500], dtype=float)


def finite_vector(data):
    values = np.asarray(data, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("Need a nonempty one-dimensional numeric vector.")
    if not np.isfinite(values).all():
        raise ValueError("Handle missing and nonfinite values under an explicit policy.")
    return values


def iqr_flags(data, factor=1.5):
    values = finite_vector(data)
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("The IQR factor must be finite and nonnegative.")
    q1, q3 = np.percentile(values, [25, 75], method="linear")
    iqr = q3 - q1
    lower, upper = q1 - factor * iqr, q3 + factor * iqr
    return {
        "q1": float(q1), "q3": float(q3), "iqr": float(iqr),
        "lower": float(lower), "upper": float(upper),
        "mask": (values < lower) | (values > upper),
    }


def z_flags(data, threshold=3.0, ddof=0):
    values = finite_vector(data)
    if ddof not in (0, 1) or len(values) <= ddof:
        raise ValueError("Use ddof=0 or 1 with enough observations.")
    if not np.isfinite(threshold) or threshold <= 0:
        raise ValueError("The z threshold must be finite and positive.")
    std = float(values.std(ddof=ddof))
    if std == 0:
        raise ValueError("Z-scores are undefined when standard deviation is zero.")
    mean = float(values.mean())
    z = (values - mean) / std
    return {"mean": mean, "std": std, "z": z, "mask": np.abs(z) > threshold}


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype": "none", "font.size": 10})
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), layout="constrained")
    fig.suptitle("Anomaly flags are questions, not deletion instructions", fontsize=16)
    ax = axes[0]
    ax.boxplot(VALUES, orientation="horizontal", whis=1.5, patch_artist=True,
               boxprops={"facecolor": "#b9d5ed"},
               medianprops={"color": "#111111", "linewidth": 2})
    ax.set(xlabel="Value", yticks=[], title="IQR flags: -5 and 200")
    ax.text(0.02, 0.93, "Linear quartiles: Q1=12.75; Q3=15\nFences: 9.375 and 18.375",
            transform=ax.transAxes, va="top", fontsize=9)
    ax = axes[1]
    z = z_flags(MASKING)["z"]
    ax.scatter(np.arange(1, 10), z[:-1], color="#2166ac", s=50)
    ax.scatter([10], [z[-1]], color="#c85b16", s=70, zorder=3)
    ax.axhline(3, color="#555555", linestyle="--", label="Strict flag: |z| > 3")
    ax.axhline(-3, color="#555555", linestyle="--")
    ax.set(xlabel="Observation index", ylabel="Population-standardised z-score",
           ylim=(-3.6, 3.6), xlim=(0.5, 10.5),
           title="500 inflates its own reference spread")
    ax.annotate(f"500: z={z[-1]:.6f}\nBelow 3, despite rounding to 3.00",
                xy=(10, z[-1]), xytext=(4.2, 1.6),
                arrowprops={"arrowstyle": "->", "color": "#555555"}, fontsize=9)
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, format="svg")
    fig.savefig(output.with_suffix(".png"), dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true", help="Requires Matplotlib")
    args = parser.parse_args()
    flags = iqr_flags(VALUES)
    print(f"IQR fences: [{flags['lower']:.3f}, {flags['upper']:.3f}]")
    print("IQR flags:", VALUES[flags["mask"]].tolist())
    for ddof, label in [(0, "population"), (1, "sample")]:
        result = z_flags(MASKING, ddof=ddof)
        print(f"{label}: mean={result['mean']:.1f}; SD={result['std']:.5f}; z(500)={result['z'][-1]:.6f}")
        print("z flags:", MASKING[result["mask"]].tolist())
    other = iqr_flags(MASKING)
    print("IQR flags for masking example:", MASKING[other["mask"]].tolist())
    print("Task 5: IQR=30; lower=-25; upper=95; 85 is not outside.")
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson03-anomaly-plots.svg"))


if __name__ == "__main__":
    main()
