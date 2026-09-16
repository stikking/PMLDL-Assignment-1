import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("Titanic Survival Predictor")

with st.form("prediction_form"):
    pclass = st.selectbox("Passenger Class", [1, 2, 3])
    sex = st.selectbox("Sex", ["male", "female"])
    age = st.number_input("Age", min_value=0.0, max_value=100.0, value=25.0)
    sibsp = st.number_input("Siblings/Spouse aboard", min_value=0, max_value=10, value=0)
    parch = st.number_input("Parents/Children aboard", min_value=0, max_value=10, value=0)
    fare = st.number_input("Fare", min_value=0.0, max_value=1000.0, value=50.0)
    embarked = st.selectbox("Port of Embarkation", ["C", "Q", "S"])

    submit = st.form_submit_button("Predict")

if submit:
    payload = {
        "pclass": int(pclass),
        "sex": sex,
        "age": float(age),
        "sibsp": int(sibsp),
        "parch": int(parch),
        "fare": float(fare),
        "embarked": embarked,
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        prediction = response.json()["prediction"]
        st.success(f"Prediction: {'Survived' if prediction == 1 else 'Did not survive'}")
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
