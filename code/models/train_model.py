import os
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import mlflow
import mlflow.sklearn

mlflow.set_experiment("Titanic_Pipeline")
os.makedirs("models", exist_ok=True)

X_train = pd.read_pickle("data/processed/train_X.pkl")
y_train = pd.read_pickle("data/processed/train_y.pkl")
X_test = pd.read_pickle("data/processed/test_X.pkl")
y_test = pd.read_pickle("data/processed/test_y.pkl")

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000)),
])

with mlflow.start_run():
    pipeline.fit(X_train, y_train)
    accuracy = pipeline.score(X_test, y_test)
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_param("model", "LogisticRegression")
    mlflow.sklearn.log_model(pipeline, "model")

joblib.dump(pipeline, "models/titanic_pipeline.joblib")
print(f"Stage 2 done. Test accuracy: {accuracy:.4f}")
