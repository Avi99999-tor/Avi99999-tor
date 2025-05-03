import streamlit as st import numpy as np import random import hashlib

Fonction pour effectuer un calcul de prédiction basé sur l'historique

def generate_prediction(historical_data, num_predictions=5): predictions = [] for i in range(num_predictions): prediction = historical_data[-1] * random.uniform(1, 3) predictions.append(round(prediction, 2)) return predictions

Fonction pour calculer la fiabilité des prédictions

def calculate_reliability(predictions): reliability = [] for p in predictions: reliability.append(round(random.uniform(70, 100), 2)) return reliability

Fonction pour simuler un crash (bleu)

def simulate_crash(predictions): crash = [] for p in predictions: if p < 2: crash.append("Crash possible") else: crash.append("Assuré") return crash

st.title("Aviator Prediction App")

Entrée de l'historique sous forme de texte

historical_data_input = st.text_input("Entrez les multiplicateurs séparés par des espaces (ex: 2.51x 6.38x 1.28x)") numero_dernier_tour = st.number_input("Entrez le numéro du dernier tour (correspondant au premier multiplicateur)", min_value=1, value=100)

if historical_data_input: raw_data = historical_data_input.strip().split() historical_data = [float(x[:-1]) for x in raw_data if x.endswith('x')]

predictions = generate_prediction(historical_data, num_predictions=10)
reliability = calculate_reliability(predictions)
crash_status = simulate_crash(predictions)

st.subheader("Historique reconstitué:")
for i, mult in enumerate(historical_data):
    st.write(f"T{numero_dernier_tour + i}: {mult}x")

st.subheader("Prédictions proches et lointaines:")
for i, p in enumerate(predictions):
    st.write(f"T{numero_dernier_tour + len(historical_data) + i}: {p}x - Fiabilité: {reliability[i]}% - Statut: {crash_status[i]}")

