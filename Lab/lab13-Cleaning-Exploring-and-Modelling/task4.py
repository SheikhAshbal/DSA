import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error

df = sns.load_dataset("tips")
df = df.dropna().drop_duplicates().copy()
df = df[df["total_bill"] > 0].copy()
df["tip_pct"] = df["tip"] / df["total_bill"]

X = df[["size", "total_bill"]]
y = df["tip_pct"]

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
model.fit(Xtr, ytr)
model_predictions = model.predict(Xte)

baseline = DummyRegressor(strategy="mean")
baseline.fit(Xtr, ytr)
baseline_predictions = baseline.predict(Xte)

print(
    "Linear regression MAE:",
    round(mean_absolute_error(yte, model_predictions), 5)
)
print(
    "Mean baseline MAE:",
    round(mean_absolute_error(yte, baseline_predictions), 5)
)
