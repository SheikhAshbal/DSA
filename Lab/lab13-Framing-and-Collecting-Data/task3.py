# DATA PROVENANCE
# Dataset: Iris flower dataset.
# Library: scikit-learn, loaded with sklearn.datasets.load_iris().
# Original source: UCI Machine Learning Repository.
# Source URL: https://archive.ics.uci.edu/dataset/53/iris
# Date accessed: 2026-11-06
# License: Creative Commons Attribution 4.0 International (CC BY 4.0).
# Usage terms: Sharing and adaptation are allowed with appropriate
# credit, a link to the license, and an indication of changes.
# License URL: https://creativecommons.org/licenses/by/4.0/
# Attribution: Fisher, R. A. (1936). Iris [Dataset].
# DOI: https://doi.org/10.24432/C56C76
# Version note: scikit-learn corrects two data points compared
# with the UCI version.
from sklearn.datasets import load_iris

iris = load_iris()

columns = list(iris.feature_names) + ["target"]

print("Columns:", columns)
print("Target classes:", iris.target_names.tolist())
