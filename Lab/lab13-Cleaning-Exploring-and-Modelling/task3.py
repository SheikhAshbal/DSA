import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

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

print("Training shape:", Xtr.shape)
print("Testing shape:", Xte.shape)
print("Test R²:", round(model.score(Xte, yte), 3))
