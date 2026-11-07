# Module IX: Review of Machine Learning Basics

[Back to Theory](../README.md)

This module reviews learning tasks, core algorithms, and the reasoning needed to choose and evaluate models. All three lessons are documented below.

## Lessons

| Lesson | Topic | Repository material |
| --- | --- | --- |
| 1 | [Learning Paradigms and Core Algorithms](./Lesson-01-Learning-Paradigms-and-Core-Algorithms.md) | Notes, five worked practice steps, five suggested theory answers, tested model examples, and an illustration |
| 2 | [Evaluating Models Beyond Accuracy](./Lesson-02-Evaluating-Models-Beyond-Accuracy.md) | Notes, five worked practice steps, five suggested theory answers, tested metric calculations, and plots |
| 3 | [Overfitting, Underfitting and Cross-Validation](./Lesson-03-Overfitting-Underfitting-and-Cross-Validation.md) | Notes, five worked practice steps, five suggested theory answers, tested split/CV examples, and a figure |

## Learning objectives

- Distinguish explicit rules from learned models.
- Identify supervised classification, supervised regression, and unsupervised clustering.
- Explain linear regression, decision trees, and k-means.
- Choose simple baselines without confusing interpretability with validation.
- Read confusion matrices and evaluate imbalanced classification.
- Interpret precision, recall, F1, ROC/AUC, and threshold effects.

- Diagnose underfitting and overfitting using training and validation scores.
- Design cross-validation and prevent data leakage.

## Reproducible examples

Run [lesson01-learning-demo.py](./lesson01-learning-demo.py) to inspect learned rules, clusters, and coefficients. Add --plot to regenerate the [algorithm illustration](./lesson01-algorithm-examples.svg). Tested dependencies are recorded in [lesson01-requirements.txt](./lesson01-requirements.txt).

Run [lesson02-evaluation-demo.py](./lesson02-evaluation-demo.py) for fixed prediction and score examples. Add --plot to regenerate the [evaluation figure](./lesson02-evaluation-plots.svg), using the same dependency versions.

Run [lesson03-generalisation-demo.py](./lesson03-generalisation-demo.py) for synthetic train/test, cross-validation, and leakage-safe pipeline examples. Add --plot to regenerate the [generalisation figure](./lesson03-generalisation.svg), using the same dependencies.

These are small teaching demonstrations. Lesson 3 includes synthetic held-out results; none establishes deployment performance.

Repository availability describes documented material, not course grades or submission status.
