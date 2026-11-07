"""Dynamic typing and notebook execution-order demonstrations."""
from contextlib import redirect_stdout
from io import StringIO
import math
from numbers import Real
import pandas as pd

def average(values):
    """Original lesson example: input assumptions are unchecked."""
    return sum(values) / len(values)

def validated_average(values):
    """Accept a non-empty iterable of finite real numbers, excluding bools."""
    values = list(values)
    if not values:
        raise ValueError("values must not be empty")
    if any(isinstance(v, bool) or not isinstance(v, Real) for v in values):
        raise TypeError("values must contain real numbers, excluding bools")
    if not all(math.isfinite(v) for v in values):
        raise ValueError("values must be finite")
    result = math.fsum(values) / len(values)
    if not math.isfinite(result):
        raise ValueError("average must be finite")
    return result

# These strings represent the four cells in their displayed A–B–C–D order.
CELLS = {
    "A": "df = pd.DataFrame({'PatientID': [1,2,3,4,5], 'age': [16,18,19,25,40]})",
    "B": "df = df[df.age > 18]",
    "C": "print(df.shape)",
    "D": "print(df.shape)",
}

def trace(order):
    """Use a fresh namespace for each simulated kernel execution history."""
    namespace = {"pd": pd}
    outputs = {}
    for label in order:
        capture = StringIO()
        with redirect_stdout(capture):
            exec(CELLS[label], namespace)
        if capture.getvalue():
            outputs[label] = capture.getvalue().strip()
    return outputs

def main():
    print("average([2,4,6]):", average([2,4,6]))
    try:
        average([2,4,"6"])
    except TypeError as error:
        print("runtime error:", error)
    print("validated average:", validated_average([2,4,6]))
    print("Historical A,C,B,D:", trace("ACBD"))
    print("Fresh linear A,B,C,D:", trace("ABCD"))
    print("Note: age > 18 excludes age 18.")

if __name__ == "__main__":
    main()
