"""Calibrated null-test simulation and descriptive ordinary least squares."""
import argparse
import math
from pathlib import Path
import random
import statistics as st

import numpy as np

HOURS = np.array([1,2,3,4,5,6,7,8],dtype=float)
SCORES = np.array([52,58,63,71,74,80,85,88],dtype=float)


def false_positive_risk(tests,alpha=0.05):
    if not isinstance(tests,int) or tests < 0 or not math.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("Use a nonnegative integer test count and alpha in [0,1].")
    # Assumes independent tests for the family-level probability.
    return 1-(1-alpha)**tests


def null_test_pvalue(rng,n=30):
    if not isinstance(n,int) or n <= 0:
        raise ValueError("n must be a positive integer.")
    # Both groups are independent N(0,1), with sigma=1 treated as known.
    a = [rng.gauss(0,1) for _ in range(n)]
    b = [rng.gauss(0,1) for _ in range(n)]
    z = (st.mean(a)-st.mean(b))/math.sqrt(2/n)
    return math.erfc(abs(z)/math.sqrt(2))


def simulate_null_families(repeats=1000,tests=20,alpha=0.05,seed=7):
    if not isinstance(repeats,int) or repeats <= 0:
        raise ValueError("repeats must be a positive integer.")
    false_positive_risk(tests,alpha)
    rng = random.Random(seed)
    return [
        sum(null_test_pvalue(rng) < alpha for _ in range(tests))
        for _ in range(repeats)
    ]


def fit_line(x,y):
    x,y = np.asarray(x,dtype=float),np.asarray(y,dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) < 2:
        raise ValueError("Need equally sized paired one-dimensional vectors.")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Choose a missing/invalid-data policy before fitting.")
    if np.ptp(x) == 0 or np.ptp(y) == 0:
        raise ValueError("This correlation/R-squared demonstration needs nonconstant inputs.")
    slope,intercept = np.polyfit(x,y,1)
    fitted = slope*x+intercept
    residuals = y-fitted
    r = float(np.corrcoef(x,y)[0,1])
    r2 = float(1-np.sum(residuals**2)/np.sum((y-y.mean())**2))
    return {"slope":float(slope),"intercept":float(intercept),
            "fitted":fitted,"residuals":residuals,"r":r,"r2":r2}


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype":"none","font.size":10})
    fig,axes = plt.subplots(2,2,figsize=(12,8),layout="constrained")
    fig.suptitle("Hypothesis tests and regression: evidence with limits",fontsize=16)
    model = fit_line(HOURS,SCORES)
    ax = axes[0,0]
    ax.scatter(HOURS,SCORES,color="#2166ac",label="Eight teaching observations")
    ax.plot(HOURS,model["fitted"],color="#2166ac",label="OLS within observed range")
    ax.plot([8,10],[model["slope"]*8+model["intercept"],model["slope"]*10+model["intercept"]],
            color="#c85b16",linestyle="--",label="Extrapolation")
    ax.scatter([10],[model["slope"]*10+model["intercept"]],color="#c85b16",marker="x",s=60)
    ax.set(title="Fitted score = 5.25 x hours + 47.75",xlabel="Hours",ylabel="Score")
    ax.legend(frameon=False,fontsize=8)

    ax = axes[0,1]
    ax.scatter(model["fitted"],model["residuals"],color="#2166ac")
    ax.axhline(0,color="#777777",linestyle="--")
    ax.set(title=f"Residual inspection, despite R-squared = {model['r2']:.3f}",
           xlabel="Fitted score",ylabel="Observed minus fitted")

    ax = axes[1,0]
    tests = [1,5,20]
    risks = [100*false_positive_risk(k) for k in tests]
    bars = ax.bar([str(k) for k in tests],risks,color="#2166ac")
    ax.bar_label(bars,labels=[f"{p:.1f}%" for p in risks],padding=3)
    ax.set(title="Independent true-null tests at alpha 0.05",xlabel="Number of tests",ylabel="Chance of at least one false positive (%)",ylim=(0,75))

    ax = axes[1,1]
    counts = simulate_null_families()
    ax.hist(counts,bins=np.arange(-0.5,max(counts)+1.5,1),color="#2166ac",edgecolor="white")
    ax.set(title="1,000 simulated families of 20 true-null tests",xlabel="False positives in one family",ylabel="Families")
    ax.text(0.98,0.95,f"Average count: {st.mean(counts):.2f}\nFamilies with any: {sum(k>0 for k in counts)/len(counts):.1%}",
            transform=ax.transAxes,ha="right",va="top",fontsize=9)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,format="svg")
    fig.savefig(output.with_suffix(".png"),dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot",action="store_true",help="Requires Matplotlib")
    args = parser.parse_args()
    model = fit_line(HOURS,SCORES)
    print(f"OLS line: score = {model['slope']:.2f} * hours + {model['intercept']:.2f}")
    print(f"Prediction at 10 hours (extrapolation): {model['slope']*10+model['intercept']:.2f}")
    print(f"r = {model['r']:.6f}; training R-squared = {model['r2']:.6f}")
    print(f"Expected false positives in 20 calibrated tests: {20*0.05:.2f}")
    print(f"At least one, assuming independent tests: {false_positive_risk(20):.4%}")
    counts = simulate_null_families()
    print(f"Simulated mean false positives per family: {st.mean(counts):.3f}")
    print(f"Simulated families with at least one: {sum(k>0 for k in counts)/len(counts):.1%}")
    print("No regression-slope significance test or causal effect is calculated.")
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson03-testing-regression-plots.svg"))


if __name__ == "__main__":
    main()
