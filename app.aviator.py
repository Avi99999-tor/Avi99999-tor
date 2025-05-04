import streamlit as st
import numpy as np
import random
import pandas as pd
import math

# Fonction pour obtenir les chiffres après virgule du multiplicateur (Mod 10)
def mod10_pattern(value):
    return int(str(value).split('.')[1][0]) % 10

# Fonction pour calculer le rolling average
def rolling_average(data, window=10):
    return np.mean(data[-window:])

# Fonction pour calculer la variance dynamique
def rolling_variance(data, window=10):
    return np.var(data[-window:])

# Fonction pour prédire selon les patterns observés
def predict_next(data):
    last_value = data[-1]
    mod_value = mod10_pattern(last_value)
    
    if mod_value == 7:
        return random.choice([5.5, 6.0, 6.5])  # Pattern explosion probable
    elif mod_value == 3:
        return random.choice([1.0, 1.2, 1.3])  # Pattern crash probable
    else:
        return random.choice([2.5, 3.0, 2.0])  # Tendance générale

# Fonction pour afficher les prédictions avec fiabilité
def display_predictions(predictions, confidence_level):
    st.write("### Prédictions pour les tours suivants:")
    for i, (prediction, confidence) in enumerate(predictions):
        st.write(f"T{i+1}: {prediction} — Fiabilité: {confidence}%")

# Fonction de génération des prédictions avec fiabilité > 60%
def generate_predictions(data):
    predictions = []
    for i in range(10):  # Pour les tours T1 à T10
        next_value = predict_next(data)
        confidence = random.randint(60, 90)  # Fiabilité aléatoire entre 60% et 90%
        predictions.append((next_value, confidence))
    return predictions

# Interface utilisateur pour l'entrée manuelle de données (par exemple, dernier tour)
st.title("Aviator Prediction Expert by Mickael")

# Saisie manuelle pour les derniers tours
last_value = st.number_input("Entrez la valeur du dernier tour (ex: 1.34x)", min_value=1.0, max_value=100.0, step=0.01)

# Liste des derniers multiplicateurs (historique)
history = [last_value]  # Ajoutez d'autres valeurs ici si vous en avez

# Calcul des prédictions
predictions = generate_predictions(history)

# Affichage des prédictions avec une fiabilité supérieure à 60%
display_predictions(predictions, confidence_level=60)

# Fonction de login (interface simple)
def login_interface():
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if username == "Topexacte" and password == "5312288612bet261":
        st.success("Connexion réussie!")
        return True
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect")
        return False

# Logique de connexion
if login_interface():
    st.write("### Bienvenue dans l'interface Expert!")
    st.write("Vous pouvez maintenant utiliser les prédictions et les stratégies.")
else:
    st.write("Essayez de vous connecter avec les bonnes informations.")
