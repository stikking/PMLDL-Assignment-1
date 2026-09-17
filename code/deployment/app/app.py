import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("Titanic Survival Predictor")

# Human-readable labels -> values expected by the API
CLASSES = {"1st class": 1, "2nd class": 2, "3rd class": 3}
SEXES = {"Male": "male", "Female": "female"}
PORTS = {"Cherbourg": "C", "Queenstown": "Q", "Southampton": "S"}

with st.form("prediction_form"):
    pclass_label = st.selectbox("Passenger Class", list(CLASSES.keys()))
    sex_label = st.selectbox("Sex", list(SEXES.keys()))
    age = st.number_input("Age", min_value=0.0, max_value=100.0, value=25.0)
    sibsp = st.number_input("Siblings/Spouse aboard", min_value=0, max_value=10, value=0)
    parch = st.number_input("Parents/Children aboard", min_value=0, max_value=10, value=0)
    fare = st.number_input("Fare", min_value=0.0, max_value=1000.0, value=50.0)
    port_label = st.selectbox("Port of Embarkation", list(PORTS.keys()))

    submit = st.form_submit_button("Predict")

if submit:
    payload = {
        "pclass": CLASSES[pclass_label],
        "sex": SEXES[sex_label],
        "age": float(age),
        "sibsp": int(sibsp),
        "parch": int(parch),
        "fare": float(fare),
        "embarked": PORTS[port_label],
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        prediction = response.json()["prediction"]
        st.success(f"Prediction: {'Survived' if prediction == 1 else 'Did not survive'}")
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
