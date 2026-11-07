# Module VIII: Review of Probability and Statistics

[Back to Theory](../README.md)

This module reviews probability, sampling, uncertainty, hypothesis testing, and simple regression. All three lessons are documented below.

## Lessons

| Lesson | Topic | Repository material |
| --- | --- | --- |
| 1 | [Probability Fundamentals and Key Distributions](./Lesson-01-Probability-Fundamentals-and-Key-Distributions.md) | Notes, five worked practice steps, five suggested theory answers, tested Python calculations, and distribution plots |
| 2 | [Sampling, the Central Limit Theorem and Confidence Intervals](./Lesson-02-Sampling-CLT-and-Confidence-Intervals.md) | Notes, five worked practice steps, five suggested theory answers, tested simulations, and plots |
| 3 | [Hypothesis Testing, and Linear Regression](./Lesson-03-Hypothesis-Testing-and-Linear-Regression.md) | Notes, five worked practice steps, five suggested theory answers, tested simulations, and plots |

## Learning objectives

- Apply probability rules with stated assumptions.
- Distinguish conditional probabilities and independence.
- Explain base-rate effects.
- Match normal, binomial, and Poisson models to a generating process.
- Interpret normal coverage and outlier flags.
- Distinguish sampling bias from random variation.
- Explain the CLT, standard errors, and confidence-interval coverage.
- Formulate hypotheses and interpret p-values without common reversals.
- Explain multiplicity and interpret regression coefficients and fit.

## Reproducible examples

Run [lesson01-probability-demo.py](./lesson01-probability-demo.py) for exact-count calculations and a seeded normal simulation. Add --plot to regenerate the [distribution figure](./lesson01-distributions.svg), using the version in [lesson01-requirements.txt](./lesson01-requirements.txt).

Run [lesson02-sampling-demo.py](./lesson02-sampling-demo.py) for the CLT and known-sigma interval simulations. Add --plot to regenerate the [sampling figure](./lesson02-sampling-plots.svg). The plotting dependency is shared with Lesson 1.

Run [lesson03-testing-regression-demo.py](./lesson03-testing-regression-demo.py) for calibrated null-test simulations and an OLS fit. Add --plot for the [testing and regression figure](./lesson03-testing-regression-plots.svg). Dependencies are in [lesson03-requirements.txt](./lesson03-requirements.txt).

Repository availability describes documented material, not course grades or submission status.
