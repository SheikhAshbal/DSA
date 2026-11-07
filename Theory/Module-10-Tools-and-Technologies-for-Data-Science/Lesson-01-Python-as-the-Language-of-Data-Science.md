# Lesson 1: Python as the Language of Data Science

[Theory index](../README.md) · [Module overview](./README.md)

**Course:** Data Science and Analytics  
**Module X:** Tools and Technologies for Data Science  
**Estimated study time:** 45 minutes

## Learning objectives

- Explain Python's appeal through readability, libraries, and integration.
- Distinguish the interpreter, dynamic typing, and standard library.
- Describe the roles of major scientific Python tools.
- Choose notebooks or Python modules for an appropriate task.
- Explain hidden notebook state and apply a clean-run discipline.

## 1. Productivity comes from the whole workflow

Python is widely used in data science because readable code, a mature ecosystem, and integration with other systems let analysts work efficiently. It is not necessary for every operation to execute as a fast Python-level loop.

As a **glue language**, Python can coordinate file loading, databases, numerical routines, visualisation, and modelling. Many numerical library operations delegate work to compiled implementations, including C, C++, Fortran, and specialised numerical libraries.

This separates the interface an analyst writes from the implementation doing much of the computation. Calling a compiled array operation can avoid the overhead of an explicit Python loop. It does not make every Python program fast: object types, algorithm choice, memory traffic, and the particular operation still matter.

The practical question is how quickly a reliable analysis can be developed, checked, maintained, and run. Runtime remains important when it is a bottleneck. Measure the actual workload before choosing an optimisation or another language.

The source's library line counts are illustrative, unversioned estimates, not measurements reproduced here. This lesson does not rely on them or on a claim that Python is universally the best choice. R and other languages also have mature ecosystems; R is not the oldest statistical programming language.

## 2. The scientific ecosystem

| Tool | Main role | Example |
| --- | --- | --- |
| NumPy | Multidimensional numerical arrays and array operations | Vectorised arithmetic |
| pandas | Labelled tables and data preparation | Filter records, join tables, handle missing values |
| SciPy | Scientific algorithms | Optimisation and statistical routines |
| Matplotlib / seaborn | Plotting and statistical visualisation | Explain patterns with charts |
| scikit-learn | Machine-learning estimators and evaluation tools | Fit a pipeline and cross-validate |
| Jupyter | Interactive computational notebooks | Combine an explanation, code, and results |

Tools are useful together: a table can be prepared, converted into model inputs, evaluated, and plotted without rebuilding every component. Community examples and documentation reduce learning and development effort, although copied code still needs review and validation.

