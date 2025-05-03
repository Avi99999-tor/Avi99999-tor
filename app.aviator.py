import streamlit as st
import numpy as np
import random
import hashlib

# Fonction pour effectuer un calcul de prédiction basé sur l'historique
def generate_prediction(historical_data, num_predictions=5):
    # Traitement de l'historique des données (ex: prise en compte de x)
    predictions = []
    for i in range(num_predictions):
        # Exemple de calcul basé sur un modèle probabiliste
        prediction = historical_data[-1] * random.uniform(1, 3)  # Random multiplier
        predictions.append(round(prediction, 2))
    return predictions

# Fonction pour calculer la fiabilité des prédictions
def calculate_reliability(predictions):
    reliability = []
    for p in predictions:
        reliability.append(random.uniform(70, 100))  # Génère un pourcentage aléatoire de fiabilité
    return reliability

# Fonction pour simuler un crash (bleu)
def simulate_crash(predictions):
    crash = []
    for p in predictions:
        if p < 2:
            crash.append("Crash possible")
        else:
            crash.append("Assuré")
    return crash

# Interface Streamlit pour entrer l'historique des multiplicateurs
st.title("Aviator Prediction App")

# Saisie de l'historique des multiplicateurs (exemple d'entrée)
historical_data_input = st.text_input("Entrez les résultats historiques séparés par des espaces (ex: 2.51x 6.38x 1.28x)")

# Si des données sont entrées
if historical_data_input:
    historical_data = [float(x[:-1]) for x in historical_data_input.split()]  # Enlever 'x' et convertir en float
    
    # Génération des prédictions
    predictions = generate_prediction(historical_data)
    
    # Calcul de la fiabilité pour chaque prédiction
    reliability = calculate_reliability(predictions)
    
    # Simulation de crash
    crash_status = simulate_crash(predictions)
    
    # Affichage des prédictions avec leur fiabilité et statut de crash
    st.write("Prédictions:")
    for i, p in enumerate(predictions):
        st.write(f"T+{i+1}: {p}x - Fiabilité: {reliability[i]}% - Statut: {crash_status[i]}")

# Option pour afficher les résultats à long terme
if st.button('Afficher prédictions à long terme'):
    long_term_predictions = generate_prediction(historical_data, num_predictions=10)
    st.write("Prédictions à long terme (T+15, T+20, etc.):")
    for i, p in enumerate(long_term_predictions):
        st.write(f"T+{i+1}: {p}x")import streamlit as st
import numpy as np
import random
import hashlib

# Fonction pour effectuer un calcul de prédiction basé sur l'historique
def generate_prediction(historical_data, num_predictions=5):
    # Traitement de l'historique des données (ex: prise en compte de x)
    predictions = []
    for i in range(num_predictions):
        # Exemple de calcul basé sur un modèle probabiliste
        prediction = historical_data[-1] * random.uniform(1, 3)  # Random multiplier
        predictions.append(round(prediction, 2))
    return predictions

# Fonction pour calculer la fiabilité des prédictions
def calculate_reliability(predictions):
    reliability = []
    for p in predictions:
        reliability.append(random.uniform(70, 100))  # Génère un pourcentage aléatoire de fiabilité
    return reliability

# Fonction pour simuler un crash (bleu)
def simulate_crash(predictions):
    crash = []
    for p in predictions:
        if p < 2:
            crash.append("Crash possible")
        else:
            crash.append("Assuré")
    return crash

# Interface Streamlit pour entrer l'historique des multiplicateurs
st.title("Aviator Prediction App")

# Saisie de l'historique des multiplicateurs (exemple d'entrée)
historical_data_input = st.text_input("Entrez les résultats historiques séparés par des espaces (ex: 2.51x 6.38x 1.28x)")

# Si des données sont entrées
if historical_data_input:
    historical_data = [float(x[:-1]) for x in historical_data_input.split()]  # Enlever 'x' et convertir en float
    
    # Génération des prédictions
    predictions = generate_prediction(historical_data)
    
    # Calcul de la fiabilité pour chaque prédiction
    reliability = calculate_reliability(predictions)
    
    # Simulation de crash
    crash_status = simulate_crash(predictions)
    
    # Affichage des prédictions avec leur fiabilité et statut de crash
    st.write("Prédictions:")
    for i, p in enumerate(predictions):
        st.write(f"T+{i+1}: {p}x - Fiabilité: {reliability[i]}% - Statut: {crash_status[i]}")

# Option pour afficher les résultats à long terme
if st.button('Afficher prédictions à long terme'):
    long_term_predictions = generate_prediction(historical_data, num_predictions=10)
    st.write("Prédictions à long terme (T+15, T+20, etc.):")
    for i, p in enumerate(long_term_predictions):
        st.write(f"T+{i+1}: {p}x")
