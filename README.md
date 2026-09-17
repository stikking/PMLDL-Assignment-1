@'
# Titanic Survival Prediction Pipeline - PMLDL Assignment 1

Automated MLOps pipeline: data engineering -> model engineering -> deployment.
The entire pipeline (all three stages) runs in Docker containers and is
scheduled automatically every 5 minutes.

## Architecture

1. **Data Engineering** (container: pipeline, code/datasets/process_data.py) —
   downloads Titanic data (if missing), imputes missing values (age, embarked),
   removes outliers (fare, IQR), splits into train/test, saves to data/processed/.
2. **Model Engineering** (container: pipeline, code/models/train_model.py) —
   sklearn Pipeline (StandardScaler + LogisticRegression), logs test accuracy
   and the model to MLflow, saves the model to models/.
3. **Deployment** (containers: api, app) — FastAPI and Streamlit in separate
   Docker containers. The model is mounted into the API container as a
   read-only volume.

docker-compose orchestrates the chain: pipeline runs to completion ->
api starts and waits until healthy -> app starts.

## Repository Structure

    ├── code
    |   ├── datasets/process_data.py
    |   ├── models/train_model.py
    |   ├── pipeline/Dockerfile
    |   └── deployment
    |       ├── api/
    |       ├── app/
    |       └── docker-compose.yml
    ├── data
    |   ├── raw/
    |   └── processed/
    ├── models/
    ├── run_pipeline.ps1
    ├── requirements.txt
    └── README.md

## How to Run

### Prerequisites

- Docker Desktop (with compose). No Python on the host is required.

### One full run

    powershell -ExecutionPolicy Bypass -File .\run_pipeline.ps1

or directly:

    cd code/deployment
    docker compose up -d --build --force-recreate

After it finishes:

- Web app: http://localhost:8501
- API docs (Swagger): http://localhost:8000/docs

The pipeline container exits with code 0 after stages 1-2 — this is expected.

### Schedule (every 5 minutes)

    schtasks /Create /TN "MLPipeline" /TR "powershell -ExecutionPolicy Bypass -File C:\path\to\PMLDL-Assignment-1\run_pipeline.ps1" /SC MINUTE /MO 5 /F

Logs: pipeline.log (timestamped, appended on every run).

### Re-run data+training only

    cd code/deployment
    docker compose run --rm pipeline

## API Usage

    curl -s http://localhost:8000/health
    # {"status":"healthy"}

    curl -s -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
      "pclass": 1, "sex": "female", "age": 30,
      "sibsp": 0, "parch": 0, "fare": 50.0, "embarked": "C"
    }'
    # {"prediction":1}

## MLflow

Metrics and the model are logged on every run (mlruns/ is mounted from the
host, so runs are visible on the host machine):

    mlflow server --backend-store-uri ./mlruns --host 0.0.0.0 --port 5000
    # open http://localhost:5000
'@ | Out-File -FilePath README.md -Encoding utf8
