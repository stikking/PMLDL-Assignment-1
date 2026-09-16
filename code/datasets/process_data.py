import os
import pandas as pd
from sklearn.model_selection import train_test_split

raw_data_path = "data/raw/titanic.csv"
if not os.path.exists(raw_data_path):
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
    df = pd.read_csv(url)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(raw_data_path, index=False)
else:
    df = pd.read_csv(raw_data_path)

df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]]

df["age"] = df["age"].fillna(df["age"].median())
df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])

Q1 = df["fare"].quantile(0.25)
Q3 = df["fare"].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df["fare"] < (Q1 - 1.5 * IQR)) | (df["fare"] > (Q3 + 1.5 * IQR)))]

df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)

X = df.drop(["survived"], axis=1)
y = df["survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

os.makedirs("data/processed", exist_ok=True)
X_train.to_pickle("data/processed/train_X.pkl")
y_train.to_pickle("data/processed/train_y.pkl")
X_test.to_pickle("data/processed/test_X.pkl")
y_test.to_pickle("data/processed/test_y.pkl")
print(f"Stage 1 done. Train: {len(X_train)}, Test: {len(X_test)}")
