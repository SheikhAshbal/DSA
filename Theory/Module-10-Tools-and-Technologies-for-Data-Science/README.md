# Module X: Tools and Technologies for Data Science

[Back to Theory](../README.md)

This module introduces tools and working practices used in data science. All three lessons are documented below.

## Lessons

| Lesson | Topic | Repository material |
| --- | --- | --- |
| 1 | [Python as the Language of Data Science](./Lesson-01-Python-as-the-Language-of-Data-Science.md) | Notes, five worked practice steps, five suggested theory answers, a tested script, and a clean notebook |
| 2 | [The Essential Library Stack](./Lesson-02-The-Essential-Library-Stack.md) | Notes, five worked practice steps, five suggested theory answers, tested library examples, and a figure |
| 3 | [Cloud Notebooks: Colab, Kaggle and Reproducibility](./Lesson-03-Cloud-Notebooks-Colab-Kaggle-and-Reproducibility.md) | Notes, five worked practice steps, five suggested theory answers, and a tested local checkpoint/resume simulation |

## Learning objectives

- Explain Python's readability, ecosystem, and integration role.
- Distinguish dynamic typing, the interpreter, and the standard library.
- Choose notebooks, scripts, and modules for appropriate tasks.
- Recognise hidden state and apply reproducible execution practices.
- Choose NumPy, pandas, Matplotlib, seaborn, and scikit-learn for suitable tasks.
- Explain interoperability and compare classifiers with appropriate preprocessing.

- Distinguish runtime-local state from verified persistent artifacts.
- Record environment requirements and plan responsible cloud workflows.

## Reproducible examples

Run [lesson01-python-demo.py](./lesson01-python-demo.py) for runtime input errors and simulated notebook execution histories. Open [lesson01-execution-order.ipynb](./lesson01-execution-order.ipynb) in a Jupyter-compatible environment for the clean linear example.

[lesson01-requirements.txt](./lesson01-requirements.txt) records the tested data-library versions. Notebook interface software is a separate optional requirement. Examples use a small synthetic table and no external data.

Run [lesson02-library-demo.py](./lesson02-library-demo.py) for array, table, classifier, and development-CV examples. Add --plot to regenerate the [library-stack figure](./lesson02-library-stack.svg). Its broader dependency set is recorded in [lesson02-requirements.txt](./lesson02-requirements.txt).

Run [lesson03-checkpoint-demo.py](./lesson03-checkpoint-demo.py) with --output-dir lesson03-demo-output for a standard-library-only checkpoint/resume simulation. It needs no cloud account and was tested with Python 3.12.14.

Repository availability describes documented material, not course grades or submission status.
