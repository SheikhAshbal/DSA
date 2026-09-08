# Lab 1 — Setting Up a Reproducible Data Science Environment

Installed Python, created an isolated virtual environment, installed the
core data-science stack, and launched Jupyter.

## Steps
1. Verified Python: `python3 --version`
2. Created & activated venv: `python3 -m venv ds_env && source ds_env/bin/activate`
3. Installed stack: `pip install numpy pandas matplotlib seaborn scikit-learn`
4. Launched Jupyter: `pip install jupyter && jupyter notebook`
5. Exported dependencies: `pip freeze > requirements.txt`

## Reproduce this environment
\`\`\`bash
python3 -m venv ds_env
source ds_env/bin/activate
pip install -r requirements.txt
\`\`\`
