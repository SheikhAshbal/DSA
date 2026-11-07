"""Demonstrate finite-variance sample means and known-sigma confidence intervals."""
import argparse
import math
from pathlib import Path
import random
import statistics as st

SOURCE_MEAN = 15.0
# randint(50,100) includes 51 integers: variance (51^2 - 1) / 12.
SOURCE_VARIANCE = (1/5) * ((51**2-1)/12 + 75**2) - SOURCE_MEAN**2
SOURCE_SD = math.sqrt(SOURCE_VARIANCE)
Z95 = st.NormalDist().inv_cdf(0.975)


def draw(rng):
    return 0 if rng.random() < 0.8 else rng.randint(50,100)


def sample_means(n=40, repeats=2000, seed=1):
    if not isinstance(n,int) or n <= 0 or not isinstance(repeats,int) or repeats <= 0:
        raise ValueError("Sample size and repetitions must be positive integers.")
    rng = random.Random(seed)
    return [st.mean(draw(rng) for _ in range(n)) for _ in range(repeats)]


def known_sigma_ci(sample_mean, sigma, n):
    if not isinstance(n,int) or n <= 0:
        raise ValueError("Sample size must be a positive integer.")
    if not math.isfinite(sample_mean) or not math.isfinite(sigma) or sigma <= 0:
        raise ValueError("Use a finite mean and positive finite known sigma.")
    margin = Z95 * sigma / math.sqrt(n)
    return sample_mean-margin, sample_mean+margin


def normal_intervals(n=25, repeats=2000, seed=3):
    if not isinstance(repeats,int) or repeats <= 0:
        raise ValueError("Repetitions must be a positive integer.")
    known_sigma_ci(70,10,n)
    rng = random.Random(seed)
    results = []
    for _ in range(repeats):
        mean = st.mean(rng.gauss(70,10) for _ in range(n))
        low, high = known_sigma_ci(mean,10,n)
        results.append((mean,low,high))
    return results


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype":"none","font.size":10})
    fig, axes = plt.subplots(2,2,figsize=(12,8),layout="constrained")
    fig.suptitle("Sampling distributions and uncertainty: four different views",fontsize=16)
    rng = random.Random(4)
    raw = [draw(rng) for _ in range(10000)]
    axes[0,0].hist(raw,bins=[-0.5 + 5*i for i in range(22)],color="#2166ac",edgecolor="white")
    axes[0,0].set(title="Raw observations: many zeros",xlabel="Value (5-unit bins)",ylabel="Count")

    means = sample_means()
    ax = axes[0,1]
    ax.hist(means,bins=25,density=True,color="#b9d5ed",edgecolor="white",label="2,000 sample means")
    se = SOURCE_SD/math.sqrt(40)
    grid = [i/10 for i in range(351)]
    density = [st.NormalDist(SOURCE_MEAN,se).pdf(x) for x in grid]
    ax.plot(grid,density,color="#c85b16",label="Normal approximation")
    ax.set(title="Mean of 40 draws: approximately bell-shaped",xlabel="Sample mean",ylabel="Density")
    ax.legend(frameon=False,fontsize=8)

    ax = axes[1,0]
    ns = [25,100,400]
    widths = [known_sigma_ci(70,10,n)[1]-known_sigma_ci(70,10,n)[0] for n in ns]
    ax.plot(ns,widths,marker="o",color="#2166ac")
    for n,width in zip(ns,widths):
        ax.annotate(f"{width:.2f}",(n,width),xytext=((-30 if n == 400 else 4),5),textcoords="offset points")
    ax.set(title="Known sigma 10: four times n, half the width",xlabel="Sample size n",ylabel="95% interval width",xticks=ns,ylim=(0,9))

    ax = axes[1,1]
    intervals = normal_intervals()
    shown = intervals[:50]
    for i,(mean,low,high) in enumerate(shown,1):
        colour = "#2166ac" if low <= 70 <= high else "#c85b16"
        ax.plot([low,high],[i,i],color=colour,linewidth=1)
    ax.axvline(70,color="#111111",linestyle="--",label="True mean 70")
    hits = sum(low <= 70 <= high for _,low,high in shown)
    ax.set(title=f"50 repeated intervals: {hits}/50 contain 70",xlabel="Population-mean interval (known sigma)",ylabel="Repetition")
    ax.legend(frameon=False,fontsize=8,loc="upper left")
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,format="svg")
    fig.savefig(output.with_suffix(".png"),dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot",action="store_true",help="Requires Matplotlib")
    args = parser.parse_args()
    means = sample_means()
    print(f"True source mean: {SOURCE_MEAN:.2f}; source SD: {SOURCE_SD:.5f}")
    print(f"Mean of sample means: {st.mean(means):.2f}")
    print(f"Empirical SD of means: {st.pstdev(means):.2f}")
    print(f"Theoretical SE at n=40: {SOURCE_SD/math.sqrt(40):.5f}")
    for n in (25,100,400):
        low,high = known_sigma_ci(70,10,n)
        print(f"Known-sigma width, n={n}: {high-low:.2f}")
    intervals = normal_intervals()
    rate = sum(low <= 70 <= high for _,low,high in intervals)/len(intervals)
    print(f"Repeated normal-sample interval coverage: {rate:.1%}")
    print("60-of-400 exercise: CI endpoints cannot be computed from n and mean alone.")
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson02-sampling-plots.svg"))


if __name__ == "__main__":
    main()
