"""Verify probability examples and optionally draw three theoretical distributions."""
import argparse
from fractions import Fraction
import math
from pathlib import Path
import random


def valid_probability(p):
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError("Probability must be finite and between zero and one.")


def at_least_one(n, p):
    if not isinstance(n, int) or n < 0:
        raise ValueError("Trial count must be a nonnegative integer.")
    valid_probability(p)
    return 1 - (1 - p) ** n


def binomial_pmf(k, n, p):
    if not isinstance(n, int) or n < 0 or not isinstance(k, int):
        raise ValueError("Use an integer k and nonnegative integer n.")
    valid_probability(p)
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def poisson_pmf(k, expected_count):
    if not isinstance(k, int) or not math.isfinite(expected_count) or expected_count < 0:
        raise ValueError("Use an integer k and a finite nonnegative expected count.")
    if k < 0:
        return 0.0
    return math.exp(-expected_count) * expected_count ** k / math.factorial(k)


def normal_density(x, mu, sigma):
    if not all(math.isfinite(value) for value in (x, mu, sigma)) or sigma <= 0:
        raise ValueError("Use finite values and positive sigma.")
    return math.exp(-0.5 * ((x-mu)/sigma) ** 2) / (sigma * math.sqrt(2*math.pi))


def normal_coverage(k):
    if not math.isfinite(k) or k < 0:
        raise ValueError("Distance in standard deviations must be finite and nonnegative.")
    return math.erf(k / math.sqrt(2))


def simulated_coverage(n=100000, seed=0):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Simulation size must be a positive integer.")
    rng = random.Random(seed)
    mu, sigma = 70, 10
    values = [rng.gauss(mu, sigma) for _ in range(n)]
    return [sum(abs(x-mu) <= k*sigma for x in values) / n for k in (1,2,3)]


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype": "none", "font.size": 10})
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), layout="constrained")
    fig.suptitle("Three probability models: continuous values and discrete counts", fontsize=16)
    x = [30 + i/10 for i in range(801)]
    density = [normal_density(value,70,10) for value in x]
    axes[0].plot(x,density,color="#2166ac")
    axes[0].fill_between(x,density,where=[60 <= value <= 80 for value in x],
                         color="#b9d5ed",label="Within 1 SD: 68.27%")
    axes[0].set(title="Normal: mean 70, SD 10",xlabel="Continuous value",ylabel="Probability density",ylim=(0,0.045))
    axes[0].legend(frameon=False,fontsize=9)
    k = list(range(21))
    axes[1].bar(k,[binomial_pmf(i,20,0.5) for i in k],color="#2166ac")
    axes[1].set(title="Binomial: n=20, p=0.5",xlabel="Success count",ylabel="Probability mass",xticks=[0,5,10,15,20])
    k = list(range(16))
    axes[2].bar(k,[poisson_pmf(i,3) for i in k],color="#2166ac")
    axes[2].set(title="Poisson: expected count 3 per interval",xlabel="Event count (displayed 0 to 15)",ylabel="Probability mass",xticks=[0,3,6,9,12,15])
    for ax in axes:
        ax.spines[["top","right"]].set_visible(False)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,format="svg")
    fig.savefig(output.with_suffix(".png"),dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot",action="store_true",help="Requires Matplotlib")
    args = parser.parse_args()
    p = Fraction(1,50)
    p_none = (1-p) ** 50
    print(f"P(no login failures): {float(p_none):.4f}")
    print(f"P(at least one): {float(1-p_none):.4f}")
    fraud_rate = Fraction(20,10000)
    posterior = Fraction(18,18+300)
    print(f"P(fraud): {float(fraud_rate):.4f}")
    print(f"P(fraud | flagged): {float(posterior):.4f}")
    print(f"P(flagged | fraud): {18/20:.4f}")
    print(f"Relative increase over base rate: {float(posterior/fraud_rate):.4f} times")
    print(f"Hypothetical P(disease | positive): {99/(99+999):.4%}")
    simulated = simulated_coverage()
    for k, value in zip((1,2,3),simulated):
        print(f"Within {k} SD: theoretical {normal_coverage(k):.4%}; simulated {value:.1%}")
    print(f"Outside 3 SD, both tails: {1-normal_coverage(3):.4%}")
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson01-distributions.svg"))


if __name__ == "__main__":
    main()