[NumPy's introduction](https://numpy.org/doc/stable/user/whatisnumpy.html) explains how array operations use compiled implementations. Python-level convenience and numerical runtime performance are distinct parts of the same workflow.

## 3. Interpreter, dynamic typing, and “batteries included”

### Interpreter

You can enter Python interactively or run a script through the interpreter:

```powershell
python
python lesson01-python-demo.py
```

A usual Python workflow does not require a separate manual compilation step. “Interpreted” does not mean there is no compilation internally: CPython commonly compiles source into bytecode before executing it.

### Dynamic typing

Objects have types, and names refer to objects. A name can be rebound to an object of another type. Type annotations are optional and do not by themselves enforce runtime validation.

```python
def average(values):
    return sum(values) / len(values)

print(average([2, 4, 6]))  # 4.0
average([2, 4, "6"])      # TypeError when this path executes
```

Python does not automatically convert the string "6" into a number for this sum. The function definition can succeed even though a later call fails.

Some mistakes raise an exception; others produce plausible but wrong output. For example, multiplying a string repeats it instead of performing numeric multiplication. Static type checking can help before execution, but data values, units, shapes, missingness, and domain assumptions still require checks.

### Standard library and third-party packages

“Batteries included” primarily describes Python's standard library: tools such as pathlib, csv, json, and statistics.

NumPy, pandas, and scikit-learn belong to the third-party ecosystem and are installed separately. PyPI distributes third-party packages; it is not part of the standard library. Exact package counts change and are unnecessary for this lesson.

## 4. What is a notebook?

A computational notebook combines executable cells with their outputs and explanatory text. It can show tables, figures, formulas, and the reasoning behind an analysis.

In a Python notebook, a **kernel** is the running process that executes code and holds objects in memory. The visible document and that process's current state are related, but they are not the same thing.

Notebooks support exploration because an analyst can inspect intermediate results, revise a question, and explain each step nearby. They support storytelling because prose and visual evidence can appear beside the code that produced them.

Reusable logic usually belongs in an importable .py module. A scheduled workflow often uses a script or another explicit automated entry point. Notebooks can also be executed reliably by automation when their environment, inputs, and clean execution are controlled; the file format alone does not determine reproducibility.

## 5. Hidden state and stale outputs

Cells can execute in a different order from their displayed order. An output can remain visible after the underlying data or code has changed. A variable may exist only because a deleted or previously executed cell created it.

The core habit is **restart the kernel and run all cells from top to bottom before sharing**. Inspect the outputs and save the resulting notebook.

A clean run detects dependencies on previous kernel history. It is not proof of correct statistics or complete reproducibility. Also record input data, dependency versions, relevant random seeds, file paths, and external requirements. Validate conclusions as well as successful execution.

## 6. Worked practice

### Practice 1 — Evaluate the four claims

| Claim | Lesson answer | Explanation |
| --- | --- | --- |
| Python dominates because it has the fastest numerical runtime | False | Readability, libraries, and integration explain its appeal; speed depends on the operation |
| Heavy numerical work runs in optimised C underneath | True with qualification | Many library operations use compiled code, including C/Fortran; not every operation does |
| Ecosystem matters more to productivity than raw language speed | True in the lesson's comparison | Existing reliable tools can save substantial implementation effort |
| A faster language with no data libraries necessarily makes you more productive | False | Rebuilding missing tools can outweigh execution-time gains |

The best practical choice depends on the task and available tools, rather than a language-speed ranking alone.

### Practice 2 — Observe a runtime type error

The original average function returns 4.0 for [2,4,6]. A call with [2,4,"6"] raises TypeError when sum attempts incompatible addition.

Fast iteration is useful, but it must be paired with clear input expectations and validation. Invalid types can either stop an analysis or corrupt its meaning, connecting this example to “garbage in, garbage out”.

The companion script also defines validated_average. It rejects an empty iterable, strings, boolean values, and non-finite numbers. This example deliberately requires finite real numbers; other applications may define different valid inputs.

Do not silently coerce a malformed value just to make an error disappear. Decide what the value means, document any conversion, and check the result.

### Practice 3 — Reproduce the out-of-order trap

The displayed order is A, B, C, D:

```python
# A
df = load_data()

# B
df = df[df.age > 18]

# C
print(df.shape)

# D
print(df.shape)
```

The historical execution order is A, C, B, D. Cell C prints the original table's shape before filtering; Cell D prints the filtered shape.

Using the companion's five-row fixture:

| Execution history | Cell C output | Cell D output |
| --- | --- | --- |
| A → C → B → D | (5, 2) | (3, 2) |
| Fresh A → B → C → D | (3, 2) | (3, 2) |

In the clean run, **C changes**, because B runs before C in the displayed order. D still prints the filtered shape.

The source's parenthetical explanation says C would remain before B; that contradicts the displayed A–B–C–D order. The corrected reasoning above follows the actual cell positions.

The condition age > 18 excludes age 18. If the intended rule includes people aged 18, use age >= 18 and check the resulting counts. The demonstration preserves the supplied strict comparison.

Restarting and running all cells makes the visible execution history agree with a linear reading. Another person should not need the author's private kernel history to reconstruct a result.

### Practice 4 — Choose the right medium

| Task | Usual choice | Reason |
| --- | --- | --- |
| First exploration with charts and notes | Notebook | Inspect intermediate results and explain questions |
| Cleaning function imported by three projects | .py module | Share and test one reusable implementation |
| Nightly retraining job | Script / automated entry point | Make inputs, execution order, and failures explicit |
| Tutorial explaining an analysis | Notebook | Put prose, code, and output together |
| Team's core library | .py modules | Provide a maintainable importable interface |

A notebook used for scheduling becomes risky when it depends on interactive state, manual edits, or unrecorded inputs. Controlled notebook execution can also be automated, but a reusable module keeps shared business logic easier to maintain.

### Practice 5 — State the discipline

1. Python offers readable syntax and a mature ecosystem, and it integrates with fast compiled routines.
2. Dynamic typing allows quick experimentation, but incompatible values may fail only when the affected code runs. Validate data and test important assumptions.
3. Restart the kernel and run all notebook cells in order before trusting or sharing their outputs. This exposes dependencies on hidden execution history.
4. Put settled reusable logic in .py modules and import it from notebooks or automated jobs.

The course's honesty theme applies here: results should follow from recorded inputs and visible executable steps, rather than an undocumented interactive session.

## 7. Run the examples

The [Python demo](./lesson01-python-demo.py) reproduces the average error and both cell histories. The [notebook](./lesson01-execution-order.ipynb) provides the clean linear version with a synthetic table.

From this directory:

```powershell
python -m pip install -r lesson01-requirements.txt
python lesson01-python-demo.py
```

[Recorded dependencies](./lesson01-requirements.txt) were tested with Python 3.12.14, NumPy 2.3.5, and pandas 3.0.1. A notebook interface and compatible Python kernel are separate optional requirements; open the .ipynb in an existing Jupyter-compatible environment.

The notebook is committed with cleared outputs and execution counts. Its code cells were checked in order in a fresh Python namespace. This checks Python execution and expected outputs; it does not claim an interactive browser/kernel integration test.

## 8. Theory exercises — suggested answers

Use these as study references and explain the reasoning in your own words for course submissions.

### Task 1 — Python's dominance vs. speed

Python is popular in data science because its readable syntax helps analysts express ideas quickly, and its libraries cover much of the analysis workflow. It acts as glue between data sources, tools, and numerical routines.

Many expensive numerical operations are performed by optimised compiled implementations beneath the Python interface. This combines convenient code with efficient library operations, even though Python-level execution is not always the fastest.

### Task 2 — Ecosystem vs. raw performance

Raw performance affects how long a computation takes, while an ecosystem affects how much work is needed to build, check, and maintain the whole solution.

For many data-science tasks, libraries and community documentation contribute more to productivity because analysts can use established tools instead of reimplementing them. Runtime still matters for expensive workloads, so the choice should consider development effort and measured execution needs together.

### Task 3 — Dynamic typing risks

Python lets programmers write code without mandatory type declarations, making experimentation quick. However, incompatible inputs can remain unnoticed until the affected code executes, and some incorrect operations can produce plausible results.

Reduce these risks with clear functions, input and schema validation, tests for important cases, and optional type annotations and static checking. Check data meaning, units, shapes, and missing values as well as Python types.

### Task 4 — Notebooks for exploration

A notebook is a computational document containing executable code cells, their outputs, and explanatory text. It can place tables, charts, formulas, and interpretation together.

This makes it useful for exploration because intermediate results are easy to inspect and revise. It supports storytelling by presenting the question, method, evidence, and conclusion in one readable sequence.

### Task 5 — Notebook reproducibility analysis

A notebook's kernel retains variables between cell executions. If cells run out of order, or code changes without rerunning dependent cells, visible outputs can reflect an earlier state rather than the displayed analysis.

Before sharing, restart the kernel and run every cell from top to bottom, inspect the outputs, and save the notebook. Also record inputs and dependencies so others can reproduce that clean run. Move settled reusable logic into importable modules.

## 9. Quick revision

- Readability, libraries, and integration drive Python's practical appeal.
- Many numerical operations execute in compiled libraries.
- Dynamic typing does not mean objects have no types.
- Optional annotations alone do not validate runtime values.
- Standard-library batteries and third-party packages are different.
- A notebook document is distinct from its kernel state.
- Cell execution order can leave stale visible outputs.
- Restart and run all before sharing.
- Record the environment and data; validate the analysis.
- Keep shared reusable logic in modules.

## Sources

- User-supplied course material: *Module X: Tools and Technologies for Data Science, Python as the Language of Data Science*.
- [Python: Using the interpreter](https://docs.python.org/3/tutorial/interpreter.html).
- [NumPy: What is NumPy?](https://numpy.org/doc/stable/user/whatisnumpy.html).
- [Jupyter: The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html).

Worked responses, clarifications, and executable examples were prepared for this repository.

[Module overview](./README.md) · [Theory index](../README.md)
