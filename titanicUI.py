import streamlit as st
import math
import pickle

# Load the model with error handling
try:
    with open("model.pkl", 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Error: The model file 'model.pkl' was not found.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Header
st.title("🚢 Titanic Survival Prediction")

# Input Fields
st.header("Provide Passenger Details")
col1, col2, col3 = st.columns(3)

with col1:
    Pclass = st.selectbox("Class of Passenger", ["Premiere", "Executive", "Economy"])
with col2:
    Sex = st.selectbox("Gender", ["Male", "Female"])
with col3:
    Age = st.number_input("Age of passenger", min_value=0, max_value=120, step=1)

col4, col5 = st.columns(2)
with col4:
    SibSp = st.number_input("Number of Siblings/Spouses Aboard", min_value=0, step=1)
with col5:
    Parch = st.number_input("Number of Parents/Children Aboard", min_value=0, step=1)

col7, col8 = st.columns(2)
with col7:
    Fare = st.number_input("Fare of Journey", min_value=0.0, step=0.1)
with col8:
    Embarked = st.selectbox("Port of Embarkation", ["Cherbourg", "Queenstown", "Southampton"])

# Prediction Logic
if st.button("Predict"):
    try:
        # Map inputs to model features
        pclass = 1 if Pclass == "Premiere" else (2 if Pclass == "Executive" else 3)
        gender = 1 if Sex == "Female" else 0
        embarked = {"Cherbourg": 1, "Queenstown": 2, "Southampton": 0}.get(Embarked, 0)
        
        # Prepare input for model
        features = [pclass, gender, math.ceil(Age), math.ceil(SibSp), math.ceil(Parch), math.ceil(Fare), embarked]
        
        # Perform prediction
        result = model.predict([features])[0]
        output_labels = {1: "The passenger will Survive", 0: "The passenger will not survive"}
        st.success(f"### {output_labels[result]}")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")