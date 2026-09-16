FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas==2.1.3 numpy==1.26.0 scikit-learn==1.3.2 mlflow==2.10.2 joblib==1.3.2

COPY datasets/process_data.py /app/
COPY models/train_model.py /app/

CMD ["sh", "-c", "python process_data.py && python train_model.py"]