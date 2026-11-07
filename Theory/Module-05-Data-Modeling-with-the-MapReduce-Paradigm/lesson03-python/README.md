# Lesson 3 Python examples

[Lesson notes](../Lesson-03-The-Hadoop-Ecosystem-and-MapReduce-in-Python.md) · [Module overview](../README.md)

Python 3 standard-library examples implementing the Hadoop Streaming text interface. The bundled runner is for small local inputs; it does not start Hadoop.

## Run on Windows or Unix

From this directory:

```text
python run_local.py docs.txt
python run_local.py docs.txt --initial-letter
```

If your interpreter is named python3 or py, use that command instead.

## Files

- [mapper.py](./mapper.py): word TAB 1 for each whitespace-delimited token.
- [initial_mapper.py](./initial_mapper.py): first-character TAB 1 for each token.
- [reducer.py](./reducer.py): sums nonnegative integer values from sorted groups.
- [run_local.py](./run_local.py): executes the real scripts with a local in-memory sort.
- [docs.txt](./docs.txt): seven sample tokens across two lines.

The word totals are data=3, fun=1, is=2, science=1. Starting-character totals are d=3, f=1, i=2, s=1.

For a Unix-pipe version, see the lesson. These examples preserve casing and punctuation; they do not implement language-aware tokenisation. Worker runtime setup and Hadoop submission are outside this local demonstration.
