## Headline Finding

Party size showed a weak negative association with tip fraction
(correlation: -0.143). Using party size and total bill, linear
regression achieved a test MAE of 0.03899, compared with 0.04064
for a baseline that predicted the training mean.

The improvement was small: average error fell from about 4.06
to 3.90 percentage points. These results suggest limited
predictive value on this test split. They do not establish
causation or necessarily apply to other restaurants.

## How to Run

1. Open a terminal in this project folder.
2. Create a virtual environment:
   `python3 -m venv .venv`
3. Activate the environment:
   `source .venv/bin/activate`
4. Install the versions recorded in requirements.txt:
   `python3 -m pip install -r requirements.txt`
5. Launch JupyterLab:
   `jupyter lab`
6. Open analysis.ipynb.
7. Choose Kernel → Restart Kernel and Run All Cells.
8. Check that every cell finishes without errors and the final
   cell prints "Execution Successful" with the calculated results.

Internet access may be needed when seaborn first loads the
tips dataset.
